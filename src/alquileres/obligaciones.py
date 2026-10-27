"""Generación de obligaciones y saldo de apertura (RF-11, RF-12, RF-43, RN-04, RN-05, RN-06, RN-12, RNF-04, RNF-16;
CA-03, CA-14, CA-30, CA-49, CA-50).

`generar_obligaciones` crea las obligaciones que faltan de un contrato y no hace nada si ya están todas: es idempotente
y segura en paralelo (bloquea la fila del contrato y la restricción única de la base es la última defensa, R1). La
usan el proceso diario (`proceso.py`) y, si el administrador la pide, una llamada manual.
"""
from datetime import date, timedelta

from django.db import IntegrityError, transaction
from django.utils import timezone

from inquilinos.services import ErrorDeValidacion
from nucleo import auditoria

from . import calculo, selectors, services
from .models import Contrato, Obligacion

DIAS_DE_ANTICIPACION = 30  # RF-11, CA-30: la obligación se genera 30 días antes de que inicie el período
REGLA_DE_APERTURA = 'saldo_de_apertura'


def _autor(actor, ejecucion_id, ip_origen=None):
    """Los datos de auditoría de quien genera. R19: el proceso es el actor «sistema» y lleva su ejecución; el
    administrador no lleva ejecución."""
    if ejecucion_id is not None:
        return {'actor': 'sistema', 'tipo_actor': 'proceso', 'ejecucion_id': ejecucion_id}
    if actor in (None, '', 'sistema'):
        raise ValueError('Una generación sin ejecución del proceso necesita el actor administrador.')
    return {'actor': actor, 'ip_origen': ip_origen}


def fecha_de_apertura(contrato):
    """La fecha del saldo de apertura del contrato, o None si no tiene. Se guarda en `datos_calculo` de la obligación
    de apertura (propuesta del asistente: el modelo no tiene otra columna para ella)."""
    apertura = Obligacion.objects.filter(contrato=contrato, tipo=Obligacion.APERTURA).first()
    if apertura is None or not apertura.datos_calculo:
        return None
    return date.fromisoformat(apertura.datos_calculo['fecha_apertura'])


def _periodos_por_generar(contrato, hoy, ya_generados, desde_apertura, por_decidir):
    """Los períodos cuya obligación toca generar hoy: los que inician hasta 30 días después de `hoy` y, mientras el
    contrato no está *por decidir*, a lo sumo en la fecha de fin (RF-11); un contrato por decidir sigue generando sin
    ese tope (RF-42). Sin los incluidos en el saldo de apertura (RF-43) ni los ya generados."""
    limite = hoy + timedelta(days=DIAS_DE_ANTICIPACION)
    for per in calculo.periodos(contrato.fecha_inicio):
        if per.inicio > limite or (contrato.fecha_fin is not None and per.inicio > contrato.fecha_fin and not por_decidir):
            return
        if desde_apertura is not None and per.inicio <= desde_apertura:
            continue
        if per.inicio not in ya_generados:
            yield per


def generar_obligaciones(contrato_id, *, actor=None, ip_origen=None, ejecucion_id=None, hoy=None, ahora=None):
    """Genera las obligaciones que faltan del contrato (RF-11) y devuelve las creadas, en orden de período.

    Solo contratos *futuros*, *vigentes* o *por decidir* (RF-11, RF-42). Cada período usa la condición que lo rige
    (RN-14), con su monto, día de vencimiento y días de gracia; el vencimiento cae dentro del período (RN-05, CA-50) y la
    fecha límite suma la gracia (RN-06). Si el contrato tiene fecha de fin dentro de un período, esa obligación nace
    prorrateada con el mismo ajuste que al finalizar (RN-12, CA-14). Un contrato *por decidir* sigue generando después de
    su fecha de fin, con el importe completo (RF-42). Los períodos que inician hasta la fecha de apertura quedan dentro
    del saldo de apertura y no se generan (CA-49)."""
    ahora = ahora or timezone.now()
    hoy = hoy or selectors.hoy_local(ahora)
    autor = _autor(actor, ejecucion_id, ip_origen)
    with transaction.atomic():
        contrato = Contrato.objects.select_for_update().get(pk=contrato_id)
        estado = selectors.estado_del_contrato(contrato, hoy)
        if estado not in selectors.ESTADOS_QUE_OCUPAN:
            return []
        existentes = set(Obligacion.objects.filter(contrato=contrato, tipo=Obligacion.REGULAR)
                         .values_list('periodo_inicio', flat=True))
        condiciones = list(contrato.condiciones.all())
        creadas = []
        for per in _periodos_por_generar(
                contrato, hoy, existentes, fecha_de_apertura(contrato), estado == selectors.POR_DECIDIR):
            condicion = calculo.condicion_aplicable(condiciones, per.inicio)
            vencimiento = calculo.vencimiento(per, condicion.dia_vencimiento)
            try:
                with transaction.atomic():
                    obligacion = Obligacion.objects.create(
                        contrato=contrato, tipo=Obligacion.REGULAR, periodo_inicio=per.inicio, periodo_fin=per.fin,
                        fecha_vencimiento=vencimiento, fecha_limite=calculo.fecha_limite(vencimiento, condicion.dias_gracia),
                        importe_inicial=condicion.monto_mensual, moneda=contrato.moneda, condicion=condicion)
            except IntegrityError:
                continue   # otra ejecución la creó entre la lectura y la inserción: no es un error (RF-12)
            auditoria.registrar(
                'obligacion_generada', 'obligacion', registro_id=obligacion.pk, ahora=ahora,
                cambios={'contrato': (None, contrato.pk), 'periodo_inicio': (None, per.inicio),
                         'importe_inicial': (None, obligacion.importe_inicial)}, **autor)
            if contrato.fecha_fin is not None and per.inicio <= contrato.fecha_fin < per.fin:
                services._prorratear(contrato, obligacion, contrato.fecha_fin, autor['actor'], ip_origen, ahora,
                                     {k: v for k, v in autor.items() if k in ('tipo_actor', 'ejecucion_id')})
            creadas.append(obligacion)
        return creadas


