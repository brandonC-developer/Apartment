"""Almacenamiento privado de las fotografías (RNF-03, RNF-14, ADR-003): fuera de la raíz web, con nombre
aleatorio (UUID) y permisos mínimos; la base guarda solo la referencia. Nunca hay una URL pública: los archivos
solo salen por la vista autorizada (`views.ver_documento`)."""
import os
import re
import uuid
from pathlib import Path

from django.conf import settings

SUBCARPETA = 'cedulas'
SUBCARPETA_DE_CONTRATOS = 'contratos'  # fotografías del contrato (RF-52); las usa `alquileres`
_SUBCARPETAS = (SUBCARPETA, SUBCARPETA_DE_CONTRATOS)
_REFERENCIA = re.compile(r'^[0-9a-f]{32}\.(jpg|png)$')


class ReferenciaInvalida(Exception):
    pass


def _raiz(subcarpeta=SUBCARPETA):
    if subcarpeta not in _SUBCARPETAS:
        raise ReferenciaInvalida(subcarpeta)
    return Path(settings.RAIZ_DOCUMENTOS) / subcarpeta


def _ruta(referencia, subcarpeta=SUBCARPETA):
    """Ruta absoluta de una referencia, solo si tiene la forma que generamos nosotros (sin barras, sin `..`)."""
    if not isinstance(referencia, str) or not _REFERENCIA.match(referencia):
        raise ReferenciaInvalida(referencia)
    return _raiz(subcarpeta) / referencia


def guardar(contenido, extension, subcarpeta=SUBCARPETA):
    """Escribe el archivo con un nombre aleatorio y devuelve su referencia. Se crea con `O_EXCL` (no pisa nada) y
    permisos 0640; la carpeta, 0750. En el servidor la carpeta de documentos tiene el bit setgid para que el grupo
    del respaldo pueda leerlos."""
    if extension not in ('jpg', 'png'):
        raise ReferenciaInvalida(extension)
    carpeta = _raiz(subcarpeta)
    carpeta.mkdir(mode=0o750, parents=True, exist_ok=True)
    referencia = f'{uuid.uuid4().hex}.{extension}'
    descriptor = os.open(_ruta(referencia, subcarpeta), os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_BINARY', 0), 0o640)
    try:
        with os.fdopen(descriptor, 'wb') as archivo:
            archivo.write(contenido)
            archivo.flush()
            os.fsync(archivo.fileno())
    except BaseException:
        borrar(referencia, subcarpeta)
        raise
    return referencia


def abrir(referencia, subcarpeta=SUBCARPETA):
    """Abre el archivo para leerlo; `FileNotFoundError` si no está."""
    return open(_ruta(referencia, subcarpeta), 'rb')


def existe(referencia, subcarpeta=SUBCARPETA):
    try:
        return _ruta(referencia, subcarpeta).is_file()
    except ReferenciaInvalida:
        return False


def borrar(referencia, subcarpeta=SUBCARPETA):
    """Borra el archivo si existe; devuelve si lo borró. Nunca lanza por un archivo que ya no está."""
    try:
        _ruta(referencia, subcarpeta).unlink()
        return True
    except (FileNotFoundError, ReferenciaInvalida):
        return False
