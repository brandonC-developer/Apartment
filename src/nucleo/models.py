"""Modelos de `nucleo`: la auditoría (RF-28, RNF-06, R12, R14, R19) y la organización (RF-33)."""
from datetime import time

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import Q

from .regional import ZONA_PREDETERMINADA, validar_zona_horaria


class RegistroInmutable(Exception):
    """Se intentó editar o borrar una fila que solo admite inserción (R12, ADR-027)."""


class AuditoriaQuerySet(models.QuerySet):
    """Bloquea `update()` y `delete()` masivos. La protección real es el rol de PostgreSQL de la
    aplicación, que solo tendrá SELECT e INSERT (ADR-027); esto da un error claro antes."""

    def update(self, **kwargs):
        raise RegistroInmutable('La auditoría no admite UPDATE.')

    def delete(self):
        raise RegistroInmutable('La auditoría no admite DELETE.')


class Auditoria(models.Model):
    """Entidad AUDITORIA del MDD v0.7. Solo inserción."""
    TIPO_ADMINISTRADOR = 'administrador'
    TIPO_PROCESO = 'proceso'
    TIPOS_DE_ACTOR = [(TIPO_ADMINISTRADOR, 'Administrador'), (TIPO_PROCESO, 'Proceso')]

    entidad = models.CharField(max_length=60)
    registro_id = models.BigIntegerField(null=True, blank=True)
    actor = models.CharField(max_length=150)
    tipo_actor = models.CharField(max_length=13, choices=TIPOS_DE_ACTOR)
    # Sin clave foránea: la ejecución del proceso diario llega en la E2.
    ejecucion_id = models.BigIntegerField(null=True, blank=True)
    ip_origen = models.GenericIPAddressField(null=True, blank=True)
    accion = models.CharField(max_length=60, db_index=True)
    ocurrido_en = models.DateTimeField(db_index=True)
    campos_modificados = models.JSONField(default=list, blank=True)
    valor_anterior = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)
    valor_nuevo = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)

    objects = AuditoriaQuerySet.as_manager()

    class Meta:
        verbose_name = 'registro de auditoría'
        verbose_name_plural = 'registros de auditoría'
        ordering = ['-ocurrido_en', '-id']
        constraints = [
            # R19: un registro del proceso diario lleva actor «sistema» y su ejecución; uno del
            # administrador no lleva ejecución.
            models.CheckConstraint(
                name='auditoria_actor_y_ejecucion',
                condition=(
                    Q(tipo_actor='proceso', actor='sistema', ejecucion_id__isnull=False)
                    | Q(tipo_actor='administrador', ejecucion_id__isnull=True)
                ),
            ),
        ]

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise RegistroInmutable('Un registro de auditoría existente no se modifica.')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise RegistroInmutable('Un registro de auditoría no se borra.')

    def __str__(self):
        return f'{self.ocurrido_en:%Y-%m-%d %H:%M:%S} {self.accion} ({self.actor})'


class Organizacion(models.Model):
    """Entidad ORGANIZACION del MDD v0.7: una sola fila en la v1 (restricción de la tabla).

    La E0 solo incluye lo que necesita la configuración regional y la identidad del responsable
    (RF-33, art. 5 h de la Ley 8968); los demás atributos del MDD (correos, anticipaciones,
    retención, días de gracia) llegan con la entrega que los usa, en migraciones propias.
    """
    nombre_responsable = models.CharField(max_length=150, blank=True, default='')
    direccion_responsable = models.CharField(max_length=250, blank=True, default='')
    zona_horaria = models.CharField(
        max_length=64, default=ZONA_PREDETERMINADA, validators=[validar_zona_horaria])
    hora_proceso_diario = models.TimeField(default=time(7, 0))  # DP-02, hora local de la zona
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'organización'
        verbose_name_plural = 'organizaciones'
        constraints = [
            models.CheckConstraint(name='organizacion_una_sola_fila', condition=Q(id=1)),
        ]

    def __str__(self):
        return self.nombre_responsable or 'Organización'
