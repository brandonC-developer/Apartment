"""Crea la única cuenta administradora (RF-27, RN-25). Se ejecuta en el servidor."""
from getpass import getpass

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from cuentas.models import Administrador


class Command(BaseCommand):
    help = (
        'Crea la cuenta administradora. La contraseña se pide por teclado, nunca como argumento. '
        'El segundo factor se registrará en el primer ingreso.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--usuario', required=True)

    def handle(self, *args, usuario, **opciones):
        if Administrador.objects.exists():
            raise CommandError('Ya existe la cuenta administradora (RN-25: solo puede haber una).')
        contrasena = self.pedir_contrasena()
        try:
            validate_password(contrasena)
        except ValidationError as error:
            raise CommandError(' '.join(error.messages))
        Administrador.objects.crear_administrador(usuario, contrasena)
        self.stdout.write(self.style.SUCCESS(f'Cuenta «{usuario}» creada. Segundo factor sin registrar.'))

    def pedir_contrasena(self):
        primera = getpass('Contraseña: ')
        if primera != getpass('Repita la contraseña: '):
            raise CommandError('Las contraseñas no coinciden.')
        return primera
