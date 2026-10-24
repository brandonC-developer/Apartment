"""Fotografías del documento: subida, reemplazo, entrega autorizada y su auditoría (E1, grupo D).
RF-01, RF-02, RF-03, RF-39, RF-45; CA-11, CA-26, CA-74, CA-83. Necesitan PostgreSQL."""
import os
import tempfile
import time
from datetime import timedelta
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from cuentas.models import Administrador
from nucleo.models import Auditoria

from . import almacenamiento, services
from .models import AccesoDocumento, Consentimiento, DocumentoIdentidad, Inquilino, TextoConsentimiento
from .services import ErrorDeValidacion
from .tests import AHORA
from .tests_imagenes import a_bytes, degradado, jpeg_con_metadatos
from .tests_servicios import DATOS


def archivos_en(raiz):
    return sorted(p.name for p in Path(raiz, 'cedulas').glob('*')) if Path(raiz, 'cedulas').exists() else []


class Base(TestCase):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(self.carpeta.cleanup)
        self.enterContext(override_settings(RAIZ_DOCUMENTOS=self.carpeta.name))
        self.texto = TextoConsentimiento.objects.create(version=1, contenido='Texto', vigente_desde=AHORA)
        self.inquilino = services.registrar_inquilino(
            actor='admin', datos=dict(DATOS, telefono='8888-8888'), texto=self.texto, medio='fisico', ahora=AHORA)

    def subir(self, cara='frente', contenido=None, **extra):
        return services.subir_fotografia(
            self.inquilino.pk, cara=cara, contenido=contenido if contenido is not None else a_bytes(degradado(), 'JPEG'), actor='admin',
            ip_origen='203.0.113.5', **extra)

    def archivos(self):
        return archivos_en(self.carpeta.name)


