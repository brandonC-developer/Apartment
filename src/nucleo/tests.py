"""Pruebas del esqueleto E0 que no necesitan base de datos."""
import subprocess
import sys
from pathlib import Path

from django.conf import settings
from django.contrib.auth.hashers import make_password, identify_hasher
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase


class ConfiguracionBasicaTests(SimpleTestCase):
    def test_hash_de_contrasena_es_argon2id(self):
        # ADR-019: Argon2id; Django identifica el algoritmo en el prefijo del hash.
        resultado = make_password('una contrasena larga de prueba')
        self.assertTrue(resultado.startswith('argon2$argon2id$'))
        self.assertEqual(identify_hasher(resultado).algorithm, 'argon2')

    def test_contrasena_de_menos_de_15_caracteres_se_rechaza(self):
        with self.assertRaises(ValidationError):
            validate_password('corta12345678')  # 13 caracteres

    def test_contrasena_de_15_caracteres_sin_reglas_de_composicion(self):
        validate_password('aqui-hay-quince-')  # 16 caracteres; sin mayúsculas ni números

    def test_zona_horaria_y_marcas_utc(self):
        self.assertEqual(settings.TIME_ZONE, 'America/Costa_Rica')
        self.assertTrue(settings.USE_TZ)

    def test_no_se_usa_el_administrador_de_django(self):
        self.assertNotIn('django.contrib.admin', settings.INSTALLED_APPS)


class SecretoObligatorioTests(SimpleTestCase):
    def test_sin_secret_key_y_sin_debug_el_proyecto_no_arranca(self):
        # Se prueba en un proceso aparte porque settings ya está cargado en este.
        raiz = Path(settings.BASE_DIR)
        entorno = {'PATH': '', 'SYSTEMROOT': r'C:\Windows', 'SGA_DIRECTORIO_SECRETOS': str(raiz / 'no-existe')}
        proceso = subprocess.run(
            [sys.executable, 'manage.py', 'check'], cwd=raiz, env=entorno,
            capture_output=True, text=True,
        )
        self.assertNotEqual(proceso.returncode, 0)
        self.assertIn('Falta SECRET_KEY', proceso.stderr)
