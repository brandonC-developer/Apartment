"""Consulta de la auditoría (RF-28, CA-71): pantalla de solo lectura, con filtros por fecha, tipo de
evento, entidad y actor. Consultarla no genera un registro nuevo (decisión del solicitante)."""
from datetime import date, datetime, time, timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone
from django.utils.http import urlencode
from django.views.decorators.http import require_GET

from .models import Auditoria

POR_PAGINA = 50  # propuesta del asistente


def _fecha(texto):
    try:
        return date.fromisoformat(texto)
    except ValueError:
        return None


@login_required
@require_GET
def consultar_auditoria(request):
    filtros = {
        'desde': request.GET.get('desde', '').strip(),
        'hasta': request.GET.get('hasta', '').strip(),
        'accion': request.GET.get('accion', '').strip(),
        'entidad': request.GET.get('entidad', '').strip(),
        'actor': request.GET.get('actor', '').strip(),
    }
    registros = Auditoria.objects.all()
    zona = timezone.get_current_timezone()
    desde, hasta = _fecha(filtros['desde']), _fecha(filtros['hasta'])
    if desde:
        registros = registros.filter(ocurrido_en__gte=datetime.combine(desde, time.min, zona))
    if hasta:
        registros = registros.filter(ocurrido_en__lt=datetime.combine(hasta + timedelta(days=1), time.min, zona))
    if filtros['accion']:
        registros = registros.filter(accion=filtros['accion'])
    if filtros['entidad']:
        registros = registros.filter(entidad=filtros['entidad'])
    if filtros['actor']:
        registros = registros.filter(actor=filtros['actor'])
    pagina = Paginator(registros, POR_PAGINA).get_page(request.GET.get('pagina'))
    consulta = urlencode({k: v for k, v in filtros.items() if v})
    return render(request, 'nucleo/auditoria.html', {
        'pagina': pagina, 'filtros': filtros, 'consulta': consulta,
        'acciones': Auditoria.objects.order_by().values_list('accion', flat=True).distinct(),
    })