class SubirFotografiaTests(Base):
    def test_se_guarda_limpia_con_nombre_aleatorio_y_su_registro(self):
        original = jpeg_con_metadatos()
        d = self.subir(contenido=original)
        d.refresh_from_db()
        self.assertTrue(d.activo)
        self.assertEqual((d.cara, d.tipo_real_archivo, d.inquilino), ('frente', 'image/jpeg', self.inquilino))
        self.assertRegex(d.referencia_archivo, r'^[0-9a-f]{32}\.jpg$')
        with almacenamiento.abrir(d.referencia_archivo) as f:
            guardado = f.read()
        self.assertEqual(d.tamano_bytes, len(guardado))
        self.assertNotEqual(guardado, original)           # lo que se guarda no es lo recibido...
        for marca in (b'MarcaDeLaCamara', b'COMENTARIO-PRIVADO', b'PERSONA-EN-XMP'):
            self.assertNotIn(marca, guardado)              # ...ni conserva los metadatos
        self.assertEqual(self.archivos(), [d.referencia_archivo])

    def test_deja_su_auditoria_sin_la_imagen_ni_datos_personales(self):
        self.subir()
        r = Auditoria.objects.get(accion='fotografia_subida')
        self.assertEqual((r.actor, r.ip_origen, r.registro_id, r.valor_nuevo), ('admin', '203.0.113.5', self.inquilino.pk, {'cara': 'frente'}))
        self.assertIn('fotografia', r.campos_modificados)
        todo = str(list(Auditoria.objects.values()))
        for dato in ('Nombre Apellido', '1-1111-1111', '8888-8888'):
            self.assertNotIn(dato, todo)

    def test_un_archivo_rechazado_no_deja_nada_y_no_toca_el_otro_ya_aceptado(self):
        """CA-74 y CA-83: el rechazo de un archivo no descarta el otro."""
        reverso = self.subir('reverso')
        completo = a_bytes(degradado(200, 150), 'JPEG')
        for malo in (b'', b'no es una imagen', a_bytes(degradado(), 'GIF'), completo[:len(completo) // 2], b'\xff\xd8' + b'0' * (5 * 1024 * 1024)):
            with self.assertRaises(ErrorDeValidacion, msg=malo[:10]) as e:
                self.subir('frente', malo)
            self.assertIn('archivo', e.exception.errores)
        self.assertEqual(DocumentoIdentidad.objects.count(), 1)
        self.assertEqual(self.archivos(), [reverso.referencia_archivo])
        self.assertTrue(DocumentoIdentidad.objects.get(pk=reverso.pk).activo)
        self.assertEqual(Auditoria.objects.filter(accion__startswith='fotografia').count(), 1)

    def test_sin_consentimiento_vigente_no_se_guardan_fotografias(self):
        """RF-39: antes de guardar la fotografía de cédula."""
        services.revocar_consentimiento(self.inquilino.pk, actor='admin', ahora=AHORA + timedelta(days=1))
        with self.assertRaises(ErrorDeValidacion) as e:
            self.subir()
        self.assertIn('consentimiento', e.exception.errores)
        self.assertEqual((DocumentoIdentidad.objects.count(), self.archivos()), (0, []))

    def test_la_cara_debe_ser_frente_o_reverso_y_el_inquilino_existir_y_no_estar_desasociado(self):
        with self.assertRaises(ErrorDeValidacion):
            self.subir('lateral')
        with self.assertRaises(Inquilino.DoesNotExist):
            services.subir_fotografia(999999, cara='frente', contenido=a_bytes(degradado(), 'JPEG'), actor='admin')
        Inquilino.objects.filter(pk=self.inquilino.pk).update(
            nombre_completo=None, numero_documento=None, telefono=None, correo=None, desasociado_en=AHORA)
        with self.assertRaises(ErrorDeValidacion):
            self.subir()
        self.assertEqual(self.archivos(), [])

    def test_reemplazar_marca_la_anterior_como_eliminada_y_borra_su_archivo_al_confirmar(self):
        primera = self.subir()
        with self.captureOnCommitCallbacks(execute=True):
            segunda = self.subir(contenido=a_bytes(degradado(30, 30), 'PNG'))
        primera.refresh_from_db()
        self.assertFalse(primera.activo)
        self.assertTrue(segunda.activo)
        self.assertEqual(segunda.tipo_real_archivo, 'image/png')
        self.assertEqual(self.archivos(), [segunda.referencia_archivo])   # la anterior ya no está en el disco
        self.assertEqual(DocumentoIdentidad.objects.filter(inquilino=self.inquilino, cara='frente', eliminado_en__isnull=True).count(), 1)
        self.assertEqual(Auditoria.objects.filter(accion='fotografia_reemplazada').count(), 1)

    def test_si_la_base_falla_el_archivo_recien_guardado_se_borra_y_la_anterior_sigue_activa(self):
        """HI-07: sin archivos huérfanos."""
        primera = self.subir()
        with patch('inquilinos.services.auditoria.registrar', side_effect=RuntimeError('falla')):
            with self.assertRaises(RuntimeError):
                self.subir(contenido=a_bytes(degradado(20, 20), 'JPEG'))
        self.assertEqual(self.archivos(), [primera.referencia_archivo])
        self.assertTrue(DocumentoIdentidad.objects.get(pk=primera.pk).activo)
        self.assertEqual(DocumentoIdentidad.objects.count(), 1)

    def test_si_falla_el_guardado_en_disco_no_queda_nada_a_medias(self):
        with patch('inquilinos.services.almacenamiento.guardar', side_effect=OSError('disco lleno')):
            with self.assertRaises(OSError):
                self.subir()
        self.assertEqual((DocumentoIdentidad.objects.count(), self.archivos()), (0, []))

    def test_una_fotografia_de_un_inquilino_inactivo_se_acepta(self):
        services.desactivar_inquilino(self.inquilino.pk, actor='admin')
        self.subir()


class Navegador(TestCase):
    """Base con sesión iniciada sin pasar por el segundo factor (ya probado)."""

    def entrar(self, cliente=None):
        cliente = cliente or self.client
        admin = Administrador.objects.filter(pk=1).first() or Administrador.objects.crear_administrador('admin', 'una contrasena larga de prueba')
        cliente.force_login(admin, backend='cuentas.backends.BackendAdministrador')
        sesion = cliente.session
        sesion['sesion_inicio'] = sesion['sesion_ultima'] = time.time()
        sesion.save()
        return cliente


class SubirPorHttpTests(Base, Navegador):
    def url(self, cara='frente', inquilino=None):
        return f'/inquilinos/{(inquilino or self.inquilino).pk}/fotografias/{cara}/'

    def publicar(self, cara='frente', contenido=None, nombre='foto.jpg', cliente=None, **campos):
        archivo = SimpleUploadedFile(nombre, contenido or a_bytes(degradado(), 'JPEG'), content_type='image/jpeg')
        return (cliente or self.client).post(self.url(cara), {'archivo': archivo, **campos})

    def test_sin_sesion_se_niega_y_no_se_guarda_nada(self):
        r = self.publicar()
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r['Location'].startswith('/entrar/'))
        self.assertEqual((DocumentoIdentidad.objects.count(), self.archivos()), (0, []))

    def test_exige_el_token_csrf(self):
        cliente = self.entrar(Client(enforce_csrf_checks=True))
        self.assertEqual(self.publicar(cliente=cliente).status_code, 403)
        self.assertEqual(DocumentoIdentidad.objects.count(), 0)

    def test_con_sesion_guarda_y_responde_con_los_datos(self):
        self.entrar()
        r = self.publicar()
        self.assertEqual(r.status_code, 201)
        datos = r.json()
        self.assertEqual((datos['cara'], datos['tipo']), ('frente', 'image/jpeg'))
        self.assertEqual(DocumentoIdentidad.objects.get().pk, datos['id'])

    def test_solo_acepta_post(self):
        self.entrar()
        for metodo in (self.client.get, self.client.put, self.client.delete):
            self.assertEqual(metodo(self.url()).status_code, 405)

    def test_un_solo_archivo_por_peticion(self):
        self.entrar()
        uno = SimpleUploadedFile('a.jpg', a_bytes(degradado(), 'JPEG'), content_type='image/jpeg')
        dos = SimpleUploadedFile('b.jpg', a_bytes(degradado(), 'JPEG'), content_type='image/jpeg')
        for datos in ({'archivo': [uno, dos]}, {'archivo': uno, 'otro': dos}, {}, {'otro': dos}):
            r = self.client.post(self.url(), datos)
            self.assertEqual(r.status_code, 400, datos)
            self.assertIn('archivo', r.json()['errores'])
        self.assertEqual((DocumentoIdentidad.objects.count(), self.archivos()), (0, []))

    def test_mas_de_5_mib_se_rechaza_con_un_mensaje_y_sin_guardar(self):
        """CA-74."""
        self.entrar()
        r = self.publicar(contenido=b'\xff\xd8' + b'0' * (5 * 1024 * 1024))
        self.assertEqual(r.status_code, 400)
        self.assertIn('5 MiB', r.json()['errores']['archivo'][0])
        self.assertEqual((DocumentoIdentidad.objects.count(), self.archivos()), (0, []))

    def test_un_tipo_real_distinto_se_rechaza_aunque_el_nombre_y_el_tipo_declarado_digan_jpeg(self):
        """CA-74."""
        self.entrar()
        for falso in (b'<html><script>alert(1)</script></html>', a_bytes(degradado(), 'GIF'), b'%PDF-1.4'):
            r = self.publicar(contenido=falso, nombre='cedula.jpg')
            self.assertEqual(r.status_code, 400)
        self.assertEqual(DocumentoIdentidad.objects.count(), 0)

    def test_el_rechazo_de_un_archivo_no_descarta_el_otro_ya_aceptado(self):
        """CA-74 y CA-83."""
        self.entrar()
        self.assertEqual(self.publicar('reverso').status_code, 201)
        completo = a_bytes(degradado(200, 150), 'JPEG')
        r = self.publicar('frente', contenido=completo[:len(completo) // 2])
        self.assertEqual(r.status_code, 400)
        self.assertIn('dañada', r.json()['errores']['archivo'][0])
        self.assertEqual(DocumentoIdentidad.objects.get().cara, 'reverso')
        self.assertEqual(self.publicar('frente', contenido=completo).status_code, 201)  # un JPEG íntegro se acepta
        self.assertEqual(DocumentoIdentidad.objects.count(), 2)

    def test_cara_invalida_inquilino_inexistente_y_consentimiento_revocado(self):
        self.entrar()
        r = self.client.post(self.url('lateral'), {'archivo': SimpleUploadedFile('a.jpg', a_bytes(degradado(), 'JPEG'))})
        self.assertEqual(r.status_code, 400)
        self.assertIn('cara', r.json()['errores'])
        r = self.client.post('/inquilinos/999999/fotografias/frente/', {'archivo': SimpleUploadedFile('a.jpg', a_bytes(degradado(), 'JPEG'))})
        self.assertEqual(r.status_code, 404)
        services.revocar_consentimiento(self.inquilino.pk, actor='admin', ahora=AHORA + timedelta(days=1))
        r = self.publicar()
        self.assertEqual(r.status_code, 400)
        self.assertIn('consentimiento', r.json()['errores'])


class EntregarPorHttpTests(Base, Navegador):
    def setUp(self):
        super().setUp()
        self.documento = self.subir()
        with almacenamiento.abrir(self.documento.referencia_archivo) as f:
            self.guardado = f.read()

    def obtener(self, ruta, cliente=None):
        """Pide la ruta y cierra la respuesta al terminar (la de un archivo deja el archivo abierto)."""
        r = (cliente or self.client).get(ruta)
        # No se usa `r.close()`: emite `request_finished`, que cierra la conexión de la prueba. Se cierra solo el archivo
        # (el cliente de pruebas envuelve el contenido y `file_to_stream` queda vacío; el cierre está en `_resource_closers`).
        self.addCleanup(lambda: [cerrar() for cerrar in getattr(r, '_resource_closers', [])])
        return r

    def test_sin_sesion_se_deniega_y_el_archivo_no_sale(self):
        """CA-11."""
        for ruta in (f'/inquilinos/documentos/{self.documento.pk}/ver/', f'/inquilinos/documentos/{self.documento.pk}/descargar/'):
            r = self.obtener(ruta, Client())
            self.assertEqual(r.status_code, 302)
            self.assertTrue(r['Location'].startswith('/entrar/'))
            self.assertNotIn(self.guardado[:20], r.content)
        self.assertEqual(AccesoDocumento.objects.count(), 0)

    def test_no_hay_ninguna_url_publica_del_archivo(self):
        """CA-11: ni el nombre guardado ni una ruta de archivos estáticos o de medios sirven la imagen."""
        referencia = self.documento.referencia_archivo
        self.entrar()
        for ruta in (f'/media/{referencia}', f'/static/{referencia}', f'/{referencia}', f'/cedulas/{referencia}',
                     f'/inquilinos/documentos/{referencia}/ver/', f'/inquilinos/documentos/../{referencia}/ver/'):
            self.assertEqual(self.obtener(ruta).status_code, 404, ruta)

    def test_con_sesion_entrega_la_imagen_y_registra_quien_cuando_y_que_sin_la_imagen(self):
        """CA-26."""
        self.entrar()
        antes = timezone.now()
        r = self.obtener(f'/inquilinos/documentos/{self.documento.pk}/ver/')
        despues = timezone.now()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(b''.join(r.streaming_content), self.guardado)
        self.assertEqual(r['Content-Type'], 'image/jpeg')
        acceso = AccesoDocumento.objects.get()
        self.assertEqual((acceso.actor, acceso.accion, acceso.documento), ('admin', 'consulta', self.documento))
        self.assertTrue(antes <= acceso.ocurrido_en <= despues)
        self.assertNotIn(self.guardado[:20], str(list(AccesoDocumento.objects.values())).encode())

    def test_las_cabeceras_no_dejan_que_se_guarde_ni_se_interprete(self):
        self.entrar()
        r = self.obtener(f'/inquilinos/documentos/{self.documento.pk}/ver/')
        self.assertEqual(r['X-Content-Type-Options'], 'nosniff')
        self.assertIn('no-store', r['Cache-Control'])
        self.assertIn('private', r['Cache-Control'])
        self.assertTrue(r['Content-Disposition'].startswith('inline'))
        self.assertIn(f'documento-{self.documento.pk}.jpg', r['Content-Disposition'])
        for dato in ('Nombre', '1-1111', self.documento.referencia_archivo):
            self.assertNotIn(dato, r['Content-Disposition'])

    def test_descargar_es_otra_accion_y_va_como_adjunto(self):
        self.entrar()
        r = self.obtener(f'/inquilinos/documentos/{self.documento.pk}/descargar/')
        self.assertTrue(r['Content-Disposition'].startswith('attachment'))
        self.assertEqual(AccesoDocumento.objects.get().accion, 'descarga')

    def test_cada_consulta_deja_su_propio_registro(self):
        self.entrar()
        for _ in range(3):
            self.obtener(f'/inquilinos/documentos/{self.documento.pk}/ver/')
        self.assertEqual(AccesoDocumento.objects.count(), 3)

    def test_una_fotografia_reemplazada_o_inexistente_no_se_entrega_ni_se_registra(self):
        self.entrar()
        with self.captureOnCommitCallbacks(execute=True):
            self.subir()  # reemplaza el frente
        self.assertEqual(self.obtener(f'/inquilinos/documentos/{self.documento.pk}/ver/').status_code, 404)
        self.assertEqual(self.obtener('/inquilinos/documentos/999999/ver/').status_code, 404)
        self.assertEqual(AccesoDocumento.objects.count(), 0)

    def test_si_falta_el_archivo_en_el_disco_responde_404_sin_registrar_un_acceso(self):
        self.entrar()
        almacenamiento.borrar(self.documento.referencia_archivo)
        with self.assertLogs('sga.documentos', 'ERROR'):
            self.assertEqual(self.obtener(f'/inquilinos/documentos/{self.documento.pk}/ver/').status_code, 404)
        self.assertEqual(AccesoDocumento.objects.count(), 0)

    def test_si_no_se_puede_registrar_el_acceso_no_se_entrega_la_imagen(self):
        """RF-45: sin registro no hay imagen."""
        self.entrar()
        abierto = []
        original = almacenamiento.abrir

        def espia(referencia):
            archivo = original(referencia)
            abierto.append(archivo)
            return archivo
        with patch('inquilinos.views.almacenamiento.abrir', side_effect=espia), \
                patch('inquilinos.views.services.registrar_acceso', side_effect=RuntimeError('falla')):
            with self.assertRaises(RuntimeError):
                self.obtener(f'/inquilinos/documentos/{self.documento.pk}/ver/')
        self.assertTrue(abierto and all(a.closed for a in abierto))   # el archivo se cierra
        self.assertEqual(AccesoDocumento.objects.count(), 0)

    def test_solo_get(self):
        self.entrar()
        for metodo in (self.client.post, self.client.put, self.client.delete):
            self.assertEqual(metodo(f'/inquilinos/documentos/{self.documento.pk}/ver/').status_code, 405)


class NginxTests(TestCase):
    def test_el_cuerpo_grande_solo_se_admite_en_la_ruta_de_subida(self):
        """ADR-003: 6 MiB solo para subir una fotografía y 1 MiB en el resto."""
        from django.conf import settings
        sitio = (Path(settings.BASE_DIR) / 'despliegue/nginx/sga-sitio.conf').read_text(encoding='utf-8')
        self.assertEqual(sitio.count('client_max_body_size 6m;'), 1)
        self.assertIn('client_max_body_size 1m;', sitio)
        bloque = sitio.split('location ~ ^/inquilinos/[0-9]+/fotografias/(frente|reverso)/$ {')[1].split('}')[0]
        self.assertIn('client_max_body_size 6m;', bloque)
        self.assertIn('sga-proxy.conf', bloque)
