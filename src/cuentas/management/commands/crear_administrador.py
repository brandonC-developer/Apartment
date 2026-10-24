"""Crea la única cuenta administradora (RF-27, RN-25). Se ejecuta en el servidor."""
from getpass import getpass

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from cuentas.autenticacion import emitir_token_registro
from cuentas.models import Administrador
from nucleo import auditoria


# Quien ejecuta el comando es el solicitante, en el servidor (propuesta del asistente).
ACTOR_SERVIDOR = 'servidor'


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
        administrador = Administrador.objects.crear_administrador(usuario, contrasena)
        token = emitir_token_registro(administrador)
        auditoria.registrar(
            'cuenta_creada', 'administrador', registro_id=administrador.pk, actor=ACTOR_SERVIDOR)
        self.stdout.write(self.style.SUCCESS(f'Cuenta «{usuario}» creada. Segundo factor sin registrar.'))
        self.stdout.write(f'Token de registro del segundo factor (se muestra una sola vez, vale 24 horas): {token}')

    def pedir_contrasena(self):
        primera = getpass('Contraseña: ')
        if primera != getpass('Repita la contraseña: '):
            raise CommandError('Las contraseñas no coinciden.')
        return primera
