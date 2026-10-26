"""Cálculo de períodos, vencimientos, fechas límite y del prorrateo del último período (RN-03, RN-05, RN-06, RN-12,
RN-13). Funciones puras: no leen la base, el reloj ni la zona horaria; las fechas llegan como `date` y los importes
como `Decimal` (nunca `float`, MDD sección 1.1). Los servicios de los grupos C a E las usan.

Convenciones:
- El **día ancla** es el día de `fecha_inicio` (RN-03). Cada período empieza ese día del mes que le toca, o el último día
  de ese mes si el mes no lo tiene, y termina el día anterior al inicio del siguiente. El ancla se toma siempre de
  `fecha_inicio`, nunca del período anterior: un contrato que empieza un 31 vuelve al 31 en los meses que lo tienen.
- El período número 0 es el primero (el que empieza en `fecha_inicio`).
"""
import calendar
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction

CRC, USD = 'CRC', 'USD'
UNIDAD_MONETARIA = {CRC: Decimal(1), USD: Decimal('0.01')}  # RN-12: colones a la unidad, dólares a dos decimales


@dataclass(frozen=True)
class Periodo:
    numero: int
    inicio: date
    fin: date  # inclusive

    @property
    def dias(self):
        return (self.fin - self.inicio).days + 1


def _ultimo_dia(anio, mes):
    return calendar.monthrange(anio, mes)[1]


def _con_dia(anio, mes, dia):
    """La fecha del `dia` de ese mes, o el último día del mes si no lo tiene (RN-03, RN-05)."""
    return date(anio, mes, min(dia, _ultimo_dia(anio, mes)))


def _sumar_meses(anio, mes, meses):
    indice = anio * 12 + (mes - 1) + meses
    return indice // 12, indice % 12 + 1


def _inicio_del_periodo(fecha_inicio, numero):
    anio, mes = _sumar_meses(fecha_inicio.year, fecha_inicio.month, numero)
    return _con_dia(anio, mes, fecha_inicio.day)


def periodo(fecha_inicio, numero):
    """El período `numero` (desde 0) de un contrato que empieza en `fecha_inicio` (RN-03). Ejemplo: inicio el 10 de
    enero; período 0: 10 ene–9 feb; período 1: 10 feb–9 mar."""
    if not isinstance(fecha_inicio, date):
        raise TypeError('fecha_inicio debe ser una fecha')
    if numero < 0:
        raise ValueError('El número de período no puede ser negativo.')
    inicio = _inicio_del_periodo(fecha_inicio, numero)
    return Periodo(numero, inicio, _inicio_del_periodo(fecha_inicio, numero + 1) - timedelta(days=1))


def periodo_que_contiene(fecha_inicio, fecha):
    """El período al que pertenece `fecha`, o None si es anterior al inicio del contrato (RN-03)."""
    if fecha < fecha_inicio:
        return None
    numero = (fecha.year - fecha_inicio.year) * 12 + fecha.month - fecha_inicio.month
    candidato = periodo(fecha_inicio, numero)
    if fecha < candidato.inicio:  # la fecha cae en el mes del período, pero antes de su inicio: es del anterior
        return periodo(fecha_inicio, numero - 1)
    return candidato


def periodos(fecha_inicio, desde=0):
    """Los períodos sucesivos desde el número `desde`, sin fin: quien llama corta el recorrido."""
    numero = desde
    while True:
        yield periodo(fecha_inicio, numero)
        numero += 1


def vencimiento(per, dia_vencimiento):
    """Fecha de vencimiento de la obligación de un período (RN-05): el `dia_vencimiento` del mes en que inicia el
    período, o el último día de ese mes si no existe; si esa fecha es anterior al inicio del período, el mes siguiente;
    si excede el último día del período, el último día del período. Así siempre cae dentro del período."""
    if not 1 <= dia_vencimiento <= 31:
        raise ValueError('El día de vencimiento va de 1 a 31.')
    candidata = _con_dia(per.inicio.year, per.inicio.month, dia_vencimiento)
    if candidata < per.inicio:
        anio, mes = _sumar_meses(per.inicio.year, per.inicio.month, 1)
        candidata = _con_dia(anio, mes, dia_vencimiento)
    return min(candidata, per.fin)


