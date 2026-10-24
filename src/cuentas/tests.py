"""Pruebas de la cuenta administradora (RF-27, RN-25, CA-68, CA-69, actualización zzb).

Necesitan PostgreSQL (restricción de la tabla, bloqueo de fila).
"""
import time
from io import StringIO
from datetime import datetime, timedelta, timezone as utc
from unittest.mock import patch

import pyotp
from cryptography.fernet import Fernet
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, transaction
from django.test import TestCase, override_settings

from . import autenticacion, cifrado, views
from .autenticacion import Resultado
from .models import Administrador, CodigoRecuperacion

CLAVE_A = Fernet.generate_key().decode()
CLAVE_B = Fernet.generate_key().decode()
CONTRASENA = 'una contrasena de prueba larga'
AHORA = datetime(2026, 10, 23, 12, 0, 0, tzinfo=utc.utc)


def codigo_en(secreto, momento, desfase=0):
    """Código TOTP del momento desplazado `desfase` segundos (±30 = un intervalo)."""
    return pyotp.TOTP(secreto).at(int(momento.timestamp()) + desfase)


@override_settings(CLAVES_CIFRADO=[CLAVE_A])
class CuentaTestCase(TestCase):
    def setUp(self):
        self.secreto = pyotp.random_base32()
        self.admin = Administrador.objects.crear_administrador('admin', CONTRASENA)
        self.admin.fijar_secreto_segundo_factor(self.secreto)
        self.admin.segundo_factor_activo = True
        self.admin.save()


