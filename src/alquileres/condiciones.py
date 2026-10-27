"""Reajuste, corrección y ajuste manual del importe (RF-09, RF-10, RN-12, RN-14; CA-12, CA-22, CA-39, CA-40, CA-51, CA-55).

Todo cambio de importe es un `AjusteObligacion` inmutable y todo cambio de condiciones es una fila nueva de
`CondicionContrato`: nada se sobrescribe y el importe vigente se deriva (ADR-014, ADR-016). Cada operación va en una
transacción con su auditoría; si algún ajuste dejara una obligación por debajo de lo abonado, **no se cambia nada**.

La única excepción a la inmutabilidad es la de la decisión 3 de la E2 (26-oct-2026): una corrección retroactiva puede
actualizar `fecha_vencimiento` y `fecha_limite` de las obligaciones no pagadas, con el valor anterior y el nuevo en la
auditoría.
"""
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction

from django.db import transaction
from django.utils import timezone

from nucleo import auditoria, formato

from . import calculo, movimientos, selectors
from .models import AjusteObligacion, CondicionContrato, Obligacion
from .services import ErrorDeValidacion, _bloquear_contrato, _decimal, _entero, _fecha, _texto, _validar_monto

MAXIMO_TOPE = Decimal(100)                # propuesta del asistente: un tope razonable en %, la ERS no lo fija
MAXIMO_PORCENTAJE = Decimal('9999.9999')  # lo que cabe en `numeric(8,4)`
MAXIMO_DIAS_GRACIA = 365


@dataclass(frozen=True)
class ResultadoDeCondicion:
    """Lo que devuelve una operación de condiciones: la condición nueva (o None en un ajuste manual), las advertencias
    que no bloquean y cuántas obligaciones se ajustaron, se dejaron igual o se saltaron."""
    condicion: CondicionContrato | None
    advertencias: tuple = ()
    ajustadas: int = 0
    sin_cambio: int = 0
    saltadas_pagadas: int = 0
    saltadas_manuales: int = 0
    fechas_corregidas: int = 0
    ajustes: tuple = ()


def _esta_pagada(obligacion, vigente):
    abonado = movimientos.abonos_validos(obligacion)
    return abonado > 0 and abonado >= vigente


def _importe_objetivo(contrato, obligacion, monto):
    """El importe que le corresponde a la obligación con ese monto mensual: el monto completo, o su prorrateo si el período
    contiene el fin del contrato (RN-12)."""
    fin = contrato.fecha_fin
    if fin is not None and obligacion.periodo_inicio <= fin < obligacion.periodo_fin:
        numero = calculo.periodo_que_contiene(contrato.fecha_inicio, obligacion.periodo_inicio).numero
        per = calculo.Periodo(numero, obligacion.periodo_inicio, obligacion.periodo_fin)
        return calculo.prorratear_ultimo_periodo(monto, obligacion.moneda, per, fin).importe_final
    return monto


def _comprobar_no_baja_de_lo_abonado(obligacion, objetivo):
    abonado = movimientos.abonos_validos(obligacion)
    if objetivo < abonado:
        exceso = abonado - objetivo
        raise ErrorDeValidacion({'importe': [
            f'El cambio deja el importe de un período en {formato.moneda(objetivo, obligacion.moneda)}, '
            f'por debajo de lo ya abonado ({formato.moneda(abonado, obligacion.moneda)}): '
            f'el exceso es de {formato.moneda(exceso, obligacion.moneda)}.']})


