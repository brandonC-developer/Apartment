"""Constantes de la configuración regional (RF-33, ADR-005)."""
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.core.exceptions import ValidationError

CRC = 'CRC'
USD = 'USD'
MONEDAS = (CRC, USD)
MONEDA_PREDETERMINADA = CRC
ZONA_PREDETERMINADA = 'America/Costa_Rica'
# Símbolo delante de la cifra (RNF-12). El de USD es propuesta del asistente.
SIMBOLOS = {CRC: '₡', USD: '$'}


def validar_zona_horaria(valor):
    """Un identificador IANA que el sistema conozca (RF-33)."""
    try:
        ZoneInfo(valor)
    except (ZoneInfoNotFoundError, ValueError, OSError):
        raise ValidationError('«%(valor)s» no es una zona horaria IANA conocida.', params={'valor': valor})
