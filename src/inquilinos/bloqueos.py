"""Punto de extensión del bloqueo de desactivar a un inquilino (RF-04, CA-29; decisión del solicitante del
24-oct-2026).

`inquilinos` no puede importar `alquileres` (ADR-030: las dependencias van hacia abajo y un ciclo rompería
las migraciones). Por eso cada aplicación que sepa de un motivo de bloqueo registra aquí una función que
recibe el inquilino y devuelve una lista de motivos (vacía si no bloquea). La E1 no registra ninguna
real: la E2 aporta «contrato vigente» y la E3, «saldos pendientes».
"""

_comprobaciones = []


def registrar(funcion):
    """Registra una comprobación; sirve como decorador. Registrar dos veces la misma no la duplica."""
    if funcion not in _comprobaciones:
        _comprobaciones.append(funcion)
    return funcion


def quitar(funcion):
    """Solo para las pruebas."""
    if funcion in _comprobaciones:
        _comprobaciones.remove(funcion)


def motivos_de_bloqueo(inquilino):
    """Todos los motivos que impiden desactivar al inquilino."""
    motivos = []
    for comprobacion in tuple(_comprobaciones):
        motivos.extend(comprobacion(inquilino) or [])
    return motivos