def _ajustar_importes(contrato, condicion, tipo, motivo, actor, ip_origen, ahora):
    """Ajusta, con filas nuevas, las obligaciones regulares, no anuladas y no pagadas cuyo período inicia en o después
    de la fecha efectiva (RF-10), al monto de la condición que rige cada período. Las pagadas no se tocan; las que
    tuvieron un ajuste manual (RF-09) tampoco, para no deshacer una decisión explícita; si algún cambio deja una obligación
    por debajo de lo abonado se rechaza todo (CA-40)."""
    condiciones = list(contrato.condiciones.all())
    ajustes, sin_cambio, pagadas, manuales = [], 0, 0, 0
    obligaciones = Obligacion.objects.select_for_update().filter(
        contrato=contrato, tipo=Obligacion.REGULAR, anulada_en__isnull=True,
        periodo_inicio__gte=condicion.vigente_desde).order_by('periodo_inicio')
    for obligacion in obligaciones:
        vigente = selectors.importe_vigente(obligacion)
        if _esta_pagada(obligacion, vigente):
            pagadas += 1
            continue
        if AjusteObligacion.objects.filter(obligacion=obligacion, tipo=AjusteObligacion.AJUSTE_MANUAL).exists():
            manuales += 1
            continue
        aplicable = calculo.condicion_aplicable(condiciones, obligacion.periodo_inicio)
        objetivo = _importe_objetivo(contrato, obligacion, aplicable.monto_mensual)
        if objetivo == vigente:
            sin_cambio += 1
            continue
        _comprobar_no_baja_de_lo_abonado(obligacion, objetivo)
        ajuste = AjusteObligacion.objects.create(
            obligacion=obligacion, tipo=tipo, importe_delta=objetivo - vigente, condicion=condicion, motivo=motivo,
            registrado_en=ahora)
        auditoria.registrar('ajuste_registrado', 'obligacion', registro_id=obligacion.pk, actor=actor, ip_origen=ip_origen,
                            cambios={'importe_vigente': (vigente, objetivo), 'tipo': (None, tipo)}, ahora=ahora)
        ajustes.append(ajuste)
    return ajustes, sin_cambio, pagadas, manuales


def _corregir_fechas_de_pago(contrato, condicion, actor, ip_origen, ahora):
    """Decisión 3 de la E2: actualiza `fecha_vencimiento` y `fecha_limite` de las obligaciones regulares, no anuladas y
    no pagadas cuyo período inicia en o después de la fecha efectiva, según la condición que rige cada período."""
    condiciones = list(contrato.condiciones.all())
    corregidas = 0
    obligaciones = Obligacion.objects.select_for_update().filter(
        contrato=contrato, tipo=Obligacion.REGULAR, anulada_en__isnull=True,
        periodo_inicio__gte=condicion.vigente_desde).order_by('periodo_inicio')
    for obligacion in obligaciones:
        if _esta_pagada(obligacion, selectors.importe_vigente(obligacion)):
            continue
        aplicable = calculo.condicion_aplicable(condiciones, obligacion.periodo_inicio)
        numero = calculo.periodo_que_contiene(contrato.fecha_inicio, obligacion.periodo_inicio).numero
        per = calculo.Periodo(numero, obligacion.periodo_inicio, obligacion.periodo_fin)
        vencimiento = calculo.vencimiento(per, aplicable.dia_vencimiento)
        limite = calculo.fecha_limite(vencimiento, aplicable.dias_gracia)
        if (vencimiento, limite) == (obligacion.fecha_vencimiento, obligacion.fecha_limite):
            continue
        antes = (obligacion.fecha_vencimiento, obligacion.fecha_limite)
        obligacion.fecha_vencimiento, obligacion.fecha_limite = vencimiento, limite
        obligacion.save(update_fields=['fecha_vencimiento', 'fecha_limite'])
        auditoria.registrar('obligacion_fechas_corregidas', 'obligacion', registro_id=obligacion.pk, actor=actor,
                            ip_origen=ip_origen, cambios={'fecha_vencimiento': (antes[0], vencimiento),
                                                          'fecha_limite': (antes[1], limite)}, ahora=ahora)
        corregidas += 1
    return corregidas


def _porcentaje(actual, nuevo):
    """(nuevo − actual) / actual × 100, exacto como fracción y redondeado a 4 decimales (`numeric(8,4)`)."""
    exacto = (Fraction(nuevo) - Fraction(actual)) / Fraction(actual) * 100
    redondeado = (Decimal(exacto.numerator) / Decimal(exacto.denominator)).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    return exacto, redondeado


