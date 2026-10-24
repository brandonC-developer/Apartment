"""Reducción de la fotografía en el navegador, con un navegador real (RF-50; CA-73, CA-74, CA-83).

Selenium con `StaticLiveServerTestCase`, como decide la estrategia de pruebas. Se omiten si falta Selenium o un
navegador (Chrome, Edge o Firefox) con su controlador; no corren en WSL, donde no hay navegador. El peso con fotos
reales de un iPhone y dos Android se mide a mano en el grupo G; aquí se usan imágenes generadas."""
import os
import tempfile
import time
from io import BytesIO
from pathlib import Path
from unittest import SkipTest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client, override_settings
from PIL import Image

from cuentas.models import Administrador
from nucleo.models import Auditoria

from . import almacenamiento, services
from .models import DocumentoIdentidad, TextoConsentimiento
from .tests import AHORA
from .tests_imagenes import a_bytes
from .tests_servicios import DATOS

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:  # Selenium no está instalado (no es de producción: requirements-pruebas.txt)
    webdriver = None

LIMITE = 5 * 1024 * 1024


def crear_navegador():
    """El primer navegador que arranque, sin ventana (o el de `SGA_NAVEGADOR`). Devuelve (navegador, motivos de lo que falló)."""
    if webdriver is None:
        return None, ['Selenium no está instalado (requirements-pruebas.txt)']
    motivos = []
    elegido = os.environ.get('SGA_NAVEGADOR')   # chrome, edge o firefox, para probar uno en concreto
    for nombre in ((elegido,) if elegido else ('chrome', 'edge', 'firefox')):
        try:
            if nombre == 'chrome':
                opciones = webdriver.ChromeOptions()
                opciones.add_argument('--headless=new')
                opciones.add_argument('--no-sandbox')
                opciones.add_argument('--disable-gpu')
                return webdriver.Chrome(options=opciones), motivos
            if nombre == 'edge':
                opciones = webdriver.EdgeOptions()
                opciones.add_argument('--headless=new')
                opciones.add_argument('--no-sandbox')
                opciones.add_argument('--disable-gpu')
                return webdriver.Edge(options=opciones), motivos
            opciones = webdriver.FirefoxOptions()
            opciones.add_argument('-headless')
            return webdriver.Firefox(options=opciones), motivos
        except Exception as error:  # el navegador o su controlador no están
            motivos.append(f'{nombre}: {str(error).splitlines()[0][:100]}')
    return None, motivos


def ruido(ancho, alto, calidad=70, exif=None):
    imagen = Image.frombytes('RGB', (ancho, alto), os.urandom(ancho * alto * 3))
    salida = BytesIO()
    imagen.save(salida, 'JPEG', quality=calidad, **({'exif': exif} if exif else {}))
    return salida.getvalue()


