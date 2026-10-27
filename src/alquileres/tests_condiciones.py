"""Reajuste, corrección y ajuste manual (RF-09, RF-10, RN-12, RN-14; CA-12, CA-22, CA-39, CA-40, CA-51, CA-55).
Necesitan PostgreSQL."""
from datetime import date
from decimal import Decimal

from django.db import IntegrityError, connection, transaction

from nucleo.models import Auditoria

from . import condiciones, movimientos, selectors, services
from .models import AjusteObligacion, CondicionContrato, Obligacion
from .tests_servicios import AHORA, Base, ConMovimientos, d, obligacion_del_periodo


class BaseDeCondiciones(Base):
    """Un contrato de vivienda en colones que empieza el 10 de enero de 2026 (períodos del 10 al 9) con cinco obligaciones."""

    def setUp(self):
        super().setUp()
        self.contrato = self.crear(fecha_inicio=d('2026-01-10'), dia_vencimiento=15).contrato
        self.obligaciones = [obligacion_del_periodo(self.contrato, n) for n in range(5)]   # ene a mayo

    def reajustar(self, notificacion='2026-03-20', monto='315000.00', tope='3.2', fuente='Certificación del INEC', **extra):
        return condiciones.reajustar_contrato(
            self.contrato.pk, actor='admin', ip_origen='203.0.113.5', fecha_notificacion=d(notificacion), nuevo_monto=monto,
            tope_digitado=tope, fuente_tope=fuente, ahora=AHORA, **extra)

    def corregir(self, efectiva='2026-03-10', motivo='El monto era 310000', **extra):
        return condiciones.corregir_contrato(
            self.contrato.pk, actor='admin', ip_origen='203.0.113.5', fecha_efectiva=d(efectiva), motivo=motivo, ahora=AHORA, **extra)

    def vigentes(self):
        return [selectors.importe_vigente(Obligacion.objects.get(pk=o.pk)) for o in self.obligaciones]

    def errores_de(self, funcion, **extra):
        with self.assertRaises(condiciones.ErrorDeValidacion) as contexto:
            funcion(**extra)
        return contexto.exception.errores


