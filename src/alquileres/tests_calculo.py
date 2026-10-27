"""Cálculo de períodos, vencimientos, fechas límite y prorrateo (RN-03, RN-05, RN-06, RN-12, RN-13). No usan la base."""
import calendar
from collections import namedtuple
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.test import SimpleTestCase

from . import calculo
from .calculo import (
    condicion_aplicable, fecha_limite, periodo, periodo_que_contiene, periodos, prorratear_ultimo_periodo, redondear,
    vencimiento)


def d(texto):
    return date.fromisoformat(texto)


def rango(per):
    return per.inicio.isoformat(), per.fin.isoformat()


class PeriodoTests(SimpleTestCase):
    def test_ejemplo_de_rn_03_inicio_el_10_de_enero(self):
        self.assertEqual(rango(periodo(d('2026-01-10'), 0)), ('2026-01-10', '2026-02-09'))
        self.assertEqual(rango(periodo(d('2026-01-10'), 1)), ('2026-02-10', '2026-03-09'))
        self.assertEqual(periodo_que_contiene(d('2026-01-10'), d('2026-02-10')).numero, 1)   # el 10 de febrero es del segundo

    def test_inicio_el_31_vuelve_al_31_en_los_meses_que_lo_tienen(self):
        """El ancla sale de `fecha_inicio`, no del período anterior."""
        esperado = [('2027-01-31', '2027-02-27'), ('2027-02-28', '2027-03-30'), ('2027-03-31', '2027-04-29'),
                    ('2027-04-30', '2027-05-30'), ('2027-05-31', '2027-06-29')]
        self.assertEqual([rango(periodo(d('2027-01-31'), n)) for n in range(5)], esperado)

    def test_ano_bisiesto_con_inicio_el_31(self):
        self.assertEqual(rango(periodo(d('2028-01-31'), 0)), ('2028-01-31', '2028-02-28'))
        self.assertEqual(rango(periodo(d('2028-01-31'), 1)), ('2028-02-29', '2028-03-30'))   # existe el 29 de febrero

    def test_inicio_el_29_el_30_y_el_29_de_febrero(self):
        self.assertEqual(rango(periodo(d('2027-01-29'), 1)), ('2027-02-28', '2027-03-28'))
        self.assertEqual(rango(periodo(d('2027-01-30'), 1)), ('2027-02-28', '2027-03-29'))
        self.assertEqual(rango(periodo(d('2028-02-29'), 0)), ('2028-02-29', '2028-03-28'))
        self.assertEqual(rango(periodo(d('2028-02-29'), 12)), ('2029-02-28', '2029-03-28'))   # el año siguiente no es bisiesto

    def test_cambio_de_ano(self):
        self.assertEqual(rango(periodo(d('2026-12-15'), 0)), ('2026-12-15', '2027-01-14'))
        self.assertEqual(rango(periodo(d('2026-12-15'), 1)), ('2027-01-15', '2027-02-14'))
        self.assertEqual(rango(periodo(d('2026-11-30'), 3)), ('2027-02-28', '2027-03-29'))

    def test_dias_del_periodo(self):
        self.assertEqual([periodo(d('2027-01-01'), n).dias for n in range(3)], [31, 28, 31])
        self.assertEqual(periodo(d('2028-02-01'), 0).dias, 29)

    def test_los_periodos_son_contiguos_sin_huecos_ni_solapes_para_todo_ancla_y_varios_anos(self):
        for anio in (2026, 2027, 2028, 2100):   # 2100 no es bisiesto aunque es múltiplo de 4
            for dia in range(1, 32):
                for mes in range(1, 13):
                    if dia > calendar.monthrange(anio, mes)[1]:
                        continue
                    inicio = date(anio, mes, dia)
                    anterior = None
                    for per in periodos(inicio):
                        if per.numero == 30:
                            break
                        self.assertTrue(28 <= per.dias <= 31, (inicio, per))
                        if anterior is None:
                            self.assertEqual(per.inicio, inicio)
                        else:
                            self.assertEqual(anterior.fin + timedelta(days=1), per.inicio, (inicio, per))
                        anterior = per

    def test_periodo_que_contiene_coincide_con_el_recorrido_dia_a_dia(self):
        for inicio in (d('2026-01-10'), d('2027-01-31'), d('2028-01-31'), d('2026-12-15'), d('2027-03-30')):
            todos = [periodo(inicio, n) for n in range(26)]
            dia = inicio
            while dia <= todos[-1].fin:
                encontrado = periodo_que_contiene(inicio, dia)
                self.assertTrue(encontrado.inicio <= dia <= encontrado.fin, (inicio, dia, encontrado))
                self.assertEqual(encontrado, todos[encontrado.numero], (inicio, dia))
                dia += timedelta(days=1)

    def test_una_fecha_anterior_al_inicio_no_pertenece_a_ningun_periodo(self):
        self.assertIsNone(periodo_que_contiene(d('2026-01-10'), d('2026-01-09')))

    def test_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            periodo(d('2026-01-10'), -1)
        with self.assertRaises(TypeError):
            periodo('2026-01-10', 0)

    def test_periodos_desde_un_numero(self):
        primero = next(periodos(d('2026-01-10'), desde=5))
        self.assertEqual((primero.numero, primero.inicio), (5, d('2026-06-10')))


