"""Vistas de las fotografías del documento (RF-01, RF-02, RF-45; CA-11, CA-26, CA-74).

Las pantallas de la lista y la ficha son del grupo F; aquí están la subida de UN archivo por petición (la usa el
script de reducción del navegador, RF-50) y la entrega de la imagen, que es la única vía para verla: sin sesión se
niega y no hay URL pública del archivo (CA-11); cada consulta o descarga queda registrada (CA-26).
"""
import logging

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from . import almacenamiento, selectors, services
from .models import TAMANO_MAXIMO, AccesoDocumento, DocumentoIdentidad, Inquilino

registro = logging.getLogger('sga.documentos')


@never_cache
@login_required
@require_GET
def pagina_fotografias(request, inquilino_id):
    """Página mínima para subir el frente y el reverso con el script de reducción (RF-50). La ficha completa y los
    textos definitivos son del grupo F; esta página solo existe para que la subida tenga dónde ocurrir."""
    try:
        ficha = selectors.obtener_ficha(inquilino_id)
    except Inquilino.DoesNotExist:
        raise Http404
    return render(request, 'inquilinos/fotografias.html', {
        'ficha': ficha, 'caras': [('frente', 'Frente', ficha['frente']), ('reverso', 'Reverso', ficha['reverso'])]})


def _ip(request):
    from nucleo import auditoria
    return auditoria.ip_de_origen(request)


@login_required
@require_POST
def subir_fotografia(request, inquilino_id, cara):
    """Recibe UNA fotografía en el campo `archivo` (RF-02, CA-74). Un archivo rechazado no descarta el otro ya
    aceptado: cada cara va en su propia petición."""
    if sum(len(lista) for _, lista in request.FILES.lists()) != 1 or len(request.FILES.getlist('archivo')) != 1:
        return JsonResponse({'errores': {'archivo': ['Envíe un solo archivo por petición, en el campo «archivo».']}}, status=400)
    archivo = request.FILES['archivo']
    if archivo.size > TAMANO_MAXIMO:
        return JsonResponse({'errores': {'archivo': ['El archivo pesa más de 5 MiB.']}}, status=400)
    contenido = archivo.read(TAMANO_MAXIMO + 1)
    try:
        documento = services.subir_fotografia(
            inquilino_id, cara=cara, contenido=contenido, actor=request.user.usuario, ip_origen=_ip(request))
    except Inquilino.DoesNotExist:
        raise Http404
    except services.ErrorDeValidacion as error:
        return JsonResponse({'errores': error.errores}, status=400)
    return JsonResponse({
        'id': documento.pk, 'cara': documento.cara, 'tipo': documento.tipo_real_archivo,
        'tamano_bytes': documento.tamano_bytes}, status=201)


def _entregar(request, pk, accion):
    documento = DocumentoIdentidad.objects.filter(pk=pk, eliminado_en__isnull=True).first()
    if documento is None:
        raise Http404
    try:
        archivo = almacenamiento.abrir(documento.referencia_archivo)
    except (FileNotFoundError, almacenamiento.ReferenciaInvalida):
        registro.error('Falta el archivo de un documento (id %s).', documento.pk)
        raise Http404
    try:
        # Si el registro del acceso falla, no se entrega la imagen (RF-45).
        services.registrar_acceso(documento, actor=request.user.usuario, accion=accion)
    except BaseException:
        archivo.close()
        raise
    descarga = accion == AccesoDocumento.DESCARGA
    extension = 'jpg' if documento.tipo_real_archivo == 'image/jpeg' else 'png'
    return FileResponse(
        archivo, content_type=documento.tipo_real_archivo, as_attachment=descarga,
        filename=f'documento-{documento.pk}.{extension}')  # el nombre no lleva datos personales


@never_cache
@login_required
@require_GET
def ver_documento(request, pk):
    return _entregar(request, pk, AccesoDocumento.CONSULTA)


@never_cache
@login_required
@require_GET
def descargar_documento(request, pk):
    return _entregar(request, pk, AccesoDocumento.DESCARGA)