@transaction.atomic
def reajustar_contrato(contrato_id, *, actor, ip_origen=None, fecha_notificacion, nuevo_monto, tope_digitado=None,
                       fuente_tope=None, motivo=None, ahora=None):
    """Reajuste del monto (RF-10, RN-14; CA-12, CA-39, CA-51). La fecha efectiva se normaliza al inicio del período
    siguiente al que contiene la notificación; aplica a las obligaciones de períodos que inician desde entonces y las
    anteriores mantienen su monto. En vivienda se exige el tope vigente y su fuente (certificación del INEC o
    publicación del MIVAH); si el porcentaje lo supera solo se advierte (DP-22); una vivienda con precio en dólares se
    rechaza (OL-07). Advertencias y reglas legales: pendientes de validación por un abogado (DP-17)."""
    ahora = ahora or timezone.now()
    hoy = selectors.hoy_local(ahora)
    contrato = _bloquear_contrato(contrato_id)
    errores = {}
    notificacion = _fecha(fecha_notificacion, 'fecha_notificacion', errores)
    monto = _validar_monto(nuevo_monto, errores, 'nuevo_monto')
    es_vivienda = contrato.destino == contrato.VIVIENDA
    if es_vivienda and contrato.moneda != calculo.CRC:
        errores['moneda'] = ['Una vivienda con el precio en moneda extranjera no se reajusta (OL-07, pendiente de validación por un abogado).']
    tope, fuente = _validar_tope(tope_digitado, fuente_tope, es_vivienda, errores)
    if notificacion is not None:
        if notificacion < contrato.fecha_inicio:
            errores['fecha_notificacion'] = ['La notificación no puede ser anterior al inicio del contrato.']
        elif notificacion > hoy:
            errores['fecha_notificacion'] = ['La fecha de notificación no puede ser futura.']
    efectiva = actual = None
    if notificacion is not None and 'fecha_notificacion' not in errores:
        efectiva = calculo.periodo(contrato.fecha_inicio, calculo.periodo_que_contiene(contrato.fecha_inicio, notificacion).numero + 1).inicio
        if contrato.fecha_fin is not None and efectiva > contrato.fecha_fin:
            errores['fecha_notificacion'] = [f'La fecha efectiva ({efectiva.isoformat()}) queda después del fin del contrato.']
        elif contrato.condiciones.filter(tipo=CondicionContrato.REAJUSTE, vigente_desde=efectiva).exists():
            errores['fecha_notificacion'] = [f'Ya hay un reajuste con fecha efectiva {efectiva.isoformat()}; use una corrección.']
        else:
            actual = selectors.condicion_vigente_en(contrato, efectiva)
    if monto is not None and actual is not None and monto == actual.monto_mensual:
        errores['nuevo_monto'] = ['El nuevo monto es igual al actual: no hay nada que reajustar.']
    if errores:
        raise ErrorDeValidacion(errores)

    exacto, porcentaje = _porcentaje(actual.monto_mensual, monto)
    if abs(porcentaje) > MAXIMO_PORCENTAJE:
        raise ErrorDeValidacion({'nuevo_monto': ['El porcentaje de cambio es desproporcionado: revise el monto.']})
    advertencias = []
    if es_vivienda and exacto > Fraction(tope):
        advertencias.append(f'El reajuste es de {formato.porcentaje(porcentaje, 2)} y supera el tope digitado de '
                            f'{formato.porcentaje(tope, 2)} ({fuente}); un reajuste mayor al legal es nulo (OL-06, '
                            'pendiente de validación por un abogado). Se guardó de todos modos.')
    condicion = CondicionContrato.objects.create(
        contrato=contrato, monto_mensual=monto, dia_vencimiento=actual.dia_vencimiento, dias_gracia=actual.dias_gracia,
        vigente_desde=efectiva, tipo=CondicionContrato.REAJUSTE, fecha_notificacion=notificacion, porcentaje=porcentaje,
        tope_digitado=tope, fuente_tope=fuente, motivo=_texto(motivo) or None, registrada_en=ahora)
    auditoria.registrar('contrato_reajustado', 'contrato', registro_id=contrato.pk, actor=actor, ip_origen=ip_origen, cambios={
        'monto_mensual': (actual.monto_mensual, monto), 'vigente_desde': (None, efectiva),
        'fecha_notificacion': (None, notificacion), 'porcentaje': (None, porcentaje), 'tope_digitado': (None, tope),
        'fuente_tope': (None, fuente), 'motivo': (None, _texto(motivo) or None)}, ahora=ahora)
    ajustes, sin_cambio, pagadas, manuales = _ajustar_importes(
        contrato, condicion, AjusteObligacion.REAJUSTE, _texto(motivo), actor, ip_origen, ahora)
    return ResultadoDeCondicion(condicion, tuple(advertencias), len(ajustes), sin_cambio, pagadas, manuales, 0, tuple(ajustes))


