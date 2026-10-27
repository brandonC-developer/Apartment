"""Generación de obligaciones, saldo de apertura, estado derivado y proceso diario (RF-11, RF-12, RF-14, RF-42, RF-43,
RNF-04, RNF-16; CA-03, CA-14, CA-30, CA-36, CA-49, CA-50). Necesitan PostgreSQL."""
from datetime import date
from decimal import Decimal
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, connection

from nucleo.models import Auditoria

from . import calculo, condiciones, movimientos, obligaciones, proceso, selectors, services
from .models import AjusteObligacion, CondicionContrato, EjecucionProceso, Obligacion
from .tests_servicios import AHORA, Base, ConMovimientos, d


class BaseDeObligaciones(Base):
    def contrato(self, inicio='2026-01-10', **extra):
        return self.crear(fecha_inicio=d(inicio), **extra).contrato

    def generar(self, contrato, hoy, **extra):
        extra.setdefault('actor', 'admin')
        return obligaciones.generar_obligaciones(contrato.pk, hoy=d(hoy), ahora=AHORA, **extra)

    def periodos(self, contrato):
        return [(o.periodo_inicio.isoformat(), o.periodo_fin.isoformat(), o.fecha_vencimiento.isoformat())
                for o in Obligacion.objects.filter(contrato=contrato, tipo='regular').order_by('periodo_inicio')]


