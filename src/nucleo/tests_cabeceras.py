"""Cabeceras de seguridad (ADR-032, decisiones 5 y 16). Necesitan PostgreSQL por la zona horaria."""
import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, TestCase

from nucleo.middleware import POLITICA_DE_CONTENIDO


class PoliticaDeContenidoTests(TestCase):
    def test_toda_respuesta_lleva_la_politica_como_informe(self):
        for ruta in ('/entrar/', '/auditoria/', '/no-existe/'):
            r = self.client.get(ruta)
            self.assertEqual(r['Content-Security-Policy-Report-Only'], POLITICA_DE_CONTENIDO, ruta)

    def test_la_politica_es_la_de_la_decision_16(self):
        for parte in ("default-src 'none'", "script-src 'self'", "style-src 'self'", "frame-ancestors 'none'",
                      "object-src 'none'", "base-uri 'none'", "form-action 'self'"):
            self.assertIn(parte, POLITICA_DE_CONTENIDO)
        self.assertNotIn('unsafe', POLITICA_DE_CONTENIDO)

    def test_las_respuestas_llevan_las_cabeceras_que_pone_django(self):
        r = self.client.get('/entrar/')
        self.assertEqual(r['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(r['X-Frame-Options'], 'DENY')
        self.assertEqual(r['Referrer-Policy'], 'same-origin')


class PlantillasSinCodigoEnLineaTests(SimpleTestCase):
    """La política prohíbe scripts y estilos en línea: ninguna plantilla debe tenerlos (sí un `<script src>` propio)."""

    def test_sin_script_style_ni_manejadores_en_linea(self):
        plantillas = list(Path(settings.BASE_DIR).glob('*/templates/**/*.html'))
        self.assertTrue(plantillas)
        for ruta in plantillas:
            texto = ruta.read_text(encoding='utf-8')
            self.assertIsNone(re.search(r'<script(?![^>]*\ssrc=)|<style|\sstyle\s*=|\son[a-z]+\s*=|javascript:', texto, re.I), ruta)
