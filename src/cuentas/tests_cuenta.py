"""Pendientes pequeños de la E0 (actualización 2026-10-24l): códigos nuevos desde la sesión,
concurrencia del contador, acceso denegado en todas las vistas, CSRF y que los registros no lleven
secretos. Necesitan PostgreSQL."""
import logging
import re
import threading
from datetime import datetime, timezone as utc

import pyotp
from django.db import connection
from django.test import Client, TestCase, TransactionTestCase, override_settings
from django.urls import URLPattern, URLResolver, get_resolver, reverse

from nucleo.models import Auditoria

from . import autenticacion
from .autenticacion import Resultado
from .models import Administrador, CodigoRecuperacion
from .tests import CLAVE_A, CONTRASENA

AHORA = datetime(2026, 10, 24, 12, 0, 0, tzinfo=utc.utc)


def cuenta_con_segundo_factor():
    secreto = pyotp.random_base32()
    admin = Administrador.objects.crear_administrador('admin', CONTRASENA)
    admin.fijar_secreto_segundo_factor(secreto)
    admin.segundo_factor_activo = True
    admin.save()
    return admin, secreto


def iniciar_sesion(cliente, secreto, codigo=None):
    Administrador.objects.update(ultimo_intervalo_totp=None)
    cliente.post('/entrar/', {'usuario': 'admin', 'contrasena': CONTRASENA})
    cliente.post('/entrar/codigo/', {'codigo': codigo or pyotp.TOTP(secreto).now()})


@override_settings(CLAVES_CIFRADO=[CLAVE_A])
class CodigosNuevosTests(TestCase):
    def setUp(self):
        self.admin, self.secreto = cuenta_con_segundo_factor()
        self.viejos = autenticacion.emitir_codigos_recuperacion(self.admin, CONTRASENA)
        iniciar_sesion(self.client, self.secreto)

    def test_exige_sesion(self):
        self.assertRedirects(Client().get('/cuenta/codigos/'), '/entrar/?next=/cuenta/codigos/', fetch_redirect_response=False)
        self.assertEqual(Client().post('/cuenta/codigos/', {'contrasena': CONTRASENA}).status_code, 302)

    def test_la_contrasena_actual_genera_diez_codigos_e_invalida_los_anteriores(self):
        r = self.client.post('/cuenta/codigos/', {'contrasena': CONTRASENA})
        nuevos = re.findall(r'<code>([A-Z2-9]{5}-[A-Z2-9]{5})</code>', r.content.decode())
        self.assertEqual(len(nuevos), 10)
        self.assertFalse(set(nuevos) & set(self.viejos))
        self.assertEqual(CodigoRecuperacion.objects.count(), 10)
        self.assertIn('no-store', r['Cache-Control'])
        self.client.post('/salir/')
        self.client.post('/entrar/', {'usuario': 'admin', 'contrasena': CONTRASENA})
        self.client.post('/entrar/codigo/', {'codigo': self.viejos[0]})
        self.assertEqual(self.client.get('/').status_code, 302)  # un código viejo ya no sirve
        self.client.post('/entrar/codigo/', {'codigo': nuevos[0]})
        self.assertEqual(self.client.get('/').status_code, 200)

    def test_con_la_contrasena_equivocada_no_se_emite_nada_y_cuenta_como_fallo(self):
        r = self.client.post('/cuenta/codigos/', {'contrasena': 'mal'})
        self.assertContains(r, 'Contraseña incorrecta')
        self.assertEqual(CodigoRecuperacion.objects.count(), 10)
        self.assertTrue(autenticacion.codigo_disponible(self.admin, self.viejos[0]))
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.fallos_consecutivos, 1)
        self.assertEqual(Auditoria.objects.filter(accion='inicio_sesion_fallido').count(), 1)

    def test_cinco_fallos_producen_espera_y_no_se_emite_aunque_acierte_despues(self):
        for _ in range(5):
            self.client.post('/cuenta/codigos/', {'contrasena': 'mal'})
        r = self.client.post('/cuenta/codigos/', {'contrasena': CONTRASENA})
        self.assertContains(r, 'Espere')
        self.assertTrue(autenticacion.codigo_disponible(self.admin, self.viejos[0]))
        self.assertEqual(Auditoria.objects.filter(accion='cinco_fallos_seguidos').count(), 1)

    def test_deja_el_aviso_de_seguridad_en_la_auditoria_y_en_la_pantalla_de_inicio(self):
        self.client.post('/cuenta/codigos/', {'contrasena': CONTRASENA})
        self.assertEqual(Auditoria.objects.filter(accion='codigos_emitidos').count(), 1)
        self.client.post('/salir/')
        iniciar_sesion(self.client, self.secreto)
        self.assertContains(self.client.get('/'), 'codigos_emitidos')

    def test_la_pantalla_no_guarda_codigos_ni_contrasena_en_la_auditoria(self):
        r = self.client.post('/cuenta/codigos/', {'contrasena': CONTRASENA})
        nuevos = re.findall(r'<code>([A-Z2-9]{5}-[A-Z2-9]{5})</code>', r.content.decode())
        todo = str(list(Auditoria.objects.values()))
        self.assertNotIn(CONTRASENA, todo)
        for codigo in nuevos + self.viejos:
            self.assertNotIn(codigo, todo)

    def test_recargar_la_pagina_no_vuelve_a_mostrar_los_codigos(self):
        self.client.post('/cuenta/codigos/', {'contrasena': CONTRASENA})
        r = self.client.get('/cuenta/codigos/')
        self.assertNotContains(r, '<code>')
        self.assertContains(r, 'name="contrasena"')