class GeneracionTests(BaseDeObligaciones):
    def test_ca_03_periodos_y_vencimientos_con_mes_corto_y_dia_31(self):
        contrato = self.contrato('2026-01-10', monto_mensual=Decimal('180000.00'), dia_vencimiento=31)
        self.generar(contrato, '2026-03-01')
        self.assertEqual(self.periodos(contrato), [
            ('2026-01-10', '2026-02-09', '2026-01-31'),
            ('2026-02-10', '2026-03-09', '2026-02-28'),
            ('2026-03-10', '2026-04-09', '2026-03-31')])

    def test_ca_03_en_anio_bisiesto_febrero_vence_el_29(self):
        contrato = self.contrato('2028-01-10', dia_vencimiento=31)
        self.generar(contrato, '2028-03-01')
        self.assertEqual(self.periodos(contrato)[1], ('2028-02-10', '2028-03-09', '2028-02-29'))

    def test_ca_03_ejecutar_de_nuevo_no_crea_duplicados(self):
        contrato = self.contrato('2026-01-10')
        primera = self.generar(contrato, '2026-03-01')
        segunda = self.generar(contrato, '2026-03-01')
        self.assertEqual((len(primera), len(segunda)), (3, 0))
        self.assertEqual(Obligacion.objects.filter(contrato=contrato).count(), 3)

    def test_ejecutar_otro_dia_solo_agrega_los_periodos_que_faltan(self):
        contrato = self.contrato('2026-01-10')
        self.generar(contrato, '2026-03-01')
        nuevas = self.generar(contrato, '2026-03-11')   # 11 mar + 30 días = 10 abr
        self.assertEqual([o.periodo_inicio for o in nuevas], [d('2026-04-10')])

    def test_ca_30_genera_a_los_30_dias_y_no_antes(self):
        contrato = self.contrato('2026-04-10')
        self.assertEqual(self.generar(contrato, '2026-03-10'), [])
        self.assertEqual(len(self.generar(contrato, '2026-03-11')), 1)

    def test_ca_50_el_vencimiento_cae_dentro_del_periodo(self):
        contrato = self.contrato('2026-01-31', dia_vencimiento=30)
        self.generar(contrato, '2026-01-31')
        primera = Obligacion.objects.get(contrato=contrato, periodo_inicio=d('2026-01-31'))
        self.assertEqual((primera.periodo_fin, primera.fecha_vencimiento), (d('2026-02-27'), d('2026-02-27')))

    def test_la_fecha_limite_suma_los_dias_de_gracia_y_se_copian_monto_y_moneda(self):
        contrato = self.contrato('2026-01-10', dia_vencimiento=5, dias_gracia=7, monto_mensual=Decimal('250000.00'))
        self.generar(contrato, '2026-01-10')
        o = Obligacion.objects.filter(contrato=contrato).order_by('periodo_inicio').first()
        self.assertEqual((o.fecha_vencimiento, o.fecha_limite), (d('2026-02-05'), d('2026-02-12')))
        self.assertEqual((o.importe_inicial, o.moneda, o.condicion.tipo), (Decimal('250000.00'), 'CRC', 'inicial'))

    def test_cada_periodo_usa_la_condicion_que_lo_rige(self):
        contrato = self.contrato('2026-01-10')
        CondicionContrato.objects.create(
            contrato=contrato, monto_mensual=Decimal('330000.00'), dia_vencimiento=10, dias_gracia=3,
            vigente_desde=d('2026-03-10'), tipo='correccion', motivo='prueba', registrada_en=AHORA)
        self.generar(contrato, '2026-03-01')
        montos = [o.importe_inicial for o in Obligacion.objects.filter(contrato=contrato).order_by('periodo_inicio')]
        self.assertEqual(montos, [Decimal('300000.00')] * 2 + [Decimal('330000.00')])

    def test_un_contrato_en_dolares_se_genera_en_dolares(self):
        contrato = self.contrato('2026-01-10', moneda='USD', destino='otro', monto_mensual=Decimal('450.50'))
        self.generar(contrato, '2026-01-10')
        o = Obligacion.objects.get(contrato=contrato)
        self.assertEqual((o.moneda, o.importe_inicial), ('USD', Decimal('450.50')))

    def test_un_contrato_con_fin_no_genera_periodos_que_inician_despues_del_fin(self):
        contrato = self.contrato('2026-01-10', fecha_fin=d('2026-03-25'))
        self.generar(contrato, '2026-03-01')
        self.assertEqual([p[0] for p in self.periodos(contrato)], ['2026-01-10', '2026-02-10', '2026-03-10'])
        self.generar(contrato, '2026-03-24')   # el fin aún no pasó: 24 mar + 30 días alcanza el 23 abr
        self.assertEqual(len(self.periodos(contrato)), 3)

    def test_ca_14_el_ultimo_periodo_nace_prorrateado(self):
        contrato = self.contrato('2026-01-10', fecha_fin=d('2026-03-25'), monto_mensual=Decimal('180000.00'))
        self.generar(contrato, '2026-03-01')
        ultima = Obligacion.objects.get(contrato=contrato, periodo_inicio=d('2026-03-10'))
        self.assertEqual(ultima.importe_inicial, Decimal('180000.00'))
        self.assertEqual(selectors.importe_vigente(ultima), Decimal('92903.00'))
        ajuste = AjusteObligacion.objects.get(obligacion=ultima)
        self.assertEqual(ajuste.tipo, 'prorrateo_fin')
        self.assertIn('16 de 31 días', ajuste.motivo)
        # los demás períodos no se prorratean
        completas = Obligacion.objects.filter(contrato=contrato).exclude(pk=ultima.pk)
        self.assertEqual({selectors.importe_vigente(o) for o in completas}, {Decimal('180000.00')})

    def test_un_fin_en_el_ultimo_dia_del_periodo_no_prorratea(self):
        contrato = self.contrato('2026-01-10', fecha_fin=d('2026-03-09'))
        self.generar(contrato, '2026-03-01')
        self.assertFalse(AjusteObligacion.objects.exists())

    def test_por_decidir_sigue_generando_con_el_importe_completo(self):
        contrato = self.contrato('2026-01-10', fecha_fin=d('2026-03-25'), monto_mensual=Decimal('180000.00'))
        self.generar(contrato, '2026-03-01')
        self.assertEqual(selectors.estado_del_contrato(contrato, d('2026-04-20')), selectors.POR_DECIDIR)
        nuevas = self.generar(contrato, '2026-04-20')   # hasta el 20 de mayo
        self.assertEqual([o.periodo_inicio for o in nuevas], [d('2026-04-10'), d('2026-05-10')])
        self.assertEqual({selectors.importe_vigente(o) for o in nuevas}, {Decimal('180000.00')})

    def test_un_contrato_finalizado_anulado_o_con_fin_pasado_cerrado_no_genera(self):
        finalizado = self.contrato_directo(inicio='2026-01-10', fin='2026-02-20', cerrado_en=AHORA)
        anulado = self.contrato_directo(inicio='2026-01-10', anulado_en=AHORA, motivo_anulacion='error')
        for contrato in (finalizado, anulado):
            CondicionContrato.objects.create(
                contrato=contrato, monto_mensual=Decimal('100000.00'), dia_vencimiento=5, dias_gracia=7,
                vigente_desde=d('2026-01-10'), tipo='inicial', registrada_en=AHORA)
            self.assertEqual(self.generar(contrato, '2026-10-26'), [])
        self.assertFalse(Obligacion.objects.exists())

    def test_un_periodo_anulado_no_se_vuelve_a_generar(self):
        contrato = self.contrato('2026-01-10')
        self.generar(contrato, '2026-03-01')
        anulada = Obligacion.objects.get(contrato=contrato, periodo_inicio=d('2026-03-10'))
        services._anular_obligacion(anulada, 'prueba', 'admin', None, AHORA)
        self.assertEqual(self.generar(contrato, '2026-03-01'), [])
        self.assertEqual(Obligacion.objects.filter(contrato=contrato).count(), 3)

    def test_rf12_si_otra_ejecucion_gano_la_carrera_no_hay_error_ni_duplicado(self):
        contrato = self.contrato('2026-01-10')
        self.generar(contrato, '2026-01-10')
        existente = calculo.periodo(contrato.fecha_inicio, 0)
        with patch.object(obligaciones, '_periodos_por_generar', return_value=[existente]):
            self.assertEqual(self.generar(contrato, '2026-01-10'), [])
        self.assertEqual(Obligacion.objects.filter(contrato=contrato).count(), 1)

    def test_rf12_la_base_rechaza_la_segunda_obligacion_del_periodo(self):
        contrato = self.contrato('2026-01-10')
        self.generar(contrato, '2026-01-10')
        o = Obligacion.objects.get(contrato=contrato)
        with self.assertRaises(IntegrityError), connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO alquileres_obligacion (contrato_id, tipo, periodo_inicio, periodo_fin, fecha_vencimiento, "
                "fecha_limite, importe_inicial, moneda, creado_en) SELECT contrato_id, tipo, periodo_inicio, periodo_fin, "
                "fecha_vencimiento, fecha_limite, importe_inicial, moneda, creado_en FROM alquileres_obligacion WHERE id = %s",
                [o.pk])

    def test_la_generacion_se_audita_con_el_actor_que_la_pide(self):
        contrato = self.contrato('2026-01-10')
        self.generar(contrato, '2026-01-10', actor='admin', ip_origen='203.0.113.5')
        evento = Auditoria.objects.get(accion='obligacion_generada')
        self.assertEqual((evento.actor, evento.tipo_actor, evento.ejecucion_id, str(evento.ip_origen)),
                         ('admin', 'administrador', None, '203.0.113.5'))

    def test_el_actor_sistema_exige_una_ejecucion_y_una_llamada_sin_actor_se_rechaza(self):
        contrato = self.contrato('2026-01-10')
        for actor in (None, '', 'sistema'):
            with self.assertRaises(ValueError):
                obligaciones.generar_obligaciones(contrato.pk, actor=actor, hoy=d('2026-01-10'), ahora=AHORA)

    def test_un_dia_ancla_31_vuelve_al_31_en_los_meses_que_lo_tienen(self):
        contrato = self.contrato('2026-01-31', dia_vencimiento=31)
        self.generar(contrato, '2026-05-01')   # 1 may + 30 días = 31 may
        self.assertEqual([p[0] for p in self.periodos(contrato)],
                         ['2026-01-31', '2026-02-28', '2026-03-31', '2026-04-30', '2026-05-31'])


