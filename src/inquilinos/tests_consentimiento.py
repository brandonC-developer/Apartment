"""Consentimiento, grupo C de la E1 (RF-39, OL-13; CA-67 primera y segunda parte). Necesitan PostgreSQL."""
import re
import tempfile
from datetime import timedelta
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, TestCase

from nucleo import organizacion
from nucleo.models import Auditoria

from . import ganchos, selectors, services, textos
from .models import Consentimiento, DocumentoIdentidad, Inquilino, TextoConsentimiento
from .services import ErrorDeValidacion
from .tests import AHORA, un_documento
from .tests_servicios import DATOS


class BorradorTests(SimpleTestCase):
    def texto(self):
        return textos.construir_borrador('Nombre del Responsable', 'Calle 1, San José')

    def test_trae_los_ocho_puntos_del_articulo_5_en_su_orden(self):
        texto = self.texto()
        encabezados = ['Existencia de una base de datos', 'Fines de la recolección', 'Destinatarios', 'Carácter obligatorio o facultativo',
                       'Tratamiento que se dará', 'Consecuencias de negarse', 'Derechos que le asisten',
                       'Identidad y dirección del responsable']
        posiciones = []
        for numero, encabezado in enumerate(encabezados, 1):
            marca = f'{numero}. {encabezado}'
            self.assertIn(marca, texto)
            posiciones.append(texto.index(marca))
        self.assertEqual(posiciones, sorted(posiciones))

    def test_el_punto_8_dice_quien_es_el_responsable(self):
        texto = self.texto()
        self.assertIn('Nombre del Responsable, con dirección en Calle 1, San José', texto)
        self.assertNotIn('{', texto)
        self.assertNotIn('}', texto)

    def test_dice_en_el_propio_texto_que_es_un_borrador_sin_validar_y_marca_lo_que_debe_ver_el_abogado(self):
        texto = self.texto()
        self.assertTrue(texto.startswith(textos.MARCA_DE_BORRADOR))
        self.assertGreaterEqual(len(re.findall(r'\[A VALIDAR POR EL ABOGADO', texto)), 3)
        self.assertIn('DP-31', texto)
        self.assertIn('DP-18', texto)

    def test_el_consentimiento_es_expreso_por_escrito_y_revocable_sin_efecto_retroactivo(self):
        texto = self.texto()
        for frase in ('consentimiento expreso', 'físico o electrónico', 'no tiene efecto retroactivo'):
            self.assertIn(frase, texto)

    def test_lo_obligatorio_y_lo_facultativo_coinciden_con_la_ers(self):
        punto4 = self.texto().split('4. ')[1].split('5. ')[0]
        self.assertIn('Son obligatorios su nombre completo, el tipo y el número', punto4)
        self.assertIn('frente', punto4)
        self.assertIn('Son facultativos su teléfono, su correo electrónico y la fotografía del reverso', punto4)

    def test_no_afirma_que_cumpla_la_ley(self):
        texto = self.texto().lower()
        for prohibida in ('cumple con la ley', 'conforme a la ley', 'validado por un abogado.'):
            self.assertNotIn(prohibida, texto)

    def test_sin_nombre_o_sin_direccion_no_se_genera(self):
        for nombre, direccion in (('', 'x'), ('x', ''), (None, 'x'), ('  ', 'x'), ('x', None)):
            with self.assertRaises(textos.FaltaIdentidadDelResponsable):
                textos.construir_borrador(nombre, direccion)


class VersionesTests(TestCase):
    def test_crea_la_version_1_como_borrador_y_audita(self):
        texto, creada = services.crear_version_texto('Texto uno', actor='servidor', ahora=AHORA)
        self.assertTrue(creada)
        self.assertEqual((texto.version, texto.borrador, texto.vigente_desde), (1, True, AHORA))
        r = Auditoria.objects.get(accion='texto_consentimiento_cargado')
        self.assertEqual((r.actor, r.valor_nuevo), ('servidor', {'version': 1, 'borrador': True}))

    def test_el_mismo_contenido_no_crea_otra_version_y_uno_distinto_si(self):
        uno, _ = services.crear_version_texto('Texto uno', actor='servidor')
        igual, creada = services.crear_version_texto('  Texto uno \n', actor='servidor')
        self.assertFalse(creada)
        self.assertEqual(igual, uno)
        dos, creada = services.crear_version_texto('Texto dos', actor='servidor')
        self.assertTrue(creada)
        self.assertEqual(dos.version, 2)
        self.assertEqual(TextoConsentimiento.objects.get(version=1).contenido, 'Texto uno')  # la anterior no cambia

    def test_validado_por_el_abogado_es_una_version_nueva_aunque_el_texto_sea_igual(self):
        services.crear_version_texto('Texto', actor='servidor')
        validado, creada = services.crear_version_texto('Texto', actor='servidor', borrador=False)
        self.assertTrue(creada)
        self.assertFalse(validado.borrador)
        self.assertEqual(TextoConsentimiento.objects.count(), 2)

    def test_un_texto_vacio_se_rechaza(self):
        for vacio in ('', '  \n', None):
            with self.assertRaises(ErrorDeValidacion):
                services.crear_version_texto(vacio, actor='servidor')


