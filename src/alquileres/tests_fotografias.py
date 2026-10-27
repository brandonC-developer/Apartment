"""Fotografías del contrato y cédula desde el perfil de la propiedad (RF-51, RF-52, RF-02, RF-45; CA-75, CA-76, CA-77,
CA-82). Necesitan PostgreSQL."""
import tempfile
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import Client, override_settings
from django.utils import timezone
from PIL import Image

from inquilinos import almacenamiento, services as servicios_de_inquilinos
from inquilinos.models import DocumentoIdentidad
from inquilinos.tests_fotografias import Navegador
from inquilinos.tests_imagenes import a_bytes, degradado, jpeg_con_metadatos
from nucleo.models import Auditoria

from . import fotografias, selectors
from .models import AccesoDocumentoContrato, DocumentoContrato, Propiedad
from .tests_servicios import AHORA, Base, d


def jpeg():
    return a_bytes(degradado(), 'JPEG')


def archivos_de(raiz, subcarpeta):
    carpeta = Path(raiz, subcarpeta)
    return sorted(p.name for p in carpeta.glob('*')) if carpeta.exists() else []


class BaseDeFotografias(Base):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(self.carpeta.cleanup)
        self.enterContext(override_settings(RAIZ_DOCUMENTOS=self.carpeta.name))
        super().setUp()
        self.contrato = self.crear(fecha_inicio=d('2026-01-01')).contrato   # vigente hoy

    def subir(self, contrato=None, contenido=None, **extra):
        return fotografias.subir_fotografia_del_contrato(
            (contrato or self.contrato).pk, contenido=contenido if contenido is not None else jpeg(), actor='admin',
            ip_origen='203.0.113.5', ahora=AHORA, **extra)

    def del_contrato(self):
        return archivos_de(self.carpeta.name, 'contratos')

    def de_cedulas(self):
        return archivos_de(self.carpeta.name, 'cedulas')

    def subir_cedula(self, cara='frente', propiedad=None, contenido=None):
        return fotografias.subir_cedula_desde_la_propiedad(
            (propiedad or self.propiedad).pk, cara=cara, contenido=contenido if contenido is not None else jpeg(),
            actor='admin', ip_origen='203.0.113.5', ahora=AHORA)

    def errores(self, funcion, **extra):
        with self.assertRaises(fotografias.ErrorDeValidacion) as contexto:
            funcion(**extra)
        return contexto.exception.errores


