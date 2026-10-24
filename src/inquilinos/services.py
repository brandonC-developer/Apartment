"""Escritura de inquilinos: registrar, actualizar, desactivar y reactivar (RF-01, RF-03, RF-04, RF-39).

Cada operación va en una transacción con su registro de auditoría (RF-28): de los campos personales
solo consta que cambiaron, nunca su valor (R14, CA-53). Los servicios no leen la sesión ni la petición:
reciben el actor y la IP. Las lecturas están en `selectors.py` (ADR-030).
"""
import re

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import transaction
from django.utils import timezone

from nucleo import auditoria

from . import bloqueos
from .models import Consentimiento, Inquilino, TextoConsentimiento

CAMPOS_EDITABLES = ('nombre_completo', 'tipo_documento', 'numero_documento', 'telefono', 'correo')
_TELEFONO = re.compile(r'^[0-9+().\- ]{6,40}$')


class ErrorDeValidacion(Exception):
    """Los datos no son válidos; `errores` es {campo: [mensajes]} (RF-02)."""

    def __init__(self, errores):
        super().__init__(errores)
        self.errores = errores


class DocumentoDuplicado(Exception):
    """Ya existe otro inquilino activo con el mismo tipo y número de documento (RF-01, CA-25).
    Es una advertencia: no se guarda hasta que quien llama confirme."""

    def __init__(self, duplicados):
        super().__init__('Documento duplicado')
        self.duplicados = list(duplicados)


class NoSePuedeDesactivar(Exception):
    """Algún motivo impide desactivar al inquilino (RF-04, CA-29)."""

    def __init__(self, motivos):
        super().__init__('No se puede desactivar')
        self.motivos = list(motivos)


def _limpiar(valor):
    valor = (valor or '').strip()
    return valor or None


def validar_datos(datos, *, parciales=False):
    """Normaliza y valida los campos de un inquilino; devuelve los valores limpios o lanza
    `ErrorDeValidacion`. Con `parciales` solo valida las claves presentes (actualización)."""
    errores, limpios = {}, {}

    def requerido(campo, maximo, mensaje):
        if parciales and campo not in datos:
            return
        valor = _limpiar(datos.get(campo))
        if valor is None:
            errores[campo] = [mensaje]
        elif len(valor) > maximo:
            errores[campo] = [f'No puede pasar de {maximo} caracteres.']
        else:
            limpios[campo] = valor

    requerido('nombre_completo', 200, 'El nombre completo es obligatorio.')
    requerido('numero_documento', 60, 'El número de documento es obligatorio.')
    if not parciales or 'tipo_documento' in datos:
        tipo = _limpiar(datos.get('tipo_documento'))
        if tipo not in {t for t, _ in Inquilino.TIPOS_DE_DOCUMENTO}:
            errores['tipo_documento'] = ['Elija cédula, DIMEX, pasaporte u otro.']
        else:
            limpios['tipo_documento'] = tipo
    if not parciales or 'telefono' in datos:
        telefono = _limpiar(datos.get('telefono'))
        if telefono is not None and (not _TELEFONO.match(telefono) or sum(c.isdigit() for c in telefono) < 6):
            errores['telefono'] = ['El teléfono debe tener al menos 6 dígitos y solo dígitos, espacios, + - ( ) o punto.']
        else:
            limpios['telefono'] = telefono
    if not parciales or 'correo' in datos:
        correo = _limpiar(datos.get('correo'))
        if correo is not None:
            try:
                if len(correo) > 254:
                    raise ValidationError('largo')
                EmailValidator()(correo)
            except ValidationError:
                errores['correo'] = ['El correo no es una dirección válida.']
        if 'correo' not in errores:
            limpios['correo'] = correo
    if errores:
        raise ErrorDeValidacion(errores)
    return limpios


def buscar_duplicados(tipo_documento, numero_documento, *, excluir_id=None):
    """Los inquilinos activos con el mismo tipo y número de documento (RF-01, CA-25)."""
    if not numero_documento:
        return Inquilino.objects.none()
    encontrados = Inquilino.objects.filter(
        tipo_documento=tipo_documento, numero_documento=numero_documento.strip(), activo=True)
    return encontrados.exclude(pk=excluir_id) if excluir_id else encontrados


def _cambios_de_creacion(limpios):
    return {campo: (None, valor) for campo, valor in limpios.items() if valor is not None}


