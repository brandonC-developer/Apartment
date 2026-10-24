"""Formato propio de fechas, números, moneda y porcentajes (RNF-12, decisión del solicitante del
21-oct-2026): no depende del idioma por defecto de la plataforma, cuyo separador de miles en `es` es
un espacio no separable.

Fechas dd/mm/aaaa; números con punto de miles y coma decimal; símbolo de la moneda delante
(₡180.000,50); porcentajes con coma (3,2 %). Todo con `Decimal`: nunca `float` (RNF-17). El redondeo
de la presentación es medio hacia arriba; el de los importes del negocio lo hacen los servicios.
"""
import re
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from django.utils import timezone

from .regional import SIMBOLOS

_ENTRADA = re.compile(r'^(?P<signo>[+-]?)(?P<entera>\d{1,3}(?:\.\d{3})+|\d+)(?:,(?P<decimal>\d+))?$')


def _decimal(valor):
    if isinstance(valor, float):
        raise TypeError('Los importes no se manejan como float (RNF-17); use Decimal.')
    return valor if isinstance(valor, Decimal) else Decimal(str(valor))


def numero(valor, decimales=2):
    """180000.5 → «180.000,50»."""
    cifra = _decimal(valor).quantize(Decimal(1).scaleb(-decimales), rounding=ROUND_HALF_UP)
    signo = '-' if cifra < 0 else ''
    entera, _, fraccion = f'{abs(cifra):f}'.partition('.')
    entera = f'{int(entera):,}'.replace(',', '.')
    return f'{signo}{entera},{fraccion}' if decimales else f'{signo}{entera}'


def moneda(valor, codigo, decimales=2):
    """«₡180.000,50»; el signo negativo va antes del símbolo (propuesta del asistente)."""
    texto = numero(valor, decimales)
    signo, cifra = ('-', texto[1:]) if texto.startswith('-') else ('', texto)
    return f'{signo}{SIMBOLOS[codigo]}{cifra}'


def porcentaje(valor, decimales=1):
    """3.2 → «3,2 %»."""
    return f'{numero(valor, decimales)} %'


def fecha(valor):
    return valor.strftime('%d/%m/%Y')


def fecha_hora(instante, segundos=False):
    """El instante se presenta en la zona activa, que es la de la organización (RF-33)."""
    local = timezone.localtime(instante)
    return local.strftime('%d/%m/%Y %H:%M:%S' if segundos else '%d/%m/%Y %H:%M')


def leer_decimal(texto):
    """«180.000,50» → Decimal('180000.50'). Solo admite el formato del sistema: el punto agrupa de
    a tres cifras y la coma separa los decimales. Cualquier otra forma (por ejemplo «1.5») se
    rechaza con ValueError, porque «1.234» sería ambiguo."""
    coincidencia = _ENTRADA.match((texto or '').strip())
    if not coincidencia:
        raise ValueError('Número no válido: use punto para los miles y coma para los decimales.')
    entera = coincidencia['entera'].replace('.', '')
    cifra = f"{coincidencia['signo']}{entera}.{coincidencia['decimal'] or '0'}"
    try:
        return Decimal(cifra)
    except InvalidOperation:  # pragma: no cover - la expresión regular ya lo impide
        raise ValueError('Número no válido.')


def leer_fecha(texto):
    """«05/02/2026» → date(2026, 2, 5). Solo dd/mm/aaaa."""
    coincidencia = re.fullmatch(r'(\d{2})/(\d{2})/(\d{4})', (texto or '').strip())
    if not coincidencia:
        raise ValueError('Fecha no válida: use dd/mm/aaaa.')
    dia, mes, anio = (int(x) for x in coincidencia.groups())
    return date(anio, mes, dia)
