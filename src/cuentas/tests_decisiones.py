"""Decisiones del solicitante del 24-oct-2026 (actualización 2026-10-24o): códigos de recuperación con
Argon2id y sal (NIST SP 800-63B), `DELETE` de los códigos anteriores y secreto del autenticador
ilegible. Necesitan PostgreSQL."""
import re

import pyotp
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from django.test import TestCase, override_settings

from nucleo.models import Auditoria

from . import autenticacion
from .models import Administrador, CodigoRecuperacion
from .tests import CLAVE_A, CLAVE_B, CONTRASENA
from .tests_cuenta import cuenta_con_segundo_factor, iniciar_sesion


@override_settings(CLAVES_CIFRADO=[CLAVE_A])
class CodigosConArgon2Tests(TestCase):
    def setUp(self):
        self.admin, _ = cuenta_con_segundo_factor()
        self.codigos = autenticacion.emitir_codigos_recuperacion(self.admin, CONTRASENA)

    def test_se_guardan_como_argon2id_con_sal_distinta_por_codigo(self):
        hashes = list(CodigoRecuperacion.objects.values_list('hash_codigo', flat=True))
        self.assertEqual(len(hashes), 10)
        self.assertTrue(all(h.startswith('$argon2id$') for h in hashes))
        self.assertEqual(len(set(hashes)), 10)
        # El mismo código dos veces produce hashes distintos (sal).
        self.assertNotEqual(autenticacion._hash_codigo(self.codigos[0]), autenticacion._hash_codigo(self.codigos[0]))

    def test_el_hash_no_contiene_el_codigo_ni_se_puede_buscar_por_el_hash_del_codigo(self):
        import hashlib
        sha = hashlib.sha256(autenticacion._normalizar_codigo(self.codigos[0]).encode()).hexdigest()
        todo = ' '.join(CodigoRecuperacion.objects.values_list('hash_codigo', flat=True))
        self.assertNotIn(sha, todo)
        self.assertNotIn(autenticacion._normalizar_codigo(self.codigos[0]), todo)

    def test_un_codigo_correcto_sirve_una_vez_y_uno_equivocado_no(self):
        self.assertTrue(autenticacion.codigo_disponible(self.admin, self.codigos[3]))
        self.assertFalse(autenticacion.codigo_disponible(self.admin, 'AAAAA-AAAAA'))
        r = autenticacion.verificar_codigo_recuperacion(self.admin.pk, self.codigos[3].lower())
        self.assertTrue(r.correcto)
        self.assertFalse(autenticacion.codigo_disponible(self.admin, self.codigos[3]))
        self.admin.refresh_from_db()
        self.assertEqual(CodigoRecuperacion.objects.filter(usado_en__isnull=False).count(), 1)

    def test_los_parametros_de_produccion_son_los_minimos_de_owasp(self):
        """Se comprueba en un proceso aparte porque en las pruebas se usan parámetros baratos."""
        import subprocess, sys
        from django.conf import settings
        salida = subprocess.run(
            [sys.executable, '-c',
             "import os; os.environ['SGA_DEBUG']='1'; os.environ['DJANGO_SETTINGS_MODULE']='sga.settings'; "
             "from django.conf import settings as s; print(s.CODIGOS_ARGON2)"],
            cwd=settings.BASE_DIR, capture_output=True, text=True).stdout.strip()
        self.assertEqual(salida, "{'time_cost': 2, 'memory_cost': 19456, 'parallelism': 1}")
        real = PasswordHasher(time_cost=2, memory_cost=19456, parallelism=1).hash('XXXXXXXXXX')
        self.assertIn('m=19456,t=2,p=1', real)

    def test_en_pruebas_los_parametros_son_baratos(self):
        from django.conf import settings
        self.assertEqual(settings.CODIGOS_ARGON2['memory_cost'], 1024)


@override_settings(CLAVES_CIFRADO=[CLAVE_A])
class SecretoIlegibleTests(TestCase):
    """La clave Fernet se perdió o cambió: el secreto del autenticador no se puede leer."""

    def setUp(self):
        self.admin, self.secreto = cuenta_con_segundo_factor()
        self.recuperacion = autenticacion.emitir_codigos_recuperacion(self.admin, CONTRASENA)

    def test_un_codigo_totp_con_la_clave_cambiada_es_un_fallo_y_no_un_error_500(self):
        with override_settings(CLAVES_CIFRADO=[CLAVE_B]):
            self.client.post('/entrar/', {'usuario': 'admin', 'contrasena': CONTRASENA})
            r = self.client.post('/entrar/codigo/', {'codigo': pyotp.TOTP(self.secreto).now()})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Código incorrecto')
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.fallos_consecutivos, 1)
        self.assertEqual(Auditoria.objects.filter(accion='segundo_factor_ilegible').count(), 1)
        self.assertEqual(self.client.get('/').status_code, 302)

    def test_con_un_codigo_de_recuperacion_se_entra_igual_y_el_evento_sale_en_la_alerta(self):
        with override_settings(CLAVES_CIFRADO=[CLAVE_B]):
            self.client.post('/entrar/', {'usuario': 'admin', 'contrasena': CONTRASENA})
            self.client.post('/entrar/codigo/', {'codigo': pyotp.TOTP(self.secreto).now()})
            self.client.post('/entrar/codigo/', {'codigo': self.recuperacion[0]})
            r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'segundo_factor_ilegible')

    def test_con_la_clave_bien_el_mismo_codigo_entra(self):
        iniciar_sesion(self.client, self.secreto)
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(Auditoria.objects.filter(accion='segundo_factor_ilegible').count(), 0)

    def test_la_clave_nueva_primero_con_la_vieja_en_la_lista_sigue_leyendo_el_secreto(self):
        """Rotación (MultiFernet): no es un secreto ilegible."""
        with override_settings(CLAVES_CIFRADO=[CLAVE_B, CLAVE_A]):
            iniciar_sesion(self.client, self.secreto)
            self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(Auditoria.objects.filter(accion='segundo_factor_ilegible').count(), 0)