@override_settings(CLAVES_CIFRADO=[CLAVE_A])
class ConcurrenciaTests(TransactionTestCase):
    """El bloqueo de fila del contador (select_for_update) con conexiones reales en paralelo."""
    serialized_rollback = True

    def paralelo(self, tarea, hilos):
        resultados, errores = [], []
        barrera = threading.Barrier(hilos)

        def correr(i):
            try:
                barrera.wait(timeout=10)
                resultados.append(tarea(i))
            except Exception as e:  # pragma: no cover - solo si falla la prueba
                errores.append(e)
            finally:
                connection.close()

        trabajos = [threading.Thread(target=correr, args=(i,)) for i in range(hilos)]
        for t in trabajos:
            t.start()
        for t in trabajos:
            t.join(timeout=30)
        self.assertEqual(errores, [])
        return resultados

    def test_ocho_fallos_simultaneos_cuentan_exactamente_cinco_y_un_solo_aviso(self):
        cuenta_con_segundo_factor()
        resultados = self.paralelo(lambda i: autenticacion.comprobar_contrasena('admin', 'mal', ahora=AHORA), 8)
        self.assertEqual(Administrador.objects.get().fallos_consecutivos, 5)
        self.assertEqual(sum(r.aviso_cinco_fallos for r in resultados), 1)
        self.assertEqual(sum(r.resultado is Resultado.EN_ESPERA for r in resultados), 3)

    def test_un_codigo_totp_valido_enviado_dos_veces_a_la_vez_solo_se_acepta_una(self):
        admin, secreto = cuenta_con_segundo_factor()
        codigo = pyotp.TOTP(secreto).at(int(AHORA.timestamp()))
        resultados = self.paralelo(lambda i: autenticacion.verificar_totp(admin.pk, codigo, ahora=AHORA), 4)
        self.assertEqual(sum(r.correcto for r in resultados), 1)

    def test_un_codigo_de_recuperacion_enviado_a_la_vez_solo_sirve_una_vez(self):
        admin, _ = cuenta_con_segundo_factor()
        codigo = autenticacion.emitir_codigos_recuperacion(admin, CONTRASENA)[0]
        resultados = self.paralelo(lambda i: autenticacion.verificar_codigo_recuperacion(admin.pk, codigo, ahora=AHORA), 4)
        self.assertEqual(sum(r.correcto for r in resultados), 1)


def _rutas(patrones, prefijo='', espacio=''):
    for p in patrones:
        if isinstance(p, URLResolver):
            yield from _rutas(p.url_patterns, prefijo + str(p.pattern), p.namespace or espacio)
        elif isinstance(p, URLPattern) and p.name:
            yield (f'{espacio}:{p.name}' if espacio else p.name), prefijo + str(p.pattern)


# Las únicas vistas que se pueden abrir sin sesión: los pasos del inicio de sesión y el cierre.
VISTAS_PUBLICAS = {
    'cuentas:iniciar_sesion', 'cuentas:segundo_paso', 'cuentas:registro_segundo_factor', 'cuentas:cerrar_sesion',
}


class TodasLasVistasTests(TestCase):
    def test_toda_vista_exige_sesion_salvo_las_del_inicio_de_sesion(self):
        """Una vista nueva que no esté en la lista pública y responda sin sesión hace fallar esta prueba."""
        rutas = dict(_rutas(get_resolver().url_patterns))
        self.assertIn('cuentas:inicio', rutas)
        self.assertIn('nucleo:auditoria', rutas)
        for nombre in rutas:
            if nombre in VISTAS_PUBLICAS:
                continue
            for metodo in ('get', 'post'):
                r = getattr(Client(), metodo)(reverse(nombre))
                self.assertEqual(r.status_code, 302, f'{metodo.upper()} {nombre} responde sin sesión')
                self.assertTrue(r['Location'].startswith('/entrar/'), f'{nombre}: {r["Location"]}')

    def test_las_vistas_publicas_existen(self):
        rutas = dict(_rutas(get_resolver().url_patterns))
        self.assertLessEqual(VISTAS_PUBLICAS, set(rutas))

    def test_las_vistas_publicas_no_dan_error_sin_sesion(self):
        for nombre in VISTAS_PUBLICAS:
            self.assertLess(Client().get(reverse(nombre)).status_code, 500, nombre)

    def test_el_cierre_de_sesion_no_acepta_get(self):
        self.assertEqual(Client().get(reverse('cuentas:cerrar_sesion')).status_code, 405)


