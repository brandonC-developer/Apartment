"""Inicio de sesión en dos pasos (RF-26, RF-27, RNF-01, CA-47, CA-48, CA-68, CA-69).

Paso 1: usuario y contraseña. Si son correctos NO se inicia sesión: solo se anota en la sesión
que ese administrador pasó el primer paso, durante 5 minutos (plazo propuesto por el asistente).
Paso 2: código TOTP o código de recuperación. Solo entonces se llama a `login()`.
Si la cuenta aún no tiene segundo factor, el paso 2 es el registro (actualización 2026-10-24d):
primero el token que imprimen los comandos del servidor y después el código de la aplicación.
"""
import logging
import time

import pyotp
from cryptography.fernet import InvalidToken
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST

from . import autenticacion, cifrado
from .autenticacion import Resultado
from .middleware import marcar_inicio
from .models import Administrador

registro = logging.getLogger('sga.seguridad')

CLAVE_PENDIENTE = 'primer_paso_administrador'
CLAVE_PENDIENTE_HASTA = 'primer_paso_hasta'
CLAVE_SECRETO_REGISTRO = 'secreto_registro_cifrado'
CLAVE_TOKEN_VERIFICADO = 'token_registro_verificado'
VIGENCIA_PRIMER_PASO = 5 * 60
BACKEND = 'cuentas.backends.BackendAdministrador'

# Un mismo mensaje para usuario inexistente, contraseña incorrecta y cuenta en espera, para no
# revelar cuál de ellos ocurrió en el primer paso.
MENSAJE_PRIMER_PASO = 'Usuario o contraseña incorrectos, o la cuenta está en espera. Intente más tarde.'
MENSAJE_ESPERA = 'Demasiados intentos fallidos. Espere antes de intentar de nuevo.'


def _olvidar_primer_paso(request):
    """Descarta todo lo que depende del primer paso, incluido el secreto de registro propuesto."""
    for clave in (CLAVE_PENDIENTE, CLAVE_PENDIENTE_HASTA, CLAVE_SECRETO_REGISTRO, CLAVE_TOKEN_VERIFICADO):
        request.session.pop(clave, None)


def _administrador_pendiente(request):
    """El administrador que pasó el primer paso hace menos de 5 minutos, o None (y se limpia)."""
    pendiente = request.session.get(CLAVE_PENDIENTE)
    if pendiente is not None and time.time() <= request.session.get(CLAVE_PENDIENTE_HASTA, 0):
        administrador = Administrador.objects.filter(pk=pendiente).first()
        if administrador is not None:
            return administrador
    _olvidar_primer_paso(request)
    return None


def _avisar_cinco_fallos(respuesta):
    """Marca provisional del aviso de seguridad al quinto fallo seguido (CA-68). El aviso real
    (alerta en la web y auditoría en la E0, correo en la E4; HI-01, HI-05) depende de la auditoría,
    que aún no existe: por ahora solo queda en el registro del servidor, sin datos personales."""
    if respuesta.aviso_cinco_fallos:
        registro.warning('Cinco intentos fallidos seguidos en la cuenta administradora.')


def _mensaje_de_fallo(respuesta, texto):
    return MENSAJE_ESPERA if respuesta.resultado is Resultado.EN_ESPERA else texto


@require_http_methods(['GET', 'POST'])
def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('cuentas:inicio')
    error = None
    if request.method == 'POST':
        _olvidar_primer_paso(request)
        respuesta = autenticacion.comprobar_contrasena(
            request.POST.get('usuario', ''), request.POST.get('contrasena', ''))
        _avisar_cinco_fallos(respuesta)
        if respuesta.correcto:
            request.session[CLAVE_PENDIENTE] = respuesta.administrador.pk
            request.session[CLAVE_PENDIENTE_HASTA] = time.time() + VIGENCIA_PRIMER_PASO
            if respuesta.administrador.segundo_factor_activo:
                return redirect('cuentas:segundo_paso')
            return redirect('cuentas:registro_segundo_factor')
        error = MENSAJE_PRIMER_PASO
    return render(request, 'cuentas/iniciar_sesion.html', {'error': error})