class FotografiaDelContratoTests(BaseDeFotografias):
    def test_se_guarda_limpia_en_la_carpeta_de_contratos_con_nombre_aleatorio(self):
        documento = self.subir(contenido=jpeg_con_metadatos())
        documento.refresh_from_db()
        self.assertEqual((documento.contrato, documento.orden, documento.tipo_real_archivo), (self.contrato, 1, 'image/jpeg'))
        self.assertRegex(documento.referencia_archivo, r'^[0-9a-f]{32}\.jpg$')
        self.assertEqual(self.del_contrato(), [documento.referencia_archivo])
        self.assertNotIn(documento.referencia_archivo, self.de_cedulas())

    def test_ca_82_los_metadatos_no_llegan_al_archivo_guardado(self):
        documento = self.subir(contenido=jpeg_con_metadatos())
        with almacenamiento.abrir(documento.referencia_archivo, 'contratos') as f:
            guardado = f.read()
        for marca in (b'MarcaDeLaCamara', b'COMENTARIO-PRIVADO', b'PERSONA-EN-XMP', b'Exif'):
            self.assertNotIn(marca, guardado)
        self.assertEqual(Image.open(BytesIO(guardado)).getexif().get_ifd(0x8825), {})   # sin ubicación

    def test_se_numeran_de_1_a_n(self):
        self.assertEqual([self.subir().orden for _ in range(3)], [1, 2, 3])

    def test_ca_76_la_numero_11_se_rechaza_con_un_mensaje_y_se_conservan_las_10(self):
        for _ in range(10):
            self.subir()
        errores = self.errores(self.subir)
        self.assertIn('máximo', errores['archivo'][0])
        self.assertIn('10', errores['archivo'][0])
        self.assertEqual(DocumentoContrato.objects.filter(contrato=self.contrato).count(), 10)
        self.assertEqual(len(self.del_contrato()), 10)   # la rechazada no dejó un archivo

    def test_el_limite_es_por_contrato(self):
        for _ in range(10):
            self.subir()
        otro = self.contrato_directo(inicio='2025-01-01', fin='2025-12-31')
        self.assertEqual(self.subir(contrato=otro).orden, 1)

    def test_ca_76_un_archivo_rechazado_no_guarda_nada_y_no_toca_los_ya_guardados(self):
        self.subir()
        for malo in (b'', b'esto no es una imagen', b'GIF89a' + b'\x00' * 50, b'\xff\xd8\xff' + b'\x00' * (5 * 1024 * 1024)):
            with self.assertRaises(fotografias.ErrorDeValidacion):
                self.subir(contenido=malo)
        self.assertEqual(DocumentoContrato.objects.count(), 1)
        self.assertEqual(len(self.del_contrato()), 1)

    def test_ca_76_no_crea_ni_modifica_la_cedula_y_la_cedula_no_toca_el_contrato(self):
        cedulas = DocumentoIdentidad.objects.count()
        self.subir()
        self.assertEqual(DocumentoIdentidad.objects.count(), cedulas)
        fotos = DocumentoContrato.objects.count()
        self.subir_cedula()
        self.assertEqual(DocumentoContrato.objects.count(), fotos)

    def test_la_auditoria_dice_el_orden_sin_la_imagen_ni_datos_personales(self):
        documento = self.subir()
        evento = Auditoria.objects.get(accion='fotografia_contrato_subida')
        self.assertEqual((evento.actor, evento.entidad, evento.registro_id), ('admin', 'contrato', self.contrato.pk))
        self.assertEqual(evento.valor_nuevo, {'orden': 1})
        self.assertNotIn(documento.referencia_archivo, str(evento.valor_nuevo))

    def test_un_contrato_anulado_o_inexistente_no_recibe_fotografias(self):
        anulado = self.contrato_directo(anulado_en=AHORA, motivo_anulacion='Error')
        self.assertIn('contrato', self.errores(self.subir, contrato=anulado))
        self.assertEqual(self.del_contrato(), [])
        with self.assertRaises(self.contrato.__class__.DoesNotExist):
            fotografias.subir_fotografia_del_contrato(0, contenido=jpeg(), actor='admin')

    def test_un_contrato_finalizado_si_recibe_fotografias(self):
        finalizado = self.contrato_directo(inicio='2025-01-01', fin='2025-12-31', cerrado_en=AHORA)
        self.assertEqual(self.subir(contrato=finalizado).orden, 1)

    def test_si_la_base_falla_el_archivo_recien_guardado_se_borra(self):
        with patch.object(DocumentoContrato.objects, 'create', side_effect=IntegrityError('x')):
            with self.assertRaises(IntegrityError):
                self.subir()
        self.assertEqual(self.del_contrato(), [])
        self.assertEqual(DocumentoContrato.objects.count(), 0)

    def test_el_acceso_se_registra_con_actor_y_accion_y_sin_la_imagen(self):
        documento = self.subir()
        acceso = fotografias.registrar_acceso_al_contrato(documento, actor='admin', accion='consulta', ahora=AHORA)
        self.assertEqual((acceso.actor, acceso.accion, acceso.documento, acceso.ocurrido_en), ('admin', 'consulta', documento, AHORA))
        with self.assertRaises(ValueError):
            fotografias.registrar_acceso_al_contrato(documento, actor='admin', accion='borrar')