class ReajusteTests(BaseDeCondiciones):
    def test_ca_12_la_fecha_efectiva_es_el_inicio_del_periodo_siguiente_a_la_notificacion(self):
        """Período 10 mar–9 abr, notificado el 20 de marzo: rige desde el 10 de abril."""
        r = self.reajustar(notificacion='2026-03-20')
        self.assertEqual(r.condicion.vigente_desde, d('2026-04-10'))
        self.assertEqual(r.condicion.tipo, 'reajuste')
        self.assertEqual(r.condicion.fecha_notificacion, d('2026-03-20'))
        # ene, feb y mar (períodos 0 a 2) mantienen su monto; abr y may (3 y 4) aplican el nuevo
        self.assertEqual(self.vigentes(), [Decimal('300000.00')] * 3 + [Decimal('315000.00')] * 2)
        self.assertEqual((r.ajustadas, r.sin_cambio), (2, 0))

    def test_la_notificacion_el_mismo_dia_que_inicia_un_periodo_cuenta_para_el_siguiente(self):
        self.assertEqual(self.reajustar(notificacion='2026-03-10').condicion.vigente_desde, d('2026-04-10'))

    def test_la_notificacion_el_ultimo_dia_del_periodo_tambien(self):
        self.assertEqual(self.reajustar(notificacion='2026-04-09').condicion.vigente_desde, d('2026-04-10'))

    def test_el_porcentaje_se_calcula_con_cuatro_decimales(self):
        r = self.reajustar(monto='315000.00')
        self.assertEqual(r.condicion.porcentaje, Decimal('5.0000'))
        otro = self.reajustar(notificacion='2026-04-12', monto='318333.33', tope='9')
        self.assertEqual(otro.condicion.porcentaje, Decimal('1.0582'))   # (318333.33 − 315000) / 315000 × 100

    def test_ca_51_el_tope_y_la_fuente_se_conservan_y_si_el_porcentaje_los_supera_solo_advierte(self):
        r = self.reajustar(monto='315000.00', tope='3.2', fuente='Certificación del INEC')   # 5 % > 3,2 %
        self.assertEqual((r.condicion.tope_digitado, r.condicion.fuente_tope), (Decimal('3.2000'), 'Certificación del INEC'))
        self.assertEqual(len(r.advertencias), 1)
        self.assertIn('supera el tope', r.advertencias[0])
        self.assertIn('5,00 %', r.advertencias[0])
        self.assertEqual(self.vigentes()[-1], Decimal('315000.00'))   # se guardó de todos modos

    def test_con_el_porcentaje_dentro_del_tope_no_advierte(self):
        for monto, tope in (('309000.00', '3.2'), ('309600.00', '3.2')):    # 3 % y exactamente 3,2 %
            contrato = self.crear(propiedad=self.nueva_propiedad(), fecha_inicio=d('2026-01-10')).contrato
            r = condiciones.reajustar_contrato(contrato.pk, actor='admin', fecha_notificacion=d('2026-03-20'), nuevo_monto=monto,
                                               tope_digitado=tope, fuente_tope='INEC', ahora=AHORA)
            self.assertEqual(r.advertencias, (), monto)

    def test_ca_51_en_vivienda_se_exigen_el_tope_y_la_fuente(self):
        self.assertIn('tope_digitado', self.errores_de(self.reajustar, tope=None, fuente=None))
        self.assertIn('fuente_tope', self.errores_de(self.reajustar, tope='3.2', fuente='  '))
        self.assertIn('tope_digitado', self.errores_de(self.reajustar, tope=None, fuente='INEC'))
        for tope in ('-1', '101', 'abc', '3.12345'):
            self.assertIn('tope_digitado', self.errores_de(self.reajustar, tope=tope), tope)
        self.assertEqual(CondicionContrato.objects.filter(tipo='reajuste').count(), 0)

    def test_ca_39_una_vivienda_con_precio_en_dolares_se_rechaza(self):
        usd = self.crear(propiedad=self.nueva_propiedad(), fecha_inicio=d('2026-01-10'), moneda='USD').contrato
        errores = self.errores_de(condiciones.reajustar_contrato, contrato_id=usd.pk, actor='admin',
                                  fecha_notificacion=d('2026-03-20'), nuevo_monto='550.00', tope_digitado='3.2',
                                  fuente_tope='INEC', ahora=AHORA)
        self.assertIn('moneda extranjera', errores['moneda'][0])

    def test_otro_destino_no_exige_tope_y_admite_dolares(self):
        otro = self.crear(propiedad=self.nueva_propiedad(), fecha_inicio=d('2026-01-10'), destino='otro', moneda='USD').contrato
        r = condiciones.reajustar_contrato(otro.pk, actor='admin', fecha_notificacion=d('2026-03-20'), nuevo_monto='550.00', ahora=AHORA)
        self.assertEqual((r.condicion.tope_digitado, r.condicion.fuente_tope, r.advertencias), (None, None, ()))
        self.assertEqual(r.condicion.monto_mensual, Decimal('550.00'))

    def test_otro_destino_con_tope_sin_fuente_se_rechaza(self):
        otro = self.crear(propiedad=self.nueva_propiedad(), fecha_inicio=d('2026-01-10'), destino='otro').contrato
        errores = self.errores_de(condiciones.reajustar_contrato, contrato_id=otro.pk, actor='admin',
                                  fecha_notificacion=d('2026-03-20'), nuevo_monto='330000', tope_digitado='4', ahora=AHORA)
        self.assertIn('fuente_tope', errores)

    def test_fecha_y_monto_invalidos(self):
        casos = [(dict(notificacion='2026-01-09'), 'fecha_notificacion', 'anterior al inicio'),
                 (dict(notificacion='2026-10-27'), 'fecha_notificacion', 'futura'),
                 (dict(monto='300000.00'), 'nuevo_monto', 'igual al actual'),
                 (dict(monto='0'), 'nuevo_monto', 'mayor que cero'),
                 (dict(monto='abc'), 'nuevo_monto', 'número válido'),
                 (dict(monto='99999999999.99'), 'nuevo_monto', 'desproporcionado')]
        for extra, campo, texto in casos:
            self.assertIn(texto, self.errores_de(self.reajustar, **extra)[campo][0], campo)
        self.assertEqual(CondicionContrato.objects.filter(tipo='reajuste').count(), 0)

    def test_la_fecha_efectiva_no_puede_quedar_despues_del_fin_del_contrato(self):
        contrato = self.crear(propiedad=self.nueva_propiedad(), fecha_inicio=d('2026-01-10'), fecha_fin=d('2026-04-09')).contrato
        errores = self.errores_de(condiciones.reajustar_contrato, contrato_id=contrato.pk, actor='admin',
                                  fecha_notificacion=d('2026-03-20'), nuevo_monto='315000', tope_digitado='5', fuente_tope='INEC', ahora=AHORA)
        self.assertIn('después del fin', errores['fecha_notificacion'][0])

    def test_no_hay_dos_reajustes_con_la_misma_fecha_efectiva(self):
        self.reajustar()
        self.assertIn('use una corrección', self.errores_de(self.reajustar, notificacion='2026-03-25', monto='320000')['fecha_notificacion'][0])

    def test_un_segundo_reajuste_parte_del_monto_ya_reajustado(self):
        self.reajustar(monto='315000.00')                                            # desde abril
        r = self.reajustar(notificacion='2026-04-15', monto='330750.00', tope='5')   # +5 % sobre 315000, desde mayo
        self.assertEqual(r.condicion.porcentaje, Decimal('5.0000'))
        self.assertEqual(self.vigentes(), [Decimal('300000.00')] * 3 + [Decimal('315000.00'), Decimal('330750.00')])

    def test_las_obligaciones_pagadas_no_se_modifican(self):
        movimientos.usar(ConMovimientos('300000', obligaciones_con_pagos=[self.obligaciones[3].pk]))   # abril, pagada completa
        r = self.reajustar()
        self.assertEqual((r.ajustadas, r.saltadas_pagadas), (1, 1))
        self.assertEqual(self.vigentes()[3], Decimal('300000.00'))
        self.assertEqual(self.vigentes()[4], Decimal('315000.00'))

    def test_una_obligacion_con_abono_parcial_si_se_ajusta(self):
        movimientos.usar(ConMovimientos('100000', obligaciones_con_pagos=[self.obligaciones[3].pk]))
        self.reajustar()
        self.assertEqual(self.vigentes()[3], Decimal('315000.00'))

    def test_se_audita_con_el_valor_anterior_el_nuevo_la_fecha_efectiva_y_el_motivo(self):
        self.reajustar(motivo='Reajuste anual')
        e = Auditoria.objects.get(accion='contrato_reajustado')
        self.assertEqual(e.ip_origen, '203.0.113.5')
        self.assertEqual((e.valor_anterior['monto_mensual'], e.valor_nuevo['monto_mensual']), ('300000.00', '315000.00'))
        self.assertEqual((e.valor_nuevo['vigente_desde'], e.valor_nuevo['porcentaje'], e.valor_nuevo['motivo']),
                         ('2026-04-10', '5.0000', 'Reajuste anual'))
        self.assertEqual(Auditoria.objects.filter(accion='ajuste_registrado').count(), 2)

    def test_las_obligaciones_nuevas_toman_el_monto_reajustado_por_la_condicion_aplicable(self):
        self.reajustar()
        condicion = selectors.condicion_vigente_en(self.contrato, d('2026-06-10'))
        self.assertEqual(condicion.monto_mensual, Decimal('315000.00'))
        self.assertEqual(selectors.condicion_vigente_en(self.contrato, d('2026-04-09')).monto_mensual, Decimal('300000.00'))

    def test_el_ultimo_periodo_ya_prorrateado_se_reajusta_prorrateado(self):
        contrato = self.crear(propiedad=self.nueva_propiedad(), fecha_inicio=d('2026-01-10'), moneda='CRC').contrato
        obligaciones = [obligacion_del_periodo(contrato, n) for n in range(5)]
        services.finalizar_contrato(contrato.pk, actor='admin', fecha_fin=d('2026-05-02'), ahora=AHORA)   # cae en el período 10 abr–9 may
        antes = [selectors.importe_vigente(Obligacion.objects.get(pk=o.pk)) for o in obligaciones]
        condiciones.reajustar_contrato(contrato.pk, actor='admin', fecha_notificacion=d('2026-03-20'), nuevo_monto='315000.00',
                                       tope_digitado='5', fuente_tope='INEC', ahora=AHORA)
        despues = [selectors.importe_vigente(Obligacion.objects.get(pk=o.pk)) for o in obligaciones]
        self.assertEqual(despues[:3], antes[:3])
        self.assertEqual(despues[3], Decimal('241500.00'))          # 315000 × 23 / 30: el último período sigue prorrateado
        self.assertIsNotNone(Obligacion.objects.get(pk=obligaciones[4].pk).anulada_en)   # la del período siguiente se anuló al finalizar
        self.assertEqual(despues[4], antes[4])                      # y una anulada no se reajusta

    def test_un_contrato_anulado_no_se_reajusta(self):
        services.anular_contrato(self.contrato.pk, actor='admin', motivo='Error', ahora=AHORA)
        with self.assertRaises(condiciones.ErrorDeValidacion):
            self.reajustar()