class MasMesesTests(SimpleTestCase):
    def test_suma_meses_y_recorta_al_ultimo_dia_si_no_existe(self):
        self.assertEqual(calculo.mas_meses(d('2026-10-26'), 3), d('2027-01-26'))
        self.assertEqual(calculo.mas_meses(d('2027-01-31'), 1), d('2027-02-28'))
        self.assertEqual(calculo.mas_meses(d('2028-01-31'), 1), d('2028-02-29'))
        self.assertEqual(calculo.mas_meses(d('2028-02-29'), 12), d('2029-02-28'))
        self.assertEqual(calculo.mas_meses(d('2026-12-15'), 3), d('2027-03-15'))
        self.assertEqual(calculo.mas_meses(d('2027-01-10'), 0), d('2027-01-10'))


class VencimientoTests(SimpleTestCase):
    def test_el_dia_de_vencimiento_dentro_del_mes_de_inicio(self):
        self.assertEqual(vencimiento(periodo(d('2026-01-01'), 0), 5), d('2026-01-05'))
        self.assertEqual(vencimiento(periodo(d('2026-01-10'), 0), 10), d('2026-01-10'))   # el mismo día de inicio

    def test_si_el_dia_es_anterior_al_inicio_se_usa_el_mes_siguiente(self):
        per = periodo(d('2026-01-10'), 0)   # 10 ene–9 feb
        self.assertEqual(vencimiento(per, 5), d('2026-02-05'))
        self.assertEqual(vencimiento(per, 9), d('2026-02-09'))

    def test_dia_31_en_meses_cortos_cae_en_el_ultimo_dia(self):
        self.assertEqual(vencimiento(periodo(d('2027-02-01'), 0), 31), d('2027-02-28'))
        self.assertEqual(vencimiento(periodo(d('2028-02-01'), 0), 31), d('2028-02-29'))
        self.assertEqual(vencimiento(periodo(d('2027-04-01'), 0), 31), d('2027-04-30'))

    def test_si_excede_el_ultimo_dia_del_periodo_se_usa_el_ultimo_dia_del_periodo(self):
        per = periodo(d('2027-03-31'), 0)   # 31 mar–29 abr
        self.assertEqual(vencimiento(per, 30), d('2027-04-29'))   # 30 mar < inicio → 30 abr > fin → 29 abr

    def test_ancla_31_con_vencimiento_31(self):
        self.assertEqual(vencimiento(periodo(d('2027-01-31'), 1), 31), d('2027-02-28'))   # período 28 feb–30 mar

    def test_siempre_cae_dentro_del_periodo_para_todo_dia_y_ancla(self):
        for anio in (2027, 2028):
            for ancla in (1, 15, 28, 29, 30, 31):
                for dia in range(1, 32):
                    for per in (periodo(date(anio, 1, min(ancla, 31)), n) for n in range(14)):
                        v = vencimiento(per, dia)
                        self.assertTrue(per.inicio <= v <= per.fin, (anio, ancla, dia, per, v))

    def test_dia_fuera_de_rango(self):
        for dia in (0, 32, -1):
            with self.assertRaises(ValueError):
                vencimiento(periodo(d('2026-01-10'), 0), dia)


class FechaLimiteTests(SimpleTestCase):
    def test_vencimiento_mas_dias_de_gracia(self):
        self.assertEqual(fecha_limite(d('2026-01-05'), 7), d('2026-01-12'))
        self.assertEqual(fecha_limite(d('2026-01-31'), 7), d('2026-02-07'))
        self.assertEqual(fecha_limite(d('2026-12-28'), 7), d('2027-01-04'))
        self.assertEqual(fecha_limite(d('2026-01-05'), 0), d('2026-01-05'))

    def test_gracia_negativa(self):
        with self.assertRaises(ValueError):
            fecha_limite(d('2026-01-05'), -1)


Condicion = namedtuple('Condicion', 'id vigente_desde')