class ModeloTests(CuentaTestCase):
    def test_solo_cabe_una_cuenta(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Administrador.objects.crear_administrador('otro', CONTRASENA)
        self.assertEqual(Administrador.objects.count(), 1)

    def test_la_restriccion_esta_en_la_base_y_no_solo_en_el_gestor(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Administrador.objects.create(id=2, usuario='otro')

    def test_contrasena_con_argon2id(self):
        self.assertTrue(self.admin.password.startswith('argon2$argon2id$'))
        self.assertTrue(self.admin.check_password(CONTRASENA))
        self.assertNotIn(CONTRASENA, self.admin.password)

    def test_el_gestor_no_crea_usuarios_ni_superusuarios(self):
        with self.assertRaises(NotImplementedError):
            Administrador.objects.create_superuser('x', 'y')
        with self.assertRaises(NotImplementedError):
            Administrador.objects.create_user('x', 'y')


class CifradoTests(CuentaTestCase):
    def test_el_secreto_no_se_guarda_en_claro(self):
        guardado = Administrador.objects.values_list('secreto_segundo_factor', flat=True).get()
        self.assertNotEqual(guardado, self.secreto)
        self.assertNotIn(self.secreto, guardado)
        self.assertEqual(self.admin.secreto_segundo_factor_en_claro(), self.secreto)

    def test_rotacion_de_clave(self):
        token_viejo = self.admin.secreto_segundo_factor
        with override_settings(CLAVES_CIFRADO=[CLAVE_B, CLAVE_A]):
            # Con la clave nueva primero se sigue descifrando lo cifrado con la anterior...
            self.assertEqual(cifrado.descifrar(token_viejo), self.secreto)
            token_nuevo = cifrado.recifrar(token_viejo)
        # ...y tras rotar, la clave anterior ya no hace falta.
        with override_settings(CLAVES_CIFRADO=[CLAVE_B]):
            self.assertEqual(cifrado.descifrar(token_nuevo), self.secreto)
        with override_settings(CLAVES_CIFRADO=[CLAVE_B]):
            with self.assertRaises(Exception):
                cifrado.descifrar(token_viejo)

    def test_sin_clave_no_se_cifra(self):
        from django.core.exceptions import ImproperlyConfigured
        with override_settings(CLAVES_CIFRADO=[]):
            with self.assertRaises(ImproperlyConfigured):
                cifrado.cifrar('x')


class TotpTests(CuentaTestCase):
    def test_codigo_del_intervalo_actual_se_acepta(self):
        r = autenticacion.verificar_totp(self.admin.pk, codigo_en(self.secreto, AHORA), ahora=AHORA)
        self.assertEqual(r.resultado, Resultado.CORRECTO)

    def test_un_codigo_ya_aceptado_no_se_repite(self):
        codigo = codigo_en(self.secreto, AHORA)
        autenticacion.verificar_totp(self.admin.pk, codigo, ahora=AHORA)
        r = autenticacion.verificar_totp(self.admin.pk, codigo, ahora=AHORA + timedelta(seconds=5))
        self.assertEqual(r.resultado, Resultado.INCORRECTO)

    def test_se_tolera_un_intervalo_anterior_y_uno_posterior(self):
        anterior = codigo_en(self.secreto, AHORA, desfase=-30)
        r = autenticacion.verificar_totp(self.admin.pk, anterior, ahora=AHORA)
        self.assertEqual(r.resultado, Resultado.CORRECTO)
        otro = Administrador.objects.get(pk=1)
        otro.ultimo_intervalo_totp = None
        otro.save()
        posterior = codigo_en(self.secreto, AHORA, desfase=30)
        r = autenticacion.verificar_totp(self.admin.pk, posterior, ahora=AHORA)
        self.assertEqual(r.resultado, Resultado.CORRECTO)

    def test_dos_intervalos_de_diferencia_no_se_aceptan(self):
        r = autenticacion.verificar_totp(self.admin.pk, codigo_en(self.secreto, AHORA, desfase=-60), ahora=AHORA)
        self.assertEqual(r.resultado, Resultado.INCORRECTO)
        r = autenticacion.verificar_totp(self.admin.pk, codigo_en(self.secreto, AHORA, desfase=60), ahora=AHORA)
        self.assertEqual(r.resultado, Resultado.INCORRECTO)

    def test_un_codigo_de_un_intervalo_anterior_al_ultimo_aceptado_se_rechaza(self):
        autenticacion.verificar_totp(self.admin.pk, codigo_en(self.secreto, AHORA), ahora=AHORA)
        r = autenticacion.verificar_totp(
            self.admin.pk, codigo_en(self.secreto, AHORA, desfase=-30), ahora=AHORA)
        self.assertEqual(r.resultado, Resultado.INCORRECTO)

    def test_codigo_incorrecto_o_vacio(self):
        for codigo in ('000000', '', None, 'abcdef'):
            r = autenticacion.verificar_totp(self.admin.pk, codigo, ahora=AHORA)
            self.assertEqual(r.resultado, Resultado.INCORRECTO)

    def test_sin_secreto_registrado_no_hay_acceso(self):
        self.admin.secreto_segundo_factor = ''
        self.admin.save()
        r = autenticacion.verificar_totp(self.admin.pk, '123456', ahora=AHORA)
        self.assertEqual(r.resultado, Resultado.INCORRECTO)


class LimiteDeIntentosTests(CuentaTestCase):
    def test_las_esperas_de_la_regla(self):
        esperadas = {0: 0, 4: 0, 5: 60, 6: 120, 7: 240, 8: 480, 9: 960, 10: 1920, 11: 3600, 12: 3600, 30: 3600}
        for fallos, segundos in esperadas.items():
            self.assertEqual(autenticacion.segundos_de_espera(fallos), segundos, fallos)

    def test_cinco_fallos_inician_la_espera_de_un_minuto(self):
        for i in range(4):
            r = autenticacion.comprobar_contrasena('admin', 'mal', ahora=AHORA + timedelta(seconds=i))
            self.assertFalse(r.aviso_cinco_fallos)
        r = autenticacion.comprobar_contrasena('admin', 'mal', ahora=AHORA + timedelta(seconds=4))
        self.assertTrue(r.aviso_cinco_fallos)
        self.assertEqual(r.espera_hasta, AHORA + timedelta(seconds=4 + 60))

    def test_el_aviso_de_cinco_fallos_se_da_una_sola_vez(self):
        avisos = []
        momento = AHORA
        for i in range(8):
            momento += timedelta(hours=2)
            avisos.append(autenticacion.comprobar_contrasena('admin', 'mal', ahora=momento).aviso_cinco_fallos)
        self.assertEqual(avisos.count(True), 1)

    def test_durante_la_espera_se_rechaza_sin_sumar_fallos(self):
        for i in range(5):
            autenticacion.comprobar_contrasena('admin', 'mal', ahora=AHORA)
        r = autenticacion.comprobar_contrasena('admin', CONTRASENA, ahora=AHORA + timedelta(seconds=30))
        self.assertEqual(r.resultado, Resultado.EN_ESPERA)
        r = autenticacion.verificar_totp(
            self.admin.pk, codigo_en(self.secreto, AHORA), ahora=AHORA + timedelta(seconds=30))
        self.assertEqual(r.resultado, Resultado.EN_ESPERA)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.fallos_consecutivos, 5)

    def test_pasada_la_espera_se_puede_intentar_y_un_fallo_duplica_la_espera(self):
        for i in range(5):
            autenticacion.comprobar_contrasena('admin', 'mal', ahora=AHORA)
        despues = AHORA + timedelta(seconds=61)
        r = autenticacion.comprobar_contrasena('admin', 'mal', ahora=despues)
        self.assertEqual(r.resultado, Resultado.INCORRECTO)
        self.assertEqual(r.espera_hasta, despues + timedelta(seconds=120))

    def test_el_tope_es_una_hora_y_no_hay_bloqueo_permanente(self):
        momento = AHORA
        for i in range(20):
            momento += timedelta(hours=2)
            autenticacion.comprobar_contrasena('admin', 'mal', ahora=momento)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.espera_hasta, momento + timedelta(seconds=3600))
        r = autenticacion.comprobar_contrasena('admin', CONTRASENA, ahora=momento + timedelta(hours=1, seconds=1))
        self.assertEqual(r.resultado, Resultado.CORRECTO)

    def test_los_fallos_de_contrasena_y_de_totp_comparten_el_contador(self):
        for i in range(3):
            autenticacion.comprobar_contrasena('admin', 'mal', ahora=AHORA)
        for i in range(2):
            autenticacion.verificar_totp(self.admin.pk, '000000', ahora=AHORA)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.fallos_consecutivos, 5)
        self.assertIsNotNone(self.admin.espera_hasta)

    def test_una_contrasena_correcta_no_reinicia_el_contador_pero_el_totp_si(self):
        for i in range(3):
            autenticacion.comprobar_contrasena('admin', 'mal', ahora=AHORA)
        autenticacion.comprobar_contrasena('admin', CONTRASENA, ahora=AHORA)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.fallos_consecutivos, 3)
        autenticacion.verificar_totp(self.admin.pk, codigo_en(self.secreto, AHORA), ahora=AHORA)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.fallos_consecutivos, 0)
        self.assertIsNone(self.admin.espera_hasta)

    def test_un_usuario_inexistente_no_toca_la_cuenta(self):
        r = autenticacion.comprobar_contrasena('nadie', 'mal', ahora=AHORA)
        self.assertEqual(r.resultado, Resultado.INCORRECTO)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.fallos_consecutivos, 0)


