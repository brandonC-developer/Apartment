"""Mide, con un navegador real, qué hace el script de reducción (RF-50) con las fotografías de una carpeta.

No es una prueba automática: sirve para el criterio de salida de la E1 (peso de fotos reales de un iPhone y dos Android,
CA-73) y para la medición de metadatos (CA-82). Las fotografías son datos personales: se leen de la carpeta que se indique,
no se copian al repositorio y no se suben a ningún servidor; solo se imprimen cifras y los nombres de las etiquetas
de metadatos (no sus valores, salvo si hay o no ubicación GPS).

    cd src
    .venv\\Scripts\\python despliegue\\medir_reduccion.py CARPETA [--guardar CARPETA_DE_SALIDA]

Requiere Pillow, Selenium (requirements-pruebas.txt) y Chrome, Edge o Firefox. `--guardar` escribe cada resultado reducido
para poder abrirlo y compararlo a simple vista; bórrelo después, tiene los mismos datos personales que el original.
"""
import argparse
import base64
import functools
import http.server
import os
import shutil
import sys
import tempfile
import threading
from io import BytesIO
from pathlib import Path

from PIL import ExifTags, Image

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
os.environ.setdefault('SGA_DEBUG', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sga.settings')
import django  # noqa: E402

django.setup()
from inquilinos.tests_navegador import crear_navegador  # noqa: E402

SCRIPT = RAIZ / 'inquilinos' / 'static' / 'inquilinos' / 'reducir_fotografia.js'
EXTENSIONES = {'.jpg', '.jpeg', '.png', '.heic', '.heif', '.webp', '.avif', '.gif', '.bmp', '.tiff', '.tif'}
OBJETIVO = 2000000
LIMITE = 5 * 1024 * 1024
PAGINA = '<!doctype html><meta charset="utf-8"><input type="file" id="f"><script src="reducir_fotografia.js"></script>'

LLAMADA = """
const hecho = arguments[arguments.length - 1];
const archivo = document.getElementById('f').files[0];
window.SGA.fotografia.prepararEnvio(archivo).then(async (r) => {
  const bytes = new Uint8Array(await r.blob.arrayBuffer());
  let binario = '';
  for (let i = 0; i < bytes.length; i += 32768) { binario += String.fromCharCode.apply(null, bytes.subarray(i, i + 32768)); }
  hecho({ok: true, ancho: r.ancho, alto: r.alto, calidad: r.calidad, original: r.original, tipo: r.blob.type, base64: btoa(binario)});
}).catch((e) => hecho({ok: false, mensaje: String(e && e.message || e)}));
"""


def mib(n):
    return f'{n / 1048576:.2f} MiB'


def metadatos(imagen):
    """Nombres de etiquetas EXIF presentes (sin valores), si hay GPS, orientación y perfil de color."""
    exif = imagen.getexif()
    nombres = sorted(ExifTags.TAGS.get(k, str(k)) for k in exif.keys() if k not in (ExifTags.IFD.Exif, ExifTags.IFD.GPSInfo))
    return {
        'etiquetas': nombres,
        'gps': bool(exif.get_ifd(ExifTags.IFD.GPSInfo)),
        'orientacion': exif.get(ExifTags.Base.Orientation),
        'icc': bool(imagen.info.get('icc_profile')),
        'xmp': 'xmp' in imagen.info or 'XML:com.adobe.xmp' in imagen.info,
    }


def servir(carpeta):
    class Manejador(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k):
            pass

    manejador = functools.partial(Manejador, directory=str(carpeta))
    servidor = http.server.ThreadingHTTPServer(('127.0.0.1', 0), manejador)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor


def main():
    analizador = argparse.ArgumentParser()
    analizador.add_argument('carpeta')
    analizador.add_argument('--guardar')
    argumentos = analizador.parse_args()
    fotos = sorted(p for p in Path(argumentos.carpeta).iterdir() if p.suffix.lower() in EXTENSIONES)
    if not fotos:
        sys.exit('No hay imágenes en la carpeta.')
    navegador, motivos = crear_navegador()
    if navegador is None:
        sys.exit('Sin navegador: ' + '; '.join(motivos))
    with tempfile.TemporaryDirectory() as sitio:
        shutil.copy(SCRIPT, Path(sitio, 'reducir_fotografia.js'))
        Path(sitio, 'index.html').write_text(PAGINA, encoding='utf-8')
        servidor = servir(sitio)
        try:
            print(f'Navegador: {navegador.capabilities.get("browserName")} {navegador.capabilities.get("browserVersion")}')
            for foto in fotos:
                navegador.get(f'http://127.0.0.1:{servidor.server_port}/index.html')
                navegador.set_script_timeout(120)
                navegador.find_element('id', 'f').send_keys(str(foto.resolve()))
                original = foto.read_bytes()
                print(f'\n== {foto.name}')
                try:
                    with Image.open(BytesIO(original)) as imagen:
                        antes = metadatos(imagen)
                        print(f'  original: {imagen.format} {imagen.width}x{imagen.height} {imagen.mode}, {mib(len(original))}, '
                              f'GPS {"sí" if antes["gps"] else "no"}, orientación {antes["orientacion"]}, '
                              f'perfil ICC {"sí" if antes["icc"] else "no"}, XMP {"sí" if antes["xmp"] else "no"}')
                        print(f'  etiquetas EXIF: {", ".join(antes["etiquetas"]) or "(ninguna)"}')
                except Exception as error:
                    print(f'  Pillow no abre el original ({type(error).__name__}); es lo que verá el servidor.')
                resultado = navegador.execute_async_script(LLAMADA)
                if not resultado['ok']:
                    print(f'  el script avisa y no envía nada: {resultado["mensaje"]}')
                    continue
                datos = base64.b64decode(resultado['base64'])
                with Image.open(BytesIO(datos)) as imagen:
                    despues = metadatos(imagen)
                    cumple = 'cumple' if len(datos) <= OBJETIVO else 'NO cumple'
                    print(f'  enviado:  {"el original" if resultado["original"] else "reducido"} {imagen.format} '
                          f'{imagen.width}x{imagen.height}, {mib(len(datos))} ({cumple} el objetivo de 2 MB; '
                          f'{"dentro" if len(datos) <= LIMITE else "FUERA"} de 5 MiB), calidad {resultado["calidad"]}, '
                          f'{len(datos) * 100 / len(original):.0f} % del original')
                    print(f'            GPS {"sí" if despues["gps"] else "no"}, etiquetas EXIF {len(despues["etiquetas"])}, '
                          f'perfil ICC {"sí" if despues["icc"] else "no"}')
                if argumentos.guardar:
                    Path(argumentos.guardar).mkdir(parents=True, exist_ok=True)
                    Path(argumentos.guardar, foto.stem + '_reducida.jpg').write_bytes(datos)
        finally:
            servidor.shutdown()
            navegador.quit()


if __name__ == '__main__':
    main()