@transaction.atomic
def registrar_saldo_de_apertura(contrato_id, *, actor, ip_origen=None, importe, fecha_apertura, fecha_vencimiento=None,
                                ahora=None, hoy=None):
    """Registra el saldo de apertura de un contrato que empezó antes de cargarse en el sistema (RF-43, CA-49): una
    obligación sin período por lo adeudado por todos los períodos iniciados hasta `fecha_apertura`. Su vencimiento lo
    digita el administrador (por omisión, la fecha de apertura más los días de gracia del contrato) y su fecha límite es
    esa misma fecha; no hay alertas retroactivas porque la obligación vence desde esa fecha.

    Reglas propuestas por el asistente: la fecha de apertura no es anterior al inicio del contrato ni futura; el
    vencimiento no es anterior a la fecha de apertura; solo hay un saldo de apertura por contrato (R1); no se registra si
    ya hay obligaciones regulares vigentes de períodos incluidos en el saldo (se duplicaría lo adeudado)."""
    ahora = ahora or timezone.now()
    hoy = hoy or selectors.hoy_local(ahora)
    contrato = services._bloquear_contrato(contrato_id)
    errores = {}
    monto = services._validar_monto(importe, errores, 'importe')
    apertura = services._fecha(fecha_apertura, 'fecha_apertura', errores)
    vence = services._fecha(fecha_vencimiento, 'fecha_vencimiento', errores, obligatoria=False)
    if apertura is not None:
        if apertura < contrato.fecha_inicio:
            errores['fecha_apertura'] = ['La fecha de apertura no puede ser anterior al inicio del contrato.']
        elif apertura > hoy:
            errores['fecha_apertura'] = ['La fecha de apertura no puede ser futura.']
        elif Obligacion.objects.filter(contrato=contrato, tipo=Obligacion.REGULAR, anulada_en__isnull=True,
                                       periodo_inicio__lte=apertura).exists():
            errores['fecha_apertura'] = ['El contrato ya tiene obligaciones de períodos incluidos en el saldo de apertura.']
    if Obligacion.objects.filter(contrato=contrato, tipo=Obligacion.APERTURA).exists():
        errores['contrato'] = ['El contrato ya tiene un saldo de apertura.']
    if apertura is not None and vence is not None and vence < apertura:
        errores['fecha_vencimiento'] = ['El vencimiento no puede ser anterior a la fecha de apertura.']
    if errores:
        raise ErrorDeValidacion(errores)
    if vence is None:
        condicion = selectors.condicion_vigente_en(contrato, apertura)
        vence = calculo.fecha_limite(apertura, condicion.dias_gracia)
    obligacion = Obligacion.objects.create(
        contrato=contrato, tipo=Obligacion.APERTURA, fecha_vencimiento=vence, fecha_limite=vence, importe_inicial=monto,
        moneda=contrato.moneda,
        datos_calculo={'regla': REGLA_DE_APERTURA, 'fecha_apertura': apertura.isoformat()})
    auditoria.registrar(
        'saldo_apertura_registrado', 'obligacion', registro_id=obligacion.pk, actor=actor, ip_origen=ip_origen,
        ahora=ahora, cambios={'contrato': (None, contrato.pk), 'importe_inicial': (None, monto),
                              'fecha_apertura': (None, apertura), 'fecha_vencimiento': (None, vence)})
    return obligacion
