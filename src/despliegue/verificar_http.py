"""Recorrido real por HTTPS contra Nginx y Gunicorn (etapa A). Se ejecuta con el rol de la aplicación:

    runuser -u sga_app -- env $(grep -v "^#" /etc/sga/entorno | xargs) /opt/sga/venv/bin/python \
        /opt/sga/src/manage.py shell -c "exec(open('/opt/sga/src/despliegue/verificar_http.py').read())"

Crea una cuenta de prueba, registra su segundo factor, inicia sesión, consulta la auditoría y comprueba
cabeceras, IP de origen y registro de Nginx. El límite de solicitudes lo prueba `verificar.sh` aparte. `verificar.sh` borra después los datos.
"""
import http.cookiejar
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

import pyotp

from cuentas import autenticacion
from cuentas.models import Administrador
from nucleo.models import Auditoria

BASE = 'https://localhost'
CONTRASENA = 'una contrasena larga de prueba del despliegue'
SPOOF = '203.0.113.77'
fallos = []


def comprobar(condicion, texto):
    print(('OK     ' if condicion else 'FALLA  ') + texto)
    if not condicion:
        fallos.append(texto)


class SinRedireccion(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


jar = http.cookiejar.CookieJar()
contexto = ssl.create_default_context()
contexto.check_hostname = False
contexto.verify_mode = ssl.CERT_NONE
abridor = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(jar), urllib.request.HTTPSHandler(context=contexto), SinRedireccion())


def pedir(ruta, datos=None, cabeceras=None):
    cab = {'X-Forwarded-For': SPOOF, 'Referer': BASE + '/', 'Origin': BASE}  # el cliente intenta falsificar su IP
    cab.update(cabeceras or {})
    cuerpo = urllib.parse.urlencode(datos).encode() if datos is not None else None
    peticion = urllib.request.Request(BASE + ruta, data=cuerpo, headers=cab)
    try:
        r = abridor.open(peticion, timeout=20)
    except urllib.error.HTTPError as e:
        r = e
    return r.status, dict(r.headers), r.read().decode('utf-8', 'replace')


def csrf(html):
    return re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html).group(1)


def formulario(ruta, **campos):
    _, _, html = pedir(ruta)
    return pedir(ruta, {'csrfmiddlewaretoken': csrf(html), **campos})


# 0. Cabeceras de la página pública
estado, cab, html = pedir('/entrar/')
comprobar(estado == 200, 'GET /entrar/ responde 200 por HTTPS')
comprobar(re.fullmatch(r'nginx', cab.get('Server', '')) is not None, f"Server sin versión: {cab.get('Server')!r}")
comprobar('Content-Security-Policy-Report-Only' in cab, 'lleva la política de contenido como informe')
comprobar(cab.get('X-Content-Type-Options') == 'nosniff' and cab.get('X-Frame-Options') == 'DENY', 'nosniff y X-Frame-Options')
set_cookies = [h for h in (cab.get('Set-Cookie') or '').split(', ')]
cookies_csrf = [c for c in jar if c.name == 'csrftoken']
comprobar(bool(cookies_csrf) and cookies_csrf[0].secure, 'la cookie CSRF es Secure')

# 1. Cuenta de prueba con segundo factor por el flujo real
Administrador.objects.all().exists() and (print('FALLA  ya existe una cuenta; use una base limpia') or sys.exit(1))
admin = Administrador.objects.crear_administrador('admin_despliegue', CONTRASENA)
token = autenticacion.emitir_token_registro(admin)
estado, _, _ = formulario('/entrar/', usuario='admin_despliegue', contrasena=CONTRASENA)
comprobar(estado == 302, 'la contraseña lleva al segundo paso (302)')
formulario('/entrar/registro/', token=token)
_, _, html = pedir('/entrar/registro/')
secreto = re.search(r'<code>([A-Z2-7]{32})</code>', html).group(1)
estado, _, html = formulario('/entrar/registro/', codigo=pyotp.TOTP(secreto).now())
comprobar(estado == 200 and len(re.findall(r'<code>[A-Z2-9]{5}-[A-Z2-9]{5}</code>', html)) == 10, 'el registro entrega 10 códigos de recuperación')
sesion = [c for c in jar if c.name == 'sessionid']
comprobar(bool(sesion) and sesion[0].secure and sesion[0].has_nonstandard_attr('HttpOnly'), 'la cookie de sesión es Secure y HttpOnly')
estado, cab, html = pedir('/')
comprobar(estado == 200 and 'Sesión iniciada' in html, 'la página protegida abre con la sesión (Django detecta HTTPS detrás de Nginx)')
estado, _, html = pedir('/auditoria/?actor=BUSQUEDA-SECRETA-123')
comprobar(estado == 200, 'la pantalla de auditoría responde')

# 2. IP de origen: la falsificada por el cliente no debe llegar a la auditoría
ips = set(Auditoria.objects.exclude(ip_origen=None).values_list('ip_origen', flat=True))
comprobar(SPOOF not in ips and ips == {'127.0.0.1'}, f'la auditoría guarda la IP real y no la falsificada: {sorted(ips)}')

# 3. Cierre de sesión y acceso denegado
formulario_cierre = pedir('/')
_, _, html = pedir('/')
estado, _, _ = pedir('/salir/', {'csrfmiddlewaretoken': csrf(html)})
estado, _, _ = pedir('/')
comprobar(estado == 302, 'tras cerrar sesión, la página protegida redirige al inicio de sesión')

print()
print('RESULTADO:', 'sin fallos' if not fallos else f'{len(fallos)} fallo(s)')
sys.exit(1 if fallos else 0)
