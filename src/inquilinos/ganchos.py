"""Ganchos para que otras aplicaciones reaccionen a un evento de `inquilinos` sin que `inquilinos` las importe
(ADR-030: las dependencias van hacia abajo).

`al_revocar`: funciones que reciben el consentimiento recién revocado y se ejecutan **dentro de la misma
transacción**. La E5 (`privacidad`) registrará la que abre de oficio la solicitud de supresión (RF-39, RF-40);
la E2, nada: consulta `selectors.tiene_consentimiento_vigente` antes de crear un contrato. Si un gancho falla,
la revocación se deshace.
"""

_al_revocar = []


def registrar_al_revocar(funcion):
    if funcion not in _al_revocar:
        _al_revocar.append(funcion)
    return funcion


def quitar_al_revocar(funcion):
    """Solo para las pruebas."""
    if funcion in _al_revocar:
        _al_revocar.remove(funcion)


def ejecutar_al_revocar(consentimiento):
    for funcion in tuple(_al_revocar):
        funcion(consentimiento)