class RenovacionYFinalizacionTests(BaseDeObligaciones):
    def test_renovar_retira_el_prorrateo_del_ultimo_periodo_si_el_contrato_continua(self):
        contrato = self.contrato('2026-01-10', fecha_fin=d('2026-03-25'), monto_mensual=Decimal('180000.00'))
        self.generar(contrato, '2026-03-01')
        services.renovar_contrato(contrato.pk, actor='admin', nueva_fecha_fin=d('2026-12-31'), motivo='Se renueva', ahora=AHORA)
        ultima = Obligacion.objects.get(contrato=contrato, periodo_inicio=d('2026-03-10'))
        self.assertEqual(selectors.importe_vigente(ultima), Decimal('180000.00'))
        self.assertEqual(list(AjusteObligacion.objects.filter(obligacion=ultima).values_list('importe_delta', flat=True)),
                         [Decimal('-87097.00'), Decimal('87097.00')])
        self.assertEqual(len(self.generar(contrato, '2026-04-20')), 2)

    def test_renovar_a_un_fin_dentro_del_mismo_periodo_vuelve_a_prorratear_sobre_el_importe_completo(self):
        contrato = self.contrato('2026-01-10', fecha_fin=d('2026-03-20'), monto_mensual=Decimal('180000.00'))
        self.generar(contrato, '2026-03-01')
        services.renovar_contrato(contrato.pk, actor='admin', nueva_fecha_fin=d('2026-03-25'), motivo='Se alarga', ahora=AHORA)
        ultima = Obligacion.objects.get(contrato=contrato, periodo_inicio=d('2026-03-10'))
        self.assertEqual(selectors.importe_vigente(ultima), Decimal('92903.00'))

    def test_renovar_sin_prorrateo_previo_no_toca_ninguna_obligacion(self):
        contrato = self.contrato('2026-01-10', fecha_fin=d('2026-03-09'))
        self.generar(contrato, '2026-03-01')
        services.renovar_contrato(contrato.pk, actor='admin', nueva_fecha_fin=d('2026-12-31'), motivo='Se renueva', ahora=AHORA)
        self.assertFalse(AjusteObligacion.objects.exists())

    def test_finalizar_antes_del_fin_pactado_prorratea_sobre_el_importe_completo_y_no_sobre_el_prorrateado(self):
        contrato = self.contrato('2026-01-10', fecha_fin=d('2026-03-25'), monto_mensual=Decimal('180000.00'))
        self.generar(contrato, '2026-03-01')
        services.finalizar_contrato(contrato.pk, actor='admin', fecha_fin=d('2026-03-20'), ahora=AHORA, hoy=d('2026-03-01'))
        ultima = Obligacion.objects.get(contrato=contrato, periodo_inicio=d('2026-03-10'))
        per = calculo.periodo(contrato.fecha_inicio, 2)
        esperado = calculo.prorratear_ultimo_periodo(Decimal('180000.00'), 'CRC', per, d('2026-03-20')).importe_final
        self.assertEqual(selectors.importe_vigente(ultima), esperado)
        self.assertEqual(esperado, Decimal('63871'))


