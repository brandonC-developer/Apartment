"""Proceso diario (RF-11, RF-42, RNF-04, RNF-16; DAS 10.1): genera las obligaciones que faltan de los contratos
futuros, vigentes y por decidir y deja constancia de la ejecución en `EjecucionProceso`.

Puede ejecutarse las veces que se quiera: una segunda ejecución el mismo día no crea nada (RNF-16). Un contrato que
falla no detiene a los demás; la ejecución termina `fallida` y su detalle dice cuáles fallaron. Los contratos *por
decidir* siguen generando obligaciones hasta que el administrador los cierre o los renueve (RF-42). Los avisos de RF-42
(120 días antes, notificación persistente y resumen por correo) son de la entrega de notificaciones.
"""
import logging

from django.utils import timezone

from nucleo import auditoria

from . import obligaciones, selectors
from .models import EjecucionProceso

registro = logging.getLogger(__name__)


def ejecutar(*, hoy=None, ahora=None):
    """Corre el proceso y devuelve su `EjecucionProceso` ya terminada."""
    ahora = ahora or timezone.now()
    hoy = hoy or selectors.hoy_local(ahora)
    ejecucion = EjecucionProceso.objects.create(fecha_local=hoy, iniciada_en=ahora)
    revisados, generadas, fallidos = 0, 0, []
    try:
        ids = list(selectors.contratos_en_estado(*selectors.ESTADOS_QUE_OCUPAN, hoy=hoy)
                   .order_by('pk').values_list('pk', flat=True))
        for contrato_id in ids:
            revisados += 1
            try:
                generadas += len(obligaciones.generar_obligaciones(
                    contrato_id, ejecucion_id=ejecucion.pk, hoy=hoy, ahora=ahora))
            except Exception as error:  # un contrato defectuoso no detiene a los demás
                registro.exception('Proceso diario: falló el contrato %s', contrato_id)
                fallidos.append(f'contrato {contrato_id}: {type(error).__name__}')
        detalle = f'Contratos revisados: {revisados}. Obligaciones generadas: {generadas}.'
        resultado = EjecucionProceso.CORRECTA
        if fallidos:
            resultado = EjecucionProceso.FALLIDA
            detalle += ' Fallaron: ' + '; '.join(fallidos) + '.'
    except Exception as error:  # fallo general: se registra y se deja ver
        registro.exception('Proceso diario: falló la ejecución')
        resultado, detalle = EjecucionProceso.FALLIDA, f'Falló la ejecución: {type(error).__name__}.'
    ejecucion.terminada_en, ejecucion.resultado, ejecucion.detalle = timezone.now(), resultado, detalle
    ejecucion.save(update_fields=['terminada_en', 'resultado', 'detalle'])
    auditoria.registrar(
        'proceso_diario_ejecutado', 'ejecucion_proceso', registro_id=ejecucion.pk, actor='sistema',
        tipo_actor='proceso', ejecucion_id=ejecucion.pk, ahora=ahora,
        cambios={'resultado': (None, resultado), 'obligaciones_generadas': (None, generadas)})
    return ejecucion