class BackendTests(CuentaTestCase):
    def test_contrasena_correcta_devuelve_la_cuenta(self):
        self.assertEqual(authenticate(usuario='admin', contrasena=CONTRASENA), self.admin)

    def test_contrasena_incorrecta_o_usuario_inexistente_devuelve_none(self):
        self.assertIsNone(authenticate(usuario='admin', contrasena='mal'))
        self.assertIsNone(authenticate(usuario='nadie', contrasena=CONTRASENA))

    def test_el_backend_no_concede_permisos(self):
        self.assertFalse(hasattr(self.admin, 'has_perm'))
        self.assertFalse(hasattr(self.admin, 'is_staff'))


class CodigosRecuperacionTests(CuentaTestCase):
    def test_emite_diez_codigos_distintos_y_solo_guarda_hashes(self):
        codigos = autenticacion.emitir_codigos_recuperacion(self.admin, CONTRASENA)
        self.assertEqual(len(codigos), 10)
        self.assertEqual(len(set(codigos)), 10)
        guardados = list(CodigoRecuperacion.objects.values_list('hash_codigo', flat=True))
        self.assertEqual(len(guardados), 10)
        for c in codigos:
            self.assertNotIn(c, guardados)
            self.assertNotIn(c.replace('-', ''), guardados)

    def test_emitir_exige_la_contrasena_actual(self):
        self.assertIsNone(autenticacion.emitir_codigos_recuperacion(self.admin, 'mal'))
        self.assertEqual(CodigoRecuperacion.objects.count(), 0)

    def test_un_codigo_sirve_una_sola_vez(self):
        codigo = autenticacion.emitir_codigos_recuperacion(self.admin, CONTRASENA)[0]
        r = autenticacion.verificar_codigo_recuperacion(self.admin.pk, codigo, ahora=AHORA)
        self.assertEqual(r.resultado, Resultado.CORRECTO)
        r = autenticacion.verificar_codigo_recuperacion(self.admin.pk, codigo, ahora=AHORA)
        self.assertEqual(r.resultado, Resultado.INCORRECTO)

    def test_acepta_minusculas_y_sin_guion(self):
        codigo = autenticacion.emitir_codigos_recuperacion(self.admin, CONTRASENA)[0]
        r = autenticacion.verificar_codigo_recuperacion(
            self.admin.pk, codigo.lower().replace('-', ' '), ahora=AHORA)
        self.assertEqual(r.resultado, Resultado.CORRECTO)

    def test_emitir_de_nuevo_invalida_los_anteriores(self):
        viejos = autenticacion.emitir_codigos_recuperacion(self.admin, CONTRASENA)
        nuevos = autenticacion.emitir_codigos_recuperacion(self.admin, CONTRASENA)
        self.assertEqual(CodigoRecuperacion.objects.count(), 10)
        r = autenticacion.verificar_codigo_recuperacion(self.admin.pk, viejos[0], ahora=AHORA)
        self.assertEqual(r.resultado, Resultado.INCORRECTO)
        r = autenticacion.verificar_codigo_recuperacion(self.admin.pk, nuevos[0], ahora=AHORA)
        self.assertEqual(r.resultado, Resultado.CORRECTO)

    def test_comparten_el_contador_de_fallos_y_la_espera(self):
        codigo = autenticacion.emitir_codigos_recuperacion(self.admin, CONTRASENA)[0]
        for _ in range(5):
            r = autenticacion.verificar_codigo_recuperacion(self.admin.pk, 'AAAAA-AAAAA', ahora=AHORA)
        self.assertTrue(r.aviso_cinco_fallos)
        r = autenticacion.verificar_codigo_recuperacion(
            self.admin.pk, codigo, ahora=AHORA + timedelta(seconds=10))
        self.assertEqual(r.resultado, Resultado.EN_ESPERA)
        r = autenticacion.verificar_codigo_recuperacion(
            self.admin.pk, codigo, ahora=AHORA + timedelta(seconds=61))
        self.assertEqual(r.resultado, Resultado.CORRECTO)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.fallos_consecutivos, 0)


