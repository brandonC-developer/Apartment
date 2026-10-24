"""Pruebas del modelo y el servicio de auditoría (RF-28, R12, R14, R19, CA-53). Necesitan PostgreSQL."""
from datetime import date
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.test import RequestFactory, TestCase, override_settings

from . import auditoria
from .models import Auditoria, RegistroInmutable


def un_registro(**extra):
    datos = dict(accion='prueba', entidad='contrato', actor='admin')
    datos.update(extra)
    return auditoria.registrar(datos.pop('accion'), datos.pop('entidad'), **datos)


class ServicioTests(TestCase):
    def test_un_cambio_de_importe_guarda_valores_y_uno_de_telefono_solo_el_nombre(self):
        r = un_registro(cambios={
            'telefono': ('8888-0000', '7777-1111'),
            'importe': (Decimal('180000.00'), Decimal('190000.00')),
            'vence': (date(2026, 11, 1), date(2026, 12, 1)),
        })
        r.refresh_from_db()
        self.assertEqual(r.campos_modificados, ['telefono', 'importe', 'vence'])
        self.assertEqual(r.valor_anterior, {'importe': '180000.00', 'vence': '2026-11-01'})
        self.assertEqual(r.valor_nuevo, {'importe': '190000.00', 'vence': '2026-12-01'})
        texto = str(r.valor_anterior) + str(r.valor_nuevo)
        self.assertNotIn('8888', texto)
        self.assertNotIn('7777', texto)

    def test_ningun_campo_personal_ni_secreto_conserva_su_valor(self):
        cambios = {c: ('antes-secreto', 'despues-secreto')
                   for c in auditoria.CAMPOS_PERSONALES | auditoria.CAMPOS_SECRETOS}
        r = un_registro(cambios=cambios)
        r.refresh_from_db()
        self.assertEqual(set(r.campos_modificados), set(cambios))
        self.assertIsNone(r.valor_anterior)
        self.assertIsNone(r.valor_nuevo)

    def test_sin_cambios_no_hay_valores(self):
        r = un_registro()
        self.assertEqual((r.campos_modificados, r.valor_anterior, r.valor_nuevo), ([], None, None))


class InmutabilidadTests(TestCase):
    def test_no_se_edita_ni_se_borra(self):
        r = un_registro()
        r.accion = 'otra'
        with self.assertRaises(RegistroInmutable):
            r.save()
        with self.assertRaises(RegistroInmutable):
            r.delete()
        with self.assertRaises(RegistroInmutable):
            Auditoria.objects.all().update(accion='otra')
        with self.assertRaises(RegistroInmutable):
            Auditoria.objects.all().delete()
        with self.assertRaises(RegistroInmutable):
            Auditoria.objects.filter(pk=r.pk).update(accion='otra')
        self.assertEqual(Auditoria.objects.get().accion, 'prueba')


class RestriccionR19Tests(TestCase):
    def test_proceso_exige_actor_sistema_y_ejecucion(self):
        un_registro(tipo_actor='proceso', actor='sistema', ejecucion_id=7)
        for extra in (
            dict(tipo_actor='proceso', actor='sistema'),
            dict(tipo_actor='proceso', actor='admin', ejecucion_id=7),
            dict(tipo_actor='administrador', actor='admin', ejecucion_id=7),
        ):
            with self.assertRaises(IntegrityError), transaction.atomic():
                un_registro(**extra)
        self.assertEqual(Auditoria.objects.count(), 1)


class IpDeOrigenTests(TestCase):
    def peticion(self, **meta):
        return RequestFactory().get('/', **meta)

    def test_usa_remote_addr_sin_cabecera_de_confianza(self):
        with override_settings(IP_ORIGEN_CABECERA=None):
            self.assertEqual(auditoria.ip_de_origen(self.peticion(REMOTE_ADDR='203.0.113.9')), '203.0.113.9')
            # Una cabecera enviada por el cliente se ignora si no está configurada como de confianza.
            self.assertEqual(
                auditoria.ip_de_origen(self.peticion(REMOTE_ADDR='203.0.113.9', HTTP_X_REAL_IP='1.1.1.1')),
                '203.0.113.9')

    def test_usa_la_cabecera_que_pone_nginx(self):
        with override_settings(IP_ORIGEN_CABECERA='HTTP_X_REAL_IP'):
            self.assertEqual(
                auditoria.ip_de_origen(self.peticion(REMOTE_ADDR='', HTTP_X_REAL_IP='198.51.100.4')),
                '198.51.100.4')

    def test_un_valor_que_no_es_ip_se_descarta(self):
        with override_settings(IP_ORIGEN_CABECERA='HTTP_X_REAL_IP'):
            self.assertIsNone(auditoria.ip_de_origen(self.peticion(HTTP_X_REAL_IP="1.1.1.1'; DROP TABLE")))
            self.assertIsNone(auditoria.ip_de_origen(self.peticion()))

    def test_admite_ipv6(self):
        with override_settings(IP_ORIGEN_CABECERA=None):
            self.assertEqual(auditoria.ip_de_origen(self.peticion(REMOTE_ADDR='2001:db8::1')), '2001:db8::1')
