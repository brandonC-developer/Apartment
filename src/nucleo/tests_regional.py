"""Organización y configuración regional (RF-33, RNF-12, RNF-17, CA-18)."""
from datetime import date, datetime, time, timezone as utc
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.template import Context, Template
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from . import auditoria, formato, organizacion
from .models import Auditoria, Organizacion
from .regional import MONEDA_PREDETERMINADA, MONEDAS, ZONA_PREDETERMINADA


class FormatoTests(SimpleTestCase):
    def test_numeros_con_punto_de_miles_y_coma_decimal(self):
        casos = [
            (Decimal('180000.5'), '180.000,50'), (Decimal('0'), '0,00'), (Decimal('999.995'), '1.000,00'),
            (Decimal('1234567.891'), '1.234.567,89'), (180000, '180.000,00'), (Decimal('-1500.5'), '-1.500,50'),
            (Decimal('0.005'), '0,01'), (Decimal('-0.001'), '0,00'),
        ]
        for valor, esperado in casos:
            self.assertEqual(formato.numero(valor), esperado, valor)

    def test_sin_decimales(self):
        self.assertEqual(formato.numero(Decimal('92903.226'), 0), '92.903')
        self.assertEqual(formato.numero(Decimal('0.5'), 0), '1')

    def test_el_separador_de_miles_es_un_punto_y_no_un_espacio(self):
        self.assertNotIn(' ', formato.numero(Decimal('1234567.89')))
        self.assertNotIn(' ', formato.numero(Decimal('1234567.89')))

    def test_moneda_con_el_simbolo_delante(self):
        self.assertEqual(formato.moneda(Decimal('180000.50'), 'CRC'), '₡180.000,50')
        self.assertEqual(formato.moneda(Decimal('300'), 'USD'), '$300,00')
        self.assertEqual(formato.moneda(Decimal('-20000.25'), 'CRC'), '-₡20.000,25')
        self.assertEqual(formato.moneda(Decimal('92903'), 'CRC', 0), '₡92.903')

    def test_colones_sin_decimales_si_son_enteros_y_con_dos_si_tienen_centimos(self):
        """Decisión del solicitante, 24-oct-2026: nunca se oculta un céntimo guardado."""
        casos = [
            (Decimal('180000'), '₡180.000'), (Decimal('180000.00'), '₡180.000'), (180000, '₡180.000'),
            (Decimal('92903'), '₡92.903'), (Decimal('0'), '₡0'), (Decimal('-20000'), '-₡20.000'),
            (Decimal('180000.50'), '₡180.000,50'), (Decimal('150000.01'), '₡150.000,01'),
            (Decimal('150000.004'), '₡150.000'),  # menos de medio céntimo: se muestra entero
            (Decimal('150000.005'), '₡150.000,01'),  # medio céntimo sube: ya hay céntimo y se muestra
        ]
        for valor, esperado in casos:
            self.assertEqual(formato.moneda(valor, 'CRC'), esperado, valor)

    def test_dolares_siempre_con_dos_decimales(self):
        for valor, esperado in ((Decimal('300'), '$300,00'), (Decimal('300.5'), '$300,50'), (Decimal('0'), '$0,00')):
            self.assertEqual(formato.moneda(valor, 'USD'), esperado)

    def test_porcentaje_con_coma(self):
        self.assertEqual(formato.porcentaje(Decimal('3.2')), '3,2 %')
        self.assertEqual(formato.porcentaje(5, 0), '5 %')

    def test_los_float_se_rechazan(self):
        with self.assertRaises(TypeError):
            formato.numero(0.1)

    def test_fechas_dd_mm_aaaa(self):
        self.assertEqual(formato.fecha(date(2026, 2, 5)), '05/02/2026')
        self.assertEqual(formato.leer_fecha('05/02/2026'), date(2026, 2, 5))
        for malo in ('2026-02-05', '5/2/2026', '31/02/2026', '', None, '05/02/26'):
            with self.assertRaises(ValueError, msg=malo):
                formato.leer_fecha(malo)

    def test_leer_decimal_solo_acepta_el_formato_del_sistema(self):
        self.assertEqual(formato.leer_decimal('180.000,50'), Decimal('180000.50'))
        self.assertEqual(formato.leer_decimal('180000'), Decimal('180000'))
        self.assertEqual(formato.leer_decimal(' 3,2 '), Decimal('3.2'))
        self.assertEqual(formato.leer_decimal('-1.500,5'), Decimal('-1500.5'))
        for malo in ('1.5', '1.23', '1,234.56', '12.34.567', '1..000', '1,', ',5', 'abc', '', None, '1 000'):
            with self.assertRaises(ValueError, msg=malo):
                formato.leer_decimal(malo)

    def test_ida_y_vuelta(self):
        for valor in (Decimal('0.00'), Decimal('12.30'), Decimal('999999.99'), Decimal('1234567.00')):
            self.assertEqual(formato.leer_decimal(formato.numero(valor)), valor)

    def test_filtros_de_plantilla(self):
        plantilla = Template(
            '{% load formato %}{{ m|moneda:"CRC" }}|{{ p|porcentaje }}|{{ f|fecha }}|{{ n|numero:0 }}|{{ v|moneda }}|{{ e|moneda:"CRC" }}')
        salida = plantilla.render(Context({'m': Decimal('180000.5'), 'p': Decimal('3.2'),
                                           'f': date(2026, 2, 5), 'n': Decimal('1234.5'), 'v': None, 'e': Decimal('180000')}))
        self.assertEqual(salida, '₡180.000,50|3,2 %|05/02/2026|1.235||₡180.000')