class CorreccionTests(BaseDeCondiciones):
    def test_ca_22_las_pagadas_no_cambian_las_no_pagadas_se_actualizan_y_el_historial_reconstruye(self):
        movimientos.usar(ConMovimientos('300000', obligaciones_con_pagos=[self.obligaciones[2].pk]))   # marzo pagada
        r = self.corregir(efectiva='2026-03-10', monto_mensual='310000.00')     # marzo, abril y mayo
        self.assertEqual(self.vigentes(), [Decimal('300000.00')] * 3 + [Decimal('310000.00')] * 2)   # marzo (pagada) intacta
        self.assertEqual((r.ajustadas, r.saltadas_pagadas), (2, 1))
        historial = selectors.historial_de_importes(Obligacion.objects.get(pk=self.obligaciones[3].pk))
        self.assertEqual([(p['tipo'], p['anterior'], p['nuevo']) for p in historial],
                         [('inicial', None, Decimal('300000.00')), ('correccion', Decimal('300000.00'), Decimal('310000.00'))])
        self.assertEqual(historial[1]['motivo'], 'El monto era 310000')

    def test_las_vencidas_no_pagadas_tambien_se_corrigen(self):
        self.assertTrue(all(o.fecha_limite < d('2026-10-26') for o in self.obligaciones))    # todas vencidas hoy
        r = self.corregir(efectiva='2026-01-10', monto_mensual='310000.00')
        self.assertEqual(r.ajustadas, 5)
        self.assertEqual(self.vigentes(), [Decimal('310000.00')] * 5)

    def test_ca_55_el_importe_inicial_se_conserva_y_el_vigente_se_deriva(self):
        self.corregir(efectiva='2026-05-10', monto_mensual='200000.00')
        mayo = Obligacion.objects.get(pk=self.obligaciones[4].pk)
        self.assertEqual((mayo.importe_inicial, selectors.importe_vigente(mayo)), (Decimal('300000.00'), Decimal('200000.00')))
        ajuste = AjusteObligacion.objects.get(obligacion=mayo)
        self.assertEqual((ajuste.importe_delta, ajuste.motivo, ajuste.tipo), (Decimal('-100000.00'), 'El monto era 310000', 'correccion'))

    def test_ca_40_un_cambio_por_debajo_de_lo_abonado_se_bloquea_y_muestra_el_exceso(self):
        movimientos.usar(ConMovimientos('100000', obligaciones_con_pagos=[self.obligaciones[4].pk]))
        errores = self.errores_de(self.corregir, efectiva='2026-05-10', monto_mensual='80000.00')
        self.assertIn('₡20.000', errores['importe'][0])
        self.assertIn('₡100.000', errores['importe'][0])
        self.assertEqual(AjusteObligacion.objects.count(), 0)
        self.assertEqual(CondicionContrato.objects.filter(tipo='correccion').count(), 0)   # no cambió nada

    def test_si_una_obligacion_baja_de_lo_abonado_no_se_ajusta_ninguna(self):
        movimientos.usar(ConMovimientos('100000', obligaciones_con_pagos=[self.obligaciones[4].pk]))
        with self.assertRaises(condiciones.ErrorDeValidacion):
            self.corregir(efectiva='2026-03-10', monto_mensual='80000.00')
        self.assertEqual(self.vigentes(), [Decimal('300000.00')] * 5)

    def test_la_correccion_exige_motivo_y_algo_que_corregir(self):
        for motivo in ('', '   ', None):
            self.assertIn('motivo', self.errores_de(self.corregir, motivo=motivo, monto_mensual='310000'))
        self.assertIn('correccion', self.errores_de(self.corregir))
        self.assertIn('no cambia nada', self.errores_de(self.corregir, monto_mensual='300000.00')['correccion'][0])

    def test_la_fecha_efectiva_va_entre_el_inicio_y_el_fin(self):
        self.assertIn('anterior al inicio', self.errores_de(self.corregir, efectiva='2026-01-09', monto_mensual='310000')['fecha_efectiva'][0])
        cerrado = self.crear(propiedad=self.nueva_propiedad(), fecha_inicio=d('2026-01-10'), fecha_fin=d('2026-06-09')).contrato
        errores = self.errores_de(condiciones.corregir_contrato, contrato_id=cerrado.pk, actor='admin', fecha_efectiva=d('2026-07-10'),
                                  motivo='x', monto_mensual='310000', ahora=AHORA)
        self.assertIn('después del fin', errores['fecha_efectiva'][0])

    def test_los_valores_invalidos_se_rechazan(self):
        for campo, valor in (('monto_mensual', '0'), ('dia_vencimiento', 32), ('dia_vencimiento', 'x'), ('dias_gracia', -1), ('dias_gracia', 400)):
            self.assertIn(campo, self.errores_de(self.corregir, **{campo: valor}), msg=(campo, valor))

    def test_corregir_el_dia_de_vencimiento_actualiza_las_fechas_de_las_no_pagadas_con_auditoria(self):
        """Decisión 3 de la E2: se actualizan fecha_vencimiento y fecha_limite; el valor anterior queda en la auditoría."""
        movimientos.usar(ConMovimientos('300000', obligaciones_con_pagos=[self.obligaciones[2].pk]))   # marzo pagada
        antes = [(o.fecha_vencimiento, o.fecha_limite) for o in self.obligaciones]
        r = self.corregir(efectiva='2026-02-10', dia_vencimiento=20, dias_gracia=3)
        self.assertEqual(r.fechas_corregidas, 3)       # febrero, abril y mayo; marzo está pagada
        febrero = Obligacion.objects.get(pk=self.obligaciones[1].pk)
        self.assertEqual((febrero.fecha_vencimiento, febrero.fecha_limite), (d('2026-02-20'), d('2026-02-23')))
        marzo = Obligacion.objects.get(pk=self.obligaciones[2].pk)
        self.assertEqual((marzo.fecha_vencimiento, marzo.fecha_limite), antes[2])    # la pagada no cambia
        enero = Obligacion.objects.get(pk=self.obligaciones[0].pk)
        self.assertEqual((enero.fecha_vencimiento, enero.fecha_limite), antes[0])    # anterior a la fecha efectiva
        evento = Auditoria.objects.filter(accion='obligacion_fechas_corregidas', registro_id=febrero.pk).get()
        self.assertEqual((evento.valor_anterior['fecha_vencimiento'], evento.valor_nuevo['fecha_vencimiento']),
                         (antes[1][0].isoformat(), '2026-02-20'))
        self.assertEqual(febrero.importe_inicial, Decimal('300000.00'))      # el importe no se tocó
        self.assertEqual(self.vigentes()[1], Decimal('300000.00'))

    def test_las_obligaciones_vencidas_dejan_de_estarlo_si_la_fecha_corregida_es_posterior(self):
        r = self.corregir(efectiva='2026-05-10', dia_vencimiento=9, dias_gracia=200)
        mayo = Obligacion.objects.get(pk=self.obligaciones[4].pk)
        self.assertEqual(r.fechas_corregidas, 1)
        self.assertGreater(mayo.fecha_limite, d('2026-10-26'))

    def test_el_vencimiento_corregido_siempre_cae_dentro_del_periodo(self):
        self.corregir(efectiva='2026-01-10', dia_vencimiento=31)
        for o in self.obligaciones:
            o.refresh_from_db()
            self.assertTrue(o.periodo_inicio <= o.fecha_vencimiento <= o.periodo_fin, o.periodo_inicio)

    def test_una_correccion_solo_de_fechas_no_ajusta_importes(self):
        r = self.corregir(efectiva='2026-03-10', dia_vencimiento=25)
        self.assertEqual((r.ajustadas, AjusteObligacion.objects.count()), (0, 0))

    def test_correccion_y_reajuste_se_combinan_por_el_periodo(self):
        self.reajustar(monto='315000.00')                                # desde abril
        self.corregir(efectiva='2026-03-10', monto_mensual='310000.00')  # corrige marzo en adelante, pero abril y mayo ya tienen el reajuste
        self.assertEqual(self.vigentes(), [Decimal('300000.00'), Decimal('300000.00'), Decimal('310000.00'),
                                           Decimal('315000.00'), Decimal('315000.00')])

    def test_corregir_la_condicion_inicial_con_su_misma_fecha_gana_la_registrada_despues(self):
        self.corregir(efectiva='2026-01-10', monto_mensual='290000.00')
        self.assertEqual(selectors.condicion_vigente_en(self.contrato, d('2026-01-10')).tipo, 'correccion')
        self.assertEqual(self.contrato.condiciones.count(), 2)          # la inicial se conserva

    def test_el_ultimo_periodo_corregido_se_prorratea_con_el_monto_nuevo(self):
        contrato = self.crear(propiedad=self.nueva_propiedad(), fecha_inicio=d('2027-01-01')).contrato
        obligaciones = [obligacion_del_periodo(contrato, n) for n in range(2)]
        services.finalizar_contrato(contrato.pk, actor='admin', fecha_fin=d('2027-02-10'), ahora=AHORA)   # febrero: 10 de 28
        condiciones.corregir_contrato(contrato.pk, actor='admin', fecha_efectiva=d('2027-01-01'), motivo='Era 280000',
                                      monto_mensual='280000.00', ahora=AHORA)
        self.assertEqual(selectors.importe_vigente(Obligacion.objects.get(pk=obligaciones[0].pk)), Decimal('280000.00'))
        self.assertEqual(selectors.importe_vigente(Obligacion.objects.get(pk=obligaciones[1].pk)), Decimal('100000.00'))   # 280000 × 10 / 28

    def test_una_obligacion_con_ajuste_manual_conserva_su_importe_y_se_avisa(self):
        contrato = self.crear(propiedad=self.nueva_propiedad(), fecha_inicio=d('2027-01-01')).contrato
        obligaciones = [obligacion_del_periodo(contrato, n) for n in range(2)]
        services.finalizar_contrato(contrato.pk, actor='admin', fecha_fin=d('2027-02-10'), ahora=AHORA)
        condiciones.ajustar_manualmente(obligaciones[1].pk, actor='admin', nuevo_importe='90000.00', motivo='Acuerdo con el inquilino', ahora=AHORA)
        r = condiciones.corregir_contrato(contrato.pk, actor='admin', fecha_efectiva=d('2027-01-01'), motivo='Era 280000',
                                          monto_mensual='280000.00', ahora=AHORA)
        self.assertEqual(r.saltadas_manuales, 1)
        self.assertIn('ajuste manual', r.advertencias[0])
        self.assertEqual(selectors.importe_vigente(Obligacion.objects.get(pk=obligaciones[1].pk)), Decimal('90000.00'))

    def test_se_audita_la_correccion(self):
        self.corregir(efectiva='2026-03-10', monto_mensual='310000.00', dia_vencimiento=20)
        e = Auditoria.objects.get(accion='contrato_corregido')
        self.assertEqual((e.valor_anterior['monto_mensual'], e.valor_nuevo['monto_mensual']), ('300000.00', '310000.00'))
        self.assertEqual((e.valor_anterior['dia_vencimiento'], e.valor_nuevo['dia_vencimiento']), (15, 20))
        self.assertEqual((e.valor_nuevo['vigente_desde'], e.valor_nuevo['motivo']), ('2026-03-10', 'El monto era 310000'))


