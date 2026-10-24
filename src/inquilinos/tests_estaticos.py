"""Script de reducción: archivo estático propio, página que lo usa y política de contenido (RF-50; decisión 4 de la E1).
Necesitan PostgreSQL solo las de la página."""
import re
import tempfile
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase, override_settings

from . import services
from .models import TextoConsentimiento
from .tests import AHORA
from .tests_fotografias import Navegador
from .tests_servicios import DATOS

RUTA_DEL_SCRIPT = 'inquilinos/reducir_fotografia.js'


def codigo_del_script():
    return Path(finders.find(RUTA_DEL_SCRIPT)).read_text(encoding='utf-8')


class ScriptEstaticoTests(SimpleTestCase):
    def test_esta_en_los_estaticos_de_la_aplicacion(self):
        self.assertIsNotNone(finders.find(RUTA_DEL_SCRIPT))

    def test_tiene_las_cifras_de_rf_50(self):
        codigo = codigo_del_script()
        for esperado in ('LADO_MAXIMO = 2048', '[0.85, 0.80, 0.75, 0.70]', 'OBJETIVO_BYTES = 2000000', 'LIMITE_BYTES = 5242880',
                         "'image/jpeg', 'image/png'", "imageOrientation: 'from-image'"):
            self.assertIn(esperado, codigo)

    def test_no_usa_nada_que_la_politica_de_contenido_o_la_seguridad_desaconsejen(self):
        codigo = re.sub(r'/\*.*?\*/', '', codigo_del_script(), flags=re.S)   # sin los comentarios
        for prohibido in ('eval(', 'new Function', 'innerHTML', 'outerHTML', 'insertAdjacentHTML', 'document.write',
                          'javascript:', 'http://', 'https://', 'localStorage', 'sessionStorage', 'XMLHttpRequest',
                          'importScripts', 'postMessage', 'setTimeout(\'', 'setTimeout("', 'setInterval(\''):
            self.assertNotIn(prohibido, codigo, prohibido)
        self.assertTrue(codigo.lstrip().startswith('(function () {'))
        self.assertIn("'use strict'", codigo)

    def test_los_mensajes_al_usuario_se_escriben_como_texto_no_como_html(self):
        codigo = codigo_del_script()
        self.assertIn('region.textContent = texto', codigo)

    def test_los_ajustes_de_estaticos(self):
        self.assertEqual(settings.STATIC_URL, '/static/')  # Django la normaliza
        raiz = Path(settings.STATIC_ROOT)
        self.assertNotEqual(raiz, Path(settings.RAIZ_DOCUMENTOS))
        self.assertNotIn(Path(settings.RAIZ_DOCUMENTOS).as_posix(), raiz.as_posix() + '/')
        self.assertNotIn(Path(settings.BASE_DIR).resolve(), [raiz.resolve(), *raiz.resolve().parents])

    def test_collectstatic_copia_el_script_a_la_carpeta_de_estaticos_sin_cambiarlo(self):
        with tempfile.TemporaryDirectory() as destino, override_settings(STATIC_ROOT=destino):
            call_command('collectstatic', interactive=False, verbosity=0)
            copiado = Path(destino, RUTA_DEL_SCRIPT)
            self.assertTrue(copiado.is_file())
            self.assertEqual(copiado.read_text(encoding='utf-8'), codigo_del_script())
            self.assertEqual(sorted(p.name for p in Path(destino).rglob('*') if p.is_file()), ['reducir_fotografia.js'])


class PaginaDeFotografiasTests(Navegador):
    def setUp(self):
        texto = TextoConsentimiento.objects.create(version=1, contenido='Texto', vigente_desde=AHORA)
        self.inquilino = services.registrar_inquilino(actor='admin', datos=dict(DATOS), texto=texto, medio='fisico', ahora=AHORA)

    def test_exige_sesion(self):
        r = self.client.get(f'/inquilinos/{self.inquilino.pk}/fotografias/')
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r['Location'].startswith('/entrar/'))

    def test_trae_un_formulario_por_cara_con_token_y_el_script_propio(self):
        self.entrar()
        r = self.client.get(f'/inquilinos/{self.inquilino.pk}/fotografias/')
        html = r.content.decode()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(re.findall(r'<form[^>]*data-sga-fotografia', html)), 2)
        for cara in ('frente', 'reverso'):
            self.assertIn(f'action="/inquilinos/{self.inquilino.pk}/fotografias/{cara}/"', html)
        self.assertEqual(html.count('csrfmiddlewaretoken'), 2)
        self.assertEqual(re.findall(r'<script[^>]*src="([^"]+)"', html), ['/static/inquilinos/reducir_fotografia.js'])
        self.assertIsNone(re.search(r'<script(?![^>]*\ssrc=)|\son[a-z]+\s*=|\sstyle\s*=', html, re.I))
        self.assertIn('Falta el frente', html)
        self.assertIn('no-store', r['Cache-Control'])

    def test_un_inquilino_inexistente_da_404(self):
        self.entrar()
        self.assertEqual(self.client.get('/inquilinos/999999/fotografias/').status_code, 404)

    def test_avisa_si_no_hay_consentimiento_vigente(self):
        self.entrar()
        services.revocar_consentimiento(self.inquilino.pk, actor='admin')
        self.assertIn('no tiene un consentimiento vigente', self.client.get(f'/inquilinos/{self.inquilino.pk}/fotografias/').content.decode())
