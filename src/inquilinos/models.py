"""Inquilinos, consentimiento y fotografías del documento (RF-01 a RF-05, RF-39, RF-45; MDD v0.7).

Dependencias (ADR-030): solo hacia `nucleo`. El acceso a una fotografía de contrato (RF-52) no está
aquí: lo resuelve la E2 (ver la actualización 2026-10-24r).
"""
from django.db import models
from django.db.models import Q

from nucleo.models import RegistroProtegido

TAMANO_MAXIMO = 5 * 1024 * 1024  # 5 242 880 bytes (RF-02, R27)
TIPOS_DE_IMAGEN = ('image/jpeg', 'image/png')


class Inquilino(models.Model):
    """Entidad INQUILINO. Los datos personales se anulan al desasociar (RF-41, la E5)."""
    CEDULA, DIMEX, PASAPORTE, OTRO = 'cedula', 'dimex', 'pasaporte', 'otro'
    TIPOS_DE_DOCUMENTO = [(CEDULA, 'Cédula'), (DIMEX, 'DIMEX'), (PASAPORTE, 'Pasaporte'), (OTRO, 'Otro')]

    nombre_completo = models.CharField(max_length=200, null=True)
    tipo_documento = models.CharField(max_length=10, choices=TIPOS_DE_DOCUMENTO)
    numero_documento = models.CharField(max_length=60, null=True)
    telefono = models.CharField(max_length=40, null=True, blank=True)
    correo = models.CharField(max_length=254, null=True, blank=True)
    activo = models.BooleanField(default=True)
    desasociado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'inquilino'
        verbose_name_plural = 'inquilinos'
        ordering = ['nombre_completo', 'id']
        indexes = [
            # Para advertir de un documento duplicado (RF-01); no es único: es una advertencia, no un bloqueo.
            models.Index(fields=['tipo_documento', 'numero_documento'], name='inquilino_documento_idx'),
        ]
        constraints = [
            models.CheckConstraint(
                name='inquilino_tipo_de_documento',
                condition=Q(tipo_documento__in=['cedula', 'dimex', 'pasaporte', 'otro']),
            ),
            # El nombre y el número de documento son obligatorios, salvo en un inquilino desasociado.
            models.CheckConstraint(
                name='inquilino_datos_obligatorios',
                condition=(
                    Q(desasociado_en__isnull=False)
                    | (Q(nombre_completo__isnull=False) & ~Q(nombre_completo='')
                       & Q(numero_documento__isnull=False) & ~Q(numero_documento=''))
                ),
            ),
            # Un inquilino desasociado no conserva datos personales (RF-41).
            models.CheckConstraint(
                name='inquilino_desasociado_sin_datos',
                condition=(
                    Q(desasociado_en__isnull=True)
                    | (Q(nombre_completo__isnull=True) & Q(numero_documento__isnull=True)
                       & Q(telefono__isnull=True) & Q(correo__isnull=True))
                ),
            ),
        ]

    def __str__(self):
        return self.nombre_completo or f'Inquilino {self.pk} (desasociado)'


class TextoConsentimiento(RegistroProtegido):
    """Cada versión del texto informativo, inmutable (RF-39: una versión nueva es una fila nueva).

    `borrador` es verdadero mientras ningún abogado haya validado el texto (decisión del solicitante
    del 24-oct-2026; DP-21): el sistema lo muestra como «sin validar por abogado».
    """
    version = models.PositiveIntegerField(unique=True)
    contenido = models.TextField()
    borrador = models.BooleanField(default=True)
    vigente_desde = models.DateTimeField()

    class Meta:
        verbose_name = 'texto de consentimiento'
        verbose_name_plural = 'textos de consentimiento'
        ordering = ['-version']
        constraints = [
            models.CheckConstraint(name='texto_consentimiento_con_contenido', condition=~Q(contenido='')),
        ]

    def __str__(self):
        return f'Versión {self.version}' + (' (borrador sin validar)' if self.borrador else '')


