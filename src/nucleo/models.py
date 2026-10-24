"""Modelos de `nucleo`. Por ahora solo la auditoría (RF-28, RNF-06, R12, R14, R19)."""
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import Q


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