def correr(*args):
    salida = StringIO()
    call_command('cargar_texto_consentimiento', *args, stdout=salida)
    return salida.getvalue()


class ComandoTests(TestCase):
    def test_sin_la_identidad_del_responsable_no_carga_nada(self):
        with self.assertRaises(CommandError) as e:
            correr()
        self.assertIn('configurar_organizacion', str(e.exception))
        self.assertEqual(TextoConsentimiento.objects.count(), 0)

    def test_con_la_identidad_carga_el_borrador_y_repetirlo_no_crea_otra(self):
        organizacion.actualizar(actor='servidor', nombre_responsable='Nombre del Responsable',
                                direccion_responsable='Calle 1')
        self.assertIn('Versión 1 cargada (borrador sin validar por abogado)', correr())
        texto = TextoConsentimiento.objects.get()
        self.assertTrue(texto.borrador)
        self.assertIn('Nombre del Responsable, con dirección en Calle 1', texto.contenido)
        self.assertIn('ya tiene este contenido', correr())
        self.assertEqual(TextoConsentimiento.objects.count(), 1)

    def test_si_cambia_el_responsable_hay_una_version_nueva_y_la_vieja_no_se_toca(self):
        organizacion.actualizar(actor='servidor', nombre_responsable='Uno', direccion_responsable='A')
        correr()
        organizacion.actualizar(actor='servidor', nombre_responsable='Dos')
        correr()
        v1, v2 = TextoConsentimiento.objects.order_by('version')
        self.assertIn('Uno, con dirección en A', v1.contenido)
        self.assertIn('Dos, con dirección en A', v2.contenido)

    def test_con_archivo_y_validado_carga_el_texto_del_abogado(self):
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta, 'texto.txt')
            archivo.write_text('Texto definitivo del abogado', encoding='utf-8')
            self.assertIn('borrador sin validar', correr('--archivo', str(archivo)))
            self.assertIn('validado por abogado', correr('--archivo', str(archivo), '--validado'))
        versiones = list(TextoConsentimiento.objects.order_by('version').values_list('borrador', flat=True))
        self.assertEqual(versiones, [True, False])

    def test_validado_sin_archivo_y_un_archivo_inexistente_se_rechazan(self):
        with self.assertRaises(CommandError):
            correr('--validado')
        with self.assertRaises(CommandError):
            correr('--archivo', '/no/existe.txt')
        self.assertEqual(TextoConsentimiento.objects.count(), 0)


