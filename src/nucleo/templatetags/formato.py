"""Filtros de plantilla con el formato propio (RNF-12): {% load formato %}."""
from django import template

from .. import formato as f

register = template.Library()


@register.filter(name='fecha')
def filtro_fecha(valor):
    return f.fecha(valor) if valor else ''


@register.filter(name='fecha_hora')
def filtro_fecha_hora(valor, segundos=False):
    return f.fecha_hora(valor, segundos=bool(segundos)) if valor else ''


@register.filter(name='moneda')
def filtro_moneda(valor, codigo='CRC'):
    return f.moneda(valor, codigo) if valor is not None else ''


@register.filter(name='numero')
def filtro_numero(valor, decimales=2):
    return f.numero(valor, int(decimales)) if valor is not None else ''


@register.filter(name='porcentaje')
def filtro_porcentaje(valor, decimales=1):
    return f.porcentaje(valor, int(decimales)) if valor is not None else ''
