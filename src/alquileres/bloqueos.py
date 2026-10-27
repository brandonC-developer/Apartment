"""Comprobaciones que `alquileres` registra en el punto de extensión de `inquilinos` para impedir desactivar a un
inquilino (RF-04, CA-29; decisión 5 de la E1). La E2 aporta «contrato futuro, vigente o por decidir»; la de saldos
pendientes es de la E3."""
from . import selectors


def por_contrato(inquilino):
    """Los motivos por los que el inquilino no se puede desactivar mientras tenga un contrato que lo ocupe (propuesta: se
    cuentan también los futuros, igual que para inactivar una propiedad, RF-06)."""
    hoy = selectors.hoy_local()
    return [
        f'Tiene un contrato {selectors.estado_del_contrato(c, hoy).replace("_", " ")} en la propiedad «{c.propiedad.alias}».'
        for c in selectors.contratos_que_ocupan_al_inquilino(inquilino, hoy).select_related('propiedad')]
