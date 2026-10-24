"""Acceso a la organización y su cambio con auditoría (RF-33, RF-28, CA-18)."""
from django.db import transaction

from . import auditoria
from .models import Organizacion

CAMPOS_EDITABLES = ('nombre_responsable', 'direccion_responsable', 'zona_horaria', 'hora_proceso_diario')


def actual():
    """La única fila de la organización; se crea con los valores predeterminados si faltara."""
    organizacion, _ = Organizacion.objects.get_or_create(pk=1)
    return organizacion


def actualizar(*, actor, ip_origen=None, **campos):
    """Cambia campos de la organización y deja constancia en la auditoría (solo los nombres de los
    campos personales; los valores de la zona y la hora sí constan). Cambiar la zona no modifica
    ningún registro histórico: los instantes están en UTC y las fechas de calendario no tienen
    zona (RNF-17, CA-18); solo cambia cómo se presentan."""
    desconocidos = set(campos) - set(CAMPOS_EDITABLES)
    if desconocidos:
        raise ValueError(f'Campos no editables: {sorted(desconocidos)}')
    with transaction.atomic():
        organizacion = Organizacion.objects.select_for_update().get(pk=1)
        cambios = {}
        for campo, nuevo in campos.items():
            anterior = getattr(organizacion, campo)
            if anterior != nuevo:
                cambios[campo] = (anterior, nuevo)
                setattr(organizacion, campo, nuevo)
        if cambios:
            organizacion.full_clean()
            organizacion.save()
            auditoria.registrar(
                'organizacion_actualizada', 'organizacion', registro_id=1, actor=actor,
                ip_origen=ip_origen, cambios=cambios)
    return organizacion
