"""Concede al rol de la aplicación y al de respaldos lo que corresponde (ADR-031, decisión 3).

Debe ejecutarlo el rol dueño después de cada `migrate`:
    SGA_BD_USUARIO=sga_dueno python manage.py migrate
    SGA_BD_USUARIO=sga_dueno python manage.py aplicar_privilegios
Es idempotente. Una tabla sin entrada en `sga/privilegios.py` queda sin privilegios y el comando
avisa de cuáles son.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from nucleo import privilegios
from sga.privilegios import PRIVILEGIOS


class Command(BaseCommand):
    help = 'Aplica el archivo de privilegios de las tablas (idempotente).'

    def add_arguments(self, parser):
        parser.add_argument('--mostrar', action='store_true', help='Solo imprime el SQL, sin ejecutarlo.')

    def handle(self, *args, mostrar, **opciones):
        if mostrar:
            self.stdout.write(';\n'.join(privilegios.sentencias()) + ';')
            return
        sin_entrada = sorted(privilegios.tablas_existentes() - set(PRIVILEGIOS))
        with transaction.atomic():
            privilegios.aplicar()
        self.stdout.write(self.style.SUCCESS(f'Privilegios aplicados a {len(PRIVILEGIOS)} tablas.'))
        for tabla in sin_entrada:
            self.stdout.write(self.style.WARNING(
                f'La tabla «{tabla}» no consta en sga/privilegios.py: la aplicación no tiene acceso.'))
