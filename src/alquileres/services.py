"""Escritura de propiedades y contratos: registrar, crear, finalizar, renovar, anular y sustituir (RF-06 a RF-10, RF-36,
RF-42, RF-48; RN-02, RN-17, RN-30; CA-02, CA-24, CA-29, CA-31, CA-32, CA-62, CA-63, CA-67, CA-78).

Cada operación va en una transacción con su registro de auditoría (RF-28). Los servicios no leen la sesión ni la
petición: reciben el actor y la IP. Las lecturas están en `selectors.py` y los cálculos en `calculo.py` (ADR-030).
Los errores de datos son `inquilinos.services.ErrorDeValidacion`, los mismos que ya manejan las vistas.
"""
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils import timezone

from inquilinos import selectors as selectores_de_inquilinos
from inquilinos.models import Inquilino
from inquilinos.services import ErrorDeValidacion
from nucleo import auditoria

from . import calculo, movimientos, selectors
from .models import AjusteObligacion, CondicionContrato, Contrato, Obligacion, Propiedad

DIAS_GRACIA_PREDETERMINADOS = 7  # RN-06
MAXIMO_DIAS_GRACIA = 365  # propuesta del asistente: un tope razonable; la ERS no lo fija
MESES_DE_AVISO = 3  # RF-09 y OL-09: aviso de tres meses
ANIOS_MINIMOS = 3  # RF-07, OL-08: vigencia mínima de tres años (advertencia, no bloqueo)
CAMPOS_DE_LA_PROPIEDAD = ('alias', 'descripcion', 'direccion')


class NoSePuedeInactivar(Exception):
    """La propiedad tiene un contrato futuro, vigente o por decidir (RF-06, CA-63)."""

    def __init__(self, motivos):
        super().__init__('No se puede marcar inactiva')
        self.motivos = list(motivos)


@dataclass(frozen=True)
class Resultado:
    """Lo que devuelve una operación sobre un contrato: el contrato, las advertencias que no bloquean y lo que hizo."""
    contrato: Contrato
    advertencias: tuple = ()
    obligaciones_anuladas: int = 0
    ajuste: AjusteObligacion | None = None


# --- validación

def _texto(valor):
    return (valor or '').strip()


def _fecha(valor, campo, errores, obligatoria=True):
    if valor is None or valor == '':
        if obligatoria:
            errores[campo] = ['La fecha es obligatoria.']
        return None
    if isinstance(valor, date) and not hasattr(valor, 'hour'):
        return valor
    errores[campo] = ['La fecha no es válida.']
    return None


def _decimal(valor, campo, errores):
    if isinstance(valor, float):
        errores[campo] = ['El importe no puede darse como número decimal binario; use un texto o Decimal.']
        return None
    try:
        numero = valor if isinstance(valor, Decimal) else Decimal(str(valor).strip().replace(' ', ''))
    except (InvalidOperation, ValueError, TypeError):
        errores[campo] = ['El importe no es un número válido.']
        return None
    if not numero.is_finite():
        errores[campo] = ['El importe no es un número válido.']
        return None
    return numero


def _entero(valor, campo, errores, minimo, maximo, texto):
    try:
        if isinstance(valor, bool) or isinstance(valor, float):
            raise ValueError
        numero = int(str(valor).strip())
    except (ValueError, TypeError):
        errores[campo] = [texto]
        return None
    if not minimo <= numero <= maximo:
        errores[campo] = [texto]
        return None
    return numero


def _validar_propiedad(datos, *, parciales=False, excluir_id=None):
    errores, limpios = {}, {}
    if not parciales or 'alias' in datos:
        alias = _texto(datos.get('alias'))
        if not alias:
            errores['alias'] = ['El alias es obligatorio.']
        elif len(alias) > 60:
            errores['alias'] = ['El alias no puede pasar de 60 caracteres.']
        elif Propiedad.objects.filter(alias__iexact=alias).exclude(pk=excluir_id).exists():
            errores['alias'] = ['Ya existe una propiedad con ese alias.']
        else:
            limpios['alias'] = alias
    for campo in ('descripcion', 'direccion'):
        if not parciales or campo in datos:
            limpios[campo] = _texto(datos.get(campo))
    if errores:
        raise ErrorDeValidacion(errores)
    return limpios