class SaldoDeAperturaTests(BaseDeObligaciones):
    def abrir(self, contrato, importe='360000.00', fecha='2026-10-26', **extra):
        return obligaciones.registrar_saldo_de_apertura(
            contrato.pk, actor='admin', ip_origen='203.0.113.5', importe=Decimal(importe), fecha_apertura=d(fecha),
            ahora=AHORA, hoy=d('2026-10-26'), **extra)

    def errores(self, contrato, **extra):
        with self.assertRaises(services.ErrorDeValidacion) as contexto:
            self.abrir(contrato, **extra)
        return contexto.exception.errores

    def test_ca_49_genera_la_obligacion_de_apertura_sin_periodo(self):
        contrato = self.contrato('2024-10-26', dias_gracia=7)
        o = self.abrir(contrato)
        o.refresh_from_db()
        self.assertEqual((o.tipo, o.importe_inicial, o.periodo_inicio, o.periodo_fin, o.condicion_id),
                         ('apertura', Decimal('360000.00'), None, None, None))
        self.assertEqual(o.datos_calculo, {'regla': 'saldo_de_apertura', 'fecha_apertura': '2026-10-26'})

    def test_ca_49_el_vencimiento_por_omision_es_la_apertura_mas_los_dias_de_gracia_y_el_limite_es_el_mismo(self):
        contrato = self.contrato('2024-10-26', dias_gracia=7)
        o = self.abrir(contrato)
        self.assertEqual((o.fecha_vencimiento, o.fecha_limite), (d('2026-11-02'), d('2026-11-02')))

    def test_ca_49_el_administrador_digita_el_vencimiento(self):
        contrato = self.contrato('2024-10-26')
        o = self.abrir(contrato, fecha_vencimiento=d('2026-12-15'))
        self.assertEqual((o.fecha_vencimiento, o.fecha_limite), (d('2026-12-15'), d('2026-12-15')))

    def test_ca_49_las_obligaciones_regulares_empiezan_despues_de_la_apertura(self):
        """El período que inicia el mismo día de la apertura (26 oct) queda dentro del saldo y no se genera."""
        contrato = self.contrato('2024-10-26')
        self.abrir(contrato)
        self.assertEqual(self.generar(contrato, '2026-10-26'), [])
        nuevas = self.generar(contrato, '2026-10-27')   # 27 oct + 30 días = 26 nov
        self.assertEqual([o.periodo_inicio for o in nuevas], [d('2026-11-26')])
        self.assertEqual(Obligacion.objects.filter(contrato=contrato, tipo='regular').count(), 1)

    def test_ca_49_no_hay_alerta_retroactiva_la_apertura_vence_desde_su_fecha(self):
        contrato = self.contrato('2024-10-26', dias_gracia=7)
        o = self.abrir(contrato)
        self.assertEqual(selectors.estado_de_la_obligacion(o, d('2026-11-02')), selectors.PENDIENTE)
        self.assertEqual(selectors.estado_de_la_obligacion(o, d('2026-11-03')), selectors.VENCIDA)

    def test_se_audita_con_importe_y_fechas(self):
        contrato = self.contrato('2024-10-26')
        o = self.abrir(contrato)
        evento = Auditoria.objects.get(accion='saldo_apertura_registrado', registro_id=o.pk)
        self.assertEqual((evento.actor, evento.tipo_actor), ('admin', 'administrador'))
        self.assertEqual(sorted(evento.campos_modificados),
                         ['contrato', 'fecha_apertura', 'fecha_vencimiento', 'importe_inicial'])

    def test_un_solo_saldo_de_apertura_por_contrato(self):
        contrato = self.contrato('2024-10-26')
        self.abrir(contrato)
        self.assertIn('contrato', self.errores(contrato))
        self.assertEqual(Obligacion.objects.filter(tipo='apertura').count(), 1)

    def test_se_rechazan_el_importe_invalido_y_las_fechas_imposibles(self):
        contrato = self.contrato('2024-10-26')
        self.assertIn('importe', self.errores(contrato, importe='0'))
        self.assertIn('importe', self.errores(contrato, importe='-5'))
        self.assertIn('fecha_apertura', self.errores(contrato, fecha='2024-10-25'))   # antes del inicio
        self.assertIn('fecha_apertura', self.errores(contrato, fecha='2026-10-27'))   # futura
        self.assertIn('fecha_vencimiento', self.errores(contrato, fecha_vencimiento=d('2026-10-25')))
        self.assertFalse(Obligacion.objects.exists())

    def test_la_fecha_de_apertura_puede_ser_el_dia_de_inicio_y_ese_primer_periodo_queda_en_el_saldo(self):
        contrato = self.contrato('2026-10-26')
        self.abrir(contrato, fecha='2026-10-26')
        self.assertEqual(self.generar(contrato, '2026-10-26'), [])

    def test_se_rechaza_si_ya_hay_obligaciones_de_periodos_incluidos_en_el_saldo(self):
        contrato = self.contrato('2026-01-10')
        self.generar(contrato, '2026-03-01')
        self.assertIn('fecha_apertura', self.errores(contrato, fecha='2026-03-01'))
        self.assertEqual(Obligacion.objects.filter(tipo='apertura').count(), 0)

    def test_se_rechaza_en_un_contrato_anulado(self):
        contrato = self.contrato('2024-10-26')
        services.anular_contrato(contrato.pk, actor='admin', motivo='Error', ahora=AHORA)
        self.assertIn('contrato', self.errores(contrato))