class CedulaDesdeLaPropiedadTests(BaseDeFotografias):
    def setUp(self):
        super().setUp()
        self.ficha = self.contrato.inquilino

    def activos(self, cara='frente'):
        return list(DocumentoIdentidad.objects.filter(inquilino=self.ficha, cara=cara, eliminado_en__isnull=True))

    def test_ca_75_la_fotografia_queda_en_la_ficha_del_inquilino_del_contrato_vigente(self):
        documento = self.subir_cedula('reverso')
        self.assertEqual((documento.inquilino, documento.cara), (self.ficha, 'reverso'))
        self.assertEqual(len(self.activos('reverso')), 1)
        self.assertFalse(hasattr(documento, 'propiedad_id'))   # no queda asociada a la propiedad

    def test_ca_75_la_misma_regla_de_la_ficha_la_auditoria_dice_inquilino(self):
        self.subir_cedula()
        evento = Auditoria.objects.get(accion__startswith='fotografia_', entidad='inquilino')
        self.assertEqual(evento.registro_id, self.ficha.pk)

    def test_ca_75_sin_contrato_vigente_se_rechaza_con_el_aviso(self):
        libre = self.nueva_propiedad()
        errores = self.errores(self.subir_cedula, propiedad=libre)
        self.assertEqual(errores['propiedad'], ['No hay contrato vigente.'])

    def test_ca_75_con_solo_un_contrato_futuro_tampoco_hay_contrato_vigente(self):
        otra = self.nueva_propiedad()
        self.crear(propiedad=otra, inquilino=self.nuevo_inquilino(), fecha_inicio=d('2099-01-01'))
        antes = DocumentoIdentidad.objects.count()
        self.assertEqual(self.errores(self.subir_cedula, propiedad=otra)['propiedad'], ['No hay contrato vigente.'])
        self.assertEqual(DocumentoIdentidad.objects.count(), antes)

    def test_ca_75_si_la_cara_ya_estaba_cargada_se_reemplaza_y_queda_una_activa(self):
        anterior = self.activos('frente')[0]
        nuevo = self.subir_cedula('frente')
        anterior.refresh_from_db()
        self.assertIsNotNone(anterior.eliminado_en)
        self.assertEqual(self.activos('frente'), [nuevo])

    def test_rf_39_sin_consentimiento_vigente_no_se_guarda(self):
        servicios_de_inquilinos.revocar_consentimiento(self.ficha.pk, actor='admin', ahora=AHORA)
        self.assertIn('consentimiento', self.errores(self.subir_cedula))

    def test_un_archivo_invalido_se_rechaza_como_en_la_ficha(self):
        self.assertIn('archivo', self.errores(self.subir_cedula, contenido=b'no es imagen'))

    def test_una_propiedad_inexistente_lanza_no_existe(self):
        with self.assertRaises(Propiedad.DoesNotExist):
            fotografias.subir_cedula_desde_la_propiedad(0, cara='frente', contenido=jpeg(), actor='admin')

    def test_el_selector_ofrece_agregar_o_reemplazar_segun_la_cara(self):
        cedula = selectors.cedula_en_el_perfil(self.propiedad)
        self.assertTrue(cedula['habilitada'])
        acciones = {c['cara']: (c['accion'], c['documento_id'] is not None) for c in cedula['caras']}
        self.assertEqual(acciones, {'frente': ('Reemplazar', True), 'reverso': ('Agregar', False)})
        self.assertEqual(cedula['contrato'], self.contrato)

    def test_el_selector_desactiva_la_accion_sin_contrato_vigente(self):
        libre = selectors.cedula_en_el_perfil(self.nueva_propiedad())
        self.assertEqual((libre['habilitada'], libre['aviso'], libre['caras']), (False, 'No hay contrato vigente.', []))

    def test_el_selector_cuenta_el_contrato_por_decidir_como_vigente(self):
        por_decidir = self.nueva_propiedad()
        self.contrato_directo(propiedad=por_decidir, inicio='2025-01-01', fin='2025-12-31')
        self.assertTrue(selectors.cedula_en_el_perfil(por_decidir)['habilitada'])

    def test_el_selector_de_fotografias_cuenta_las_que_caben(self):
        self.subir(), self.subir()
        datos = selectors.fotografias_del_contrato(self.contrato)
        self.assertEqual(([x.orden for x in datos['documentos']], datos['restantes']), ([1, 2], 8))


