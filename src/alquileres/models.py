"""Propiedades, contratos, obligaciones y fotografías del contrato (RF-06 a RF-12, RF-43, RF-52; MDD v0.7; ADR-014,
ADR-016, ADR-030, ADR-031).

Dependencias (ADR-030): `alquileres` depende de `nucleo` y de `inquilinos`, nunca al revés. Por eso el acceso a la
fotografía de un contrato tiene su propia tabla aquí (decisión 1 de la E2, 26-oct-2026) y no una clave foránea desde
`inquilinos`, que crearía un ciclo de migraciones.

Los importes y los estados derivados (saldo, estado de la obligación, del contrato y de la propiedad) NO se
almacenan (MDD, sección 5). Las filas que no se editan ni se borran (R12) usan `RegistroProtegido`: lo que no está en
`CAMPOS_ACTUALIZABLES` no se actualiza, y la protección real es el rol de PostgreSQL de la aplicación (`sga/privilegios.py`).
"""
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateRangeField, RangeOperators
from django.db import models
from django.db.models import F, Func, Q, Value
from django.db.models.functions import Lower

from inquilinos.models import TAMANO_MAXIMO, TIPOS_DE_IMAGEN, Inquilino
from nucleo.models import RegistroProtegido

CRC, USD = 'CRC', 'USD'
MONEDAS = [(CRC, 'Colones'), (USD, 'Dólares')]  # RN-23
MAXIMO_DE_FOTOGRAFIAS_POR_CONTRATO = 10  # RF-52, R28


class Propiedad(models.Model):
    """Entidad PROPIEDAD (RF-06). El estado disponible u ocupada se deriva del contrato vigente."""
    alias = models.CharField(max_length=60)
    descripcion = models.TextField(blank=True, default='')
    direccion = models.TextField(blank=True, default='')
    inactiva = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'propiedad'
        verbose_name_plural = 'propiedades'
        ordering = ['alias', 'id']
        constraints = [
            # R20: alias obligatorio y único. Que no distinga mayúsculas es propuesta del asistente.
            models.CheckConstraint(name='propiedad_alias_con_texto', condition=~Q(alias__regex=r'^\s*$')),
            models.UniqueConstraint(Lower('alias'), name='propiedad_alias_unico'),
        ]

    def __str__(self):
        return self.alias


class Contrato(RegistroProtegido):
    """Entidad CONTRATO (RF-07 a RF-10, RF-36, RF-48). Las condiciones económicas viven en `CondicionContrato`.
    Solo cambian la fecha de fin (RF-09, y su renovación), el cierre y la anulación (RF-48); el cierre y la anulación
    se completan una sola vez.

    `cerrado_en` (propuesta del asistente, actualización 2026-10-26i) distingue un contrato *finalizado* (el
    administrador registró su fin, RF-09) de uno *por decidir* (la fecha de fin pasó sin cierre ni renovación,
    RF-42): sin esa marca el estado de RN-30 no se puede derivar."""
    CAMPOS_ACTUALIZABLES = ('fecha_fin', 'cerrado_en', 'anulado_en', 'motivo_anulacion')
    VIVIENDA, OTRO = 'vivienda', 'otro'
    DESTINOS = [(VIVIENDA, 'Vivienda'), (OTRO, 'Otro')]  # OL-06, OL-08

    inquilino = models.ForeignKey(Inquilino, on_delete=models.PROTECT, related_name='contratos')
    propiedad = models.ForeignKey(Propiedad, on_delete=models.PROTECT, related_name='contratos')
    destino = models.CharField(max_length=8, choices=DESTINOS)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)  # inclusive (RN-02)
    moneda = models.CharField(max_length=3, choices=MONEDAS)
    cerrado_en = models.DateTimeField(null=True, blank=True)
    anulado_en = models.DateTimeField(null=True, blank=True)
    motivo_anulacion = models.TextField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'contrato'
        verbose_name_plural = 'contratos'
        ordering = ['-fecha_inicio', '-id']
        constraints = [
            # R2 (ADR-031 decisión 1): dos contratos de una propiedad no comparten ningún día; ambas fechas son
            # inclusivas y sin fecha de fin el rango queda abierto. Un contrato anulado no cuenta (RN-02).
            ExclusionConstraint(
                name='contrato_sin_solape',
                expressions=[
                    ('propiedad', RangeOperators.EQUAL),
                    (Func(F('fecha_inicio'), F('fecha_fin'), Value('[]'), function='daterange',
                          output_field=DateRangeField()), RangeOperators.OVERLAPS),
                ],
                condition=Q(anulado_en__isnull=True),
            ),
            models.CheckConstraint(name='contrato_moneda', condition=Q(moneda__in=['CRC', 'USD'])),
            models.CheckConstraint(name='contrato_destino', condition=Q(destino__in=['vivienda', 'otro'])),
            models.CheckConstraint(
                name='contrato_fin_no_anterior_al_inicio',
                condition=Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=F('fecha_inicio'))),
            # Un contrato cerrado tiene su fecha de fin.
            models.CheckConstraint(name='contrato_cerrado_con_fin', condition=Q(cerrado_en__isnull=True) | Q(fecha_fin__isnull=False)),
            # R21: la anulación lleva su motivo, y sin anulación no hay motivo.
            models.CheckConstraint(
                name='contrato_anulacion_con_motivo',
                condition=(Q(anulado_en__isnull=True, motivo_anulacion__isnull=True)
                           | (Q(anulado_en__isnull=False) & Q(motivo_anulacion__isnull=False)
                              & ~Q(motivo_anulacion__regex=r'^\s*$')))),
        ]

    def __str__(self):
        return f'Contrato {self.pk} ({self.propiedad_id})'


