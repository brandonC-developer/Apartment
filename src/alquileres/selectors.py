"""Lectura de propiedades y contratos: estados derivados (RN-30, RF-06, RF-42). No audita (RF-45 solo exige auditar la
cédula) ni escribe. Los estados no se almacenan: se derivan de las fechas y de las marcas (MDD sección 5)."""
from decimal import Decimal

from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from . import movimientos
from .models import AjusteObligacion, Contrato, Propiedad

PENDIENTE, VENCIDA, PAGADA, ANULADA = 'pendiente', 'vencida', 'pagada', 'anulada'  # estados de la obligación (RF-14)
FUTURO, VIGENTE, POR_DECIDIR, FINALIZADO, ANULADO = 'futuro', 'vigente', 'por_decidir', 'finalizado', 'anulado'
ESTADOS_DE_CONTRATO = (FUTURO, VIGENTE, POR_DECIDIR, FINALIZADO, ANULADO)
DISPONIBLE, OCUPADA, INACTIVA = 'disponible', 'ocupada', 'inactiva'
ESTADOS_QUE_OCUPAN = (FUTURO, VIGENTE, POR_DECIDIR)  # RF-06: no se inactiva la propiedad ni se desactiva al inquilino


def hoy_local(ahora=None):
    return timezone.localdate(ahora)


def estado_del_contrato(contrato, hoy=None):
    """RN-30: anulado; futuro si hoy es anterior al inicio; con fecha de fin vencida, finalizado si el administrador lo
    cerró (RF-09) o por decidir si no (RF-42); en cualquier otro caso, vigente."""
    hoy = hoy or hoy_local()
    if contrato.anulado_en is not None:
        return ANULADO
    if hoy < contrato.fecha_inicio:
        return FUTURO
    if contrato.fecha_fin is not None and contrato.fecha_fin < hoy:
        return FINALIZADO if contrato.cerrado_en is not None else POR_DECIDIR
    return VIGENTE


def _filtro_de_estado(estados, hoy):
    """El mismo cálculo de `estado_del_contrato`, para consultas (sin cargar los contratos)."""
    consulta = Q(pk__in=[])
    no_anulado = Q(anulado_en__isnull=True)
    if FUTURO in estados:
        consulta |= no_anulado & Q(fecha_inicio__gt=hoy)
    en_curso = no_anulado & Q(fecha_inicio__lte=hoy)
    if VIGENTE in estados:
        consulta |= en_curso & (Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=hoy))
    if POR_DECIDIR in estados:
        consulta |= en_curso & Q(fecha_fin__lt=hoy, cerrado_en__isnull=True)
    if FINALIZADO in estados:
        consulta |= en_curso & Q(fecha_fin__lt=hoy, cerrado_en__isnull=False)
    if ANULADO in estados:
        consulta |= Q(anulado_en__isnull=False)
    return consulta


def contratos_en_estado(*estados, hoy=None, **filtros):
    """Los contratos que están en alguno de esos estados hoy; `filtros` acota (por ejemplo, `inquilino=`)."""
    hoy = hoy or hoy_local()
    return Contrato.objects.filter(_filtro_de_estado(estados, hoy), **filtros)


def contratos_que_ocupan_la_propiedad(propiedad, hoy=None):
    """Contratos futuros, vigentes o por decidir de una propiedad (RF-06, CA-63)."""
    return contratos_en_estado(*ESTADOS_QUE_OCUPAN, hoy=hoy, propiedad=propiedad)


def contratos_que_ocupan_al_inquilino(inquilino, hoy=None):
    """Contratos futuros, vigentes o por decidir de un inquilino (RF-04, CA-29)."""
    return contratos_en_estado(*ESTADOS_QUE_OCUPAN, hoy=hoy, inquilino=inquilino)


def estado_de_la_propiedad(propiedad, hoy=None):
    """RF-06: inactiva si el administrador la marcó; ocupada si tiene un contrato vigente; si no, disponible."""
    if propiedad.inactiva:
        return INACTIVA
    return OCUPADA if contratos_en_estado(VIGENTE, POR_DECIDIR, hoy=hoy, propiedad=propiedad).exists() else DISPONIBLE


def contrato_vigente_de_la_propiedad(propiedad, hoy=None):
    """El contrato vigente (o por decidir) de la propiedad, o None; la cédula y el contrato se agregan desde su perfil (RF-51)."""
    return contratos_en_estado(VIGENTE, POR_DECIDIR, hoy=hoy, propiedad=propiedad).first()


def listar_propiedades(*, busqueda=None, incluir_inactivas=True):
    propiedades = Propiedad.objects.all()
    texto = (busqueda or '').strip()
    if texto:
        propiedades = propiedades.filter(Q(alias__icontains=texto) | Q(direccion__icontains=texto))
    return propiedades if incluir_inactivas else propiedades.filter(inactiva=False)


def condicion_vigente_en(contrato, fecha):
    """La condición del contrato que rige en una fecha: la de mayor `vigente_desde` que no la supere; en un empate,
    la registrada después (propuesta, ver `calculo.condicion_aplicable`)."""
    from . import calculo
    return calculo.condicion_aplicable(list(contrato.condiciones.all()), fecha)


def historial_de_importes(obligacion):
    """El importe de la obligación paso a paso: el inicial y cada ajuste con su importe anterior y el nuevo, para
    reconstruir los valores sin que ninguno se haya sobrescrito (CA-22, CA-55, ADR-016)."""
    pasos, actual = [], obligacion.importe_inicial
    pasos.append({'registrado_en': obligacion.creado_en, 'tipo': 'inicial', 'motivo': '', 'anterior': None, 'nuevo': actual})
    for ajuste in AjusteObligacion.objects.filter(obligacion=obligacion).order_by('registrado_en', 'id'):
        pasos.append({'registrado_en': ajuste.registrado_en, 'tipo': ajuste.tipo, 'motivo': ajuste.motivo,
                      'anterior': actual, 'nuevo': actual + ajuste.importe_delta})
        actual += ajuste.importe_delta
    return pasos


def saldo_de_la_obligacion(obligacion):
    """Importe vigente menos los movimientos válidos aplicados (RN-22): se deriva, nunca se guarda. Hasta la E3 no hay
    movimientos y el saldo es el importe vigente."""
    return importe_vigente(obligacion) - movimientos.abonos_validos(obligacion)


def estado_de_la_obligacion(obligacion, hoy=None):
    """RF-14: anulada si fue anulada; pagada si el saldo es cero; vencida si hay saldo y `hoy` (la fecha local de la
    organización) supera la fecha límite; pendiente en cualquier otro caso. El último día de gracia aún es pendiente."""
    hoy = hoy or hoy_local()
    if obligacion.anulada_en is not None:
        return ANULADA
    if saldo_de_la_obligacion(obligacion) <= 0:
        return PAGADA
    return VENCIDA if hoy > obligacion.fecha_limite else PENDIENTE


def importe_vigente(obligacion):
    """Importe exigible vigente: el inicial más la suma de sus ajustes (MDD sección 5, RF-10)."""
    suma = AjusteObligacion.objects.filter(obligacion=obligacion).aggregate(total=Coalesce(Sum('importe_delta'), Decimal('0')))
    return obligacion.importe_inicial + suma['total']
