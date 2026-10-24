"""Servicio de auditoría (RF-28, RNF-06, CA-53, CA-71).

Regla R14: la auditoría no guarda valores de campos personales ni secretos. Quien llama pasa un
diccionario `cambios` {campo: (antes, después)}; de los campos personales y de los secretos solo
se conserva el nombre, nunca el valor.
"""
import ipaddress

from django.conf import settings
from django.utils import timezone

from .models import Auditoria

# RF-28: nombre, número de documento, teléfono, correo e imagen de cédula.
CAMPOS_PERSONALES = frozenset({
    'nombre_completo', 'numero_documento', 'tipo_documento', 'telefono', 'correo', 'correo_electronico',
    'imagen_cedula', 'fotografia', 'archivo',
    # Identidad y direcciones del responsable (ORGANIZACION): también datos personales.
    'nombre_responsable', 'direccion_responsable', 'correo_admin', 'correo_aviso_secundario',
    'telefono_whatsapp_admin',
})
# Nunca se guardan sus valores: contraseñas, códigos, tokens y secretos.
CAMPOS_SECRETOS = frozenset({
    'password', 'contrasena', 'secreto', 'secreto_segundo_factor', 'codigo', 'token', 'hash_codigo',
    'token_registro_hash',
})
SIN_VALOR = CAMPOS_PERSONALES | CAMPOS_SECRETOS

# Eventos de seguridad de la cuenta que la pantalla de inicio destaca (CA-68, CA-69, CA-70, HI-01).
EVENTOS_DE_SEGURIDAD = (
    'cinco_fallos_seguidos', 'codigo_recuperacion_usado', 'codigos_emitidos',
    'segundo_factor_registrado', 'segundo_factor_rescatado',
)
ACCIONES_DE_AUTENTICACION = (
    'inicio_sesion', 'inicio_sesion_fallido', 'cierre_sesion', 'cuenta_creada',
) + EVENTOS_DE_SEGURIDAD


def registrar(accion, entidad, *, registro_id=None, actor, tipo_actor=Auditoria.TIPO_ADMINISTRADOR,
              ejecucion_id=None, ip_origen=None, cambios=None, ahora=None):
    """Inserta un registro de auditoría y lo devuelve."""
    campos, anteriores, nuevos = [], {}, {}
    for campo, (antes, despues) in (cambios or {}).items():
        campos.append(campo)
        if campo not in SIN_VALOR:
            anteriores[campo] = antes
            nuevos[campo] = despues
    return Auditoria.objects.create(
        accion=accion, entidad=entidad, registro_id=registro_id, actor=actor, tipo_actor=tipo_actor,
        ejecucion_id=ejecucion_id, ip_origen=ip_origen or None, ocurrido_en=ahora or timezone.now(),
        campos_modificados=campos, valor_anterior=anteriores or None, valor_nuevo=nuevos or None,
    )


def ip_de_origen(request):
    """Dirección IP del cliente. Detrás de Nginx, Gunicorn solo ve el socket Unix: Nginx debe
    enviar `X-Forwarded-For $remote_addr` sustituyendo la del cliente (el cliente no puede
    falsificarla porque Gunicorn solo es alcanzable por ese socket; ADR-032, decisión 13). `IP_ORIGEN_CABECERA` indica la
    cabecera de confianza; sin ella se usa `REMOTE_ADDR`. Un valor que no sea una IP se descarta."""
    cabecera = getattr(settings, 'IP_ORIGEN_CABECERA', None)
    valor = request.META.get(cabecera, '') if cabecera else request.META.get('REMOTE_ADDR', '')
    try:
        return str(ipaddress.ip_address(valor.strip()))
    except ValueError:
        return None


def eventos_de_seguridad_desde_el_inicio_anterior():
    """Alerta web de los avisos de seguridad (HI-01): los eventos posteriores al inicio de sesión
    anterior al actual, o todos si no hay uno anterior. No necesita otro estado que la auditoría;
    la ventana es propuesta del asistente."""
    inicios = list(Auditoria.objects.filter(accion='inicio_sesion').values_list('ocurrido_en', flat=True)[:2])
    return eventos_de_seguridad_desde(inicios[1] if len(inicios) == 2 else None)


def eventos_de_seguridad_desde(instante):
    """Eventos de seguridad de la cuenta posteriores a `instante` (o todos si es None)."""
    eventos = Auditoria.objects.filter(accion__in=EVENTOS_DE_SEGURIDAD)
    if instante is not None:
        eventos = eventos.filter(ocurrido_en__gt=instante)
    return eventos