class AjusteManualTests(Base):
    def setUp(self):
        super().setUp()
        self.contrato = self.crear(fecha_inicio=d('2027-01-01')).contrato
        self.obligaciones = [obligacion_del_periodo(self.contrato, n) for n in range(3)]
        services.finalizar_contrato(self.contrato.pk, actor='admin', fecha_fin=d('2027-02-10'), ahora=AHORA)
        self.ultima = self.obligaciones[1]   # febrero, prorrateada a 107143

    def ajustar(self, obligacion=None, importe='100000.00', motivo='Acuerdo con el inquilino'):
        return condiciones.ajustar_manualmente((obligacion or self.ultima).pk, actor='admin', ip_origen='203.0.113.5',
                                               nuevo_importe=importe, motivo=motivo, ahora=AHORA)

    def test_ajusta_el_ultimo_periodo_con_un_ajuste_inmutable_y_audita(self):
        ajuste = self.ajustar()
        self.assertEqual((ajuste.tipo, ajuste.importe_delta, ajuste.motivo), ('ajuste_manual', Decimal('-7143.00'), 'Acuerdo con el inquilino'))
        self.assertEqual(selectors.importe_vigente(Obligacion.objects.get(pk=self.ultima.pk)), Decimal('100000.00'))
        self.assertEqual(Obligacion.objects.get(pk=self.ultima.pk).importe_inicial, Decimal('300000.00'))
        e = Auditoria.objects.filter(accion='ajuste_registrado', registro_id=self.ultima.pk).latest('id')
        self.assertEqual((e.valor_anterior['importe_vigente'], e.valor_nuevo['importe_vigente']), ('107143.00', '100000.00'))
        self.assertEqual(e.valor_nuevo['motivo'], 'Acuerdo con el inquilino')

    def test_exige_motivo_y_un_importe_distinto_y_valido(self):
        for motivo in ('', '  ', None):
            self.assertIn('motivo', self.errores_de(self.ajustar, motivo=motivo))
        self.assertIn('ya tiene ese importe', self.errores_de(self.ajustar, importe='107143.00')['nuevo_importe'][0])
        self.assertIn('mayor que cero', self.errores_de(self.ajustar, importe='0')['nuevo_importe'][0])

    def errores_de(self, funcion, **extra):
        with self.assertRaises(condiciones.ErrorDeValidacion) as contexto:
            funcion(**extra)
        return contexto.exception.errores

    def test_solo_el_ultimo_periodo_de_un_contrato_finalizado(self):
        self.assertIn('último período', self.errores_de(self.ajustar, obligacion=self.obligaciones[0])['obligacion'][0])
        abierto = self.crear(propiedad=self.nueva_propiedad(), fecha_inicio=d('2027-01-01')).contrato
        o = obligacion_del_periodo(abierto, 0)
        self.assertIn('último período', self.errores_de(self.ajustar, obligacion=o)['obligacion'][0])

    def test_no_se_ajusta_una_obligacion_anulada(self):
        self.assertIn('no esté anulado', self.errores_de(self.ajustar, obligacion=self.obligaciones[2])['obligacion'][0].replace('anulada', 'anulado'))

    def test_no_baja_de_lo_abonado(self):
        movimientos.usar(ConMovimientos('105000', obligaciones_con_pagos=[self.ultima.pk]))
        self.assertIn('exceso', self.errores_de(self.ajustar, importe='100000.00')['importe'][0])
        self.assertEqual(selectors.importe_vigente(Obligacion.objects.get(pk=self.ultima.pk)), Decimal('107143.00'))


