"""Reglas de autenticación de la cuenta administradora (RF-27, CA-68, CA-69).

Las cifras (5 fallos, espera de 1 minuto que se duplica hasta 1 hora, intervalo de 30 s y
tolerancia de un intervalo) son las de la ERS v1.16, propuestas del asistente y aceptadas por
el solicitante. Que un intento hecho durante la espera no sume otro fallo es propuesta del
asistente.
"""
import hashlib
import hmac
import secrets
from datetime import timedelta
from enum import Enum

import pyotp
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from cryptography.fernet import InvalidToken
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone

from .models import Administrador, CodigoRecuperacion

UMBRAL_FALLOS = 5
ESPERA_BASE_SEGUNDOS = 60
ESPERA_MAXIMA_SEGUNDOS = 3600
INTERVALO_TOTP = 30
DIGITOS_TOTP = 6


class Resultado(Enum):
    CORRECTO = 'correcto'
    INCORRECTO = 'incorrecto'
    EN_ESPERA = 'en_espera'
    TOKEN_INVALIDO = 'token_invalido'


class Respuesta:
    """Resultado de un intento. `aviso_cinco_fallos` es verdadero solo en el quinto fallo
    seguido: quien llama debe enviar el aviso de seguridad (CA-68)."""

    def __init__(self, resultado, administrador=None, aviso_cinco_fallos=False, espera_hasta=None,
                 secreto_ilegible=False):
        self.secreto_ilegible = secreto_ilegible
        self.resultado = resultado
        self.administrador = administrador
        self.aviso_cinco_fallos = aviso_cinco_fallos
        self.espera_hasta = espera_hasta

    @property
    def correcto(self):
        return self.resultado is Resultado.CORRECTO


def segundos_de_espera(fallos):
    if fallos < UMBRAL_FALLOS:
        return 0
    return min(ESPERA_BASE_SEGUNDOS * 2 ** (fallos - UMBRAL_FALLOS), ESPERA_MAXIMA_SEGUNDOS)


def _en_espera(administrador, ahora):
    return administrador.espera_hasta is not None and ahora < administrador.espera_hasta


def _registrar_fallo(administrador, ahora):
    administrador.fallos_consecutivos += 1
    espera = segundos_de_espera(administrador.fallos_consecutivos)
    administrador.espera_hasta = ahora + timedelta(seconds=espera) if espera else None
    administrador.save(update_fields=['fallos_consecutivos', 'espera_hasta', 'actualizado_en'])
    return Respuesta(
        Resultado.INCORRECTO,
        aviso_cinco_fallos=administrador.fallos_consecutivos == UMBRAL_FALLOS,
        espera_hasta=administrador.espera_hasta,
    )


def comprobar_contrasena(usuario, contrasena, ahora=None):
    """Primer paso. Una contraseña correcta NO reinicia el contador: solo lo reinicia el
    segundo factor correcto, porque el contador se comparte entre los dos pasos."""
    ahora = ahora or timezone.now()
    with transaction.atomic():
        administrador = Administrador.objects.select_for_update().filter(usuario=usuario).first()
        if administrador is None:
            make_password(contrasena)  # tiempo parecido al de una cuenta real
            return Respuesta(Resultado.INCORRECTO)
        if _en_espera(administrador, ahora):
            return Respuesta(Resultado.EN_ESPERA, espera_hasta=administrador.espera_hasta)
        if administrador.check_password(contrasena):
            return Respuesta(Resultado.CORRECTO, administrador=administrador)
        return _registrar_fallo(administrador, ahora)


def _intervalo_aceptado(secreto, codigo, ahora):
    """Intervalo del código si coincide con el actual o con uno anterior o posterior; si no, None."""
    totp = pyotp.TOTP(secreto, digits=DIGITOS_TOTP, interval=INTERVALO_TOTP)
    actual = int(ahora.timestamp()) // INTERVALO_TOTP
    codigo = ''.join((codigo or '').split())  # '123 456', como lo muestran las aplicaciones
    aceptado = None
    for intervalo in (actual - 1, actual, actual + 1):
        esperado = totp.at(intervalo * INTERVALO_TOTP)
        if hmac.compare_digest(esperado, codigo):
            aceptado = intervalo
    return aceptado


