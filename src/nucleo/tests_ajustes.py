"""Ajustes de producción y lectura de secretos (ADR-032 decisiones 5, 6 y 13). Se prueban en un proceso
aparte porque `settings` ya está cargado en este y depende del entorno."""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

CODIGO = (
    "import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'sga.settings'; "
    "from django.conf import settings as s; "
    "print('|'.join(str(x) for x in [bool(s.SECRET_KEY), s.DEBUG, s.SESSION_COOKIE_SECURE, s.CSRF_COOKIE_SECURE, "
    "s.SECURE_SSL_REDIRECT, s.SECURE_PROXY_SSL_HEADER, s.SECURE_HSTS_SECONDS, s.IP_ORIGEN_CABECERA, "
    "s.ALLOWED_HOSTS, s.SECRET_KEY[:8]]))"
)


def ajustes(**entorno):
    base = {k: v for k, v in os.environ.items() if not k.startswith('SGA_')}
    base.update(entorno)
    p = subprocess.run([sys.executable, '-c', CODIGO], cwd=settings.BASE_DIR, env=base, capture_output=True, text=True)
    return p.returncode, p.stdout.strip().split('|'), p.stderr


class AjustesDeProduccionTests(SimpleTestCase):
    def test_la_clave_secreta_se_lee_de_la_variable_de_entorno(self):
        codigo, v, err = ajustes(SGA_SECRET_KEY='entorno-prueba-0123456789-abcdefghijklmnopqrstuvwxyz', SGA_DIRECTORIO_SECRETOS='/no/existe')
        self.assertEqual(codigo, 0, err)
        self.assertEqual(v[0], 'True')
        self.assertEqual(v[-1], 'entorno-')

    def test_la_clave_secreta_se_lee_de_un_archivo_del_directorio_de_secretos(self):
        with tempfile.TemporaryDirectory() as carpeta:
            Path(carpeta, 'secret_key').write_text('archivo--0123456789abcdefghijklmnopqrstuvwxyz\n')
            codigo, v, err = ajustes(SGA_DIRECTORIO_SECRETOS=carpeta)
        self.assertEqual(codigo, 0, err)
        self.assertEqual(v[-1], 'archivo-')  # viene del archivo y no del entorno

    def test_sin_depuracion_las_cookies_son_seguras_y_se_redirige_a_https(self):
        codigo, v, err = ajustes(SGA_SECRET_KEY='clave-de-prueba-del-entorno-0123456789', SGA_HOSTS_PERMITIDOS='localhost, ejemplo.cr')
        self.assertEqual(codigo, 0, err)
        debug, sesion, csrf, redireccion, cabecera, hsts, ip, hosts = v[1:9]
        self.assertEqual((debug, sesion, csrf, redireccion), ('False', 'True', 'True', 'True'))
        self.assertEqual(cabecera, "('HTTP_X_FORWARDED_PROTO', 'https')")
        self.assertEqual(hsts, '0')  # HSTS por etapas: se activa en la etapa B
        self.assertEqual(ip, 'HTTP_X_FORWARDED_FOR')
        self.assertEqual(hosts, "['localhost', 'ejemplo.cr']")

    def test_con_depuracion_se_usa_remote_addr_y_no_se_fuerza_https(self):
        codigo, v, err = ajustes(SGA_DEBUG='1')
        self.assertEqual(codigo, 0, err)
        debug, sesion, redireccion, ip = v[1], v[2], v[4], v[7]
        self.assertEqual((debug, sesion, redireccion, ip), ('True', 'False', 'False', 'None'))
        self.assertEqual(v[-1], 'solo-des')  # la clave de desarrollo, solo con depuración
