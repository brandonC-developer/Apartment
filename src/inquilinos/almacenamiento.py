"""Almacenamiento privado de las fotografías (RNF-03, RNF-14, ADR-003): fuera de la raíz web, con nombre
aleatorio (UUID) y permisos mínimos; la base guarda solo la referencia. Nunca hay una URL pública: los archivos
solo salen por la vista autorizada (`views.ver_documento`)."""
import os
import re
import uuid
from pathlib import Path

from django.conf import settings

SUBCARPETA = 'cedulas'
_REFERENCIA = re.compile(r'^[0-9a-f]{32}\.(jpg|png)$')


class ReferenciaInvalida(Exception):
    pass


def _raiz():
    return Path(settings.RAIZ_DOCUMENTOS) / SUBCARPETA


def _ruta(referencia):
    """Ruta absoluta de una referencia, solo si tiene la forma que generamos nosotros (sin barras, sin `..`)."""
    if not isinstance(referencia, str) or not _REFERENCIA.match(referencia):
        raise ReferenciaInvalida(referencia)
    return _raiz() / referencia


def guardar(contenido, extension):
    """Escribe el archivo con un nombre aleatorio y devuelve su referencia. Se crea con `O_EXCL` (no pisa nada) y
    permisos 0640; la carpeta, 0750. En el servidor la carpeta de documentos tiene el bit setgid para que el grupo
    del respaldo pueda leerlos."""
    if extension not in ('jpg', 'png'):
        raise ReferenciaInvalida(extension)
    carpeta = _raiz()
    carpeta.mkdir(mode=0o750, parents=True, exist_ok=True)
    referencia = f'{uuid.uuid4().hex}.{extension}'
    descriptor = os.open(_ruta(referencia), os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_BINARY', 0), 0o640)
    try:
        with os.fdopen(descriptor, 'wb') as archivo:
            archivo.write(contenido)
            archivo.flush()
            os.fsync(archivo.fileno())
    except BaseException:
        borrar(referencia)
        raise
    return referencia


def abrir(referencia):
    """Abre el archivo para leerlo; `FileNotFoundError` si no está."""
    return open(_ruta(referencia), 'rb')


def existe(referencia):
    try:
        return _ruta(referencia).is_file()
    except ReferenciaInvalida:
        return False


def borrar(referencia):
    """Borra el archivo si existe; devuelve si lo borró. Nunca lanza por un archivo que ya no está."""
    try:
        _ruta(referencia).unlink()
        return True
    except (FileNotFoundError, ReferenciaInvalida):
        return False