def verificar_totp(administrador_id, codigo, ahora=None):
    """Segundo paso. Acepta el intervalo actual y uno anterior o posterior (CA-69) y rechaza un
    intervalo no posterior al último aceptado, para que un código no se reutilice. Si es
    correcto reinicia el contador de fallos."""
    ahora = ahora or timezone.now()
    with transaction.atomic():
        administrador = Administrador.objects.select_for_update().get(pk=administrador_id)
        if _en_espera(administrador, ahora):
            return Respuesta(Resultado.EN_ESPERA, espera_hasta=administrador.espera_hasta)
        if not administrador.secreto_segundo_factor:
            return _registrar_fallo(administrador, ahora)
        try:
            secreto = administrador.secreto_segundo_factor_en_claro()
        except InvalidToken:
            # La clave de cifrado cambió o se perdió (decisión del solicitante, 24-oct-2026): el
            # secreto guardado no se puede leer. Cuenta como fallo y la persona entra con un código
            # de recuperación y se resuelve con `rescatar_segundo_factor`.
            respuesta = _registrar_fallo(administrador, ahora)
            respuesta.secreto_ilegible = True
            return respuesta
        aceptado = _intervalo_aceptado(secreto, codigo, ahora)
        ultimo = administrador.ultimo_intervalo_totp
        if aceptado is None or (ultimo is not None and aceptado <= ultimo):
            return _registrar_fallo(administrador, ahora)
        administrador.ultimo_intervalo_totp = aceptado
        administrador.fallos_consecutivos = 0
        administrador.espera_hasta = None
        administrador.save(update_fields=[
            'ultimo_intervalo_totp', 'fallos_consecutivos', 'espera_hasta', 'actualizado_en',
        ])
        return Respuesta(Resultado.CORRECTO, administrador=administrador)


# Códigos de recuperación (RF-27, CA-69). 10 por emisión (ERS). El formato —10 caracteres de un
# alfabeto sin caracteres confusos, unos 49 bits— y el hash SHA-256 son propuestas del asistente.
CODIGOS_POR_EMISION = 10
LONGITUD_CODIGO = 10
ALFABETO_CODIGO = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'


def _normalizar_codigo(codigo):
    return ''.join((codigo or '').upper().split()).replace('-', '')


def _hasher():
    return PasswordHasher(**settings.CODIGOS_ARGON2)


def _hash_codigo(codigo):
    """Argon2id con sal propia por código (decisión del solicitante, 24-oct-2026; NIST SP 800-63B:
    un secreto de menos de 112 bits va con sal y un esquema de hash de contraseñas). El hash lleva
    sus parámetros y su sal, por eso no se puede buscar por él: se verifica contra cada código."""
    return _hasher().hash(_normalizar_codigo(codigo))


def _coincide(hash_guardado, codigo):
    try:
        return _hasher().verify(hash_guardado, _normalizar_codigo(codigo))
    except (VerifyMismatchError, InvalidHashError):
        return False


def codigo_disponible(administrador, codigo):
    """¿Hay un código sin usar que coincida? (para pruebas y comprobaciones, sin consumirlo)"""
    return any(
        _coincide(h, codigo) for h in CodigoRecuperacion.objects.filter(
            administrador=administrador, usado_en__isnull=True).values_list('hash_codigo', flat=True))


def emitir_codigos_recuperacion(administrador, contrasena):
    """Emite 10 códigos nuevos e invalida los anteriores. Exige la contraseña actual (CA-69).
    Devuelve la lista en claro (única vez que existen) o None si la contraseña no es correcta.
    Quien llama debe enviar el aviso de seguridad."""
    if not administrador.check_password(contrasena):
        return None
    return _generar_codigos(administrador)


def _generar_codigos(administrador):
    codigos = [
        ''.join(secrets.choice(ALFABETO_CODIGO) for _ in range(LONGITUD_CODIGO))
        for _ in range(CODIGOS_POR_EMISION)
    ]
    with transaction.atomic():
        CodigoRecuperacion.objects.filter(administrador=administrador).delete()
        CodigoRecuperacion.objects.bulk_create([
            CodigoRecuperacion(administrador=administrador, hash_codigo=_hash_codigo(c))
            for c in codigos
        ])
    return [f'{c[:5]}-{c[5:]}' for c in codigos]


