"""Pantallas de los inquilinos: lista, registro, ficha, edición, desactivar/reactivar y revocar el consentimiento
(RF-01, RF-03, RF-04, RF-05, RF-39; CA-01, CA-25, CA-29, CA-67). Funcionales y accesibles, sin estilos: el diseño
espera a los wireframes (decisión 6 de la E1).

Las vistas solo leen la petición y llaman a `services` y `selectors` (ADR-030). Toda acción que cambia datos es
POST con token CSRF y exige sesión; las de riesgo (desactivar, reactivar, revocar) piden primero una confirmación.
"""
from datetime import datetime, time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.http import urlencode
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_http_methods

from nucleo import auditoria

from . import selectors, services
from .models import Consentimiento, Inquilino

POR_PAGINA = 50  # propuesta del asistente, como en la auditoría
CAMPOS = services.CAMPOS_EDITABLES


def _ip(request):
    return auditoria.ip_de_origen(request)


def _inquilino_o_404(inquilino_id):
    try:
        return selectors.obtener_ficha(inquilino_id)
    except Inquilino.DoesNotExist:
        raise Http404


def _datos(request):
    return {campo: request.POST.get(campo, '') for campo in CAMPOS}


@never_cache
@login_required
@require_GET
def lista(request):
    """Búsqueda por nombre, documento, teléfono o correo; filtro de estado y «Sin frente» (RF-03)."""
    busqueda = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', 'activos')
    if estado not in selectors.ESTADOS:
        estado = 'activos'
    sin_frente = request.GET.get('sin_frente') == '1'
    inquilinos = selectors.listar_inquilinos(busqueda=busqueda, estado=estado, sin_frente=sin_frente)
    pagina = Paginator(inquilinos, POR_PAGINA).get_page(request.GET.get('pagina'))
    filtros = {'q': busqueda, 'estado': estado, 'sin_frente': '1' if sin_frente else ''}
    return render(request, 'inquilinos/lista.html', {
        'pagina': pagina, 'filtros': filtros, 'consulta': urlencode({k: v for k, v in filtros.items() if v}),
        'estados': [('activos', 'Activos'), ('inactivos', 'Desactivados'), ('todos', 'Todos')]})


def _fecha_del_consentimiento(texto, ahora):
    """La fecha indicada, a mediodía hora local, sin pasar del instante actual. Vacía = ahora. Propuesta del
    asistente: la ficha pide solo la fecha porque un consentimiento en papel no trae la hora."""
    texto = (texto or '').strip()
    if not texto:
        return ahora, None
    try:
        dia = datetime.strptime(texto, '%Y-%m-%d').date()
    except ValueError:
        return ahora, 'La fecha del consentimiento no es válida.'
    if dia > timezone.localdate(ahora):
        return ahora, 'La fecha del consentimiento no puede ser futura.'
    momento = timezone.make_aware(datetime.combine(dia, time(12, 0)), timezone.get_current_timezone())
    return min(momento, ahora), None


@never_cache
@login_required
@require_http_methods(['GET', 'POST'])
def nuevo(request):
    """Registro con el texto informativo a la vista y el consentimiento obligatorio (RF-01, RF-39; CA-01)."""
    texto = selectors.texto_vigente()
    contexto = {'texto': texto, 'tipos': Inquilino.TIPOS_DE_DOCUMENTO, 'medios': Consentimiento.MEDIOS,
                'valores': {'medio': '', 'tipo_documento': Inquilino.CEDULA}, 'errores': {}, 'duplicados': []}
    if request.method == 'GET' or texto is None:
        return render(request, 'inquilinos/nuevo.html', contexto)
    ahora = timezone.now()
    valores = {**_datos(request), 'medio': request.POST.get('medio', ''),
               'otorgado_en': request.POST.get('otorgado_en', ''),
               'confirma': request.POST.get('confirma') == '1',
               'confirmar_duplicado': request.POST.get('confirmar_duplicado') == '1'}
    contexto['valores'] = valores
    otorgado_en, error_fecha = _fecha_del_consentimiento(valores['otorgado_en'], ahora)
    errores = {'otorgado_en': [error_fecha]} if error_fecha else {}
    if not valores['confirma']:
        errores['consentimiento'] = ['Confirme que se mostró el texto informativo y que la persona dio su consentimiento.']
    if not errores:
        try:
            inquilino = services.registrar_inquilino(
                actor=request.user.usuario, ip_origen=_ip(request), datos=_datos(request), texto=texto,
                medio=valores['medio'], otorgado_en=otorgado_en, confirmar_duplicado=valores['confirmar_duplicado'],
                ahora=ahora)
        except services.ErrorDeValidacion as error:
            errores = error.errores
        except services.DocumentoDuplicado as aviso:
            contexto['duplicados'] = aviso.duplicados
        else:
            messages.success(request, 'Inquilino registrado. Falta cargar las fotografías del documento.')
            return redirect('inquilinos:ficha', inquilino_id=inquilino.pk)
    contexto['errores'] = errores
    return render(request, 'inquilinos/nuevo.html', contexto, status=400 if errores else 200)