class CasosLimiteTests(BaseDeCondiciones):
    def test_la_fuente_del_tope_no_pasa_de_200_caracteres(self):
        self.assertIn('200', self.errores_de(self.reajustar, fuente='x' * 201)['fuente_tope'][0])
        self.reajustar(fuente='x' * 200)

    def test_la_fecha_efectiva_es_obligatoria_y_sin_condicion_vigente_se_rechaza(self):
        self.assertIn('fecha_efectiva', self.errores_de(condiciones.corregir_contrato, contrato_id=self.contrato.pk, actor='admin',
                                                        fecha_efectiva=None, motivo='x', monto_mensual='310000', ahora=AHORA))
        from unittest.mock import patch
        with patch('alquileres.condiciones.selectors.condicion_vigente_en', return_value=None):
            self.assertIn('No hay condiciones', self.errores_de(self.corregir, monto_mensual='310000')['fecha_efectiva'][0])


class FechasDePagoYProteccionTests(BaseDeCondiciones):
    def test_la_base_deja_corregir_solo_las_fechas_y_no_el_importe_ni_el_periodo(self):
        o = Obligacion.objects.get(pk=self.obligaciones[0].pk)
        o.fecha_vencimiento = d('2026-01-20')
        o.fecha_limite = d('2026-01-27')
        o.save(update_fields=['fecha_vencimiento', 'fecha_limite'])
        o.importe_inicial = Decimal('1')
        with self.assertRaises(Exception):
            o.save(update_fields=['importe_inicial'])

    def test_la_fecha_limite_no_puede_quedar_antes_del_vencimiento(self):
        o = Obligacion.objects.get(pk=self.obligaciones[0].pk)
        o.fecha_limite = o.fecha_vencimiento - (d('2026-01-02') - d('2026-01-01'))
        with self.assertRaises(IntegrityError), transaction.atomic():
            o.save(update_fields=['fecha_limite'])

    def test_el_importe_inicial_sigue_protegido_con_sql_directo_para_el_rol_de_la_aplicacion(self):
        # la prueba de privilegios (nucleo.tests_privilegios) ejecuta esto como el rol de la aplicación; aquí solo se confirma
        # que ninguna operación de este módulo escribe `importe_inicial`
        import inspect
        self.assertNotIn('importe_inicial=', inspect.getsource(condiciones).replace('obligacion.importe_inicial', ''))
        self.assertNotIn("'importe_inicial'", inspect.getsource(condiciones))