class CondicionContrato(RegistroProtegido):
    """Entidad CONDICION_CONTRATO (RF-10, RN-14, ADR-014): el historial de monto, vencimiento y gracia. Solo
    inserción: una corrección retroactiva es una fila nueva y cada obligación afectada recibe un ajuste."""
    INICIAL, REAJUSTE, CORRECCION = 'inicial', 'reajuste', 'correccion'
    TIPOS = [(INICIAL, 'Inicial'), (REAJUSTE, 'Reajuste'), (CORRECCION, 'Corrección')]

    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, related_name='condiciones')
    monto_mensual = models.DecimalField(max_digits=14, decimal_places=2)
    dia_vencimiento = models.PositiveSmallIntegerField()
    dias_gracia = models.PositiveSmallIntegerField()
    vigente_desde = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPOS)
    fecha_notificacion = models.DateField(null=True, blank=True)  # solo en reajustes
    porcentaje = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)  # solo en reajustes
    tope_digitado = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)  # DP-22
    fuente_tope = models.CharField(max_length=200, null=True, blank=True)  # INEC o MIVAH
    motivo = models.TextField(null=True, blank=True)  # obligatorio en correcciones
    registrada_en = models.DateTimeField()

    class Meta:
        verbose_name = 'condición del contrato'
        verbose_name_plural = 'condiciones del contrato'
        ordering = ['contrato_id', 'vigente_desde', 'id']
        constraints = [
            # R3 (la parte de una sola tabla; que `vigente_desde` no preceda al inicio la comprueba el servicio).
            models.CheckConstraint(name='condicion_monto_positivo', condition=Q(monto_mensual__gt=0)),
            models.CheckConstraint(name='condicion_dia_de_vencimiento', condition=Q(dia_vencimiento__gte=1, dia_vencimiento__lte=31)),
            models.CheckConstraint(name='condicion_tipo', condition=Q(tipo__in=['inicial', 'reajuste', 'correccion'])),
            # Una sola condición inicial por contrato.
            models.UniqueConstraint(fields=['contrato'], condition=Q(tipo='inicial'), name='condicion_una_inicial'),
            # Los datos del reajuste solo van en reajustes, y el reajuste los lleva (RF-10).
            models.CheckConstraint(
                name='condicion_datos_de_reajuste',
                condition=(Q(tipo='reajuste', fecha_notificacion__isnull=False, porcentaje__isnull=False)
                           | (~Q(tipo='reajuste') & Q(fecha_notificacion__isnull=True, porcentaje__isnull=True,
                                                      tope_digitado__isnull=True, fuente_tope__isnull=True)))),
            # El tope digitado y su fuente van juntos o no van.
            models.CheckConstraint(
                name='condicion_tope_con_fuente',
                condition=(Q(tope_digitado__isnull=True, fuente_tope__isnull=True)
                           | (Q(tope_digitado__isnull=False) & Q(fuente_tope__isnull=False)
                              & ~Q(fuente_tope__regex=r'^\s*$')))),
            # La corrección exige motivo.
            models.CheckConstraint(
                name='condicion_correccion_con_motivo',
                condition=~Q(tipo='correccion') | (Q(motivo__isnull=False) & ~Q(motivo__regex=r'^\s*$'))),
        ]