class InicioDeSesionTests(CuentaTestCase):
    def primer_paso(self, contrasena=CONTRASENA):
        return self.client.post('/entrar/', {'usuario': 'admin', 'contrasena': contrasena})

    def codigo_actual(self):
        return pyotp.TOTP(self.secreto).now()

    def segundo_paso(self, codigo):
        return self.client.post('/entrar/codigo/', {'codigo': codigo})

    def test_la_pagina_protegida_exige_iniciar_sesion(self):
        r = self.client.get('/')
        self.assertRedirects(r, '/entrar/?next=/', fetch_redirect_response=False)

    def test_la_contrasena_sola_no_inicia_sesion(self):
        r = self.primer_paso()
        self.assertRedirects(r, '/entrar/codigo/', fetch_redirect_response=False)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.get('/').status_code, 302)

    def test_el_segundo_paso_sin_primer_paso_vuelve_al_inicio(self):
        r = self.client.get('/entrar/codigo/')
        self.assertRedirects(r, '/entrar/', fetch_redirect_response=False)
        r = self.segundo_paso(self.codigo_actual())
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_contrasena_y_totp_inician_sesion_y_cerrar_la_termina(self):
        self.primer_paso()
        r = self.segundo_paso(self.codigo_actual())
        self.assertRedirects(r, '/', fetch_redirect_response=False)
        self.assertEqual(self.client.get('/').status_code, 200)
        self.client.post('/salir/')
        self.assertEqual(self.client.get('/').status_code, 302)

    def test_contrasena_y_codigo_de_recuperacion_inician_sesion(self):
        codigo = autenticacion.emitir_codigos_recuperacion(self.admin, CONTRASENA)[0]
        self.primer_paso()
        self.segundo_paso(codigo)
        self.assertEqual(self.client.get('/').status_code, 200)

    def test_totp_incorrecto_no_inicia_sesion(self):
        self.primer_paso()
        r = self.segundo_paso('000000')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.client.get('/').status_code, 302)

    def test_contrasena_incorrecta_da_el_mismo_mensaje_que_usuario_inexistente(self):
        a = self.client.post('/entrar/', {'usuario': 'admin', 'contrasena': 'mal'})
        b = self.client.post('/entrar/', {'usuario': 'nadie', 'contrasena': 'mal'})
        self.assertContains(a, views.MENSAJE_PRIMER_PASO)
        self.assertContains(b, views.MENSAJE_PRIMER_PASO)

    def test_sin_segundo_factor_activo_no_hay_acceso(self):
        self.admin.segundo_factor_activo = False
        self.admin.save()
        r = self.primer_paso()
        self.assertEqual(r.status_code, 200)
        self.assertNotIn('primer_paso_administrador', self.client.session)

    def test_el_primer_paso_caduca(self):
        self.primer_paso()
        with patch('cuentas.views.time.time', return_value=time.time() + 6 * 60):
            r = self.segundo_paso(self.codigo_actual())
        self.assertRedirects(r, '/entrar/', fetch_redirect_response=False)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_los_fallos_del_segundo_paso_cuentan_y_producen_espera(self):
        self.primer_paso()
        for _ in range(5):
            self.segundo_paso('000000')
        r = self.segundo_paso(self.codigo_actual())
        self.assertContains(r, 'Espere')
        self.assertNotIn('_auth_user_id', self.client.session)

    def iniciar(self):
        self.primer_paso()
        self.segundo_paso(self.codigo_actual())

    def test_una_hora_de_inactividad_cierra_la_sesion(self):
        self.iniciar()
        with patch('cuentas.middleware.time.time', return_value=time.time() + 3601):
            self.assertEqual(self.client.get('/').status_code, 302)
        self.assertEqual(self.client.get('/').status_code, 302)

    def test_la_actividad_mantiene_la_sesion_pero_a_las_24_horas_se_cierra(self):
        self.iniciar()
        inicio = time.time()
        for horas in range(1, 24):
            with patch('cuentas.middleware.time.time', return_value=inicio + horas * 3000):
                if horas * 3000 > 24 * 3600:
                    break
                self.assertEqual(self.client.get('/').status_code, 200, horas)
        with patch('cuentas.middleware.time.time', return_value=inicio + 24 * 3600 + 1):
            self.assertEqual(self.client.get('/').status_code, 302)

    def test_una_sesion_sin_marcas_de_tiempo_se_cierra(self):
        self.iniciar()
        sesion = self.client.session
        del sesion['sesion_inicio']
        sesion.save()
        self.assertEqual(self.client.get('/').status_code, 302)


