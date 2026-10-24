"""Comando configurar_organizacion (decisión del solicitante, 24-oct-2026). Necesita PostgreSQL."""
from datetime import time
from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from .models import Auditoria, Organizacion


def correr(*args):
    salida = StringIO()
    call_command('configurar_organizacion', *args, stdout=salida)
    return salida.getvalue()


class ConfigurarOrganizacionTests(TestCase):
    def test_sin_opciones_muestra_la_configuracion_y_no_cambia_nada(self):
        texto = correr()
        self.assertIn('Zona horaria: America/Costa_Rica', texto)
        self.assertIn('Hora del proceso diario: 07:00', texto)
        self.assertIn('(sin definir)', texto)
        self.assertEqual(Auditoria.objects.count(), 0)

    def test_cambia_el_responsable_la_zona_y_la_hora_y_lo_audita_sin_valores_personales(self):
        texto = correr('--nombre-responsable', ' Nombre Apellido ', '--direccion-responsable', 'Calle 1',
                       '--zona-horaria', 'America/Bogota', '--hora-proceso-diario', '06:30')
        o = Organizacion.objects.get()
        self.assertEqual((o.nombre_responsable, o.direccion_responsable, o.zona_horaria, o.hora_proceso_diario),
                         ('Nombre Apellido', 'Calle 1', 'America/Bogota', time(6, 30)))
        self.assertIn('Organización actualizada', texto)
        r = Auditoria.objects.get(accion='organizacion_actualizada')
        self.assertEqual(r.actor, 'servidor')
        self.assertEqual(set(r.campos_modificados),
                         {'nombre_responsable', 'direccion_responsable', 'zona_horaria', 'hora_proceso_diario'})
        valores = str(r.valor_anterior) + str(r.valor_nuevo)
        self.assertNotIn('Nombre', valores)
        self.assertNotIn('Calle', valores)
        self.assertIn('America/Bogota', valores)

    def test_rechaza_una_zona_o_una_hora_invalidas_sin_cambiar_nada(self):
        for opciones in (('--zona-horaria', 'Marte/Olympus'), ('--hora-proceso-diario', '25:00'),
                         ('--hora-proceso-diario', 'tarde')):
            with self.assertRaises(CommandError, msg=opciones):
                correr(*opciones)
        self.assertEqual(Organizacion.objects.get().zona_horaria, 'America/Costa_Rica')
        self.assertEqual(Auditoria.objects.count(), 0)

    def test_repetir_el_mismo_valor_no_genera_auditoria(self):
        correr('--zona-horaria', 'America/Costa_Rica')
        self.assertEqual(Auditoria.objects.count(), 0)
