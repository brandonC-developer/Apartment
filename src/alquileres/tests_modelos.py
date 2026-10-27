"""Modelos de la E2 (grupo A): restricciones del modelo de datos v0.7 y protección de las filas. Necesitan PostgreSQL."""
from datetime import date, datetime, timedelta, timezone as utc
from decimal import Decimal

from django.db import IntegrityError, connection, transaction
from django.test import TestCase

from inquilinos.models import TAMANO_MAXIMO
from inquilinos.tests import un_inquilino
from nucleo.models import RegistroInmutable

from .models import (
    AccesoDocumentoContrato, AjusteObligacion, CondicionContrato, Contrato, DocumentoContrato, EjecucionProceso,
    Obligacion, Propiedad)

AHORA = datetime(2026, 10, 26, 12, 0, 0, tzinfo=utc.utc)


def una_propiedad(alias='Casa 1', **extra):
    return Propiedad.objects.create(alias=alias, **extra)


def un_contrato(propiedad=None, inquilino=None, inicio=date(2026, 1, 1), fin=None, **extra):
    datos = dict(inquilino=inquilino or un_inquilino(numero_documento=f'c-{Contrato.objects.count()}'),
                 propiedad=propiedad or una_propiedad(f'P{Propiedad.objects.count()}'), destino='vivienda',
                 fecha_inicio=inicio, fecha_fin=fin, moneda='CRC')
    datos.update(extra)
    return Contrato.objects.create(**datos)


def una_condicion(contrato, **extra):
    datos = dict(contrato=contrato, monto_mensual=Decimal('300000.00'), dia_vencimiento=5, dias_gracia=7,
                 vigente_desde=contrato.fecha_inicio, tipo='inicial', registrada_en=AHORA)
    datos.update(extra)
    return CondicionContrato.objects.create(**datos)


def una_obligacion(contrato, inicio=date(2026, 1, 1), **extra):
    datos = dict(contrato=contrato, tipo='regular', periodo_inicio=inicio, periodo_fin=inicio + timedelta(days=29),
                 fecha_vencimiento=inicio + timedelta(days=4), fecha_limite=inicio + timedelta(days=11),
                 importe_inicial=Decimal('300000.00'), moneda='CRC')
    datos.update(extra)
    return Obligacion.objects.create(**datos)


class PropiedadTests(TestCase):
    def test_se_guarda_activa_y_con_descripcion_y_direccion_vacias(self):
        p = una_propiedad()
        p.refresh_from_db()
        self.assertFalse(p.inactiva)
        self.assertEqual((p.descripcion, p.direccion, str(p)), ('', '', 'Casa 1'))

    def test_el_alias_es_obligatorio(self):
        for alias in ('', '   ', '\t'):
            with self.assertRaises(IntegrityError, msg=repr(alias)), transaction.atomic():
                una_propiedad(alias)

    def test_el_alias_es_unico_sin_distinguir_mayusculas(self):
        una_propiedad('Casa 1')
        for repetido in ('Casa 1', 'casa 1', 'CASA 1'):
            with self.assertRaises(IntegrityError, msg=repetido), transaction.atomic():
                una_propiedad(repetido)
        una_propiedad('Casa 2')

    def test_no_se_borra_una_propiedad_con_contratos(self):
        c = un_contrato()
        with self.assertRaises(Exception), transaction.atomic():
            c.propiedad.delete()


