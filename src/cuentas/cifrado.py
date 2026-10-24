"""Cifrado del secreto del segundo factor con Fernet/MultiFernet (actualización zzb).

Protege contra una fuga de la base o de un respaldo; no contra una aplicación comprometida,
que lee la clave de /etc/sga (ADR-032, decisión 6).
"""
from cryptography.fernet import Fernet, MultiFernet
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def _multifernet():
    claves = settings.CLAVES_CIFRADO
    if not claves:
        raise ImproperlyConfigured(
            'Falta la clave de cifrado: defina SGA_CLAVE_CIFRADO o el archivo /etc/sga/clave_cifrado.'
        )
    return MultiFernet([Fernet(clave) for clave in claves])


def cifrar(texto):
    return _multifernet().encrypt(texto.encode('utf-8')).decode('ascii')


def descifrar(token):
    return _multifernet().decrypt(token.encode('ascii')).decode('utf-8')


def recifrar(token):
    """Vuelve a cifrar un token con la primera clave (rotación)."""
    return _multifernet().rotate(token.encode('ascii')).decode('ascii')