def _validar_condiciones(datos, fecha_inicio, errores):
    """Monto, día de vencimiento y días de gracia (R3). El día de vencimiento, por omisión, es el de inicio (DP-24)."""
    monto = _decimal(datos.get('monto_mensual'), 'monto_mensual', errores)
    if monto is not None:
        if monto <= 0:
            errores['monto_mensual'] = ['El monto mensual debe ser mayor que cero.']
            monto = None
        elif monto != monto.quantize(Decimal('0.01')) or abs(monto) >= Decimal(10) ** 12:
            errores['monto_mensual'] = ['El monto admite hasta dos decimales y no más de 12 cifras enteras.']
            monto = None
    dia = datos.get('dia_vencimiento')
    if dia in (None, ''):
        dia = fecha_inicio.day if fecha_inicio else None
    else:
        dia = _entero(dia, 'dia_vencimiento', errores, 1, 31, 'El día de vencimiento va de 1 a 31.')
    gracia = datos.get('dias_gracia')
    if gracia in (None, ''):
        gracia = DIAS_GRACIA_PREDETERMINADOS
    else:
        gracia = _entero(gracia, 'dias_gracia', errores, 0, MAXIMO_DIAS_GRACIA,
                         f'Los días de gracia van de 0 a {MAXIMO_DIAS_GRACIA}.')
    return monto, dia, gracia


def _solapados(propiedad_id, inicio, fin, excluir_id=None):
    """Contratos no anulados de la propiedad que comparten algún día con [inicio, fin] (ambos inclusive; sin fin, abierto)."""
    consulta = Contrato.objects.filter(propiedad_id=propiedad_id, anulado_en__isnull=True)
    consulta = consulta.filter(Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=inicio))
    if fin is not None:
        consulta = consulta.filter(fecha_inicio__lte=fin)
    return consulta.exclude(pk=excluir_id) if excluir_id else consulta


def _mensaje_de_solape(contratos):
    primero = contratos.order_by('fecha_inicio').first()
    fin = primero.fecha_fin.isoformat() if primero.fecha_fin else 'sin fecha de fin'
    return (f'Las fechas se solapan con otro contrato de la propiedad (del {primero.fecha_inicio.isoformat()} al {fin}); '
            'el nuevo debe empezar al menos el día siguiente al fin del anterior.')


def _advertencia_de_vigencia(fecha_inicio, fecha_fin):
    """RF-07: avisa, sin bloquear, si la vigencia pactada es menor de tres años (OL-08; propuesta de cómo medirla: el
    contrato dura tres años si termina, como mínimo, el día anterior al tercer aniversario del inicio)."""
    if fecha_fin is None:
        return None
    if fecha_fin < calculo.mas_meses(fecha_inicio, 12 * ANIOS_MINIMOS) - timedelta(days=1):
        return ('La vigencia pactada es menor de tres años; para una vivienda la ley entiende de tres años una duración '
                'menor o no pactada (OL-08, pendiente de validación por un abogado).')
    return None


def _auditar(accion, contrato, actor, ip_origen, cambios, ahora):
    return auditoria.registrar(accion, 'contrato', registro_id=contrato.pk, actor=actor, ip_origen=ip_origen,
                               cambios=cambios, ahora=ahora)


# --- propiedades (RF-06)

@transaction.atomic
def registrar_propiedad(*, actor, ip_origen=None, datos, ahora=None):
    """Registra una propiedad con su alias único (R20, CA-63)."""
    ahora = ahora or timezone.now()
    limpios = _validar_propiedad(datos)
    try:
        with transaction.atomic():
            propiedad = Propiedad.objects.create(**limpios)
    except IntegrityError:   # otro alias igual llegó a la vez
        raise ErrorDeValidacion({'alias': ['Ya existe una propiedad con ese alias.']})
    auditoria.registrar('propiedad_registrada', 'propiedad', registro_id=propiedad.pk, actor=actor, ip_origen=ip_origen,
                        cambios={campo: (None, valor) for campo, valor in limpios.items()}, ahora=ahora)
    return propiedad


