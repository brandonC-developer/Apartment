"""Activa la zona horaria de la organización en cada petición (RF-33, RNF-12): las fechas y horas
se presentan en esa zona; los instantes siguen guardándose en UTC (RNF-17)."""
from zoneinfo import ZoneInfo

from django.conf import settings
from django.utils import timezone

from .models import Organizacion


class ZonaHorariaDeLaOrganizacion:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        zona = Organizacion.objects.values_list('zona_horaria', flat=True).first()
        try:
            timezone.activate(ZoneInfo(zona or settings.TIME_ZONE))
        except (KeyError, ValueError, OSError):
            timezone.activate(ZoneInfo(settings.TIME_ZONE))
        try:
            return self.get_response(request)
        finally:
            timezone.deactivate()


# ADR-032, decisión 16: política fija y estricta, sin scripts ni estilos en línea. En la etapa A se
# envía solo como informe (Report-Only); pasa a obligatoria cuando no haya violaciones.
POLITICA_DE_CONTENIDO = (
    "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' blob:; "
    "connect-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'; object-src 'none'"
)


class PoliticaDeContenido:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        respuesta = self.get_response(request)
        respuesta.headers.setdefault('Content-Security-Policy-Report-Only', POLITICA_DE_CONTENIDO)
        return respuesta
