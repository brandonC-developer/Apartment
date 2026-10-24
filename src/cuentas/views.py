"""Inicio de sesión en dos pasos (RF-26, RF-27, RNF-01, CA-47, CA-48, CA-68, CA-69).

Paso 1: usuario y contraseña. Si son correctos NO se inicia sesión: solo se anota en la sesión
que ese administrador pasó el primer paso, durante 5 minutos (plazo propuesto por el asistente).
Paso 2: código TOTP o código de recuperación. Solo entonces se llama a `login()`.
"""
import time

import pyotp

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from . import autenticacion, cifrado
from .middleware import marcar_inicio
from .models import Administrador

CLAVE_PENDIENTE = 'primer_paso_administrador'
CLAVE_PENDIENTE_HASTA = 'primer_paso_hasta'
CLAVE_SECRETO_REGISTRO = 'secreto_registro_cifrado'
VIGENCIA_PRIMER_PASO = 5 * 60
BACKEND = 'cuentas.backends.BackendAdministrador'

# Un mismo mensaje para usuario inexistente, contraseña incorrecta y cuenta en espera, para no
# revelar cuál de ellos ocurrió en el primer paso.
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
        if respuesta.correcto:
            request.session[CLAVE_PENDIENTE] = administrador.pk
            request.session[CLAVE_PENDIENTE_HASTA] = time.time() + VIGENCIA_PRIMER_PASO
            if administrador.segundo_factor_activo:
                return redirect('cuentas:segundo_paso')
            return redirect('cuentas:registro_segundo_factor')
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
    if not Administrador.objects.filter(pk=pendiente, segundo_factor_activo=True).exists():
        return redirect('cuentas:registro_segundo_factor')
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


def _primer_paso_vigente(request):
    pendiente = request.session.get(CLAVE_PENDIENTE)
    if pendiente is None or time.time() > request.session.get(CLAVE_PENDIENTE_HASTA, 0):
        _olvidar_primer_paso(request)
        request.session.pop(CLAVE_SECRETO_REGISTRO, None)
        return None
    return pendiente


@require_http_methods(['GET', 'POST'])
def registro_segundo_factor(request):
    """Registro del segundo factor en el primer ingreso (RF-27). Solo para quien pasó el primer
    paso y aún no tiene segundo factor activo; el reemplazo con sesión iniciada es otra pantalla."""
    if request.user.is_authenticated:
        return redirect('cuentas:inicio')
    pendiente = _primer_paso_vigente(request)
    if pendiente is None:
        return redirect('cuentas:iniciar_sesion')
    administrador = Administrador.objects.get(pk=pendiente)
    if administrador.segundo_factor_activo:
        return redirect('cuentas:segundo_paso')
    cifrado_secreto = request.session.get(CLAVE_SECRETO_REGISTRO)
    secreto = cifrado.descifrar(cifrado_secreto) if cifrado_secreto else pyotp.random_base32()
    if not cifrado_secreto:
        # El secreto propuesto queda en la sesión (en la base) cifrado, no en claro.
        request.session[CLAVE_SECRETO_REGISTRO] = cifrado.cifrar(secreto)
    error = None
    if request.method == 'POST':
        respuesta, codigos = autenticacion.activar_segundo_factor(
            pendiente, secreto, request.POST.get('codigo', ''))
        if respuesta.correcto:
            _olvidar_primer_paso(request)
            request.session.pop(CLAVE_SECRETO_REGISTRO, None)
            login(request, respuesta.administrador, backend=BACKEND)
            marcar_inicio(request)
            return render(request, 'cuentas/codigos_recuperacion.html', {'codigos': codigos})
        if respuesta.resultado is autenticacion.Resultado.EN_ESPERA:
            error = 'Demasiados intentos fallidos. Espere antes de intentar de nuevo.'
        else:
            error = 'Código incorrecto.'
    uri = pyotp.TOTP(
        secreto, digits=autenticacion.DIGITOS_TOTP, interval=autenticacion.INTERVALO_TOTP,
    ).provisioning_uri(name=administrador.usuario, issuer_name='SGA')
    return render(request, 'cuentas/registro_segundo_factor.html', {
        'error': error, 'secreto': secreto, 'uri': uri})


@require_POST
def cerrar_sesion(request):
    logout(request)
    return redirect('cuentas:iniciar_sesion')


@login_required
def inicio(request):
    """Página provisional protegida; las pantallas reales llegan en entregas posteriores."""
    return render(request, 'cuentas/inicio.html')