class EstadoDeLaObligacionTests(BaseDeObligaciones):
    def setUp(self):
        super().setUp()
        self.contrato_ = self.contrato('2026-01-10', dia_vencimiento=5, dias_gracia=7)
        self.generar(self.contrato_, '2026-01-10')
        # período 10 ene–9 feb: vence el 5 de febrero, límite el 12 de febrero
        self.o = Obligacion.objects.get(contrato=self.contrato_, periodo_inicio=d('2026-01-10'))

    def estado(self, hoy):
        return selectors.estado_de_la_obligacion(self.o, d(hoy))

    def test_ca_36_el_ultimo_dia_de_gracia_es_pendiente_y_el_siguiente_vencida(self):
        self.assertEqual((self.o.fecha_vencimiento, self.o.fecha_limite), (d('2026-02-05'), d('2026-02-12')))
        self.assertEqual(self.estado('2026-02-12'), selectors.PENDIENTE)
        self.assertEqual(self.estado('2026-02-13'), selectors.VENCIDA)

    def test_antes_del_vencimiento_y_en_la_fecha_de_vencimiento_es_pendiente(self):
        self.assertEqual(self.estado('2026-01-10'), selectors.PENDIENTE)
        self.assertEqual(self.estado('2026-02-05'), selectors.PENDIENTE)

    def test_pagada_si_el_saldo_es_cero_aunque_haya_pasado_el_limite(self):
        movimientos.usar(ConMovimientos(abonado='300000.00', obligaciones_con_pagos=[self.o.pk]))
        self.assertEqual(selectors.saldo_de_la_obligacion(self.o), Decimal('0.00'))
        self.assertEqual(self.estado('2026-06-01'), selectors.PAGADA)

    def test_un_abono_parcial_no_la_paga(self):
        movimientos.usar(ConMovimientos(abonado='100000.00', obligaciones_con_pagos=[self.o.pk]))
        self.assertEqual(selectors.saldo_de_la_obligacion(self.o), Decimal('200000.00'))
        self.assertEqual(self.estado('2026-02-13'), selectors.VENCIDA)

    def test_anulada_prevalece(self):
        services._anular_obligacion(self.o, 'prueba', 'admin', None, AHORA)
        self.o.refresh_from_db()
        self.assertEqual(self.estado('2026-06-01'), selectors.ANULADA)

    def test_un_pago_no_cambia_el_dia_de_vencimiento_de_los_siguientes_periodos(self):
        movimientos.usar(ConMovimientos(abonado='300000.00', obligaciones_con_pagos=[self.o.pk]))
        self.generar(self.contrato_, '2026-03-01')
        dias = [o.fecha_vencimiento.day for o in Obligacion.objects.filter(contrato=self.contrato_, tipo='regular')]
        self.assertEqual(dias, [5, 5, 5])

    def test_el_importe_vigente_incluye_los_ajustes(self):
        condiciones.corregir_contrato(
            self.contrato_.pk, actor='admin', fecha_efectiva=d('2026-01-10'), motivo='Era 310000',
            monto_mensual=Decimal('310000.00'), ahora=AHORA)
        self.assertEqual(selectors.saldo_de_la_obligacion(self.o), Decimal('310000.00'))

    def test_usa_la_fecha_local_cuando_no_se_da_hoy(self):
        with patch.object(selectors, 'hoy_local', return_value=d('2026-02-13')):
            self.assertEqual(selectors.estado_de_la_obligacion(self.o), selectors.VENCIDA)


