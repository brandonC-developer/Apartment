"""Validación y limpieza de imágenes y almacenamiento privado (RF-02, ADR-003; CA-74, CA-82 en parte, CA-83)."""
import os
import stat
import sys
import tempfile
from io import BytesIO
from pathlib import Path

from django.test import SimpleTestCase, override_settings
from PIL import Image, ImageChops, ImageCms, PngImagePlugin

from . import almacenamiento
from .imagenes import MAX_PIXELES, ImagenInvalida, procesar_imagen
from .models import TAMANO_MAXIMO


def a_bytes(imagen, formato, **extra):
    salida = BytesIO()
    imagen.save(salida, formato, **extra)
    return salida.getvalue()


def degradado(ancho=64, alto=48, modo='RGB'):
    imagen = Image.new('RGB', (ancho, alto))
    imagen.putdata([(x * 4 % 256, y * 5 % 256, (x + y) * 3 % 256) for y in range(alto) for x in range(ancho)])
    return imagen.convert(modo) if modo != 'RGB' else imagen


def jpeg_con_metadatos(orientacion=1):
    exif = Image.Exif()
    exif[0x010F] = 'MarcaDeLaCamara'      # fabricante
    exif[0x0110] = 'ModeloDeLaCamara'     # modelo
    exif[0x0112] = orientacion
    exif[0x8825] = {1: 'N', 2: (9.0, 56.0, 12.0), 3: 'W', 4: (84.0, 4.0, 5.0)}  # ubicación GPS
    datos = a_bytes(degradado(), 'JPEG', exif=exif, quality=90, comment=b'COMENTARIO-PRIVADO')
    # XMP como segmento APP1 propio, tras la cabecera JPEG.
    xmp = b'http://ns.adobe.com/xap/1.0/\x00<x:xmpmeta>PERSONA-EN-XMP</x:xmpmeta>'
    return datos[:2] + b'\xff\xe1' + (len(xmp) + 2).to_bytes(2, 'big') + xmp + datos[2:]