def verificar_codigo_recuperacion(administrador_id, codigo, ahora=None):
    """Sustituye al TOTP en el segundo paso. Comparte el contador de fallos; uno correcto
    se marca como usado y reinicia el contador."""
    ahora = ahora or timezone.now()
    with transaction.atomic():
        administrador = Administrador.objects.select_for_update().get(pk=administrador_id)
        if _en_espera(administrador, ahora):
            return Respuesta(Resultado.EN_ESPERA, espera_hasta=administrador.espera_hasta)
        # Se verifican todos los códigos sin usar, sin cortar en el primero que coincide, para que el
        # tiempo no revele cuál era (hay a lo sumo 10).
        disponible = None
        for candidato in CodigoRecuperacion.objects.select_for_update().filter(
                administrador=administrador, usado_en__isnull=True):
            if _coincide(candidato.hash_codigo, codigo) and disponible is None:
                disponible = candidato
        if disponible is None:
            return _registrar_fallo(administrador, ahora)
        disponible.usado_en = ahora
        disponible.save(update_fields=['usado_en'])
        administrador.fallos_consecutivos = 0
        administrador.espera_hasta = None
        administrador.save(update_fields=['fallos_consecutivos', 'espera_hasta', 'actualizado_en'])
        return Respuesta(Resultado.CORRECTO, administrador=administrador)


# Token de registro del segundo factor (propuesta del asistente, actualización 2026-10-24d): sin él,
# quien conozca solo la contraseña podría registrar su propio segundo factor mientras la cuenta no
# tenga uno. Lo imprimen los comandos de creación y de rescate; se guarda solo su hash.
VIGENCIA_TOKEN_REGISTRO = timedelta(hours=24)


def hash_token(token):
    return hashlib.sha256(''.join((token or '').split()).encode('utf-8')).hexdigest()


def emitir_token_registro(administrador, ahora=None):
    """Genera un token de un solo uso, lo guarda con hash y lo devuelve en claro (única vez)."""
    ahora = ahora or timezone.now()
    token = secrets.token_urlsafe(16)
    administrador.token_registro_hash = hash_token(token)
    administrador.token_registro_vence = ahora + VIGENCIA_TOKEN_REGISTRO
    administrador.save(update_fields=['token_registro_hash', 'token_registro_vence', 'actualizado_en'])
    return token


def _token_vigente(administrador, hash_recibido, ahora):
    return bool(
        administrador.token_registro_hash
        and administrador.token_registro_vence is not None
        and ahora <= administrador.token_registro_vence
        and hmac.compare_digest(hash_recibido, administrador.token_registro_hash)
    )


def comprobar_token_registro(administrador_id, token, ahora=None):
    """Prueba de que quien registra el segundo factor tiene acceso al servidor. Un token
    incorrecto suma al contador compartido; uno correcto no lo reinicia (solo lo hace un
    segundo factor correcto)."""
    ahora = ahora or timezone.now()
    with transaction.atomic():
        administrador = Administrador.objects.select_for_update().get(pk=administrador_id)
        if administrador.segundo_factor_activo:
            return Respuesta(Resultado.INCORRECTO)
        if _en_espera(administrador, ahora):
            return Respuesta(Resultado.EN_ESPERA, espera_hasta=administrador.espera_hasta)
        if not _token_vigente(administrador, hash_token(token), ahora):
            return _registrar_fallo(administrador, ahora)
        return Respuesta(Resultado.CORRECTO, administrador=administrador)


def activar_segundo_factor(administrador_id, secreto, codigo, hash_del_token, ahora=None):
    """Registro del segundo factor en el primer ingreso (RF-27). Exige el token de registro
    (se vuelve a comprobar aquí, bajo bloqueo, y se consume). Comprueba el código contra el
    `secreto` propuesto con las mismas reglas y el mismo contador de intentos que el inicio de
    sesión; si es correcto lo guarda cifrado, lo activa y emite los 10 códigos de recuperación.
    Nunca reemplaza un segundo factor ya activo (eso exige la sesión y la contraseña). Devuelve
    (Respuesta, códigos en claro o None)."""
    ahora = ahora or timezone.now()
    with transaction.atomic():
        administrador = Administrador.objects.select_for_update().get(pk=administrador_id)
        if administrador.segundo_factor_activo:
            return Respuesta(Resultado.INCORRECTO), None
        if _en_espera(administrador, ahora):
            return Respuesta(Resultado.EN_ESPERA, espera_hasta=administrador.espera_hasta), None
        if not _token_vigente(administrador, hash_del_token or '', ahora):
            return Respuesta(Resultado.TOKEN_INVALIDO), None
        aceptado = _intervalo_aceptado(secreto, codigo, ahora)
        if aceptado is None:
            return _registrar_fallo(administrador, ahora), None
        administrador.fijar_secreto_segundo_factor(secreto)
        administrador.segundo_factor_activo = True
        administrador.ultimo_intervalo_totp = aceptado
        administrador.fallos_consecutivos = 0
        administrador.espera_hasta = None
        administrador.token_registro_hash = ''
        administrador.token_registro_vence = None
        administrador.save()
        codigos = _generar_codigos(administrador)
        return Respuesta(Resultado.CORRECTO, administrador=administrador), codigos