class CondicionAplicableTests(SimpleTestCase):
    def test_gana_la_de_mayor_fecha_que_no_supere_el_inicio_del_periodo(self):
        a, b, c = Condicion(1, d('2026-01-01')), Condicion(2, d('2026-07-01')), Condicion(3, d('2027-01-01'))
        self.assertEqual(condicion_aplicable([c, a, b], d('2026-06-30')), a)
        self.assertEqual(condicion_aplicable([c, a, b], d('2026-07-01')), b)   # el mismo día cuenta
        self.assertEqual(condicion_aplicable([c, a, b], d('2030-01-01')), c)

    def test_ninguna_rige_todavia(self):
        self.assertIsNone(condicion_aplicable([Condicion(1, d('2026-07-01'))], d('2026-06-30')))
        self.assertIsNone(condicion_aplicable([], d('2026-06-30')))

    def test_propuesta_en_el_empate_gana_la_registrada_despues(self):
        inicial, correccion = Condicion(1, d('2026-01-01')), Condicion(9, d('2026-01-01'))
        self.assertEqual(condicion_aplicable([inicial, correccion], d('2026-03-01')), correccion)


class RedondeoTests(SimpleTestCase):
    def test_colones_a_la_unidad_con_empate_hacia_arriba(self):
        self.assertEqual(redondear(Decimal('0.5'), 'CRC'), Decimal('1'))
        self.assertEqual(redondear(Decimal('1.5'), 'CRC'), Decimal('2'))
        self.assertEqual(redondear(Decimal('2.5'), 'CRC'), Decimal('3'))   # el modo del par daría 2
        self.assertEqual(redondear(Decimal('106451.61'), 'CRC'), Decimal('106452'))
        self.assertEqual(redondear(Decimal('106451.49'), 'CRC'), Decimal('106451'))

    def test_dolares_a_dos_decimales_con_empate_hacia_arriba(self):
        self.assertEqual(redondear(Decimal('1.005'), 'USD'), Decimal('1.01'))   # el modo del par daría 1.00
        self.assertEqual(redondear(Decimal('1.015'), 'USD'), Decimal('1.02'))
        self.assertEqual(redondear(Decimal('1.004'), 'USD'), Decimal('1.00'))

    def test_no_acepta_float_ni_otra_moneda(self):
        with self.assertRaises(TypeError):
            redondear(1.5, 'CRC')
        with self.assertRaises(ValueError):
            redondear(Decimal('1'), 'EUR')