class PorHttpTests(BaseDeFotografias, Navegador):
    def url_contrato(self, contrato=None):
        return f'/contratos/{(contrato or self.contrato).pk}/fotografias/subir/'

    def publicar(self, ruta, contenido=None, nombre='foto.jpg', cliente=None, campo='archivo', **extra):
        archivo = SimpleUploadedFile(nombre, contenido or jpeg(), content_type='image/jpeg')
        return (cliente or self.client).post(ruta, {campo: archivo, **extra})

    def test_sin_sesion_se_niega_y_no_se_guarda_nada(self):
        r = self.publicar(self.url_contrato())
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r['Location'].startswith('/entrar/'))
        self.assertEqual((DocumentoContrato.objects.count(), self.del_contrato()), (0, []))

    def test_exige_el_token_csrf(self):
        cliente = self.entrar(Client(enforce_csrf_checks=True))
        self.assertEqual(self.publicar(self.url_contrato(), cliente=cliente).status_code, 403)
        self.assertEqual(DocumentoContrato.objects.count(), 0)

    def test_con_sesion_guarda_y_responde_con_los_datos(self):
        self.entrar()
        r = self.publicar(self.url_contrato())
        self.assertEqual(r.status_code, 201)
        datos = r.json()
        self.assertEqual((datos['orden'], datos['tipo']), (1, 'image/jpeg'))
        self.assertEqual(DocumentoContrato.objects.get().pk, datos['id'])

    def test_solo_acepta_post(self):
        self.entrar()
        self.assertEqual(self.client.get(self.url_contrato()).status_code, 405)

    def test_un_solo_archivo_por_peticion_y_en_el_campo_archivo(self):
        self.entrar()
        dos = self.client.post(self.url_contrato(), {'archivo': [SimpleUploadedFile('a.jpg', jpeg()), SimpleUploadedFile('b.jpg', jpeg())]})
        self.assertEqual(dos.status_code, 400)
        otro_campo = self.publicar(self.url_contrato(), campo='otro')
        self.assertEqual(otro_campo.status_code, 400)
        self.assertEqual(DocumentoContrato.objects.count(), 0)

    def test_mas_de_5_mib_y_tipo_real_distinto_se_rechazan_con_un_mensaje(self):
        self.entrar()
        grande = self.publicar(self.url_contrato(), contenido=b'\xff\xd8\xff' + b'\x00' * (5 * 1024 * 1024 + 10))
        self.assertEqual(grande.status_code, 400)
        self.assertIn('5 MiB', grande.json()['errores']['archivo'][0])
        disfrazado = self.publicar(self.url_contrato(), contenido=b'MZ\x90\x00' + b'\x00' * 100, nombre='contrato.jpg')
        self.assertEqual(disfrazado.status_code, 400)
        self.assertEqual(DocumentoContrato.objects.count(), 0)

    def test_la_numero_11_responde_400_con_el_maximo(self):
        self.entrar()
        for _ in range(10):
            self.assertEqual(self.publicar(self.url_contrato()).status_code, 201)
        r = self.publicar(self.url_contrato())
        self.assertEqual(r.status_code, 400)
        self.assertIn('máximo', r.json()['errores']['archivo'][0])
        self.assertEqual(DocumentoContrato.objects.count(), 10)

    def test_un_contrato_inexistente_es_404(self):
        self.entrar()
        self.assertEqual(self.publicar('/contratos/0/fotografias/subir/').status_code, 404)

    def test_la_cedula_desde_la_propiedad_guarda_en_la_ficha_y_sin_contrato_vigente_dice_por_que(self):
        self.entrar()
        ok = self.publicar(f'/propiedades/{self.propiedad.pk}/cedula/reverso/')
        self.assertEqual((ok.status_code, ok.json()['cara']), (201, 'reverso'))
        libre = self.nueva_propiedad()
        no = self.publicar(f'/propiedades/{libre.pk}/cedula/frente/')
        self.assertEqual((no.status_code, no.json()['errores']['propiedad']), (400, ['No hay contrato vigente.']))
        self.assertEqual(self.publicar('/propiedades/0/cedula/frente/').status_code, 404)

    def test_la_cedula_desde_la_propiedad_exige_sesion_y_una_cara_valida(self):
        ruta = f'/propiedades/{self.propiedad.pk}/cedula/frente/'
        self.assertEqual(self.publicar(ruta).status_code, 302)
        self.entrar()
        self.assertEqual(self.publicar(f'/propiedades/{self.propiedad.pk}/cedula/lateral/').status_code, 400)

    def test_las_paginas_exigen_sesion_y_muestran_el_estado(self):
        self.subir()
        rutas = [f'/contratos/{self.contrato.pk}/fotografias/', f'/propiedades/{self.propiedad.pk}/cedula/']
        for ruta in rutas:
            self.assertEqual(self.client.get(ruta).status_code, 302)
        self.entrar()
        pagina = self.client.get(rutas[0]).content.decode()
        self.assertIn('1 de 10 fotografías', pagina)
        self.assertIn('data-lado-maximo="3508"', pagina)
        cedula = self.client.get(rutas[1]).content.decode()
        self.assertIn('Reemplazar', cedula)
        self.assertEqual(self.client.get('/contratos/0/fotografias/').status_code, 404)
        self.assertEqual(self.client.get('/propiedades/0/cedula/').status_code, 404)

    def test_la_pagina_de_cedula_sin_contrato_vigente_muestra_la_accion_desactivada(self):
        self.entrar()
        libre = self.nueva_propiedad()
        pagina = self.client.get(f'/propiedades/{libre.pk}/cedula/').content.decode()
        self.assertIn('disabled', pagina)
        self.assertIn('No hay contrato vigente.', pagina)

    def test_la_pagina_del_contrato_anulado_no_ofrece_subir(self):
        self.entrar()
        anulado = self.contrato_directo(anulado_en=AHORA, motivo_anulacion='Error')
        pagina = self.client.get(f'/contratos/{anulado.pk}/fotografias/').content.decode()
        self.assertIn('anulado', pagina)
        self.assertNotIn('type="file"', pagina)

    def test_con_10_fotografias_la_pagina_ya_no_ofrece_subir(self):
        self.entrar()
        for _ in range(10):
            self.subir()
        pagina = self.client.get(f'/contratos/{self.contrato.pk}/fotografias/').content.decode()
        self.assertIn('Se llegó al máximo', pagina)
        self.assertNotIn('type="file"', pagina)


