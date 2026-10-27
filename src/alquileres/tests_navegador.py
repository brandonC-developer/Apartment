"""Reducción de la fotografía del contrato en un navegador real (RF-52, RF-50; CA-76, CA-82; DP-29).

Como las de la E1: Selenium con `StaticLiveServerTestCase`; se omiten si falta Selenium o un navegador, y no corren en
WSL. Comprueban el punto de partida de 3508 px del contrato frente a los 2048 px de la cédula, con imágenes generadas;
el peso con fotos reales de teléfono se mide aparte (grupo H)."""
import tempfile
import time
from io import BytesIO
from pathlib import Path
from unittest import SkipTest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client, override_settings
from PIL import Image

from cuentas.models import Administrador
from inquilinos import almacenamiento, services as servicios_de_inquilinos
from inquilinos.models import TextoConsentimiento
from inquilinos.tests import un_documento
from inquilinos.tests_imagenes import a_bytes
from inquilinos.tests_navegador import crear_navegador

from . import services
from .models import DocumentoContrato
from .tests_servicios import AHORA, d

try:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:  # Selenium no está instalado
    By = WebDriverWait = None


class ReduccionDelContratoEnElNavegadorTests(StaticLiveServerTestCase):
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        cls.navegador, motivos = crear_navegador()
        if cls.navegador is None:
            raise SkipTest('Sin navegador para las pruebas de extremo a extremo: ' + '; '.join(motivos))
        super().setUpClass()
        cls.carpeta = tempfile.TemporaryDirectory()
        cls.raiz = override_settings(RAIZ_DOCUMENTOS=cls.carpeta.name)
        cls.raiz.enable()

    @classmethod
    def tearDownClass(cls):
        if getattr(cls, 'navegador', None) is not None:
            cls.navegador.quit()
            cls.raiz.disable()
            cls.carpeta.cleanup()
        super().tearDownClass()

    def setUp(self):
        texto = TextoConsentimiento.objects.create(version=1, contenido='Texto', vigente_desde=AHORA)
        self.inquilino = servicios_de_inquilinos.registrar_inquilino(
            actor='admin', datos=dict(nombre_completo='Persona Uno', tipo_documento='cedula', numero_documento='9-1'),
            texto=texto, medio='fisico', ahora=AHORA)
        un_documento(self.inquilino)
        self.propiedad = services.registrar_propiedad(actor='admin', datos={'alias': 'Casa 1'}, ahora=AHORA)
        self.contrato = services.crear_contrato(
            actor='admin', inquilino_id=self.inquilino.pk, propiedad_id=self.propiedad.pk, ahora=AHORA,
            datos=dict(destino='vivienda', fecha_inicio=d('2026-01-01'), fecha_fin=None, moneda='CRC',
                       monto_mensual='300000.00', dia_vencimiento=5, dias_gracia=7)).contrato
        self.archivos = tempfile.TemporaryDirectory()
        self.addCleanup(self.archivos.cleanup)
        cliente = Client()
        admin = Administrador.objects.crear_administrador('admin', 'una contrasena larga de prueba')
        cliente.force_login(admin, backend='cuentas.backends.BackendAdministrador')
        sesion = cliente.session
        sesion['sesion_inicio'] = sesion['sesion_ultima'] = time.time()
        sesion.save()
        self.navegador.get(f'{self.live_server_url}/entrar/')
        self.navegador.delete_all_cookies()
        self.navegador.add_cookie({'name': 'sessionid', 'value': sesion.session_key, 'path': '/'})

    def enviar(self, selector, contenido):
        ruta = Path(self.archivos.name) / 'foto.jpg'
        ruta.write_bytes(contenido)
        formulario = self.navegador.find_element(By.CSS_SELECTOR, selector)
        formulario.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(str(ruta))
        formulario.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        WebDriverWait(self.navegador, 90).until(
            lambda n: n.find_element(By.CSS_SELECTOR, selector).get_attribute('data-estado') in ('guardada', 'rechazada', 'sin-enviar'))
        formulario = self.navegador.find_element(By.CSS_SELECTOR, selector)
        enviado = {k: formulario.get_attribute(f'data-enviado-{k}') for k in ('bytes', 'tipo', 'ancho', 'alto', 'original')}
        return formulario.get_attribute('data-estado'), formulario.find_element(By.CSS_SELECTOR, '[data-sga-mensaje]').text, enviado

    def foto_grande(self):
        return a_bytes(Image.new('RGB', (4032, 3024), (30, 90, 160)), 'JPEG', quality=85)

    def test_la_fotografia_del_contrato_se_reduce_a_3508_px_de_lado_mayor(self):
        self.navegador.get(f'{self.live_server_url}/contratos/{self.contrato.pk}/fotografias/')
        estado, mensaje, enviado = self.enviar('form[data-sga-fotografia]', self.foto_grande())
        self.assertEqual(estado, 'guardada', mensaje)
        self.assertEqual((enviado['tipo'], enviado['ancho'], enviado['alto'], enviado['original']), ('image/jpeg', '3508', '2631', 'no'))
        documento = DocumentoContrato.objects.get(contrato=self.contrato)
        with almacenamiento.abrir(documento.referencia_archivo, 'contratos') as f:
            self.assertEqual(Image.open(BytesIO(f.read())).size, (3508, 2631))

    def test_la_cedula_desde_el_perfil_sigue_reduciendo_a_2048_px(self):
        self.navegador.get(f'{self.live_server_url}/propiedades/{self.propiedad.pk}/cedula/')
        estado, mensaje, enviado = self.enviar('form[data-cara="reverso"]', self.foto_grande())
        self.assertEqual(estado, 'guardada', mensaje)
        self.assertEqual((enviado['ancho'], enviado['alto']), ('2048', '1536'))

    def test_una_imagen_menor_que_el_punto_de_partida_no_se_amplia(self):
        self.navegador.get(f'{self.live_server_url}/contratos/{self.contrato.pk}/fotografias/')
        pequena = a_bytes(Image.new('RGB', (1200, 800), (30, 90, 160)), 'JPEG')
        estado, mensaje, enviado = self.enviar('form[data-sga-fotografia]', pequena)
        self.assertEqual(estado, 'guardada', mensaje)
        self.assertEqual((enviado['ancho'], enviado['alto']), ('1200', '800'))