@transaction.atomic
def actualizar_propiedad(propiedad_id, *, actor, ip_origen=None, datos, ahora=None):
    ahora = ahora or timezone.now()
    desconocidos = set(datos) - set(CAMPOS_DE_LA_PROPIEDAD)
    if desconocidos:
        raise ValueError(f'Campos no editables: {sorted(desconocidos)}')
    propiedad = Propiedad.objects.select_for_update().get(pk=propiedad_id)
    limpios = _validar_propiedad(datos, parciales=True, excluir_id=propiedad.pk)
    cambios = {c: (getattr(propiedad, c), v) for c, v in limpios.items() if getattr(propiedad, c) != v}
    if not cambios:
        return propiedad
    for campo, (_, nuevo) in cambios.items():
        setattr(propiedad, campo, nuevo)
    try:
        with transaction.atomic():
            propiedad.save(update_fields=list(cambios))
    except IntegrityError:
        raise ErrorDeValidacion({'alias': ['Ya existe una propiedad con ese alias.']})
    auditoria.registrar('propiedad_actualizada', 'propiedad', registro_id=propiedad.pk, actor=actor, ip_origen=ip_origen,
                        cambios=cambios, ahora=ahora)
    return propiedad


@transaction.atomic
def marcar_inactiva(propiedad_id, *, actor, ip_origen=None, ahora=None, hoy=None):
    """RF-06, CA-63: se bloquea si la propiedad tiene un contrato futuro, vigente o por decidir."""
    ahora = ahora or timezone.now()
    propiedad = Propiedad.objects.select_for_update().get(pk=propiedad_id)
    if propiedad.inactiva:
        raise ErrorDeValidacion({'propiedad': ['La propiedad ya está inactiva.']})
    contratos = selectors.contratos_que_ocupan_la_propiedad(propiedad, hoy or selectors.hoy_local(ahora))
    if contratos.exists():
        raise NoSePuedeInactivar([
            f'Tiene un contrato {selectors.estado_del_contrato(c, hoy or selectors.hoy_local(ahora)).replace("_", " ")} '
            f'(desde el {c.fecha_inicio.isoformat()}).' for c in contratos])
    propiedad.inactiva = True
    propiedad.save(update_fields=['inactiva'])
    auditoria.registrar('propiedad_inactivada', 'propiedad', registro_id=propiedad.pk, actor=actor, ip_origen=ip_origen,
                        cambios={'inactiva': (False, True)}, ahora=ahora)
    return propiedad


@transaction.atomic
def reactivar_propiedad(propiedad_id, *, actor, ip_origen=None, ahora=None):
    ahora = ahora or timezone.now()
    propiedad = Propiedad.objects.select_for_update().get(pk=propiedad_id)
    if not propiedad.inactiva:
        raise ErrorDeValidacion({'propiedad': ['La propiedad ya está activa.']})
    propiedad.inactiva = False
    propiedad.save(update_fields=['inactiva'])
    auditoria.registrar('propiedad_reactivada', 'propiedad', registro_id=propiedad.pk, actor=actor, ip_origen=ip_origen,
                        cambios={'inactiva': (True, False)}, ahora=ahora)
    return propiedad


# --- contratos