@transaction.atomic
def registrar_inquilino(*, actor, ip_origen=None, datos, texto, medio, otorgado_en=None,
                        confirmar_duplicado=False, ahora=None):
    """Guarda al inquilino con su consentimiento, sin fotografías todavía (RF-01, CA-01).

    El consentimiento es obligatorio (RF-39): se pasa la versión del texto mostrada y el medio. Si hay un
    inquilino activo con el mismo documento, lanza `DocumentoDuplicado` sin guardar, salvo que se confirme.
    """
    ahora = ahora or timezone.now()
    otorgado_en = otorgado_en or ahora
    limpios = validar_datos(datos)
    errores = {}
    if not isinstance(texto, TextoConsentimiento):
        errores['consentimiento'] = ['Falta el consentimiento: debe mostrarse el texto informativo y registrarse.']
    elif medio not in (Consentimiento.FISICO, Consentimiento.ELECTRONICO):
        errores['medio'] = ['Indique si el consentimiento fue físico o electrónico.']
    elif otorgado_en > ahora:
        errores['otorgado_en'] = ['La fecha del consentimiento no puede ser futura.']
    if errores:
        raise ErrorDeValidacion(errores)
    duplicados = buscar_duplicados(limpios['tipo_documento'], limpios['numero_documento'])
    if duplicados.exists() and not confirmar_duplicado:
        raise DocumentoDuplicado(duplicados)

    inquilino = Inquilino.objects.create(**limpios)
    Consentimiento.objects.create(inquilino=inquilino, texto=texto, medio=medio, otorgado_en=otorgado_en)
    cambios = _cambios_de_creacion(limpios)
    cambios['activo'] = (None, True)
    auditoria.registrar(
        'inquilino_registrado', 'inquilino', registro_id=inquilino.pk, actor=actor, ip_origen=ip_origen,
        cambios=cambios, ahora=ahora)
    auditoria.registrar(
        'consentimiento_otorgado', 'inquilino', registro_id=inquilino.pk, actor=actor, ip_origen=ip_origen,
        cambios={'texto_version': (None, texto.version), 'medio': (None, medio)}, ahora=ahora)
    return inquilino


def _bloquear(inquilino_id):
    inquilino = Inquilino.objects.select_for_update().get(pk=inquilino_id)
    if inquilino.desasociado_en is not None:
        raise ErrorDeValidacion({'inquilino': ['El inquilino ya fue desasociado: no se puede modificar.']})
    return inquilino


@transaction.atomic
def actualizar_inquilino(inquilino_id, *, actor, ip_origen=None, datos, confirmar_duplicado=False, ahora=None):
    """Cambia los campos indicados de la ficha (RF-03). Solo los que cambian se guardan y se auditan."""
    ahora = ahora or timezone.now()
    desconocidos = set(datos) - set(CAMPOS_EDITABLES)
    if desconocidos:
        raise ValueError(f'Campos no editables: {sorted(desconocidos)}')
    inquilino = _bloquear(inquilino_id)
    limpios = validar_datos(datos, parciales=True)
    cambios = {c: (getattr(inquilino, c), v) for c, v in limpios.items() if getattr(inquilino, c) != v}
    if not cambios:
        return inquilino
    if 'tipo_documento' in cambios or 'numero_documento' in cambios:
        tipo = limpios.get('tipo_documento', inquilino.tipo_documento)
        numero = limpios.get('numero_documento', inquilino.numero_documento)
        duplicados = buscar_duplicados(tipo, numero, excluir_id=inquilino.pk)
        if inquilino.activo and duplicados.exists() and not confirmar_duplicado:
            raise DocumentoDuplicado(duplicados)
    for campo, (_, nuevo) in cambios.items():
        setattr(inquilino, campo, nuevo)
    inquilino.save(update_fields=[*cambios, 'actualizado_en'])
    auditoria.registrar(
        'inquilino_actualizado', 'inquilino', registro_id=inquilino.pk, actor=actor, ip_origen=ip_origen,
        cambios=cambios, ahora=ahora)
    return inquilino


@transaction.atomic
def desactivar_inquilino(inquilino_id, *, actor, ip_origen=None, ahora=None):
    """Desactiva sin borrar nada (RF-04). Se bloquea si alguna comprobación registrada da un motivo (CA-29)."""
    ahora = ahora or timezone.now()
    inquilino = _bloquear(inquilino_id)
    if not inquilino.activo:
        raise ErrorDeValidacion({'inquilino': ['El inquilino ya está desactivado.']})
    motivos = bloqueos.motivos_de_bloqueo(inquilino)
    if motivos:
        raise NoSePuedeDesactivar(motivos)
    inquilino.activo = False
    inquilino.save(update_fields=['activo', 'actualizado_en'])
    auditoria.registrar(
        'inquilino_desactivado', 'inquilino', registro_id=inquilino.pk, actor=actor, ip_origen=ip_origen,
        cambios={'activo': (True, False)}, ahora=ahora)
    return inquilino


@transaction.atomic
def reactivar_inquilino(inquilino_id, *, actor, ip_origen=None, confirmar_duplicado=False, ahora=None):
    """Vuelve a activar a un inquilino desactivado (RF-04). Si otro activo usa ahora su documento, avisa."""
    ahora = ahora or timezone.now()
    inquilino = _bloquear(inquilino_id)
    if inquilino.activo:
        raise ErrorDeValidacion({'inquilino': ['El inquilino ya está activo.']})
    duplicados = buscar_duplicados(inquilino.tipo_documento, inquilino.numero_documento, excluir_id=inquilino.pk)
    if duplicados.exists() and not confirmar_duplicado:
        raise DocumentoDuplicado(duplicados)
    inquilino.activo = True
    inquilino.save(update_fields=['activo', 'actualizado_en'])
    auditoria.registrar(
        'inquilino_reactivado', 'inquilino', registro_id=inquilino.pk, actor=actor, ip_origen=ip_origen,
        cambios={'activo': (False, True)}, ahora=ahora)
    return inquilino