class EntregaDeLaFotografiaTests(BaseDeFotografias, Navegador):
    def setUp(self):
        super().setUp()
        self.documento = self.subir()
        with almacenamiento.abrir(self.documento.referencia_archivo, 'contratos') as f:
            self.guardado = f.read()
        self.ver = f'/contratos/fotografias/{self.documento.pk}/ver/'
        self.descargar = f'/contratos/fotografias/{self.documento.pk}/descargar/'

    def obtener(self, ruta, cliente=None):
        r = (cliente or self.client).get(ruta)
        self.addCleanup(lambda: [cerrar() for cerrar in getattr(r, '_resource_closers', [])])
        return r

    def test_ca_77_sin_sesion_se_deniega_y_el_archivo_no_sale(self):
        for ruta in (self.ver, self.descargar):
            r = self.obtener(ruta)
            self.assertEqual(r.status_code, 302)
            self.assertTrue(r['Location'].startswith('/entrar/'))
        self.assertEqual(AccesoDocumentoContrato.objects.count(), 0)

    def test_ca_77_no_hay_url_publica_del_archivo(self):
        self.entrar()
        referencia = self.documento.referencia_archivo
        for ruta in (f'/static/contratos/{referencia}', f'/media/contratos/{referencia}', f'/contratos/{referencia}',
                     f'/contratos/fotografias/{referencia}'):
            self.assertEqual(self.client.get(ruta).status_code, 404, ruta)

    def test_ca_77_con_sesion_entrega_la_imagen_y_registra_actor_fecha_y_accion_sin_la_imagen(self):
        self.entrar()
        antes = timezone.now()
        r = self.obtener(self.ver)
        despues = timezone.now()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(b''.join(r.streaming_content), self.guardado)
        self.assertEqual(r['Content-Type'], 'image/jpeg')
        acceso = AccesoDocumentoContrato.objects.get()
        self.assertEqual((acceso.actor, acceso.accion, acceso.documento), ('admin', 'consulta', self.documento))
        self.assertTrue(antes <= acceso.ocurrido_en <= despues)
        self.assertNotIn(self.guardado[:20], str(list(AccesoDocumentoContrato.objects.values())).encode())

    def test_las_cabeceras_no_dejan_que_se_guarde_y_el_nombre_no_lleva_datos_personales(self):
        self.entrar()
        r = self.obtener(self.ver)
        self.assertIn('no-store', r['Cache-Control'])
        self.assertIn(f'contrato-{self.documento.pk}.jpg', r['Content-Disposition'])

    def test_descargar_es_otra_accion_y_va_como_adjunto(self):
        self.entrar()
        r = self.obtener(self.descargar)
        self.assertIn('attachment', r['Content-Disposition'])
        self.assertEqual(AccesoDocumentoContrato.objects.get().accion, 'descarga')

    def test_cada_consulta_deja_su_propio_registro(self):
        self.entrar()
        for _ in range(3):
            self.obtener(self.ver)
        self.assertEqual(AccesoDocumentoContrato.objects.count(), 3)

    def test_un_documento_inexistente_es_404_y_no_registra(self):
        self.entrar()
        self.assertEqual(self.obtener('/contratos/fotografias/0/ver/').status_code, 404)
        self.assertEqual(AccesoDocumentoContrato.objects.count(), 0)

    def test_si_falta_el_archivo_en_el_disco_responde_404_sin_registrar_un_acceso(self):
        self.entrar()
        almacenamiento.borrar(self.documento.referencia_archivo, 'contratos')
        with self.assertLogs('sga.documentos', 'ERROR'):
            self.assertEqual(self.obtener(self.ver).status_code, 404)
        self.assertEqual(AccesoDocumentoContrato.objects.count(), 0)

    def test_si_no_se_puede_registrar_el_acceso_no_se_entrega_la_imagen(self):
        self.entrar()
        with patch.object(fotografias, 'registrar_acceso_al_contrato', side_effect=IntegrityError('x')):
            with self.assertRaises(IntegrityError):
                self.obtener(self.ver)

    def test_solo_get(self):
        self.entrar()
        for metodo in (self.client.post, self.client.put, self.client.delete):
            self.assertEqual(metodo(self.ver).status_code, 405)