class ProcesoDiarioTests(BaseDeObligaciones):
    def setUp(self):
        super().setUp()
        self.contrato_a = self.contrato('2026-01-10')
        self.contrato_b = self.contrato('2026-02-01', propiedad=self.nueva_propiedad(), inquilino=self.nuevo_inquilino())

    def correr(self, hoy='2026-03-01'):
        return proceso.ejecutar(hoy=d(hoy), ahora=AHORA)

    def test_genera_para_todos_los_contratos_y_registra_la_ejecucion(self):
        ejecucion = self.correr()
        ejecucion.refresh_from_db()
        self.assertEqual((ejecucion.resultado, ejecucion.fecha_local), ('correcta', d('2026-03-01')))
        self.assertIsNotNone(ejecucion.terminada_en)
        self.assertEqual(ejecucion.detalle, 'Contratos revisados: 2. Obligaciones generadas: 5.')   # A: 10 ene, 10 feb, 10 mar; B: 1 feb, 1 mar
        self.assertEqual(Obligacion.objects.count(), 5)

    def test_criterio_de_salida_dos_ejecuciones_no_producen_duplicados(self):
        self.correr()
        antes = list(Obligacion.objects.order_by('pk').values_list('pk', 'contrato_id', 'periodo_inicio'))
        segunda = self.correr()
        despues = list(Obligacion.objects.order_by('pk').values_list('pk', 'contrato_id', 'periodo_inicio'))
        self.assertEqual(antes, despues)
        self.assertEqual(segunda.detalle, 'Contratos revisados: 2. Obligaciones generadas: 0.')
        self.assertEqual(EjecucionProceso.objects.count(), 2)
        self.assertEqual(Auditoria.objects.filter(accion='obligacion_generada').count(), 5)

    def test_el_proceso_audita_como_sistema_con_su_ejecucion(self):
        ejecucion = self.correr()
        eventos = Auditoria.objects.filter(accion='obligacion_generada')
        self.assertEqual({(e.actor, e.tipo_actor, e.ejecucion_id) for e in eventos}, {('sistema', 'proceso', ejecucion.pk)})
        fin = Auditoria.objects.get(accion='proceso_diario_ejecutado')
        self.assertEqual((fin.actor, fin.tipo_actor, fin.registro_id), ('sistema', 'proceso', ejecucion.pk))

    def test_el_prorrateo_al_generar_tambien_se_audita_como_proceso(self):
        self.contrato('2026-01-10', fecha_fin=d('2026-02-20'), propiedad=self.nueva_propiedad(), inquilino=self.nuevo_inquilino())
        ejecucion = self.correr('2026-02-01')
        evento = Auditoria.objects.get(accion='ajuste_prorrateo_registrado')
        self.assertEqual((evento.actor, evento.tipo_actor, evento.ejecucion_id), ('sistema', 'proceso', ejecucion.pk))

    def test_ignora_los_contratos_que_no_estan_futuros_vigentes_ni_por_decidir(self):
        services.anular_contrato(self.contrato_b.pk, actor='admin', motivo='Error', ahora=AHORA)
        ejecucion = self.correr()
        self.assertEqual(ejecucion.detalle, 'Contratos revisados: 1. Obligaciones generadas: 3.')

    def test_un_contrato_que_falla_no_detiene_a_los_demas_y_la_ejecucion_queda_fallida(self):
        original = obligaciones.generar_obligaciones

        def con_un_fallo(contrato_id, **extra):
            if contrato_id == self.contrato_a.pk:
                raise RuntimeError('fallo de prueba con datos personales')
            return original(contrato_id, **extra)

        with patch.object(obligaciones, 'generar_obligaciones', side_effect=con_un_fallo), self.assertLogs('alquileres.proceso', 'ERROR'):
            ejecucion = self.correr()
        ejecucion.refresh_from_db()
        self.assertEqual(ejecucion.resultado, 'fallida')
        self.assertIn(f'contrato {self.contrato_a.pk}: RuntimeError', ejecucion.detalle)
        self.assertNotIn('datos personales', ejecucion.detalle)
        self.assertEqual(Obligacion.objects.filter(contrato=self.contrato_b).count(), 2)
        self.assertEqual(Obligacion.objects.filter(contrato=self.contrato_a).count(), 0)

    def test_un_fallo_general_queda_registrado_y_no_deja_la_ejecucion_en_curso(self):
        with patch.object(selectors, 'contratos_en_estado', side_effect=RuntimeError('x')), self.assertLogs('alquileres.proceso', 'ERROR'):
            ejecucion = self.correr()
        ejecucion.refresh_from_db()
        self.assertEqual((ejecucion.resultado, ejecucion.detalle), ('fallida', 'Falló la ejecución: RuntimeError.'))
        self.assertIsNotNone(ejecucion.terminada_en)

    def test_el_dia_siguiente_genera_solo_lo_nuevo(self):
        self.correr('2026-03-01')
        ejecucion = self.correr('2026-03-11')
        self.assertEqual(ejecucion.detalle, 'Contratos revisados: 2. Obligaciones generadas: 2.')   # A: 10 abr; B: 1 abr

    def test_el_comando_corre_e_informa(self):
        salida = StringIO()
        with patch.object(selectors, 'hoy_local', return_value=d('2026-03-01')):
            call_command('ejecutar_proceso_diario', stdout=salida)
        self.assertIn('correcta', salida.getvalue())
        self.assertEqual(EjecucionProceso.objects.get().resultado, 'correcta')

    def test_el_comando_termina_con_error_si_la_ejecucion_fallo(self):
        with patch.object(selectors, 'contratos_en_estado', side_effect=RuntimeError('x')), self.assertLogs('alquileres.proceso', 'ERROR'):
            with self.assertRaises(CommandError):
                call_command('ejecutar_proceso_diario', stdout=StringIO())

    def test_el_comando_dos_veces_es_idempotente(self):
        with patch.object(selectors, 'hoy_local', return_value=d('2026-03-01')):
            call_command('ejecutar_proceso_diario', stdout=StringIO())
            cantidad = Obligacion.objects.count()
            call_command('ejecutar_proceso_diario', stdout=StringIO())
        self.assertEqual(Obligacion.objects.count(), cantidad)