def fecha_limite(fecha_de_vencimiento, dias_gracia):
    """Fecha límite de pago: el vencimiento más los días de gracia (RN-06)."""
    if dias_gracia < 0:
        raise ValueError('Los días de gracia no pueden ser negativos.')
    return fecha_de_vencimiento + timedelta(days=dias_gracia)


def condicion_aplicable(condiciones, inicio_del_periodo):
    """De las condiciones de un contrato, la que rige un período: la de mayor `vigente_desde` que no supere el inicio
    del período (MDD sección 3.3). `condiciones` es una lista de objetos con `vigente_desde` e `id`. **Propuesta del
    asistente** para el empate de `vigente_desde` (una corrección que lleva la misma fecha efectiva que la anterior):
    gana la registrada después, de mayor `id`. Devuelve None si ninguna rige todavía."""
    vigentes = [c for c in condiciones if c.vigente_desde <= inicio_del_periodo]
    return max(vigentes, key=lambda c: (c.vigente_desde, c.id)) if vigentes else None


def redondear(importe, moneda):
    """Redondea una sola vez a la unidad monetaria con empate hacia arriba (`ROUND_HALF_UP`, RN-12): colones a la unidad
    entera y dólares a dos decimales. Python y `Decimal` redondean al par por omisión; aquí el modo es explícito."""
    _exigir_decimal(importe)
    if moneda not in UNIDAD_MONETARIA:
        raise ValueError(f'Moneda desconocida: {moneda}')
    return importe.quantize(UNIDAD_MONETARIA[moneda], rounding=ROUND_HALF_UP)


def _exigir_decimal(valor):
    if isinstance(valor, float) or not isinstance(valor, Decimal):
        raise TypeError('Los importes son Decimal, nunca float.')


@dataclass(frozen=True)
class Prorrateo:
    """Resultado del prorrateo del último período (RN-12, RN-13)."""
    importe_final: Decimal
    importe_delta: Decimal  # final − monto mensual; puede ser cero si el redondeo lo iguala (no se registra ajuste)
    dias_cobrables: int
    dias_del_periodo: int
    importe_previo: str  # el cociente exacto sin redondear, con 6 decimales, solo descriptivo (RN-13)
    moneda: str

    def datos_calculo(self):
        """El diccionario que se guarda en `Obligacion.datos_calculo` para reconstruir la regla (RN-13)."""
        return {
            'regla': 'prorrateo_ultimo_periodo', 'dias_cobrables': self.dias_cobrables,
            'dias_del_periodo': self.dias_del_periodo, 'importe_previo': self.importe_previo,
            'importe_final': str(self.importe_final), 'moneda': self.moneda,
        }


def prorratear_ultimo_periodo(monto_mensual, moneda, per, fecha_fin):
    """Prorratea por días el último período cuando `fecha_fin` cae dentro de él (RN-12, RF-09):
    `importe = monto × días cobrables / días del período`, con ambos extremos inclusivos, en aritmética exacta y
    redondeado una sola vez al final. Devuelve None si `fecha_fin` es el último día del período (período completo: los
    completos no se prorratean). Lanza ValueError si `fecha_fin` no está dentro del período."""
    _exigir_decimal(monto_mensual)
    if monto_mensual <= 0:
        raise ValueError('El monto mensual debe ser mayor que cero.')
    if not per.inicio <= fecha_fin <= per.fin:
        raise ValueError('La fecha de fin no está dentro del período.')
    if fecha_fin == per.fin:
        return None
    cobrables = (fecha_fin - per.inicio).days + 1
    exacto = Fraction(monto_mensual) * cobrables / per.dias  # Fraction: sin pérdida hasta el único redondeo
    previo = Decimal(exacto.numerator) / Decimal(exacto.denominator)
    unidad = Fraction(UNIDAD_MONETARIA[moneda]) if moneda in UNIDAD_MONETARIA else None
    if unidad is None:
        raise ValueError(f'Moneda desconocida: {moneda}')
    unidades = (exacto / unidad + Fraction(1, 2)).__floor__()  # empate hacia arriba; el importe es positivo
    final = (Decimal(unidades) * UNIDAD_MONETARIA[moneda]).quantize(UNIDAD_MONETARIA[moneda])
    return Prorrateo(
        importe_final=final, importe_delta=final - monto_mensual, dias_cobrables=cobrables, dias_del_periodo=per.dias,
        importe_previo=str(previo.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)), moneda=moneda)