@require_http_methods(['GET', 'POST'])
def segundo_paso(request):
    if request.user.is_authenticated:
        return redirect('cuentas:inicio')
    administrador = _administrador_pendiente(request)
    if administrador is None:
        return redirect('cuentas:iniciar_sesion')
    if not administrador.segundo_factor_activo:
        return redirect('cuentas:registro_segundo_factor')
    error = None
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '')
        normalizado = ''.join(codigo.split())
        if len(normalizado) == autenticacion.DIGITOS_TOTP and normalizado.isdigit():
            respuesta = autenticacion.verificar_totp(administrador.pk, normalizado)
        else:
            respuesta = autenticacion.verificar_codigo_recuperacion(administrador.pk, codigo)
        _avisar_cinco_fallos(respuesta)
        if respuesta.correcto:
            _olvidar_primer_paso(request)
            login(request, respuesta.administrador, backend=BACKEND)
            marcar_inicio(request)
            return redirect('cuentas:inicio')
        error = _mensaje_de_fallo(respuesta, 'Código incorrecto.')
    return render(request, 'cuentas/segundo_paso.html', {'error': error})


def _secreto_de_registro(request):
    """Secreto propuesto, guardado cifrado en la sesión. Si el guardado no se puede descifrar
    (cambió la clave o la sesión se corrompió) se descarta y se genera otro."""
    guardado = request.session.get(CLAVE_SECRETO_REGISTRO)
    if guardado:
        try:
            return cifrado.descifrar(guardado)
        except InvalidToken:
            pass
    secreto = pyotp.random_base32()
    request.session[CLAVE_SECRETO_REGISTRO] = cifrado.cifrar(secreto)
    return secreto


@never_cache
@require_http_methods(['GET', 'POST'])
def registro_segundo_factor(request):
    """Registro del segundo factor en el primer ingreso (RF-27). Solo para quien pasó el primer
    paso y aún no tiene segundo factor activo; el reemplazo con sesión iniciada es otra pantalla.
    Etapa 1: el token de registro del servidor. Etapa 2: la clave y el código de la aplicación."""
    if request.user.is_authenticated:
        return redirect('cuentas:inicio')
    administrador = _administrador_pendiente(request)
    if administrador is None:
        return redirect('cuentas:iniciar_sesion')
    if administrador.segundo_factor_activo:
        return redirect('cuentas:segundo_paso')
    if not request.session.get(CLAVE_TOKEN_VERIFICADO):
        return _pedir_token(request, administrador)

    secreto = _secreto_de_registro(request)
    error = None
    if request.method == 'POST':
        respuesta, codigos = autenticacion.activar_segundo_factor(
            administrador.pk, secreto, request.POST.get('codigo', ''),
            request.session[CLAVE_TOKEN_VERIFICADO])
        _avisar_cinco_fallos(respuesta)
        if respuesta.correcto:
            _olvidar_primer_paso(request)
            login(request, respuesta.administrador, backend=BACKEND)
            marcar_inicio(request)
            return render(request, 'cuentas/codigos_recuperacion.html', {'codigos': codigos})
        if respuesta.resultado is Resultado.TOKEN_INVALIDO:
            request.session.pop(CLAVE_TOKEN_VERIFICADO, None)
            return redirect('cuentas:registro_segundo_factor')
        error = _mensaje_de_fallo(respuesta, 'Código incorrecto.')
    uri = pyotp.TOTP(
        secreto, digits=autenticacion.DIGITOS_TOTP, interval=autenticacion.INTERVALO_TOTP,
    ).provisioning_uri(name=administrador.usuario, issuer_name='SGA')
    return render(request, 'cuentas/registro_segundo_factor.html', {
        'error': error, 'secreto': secreto, 'uri': uri})


def _pedir_token(request, administrador):
    error = None
    if request.method == 'POST':
        token = request.POST.get('token', '')
        respuesta = autenticacion.comprobar_token_registro(administrador.pk, token)
        _avisar_cinco_fallos(respuesta)
        if respuesta.correcto:
            request.session[CLAVE_TOKEN_VERIFICADO] = autenticacion.hash_token(token)
            return redirect('cuentas:registro_segundo_factor')
        error = _mensaje_de_fallo(respuesta, 'Token de registro incorrecto o vencido.')
    return render(request, 'cuentas/token_registro.html', {'error': error})


@require_POST
def cerrar_sesion(request):
    logout(request)
    return redirect('cuentas:iniciar_sesion')


@login_required
def inicio(request):
    """Página provisional protegida; las pantallas reales llegan en entregas posteriores."""
    return render(request, 'cuentas/inicio.html')