@override_settings(CLAVES_CIFRADO=[CLAVE_A])
class CsrfTests(TestCase):
    def setUp(self):
        self.admin, self.secreto = cuenta_con_segundo_factor()

    def test_todo_formulario_rechaza_un_envio_sin_token_csrf(self):
        rutas = ['/entrar/', '/entrar/codigo/', '/entrar/registro/', '/salir/', '/cuenta/codigos/']
        cliente = Client(enforce_csrf_checks=True)
        for ruta in rutas:
            self.assertEqual(cliente.post(ruta, {'usuario': 'admin', 'contrasena': CONTRASENA}).status_code, 403, ruta)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.fallos_consecutivos, 0)

    def test_con_sesion_iniciada_tampoco_se_aceptan_envios_sin_token(self):
        iniciar_sesion(self.client, self.secreto)
        cliente = Client(enforce_csrf_checks=True)
        cliente.cookies = self.client.cookies
        for ruta in ('/cuenta/codigos/', '/salir/'):
            self.assertEqual(cliente.post(ruta, {'contrasena': CONTRASENA}).status_code, 403, ruta)
        self.assertEqual(self.client.get('/').status_code, 200)

    def test_el_primer_paso_no_distingue_usuario_inexistente_de_contrasena_mala(self):
        a = self.client.post('/entrar/', {'usuario': 'admin', 'contrasena': 'mal'})
        b = self.client.post('/entrar/', {'usuario': 'nadie', 'contrasena': 'mal'})
        self.assertEqual(re.sub(r'value="[^"]+"', '', a.content.decode()), re.sub(r'value="[^"]+"', '', b.content.decode()))


class _Captura(logging.Handler):
    def __init__(self):
        super().__init__(logging.DEBUG)
        self.registros = []

    def emit(self, registro):
        self.registros.append(self.format(registro))


@override_settings(CLAVES_CIFRADO=[CLAVE_A])
class RegistrosSinSecretosTests(TestCase):
    """Condición 7 de terminado: ningún dato personal ni secreto en los registros. Se recorre el
    sistema entero con todos los registros del programa capturados."""

    def test_el_recorrido_completo_no_deja_secretos_en_ningun_registro(self):
        captura = _Captura()
        raiz = logging.getLogger()
        nivel = raiz.level
        raiz.addHandler(captura)
        raiz.setLevel(logging.DEBUG)
        try:
            admin = Administrador.objects.crear_administrador('admin', CONTRASENA)
            token = autenticacion.emitir_token_registro(admin)
            self.client.post('/entrar/', {'usuario': 'ContrasenaEnUsuario1', 'contrasena': 'mal-secreta-123'})
            self.client.post('/entrar/', {'usuario': 'admin', 'contrasena': CONTRASENA})
            self.client.post('/entrar/registro/', {'token': 'token-malo-777'})
            self.client.post('/entrar/registro/', {'token': token})
            secreto = re.search(r'<code>([A-Z2-7]{32})</code>', self.client.get('/entrar/registro/').content.decode()).group(1)
            self.client.post('/entrar/registro/', {'codigo': '999999'})
            r = self.client.post('/entrar/registro/', {'codigo': pyotp.TOTP(secreto).now()})
            codigos = re.findall(r'<code>([A-Z2-9]{5}-[A-Z2-9]{5})</code>', r.content.decode())
            r = self.client.post('/cuenta/codigos/', {'contrasena': CONTRASENA})
            nuevos = re.findall(r'<code>([A-Z2-9]{5}-[A-Z2-9]{5})</code>', r.content.decode())
            self.client.get('/auditoria/')
            self.client.post('/salir/')
        finally:
            raiz.removeHandler(captura)
            raiz.setLevel(nivel)
        texto = '\n'.join(captura.registros)
        secretos = [CONTRASENA, 'mal-secreta-123', 'ContrasenaEnUsuario1', token, 'token-malo-777', secreto, '999999',
                    *codigos, *nuevos]
        self.assertEqual(len(codigos), 10)
        for secreto_i in secretos:
            self.assertNotIn(secreto_i, texto)