class ReduccionEnElNavegadorTests(StaticLiveServerTestCase):
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
        self.texto = TextoConsentimiento.objects.create(version=1, contenido='Texto', vigente_desde=AHORA)
        self.inquilino = services.registrar_inquilino(
            actor='admin', datos=dict(DATOS), texto=self.texto, medio='fisico', ahora=AHORA)
        self.archivos = tempfile.TemporaryDirectory()
        self.addCleanup(self.archivos.cleanup)
        self.iniciar_sesion()
        self.navegador.get(f'{self.live_server_url}/inquilinos/{self.inquilino.pk}/fotografias/')

    def iniciar_sesion(self):
        cliente = Client()
        admin = Administrador.objects.crear_administrador('admin', 'una contrasena larga de prueba')
        cliente.force_login(admin, backend='cuentas.backends.BackendAdministrador')
        sesion = cliente.session
        sesion['sesion_inicio'] = sesion['sesion_ultima'] = time.time()
        sesion.save()
        self.navegador.get(f'{self.live_server_url}/entrar/')
        self.navegador.delete_all_cookies()
        self.navegador.add_cookie({'name': 'sessionid', 'value': sesion.session_key, 'path': '/'})

    # --- ayudas
    def archivo(self, nombre, contenido):
        ruta = Path(self.archivos.name) / nombre
        ruta.write_bytes(contenido)
        return str(ruta)

    def formulario(self, cara):
        return self.navegador.find_element(By.CSS_SELECTOR, f'form[data-cara="{cara}"]')

    def enviar(self, cara, ruta):
        formulario = self.formulario(cara)
        formulario.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(ruta)
        formulario.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        WebDriverWait(self.navegador, 90).until(
            lambda n: self.formulario(cara).get_attribute('data-estado') in ('guardada', 'rechazada', 'sin-enviar'))
        formulario = self.formulario(cara)
        enviado = {k: formulario.get_attribute(f'data-enviado-{k}') for k in ('bytes', 'tipo', 'ancho', 'alto', 'calidad', 'original')}
        return formulario.get_attribute('data-estado'), formulario.find_element(By.CSS_SELECTOR, '[data-sga-mensaje]').text, enviado

    def guardado(self, cara='frente'):
        documento = DocumentoIdentidad.objects.get(inquilino=self.inquilino, cara=cara, eliminado_en__isnull=True)
        with almacenamiento.abrir(documento.referencia_archivo) as f:
            return documento, Image.open(BytesIO(f.read())).convert('RGB')

    # --- CA-73
    def test_una_foto_de_4032_por_3024_y_mas_de_5_mib_se_reduce_a_2048_por_1536_jpeg_de_menos_de_5_mib(self):
        original = ruido(4032, 3024)
        self.assertGreater(len(original), LIMITE)  # sin reducir, el servidor la rechazaría
        estado, mensaje, enviado = self.enviar('frente', self.archivo('grande.jpg', original))
        self.assertEqual(estado, 'guardada', mensaje)
        self.assertEqual((enviado['tipo'], enviado['ancho'], enviado['alto'], enviado['original']), ('image/jpeg', '2048', '1536', 'no'))
        self.assertLessEqual(int(enviado['bytes']), LIMITE)
        self.assertGreaterEqual(float(enviado['calidad']), 0.70)  # RF-50: nunca por debajo de 0,70
        documento, imagen = self.guardado()
        self.assertEqual(imagen.size, (2048, 1536))
        print(f'\n[CA-73] {len(original) / 1048576:.2f} MiB de 4032x3024 -> {int(enviado["bytes"]) / 1048576:.2f} MiB '
              f'de 2048x1536 con calidad {enviado["calidad"]} (objetivo de 2 MB: {"sí" if int(enviado["bytes"]) <= 2000000 else "no"})')

    def test_una_imagen_pequena_no_se_amplia(self):
        estado, mensaje, enviado = self.enviar('frente', self.archivo('pequena.jpg', a_bytes(Image.new('RGB', (1200, 800), (30, 90, 160)), 'JPEG')))
        self.assertEqual(estado, 'guardada', mensaje)
        self.assertEqual((enviado['ancho'], enviado['alto'], enviado['tipo']), ('1200', '800', 'image/jpeg'))
        self.assertEqual(self.guardado()[1].size, (1200, 800))

    def test_se_conserva_la_orientacion_visible(self):
        """RF-50 (5): una foto de teléfono guarda la imagen de lado y una marca EXIF; debe quedar derecha."""
        crudo = Image.new('RGB', (400, 300), (0, 0, 255))
        crudo.paste((255, 0, 0), (0, 0, 200, 300))   # mitad izquierda del archivo: roja
        exif = Image.Exif()
        exif[0x0112] = 6                              # se muestra girada 90° a la derecha: la mitad roja queda ARRIBA
        estado, mensaje, enviado = self.enviar('frente', self.archivo('girada.jpg', a_bytes(crudo, 'JPEG', exif=exif, quality=95)))
        self.assertEqual(estado, 'guardada', mensaje)
        self.assertEqual((enviado['ancho'], enviado['alto']), ('300', '400'))   # como se ve, no como está el archivo
        _, imagen = self.guardado()
        self.assertEqual(imagen.size, (300, 400))
        arriba, abajo = imagen.getpixel((150, 50)), imagen.getpixel((150, 350))
        self.assertGreater(arriba[0], 200)
        self.assertLess(arriba[2], 60)
        self.assertGreater(abajo[2], 200)
        self.assertLess(abajo[0], 60)

    def test_un_png_con_transparencia_se_envia_como_jpeg_sobre_fondo_blanco(self):
        png = Image.new('RGBA', (300, 200), (0, 0, 0, 0))
        png.paste((200, 20, 20, 255), (0, 0, 150, 200))
        estado, mensaje, enviado = self.enviar('frente', self.archivo('transparente.png', a_bytes(png, 'PNG')))
        self.assertEqual(estado, 'guardada', mensaje)
        self.assertEqual(enviado['tipo'], 'image/jpeg')
        documento, imagen = self.guardado()
        self.assertEqual(documento.tipo_real_archivo, 'image/jpeg')
        claro = imagen.getpixel((250, 100))
        self.assertTrue(all(canal > 235 for canal in claro), claro)   # lo transparente quedó blanco, no negro

    def test_cada_cara_va_en_su_peticion_y_un_rechazo_no_descarta_la_otra(self):
        """CA-74 y CA-83 desde el navegador."""
        estado, mensaje, _ = self.enviar('reverso', self.archivo('reverso.jpg', a_bytes(Image.new('RGB', (400, 300), (1, 2, 3)), 'JPEG')))
        self.assertEqual(estado, 'guardada', mensaje)
        completo = a_bytes(Image.frombytes('RGB', (200, 150), os.urandom(200 * 150 * 3)), 'JPEG')
        estado, mensaje, enviado = self.enviar('frente', self.archivo('truncada.jpg', completo[:len(completo) // 2]))
        self.assertEqual(estado, 'rechazada')
        self.assertIn('dañada', mensaje)
        self.assertEqual(enviado['original'], 'si')   # el navegador no pudo reducirla y mandó el original; el servidor la rechazó
        self.assertEqual(list(DocumentoIdentidad.objects.values_list('cara', flat=True)), ['reverso'])

    def test_la_pagina_y_el_script_no_incumplen_la_politica_de_contenido(self):
        self.navegador.execute_script(
            "window.__violaciones = []; document.addEventListener('securitypolicyviolation', function (e) {"
            " window.__violaciones.push(e.violatedDirective + ' ' + e.blockedURI); });")
        estado, mensaje, _ = self.enviar('frente', self.archivo('csp.jpg', a_bytes(Image.new('RGB', (200, 100)), 'JPEG')))
        self.assertEqual(estado, 'guardada', mensaje)
        self.assertEqual(self.navegador.execute_script('return window.__violaciones;'), [])

    def test_sin_archivo_elegido_no_se_envia_nada(self):
        self.formulario('frente').find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        WebDriverWait(self.navegador, 10).until(lambda n: self.formulario('frente').get_attribute('data-estado') == 'sin-enviar')
        self.assertEqual(DocumentoIdentidad.objects.count(), 0)

    # --- CA-74: un navegador que no puede reducir
    def quitar_la_reduccion(self):
        self.navegador.execute_script(
            "HTMLCanvasElement.prototype.toBlob = undefined; window.createImageBitmap = undefined;")

    def test_un_navegador_que_no_puede_reducir_envia_el_original_si_es_jpeg_o_png_de_hasta_5_mib(self):
        self.quitar_la_reduccion()
        original = ruido(800, 600, calidad=90)
        estado, mensaje, enviado = self.enviar('frente', self.archivo('original.jpg', original))
        self.assertEqual(estado, 'guardada', mensaje)
        self.assertEqual((enviado['original'], int(enviado['bytes'])), ('si', len(original)))   # se envió tal cual
        self.assertEqual(self.guardado()[1].size, (800, 600))

    def test_un_navegador_que_no_puede_reducir_avisa_antes_de_enviar_si_pesa_mas_de_5_mib(self):
        self.quitar_la_reduccion()
        estado, mensaje, enviado = self.enviar('frente', self.archivo('enorme.jpg', ruido(4032, 3024)))
        self.assertEqual(estado, 'sin-enviar')
        self.assertIn('5 MiB', mensaje)
        self.assertEqual(DocumentoIdentidad.objects.count(), 0)   # no se hizo ninguna petición de subida
        self.assertEqual(enviado['bytes'], None)

    def test_un_navegador_que_no_puede_reducir_avisa_si_no_es_jpeg_ni_png(self):
        self.quitar_la_reduccion()
        estado, mensaje, enviado = self.enviar('frente', self.archivo('animada.gif', a_bytes(Image.new('RGB', (50, 50)), 'GIF')))
        self.assertEqual(estado, 'sin-enviar')
        self.assertIn('JPEG', mensaje)
        self.assertEqual(DocumentoIdentidad.objects.count(), 0)

    def test_lo_que_se_envia_nunca_pasa_de_5_mib_aunque_la_foto_sea_enorme(self):
        estado, mensaje, enviado = self.enviar('frente', self.archivo('muy_grande.jpg', ruido(6000, 4500, calidad=90)))
        self.assertEqual(estado, 'guardada', mensaje)
        self.assertLessEqual(int(enviado['bytes']), LIMITE)
        self.assertLessEqual(max(int(enviado['ancho']), int(enviado['alto'])), 2048)
        self.assertEqual(Auditoria.objects.filter(accion='fotografia_subida').count(), 1)
