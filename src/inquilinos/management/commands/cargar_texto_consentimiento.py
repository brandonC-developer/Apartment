"""Carga el texto informativo del consentimiento como una versión nueva (RF-39; decisión del solicitante del
24-oct-2026). Sin opciones genera el BORRADOR del asistente con la identidad del responsable guardada en la
organización y lo marca «sin validar por abogado». Con `--archivo` carga el texto de un archivo UTF-8; con
`--validado` además lo marca como validado por un abogado (DP-21).

    python manage.py cargar_texto_consentimiento
    python manage.py cargar_texto_consentimiento --archivo texto_del_abogado.txt --validado

Las versiones anteriores no se modifican; los consentimientos ya dados siguen apuntando a la suya.
"""
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from inquilinos import services, textos
from nucleo import organizacion

ACTOR_SERVIDOR = 'servidor'


class Command(BaseCommand):
    help = 'Carga el texto informativo del consentimiento como una versión nueva.'

    def add_arguments(self, parser):
        parser.add_argument('--archivo', help='Archivo UTF-8 con el texto definitivo.')
        parser.add_argument('--validado', action='store_true',
                            help='Marca el texto como validado por un abogado (solo con --archivo).')

    def handle(self, *args, archivo, validado, **opciones):
        if validado and not archivo:
            raise CommandError('--validado solo se usa con --archivo: el borrador del asistente no está validado.')
        if archivo:
            try:
                contenido = Path(archivo).read_text(encoding='utf-8')
            except (OSError, UnicodeDecodeError) as error:
                raise CommandError(f'No se pudo leer el archivo: {error}')
        else:
            org = organizacion.actual()
            try:
                contenido = textos.construir_borrador(org.nombre_responsable, org.direccion_responsable)
            except textos.FaltaIdentidadDelResponsable as error:
                raise CommandError(str(error))
        try:
            texto, creada = services.crear_version_texto(contenido, actor=ACTOR_SERVIDOR, borrador=not validado)
        except services.ErrorDeValidacion as error:
            raise CommandError(str(error.errores))
        estado = 'borrador sin validar por abogado' if texto.borrador else 'validado por abogado'
        if creada:
            self.stdout.write(self.style.SUCCESS(f'Versión {texto.version} cargada ({estado}).'))
        else:
            self.stdout.write(f'La versión {texto.version} ya tiene este contenido ({estado}); no se creó otra.')