class Obligacion(RegistroProtegido):
    """Entidad OBLIGACION (RF-11 a RF-15, RF-43, RN-04, RN-05, RN-12, RN-13). `importe_inicial` no se modifica
    nunca; solo se completa una vez la anulación. Saldo, importe vigente y estado se derivan.

    `fecha_vencimiento` y `fecha_limite` se pueden actualizar en una corrección retroactiva (RF-10, CA-22): decisión 3
    de la E2, 26-oct-2026. El valor anterior y el nuevo constan en la auditoría. Es la única excepción a la
    inmutabilidad de estas filas, además de la anulación."""
    CAMPOS_ACTUALIZABLES = ('anulada_en', 'motivo_anulacion', 'fecha_vencimiento', 'fecha_limite')
    REGULAR, APERTURA = 'regular', 'apertura'
    TIPOS = [(REGULAR, 'Regular'), (APERTURA, 'Saldo de apertura')]

    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, related_name='obligaciones')
    tipo = models.CharField(max_length=8, choices=TIPOS)
    periodo_inicio = models.DateField(null=True, blank=True)  # nulo solo en la apertura
    periodo_fin = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField()
    fecha_limite = models.DateField()  # vencimiento + días de gracia (RN-06)
    importe_inicial = models.DecimalField(max_digits=14, decimal_places=2)
    moneda = models.CharField(max_length=3, choices=MONEDAS)
    condicion = models.ForeignKey(CondicionContrato, null=True, blank=True, on_delete=models.PROTECT, related_name='obligaciones')
    datos_calculo = models.JSONField(null=True, blank=True)  # RN-12, RN-13
    anulada_en = models.DateTimeField(null=True, blank=True)
    motivo_anulacion = models.TextField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'obligación'
        verbose_name_plural = 'obligaciones'
        ordering = ['contrato_id', 'periodo_inicio', 'id']
        constraints = [
            # R1: una obligación regular por contrato y período; a lo sumo una apertura por contrato (RF-12, RNF-04).
            models.UniqueConstraint(fields=['contrato', 'periodo_inicio'], condition=Q(tipo='regular'),
                                    name='obligacion_un_periodo_por_contrato'),
            models.UniqueConstraint(fields=['contrato'], condition=Q(tipo='apertura'), name='obligacion_una_apertura'),
            models.CheckConstraint(name='obligacion_tipo', condition=Q(tipo__in=['regular', 'apertura'])),
            models.CheckConstraint(name='obligacion_moneda', condition=Q(moneda__in=['CRC', 'USD'])),
            models.CheckConstraint(
                name='obligacion_periodo_segun_tipo',
                condition=(Q(tipo='apertura', periodo_inicio__isnull=True, periodo_fin__isnull=True)
                           | Q(tipo='regular', periodo_inicio__isnull=False, periodo_fin__isnull=False,
                               periodo_fin__gte=F('periodo_inicio')))),
            models.CheckConstraint(name='obligacion_limite_no_anterior', condition=Q(fecha_limite__gte=F('fecha_vencimiento'))),
            models.CheckConstraint(name='obligacion_importe_positivo', condition=Q(importe_inicial__gt=0)),
            # RN-17: la anulación lleva su motivo.
            models.CheckConstraint(
                name='obligacion_anulacion_con_motivo',
                condition=(Q(anulada_en__isnull=True, motivo_anulacion__isnull=True)
                           | (Q(anulada_en__isnull=False) & Q(motivo_anulacion__isnull=False)
                              & ~Q(motivo_anulacion__regex=r'^\s*$')))),
        ]


class AjusteObligacion(RegistroProtegido):
    """Entidad AJUSTE_OBLIGACION (RF-09, RF-10, RN-14, ADR-016): cada cambio de importe es una fila nueva. Solo
    inserción (R12). Anterior = importe vigente antes de la fila; nuevo = anterior + `importe_delta`."""
    REAJUSTE, CORRECCION, PRORRATEO_FIN, AJUSTE_MANUAL = 'reajuste', 'correccion', 'prorrateo_fin', 'ajuste_manual'
    TIPOS = [(REAJUSTE, 'Reajuste'), (CORRECCION, 'Corrección'), (PRORRATEO_FIN, 'Prorrateo del último período'),
             (AJUSTE_MANUAL, 'Ajuste manual')]

    obligacion = models.ForeignKey(Obligacion, on_delete=models.PROTECT, related_name='ajustes')
    tipo = models.CharField(max_length=13, choices=TIPOS)
    importe_delta = models.DecimalField(max_digits=14, decimal_places=2)  # con signo; nunca cero
    condicion = models.ForeignKey(CondicionContrato, null=True, blank=True, on_delete=models.PROTECT, related_name='ajustes')
    motivo = models.TextField(blank=True, default='')
    registrado_en = models.DateTimeField()

    class Meta:
        verbose_name = 'ajuste de obligación'
        verbose_name_plural = 'ajustes de obligación'
        ordering = ['obligacion_id', 'registrado_en', 'id']
        constraints = [
            models.CheckConstraint(name='ajuste_tipo', condition=Q(tipo__in=['reajuste', 'correccion', 'prorrateo_fin', 'ajuste_manual'])),
            models.CheckConstraint(name='ajuste_delta_distinto_de_cero', condition=~Q(importe_delta=0)),
            # R13: la corrección y el ajuste manual llevan motivo.
            models.CheckConstraint(
                name='ajuste_motivo_obligatorio',
                condition=Q(tipo__in=['reajuste', 'prorrateo_fin']) | ~Q(motivo__regex=r'^\s*$')),
        ]


