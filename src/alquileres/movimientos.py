"""Punto de extensión para los movimientos (pagos) que llegan en la E3.

La E2 necesita tres preguntas sobre movimientos para finalizar y anular contratos (RF-09, RF-10, RF-48, RN-17), pero la
tabla de movimientos todavía no existe. Se contestan con un **proveedor** reemplazable, como el punto de extensión de
bloqueos de `inquilinos` (decisión 5 de la E1): el proveedor por omisión dice que no hay movimientos; la E3 lo
reemplaza con consultas reales a su tabla (`usar`). Propuesta del asistente.
"""
from decimal import Decimal


class ProveedorSinMovimientos:
    """Hasta la E3 no hay movimientos: nada está pagado."""

    def obligacion_tiene_movimientos_validos(self, obligacion):
        return False

    def abonos_validos(self, obligacion):
        """Suma de los movimientos válidos aplicados a la obligación (RN-22)."""
        return Decimal('0')

    def contrato_tiene_movimientos_validos(self, contrato):
        """Movimientos válidos de alquiler o de depósito del contrato (RF-48)."""
        return False


_proveedor = ProveedorSinMovimientos()


def usar(proveedor):
    global _proveedor
    _proveedor = proveedor


def restablecer():
    """Vuelve al proveedor por omisión (las pruebas)."""
    usar(ProveedorSinMovimientos())


def obligacion_tiene_movimientos_validos(obligacion):
    return _proveedor.obligacion_tiene_movimientos_validos(obligacion)


def abonos_validos(obligacion):
    return _proveedor.abonos_validos(obligacion)


def contrato_tiene_movimientos_validos(contrato):
    return _proveedor.contrato_tiene_movimientos_validos(contrato)