class ContratoTests(TestCase):
    def test_se_guarda_con_el_rango_abierto(self):
        c = un_contrato()
        c.refresh_from_db()
        self.assertIsNone(c.fecha_fin)
        self.assertIsNone(c.anulado_en)
        self.assertEqual(c.moneda, 'CRC')

    def test_moneda_y_destino_validos(self):
        un_contrato(moneda='USD')
        for extra in (dict(moneda='EUR'), dict(destino='comercio')):
            with self.assertRaises(IntegrityError, msg=str(extra)), transaction.atomic():
                un_contrato(**extra)

    def test_la_fecha_de_fin_no_precede_al_inicio_pero_puede_ser_el_mismo_dia(self):
        un_contrato(inicio=date(2026, 1, 1), fin=date(2026, 1, 1))
        with self.assertRaises(IntegrityError), transaction.atomic():
            un_contrato(inicio=date(2026, 2, 1), fin=date(2026, 1, 31))

    def test_r21_la_anulacion_lleva_su_motivo_y_sin_anulacion_no_hay_motivo(self):
        for extra in (dict(anulado_en=AHORA), dict(anulado_en=AHORA, motivo_anulacion='  '),
                      dict(motivo_anulacion='sin anular')):
            with self.assertRaises(IntegrityError, msg=str(extra)), transaction.atomic():
                un_contrato(**extra)
        un_contrato(anulado_en=AHORA, motivo_anulacion='Error de captura')

    def test_el_inquilino_con_contrato_no_se_borra(self):
        c = un_contrato()
        with self.assertRaises(Exception), transaction.atomic():
            c.inquilino.delete()