class Consentimiento(RegistroProtegido):
    """El consentimiento de un inquilino sobre una versión del texto (RF-39, OL-13). Solo se puede
    registrar la revocación, sin efecto retroactivo."""
    CAMPOS_ACTUALIZABLES = ('revocado_en',)
    FISICO, ELECTRONICO = 'fisico', 'electronico'
    MEDIOS = [(FISICO, 'Físico'), (ELECTRONICO, 'Electrónico')]

    inquilino = models.ForeignKey(Inquilino, on_delete=models.PROTECT, related_name='consentimientos')
    texto = models.ForeignKey(TextoConsentimiento, on_delete=models.PROTECT, related_name='consentimientos')
    medio = models.CharField(max_length=12, choices=MEDIOS)
    otorgado_en = models.DateTimeField()
    revocado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'consentimiento'
        verbose_name_plural = 'consentimientos'
        ordering = ['-otorgado_en', '-id']
        constraints = [
            models.CheckConstraint(name='consentimiento_medio', condition=Q(medio__in=['fisico', 'electronico'])),
            models.CheckConstraint(
                name='consentimiento_revocacion_posterior',
                condition=Q(revocado_en__isnull=True) | Q(revocado_en__gte=models.F('otorgado_en')),
            ),
        ]

    @property
    def vigente(self):
        return self.revocado_en is None


class DocumentoIdentidad(RegistroProtegido):
    """Una fotografía de una cara del documento (RF-01, RF-02, ADR-003). Reemplazarla marca la anterior
    como eliminada (R25). El archivo está en el almacenamiento privado, con nombre aleatorio."""
    CAMPOS_ACTUALIZABLES = ('eliminado_en',)
    FRENTE, REVERSO = 'frente', 'reverso'
    CARAS = [(FRENTE, 'Frente'), (REVERSO, 'Reverso')]

    inquilino = models.ForeignKey(Inquilino, on_delete=models.PROTECT, related_name='documentos')
    cara = models.CharField(max_length=7, choices=CARAS)
    referencia_archivo = models.CharField(max_length=255, unique=True)
    tipo_real_archivo = models.CharField(max_length=20)
    tamano_bytes = models.PositiveIntegerField()
    creado_en = models.DateTimeField(auto_now_add=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'documento de identidad'
        verbose_name_plural = 'documentos de identidad'
        ordering = ['inquilino_id', 'cara', '-creado_en']
        constraints = [
            models.CheckConstraint(name='documento_cara', condition=Q(cara__in=['frente', 'reverso'])),
            # R25: a lo sumo una fotografía activa por cara.
            models.UniqueConstraint(
                fields=['inquilino', 'cara'], condition=Q(eliminado_en__isnull=True),
                name='documento_una_activa_por_cara'),
            # R27: peso y tipo real, segunda defensa (la primera es la validación del servidor, RF-02).
            models.CheckConstraint(
                name='documento_tamano',
                condition=Q(tamano_bytes__gte=1, tamano_bytes__lte=TAMANO_MAXIMO),
            ),
            models.CheckConstraint(
                name='documento_tipo_real', condition=Q(tipo_real_archivo__in=list(TIPOS_DE_IMAGEN))),
        ]

    @property
    def activo(self):
        return self.eliminado_en is None


class AccesoDocumento(RegistroProtegido):
    """Cada consulta o descarga de una fotografía de cédula (RF-45, CA-26), sin la imagen. Solo inserción (R12).

    El acceso a la fotografía de un contrato (`DOCUMENTO_CONTRATO`, R23) no se modela todavía: esa
    entidad es de `alquileres`, que depende de esta aplicación, y una clave foránea hacia ella crearía
    un ciclo de migraciones (ADR-030). Se decide en la E2.
    """
    CONSULTA, DESCARGA = 'consulta', 'descarga'
    ACCIONES = [(CONSULTA, 'Consulta'), (DESCARGA, 'Descarga')]

    documento = models.ForeignKey(DocumentoIdentidad, on_delete=models.PROTECT, related_name='accesos')
    actor = models.CharField(max_length=150)
    accion = models.CharField(max_length=10, choices=ACCIONES)
    ocurrido_en = models.DateTimeField(db_index=True)

    class Meta:
        verbose_name = 'acceso a documento'
        verbose_name_plural = 'accesos a documentos'
        ordering = ['-ocurrido_en', '-id']
        constraints = [
            models.CheckConstraint(name='acceso_documento_accion', condition=Q(accion__in=['consulta', 'descarga'])),
        ]