def _validar_tope(tope_digitado, fuente_tope, es_vivienda, errores):
    """El tope digitado y su fuente: obligatorios en vivienda (CA-51); en otro destino, opcionales pero juntos."""
    sin_tope = tope_digitado in (None, '')
    fuente = _texto(fuente_tope)
    if sin_tope and not fuente:
        if es_vivienda:
            errores['tope_digitado'] = ['En una vivienda debe digitar el porcentaje máximo vigente y su fuente '
                                        '(certificación del INEC o publicación del MIVAH).']
        return None, None
    tope = None
    if sin_tope:
        errores['tope_digitado'] = ['Digite el tope junto con su fuente.']
    else:
        tope = _decimal(tope_digitado, 'tope_digitado', errores)
        if tope is not None and not Decimal(0) <= tope <= MAXIMO_TOPE:
            errores['tope_digitado'] = [f'El tope va de 0 a {MAXIMO_TOPE} %.']
            tope = None
        elif tope is not None and tope != tope.quantize(Decimal('0.0001')):
            errores['tope_digitado'] = ['El tope admite hasta cuatro decimales.']
            tope = None
    if not fuente:
        errores['fuente_tope'] = ['Indique la fuente del tope (certificación del INEC o publicación del MIVAH).']
    elif len(fuente) > 200:
        errores['fuente_tope'] = ['La fuente no puede pasar de 200 caracteres.']
    return (tope, fuente) if not {'tope_digitado', 'fuente_tope'} & set(errores) else (None, None)


@transaction.atomic
def corregir_contrato(contrato_id, *, actor, ip_origen=None, fecha_efectiva, motivo, monto_mensual=None,
                      dia_vencimiento=None, dias_gracia=None, ahora=None):
    """Corrección retroactiva de monto, día de vencimiento o días de gracia (RF-10, RN-14; CA-22, CA-40, CA-55), con
    motivo obligatorio. Registra una condición nueva desde `fecha_efectiva` y la aplica a las obligaciones no pagadas,
    incluidas las vencidas, cuyo período inicia en o después de esa fecha: el importe con ajustes inmutables y, por la
    decisión 3 de la E2, las fechas de vencimiento y límite actualizándolas con auditoría. Las pagadas no cambian y
    un cambio que deje una obligación por debajo de lo abonado se bloquea mostrando el exceso. Un error en el
    período (la fecha de inicio) no se corrige aquí: se anula el contrato si no tiene movimientos o se crea uno nuevo."""
    ahora = ahora or timezone.now()
    contrato = _bloquear_contrato(contrato_id)
    errores = {}
    efectiva = _fecha(fecha_efectiva, 'fecha_efectiva', errores)
    if not _texto(motivo):
        errores['motivo'] = ['El motivo es obligatorio en una corrección.']
    monto = None if monto_mensual in (None, '') else _validar_monto(monto_mensual, errores, 'monto_mensual')
    dia = None if dia_vencimiento in (None, '') else _entero(
        dia_vencimiento, 'dia_vencimiento', errores, 1, 31, 'El día de vencimiento va de 1 a 31.')
    gracia = None if dias_gracia in (None, '') else _entero(
        dias_gracia, 'dias_gracia', errores, 0, MAXIMO_DIAS_GRACIA, f'Los días de gracia van de 0 a {MAXIMO_DIAS_GRACIA}.')
    if monto_mensual in (None, '') and dia_vencimiento in (None, '') and dias_gracia in (None, ''):
        errores['correccion'] = ['Indique qué se corrige: el monto, el día de vencimiento o los días de gracia.']
    actual = None
    if efectiva is not None:
        if efectiva < contrato.fecha_inicio:
            errores['fecha_efectiva'] = ['La fecha efectiva no puede ser anterior al inicio del contrato.']
        elif contrato.fecha_fin is not None and efectiva > contrato.fecha_fin:
            errores['fecha_efectiva'] = ['La fecha efectiva queda después del fin del contrato.']
        else:
            actual = selectors.condicion_vigente_en(contrato, efectiva)
    if actual is None and not errores:
        errores['fecha_efectiva'] = ['No hay condiciones vigentes en esa fecha.']
    if actual is not None and not errores:
        nuevos = (monto if monto is not None else actual.monto_mensual, dia if dia is not None else actual.dia_vencimiento,
                  gracia if gracia is not None else actual.dias_gracia)
        if nuevos == (actual.monto_mensual, actual.dia_vencimiento, actual.dias_gracia):
            errores['correccion'] = ['La corrección no cambia nada respecto de las condiciones vigentes en esa fecha.']
    if errores:
        raise ErrorDeValidacion(errores)

    condicion = CondicionContrato.objects.create(
        contrato=contrato, monto_mensual=nuevos[0], dia_vencimiento=nuevos[1], dias_gracia=nuevos[2], vigente_desde=efectiva,
        tipo=CondicionContrato.CORRECCION, motivo=_texto(motivo), registrada_en=ahora)
    auditoria.registrar('contrato_corregido', 'contrato', registro_id=contrato.pk, actor=actor, ip_origen=ip_origen, cambios={
        'monto_mensual': (actual.monto_mensual, nuevos[0]), 'dia_vencimiento': (actual.dia_vencimiento, nuevos[1]),
        'dias_gracia': (actual.dias_gracia, nuevos[2]), 'vigente_desde': (None, efectiva), 'motivo': (None, _texto(motivo))},
        ahora=ahora)
    ajustes, sin_cambio, pagadas, manuales = _ajustar_importes(
        contrato, condicion, AjusteObligacion.CORRECCION, _texto(motivo), actor, ip_origen, ahora)
    fechas = _corregir_fechas_de_pago(contrato, condicion, actor, ip_origen, ahora)
    advertencias = []
    if manuales:
        advertencias.append(f'{manuales} obligación(es) con un ajuste manual conservaron su importe.')
    return ResultadoDeCondicion(condicion, tuple(advertencias), len(ajustes), sin_cambio, pagadas, manuales, fechas, tuple(ajustes))