class ProrrateoTests(SimpleTestCase):
    def test_ejemplo_del_modelo_300000_por_11_entre_31(self):
        per = periodo(d('2027-01-01'), 0)   # enero, 31 días
        r = prorratear_ultimo_periodo(Decimal('300000'), 'CRC', per, d('2027-01-11'))
        self.assertEqual((r.importe_final, r.dias_cobrables, r.dias_del_periodo), (Decimal('106452'), 11, 31))
        self.assertEqual(r.importe_delta, Decimal('106452') - Decimal('300000'))
        self.assertEqual(r.importe_previo, '106451.612903')

    def test_los_dos_extremos_son_inclusivos(self):
        per = periodo(d('2027-01-01'), 0)
        self.assertEqual(prorratear_ultimo_periodo(Decimal('310'), 'CRC', per, d('2027-01-01')).dias_cobrables, 1)
        self.assertEqual(prorratear_ultimo_periodo(Decimal('310'), 'CRC', per, d('2027-01-30')).dias_cobrables, 30)

    def test_fecha_de_fin_el_ultimo_dia_del_periodo_no_se_prorratea(self):
        per = periodo(d('2027-01-10'), 0)
        self.assertIsNone(prorratear_ultimo_periodo(Decimal('300000'), 'CRC', per, per.fin))

    def test_febrero_comun_y_bisiesto_cambian_el_divisor(self):
        comun = prorratear_ultimo_periodo(Decimal('280000'), 'CRC', periodo(d('2027-02-01'), 0), d('2027-02-10'))
        bisiesto = prorratear_ultimo_periodo(Decimal('290000'), 'CRC', periodo(d('2028-02-01'), 0), d('2028-02-10'))
        self.assertEqual((comun.dias_del_periodo, comun.importe_final), (28, Decimal('100000')))      # 280000×10/28
        self.assertEqual((bisiesto.dias_del_periodo, bisiesto.importe_final), (29, Decimal('100000')))  # 290000×10/29

    def test_periodo_con_ancla_31_en_febrero(self):
        per = periodo(d('2027-01-31'), 1)   # 28 feb–30 mar, 31 días
        r = prorratear_ultimo_periodo(Decimal('310000'), 'CRC', per, d('2027-03-10'))
        self.assertEqual((r.dias_cobrables, r.dias_del_periodo, r.importe_final), (11, 31, Decimal('110000')))

    def test_empate_hacia_arriba_en_colones(self):
        per = periodo(d('2027-04-01'), 0)   # 30 días
        r = prorratear_ultimo_periodo(Decimal('15'), 'CRC', per, d('2027-04-01'))   # 15 × 1 / 30 = 0.5
        self.assertEqual(r.importe_final, Decimal('1'))   # round() de Python daría 0

    def test_empate_hacia_arriba_en_dolares(self):
        per = periodo(d('2027-04-01'), 0)   # 30 días
        r = prorratear_ultimo_periodo(Decimal('30.15'), 'USD', per, d('2027-04-01'))   # 30,15 × 1 / 30 = 1,005
        self.assertEqual(r.importe_final, Decimal('1.01'))   # el modo del par daría 1,00
        self.assertEqual(str(r.importe_final), '1.01')

    def test_dolares_con_importe_que_no_es_empate(self):
        per = periodo(d('2027-01-01'), 0)
        r = prorratear_ultimo_periodo(Decimal('500.00'), 'USD', per, d('2027-01-10'))   # 500×10/31 = 161,2903…
        self.assertEqual(r.importe_final, Decimal('161.29'))

    def test_se_redondea_una_sola_vez_al_final(self):
        """Si se redondeara el importe diario antes de multiplicar, 100 × 7 / 30 daría 7 × 3,33 = 23,31 y no 23,33."""
        per = periodo(d('2027-04-01'), 0)
        r = prorratear_ultimo_periodo(Decimal('100.00'), 'USD', per, d('2027-04-07'))
        self.assertEqual(r.importe_final, Decimal('23.33'))

    def test_el_delta_puede_ser_cero_cuando_el_redondeo_iguala_al_monto(self):
        per = periodo(d('2027-04-01'), 0)   # 30 días
        r = prorratear_ultimo_periodo(Decimal('1'), 'CRC', per, d('2027-04-29'))   # 29/30 = 0,9667 → 1
        self.assertEqual((r.importe_final, r.importe_delta), (Decimal('1'), Decimal('0')))

    def test_el_resultado_nunca_supera_al_monto_ni_es_negativo(self):
        per = periodo(d('2027-01-01'), 0)
        for fin in (per.inicio + timedelta(days=n) for n in range(per.dias - 1)):
            r = prorratear_ultimo_periodo(Decimal('300000.00'), 'USD', per, fin)
            self.assertTrue(0 < r.importe_final <= Decimal('300000.00'), fin)
            self.assertTrue(r.importe_delta <= 0, fin)

    def test_coincide_con_la_formula_exacta_en_decimal(self):
        for dias_del_periodo, cobrables, monto in ((31, 11, '300000'), (28, 13, '123457'), (30, 7, '99999'), (29, 28, '1000001')):
            per = periodo(d('2028-02-01') if dias_del_periodo == 29 else d('2027-02-01') if dias_del_periodo == 28
                          else d('2027-04-01') if dias_del_periodo == 30 else d('2027-01-01'), 0)
            fin = per.inicio + timedelta(days=cobrables - 1)
            r = prorratear_ultimo_periodo(Decimal(monto), 'CRC', per, fin)
            exacto = (Decimal(monto) * cobrables) / Decimal(dias_del_periodo)
            self.assertEqual(r.importe_final, exacto.quantize(Decimal(1), rounding=ROUND_HALF_UP), (dias_del_periodo, cobrables))

    def test_datos_de_calculo_reconstruyen_la_regla(self):
        per = periodo(d('2027-01-01'), 0)
        r = prorratear_ultimo_periodo(Decimal('300000'), 'CRC', per, d('2027-01-11'))
        self.assertEqual(r.datos_calculo(), {
            'regla': 'prorrateo_ultimo_periodo', 'dias_cobrables': 11, 'dias_del_periodo': 31,
            'importe_previo': '106451.612903', 'importe_final': '106452', 'moneda': 'CRC'})

    def test_entradas_invalidas(self):
        per = periodo(d('2027-01-01'), 0)
        for monto, moneda, fin, error in ((Decimal('0'), 'CRC', d('2027-01-10'), ValueError),
                                          (Decimal('-5'), 'CRC', d('2027-01-10'), ValueError),
                                          (Decimal('300000'), 'EUR', d('2027-01-10'), ValueError),
                                          (Decimal('300000'), 'CRC', d('2026-12-31'), ValueError),
                                          (Decimal('300000'), 'CRC', d('2027-02-01'), ValueError),
                                          (300000.0, 'CRC', d('2027-01-10'), TypeError),
                                          (300000, 'CRC', d('2027-01-10'), TypeError)):
            with self.assertRaises(error, msg=str((monto, moneda, fin))):
                prorratear_ultimo_periodo(monto, moneda, per, fin)

    def test_el_modulo_no_usa_float(self):
        import inspect
        codigo = inspect.getsource(calculo)
        self.assertNotIn('float(', codigo)