@transaction.atomic
def crear_contrato(*, actor, ip_origen=None, inquilino_id, propiedad_id, datos, ahora=None):
    """Crea el contrato con su condición inicial (RF-07, CA-02). Rechaza, con todos los motivos a la vez: datos
    incoherentes, inquilino sin consentimiento vigente (CA-67) o sin el frente de su documento (R26, CA-78), propiedad
    inactiva (CA-63) y solapes (R2, CA-24). La vigencia menor de tres años solo advierte. El depósito (RF-29) es de la E3."""
    ahora = ahora or timezone.now()
    inquilino = Inquilino.objects.select_for_update().get(pk=inquilino_id)
    propiedad = Propiedad.objects.select_for_update().get(pk=propiedad_id)
    errores = {}
    inicio = _fecha(datos.get('fecha_inicio'), 'fecha_inicio', errores)
    fin = _fecha(datos.get('fecha_fin'), 'fecha_fin', errores, obligatoria=False)
    destino = _texto(datos.get('destino'))
    if destino not in {d for d, _ in Contrato.DESTINOS}:
        errores['destino'] = ['Elija vivienda u otro.']
    moneda = _texto(datos.get('moneda'))
    if moneda not in (calculo.CRC, calculo.USD):
        errores['moneda'] = ['Elija colones (CRC) o dólares (USD).']
    monto, dia, gracia = _validar_condiciones(datos, inicio, errores)
    if inicio and fin and fin < inicio:
        errores['fecha_fin'] = ['La fecha de fin no puede ser anterior a la de inicio.']
    if inquilino.desasociado_en is not None:
        errores['inquilino'] = ['El inquilino ya fue desasociado: no se le pueden crear contratos.']
    elif not inquilino.activo:
        errores['inquilino'] = ['El inquilino está desactivado: reactívelo antes de crearle un contrato.']
    if 'inquilino' not in errores:
        if not selectores_de_inquilinos.tiene_consentimiento_vigente(inquilino):
            errores['consentimiento'] = ['El inquilino no tiene un consentimiento vigente (RF-39): no se puede crear un contrato nuevo.']
        if not selectores_de_inquilinos.tiene_frente(inquilino):
            errores['frente'] = ['Falta el frente de la fotografía del documento del inquilino: cárguelo antes de crear el contrato.']
    if propiedad.inactiva:
        errores['propiedad'] = ['La propiedad está inactiva y no admite contratos nuevos.']
    if inicio and 'fecha_fin' not in errores:
        solapados = _solapados(propiedad.pk, inicio, fin)
        if solapados.exists():
            errores['fechas'] = [_mensaje_de_solape(solapados)]
    if errores:
        raise ErrorDeValidacion(errores)

    try:
        with transaction.atomic():
            contrato = Contrato.objects.create(
                inquilino=inquilino, propiedad=propiedad, destino=destino, fecha_inicio=inicio, fecha_fin=fin, moneda=moneda)
    except IntegrityError:   # otro contrato se coló entre la comprobación y el guardado (la base es la última defensa)
        raise ErrorDeValidacion({'fechas': ['Las fechas se solapan con otro contrato de la propiedad.']})
    CondicionContrato.objects.create(
        contrato=contrato, monto_mensual=monto, dia_vencimiento=dia, dias_gracia=gracia, vigente_desde=inicio,
        tipo=CondicionContrato.INICIAL, registrada_en=ahora)
    _auditar('contrato_creado', contrato, actor, ip_origen, {
        'inquilino_id': (None, inquilino.pk), 'propiedad_id': (None, propiedad.pk), 'destino': (None, destino),
        'fecha_inicio': (None, inicio), 'fecha_fin': (None, fin), 'moneda': (None, moneda),
        'monto_mensual': (None, monto), 'dia_vencimiento': (None, dia), 'dias_gracia': (None, gracia)}, ahora)
    advertencia = _advertencia_de_vigencia(inicio, fin)
    return Resultado(contrato, (advertencia,) if advertencia else ())


def _bloquear_contrato(contrato_id):
    contrato = Contrato.objects.select_for_update().get(pk=contrato_id)
    if contrato.anulado_en is not None:
        raise ErrorDeValidacion({'contrato': ['El contrato está anulado.']})
    return contrato


def _anular_obligacion(obligacion, motivo, actor, ip_origen, ahora):
    obligacion.anulada_en, obligacion.motivo_anulacion = ahora, motivo
    obligacion.save(update_fields=['anulada_en', 'motivo_anulacion'])
    auditoria.registrar('obligacion_anulada', 'obligacion', registro_id=obligacion.pk, actor=actor, ip_origen=ip_origen,
                        cambios={'anulada': (False, True), 'motivo': (None, motivo)}, ahora=ahora)


