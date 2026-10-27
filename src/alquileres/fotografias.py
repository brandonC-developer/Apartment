"""Fotografías del contrato y cédula desde el perfil de la propiedad (RF-51, RF-52, RF-02, RF-45; CA-75, CA-76,
CA-77, CA-82; DP-28, DP-29).

La fotografía del contrato es de la fila del contrato (no del inquilino ni de la propiedad): hasta 10 por contrato,
cada archivo en su propia petición, validado y reescrito por el servidor como la cédula (`inquilinos.imagenes`), en la
subcarpeta privada `contratos`. La cédula agregada desde el perfil de la propiedad se guarda en la ficha del inquilino
del contrato vigente y sigue exactamente las reglas de `inquilinos.services.subir_fotografia`.
"""
from django.db import transaction
from django.utils import timezone

from inquilinos import almacenamiento, services as servicios_de_inquilinos
from inquilinos.imagenes import ImagenInvalida, procesar_imagen
from inquilinos.services import ErrorDeValidacion
from nucleo import auditoria

from . import selectors, services
from .models import MAXIMO_DE_FOTOGRAFIAS_POR_CONTRATO, AccesoDocumentoContrato, DocumentoContrato, Propiedad

SUBCARPETA = almacenamiento.SUBCARPETA_DE_CONTRATOS


def subir_fotografia_del_contrato(contrato_id, *, contenido, actor, ip_origen=None, ahora=None):
    """Valida, limpia y guarda UNA fotografía del contrato (RF-52, CA-76). Un archivo rechazado no guarda nada y no
    toca las ya guardadas; la número 11 se rechaza con un mensaje. Bloquea la fila del contrato, así que dos subidas
    simultáneas no pasan de 10 (la base lo vuelve a comprobar, R22 y R28). Si la base falla, el archivo recién guardado
    se borra (HI-07). No crea ni modifica la cédula del inquilino."""
    ahora = ahora or timezone.now()
    try:
        imagen = procesar_imagen(contenido)
    except ImagenInvalida as error:
        raise ErrorDeValidacion({'archivo': [str(error)]})
    referencia = None
    try:
        with transaction.atomic():
            contrato = services._bloquear_contrato(contrato_id)
            existentes = DocumentoContrato.objects.filter(contrato=contrato).count()
            if existentes >= MAXIMO_DE_FOTOGRAFIAS_POR_CONTRATO:
                raise ErrorDeValidacion({'archivo': [
                    f'El contrato ya tiene {MAXIMO_DE_FOTOGRAFIAS_POR_CONTRATO} fotografías, que es el máximo.']})
            orden = existentes + 1  # no se borran: la numeración es 1..n sin huecos
            referencia = almacenamiento.guardar(imagen.contenido, imagen.extension, SUBCARPETA)
            documento = DocumentoContrato.objects.create(
                contrato=contrato, orden=orden, referencia_archivo=referencia, tipo_real_archivo=imagen.tipo,
                tamano_bytes=len(imagen.contenido))
            auditoria.registrar(
                'fotografia_contrato_subida', 'contrato', registro_id=contrato.pk, actor=actor, ip_origen=ip_origen,
                cambios={'orden': (None, orden), 'fotografia': (None, None)}, ahora=ahora)
    except BaseException:
        if referencia is not None:
            almacenamiento.borrar(referencia, SUBCARPETA)  # sin archivos huérfanos
        raise
    return documento


def registrar_acceso_al_contrato(documento, *, actor, accion, ahora=None):
    """Una consulta o descarga de la fotografía de un contrato (RF-52, CA-77): quién, cuándo y cuál, sin la imagen."""
    if accion not in (AccesoDocumentoContrato.CONSULTA, AccesoDocumentoContrato.DESCARGA):
        raise ValueError(accion)
    return AccesoDocumentoContrato.objects.create(
        documento=documento, actor=actor, accion=accion, ocurrido_en=ahora or timezone.now())


def subir_cedula_desde_la_propiedad(propiedad_id, *, cara, contenido, actor, ip_origen=None, ahora=None, hoy=None):
    """Agrega o reemplaza una cara de la cédula del inquilino del contrato vigente de la propiedad (RF-51, CA-75).
    La fotografía queda en la ficha del inquilino, con el consentimiento previo, la validación y la auditoría de
    siempre; sin contrato vigente (libre o solo con un contrato futuro) se rechaza con «No hay contrato vigente»."""
    ahora = ahora or timezone.now()
    propiedad = Propiedad.objects.get(pk=propiedad_id)
    contrato = selectors.contrato_vigente_de_la_propiedad(propiedad, hoy or selectors.hoy_local(ahora))
    if contrato is None:
        raise ErrorDeValidacion({'propiedad': [selectors.AVISO_SIN_CONTRATO_VIGENTE]})
    return servicios_de_inquilinos.subir_fotografia(
        contrato.inquilino_id, cara=cara, contenido=contenido, actor=actor, ip_origen=ip_origen, ahora=ahora)
