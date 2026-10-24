"""Pruebas de la cuenta administradora (RF-27, RN-25, CA-68, CA-69, actualización zzb).

Necesitan PostgreSQL (restricción de la tabla, bloqueo de fila).
"""
from datetime import datetime, timedelta, timezone as utc

import pyotp
from cryptography.fernet import Fernet
from django.contrib.auth import authenticate
from django.db import IntegrityError, transaction
from django.test import TestCase, override_settings

from . import autenticacion, cifrado
from .autenticacion import Resultado
from .models import Administrador

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