@never_cache
@login_required
@require_GET
def ficha(request, inquilino_id):
    return render(request, 'inquilinos/ficha.html', {'ficha': _inquilino_o_404(inquilino_id)})


@never_cache
@login_required
@require_http_methods(['GET', 'POST'])
def editar(request, inquilino_id):
    datos = _inquilino_o_404(inquilino_id)
    inquilino = datos['inquilino']
    contexto = {'ficha': datos, 'tipos': Inquilino.TIPOS_DE_DOCUMENTO, 'errores': {}, 'duplicados': [],
                'valores': {campo: getattr(inquilino, campo) or '' for campo in CAMPOS}}
    if inquilino.desasociado_en is not None:
        return render(request, 'inquilinos/editar.html', contexto, status=409)
    if request.method == 'POST':
        contexto['valores'] = {**_datos(request), 'confirmar_duplicado': request.POST.get('confirmar_duplicado') == '1'}
        try:
            services.actualizar_inquilino(
                inquilino_id, actor=request.user.usuario, ip_origen=_ip(request), datos=_datos(request),
                confirmar_duplicado=contexto['valores']['confirmar_duplicado'])
        except services.ErrorDeValidacion as error:
            contexto['errores'] = error.errores
            return render(request, 'inquilinos/editar.html', contexto, status=400)
        except services.DocumentoDuplicado as aviso:
            contexto['duplicados'] = aviso.duplicados
            return render(request, 'inquilinos/editar.html', contexto)
        messages.success(request, 'Datos guardados.')
        return redirect('inquilinos:ficha', inquilino_id=inquilino_id)
    return render(request, 'inquilinos/editar.html', contexto)


def _confirmar(request, inquilino_id, *, accion, titulo, aviso, boton, ejecutar, exito):
    """Pantalla de confirmación (GET) y ejecución (POST) de una acción de riesgo. Si el servicio avisa de un
    duplicado o de motivos de bloqueo, la pantalla los muestra; nada se cambia hasta confirmar."""
    datos = _inquilino_o_404(inquilino_id)
    contexto = {'ficha': datos, 'titulo': titulo, 'aviso': aviso, 'boton': boton, 'accion': accion,
                'errores': {}, 'duplicados': [], 'motivos': []}
    if request.method == 'POST':
        try:
            ejecutar(request, request.POST.get('confirmar_duplicado') == '1')
        except services.ErrorDeValidacion as error:
            contexto['errores'] = error.errores
            return render(request, 'inquilinos/confirmar.html', contexto, status=409)
        except services.DocumentoDuplicado as aviso_duplicado:
            contexto['duplicados'] = aviso_duplicado.duplicados
            return render(request, 'inquilinos/confirmar.html', contexto)
        except services.NoSePuedeDesactivar as bloqueo:
            contexto['motivos'] = bloqueo.motivos
            return render(request, 'inquilinos/confirmar.html', contexto, status=409)
        messages.success(request, exito)
        return redirect('inquilinos:ficha', inquilino_id=inquilino_id)
    return render(request, 'inquilinos/confirmar.html', contexto)


@never_cache
@login_required
@require_http_methods(['GET', 'POST'])
def desactivar(request, inquilino_id):
    return _confirmar(
        request, inquilino_id, accion='desactivar', titulo='Desactivar inquilino', boton='Desactivar',
        aviso='No se borra nada: la ficha, las fotografías y el historial se conservan. Se bloquea si tiene un contrato '
              'vigente o saldos pendientes.',
        ejecutar=lambda r, _: services.desactivar_inquilino(inquilino_id, actor=r.user.usuario, ip_origen=_ip(r)),
        exito='Inquilino desactivado.')


@never_cache
@login_required
@require_http_methods(['GET', 'POST'])
def reactivar(request, inquilino_id):
    return _confirmar(
        request, inquilino_id, accion='reactivar', titulo='Reactivar inquilino', boton='Reactivar',
        aviso='El inquilino vuelve a la lista de activos.',
        ejecutar=lambda r, confirmado: services.reactivar_inquilino(
            inquilino_id, actor=r.user.usuario, ip_origen=_ip(r), confirmar_duplicado=confirmado),
        exito='Inquilino reactivado.')


@never_cache
@login_required
@require_http_methods(['GET', 'POST'])
def revocar_consentimiento(request, inquilino_id):
    return _confirmar(
        request, inquilino_id, accion='revocar', titulo='Revocar el consentimiento', boton='Revocar el consentimiento',
        aviso='La revocación no borra ni cambia ningún dato ni fotografía y no tiene efecto retroactivo. Después no se '
              'podrán guardar fotografías ni crear contratos nuevos con este inquilino, y la ficha lo avisará.',
        ejecutar=lambda r, _: services.revocar_consentimiento(inquilino_id, actor=r.user.usuario, ip_origen=_ip(r)),
        exito='Consentimiento revocado. Los datos no se modificaron.')
