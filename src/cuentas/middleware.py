"""Límites de la sesión (RF-27, CA-48): cierre total a las 24 horas y por inactividad de 1 hora."""
import time

from django.contrib.auth import logout

DURACION_MAXIMA = 24 * 60 * 60
INACTIVIDAD_MAXIMA = 60 * 60
CLAVE_INICIO = 'sesion_inicio'
CLAVE_ULTIMA = 'sesion_ultima'


def marcar_inicio(request):
    ahora = time.time()
    request.session[CLAVE_INICIO] = ahora
    request.session[CLAVE_ULTIMA] = ahora


class LimiteDeSesion:
    """Debe ir después de AuthenticationMiddleware. Una sesión autenticada sin marcas de tiempo
    se cierra: no se asume que sea válida."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            ahora = time.time()
            inicio = request.session.get(CLAVE_INICIO)
            ultima = request.session.get(CLAVE_ULTIMA)
            if (inicio is None or ultima is None
                    or ahora - inicio > DURACION_MAXIMA or ahora - ultima > INACTIVIDAD_MAXIMA):
                logout(request)
            else:
                request.session[CLAVE_ULTIMA] = ahora
        return self.get_response(request)