class RevocacionTests(TestCase):
    def setUp(self):
        self.texto = TextoConsentimiento.objects.create(version=1, contenido='Texto', vigente_desde=AHORA)
        self.inquilino = services.registrar_inquilino(
            actor='admin', datos=dict(DATOS, telefono='8888-8888'), texto=self.texto, medio='fisico', ahora=AHORA)
        self.documento = un_documento(self.inquilino)
        self.addCleanup(lambda: [ganchos.quitar_al_revocar(f) for f in list(ganchos._al_revocar)])

    def revocar(self, **extra):
        return services.revocar_consentimiento(
            self.inquilino.pk, actor='admin', ip_origen='203.0.113.5', ahora=AHORA + timedelta(days=3), **extra)

    def test_registra_la_revocacion_sin_efecto_retroactivo(self):
        antes = Inquilino.objects.values().get(pk=self.inquilino.pk)
        c = self.revocar()
        c.refresh_from_db()
        self.assertEqual(c.revocado_en, AHORA + timedelta(days=3))
        self.assertEqual(c.otorgado_en, AHORA)  # lo otorgado antes no cambia
        self.assertEqual(Inquilino.objects.values().get(pk=self.inquilino.pk), antes)  # ningún dato cambia ni se borra
        self.assertEqual(DocumentoIdentidad.objects.filter(pk=self.documento.pk, eliminado_en__isnull=True).count(), 1)
        self.assertEqual(Consentimiento.objects.count(), 1)  # el consentimiento se conserva, revocado

    def test_deja_su_registro_de_auditoria_sin_datos_personales(self):
        self.revocar()
        r = Auditoria.objects.get(accion='consentimiento_revocado')
        self.assertEqual((r.actor, r.ip_origen, r.registro_id, r.valor_nuevo), ('admin', '203.0.113.5', self.inquilino.pk, {'revocado': True}))
        self.assertNotIn('8888-8888', str(list(Auditoria.objects.values())))

    def test_la_ficha_avisa_y_no_deja_crear_contratos(self):
        ficha = selectors.obtener_ficha(self.inquilino.pk)
        self.assertFalse(ficha['consentimiento_revocado'])
        self.assertTrue(ficha['puede_crear_contratos'])
        self.assertTrue(selectors.tiene_consentimiento_vigente(self.inquilino))
        self.revocar()
        ficha = selectors.obtener_ficha(self.inquilino.pk)
        self.assertTrue(ficha['consentimiento_revocado'])
        self.assertFalse(ficha['puede_crear_contratos'])
        self.assertIsNone(ficha['consentimiento_vigente'])
        self.assertFalse(selectors.tiene_consentimiento_vigente(self.inquilino))
        self.assertIsNone(selectors.consentimiento_vigente(self.inquilino))

    def test_no_hay_nada_que_revocar_dos_veces(self):
        self.revocar()
        with self.assertRaises(ErrorDeValidacion):
            self.revocar()
        self.assertEqual(Auditoria.objects.filter(accion='consentimiento_revocado').count(), 1)

    def test_la_revocacion_no_puede_ser_anterior_al_consentimiento(self):
        with self.assertRaises(ErrorDeValidacion):
            services.revocar_consentimiento(self.inquilino.pk, actor='admin', ahora=AHORA - timedelta(days=1))
        self.assertTrue(selectors.tiene_consentimiento_vigente(self.inquilino))

    def test_los_ganchos_se_ejecutan_en_la_misma_transaccion_y_si_uno_falla_se_deshace(self):
        recibidos = []

        def anotar(consentimiento):
            recibidos.append(consentimiento.pk)
        ganchos.registrar_al_revocar(anotar)
        ganchos.registrar_al_revocar(anotar)  # registrarlo dos veces no lo duplica
        c = self.revocar()
        self.assertEqual(recibidos, [c.pk])

        def falla(consentimiento):
            raise RuntimeError('la solicitud de supresión no se pudo abrir')
        otro = services.registrar_inquilino(
            actor='admin', datos=dict(DATOS, numero_documento='9-9'), texto=self.texto, medio='fisico', ahora=AHORA)
        ganchos.registrar_al_revocar(falla)
        with self.assertRaises(RuntimeError):
            services.revocar_consentimiento(otro.pk, actor='admin', ahora=AHORA + timedelta(days=1))
        self.assertTrue(selectors.tiene_consentimiento_vigente(otro))  # la revocación se deshizo
        self.assertEqual(Auditoria.objects.filter(accion='consentimiento_revocado', registro_id=otro.pk).count(), 0)

    def test_un_inquilino_inexistente_falla(self):
        with self.assertRaises(Inquilino.DoesNotExist):
            services.revocar_consentimiento(999999, actor='admin')


class TextoExactoDeCadaVersionTests(TestCase):
    """CA-67, primera parte: se puede ver el texto exacto de la versión sobre la que se consintió."""

    def test_la_ficha_muestra_el_texto_de_la_version_consentida_aunque_haya_una_nueva(self):
        v1 = TextoConsentimiento.objects.create(version=1, contenido='Texto de la versión 1', vigente_desde=AHORA)
        inquilino = services.registrar_inquilino(actor='admin', datos=dict(DATOS), texto=v1, medio='electronico', ahora=AHORA)
        v2 = TextoConsentimiento.objects.create(version=2, contenido='Texto de la versión 2', borrador=False, vigente_desde=AHORA)
        ficha = selectors.obtener_ficha(inquilino.pk)
        self.assertEqual(ficha['consentimiento'].texto.contenido, 'Texto de la versión 1')
        self.assertEqual(ficha['consentimiento'].texto.version, 1)
        self.assertTrue(ficha['consentimiento'].texto.borrador)
        self.assertEqual(selectors.texto_vigente(), v2)  # los nuevos consentimientos usan la última
        otro = services.registrar_inquilino(
            actor='admin', datos=dict(DATOS, numero_documento='5-5'), texto=selectors.texto_vigente(), medio='fisico', ahora=AHORA)
        self.assertEqual(selectors.obtener_ficha(otro.pk)['consentimiento'].texto.contenido, 'Texto de la versión 2')
        self.assertEqual(selectors.obtener_ficha(inquilino.pk)['consentimiento'].texto.contenido, 'Texto de la versión 1')
