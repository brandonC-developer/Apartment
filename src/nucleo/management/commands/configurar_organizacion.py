"""Configura la organización desde el servidor (decisión del solicitante, 24-oct-2026): el nombre y la
dirección del responsable, la zona horaria y la hora del proceso diario. No hay pantalla web para esto.

    python manage.py configurar_organizacion                      # muestra la configuración actual
    python manage.py configurar_organizacion --zona-horaria America/Costa_Rica --hora-proceso-diario 07:00

Cada cambio queda en la auditoría (del nombre y la dirección solo consta que cambiaron, no su valor).
IMPORTANTE: la hora del proceso diario también vive en el temporizador de systemd; cambiarla aquí no
mueve el temporizador. Cuando exista el proceso diario (E2), su unidad se ajusta en el servidor.
"""
from datetime import time

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from nucleo import organizacion

ACTOR_SERVIDOR = 'servidor'


class Command(BaseCommand):
    help = 'Muestra o cambia la configuración de la organización (responsable, zona, hora del proceso diario).'

    def add_arguments(self, parser):
        parser.add_argument('--nombre-responsable')
        parser.add_argument('--direccion-responsable')
        parser.add_argument('--zona-horaria', help='Identificador IANA, por ejemplo America/Costa_Rica.')
        parser.add_argument('--hora-proceso-diario', help='HH:MM en la zona de la organización.')

    def handle(self, *args, **opciones):
        cambios = {}
        if opciones['nombre_responsable'] is not None:
            cambios['nombre_responsable'] = opciones['nombre_responsable'].strip()
        if opciones['direccion_responsable'] is not None:
            cambios['direccion_responsable'] = opciones['direccion_responsable'].strip()
        if opciones['zona_horaria'] is not None:
            cambios['zona_horaria'] = opciones['zona_horaria'].strip()
        if opciones['hora_proceso_diario'] is not None:
            try:
                horas, minutos = opciones['hora_proceso_diario'].split(':')
                cambios['hora_proceso_diario'] = time(int(horas), int(minutos))
            except ValueError:
                raise CommandError('La hora debe ser HH:MM, por ejemplo 07:00.')
        if cambios:
            try:
                organizacion.actualizar(actor=ACTOR_SERVIDOR, **cambios)
            except ValidationError as error:
                raise CommandError(' '.join(f'{c}: {" ".join(m)}' for c, m in error.message_dict.items()))
            self.stdout.write(self.style.SUCCESS('Organización actualizada: ' + ', '.join(cambios)))
        actual = organizacion.actual()
        self.stdout.write(f'Responsable: {actual.nombre_responsable or "(sin definir)"}')
        self.stdout.write(f'Dirección: {actual.direccion_responsable or "(sin definir)"}')
        self.stdout.write(f'Zona horaria: {actual.zona_horaria}')
        self.stdout.write(f'Hora del proceso diario: {actual.hora_proceso_diario:%H:%M}')