@transaction.atomic
def ajustar_manualmente(obligacion_id, *, actor, ip_origen=None, nuevo_importe, motivo, ahora=None):
    """Ajuste manual del importe del último período con motivo y auditoría (RF-09, RN-12): solo la obligación regular,
    no anulada, cuyo período contiene la fecha de fin de un contrato cerrado. Es un ajuste inmutable; no puede dejar el
    importe por debajo de lo abonado."""
    ahora = ahora or timezone.now()
    contrato = _bloquear_contrato(Obligacion.objects.only('contrato_id').get(pk=obligacion_id).contrato_id)   # primero el contrato, como en el resto
    obligacion = Obligacion.objects.select_for_update().get(pk=obligacion_id)
    errores = {}
    nuevo = _validar_monto(nuevo_importe, errores, 'nuevo_importe')
    if not _texto(motivo):
        errores['motivo'] = ['El motivo es obligatorio en un ajuste manual.']
    if obligacion.anulada_en is not None or obligacion.tipo != Obligacion.REGULAR:
        errores['obligacion'] = ['Solo se ajusta una obligación regular que no esté anulada.']
    elif contrato.cerrado_en is None or contrato.fecha_fin is None or not (
            obligacion.periodo_inicio <= contrato.fecha_fin <= obligacion.periodo_fin):
        errores['obligacion'] = ['El ajuste manual es solo para la obligación del último período de un contrato finalizado (RF-09).']
    vigente = selectors.importe_vigente(obligacion)
    if nuevo is not None and nuevo == vigente:
        errores['nuevo_importe'] = ['La obligación ya tiene ese importe.']
    if errores:
        raise ErrorDeValidacion(errores)
    _comprobar_no_baja_de_lo_abonado(obligacion, nuevo)
    ajuste = AjusteObligacion.objects.create(
        obligacion=obligacion, tipo=AjusteObligacion.AJUSTE_MANUAL, importe_delta=nuevo - vigente, motivo=_texto(motivo),
        registrado_en=ahora)
    auditoria.registrar('ajuste_registrado', 'obligacion', registro_id=obligacion.pk, actor=actor, ip_origen=ip_origen,
                        cambios={'importe_vigente': (vigente, nuevo), 'tipo': (None, AjusteObligacion.AJUSTE_MANUAL),
                                 'motivo': (None, _texto(motivo))}, ahora=ahora)
    return ajuste
