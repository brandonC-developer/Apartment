"""Inicio de sesión en dos pasos (RF-26, RF-27, RNF-01, CA-47, CA-48, CA-68, CA-69).

Paso 1: usuario y contraseña. Si son correctos NO se inicia sesión: solo se anota en la sesión
que ese administrador pasó el primer paso, durante 5 minutos (plazo propuesto por el asistente).
Paso 2: código TOTP o código de recuperación. Solo entonces se llama a `login()`.
"""
import time

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from . import autenticacion
from .middleware import marcar_inicio
from .models import Administrador

CLAVE_PENDIENTE = 'primer_paso_administrador'
CLAVE_PENDIENTE_HASTA = 'primer_paso_hasta'
VIGENCIA_PRIMER_PASO = 5 * 60
BACKEND = 'cuentas.backends.BackendAdministrador'

# Un mismo mensaje para usuario inexistente, contraseña incorrecta, cuenta en espera y segundo
# factor sin activar, para no revelar cuál de ellos ocurrió en el primer paso.
MENSAJE_PRIMER_PASO = 'Usuario o contraseña incorrectos, o la cuenta está en espera. Intente más tarde.'


def _olvidar_primer_paso(request):
    request.session.pop(CLAVE_PENDIENTE, None)
    request.session.pop(CLAVE_PENDIENTE_HASTA, None)


@require_http_methods(['GET', 'POST'])
def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('cuentas:inicio')
    error = None
    if request.method == 'POST':
        _olvidar_primer_paso(request)
        respuesta = autenticacion.comprobar_contrasena(
            request.POST.get('usuario', ''), request.POST.get('contrasena', ''))
        administrador = respuesta.administrador
        if respuesta.correcto and administrador.segundo_factor_activo:
            request.session[CLAVE_PENDIENTE] = administrador.pk
            request.session[CLAVE_PENDIENTE_HASTA] = time.time() + VIGENCIA_PRIMER_PASO
            return redirect('cuentas:segundo_paso')
        error = MENSAJE_PRIMER_PASO
    return render(request, 'cuentas/iniciar_sesion.html', {'error': error})


@require_http_methods(['GET', 'POST'])
def segundo_paso(request):
    if request.user.is_authenticated:
        return redirect('cuentas:inicio')
    pendiente = request.session.get(CLAVE_PENDIENTE)
    hasta = request.session.get(CLAVE_PENDIENTE_HASTA, 0)
    if pendiente is None or time.time() > hasta:
        _olvidar_primer_paso(request)
        return redirect('cuentas:iniciar_sesion')
    error = None
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '')
        normalizado = ''.join(codigo.split())
        if len(normalizado) == autenticacion.DIGITOS_TOTP and normalizado.isdigit():
            respuesta = autenticacion.verificar_totp(pendiente, normalizado)
        else:
            respuesta = autenticacion.verificar_codigo_recuperacion(pendiente, codigo)
        if respuesta.correcto:
            _olvidar_primer_paso(request)
            login(request, Administrador.objects.get(pk=pendiente), backend=BACKEND)
            marcar_inicio(request)
            return redirect('cuentas:inicio')
        if respuesta.resultado is autenticacion.Resultado.EN_ESPERA:
            error = 'Demasiados intentos fallidos. Espere antes de intentar de nuevo.'
        else:
            error = 'Código incorrecto.'
    return render(request, 'cuentas/segundo_paso.html', {'error': error})


@require_POST
def cerrar_sesion(request):
    logout(request)
    return redirect('cuentas:iniciar_sesion')


@login_required
def inicio(request):
    """Página provisional protegida; las pantallas reales llegan en entregas posteriores."""
    return render(request, 'cuentas/inicio.html')