class ImagenesTests(SimpleTestCase):
    def test_un_jpeg_y_un_png_validos_se_aceptan_y_se_reconocen_por_su_contenido(self):
        for formato, tipo in (('JPEG', 'image/jpeg'), ('PNG', 'image/png')):
            resultado = procesar_imagen(a_bytes(degradado(), formato))
            self.assertEqual((resultado.tipo, resultado.ancho, resultado.alto), (tipo, 64, 48))
            self.assertEqual(Image.open(BytesIO(resultado.contenido)).format, formato)

    def test_el_nombre_o_el_tipo_declarado_no_importan_solo_el_contenido(self):
        gif = a_bytes(degradado(), 'GIF')
        for datos in (gif, a_bytes(degradado(), 'BMP'), a_bytes(degradado(), 'TIFF'), b'%PDF-1.4 ...', b'<html><script>alert(1)</script>',
                      b'texto cualquiera', b'MZ\x90\x00 ejecutable'):
            with self.assertRaises(ImagenInvalida, msg=datos[:12]):
                procesar_imagen(datos)

    def test_vacio_y_demasiado_grande(self):
        with self.assertRaises(ImagenInvalida):
            procesar_imagen(b'')
        with self.assertRaises(ImagenInvalida) as e:
            procesar_imagen(b'\xff\xd8' + b'0' * TAMANO_MAXIMO)
        self.assertIn('5 MiB', str(e.exception))

    def test_un_archivo_justo_en_el_limite_de_peso_no_se_rechaza_por_peso(self):
        # El límite es de 5 242 880 bytes: un archivo de ese peso llega a la decodificación (y falla por no ser imagen).
        with self.assertRaises(ImagenInvalida) as e:
            procesar_imagen(b'0' * TAMANO_MAXIMO)
        self.assertNotIn('5 MiB', str(e.exception))

    def test_un_archivo_truncado_o_danado_se_rechaza_cuando_no_se_puede_decodificar_completo(self):
        """CA-83."""
        for formato in ('JPEG', 'PNG'):
            completo = a_bytes(degradado(200, 150), formato)
            procesar_imagen(completo)  # íntegro: se acepta
            with self.assertRaises(ImagenInvalida, msg=f'{formato} truncado') as e:
                procesar_imagen(completo[:len(completo) // 2])
            self.assertTrue(str(e.exception))
            danado = bytearray(completo)
            danado[len(danado) // 3:len(danado) // 3 + 40] = b'\x00' * 40
            try:
                procesar_imagen(bytes(danado))
            except ImagenInvalida:
                pass  # lo dañado se rechaza o, si todavía decodifica, sale limpio

    def test_una_bomba_de_descompresion_se_rechaza_antes_de_decodificar(self):
        bomba = a_bytes(Image.new('1', (20000, 10000)), 'PNG')  # 200 millones de píxeles en pocos KiB
        self.assertLess(len(bomba), TAMANO_MAXIMO)
        self.assertGreater(20000 * 10000, MAX_PIXELES)
        with self.assertRaises(ImagenInvalida) as e:
            procesar_imagen(bomba)
        self.assertIn('píxeles', str(e.exception))

    def test_los_metadatos_no_llegan_al_archivo_guardado(self):
        """BR-05: ubicación, cámara, comentario y XMP."""
        original = jpeg_con_metadatos()
        for marca in (b'MarcaDeLaCamara', b'COMENTARIO-PRIVADO', b'PERSONA-EN-XMP', b'Exif'):
            self.assertIn(marca, original)  # el original sí los trae
        limpio = procesar_imagen(original).contenido
        for marca in (b'MarcaDeLaCamara', b'ModeloDeLaCamara', b'COMENTARIO-PRIVADO', b'PERSONA-EN-XMP', b'Exif', b'xmp', b'XMP'):
            self.assertNotIn(marca, limpio, marca)
        resultado = Image.open(BytesIO(limpio))
        self.assertEqual(len(resultado.getexif()), 0)
        self.assertEqual(resultado.getexif().get_ifd(0x8825), {})
        self.assertNotIn('comment', resultado.info)

    def test_un_png_pierde_sus_bloques_de_texto(self):
        informacion = PngImagePlugin.PngInfo()
        informacion.add_text('Autor', 'PERSONA-EN-PNG')
        informacion.add_itxt('XML:com.adobe.xmp', 'PERSONA-EN-XMP-PNG')
        original = a_bytes(degradado(), 'PNG', pnginfo=informacion)
        self.assertIn(b'PERSONA-EN-PNG', original)
        limpio = procesar_imagen(original).contenido
        for marca in (b'PERSONA-EN-PNG', b'PERSONA-EN-XMP-PNG', b'tEXt', b'iTXt'):
            self.assertNotIn(marca, limpio, marca)

    def test_lo_que_se_guarda_no_es_el_archivo_recibido_los_datos_añadidos_al_final_desaparecen(self):
        original = a_bytes(degradado(), 'JPEG') + b'<?php system($_GET["c"]); ?>' + b'\x00' * 10
        limpio = procesar_imagen(original).contenido
        self.assertNotIn(b'<?php', limpio)
        self.assertNotEqual(original, limpio)
        png = a_bytes(degradado(), 'PNG') + b'<script>alert(1)</script>'
        self.assertNotIn(b'<script>', procesar_imagen(png).contenido)

    def test_se_aplica_la_orientacion_y_se_quita_la_marca(self):
        """RF-50: conservar la orientación visible."""
        original = a_bytes(degradado(40, 20), 'JPEG', exif=self._exif_orientacion(6))
        resultado = procesar_imagen(original)
        self.assertEqual((resultado.ancho, resultado.alto), (20, 40))  # girada 90°
        self.assertEqual(Image.open(BytesIO(resultado.contenido)).getexif().get(0x0112), None)

    def _mpo(self, orientacion=1, ancho=64, alto=48):
        """Un JPEG con varias imágenes (MPO), como el de un iPhone, un Pixel o un Samsung: la primera es la foto y la
        segunda hace de mapa de ganancia o miniatura."""
        exif = Image.Exif()
        exif[0x010F] = 'MarcaDelTelefono'
        exif[0x0112] = orientacion
        salida = BytesIO()
        degradado(ancho, alto).save(salida, 'MPO', save_all=True, append_images=[degradado(16, 12)], exif=exif)
        return salida.getvalue()

    def test_un_jpeg_con_varias_imagenes_mpo_se_acepta_y_solo_queda_la_primera(self):
        """Hallazgo con fotos reales de un iPhone 14 Pro, un Galaxy S23 y un Pixel 8 (actualización 2026-10-26b):
        Pillow los llama «MPO» y antes esto fallaba con un KeyError (error 500)."""
        original = self._mpo()
        self.assertEqual(Image.open(BytesIO(original)).format, 'MPO')
        self.assertEqual(Image.open(BytesIO(original)).n_frames, 2)
        for orientacion in (1, 6):
            resultado = procesar_imagen(self._mpo(orientacion))
            self.assertEqual(resultado.tipo, 'image/jpeg')
            guardada = Image.open(BytesIO(resultado.contenido))
            self.assertEqual(guardada.format, 'JPEG')       # un JPEG común, no un MPO
            self.assertEqual(getattr(guardada, 'n_frames', 1), 1)
            self.assertNotIn(b'MarcaDelTelefono', resultado.contenido)
            self.assertNotIn(b'MPF', resultado.contenido)    # sin la extensión de varias imágenes
        self.assertEqual((procesar_imagen(self._mpo(6, 40, 20)).ancho, procesar_imagen(self._mpo(6, 40, 20)).alto), (20, 40))

    def test_un_mpo_truncado_se_rechaza_como_cualquier_jpeg(self):
        with self.assertRaises(ImagenInvalida):
            procesar_imagen(self._mpo(ancho=400, alto=300)[:300])

    @staticmethod
    def _exif_orientacion(valor):
        exif = Image.Exif()
        exif[0x0112] = valor
        return exif

    def test_sin_girar_el_jpeg_conserva_las_tablas_de_calidad_y_casi_los_mismos_pixeles(self):
        """No es una transcodificación sin pérdida: Pillow vuelve a codificar desde los píxeles, pero con las mismas
        tablas de calidad (`keep`), así que el peso y el aspecto casi no cambian. Se mide con una imagen sintética
        muy ruidosa (el caso malo); con fotos reales se compara en la medición del grupo G."""
        from PIL import ImageStat
        original = a_bytes(degradado(160, 120), 'JPEG', quality=70)
        limpio = procesar_imagen(original).contenido
        diferencia = ImageChops.difference(Image.open(BytesIO(original)).convert('RGB'), Image.open(BytesIO(limpio)).convert('RGB'))
        self.assertLess(max(ImageStat.Stat(diferencia).mean), 5)  # diferencia media de unos 2-3 niveles de 255
        self.assertLess(abs(len(limpio) - len(original)) / len(original), 0.05)  # el peso casi no cambia
        recomprimido_a_95 = BytesIO()
        Image.open(BytesIO(original)).save(recomprimido_a_95, 'JPEG', quality=95)
        self.assertLess(len(limpio), len(recomprimido_a_95.getvalue()))  # y no infla el archivo como lo haría una calidad fija alta

    def test_se_conserva_el_perfil_de_color_que_no_es_un_dato_personal(self):
        perfil = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
        for formato in ('JPEG', 'PNG'):
            original = a_bytes(degradado(), formato, icc_profile=perfil)
            limpio = Image.open(BytesIO(procesar_imagen(original).contenido))
            self.assertEqual(limpio.info.get('icc_profile'), perfil, formato)

    def test_modos_de_color_habituales(self):
        casos = [(degradado(modo='L'), 'JPEG'), (degradado(modo='CMYK'), 'JPEG'), (degradado(modo='RGBA'), 'PNG'),
                 (degradado(modo='L'), 'PNG'), (degradado().convert('P', palette=Image.ADAPTIVE), 'PNG'),
                 (Image.new('1', (30, 30)), 'PNG')]
        for imagen, formato in casos:
            resultado = procesar_imagen(a_bytes(imagen, formato))
            Image.open(BytesIO(resultado.contenido)).load()  # el resultado se decodifica
            self.assertEqual(resultado.tipo, 'image/jpeg' if formato == 'JPEG' else 'image/png')

    def test_png_con_transparencia_en_paleta_la_conserva(self):
        imagen = Image.new('P', (10, 10), 0)
        imagen.putpalette([255, 0, 0, 0, 255, 0] + [0] * 250)
        resultado = procesar_imagen(a_bytes(imagen, 'PNG', transparency=0))
        self.assertEqual(Image.open(BytesIO(resultado.contenido)).convert('RGBA').getpixel((0, 0))[3], 0)

    def test_la_extension_sale_del_tipo_real(self):
        self.assertEqual(procesar_imagen(a_bytes(degradado(), 'JPEG')).extension, 'jpg')
        self.assertEqual(procesar_imagen(a_bytes(degradado(), 'PNG')).extension, 'png')

    def test_una_imagen_que_crece_mas_alla_de_5_mib_al_procesarse_se_rechaza(self):
        from unittest.mock import patch

        def inflar(self, destino, *args, **kwargs):
            destino.write(b'0' * (TAMANO_MAXIMO + 1))  # simula una reescritura que pesa más que el límite
        entradas = {formato: a_bytes(degradado(30, 30), formato) for formato in ('JPEG', 'PNG')}  # antes del parche
        with patch.object(Image.Image, 'save', inflar):
            for formato, datos in entradas.items():
                with self.assertRaises(ImagenInvalida, msg=formato) as e:
                    procesar_imagen(datos)
                self.assertIn('después de limpiarla', str(e.exception))


class AlmacenamientoTests(SimpleTestCase):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(self.carpeta.cleanup)
        self.enterContext(override_settings(RAIZ_DOCUMENTOS=self.carpeta.name))

    def test_guarda_con_nombre_aleatorio_y_se_puede_leer_y_borrar(self):
        a = almacenamiento.guardar(b'uno', 'jpg')
        b = almacenamiento.guardar(b'uno', 'png')
        self.assertNotEqual(a, b)
        self.assertRegex(a, r'^[0-9a-f]{32}\.jpg$')
        self.assertRegex(b, r'^[0-9a-f]{32}\.png$')
        with almacenamiento.abrir(a) as archivo:
            self.assertEqual(archivo.read(), b'uno')
        self.assertTrue(almacenamiento.existe(a))
        self.assertTrue(almacenamiento.borrar(a))
        self.assertFalse(almacenamiento.borrar(a))  # ya no está: no falla
        self.assertFalse(almacenamiento.existe(a))
        with self.assertRaises(FileNotFoundError):
            almacenamiento.abrir(a)

    def test_el_nombre_no_contiene_nada_del_contenido_ni_del_inquilino(self):
        referencia = almacenamiento.guardar(b'contenido', 'jpg')
        self.assertTrue(Path(self.carpeta.name, 'cedulas', referencia).is_file())
        self.assertEqual(os.listdir(Path(self.carpeta.name)), ['cedulas'])

    def test_una_referencia_con_forma_distinta_a_la_generada_se_rechaza(self):
        for mala in ('../x.jpg', '..\\x.jpg', '/etc/passwd', 'a.jpg', 'A' * 32 + '.jpg', 'g' * 32 + '.jpg', '0' * 32 + '.gif',
                     '0' * 32 + '.jpg/../x', '0' * 31 + '.jpg', '0' * 32 + '.JPG', ('0' * 32 + '.jpg\x00'), '', None, 5,
                     'cedulas/' + '0' * 32 + '.jpg'):
            with self.assertRaises(almacenamiento.ReferenciaInvalida, msg=repr(mala)):
                almacenamiento.abrir(mala)
            self.assertFalse(almacenamiento.existe(mala))
            self.assertFalse(almacenamiento.borrar(mala))

    def test_una_extension_no_permitida_no_se_guarda(self):
        for extension in ('gif', 'php', '', None, 'jpg/../x'):
            with self.assertRaises(almacenamiento.ReferenciaInvalida):
                almacenamiento.guardar(b'x', extension)
        self.assertEqual(os.listdir(self.carpeta.name), [])

    def test_los_permisos_son_de_solo_el_dueno_y_el_grupo(self):
        if sys.platform == 'win32':
            self.skipTest('Los permisos POSIX no se comprueban en Windows.')
        referencia = almacenamiento.guardar(b'x', 'jpg')
        modo_archivo = stat.S_IMODE(os.stat(Path(self.carpeta.name, 'cedulas', referencia)).st_mode)
        modo_carpeta = stat.S_IMODE(os.stat(Path(self.carpeta.name, 'cedulas')).st_mode)
        self.assertEqual(modo_archivo & 0o007, 0)   # nada para otros
        self.assertEqual(modo_carpeta & 0o007, 0)
        self.assertEqual(modo_archivo & 0o200, 0o200)


class AlmacenamientoConFalloTests(SimpleTestCase):
    def test_si_falla_al_escribir_no_queda_un_archivo_parcial(self):
        """Un disco lleno o un fallo de `fsync` no deja un archivo huérfano en el almacenamiento privado."""
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as carpeta, override_settings(RAIZ_DOCUMENTOS=carpeta):
            with patch('inquilinos.almacenamiento.os.fsync', side_effect=OSError('disco lleno')):
                with self.assertRaises(OSError):
                    almacenamiento.guardar(b'contenido', 'jpg')
            self.assertEqual([p for p in Path(carpeta).rglob('*') if p.is_file()], [])