class ComandosTests(TestCase):
    def llamar(self, nombre, *args, contrasenas=(), **opciones):
        salida = StringIO()
        with patch('cuentas.management.commands.crear_administrador.getpass', side_effect=list(contrasenas)):
            call_command(nombre, *args, stdout=salida, stderr=StringIO(), **opciones)
        return salida.getvalue()

    def test_crear_administrador(self):
        self.llamar('crear_administrador', usuario='admin', contrasenas=[CONTRASENA, CONTRASENA])
        a = Administrador.objects.get()
        self.assertTrue(a.check_password(CONTRASENA))
        self.assertFalse(a.segundo_factor_activo)

    def test_crear_rechaza_contrasena_corta_o_distinta_o_segunda_cuenta(self):
        with self.assertRaises(CommandError):
            self.llamar('crear_administrador', usuario='admin', contrasenas=['corta', 'corta'])
        with self.assertRaises(CommandError):
            self.llamar('crear_administrador', usuario='admin', contrasenas=[CONTRASENA, CONTRASENA + 'x'])
        self.assertEqual(Administrador.objects.count(), 0)
        self.llamar('crear_administrador', usuario='admin', contrasenas=[CONTRASENA, CONTRASENA])
        with self.assertRaises(CommandError):
            self.llamar('crear_administrador', usuario='otro', contrasenas=[CONTRASENA, CONTRASENA])

    @override_settings(CLAVES_CIFRADO=[CLAVE_A])
    def test_rescate_desactiva_el_segundo_factor_y_cierra_sesiones(self):
        a = Administrador.objects.crear_administrador('admin', CONTRASENA)
        a.fijar_secreto_segundo_factor(pyotp.random_base32())
        a.segundo_factor_activo = True
        a.fallos_consecutivos = 7
        a.ultimo_intervalo_totp = 5
        a.save()
        autenticacion.emitir_codigos_recuperacion(a, CONTRASENA)
        self.client.force_login(a, backend='cuentas.backends.BackendAdministrador')
        self.assertEqual(Session.objects.count(), 1)
        self.llamar('rescatar_segundo_factor', confirmar=True)
        a.refresh_from_db()
        self.assertFalse(a.segundo_factor_activo)
        self.assertEqual((a.secreto_segundo_factor, a.fallos_consecutivos, a.ultimo_intervalo_totp), ('', 0, None))
        self.assertEqual(CodigoRecuperacion.objects.count(), 0)
        self.assertEqual(Session.objects.count(), 0)
        self.assertTrue(a.check_password(CONTRASENA))

    def test_rescate_pide_confirmacion(self):
        Administrador.objects.crear_administrador('admin', CONTRASENA)
        with patch('builtins.input', return_value='no'), self.assertRaises(CommandError):
            self.llamar('rescatar_segundo_factor')

    def test_rescate_sin_cuenta(self):
        with self.assertRaises(CommandError):
            self.llamar('rescatar_segundo_factor', confirmar=True)
