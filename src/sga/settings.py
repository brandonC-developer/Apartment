"""
Configuración del Sistema de Gestión de Alquileres (SGA).

Esqueleto de la entrega E0 (DOC/fase-5-implementacion). Cada valor remite al requisito
o a la decisión que lo origina. Lo marcado «propuesta» no lo ha decidido el solicitante.
Los secretos nunca van en este archivo ni en el repositorio (ADR-032, decisión 6).
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def leer_secreto(nombre, por_defecto=None):
    """Lee un secreto de la variable de entorno SGA_<NOMBRE> o del archivo /etc/sga/<nombre>
    (ADR-032, decisión 6: archivo 0640 fuera del repositorio). Propuesta: el orden y la ruta."""
    valor = os.environ.get(f'SGA_{nombre.upper()}')
    if valor:
        return valor
    ruta = Path(os.environ.get('SGA_DIRECTORIO_SECRETOS', '/etc/sga')) / nombre.lower()
    try:
        return ruta.read_text(encoding='utf-8').strip()
    except OSError:
        return por_defecto


DEBUG = os.environ.get('SGA_DEBUG', '') == '1'

SECRET_KEY = leer_secreto('SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        # Solo para desarrollo local y pruebas; nunca en un servidor.
        SECRET_KEY = 'solo-desarrollo-no-usar-en-servidor'
    else:
        raise RuntimeError(
            'Falta SECRET_KEY: defina SGA_SECRET_KEY o el archivo /etc/sga/secret_key.'
        )

ALLOWED_HOSTS = [h for h in os.environ.get('SGA_ALLOWED_HOSTS', '').split(',') if h]

# Nombres con los que se atiende al sitio, separados por comas (`check --deploy` exige que no esté
# vacío). Con SGA_DEBUG=1 y sin valor, Django admite localhost.
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('SGA_HOSTS_PERMITIDOS', '').split(',') if h.strip()]

INSTALLED_APPS = [
    # Sin django.contrib.admin: la interfaz es propia (propuesta; reduce la superficie expuesta).
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Aplicaciones del DAS (ADR-030): nucleo y cuentas (E0), inquilinos (E1).
    'nucleo',
    'cuentas',
    'inquilinos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cuentas.middleware.LimiteDeSesion',
    'nucleo.middleware.ZonaHorariaDeLaOrganizacion',
    'nucleo.middleware.PoliticaDeContenido',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sga.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sga.wsgi.application'

# PostgreSQL 18 (ADR-002). En el servidor: socket Unix y autenticación `peer`, sin contraseña
# (ADR-027, ADR-032 decisión 12). Fuera de WSL o del servidor se puede indicar otro servidor
# con SGA_BD_HOST (por ejemplo, para la integración continua).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('SGA_BD_NOMBRE', 'sga'),
        'USER': os.environ.get('SGA_BD_USUARIO', ''),
        'PASSWORD': leer_secreto('bd_contrasena', ''),
        'HOST': os.environ.get('SGA_BD_HOST', '/var/run/postgresql'),
        'PORT': os.environ.get('SGA_BD_PUERTO', ''),
        # ADR-029: una conexión por petición; ajustar al medir en el servidor real.
        'CONN_MAX_AGE': 0,
    }
}

# Documentos privados (cédulas, fotografías de contratos): una carpeta FUERA de la raíz web y del
# código, sin URL pública; solo se sirven por una vista con sesión (RNF-03, RNF-14, ADR-003). La usan
# las entregas E1 y E2; el respaldo y Gunicorn ya la conocen (despliegue/, respaldo/).
RAIZ_DOCUMENTOS = Path(os.environ.get('SGA_DOCUMENTOS', '/var/lib/sga/documentos'))

# Hash de los códigos de recuperación: Argon2id con sal por código (NIST SP 800-63B: un secreto de menos
# de 112 bits se guarda con sal y un esquema de hash de contraseñas). Parámetros mínimos de OWASP
# (19 MiB, 2 iteraciones, 1 hilo). Solo en las pruebas se usan parámetros baratos para no tardar.
CODIGOS_ARGON2 = (
    {'time_cost': 1, 'memory_cost': 1024, 'parallelism': 1} if 'test' in sys.argv
    else {'time_cost': 2, 'memory_cost': 19456, 'parallelism': 1}
)

# Roles de PostgreSQL (ADR-027): dueño (solo migraciones), aplicación y respaldos. Los nombres son
# propuesta del asistente; no son secretos. Ver db/roles.sql y `manage.py aplicar_privilegios`.
ROLES_BD = {
    'dueno': os.environ.get('SGA_ROL_DUENO', 'sga_dueno'),
    'app': os.environ.get('SGA_ROL_APP', 'sga_app'),
    'respaldos': os.environ.get('SGA_ROL_RESPALDOS', 'sga_respaldos'),
}

# Contraseñas: Argon2id (ADR-019) y mínimo de 15 caracteres sin reglas de composición (RF-26).
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 15}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
]

LANGUAGE_CODE = 'es-cr'
# La zona horaria de la organización es configurable (RF-33); este es solo el valor por
# defecto de Django. Las marcas de registro se guardan en UTC (ADR-005).
TIME_ZONE = 'America/Costa_Rica'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sesión: máximo 24 h (CA-48). El cierre por 1 h de inactividad (CA-48) aún no está implementado.
SESSION_COOKIE_AGE = 24 * 60 * 60
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Cabecera con la IP del cliente que pone Nginx: `proxy_set_header X-Forwarded-For $remote_addr;`
# SUSTITUYE la del cliente (ADR-032, decisión 13); sin ella se usa REMOTE_ADDR (desarrollo). Gunicorn
# solo es alcanzable por el socket de Nginx.
IP_ORIGEN_CABECERA = None if DEBUG else 'HTTP_X_FORWARDED_FOR'

if not DEBUG:
    # Nginx termina HTTPS y envía X-Forwarded-Proto (ADR-032, decisión 13).
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # HSTS por etapas (ADR-032, decisión 5): se activa en la etapa B con un max-age corto.
    SECURE_HSTS_SECONDS = 0
    SECURE_CONTENT_TYPE_NOSNIFF = True

# Cuenta administradora (RF-26, RF-27, RN-25): modelo propio sobre AbstractBaseUser, sin
# permisos de Django (decisión del solicitante, 23-oct-2026, actualización zz).
AUTH_USER_MODEL = 'cuentas.Administrador'
AUTHENTICATION_BACKENDS = ['cuentas.backends.BackendAdministrador']
LOGIN_URL = 'cuentas:iniciar_sesion'

# Claves de Fernet para cifrar el secreto del segundo factor (actualización zzb). Lista separada
# por comas: se cifra con la primera y se descifra con cualquiera (MultiFernet) para rotar.
CLAVES_CIFRADO = [c.strip() for c in (leer_secreto('clave_cifrado', '') or '').split(',') if c.strip()]
