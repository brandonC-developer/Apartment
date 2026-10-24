"""Rescate por el servidor cuando se pierden el TOTP y los códigos de recuperación (RF-27)."""
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from cuentas.models import Administrador, CodigoRecuperacion


class Command(BaseCommand):
    help = (
        'Desactiva el segundo factor, borra los códigos de recuperación, reinicia el contador de '
        'intentos y cierra todas las sesiones; el segundo factor se registra de nuevo en el '
        'siguiente ingreso. No cambia la contraseña.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--confirmar', action='store_true', help='No pedir confirmación.')

    def handle(self, *args, confirmar, **opciones):
        administrador = Administrador.objects.first()
        if administrador is None:
            raise CommandError('No hay cuenta administradora.')
        if not confirmar and input(f'Escriba RESCATAR para desactivar el segundo factor de «{administrador.usuario}»: ') != 'RESCATAR':
            raise CommandError('Cancelado.')
        with transaction.atomic():
            administrador.secreto_segundo_factor = ''
            administrador.segundo_factor_activo = False
            administrador.ultimo_intervalo_totp = None
            administrador.fallos_consecutivos = 0
            administrador.espera_hasta = None
            administrador.save()
            CodigoRecuperacion.objects.filter(administrador=administrador).delete()
            Session.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Segundo factor desactivado y sesiones cerradas.'))
        self.stdout.write(self.style.WARNING(
            'Pendiente de implementar: constancia en la auditoría y aviso a las dos direcciones '
            '(RF-27); regístrelo a mano.'))