@transaction.atomic
def finalizar_contrato(contrato_id, *, actor, ip_origen=None, fecha_fin, ahora=None, hoy=None):
    """Registra la fecha de fin y cierra el contrato (RF-09, RN-17, CA-31, CA-10): las obligaciones cuyo período inicia
    después del fin y no tienen movimientos válidos se anulan con auditoría; la del período que contiene el fin se
    prorratea (RN-12) con un ajuste inmutable; las obligaciones y movimientos existentes se conservan. Advierte, sin
    bloquear, si el fin está a menos de tres meses de la fecha de registro (propuesta: se mide hacia adelante, y un fin
    ya pasado también avisa). Un contrato cerrado no se reabre; solo puede acortarse el fin, no alargarse (eso es
    renovar)."""
    ahora = ahora or timezone.now()
    hoy = hoy or selectors.hoy_local(ahora)
    contrato = _bloquear_contrato(contrato_id)
    errores = {}
    fin = _fecha(fecha_fin, 'fecha_fin', errores)
    if contrato.cerrado_en is not None:
        errores['contrato'] = ['El contrato ya está cerrado. Para una nueva relación cree un contrato nuevo.']
    if fin is not None:
        if fin < contrato.fecha_inicio:
            errores['fecha_fin'] = ['La fecha de fin no puede ser anterior a la de inicio.']
        elif contrato.fecha_fin is not None and fin > contrato.fecha_fin:
            errores['fecha_fin'] = ['La fecha de fin no puede ser posterior a la actual: para alargar el contrato use «renovar».']
    if errores:
        raise ErrorDeValidacion(errores)

    anterior = contrato.fecha_fin
    contrato.fecha_fin, contrato.cerrado_en = fin, ahora
    contrato.save(update_fields=['fecha_fin', 'cerrado_en'])
    _auditar('contrato_finalizado', contrato, actor, ip_origen,
             {'fecha_fin': (anterior, fin), 'cerrado': (False, True)}, ahora)

    obligaciones = list(Obligacion.objects.select_for_update().filter(
        contrato=contrato, tipo=Obligacion.REGULAR, anulada_en__isnull=True).order_by('periodo_inicio'))
    anuladas, ajuste = 0, None
    for obligacion in obligaciones:
        if obligacion.periodo_inicio > fin:
            if not movimientos.obligacion_tiene_movimientos_validos(obligacion):
                _anular_obligacion(obligacion, f'Contrato finalizado el {fin.isoformat()}', actor, ip_origen, ahora)
                anuladas += 1
        elif obligacion.periodo_inicio <= fin <= obligacion.periodo_fin:
            ajuste = _prorratear(contrato, obligacion, fin, actor, ip_origen, ahora)

    advertencias = []
    if fin < calculo.mas_meses(hoy, MESES_DE_AVISO):
        advertencias.append('La fecha de fin dista menos de tres meses de hoy; el aviso previo es de tres meses '
                            '(OL-09, pendiente de validación por un abogado).')
    return Resultado(contrato, tuple(advertencias), anuladas, ajuste)


def _prorratear(contrato, obligacion, fin, actor, ip_origen, ahora):
    """Ajuste inmutable `prorrateo_fin` de la obligación del último período (RN-12, RF-09). El delta puede ser cero
    cuando el redondeo iguala al importe: en ese caso no se registra ningún ajuste."""
    numero = calculo.periodo_que_contiene(contrato.fecha_inicio, obligacion.periodo_inicio).numero
    per = calculo.Periodo(numero, obligacion.periodo_inicio, obligacion.periodo_fin)
    vigente = selectors.importe_vigente(obligacion)
    resultado = calculo.prorratear_ultimo_periodo(vigente, obligacion.moneda, per, fin)
    if resultado is None or resultado.importe_delta == 0:
        return None
    if resultado.importe_final < movimientos.abonos_validos(obligacion):
        raise ErrorDeValidacion({'fecha_fin': [
            'La fecha de fin deja el importe del último período por debajo de lo ya abonado; '
            'elija una fecha posterior o registre antes la reversión.']})
    ajuste = AjusteObligacion.objects.create(
        obligacion=obligacion, tipo=AjusteObligacion.PRORRATEO_FIN, importe_delta=resultado.importe_delta,
        motivo=(f'Prorrateo del último período: {resultado.dias_cobrables} de {resultado.dias_del_periodo} días '
                f'(fin {fin.isoformat()}; importe previo {resultado.importe_previo})'), registrado_en=ahora)
    auditoria.registrar('ajuste_prorrateo_registrado', 'obligacion', registro_id=obligacion.pk, actor=actor,
                        ip_origen=ip_origen, cambios={'importe_vigente': (vigente, resultado.importe_final)}, ahora=ahora)
    return ajuste