class DocumentoContrato(RegistroProtegido):
    """Entidad DOCUMENTO_CONTRATO (RF-52, ADR-003): una fotografía del contrato firmado por fila, asociada al
    contrato (no al inquilino ni a la propiedad). Solo inserción: **no tiene `eliminado_en`** porque su conservación
    depende de DP-28, todavía abierta (H20)."""
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, related_name='documentos')
    orden = models.PositiveSmallIntegerField()
    referencia_archivo = models.CharField(max_length=255, unique=True)
    tipo_real_archivo = models.CharField(max_length=20)
    tamano_bytes = models.PositiveIntegerField()
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'fotografía del contrato'
        verbose_name_plural = 'fotografías del contrato'
        ordering = ['contrato_id', 'orden']
        constraints = [
            # R22 y R28: a lo sumo 10 por contrato, numeradas de 1 a 10.
            models.UniqueConstraint(fields=['contrato', 'orden'], name='documento_contrato_un_orden'),
            models.CheckConstraint(
                name='documento_contrato_orden', condition=Q(orden__gte=1, orden__lte=MAXIMO_DE_FOTOGRAFIAS_POR_CONTRATO)),
            # R27: peso y tipo real, segunda defensa (la primera es la validación del servidor, RF-02).
            models.CheckConstraint(
                name='documento_contrato_tamano', condition=Q(tamano_bytes__gte=1, tamano_bytes__lte=TAMANO_MAXIMO)),
            models.CheckConstraint(
                name='documento_contrato_tipo_real', condition=Q(tipo_real_archivo__in=list(TIPOS_DE_IMAGEN))),
        ]


class AccesoDocumentoContrato(RegistroProtegido):
    """Cada consulta o descarga de la fotografía de un contrato (RF-45, RF-52, CA-77), sin la imagen. Solo inserción
    (R12). Es la tabla propia de la decisión 1 de la E2: R23 se cumple por construcción (una sola clave foránea)."""
    CONSULTA, DESCARGA = 'consulta', 'descarga'
    ACCIONES = [(CONSULTA, 'Consulta'), (DESCARGA, 'Descarga')]

    documento = models.ForeignKey(DocumentoContrato, on_delete=models.PROTECT, related_name='accesos')
    actor = models.CharField(max_length=150)
    accion = models.CharField(max_length=10, choices=ACCIONES)
    ocurrido_en = models.DateTimeField(db_index=True)

    class Meta:
        verbose_name = 'acceso a fotografía de contrato'
        verbose_name_plural = 'accesos a fotografías de contrato'
        ordering = ['-ocurrido_en', '-id']
        constraints = [
            models.CheckConstraint(name='acceso_contrato_accion', condition=Q(accion__in=['consulta', 'descarga'])),
        ]


class EjecucionProceso(RegistroProtegido):
    """Entidad EJECUCION_PROCESO (RNF-16, DAS 10.1): qué días corrió el proceso diario y cómo terminó. Al terminar
    solo se completan el instante, el resultado y el detalle."""
    CAMPOS_ACTUALIZABLES = ('terminada_en', 'resultado', 'detalle')
    EN_CURSO, CORRECTA, FALLIDA = 'en_curso', 'correcta', 'fallida'
    RESULTADOS = [(EN_CURSO, 'En curso'), (CORRECTA, 'Correcta'), (FALLIDA, 'Fallida')]

    fecha_local = models.DateField(db_index=True)
    iniciada_en = models.DateTimeField()
    terminada_en = models.DateTimeField(null=True, blank=True)
    resultado = models.CharField(max_length=8, choices=RESULTADOS, default=EN_CURSO)
    detalle = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'ejecución del proceso diario'
        verbose_name_plural = 'ejecuciones del proceso diario'
        ordering = ['-iniciada_en', '-id']
        constraints = [
            models.CheckConstraint(name='ejecucion_resultado', condition=Q(resultado__in=['en_curso', 'correcta', 'fallida'])),
            models.CheckConstraint(
                name='ejecucion_terminada_si_no_esta_en_curso',
                condition=Q(resultado='en_curso') | Q(terminada_en__isnull=False)),
        ]
