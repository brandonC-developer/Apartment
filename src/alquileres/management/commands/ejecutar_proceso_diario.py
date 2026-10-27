"""Proceso diario (RF-11, RNF-16): genera las obligaciones que faltan. Lo lanza el temporizador de systemd
(`sga-proceso-diario.timer`) y se puede ejecutar a mano las veces que se quiera: no crea duplicados.

    python manage.py ejecutar_proceso_diario

Termina con código distinto de cero si la ejecución quedó `fallida`, para que systemd la marque como fallida.
"""
from django.core.management.base import BaseCommand, CommandError

from alquileres import proceso
from alquileres.models import EjecucionProceso


class Command(BaseCommand):
    help = 'Genera las obligaciones que faltan de los contratos futuros, vigentes y por decidir (idempotente).'

    def handle(self, *args, **opciones):
        ejecucion = proceso.ejecutar()
        self.stdout.write(f'Ejecución {ejecucion.pk} del {ejecucion.fecha_local}: {ejecucion.resultado}. {ejecucion.detalle}')
        if ejecucion.resultado != EjecucionProceso.CORRECTA:
            raise CommandError('El proceso diario no terminó bien; revise el detalle y el registro.')