class ScriptDelContratoTests(BaseDeFotografias):
    def test_el_script_lee_el_lado_del_formulario_y_acota_el_valor(self):
        from django.contrib.staticfiles import finders
        codigo = Path(finders.find('inquilinos/reducir_fotografia.js')).read_text(encoding='utf-8')
        self.assertIn("formulario.getAttribute('data-lado-maximo')", codigo)
        self.assertIn('valor >= LADO_MINIMO && valor <= 8000 ? valor : LADO_MAXIMO', codigo)
        self.assertIn('LADO_MAXIMO = 2048', codigo)   # la cédula no cambia

    def test_solo_la_pagina_del_contrato_declara_los_3508_px(self):
        base = Path(__file__).parent / 'templates' / 'alquileres'
        self.assertIn('data-lado-maximo="{{ lado_de_partida }}"', (base / 'fotografias_contrato.html').read_text(encoding='utf-8'))
        self.assertNotIn('data-lado-maximo', (base / 'cedula_propiedad.html').read_text(encoding='utf-8'))
        from . import views
        self.assertEqual(views.LADO_DE_PARTIDA_DEL_CONTRATO, 3508)


class SubcarpetasTests(BaseDeFotografias):
    def test_el_almacenamiento_solo_admite_las_subcarpetas_conocidas(self):
        for mala in ('otra', '..', '../cedulas', ''):
            with self.assertRaises(almacenamiento.ReferenciaInvalida):
                almacenamiento.guardar(b'x', 'jpg', mala)
        self.assertFalse(almacenamiento.existe('0' * 32 + '.jpg', '..'))
        self.assertFalse(almacenamiento.borrar('0' * 32 + '.jpg', 'otra'))

    def test_un_archivo_de_contratos_no_se_abre_como_cedula_ni_al_reves(self):
        documento = self.subir()
        self.assertTrue(almacenamiento.existe(documento.referencia_archivo, 'contratos'))
        self.assertFalse(almacenamiento.existe(documento.referencia_archivo))   # la subcarpeta por omisión es cedulas
