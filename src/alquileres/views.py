"""Vistas de las fotografías del contrato y de la cédula desde la propiedad (RF-51, RF-52, RF-45; CA-75, CA-76, CA-77).

Las subidas reciben UN archivo por petición (la usa el script de reducción del navegador, RF-50) y la entrega de la
imagen del contrato es la única vía para verla: sin sesión se niega y no hay URL pública del archivo (CA-77); cada
consulta o descarga queda registrada. Las páginas son mínimas, como las de la E1: el perfil completo es del grupo G.
"""
import logging

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from inquilinos import almacenamiento
from inquilinos.models import TAMANO_MAXIMO
from inquilinos.services import ErrorDeValidacion
from nucleo import auditoria

from . import fotografias, selectors
from .models import AccesoDocumentoContrato, Contrato, DocumentoContrato, Propiedad

registro = logging.getLogger('sga.documentos')
LADO_DE_PARTIDA_DEL_CONTRATO = 3508  # DP-29: punto de partida (RF-52); se confirma al medir con fotos reales


def _archivo_unico(request):
    """El contenido del único archivo del campo `archivo`, o una respuesta de error (RF-02, CA-74, CA-76)."""
    if sum(len(lista) for _, lista in request.FILES.lists()) != 1 or len(request.FILES.getlist('archivo')) != 1:
        return None, JsonResponse({'errores': {'archivo': ['Envíe un solo archivo por petición, en el campo «archivo».']}}, status=400)
    archivo = request.FILES['archivo']
    if archivo.size > TAMANO_MAXIMO:
        return None, JsonResponse({'errores': {'archivo': ['El archivo pesa más de 5 MiB.']}}, status=400)
    return archivo.read(TAMANO_MAXIMO + 1), None


@never_cache
@login_required
@require_GET
def pagina_fotografias_del_contrato(request, contrato_id):
    contrato = Contrato.objects.filter(pk=contrato_id).first()
    if contrato is None:
        raise Http404
    return render(request, 'alquileres/fotografias_contrato.html', {
        'contrato': contrato, 'lado_de_partida': LADO_DE_PARTIDA_DEL_CONTRATO,
        **selectors.fotografias_del_contrato(contrato)})


@login_required
@require_POST
def subir_fotografia_del_contrato(request, contrato_id):
    contenido, error = _archivo_unico(request)
    if error:
        return error
    try:
        documento = fotografias.subir_fotografia_del_contrato(
            contrato_id, contenido=contenido, actor=request.user.usuario, ip_origen=auditoria.ip_de_origen(request))
    except Contrato.DoesNotExist:
        raise Http404
    except ErrorDeValidacion as falla:
        return JsonResponse({'errores': falla.errores}, status=400)
    return JsonResponse({'id': documento.pk, 'orden': documento.orden, 'tipo': documento.tipo_real_archivo,
                         'tamano_bytes': documento.tamano_bytes}, status=201)


def _entregar(request, pk, accion):
    documento = DocumentoContrato.objects.filter(pk=pk).first()
    if documento is None:
        raise Http404
    try:
        archivo = almacenamiento.abrir(documento.referencia_archivo, fotografias.SUBCARPETA)
    except (FileNotFoundError, almacenamiento.ReferenciaInvalida):
        registro.error('Falta el archivo de la fotografía de un contrato (id %s).', documento.pk)
        raise Http404
    try:
        # Si el registro del acceso falla, no se entrega la imagen (RF-45).
        fotografias.registrar_acceso_al_contrato(documento, actor=request.user.usuario, accion=accion)
    except BaseException:
        archivo.close()
        raise
    extension = 'jpg' if documento.tipo_real_archivo == 'image/jpeg' else 'png'
    return FileResponse(
        archivo, content_type=documento.tipo_real_archivo, as_attachment=accion == AccesoDocumentoContrato.DESCARGA,
        filename=f'contrato-{documento.pk}.{extension}')  # el nombre no lleva datos personales


@never_cache
@login_required
@require_GET
def ver_fotografia_del_contrato(request, pk):
    return _entregar(request, pk, AccesoDocumentoContrato.CONSULTA)


@never_cache
@login_required
@require_GET
def descargar_fotografia_del_contrato(request, pk):
    return _entregar(request, pk, AccesoDocumentoContrato.DESCARGA)


@never_cache
@login_required
@require_GET
def pagina_cedula_de_la_propiedad(request, propiedad_id):
    propiedad = Propiedad.objects.filter(pk=propiedad_id).first()
    if propiedad is None:
        raise Http404
    return render(request, 'alquileres/cedula_propiedad.html', {
        'propiedad': propiedad, 'cedula': selectors.cedula_en_el_perfil(propiedad)})


@login_required
@require_POST
def subir_cedula_desde_la_propiedad(request, propiedad_id, cara):
    contenido, error = _archivo_unico(request)
    if error:
        return error
    try:
        documento = fotografias.subir_cedula_desde_la_propiedad(
            propiedad_id, cara=cara, contenido=contenido, actor=request.user.usuario,
            ip_origen=auditoria.ip_de_origen(request))
    except Propiedad.DoesNotExist:
        raise Http404
    except ErrorDeValidacion as falla:
        return JsonResponse({'errores': falla.errores}, status=400)
    return JsonResponse({'id': documento.pk, 'cara': documento.cara, 'tipo': documento.tipo_real_archivo,
                         'tamano_bytes': documento.tamano_bytes}, status=201)
