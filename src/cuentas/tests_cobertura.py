"""Pruebas que salen de la revisión del código sin cubrir de la E0 (actualización 2026-10-24m).

Cada una cubre una línea o rama que la cobertura mostró sin ejecutar en un módulo crítico (autenticación,
sesión y registro del segundo factor). Necesitan PostgreSQL."""
from datetime import timedelta

import pyotp
from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from . import autenticacion
from .autenticacion import Resultado
from .models import Administrador
from .tests import CLAVE_A, CONTRASENA
from .tests_cuenta import cuenta_con_segundo_factor, iniciar_sesion


@override_settings(CLAVES_CIFRADO=[CLAVE_A])
class ModeloYBackendTests(TestCase):
    def setUp(self):
        self.admin, self.secreto = cuenta_con_segundo_factor()

    def test_crear_sin_usuario_se_rechaza(self):
        Administrador.objects.all().delete()
        for vacio in ('', None):
            with self.assertRaises(ValueError):
                Administrador.objects.crear_administrador(vacio, CONTRASENA)

    def test_texto_de_la_cuenta(self):
        self.assertEqual(str(self.admin), 'admin')

    def test_authenticate_sin_usuario_o_sin_contrasena_devuelve_none_y_no_toca_la_cuenta(self):
        self.assertIsNone(authenticate(usuario=None, contrasena=CONTRASENA))
        self.assertIsNone(authenticate(usuario='admin', contrasena=None))
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.fallos_consecutivos, 0)

    def test_una_sesion_de_una_cuenta_que_ya_no_existe_se_trata_como_anonima(self):
        iniciar_sesion(self.client, self.secreto)
        self.assertEqual(self.client.get('/').status_code, 200)
        Administrador.objects.all().delete()
        r = self.client.get('/')
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r['Location'].startswith('/entrar/'))
        self.assertIsNone(get_user_model()._default_manager.filter(pk=1).first())


@override_settings(CLAVES_CIFRADO=[CLAVE_A])
class UnaCuentaConSesionNoRepiteLosPasosTests(TestCase):
    def test_con_sesion_iniciada_los_pasos_del_inicio_redirigen_al_inicio(self):
        admin, secreto = cuenta_con_segundo_factor()
        iniciar_sesion(self.client, secreto)
        for ruta in ('/entrar/', '/entrar/codigo/', '/entrar/registro/'):
            r = self.client.get(ruta)
            self.assertRedirects(r, '/', fetch_redirect_response=False)
        self.assertEqual(self.client.post('/entrar/', {'usuario': 'x', 'contrasena': 'y'}).status_code, 302)
        admin.refresh_from_db()
        self.assertEqual(admin.fallos_consecutivos, 0)

    def test_cerrar_sesion_sin_sesion_no_falla_ni_audita(self):
        from nucleo.models import Auditoria
        r = Client().post('/salir/')
        self.assertRedirects(r, '/entrar/', fetch_redirect_response=False)
        self.assertEqual(Auditoria.objects.count(), 0)


@override_settings(CLAVES_CIFRADO=[CLAVE_A])
class TokenDeRegistroCaducaAMitadTests(TestCase):
    """El token se comprueba al pedirlo y otra vez, bajo bloqueo, al activar: si se vence o se consume
    entre una cosa y otra, no se activa nada y se vuelve a pedir."""

    def setUp(self):
        self.admin = Administrador.objects.crear_administrador('admin', CONTRASENA)
        self.token = autenticacion.emitir_token_registro(self.admin)
        self.client.post('/entrar/', {'usuario': 'admin', 'contrasena': CONTRASENA})
        self.client.post('/entrar/registro/', {'token': self.token})

    def test_si_el_token_se_vence_antes_de_activar_se_vuelve_a_pedir_y_no_se_activa(self):
        import re
        secreto = re.search(r'<code>([A-Z2-7]{32})</code>', self.client.get('/entrar/registro/').content.decode()).group(1)
        Administrador.objects.update(token_registro_vence=timezone.now() - timedelta(seconds=1))
        r = self.client.post('/entrar/registro/', {'codigo': pyotp.TOTP(secreto).now()})
        self.assertRedirects(r, '/entrar/registro/', fetch_redirect_response=False)
        self.assertContains(self.client.get('/entrar/registro/'), 'name="token"')
        self.admin.refresh_from_db()
        self.assertFalse(self.admin.segundo_factor_activo)
        self.assertEqual(self.client.get('/').status_code, 302)

    def test_comprobar_el_token_de_una_cuenta_que_ya_tiene_segundo_factor_no_toca_el_contador(self):
        Administrador.objects.update(segundo_factor_activo=True)
        r = autenticacion.comprobar_token_registro(self.admin.pk, self.token)
        self.assertEqual(r.resultado, Resultado.INCORRECTO)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.fallos_consecutivos, 0)