@transaction.atomic
def renovar_contrato(contrato_id, *, actor, ip_origen=None, nueva_fecha_fin, motivo, ahora=None):
    """Renueva el contrato cambiando su fecha de fin a una posterior, o quitándola (contrato abierto), con motivo y
    auditoría (RF-42, CA-32; decisión 2 de la E2, 26-oct-2026). Sigue siendo el mismo contrato y su serie de
    obligaciones continúa. Se rechaza si el contrato está anulado o cerrado, si ya es abierto, si la fecha no es posterior
    a la actual o si el cambio solapa con otro contrato."""
    ahora = ahora or timezone.now()
    contrato = _bloquear_contrato(contrato_id)
    errores = {}
    nueva = _fecha(nueva_fecha_fin, 'nueva_fecha_fin', errores, obligatoria=False)
    if not _texto(motivo):
        errores['motivo'] = ['El motivo es obligatorio.']
    if contrato.cerrado_en is not None:
        errores['contrato'] = ['El contrato ya está cerrado: para una nueva relación cree un contrato nuevo.']
    elif contrato.fecha_fin is None:
        errores['contrato'] = ['El contrato ya es abierto: no tiene fecha de fin que renovar.']
    elif nueva is not None and nueva <= contrato.fecha_fin:
        errores['nueva_fecha_fin'] = ['La nueva fecha de fin debe ser posterior a la actual.']
    if not errores:
        solapados = _solapados(contrato.propiedad_id, contrato.fecha_inicio, nueva, excluir_id=contrato.pk)
        if solapados.exists():
            errores['fechas'] = [_mensaje_de_solape(solapados)]
    if errores:
        raise ErrorDeValidacion(errores)
    anterior = contrato.fecha_fin
    contrato.fecha_fin = nueva
    try:
        with transaction.atomic():
            contrato.save(update_fields=['fecha_fin'])
    except IntegrityError:
        raise ErrorDeValidacion({'fechas': ['Las fechas se solapan con otro contrato de la propiedad.']})
    _auditar('contrato_renovado', contrato, actor, ip_origen,
             {'fecha_fin': (anterior, nueva), 'motivo': (None, _texto(motivo))}, ahora)
    return Resultado(contrato)


@transaction.atomic
def anular_contrato(contrato_id, *, actor, ip_origen=None, motivo, ahora=None):
    """Anula el contrato (RF-48, CA-62): solo si no tiene movimientos válidos (ni de alquiler ni de depósito) y con
    motivo. Sus obligaciones quedan anuladas (RN-17) y deja de contar para el solape (RN-02). El depósito sin abonos se
    anula en la E3, que lo crea."""
    ahora = ahora or timezone.now()
    contrato = _bloquear_contrato(contrato_id)
    motivo = _texto(motivo)
    errores = {}
    if not motivo:
        errores['motivo'] = ['El motivo es obligatorio.']
    if movimientos.contrato_tiene_movimientos_validos(contrato):
        errores['contrato'] = ['El contrato ya tiene movimientos válidos: no se anula, se finaliza (RF-09).']
    if errores:
        raise ErrorDeValidacion(errores)
    contrato.anulado_en, contrato.motivo_anulacion = ahora, motivo
    contrato.save(update_fields=['anulado_en', 'motivo_anulacion'])
    _auditar('contrato_anulado', contrato, actor, ip_origen, {'anulado': (False, True), 'motivo': (None, motivo)}, ahora)
    anuladas = 0
    for obligacion in Obligacion.objects.select_for_update().filter(contrato=contrato, anulada_en__isnull=True):
        _anular_obligacion(obligacion, f'Contrato anulado: {motivo}', actor, ip_origen, ahora)
        anuladas += 1
    return Resultado(contrato, obligaciones_anuladas=anuladas)


@transaction.atomic
def sustituir_inquilino(contrato_id, *, actor, ip_origen=None, fecha_fin, inquilino_id, datos, ahora=None):
    """Cierra el contrato anterior y crea uno nuevo para la misma propiedad, en una sola transacción: si el nuevo no es
    válido (por ejemplo, empieza antes del día siguiente al fin) el anterior no se cierra (RF-36, CA-24). El depósito
    del anterior no se traslada (E3). Devuelve (resultado del cierre, resultado del contrato nuevo)."""
    ahora = ahora or timezone.now()
    anterior = Contrato.objects.get(pk=contrato_id)
    cierre = finalizar_contrato(contrato_id, actor=actor, ip_origen=ip_origen, fecha_fin=fecha_fin, ahora=ahora)
    nuevo = crear_contrato(actor=actor, ip_origen=ip_origen, inquilino_id=inquilino_id, propiedad_id=anterior.propiedad_id,
                           datos=datos, ahora=ahora)
    return cierre, nuevo
