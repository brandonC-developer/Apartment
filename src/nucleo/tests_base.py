"""Esquema físico y almacenamiento privado (ADR-028, ADR-031 decisión 1, RNF-03, RNF-14)."""
import re
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.db import connection, models
from django.test import SimpleTestCase, TestCase


class IdentificadoresTests(SimpleTestCase):
    def test_todo_modelo_del_proyecto_usa_un_entero_de_64_bits_autoincremental(self):
        """ADR-028. Se extiende solo a las aplicaciones del proyecto, no a las de Django."""
        modelos = [m for nombre in ('nucleo', 'cuentas', 'inquilinos') for m in apps.get_app_config(nombre).get_models()]
        self.assertGreaterEqual(len(modelos), 9)
        for modelo in modelos:
            self.assertIsInstance(modelo._meta.pk, models.BigAutoField, modelo.__name__)


class DocumentosPrivadosTests(SimpleTestCase):
    def test_la_carpeta_esta_fuera_del_codigo_y_de_cualquier_raiz_web(self):
        raiz = Path(settings.RAIZ_DOCUMENTOS)
        # En Windows una ruta «/var/...» no tiene unidad; basta con que sea absoluta en Linux.
        self.assertTrue(raiz.is_absolute() or raiz.as_posix().startswith('/'))
        self.assertNotIn(Path(settings.BASE_DIR).resolve(), [raiz.resolve(), *raiz.resolve().parents])
        self.assertFalse(str(raiz).startswith(('/var/www', '/usr/share/nginx', '/srv/www')))
        for ajustada in ('STATIC_ROOT', 'MEDIA_ROOT'):
            valor = getattr(settings, ajustada, None)
            if valor:
                self.assertNotIn(Path(valor).resolve(), [raiz.resolve(), *raiz.resolve().parents])

    def test_no_hay_url_publica_de_archivos(self):
        # Django normaliza un MEDIA_URL vacío a «/»; lo que cuenta es que no haya MEDIA_ROOT que servir.
        self.assertFalse(getattr(settings, 'MEDIA_ROOT', ''))

    def test_ninguna_ruta_sirve_archivos_estaticos_del_proyecto(self):
        from django.urls import get_resolver
        self.assertEqual([str(p.pattern) for p in get_resolver().url_patterns if 'static' in str(p.pattern)], [])

    def test_nginx_no_sirve_la_carpeta_de_documentos(self):
        sitio = (Path(settings.BASE_DIR) / 'despliegue/nginx/sga-sitio.conf').read_text(encoding='utf-8')
        # Desde la E1 Nginx sirve /static/ (decisión del 24-oct-2026): ese es el ÚNICO alias permitido, con las barras
        # emparejadas, y nada apunta a la carpeta de documentos.
        self.assertEqual(re.findall(r'^\s*alias\s+(\S+);', sitio, re.M), ['/opt/sga/static/'])
        self.assertIn('location /static/ {', sitio)
        self.assertNotIn('root ', sitio)
        self.assertNotIn('/var/lib/sga/documentos', sitio)


class ExtensionesTests(TestCase):
    def test_btree_gist_esta_disponible_para_el_solape_de_contratos(self):
        with connection.cursor() as c:
            c.execute("SELECT 1 FROM pg_extension WHERE extname = 'btree_gist'")
            self.assertIsNotNone(c.fetchone())