class ConstantesTests(SimpleTestCase):
    def test_valores_predeterminados(self):
        self.assertEqual(MONEDA_PREDETERMINADA, 'CRC')
        self.assertEqual(MONEDAS, ('CRC', 'USD'))
        self.assertEqual(ZONA_PREDETERMINADA, 'America/Costa_Rica')


class OrganizacionTests(TestCase):
    def test_la_migracion_crea_la_fila_unica_con_los_valores_predeterminados(self):
        o = Organizacion.objects.get()
        self.assertEqual((o.pk, o.zona_horaria, o.hora_proceso_diario), (1, 'America/Costa_Rica', time(7, 0)))

    def test_solo_cabe_una_fila(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Organizacion.objects.create(id=2)
        self.assertEqual(Organizacion.objects.count(), 1)

    def test_zona_invalida_se_rechaza(self):
        o = organizacion.actual()
        o.zona_horaria = 'Marte/Olympus'
        with self.assertRaises(ValidationError):
            o.full_clean()
        with self.assertRaises(ValidationError):
            organizacion.actualizar(actor='admin', zona_horaria='Marte/Olympus')
        self.assertEqual(Organizacion.objects.get().zona_horaria, 'America/Costa_Rica')

    def test_actualizar_audita_los_nombres_de_los_campos_personales_y_los_valores_de_la_zona(self):
        organizacion.actualizar(
            actor='admin', ip_origen='203.0.113.1', nombre_responsable='Nombre Apellido',
            direccion_responsable='Calle 1', zona_horaria='America/Bogota')
        r = Auditoria.objects.get(accion='organizacion_actualizada')
        self.assertEqual(set(r.campos_modificados), {'nombre_responsable', 'direccion_responsable', 'zona_horaria'})
        self.assertEqual(r.valor_anterior, {'zona_horaria': 'America/Costa_Rica'})
        self.assertEqual(r.valor_nuevo, {'zona_horaria': 'America/Bogota'})
        self.assertNotIn('Nombre', str(r.valor_nuevo) + str(r.valor_anterior))
        self.assertNotIn('Calle', str(r.valor_nuevo))
        self.assertEqual(r.ip_origen, '203.0.113.1')

    def test_sin_cambios_no_hay_auditoria_y_los_campos_ajenos_se_rechazan(self):
        organizacion.actualizar(actor='admin', zona_horaria='America/Costa_Rica')
        self.assertEqual(Auditoria.objects.count(), 0)
        with self.assertRaises(ValueError):
            organizacion.actualizar(actor='admin', id=5)

    def test_cambiar_la_zona_no_modifica_los_registros_historicos(self):
        """CA-18: los instantes están en UTC; solo cambia la presentación."""
        instante = datetime(2026, 10, 23, 18, 0, tzinfo=utc.utc)
        r = auditoria.registrar('prueba', 'contrato', actor='admin', ahora=instante)
        with timezone.override('America/Costa_Rica'):
            antes = formato.fecha_hora(r.ocurrido_en)
        organizacion.actualizar(actor='admin', zona_horaria='Asia/Tokyo')
        r.refresh_from_db()
        self.assertEqual(r.ocurrido_en, instante)
        with timezone.override('Asia/Tokyo'):
            despues = formato.fecha_hora(r.ocurrido_en)
        self.assertEqual(antes, '23/10/2026 12:00')
        self.assertEqual(despues, '24/10/2026 03:00')


class ZonaEnLaPeticionTests(TestCase):
    def mostrar(self):
        from cuentas.models import Administrador
        return Administrador

    def pagina_de_auditoria(self):
        from cuentas.tests import CONTRASENA, CLAVE_A
        from django.test import override_settings
        import pyotp
        with override_settings(CLAVES_CIFRADO=[CLAVE_A]):
            admin = self.mostrar().objects.crear_administrador('admin', CONTRASENA)
            secreto = pyotp.random_base32()
            admin.fijar_secreto_segundo_factor(secreto)
            admin.segundo_factor_activo = True
            admin.save()
            self.client.post('/entrar/', {'usuario': 'admin', 'contrasena': CONTRASENA})
            self.client.post('/entrar/codigo/', {'codigo': pyotp.TOTP(secreto).now()})
            auditoria.registrar('hito', 'prueba', actor='admin', ahora=datetime(2026, 10, 23, 18, 0, tzinfo=utc.utc))
            return self.client.get('/auditoria/', {'accion': 'hito'}).content.decode()

    def test_la_pantalla_usa_la_zona_de_la_organizacion(self):
        self.assertIn('23/10/2026 12:00:00', self.pagina_de_auditoria())

    def test_si_cambia_la_zona_cambia_la_presentacion(self):
        organizacion.actualizar(actor='admin', zona_horaria='Asia/Tokyo')
        self.assertIn('24/10/2026 03:00:00', self.pagina_de_auditoria())

    def test_una_zona_ilegible_en_la_base_cae_a_la_predeterminada(self):
        Organizacion.objects.update(zona_horaria='Zona/Rota')
        self.assertIn('23/10/2026 12:00:00', self.pagina_de_auditoria())

    def test_la_zona_se_desactiva_al_terminar_la_peticion(self):
        organizacion.actualizar(actor='admin', zona_horaria='Asia/Tokyo')
        self.pagina_de_auditoria()
        self.assertEqual(timezone.get_current_timezone_name(), 'America/Costa_Rica')


class TextoDeLosModelosTests(TestCase):
    def test_textos(self):
        self.assertEqual(str(organizacion.actual()), 'Organización')
        organizacion.actualizar(actor='admin', nombre_responsable='Nombre Apellido')
        self.assertEqual(str(Organizacion.objects.get()), 'Nombre Apellido')
        r = auditoria.registrar('prueba', 'contrato', actor='admin', ahora=datetime(2026, 10, 24, 18, 30, 5, tzinfo=utc.utc))
        self.assertEqual(str(r), f'{r.ocurrido_en:%Y-%m-%d %H:%M:%S} prueba (admin)')