class SolapeDeContratosTests(TestCase):
    """R2 (RN-02): dos contratos de una propiedad no comparten ningún día; ambas fechas inclusive."""

    def setUp(self):
        self.propiedad = una_propiedad()
        un_contrato(self.propiedad, inicio=date(2026, 1, 1), fin=date(2026, 12, 31))

    def crear(self, inicio, fin=None, propiedad=None, **extra):
        return un_contrato(propiedad or self.propiedad, inicio=inicio, fin=fin, **extra)

    def rechazado(self, inicio, fin=None):
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.crear(inicio, fin)

    def test_un_dia_compartido_se_rechaza(self):
        self.rechazado(date(2026, 12, 31), date(2027, 6, 30))   # comparte el último día (inclusive)
        self.rechazado(date(2025, 6, 1), date(2026, 1, 1))      # comparte el primer día
        self.rechazado(date(2026, 6, 1), date(2026, 6, 30))     # dentro
        self.rechazado(date(2025, 1, 1), date(2027, 12, 31))    # lo contiene

    def test_un_contrato_sin_fin_compartiendo_un_dia_se_rechaza(self):
        self.rechazado(date(2026, 12, 31))
        self.rechazado(date(2025, 1, 1))

    def test_el_relevo_contiguo_es_valido_el_dia_siguiente_al_fin(self):
        self.crear(date(2027, 1, 1))                             # abierto, desde el día siguiente
        self.crear(date(2025, 1, 1), date(2025, 12, 31))         # termina el día anterior al inicio

    def test_un_contrato_abierto_bloquea_todo_lo_posterior(self):
        otra = una_propiedad('Casa 2')
        self.crear(date(2026, 1, 1), propiedad=otra)
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.crear(date(2030, 1, 1), propiedad=otra)

    def test_propiedades_distintas_no_se_afectan(self):
        self.crear(date(2026, 6, 1), date(2026, 6, 30), propiedad=una_propiedad('Casa 3'))

    def test_un_contrato_anulado_no_cuenta_para_el_solape(self):
        self.crear(date(2027, 1, 1), anulado_en=AHORA, motivo_anulacion='Error')
        self.crear(date(2027, 1, 1))
        anulado = self.crear(date(2026, 3, 1), date(2026, 3, 31), propiedad=una_propiedad('Casa 4'),
                             anulado_en=AHORA, motivo_anulacion='Error')
        self.assertIsNotNone(anulado.pk)

    def test_alargar_el_fin_de_un_contrato_hasta_solapar_se_rechaza(self):
        primero = self.crear(date(2027, 1, 1), date(2027, 6, 30))
        siguiente = self.crear(date(2027, 7, 1), date(2027, 12, 31))
        primero.fecha_fin = date(2027, 7, 1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            primero.save(update_fields=['fecha_fin'])
        self.assertIsNotNone(siguiente.pk)


class ProteccionDelContratoTests(TestCase):
    def test_solo_cambian_la_fecha_de_fin_y_la_anulacion(self):
        c = un_contrato()
        c.fecha_fin = date(2026, 12, 31)
        c.save(update_fields=['fecha_fin'])
        for campo, valor in (('moneda', 'USD'), ('fecha_inicio', date(2026, 2, 1)), ('destino', 'otro')):
            setattr(c, campo, valor)
            with self.assertRaises(RegistroInmutable, msg=campo):
                c.save(update_fields=[campo])
        with self.assertRaises(RegistroInmutable):
            c.save()
        with self.assertRaises(RegistroInmutable):
            Contrato.objects.filter(pk=c.pk).update(moneda='USD')

    def test_no_se_borra(self):
        c = un_contrato()
        with self.assertRaises(RegistroInmutable):
            c.delete()
        with self.assertRaises(RegistroInmutable):
            Contrato.objects.all().delete()

    def test_la_anulacion_se_completa_una_sola_vez_aunque_se_salte_django(self):
        c = un_contrato()
        c.anulado_en, c.motivo_anulacion = AHORA, 'Error de captura'
        c.save(update_fields=['anulado_en', 'motivo_anulacion'])
        with self.assertRaises(IntegrityError), transaction.atomic(), connection.cursor() as cursor:
            cursor.execute('UPDATE alquileres_contrato SET motivo_anulacion = %s WHERE id = %s', ['Otro motivo', c.pk])
        with self.assertRaises(IntegrityError), transaction.atomic(), connection.cursor() as cursor:
            cursor.execute('UPDATE alquileres_contrato SET anulado_en = NULL, motivo_anulacion = NULL WHERE id = %s', [c.pk])
        c.refresh_from_db()
        self.assertEqual(c.motivo_anulacion, 'Error de captura')


class CierreDelContratoTests(TestCase):
    def test_un_contrato_cerrado_tiene_su_fecha_de_fin(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            un_contrato(cerrado_en=AHORA)
        un_contrato(fin=date(2026, 12, 31), cerrado_en=AHORA)

    def test_el_cierre_se_completa_una_sola_vez_aunque_se_salte_django(self):
        c = un_contrato(fin=date(2026, 12, 31))
        c.cerrado_en = AHORA
        c.save(update_fields=['cerrado_en'])
        for sql in ('UPDATE alquileres_contrato SET cerrado_en = NULL WHERE id = %s',
                    "UPDATE alquileres_contrato SET cerrado_en = now() WHERE id = %s"):
            with self.assertRaises(IntegrityError, msg=sql), transaction.atomic(), connection.cursor() as cursor:
                cursor.execute(sql, [c.pk])
        c.refresh_from_db()
        self.assertEqual(c.cerrado_en, AHORA)

    def test_el_fin_de_un_contrato_cerrado_puede_corregirse_pero_el_cierre_no_cambia(self):
        c = un_contrato(fin=date(2026, 12, 31), cerrado_en=AHORA)
        c.fecha_fin = date(2026, 11, 30)
        c.save(update_fields=['fecha_fin'])
        c.refresh_from_db()
        self.assertEqual((c.fecha_fin, c.cerrado_en), (date(2026, 11, 30), AHORA))


class CondicionContratoTests(TestCase):
    def setUp(self):
        self.contrato = un_contrato()

    def rechazada(self, **extra):
        with self.assertRaises(IntegrityError, msg=str(extra)), transaction.atomic():
            una_condicion(self.contrato, **extra)

    def test_la_inicial_se_guarda_sin_datos_de_reajuste(self):
        c = una_condicion(self.contrato)
        c.refresh_from_db()
        self.assertEqual((c.monto_mensual, c.dia_vencimiento, c.dias_gracia), (Decimal('300000.00'), 5, 7))
        self.assertIsNone(c.porcentaje)

    def test_r3_monto_dia_y_gracia(self):
        self.rechazada(monto_mensual=Decimal('0'))
        self.rechazada(monto_mensual=Decimal('-1'))
        self.rechazada(dia_vencimiento=0)
        self.rechazada(dia_vencimiento=32)
        una_condicion(self.contrato, dia_vencimiento=31, dias_gracia=0)

    def test_una_sola_condicion_inicial_por_contrato(self):
        una_condicion(self.contrato)
        self.rechazada()
        una_condicion(un_contrato(), vigente_desde=date(2026, 1, 1))

    def test_el_reajuste_lleva_notificacion_y_porcentaje(self):
        self.rechazada(tipo='reajuste')
        self.rechazada(tipo='reajuste', fecha_notificacion=date(2026, 5, 1))
        una_condicion(self.contrato, tipo='reajuste', fecha_notificacion=date(2026, 5, 1), porcentaje=Decimal('5.0000'),
                      vigente_desde=date(2026, 7, 1))

    def test_los_datos_del_reajuste_no_van_en_otros_tipos(self):
        self.rechazada(tipo='inicial', porcentaje=Decimal('5'))
        self.rechazada(tipo='correccion', motivo='Error', fecha_notificacion=date(2026, 5, 1))

    def test_el_tope_digitado_va_con_su_fuente(self):
        datos = dict(tipo='reajuste', fecha_notificacion=date(2026, 5, 1), porcentaje=Decimal('5'), vigente_desde=date(2026, 7, 1))
        self.rechazada(tope_digitado=Decimal('5.5'), **datos)
        self.rechazada(fuente_tope='INEC', **datos)
        self.rechazada(tope_digitado=Decimal('5.5'), fuente_tope='  ', **datos)
        una_condicion(self.contrato, tope_digitado=Decimal('5.5'), fuente_tope='INEC', **datos)

    def test_la_correccion_exige_motivo(self):
        self.rechazada(tipo='correccion')
        self.rechazada(tipo='correccion', motivo='   ')
        una_condicion(self.contrato, tipo='correccion', motivo='El monto era 310000')

    def test_el_tipo_es_uno_de_los_tres(self):
        self.rechazada(tipo='otro')

    def test_solo_insercion(self):
        c = una_condicion(self.contrato)
        c.monto_mensual = Decimal('1')
        with self.assertRaises(RegistroInmutable):
            c.save(update_fields=['monto_mensual'])
        with self.assertRaises(RegistroInmutable):
            c.delete()
        with self.assertRaises(RegistroInmutable):
            CondicionContrato.objects.all().update(monto_mensual=1)


class ObligacionTests(TestCase):
    def setUp(self):
        self.contrato = un_contrato()

    def rechazada(self, **extra):
        with self.assertRaises(IntegrityError, msg=str(extra)), transaction.atomic():
            una_obligacion(self.contrato, **extra)

    def test_r1_una_obligacion_regular_por_contrato_y_periodo(self):
        una_obligacion(self.contrato)
        self.rechazada()
        una_obligacion(self.contrato, inicio=date(2026, 2, 1))
        una_obligacion(un_contrato(), inicio=date(2026, 1, 1))

    def test_a_lo_sumo_una_apertura_por_contrato_y_sin_periodo(self):
        datos = dict(tipo='apertura', periodo_inicio=None, periodo_fin=None)
        una_obligacion(self.contrato, **datos)
        self.rechazada(**datos)
        self.rechazada(tipo='apertura', periodo_inicio=date(2026, 1, 1))   # la apertura no tiene período

    def test_la_regular_lleva_periodo_completo_y_ordenado(self):
        self.rechazada(periodo_inicio=None, periodo_fin=None)
        self.rechazada(periodo_inicio=date(2026, 3, 1), periodo_fin=date(2026, 2, 1))

    def test_fecha_limite_importe_moneda_y_tipo(self):
        self.rechazada(inicio=date(2026, 4, 1), fecha_vencimiento=date(2026, 4, 10), fecha_limite=date(2026, 4, 9))
        self.rechazada(inicio=date(2026, 4, 1), importe_inicial=Decimal('0'))
        self.rechazada(inicio=date(2026, 4, 1), moneda='EUR')
        self.rechazada(inicio=date(2026, 4, 1), tipo='otro')

    def test_el_calculo_guardado_se_conserva(self):
        o = una_obligacion(self.contrato, datos_calculo={'dias_cobrables': 11, 'dias_del_periodo': 31, 'regla': 'prorrateo'})
        o.refresh_from_db()
        self.assertEqual(o.datos_calculo['dias_cobrables'], 11)

    def test_la_anulacion_lleva_su_motivo(self):
        o = una_obligacion(self.contrato)
        o.anulada_en = AHORA
        with self.assertRaises(IntegrityError), transaction.atomic():
            o.save(update_fields=['anulada_en'])
        o.refresh_from_db()
        o.anulada_en, o.motivo_anulacion = AHORA, 'Contrato finalizado'
        o.save(update_fields=['anulada_en', 'motivo_anulacion'])

    def test_el_importe_inicial_nunca_se_actualiza_y_la_anulacion_es_una_sola_vez(self):
        o = una_obligacion(self.contrato)
        o.importe_inicial = Decimal('1')
        with self.assertRaises(RegistroInmutable):
            o.save(update_fields=['importe_inicial'])
        o.refresh_from_db()
        o.anulada_en, o.motivo_anulacion = AHORA, 'Contrato finalizado'
        o.save(update_fields=['anulada_en', 'motivo_anulacion'])
        with self.assertRaises(IntegrityError), transaction.atomic(), connection.cursor() as cursor:
            cursor.execute('UPDATE alquileres_obligacion SET anulada_en = NULL, motivo_anulacion = NULL WHERE id = %s', [o.pk])
        with self.assertRaises(RegistroInmutable):
            o.delete()


class AjusteObligacionTests(TestCase):
    def setUp(self):
        self.obligacion = una_obligacion(un_contrato())

    def ajuste(self, **extra):
        datos = dict(obligacion=self.obligacion, tipo='reajuste', importe_delta=Decimal('15000.00'), registrado_en=AHORA)
        datos.update(extra)
        return AjusteObligacion.objects.create(**datos)

    def test_se_guarda_con_signo(self):
        self.ajuste()
        self.ajuste(tipo='prorrateo_fin', importe_delta=Decimal('-193548.00'))
        self.assertEqual(self.obligacion.ajustes.count(), 2)

    def test_el_delta_no_puede_ser_cero(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.ajuste(importe_delta=Decimal('0'))

    def test_la_correccion_y_el_ajuste_manual_llevan_motivo(self):
        for tipo in ('correccion', 'ajuste_manual'):
            for motivo in ('', '   '):
                with self.assertRaises(IntegrityError, msg=f'{tipo} {motivo!r}'), transaction.atomic():
                    self.ajuste(tipo=tipo, motivo=motivo)
            self.ajuste(tipo=tipo, motivo='Error de monto')

    def test_el_tipo_es_uno_de_los_cuatro(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.ajuste(tipo='otro')

    def test_solo_insercion(self):
        a = self.ajuste()
        a.importe_delta = Decimal('1')
        with self.assertRaises(RegistroInmutable):
            a.save(update_fields=['importe_delta'])
        with self.assertRaises(RegistroInmutable):
            a.delete()


class DocumentoContratoTests(TestCase):
    def setUp(self):
        self.contrato = un_contrato()

    def foto(self, orden=1, n=[0], **extra):
        n[0] += 1
        datos = dict(contrato=self.contrato, orden=orden, referencia_archivo=f'ref-c-{n[0]}', tipo_real_archivo='image/jpeg',
                     tamano_bytes=1000)
        datos.update(extra)
        return DocumentoContrato.objects.create(**datos)

    def test_r22_y_r28_a_lo_sumo_diez_numeradas_sin_repetir(self):
        for orden in range(1, 11):
            self.foto(orden)
        for orden in (11, 0):
            with self.assertRaises(IntegrityError, msg=str(orden)), transaction.atomic():
                self.foto(orden)
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.foto(3)   # repetido
        self.assertEqual(self.contrato.documentos.count(), 10)

    def test_otro_contrato_tiene_su_propia_numeracion(self):
        self.foto(1)
        DocumentoContrato.objects.create(contrato=un_contrato(), orden=1, referencia_archivo='otra', tipo_real_archivo='image/png',
                                         tamano_bytes=10)

    def test_r27_peso_y_tipo_real(self):
        self.foto(1, tamano_bytes=1)
        self.foto(2, tamano_bytes=TAMANO_MAXIMO)
        for extra in (dict(tamano_bytes=0), dict(tamano_bytes=TAMANO_MAXIMO + 1), dict(tipo_real_archivo='image/gif'),
                      dict(tipo_real_archivo='application/pdf')):
            with self.assertRaises(IntegrityError, msg=str(extra)), transaction.atomic():
                self.foto(3, **extra)

    def test_la_referencia_del_archivo_no_se_repite(self):
        self.foto(1, referencia_archivo='igual')
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.foto(2, referencia_archivo='igual')

    def test_solo_insercion_porque_la_conservacion_depende_de_dp_28(self):
        f = self.foto(1)
        f.tamano_bytes = 5
        with self.assertRaises(RegistroInmutable):
            f.save(update_fields=['tamano_bytes'])
        with self.assertRaises(RegistroInmutable):
            f.delete()
        self.assertFalse(hasattr(f, 'eliminado_en'))


class AccesoDocumentoContratoTests(TestCase):
    def setUp(self):
        self.foto = DocumentoContrato.objects.create(contrato=un_contrato(), orden=1, referencia_archivo='ref', tipo_real_archivo='image/jpeg',
                                                     tamano_bytes=10)

    def test_registra_quien_cuando_y_que_accion_sin_la_imagen(self):
        a = AccesoDocumentoContrato.objects.create(documento=self.foto, actor='admin', accion='consulta', ocurrido_en=AHORA)
        a.refresh_from_db()
        self.assertEqual((a.actor, a.accion, a.documento_id), ('admin', 'consulta', self.foto.pk))
        self.assertEqual({f.name for f in a._meta.get_fields()} & {'imagen', 'contenido', 'archivo'}, set())

    def test_la_accion_es_consulta_o_descarga(self):
        AccesoDocumentoContrato.objects.create(documento=self.foto, actor='admin', accion='descarga', ocurrido_en=AHORA)
        with self.assertRaises(IntegrityError), transaction.atomic():
            AccesoDocumentoContrato.objects.create(documento=self.foto, actor='admin', accion='borrar', ocurrido_en=AHORA)

    def test_la_clave_foranea_es_obligatoria_y_solo_hay_una_r23(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            AccesoDocumentoContrato.objects.create(documento_id=999999, actor='admin', accion='consulta', ocurrido_en=AHORA)
            connection.check_constraints()
        claves = [f for f in AccesoDocumentoContrato._meta.get_fields() if f.is_relation and f.many_to_one]
        self.assertEqual([f.name for f in claves], ['documento'])

    def test_solo_insercion(self):
        a = AccesoDocumentoContrato.objects.create(documento=self.foto, actor='admin', accion='consulta', ocurrido_en=AHORA)
        a.actor = 'otro'
        with self.assertRaises(RegistroInmutable):
            a.save(update_fields=['actor'])
        with self.assertRaises(RegistroInmutable):
            a.delete()


class EjecucionProcesoTests(TestCase):
    def test_nace_en_curso_y_al_terminar_solo_se_completa_el_cierre(self):
        e = EjecucionProceso.objects.create(fecha_local=date(2026, 10, 26), iniciada_en=AHORA)
        self.assertEqual(e.resultado, 'en_curso')
        e.terminada_en, e.resultado, e.detalle = AHORA + timedelta(seconds=3), 'correcta', '4 obligaciones nuevas'
        e.save(update_fields=['terminada_en', 'resultado', 'detalle'])
        e.fecha_local = date(2026, 1, 1)
        with self.assertRaises(RegistroInmutable):
            e.save(update_fields=['fecha_local'])
        with self.assertRaises(RegistroInmutable):
            e.delete()

    def test_una_ejecucion_terminada_lleva_su_instante_y_el_resultado_es_uno_de_tres(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            EjecucionProceso.objects.create(fecha_local=date(2026, 10, 26), iniciada_en=AHORA, resultado='correcta')
        with self.assertRaises(IntegrityError), transaction.atomic():
            EjecucionProceso.objects.create(fecha_local=date(2026, 10, 26), iniciada_en=AHORA, resultado='rara')

    def test_pueden_correr_varias_veces_el_mismo_dia(self):
        for _ in range(2):
            EjecucionProceso.objects.create(fecha_local=date(2026, 10, 26), iniciada_en=AHORA)
        self.assertEqual(EjecucionProceso.objects.count(), 2)
