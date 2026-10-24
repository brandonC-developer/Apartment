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
from django.utils import timezone

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

# 2b. Fotografías del documento (E1, grupo D): subida, almacenamiento privado, entrega autorizada y su registro
import grp
import os
import pwd
import random
import uuid
from io import BytesIO

from PIL import Image

from inquilinos import services as servicios_inquilinos
from inquilinos.models import AccesoDocumento, DocumentoIdentidad, TextoConsentimiento

texto_consentimiento = TextoConsentimiento.objects.create(
    version=1, contenido='Texto de la verificación', vigente_desde=timezone.now())
inquilino = servicios_inquilinos.registrar_inquilino(
    actor='admin_despliegue', datos={'nombre_completo': 'Persona de Prueba', 'tipo_documento': 'cedula',
                                     'numero_documento': '9-9999-9999'}, texto=texto_consentimiento, medio='fisico')


def jpeg(ancho=200, alto=150, ruido=False, gps=False):
    imagen = Image.new('RGB', (ancho, alto))
    if ruido:
        generador = random.Random(1)
        imagen.putdata([(generador.randrange(256), generador.randrange(256), generador.randrange(256))
                        for _ in range(ancho * alto)])
    exif = Image.Exif()
    if gps:
        exif[0x8825] = {1: 'N', 2: (9.0, 56.0, 12.0), 3: 'W', 4: (84.0, 4.0, 5.0)}
        exif[0x010F] = 'MarcaDeLaCamara'
    salida = BytesIO()
    imagen.save(salida, 'JPEG', exif=exif, quality=95)
    return salida.getvalue()


def subir(cara, contenido, ruta=None):
    frontera = uuid.uuid4().hex
    salto = chr(13) + chr(10)
    cabecera = salto.join([f'--{frontera}', 'Content-Disposition: form-data; name="archivo"; filename="f.jpg"',
                           'Content-Type: image/jpeg', '', ''])
    cuerpo = cabecera.encode() + contenido + (salto + f'--{frontera}--' + salto).encode()
    token = [c.value for c in jar if c.name == 'csrftoken'][0]
    peticion = urllib.request.Request(
        BASE + (ruta or f'/inquilinos/{inquilino.pk}/fotografias/{cara}/'), data=cuerpo, method='POST',
        headers={'Content-Type': f'multipart/form-data; boundary={frontera}', 'X-CSRFToken': token,
                 'Referer': BASE + '/', 'Origin': BASE})
    try:
        respuesta = abridor.open(peticion, timeout=60)
    except urllib.error.HTTPError as e:
        respuesta = e
    return respuesta.status, respuesta.read().decode('utf-8', 'replace')


original = jpeg(gps=True)
estado, cuerpo = subir('frente', original)
comprobar(estado == 201, f'la subida de la cédula responde 201 ({estado})')
documento = DocumentoIdentidad.objects.get(inquilino=inquilino, cara='frente', eliminado_en__isnull=True)
ruta_archivo = os.path.join('/var/lib/sga/documentos/cedulas', documento.referencia_archivo)
datos_guardados = open(ruta_archivo, 'rb').read()
comprobar(b'MarcaDeLaCamara' not in datos_guardados and b'Exif' not in datos_guardados, 'el archivo guardado no conserva los metadatos')
info = os.stat(ruta_archivo)
comprobar(oct(info.st_mode & 0o777) == '0o640', f'el archivo es 0640 ({oct(info.st_mode & 0o777)})')
comprobar(pwd.getpwuid(info.st_uid).pw_name == 'sga_app' and grp.getgrgid(info.st_gid).gr_name == 'sga_respaldos',
          'el archivo es de sga_app y del grupo del respaldo (setgid)')
estado, _, _ = pedir(f'/inquilinos/documentos/{documento.pk}/ver/')
comprobar(estado == 200, 'con sesión se entrega la cédula')
abierto = urllib.request.Request(BASE + f'/inquilinos/documentos/{documento.pk}/ver/', headers={'Referer': BASE + '/'})
respuesta = abridor.open(abierto, timeout=30)
comprobar(respuesta.read() == datos_guardados and respuesta.headers['Cache-Control'].startswith('max-age=0')
          or 'no-store' in respuesta.headers['Cache-Control'], 'la imagen entregada es la guardada y no se guarda en caché')
sin_sesion = urllib.request.build_opener(urllib.request.HTTPSHandler(context=contexto), SinRedireccion())
try:
    sin_sesion.open(BASE + f'/inquilinos/documentos/{documento.pk}/ver/', timeout=30)
    estado_anonimo = 200
except urllib.error.HTTPError as e:
    estado_anonimo = e.code
comprobar(estado_anonimo == 302, f'sin sesión se niega (CA-11): {estado_anonimo}')
comprobar(AccesoDocumento.objects.count() == 2, f'cada consulta quedó registrada (CA-26): {AccesoDocumento.objects.count()} accesos')
estado, _ = subir('reverso', jpeg(1500, 1500, ruido=True))
comprobar(estado == 201, f'Nginx admite un cuerpo de más de 1 MiB en la ruta de subida ({estado})')
estado, _ = subir('reverso', os.urandom(7 * 1024 * 1024))
comprobar(estado == 413, f'Nginx rechaza más de 6 MiB incluso en la ruta de subida ({estado})')
estado, _ = subir('reverso', os.urandom(2 * 1024 * 1024), ruta='/entrar/')
comprobar(estado == 413, f'Nginx rechaza más de 1 MiB en el resto de las rutas ({estado})')

# 3. Cierre de sesión y acceso denegado
formulario_cierre = pedir('/')
_, _, html = pedir('/')
estado, _, _ = pedir('/salir/', {'csrfmiddlewaretoken': csrf(html)})
estado, _, _ = pedir('/')
comprobar(estado == 302, 'tras cerrar sesión, la página protegida redirige al inicio de sesión')

print()
print('RESULTADO:', 'sin fallos' if not fallos else f'{len(fallos)} fallo(s)')
sys.exit(1 if fallos else 0)
