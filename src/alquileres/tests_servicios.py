"""Servicios y selectores de propiedades y contratos (RF-06 a RF-10, RF-36, RF-42, RF-48; CA-02, CA-10, CA-24, CA-29,
CA-31, CA-32, CA-62, CA-63, CA-67, CA-78). Necesitan PostgreSQL."""
import itertools
from datetime import date, datetime, timedelta, timezone as utc
from decimal import Decimal
from unittest.mock import patch

from django.db import IntegrityError
from django.test import TestCase

from inquilinos import services as servicios_de_inquilinos
from inquilinos.models import TextoConsentimiento
from inquilinos.services import ErrorDeValidacion, NoSePuedeDesactivar
from inquilinos.tests import un_documento
from nucleo.models import Auditoria

from . import calculo, movimientos, selectors, services
from .models import AjusteObligacion, Contrato, Obligacion, Propiedad
from .services import NoSePuedeInactivar

AHORA = datetime(2026, 10, 26, 12, 0, 0, tzinfo=utc.utc)   # hoy local: 2026-10-26
HOY = date(2026, 10, 26)
CONTADOR = itertools.count(1)


def d(texto):
    return date.fromisoformat(texto)


def obligacion_del_periodo(contrato, numero, importe='300000.00', **extra):
    per = calculo.periodo(contrato.fecha_inicio, numero)
    vencimiento = calculo.vencimiento(per, 5)
    datos = dict(contrato=contrato, tipo=Obligacion.REGULAR, periodo_inicio=per.inicio, periodo_fin=per.fin,
                 fecha_vencimiento=vencimiento, fecha_limite=calculo.fecha_limite(vencimiento, 7),
                 importe_inicial=Decimal(importe), moneda=contrato.moneda)
    datos.update(extra)
    return Obligacion.objects.create(**datos)


class ConMovimientos:
    """Proveedor falso de la E3: dice que hay movimientos y cuánto está abonado."""

    def __init__(self, abonado='0', obligaciones_con_pagos=(), contrato_con_pagos=False):
        self.abonado, self.con_pagos, self.contrato_con_pagos = Decimal(abonado), set(obligaciones_con_pagos), contrato_con_pagos

    def obligacion_tiene_movimientos_validos(self, obligacion):
        return obligacion.pk in self.con_pagos

    def abonos_validos(self, obligacion):
        return self.abonado if obligacion.pk in self.con_pagos else Decimal('0')

    def contrato_tiene_movimientos_validos(self, contrato):
        return self.contrato_con_pagos


class Base(TestCase):
    def setUp(self):
        self.addCleanup(movimientos.restablecer)
        self.texto = TextoConsentimiento.objects.create(version=1, contenido='Texto', vigente_desde=AHORA)
        self.inquilino = self.nuevo_inquilino()
        self.propiedad = services.registrar_propiedad(actor='admin', datos={'alias': 'Casa 1'}, ahora=AHORA)

    def nuevo_inquilino(self, con_frente=True):
        n = next(CONTADOR)
        inquilino = servicios_de_inquilinos.registrar_inquilino(
            actor='admin', datos=dict(nombre_completo=f'Persona {n}', tipo_documento='cedula', numero_documento=f'9-{n}'),
            texto=self.texto, medio='fisico', ahora=AHORA)
        if con_frente:
            un_documento(inquilino)
        return inquilino

    def datos(self, **extra):
        datos = dict(destino='vivienda', fecha_inicio=d('2027-01-01'), fecha_fin=None, moneda='CRC',
                     monto_mensual=Decimal('300000.00'), dia_vencimiento=5, dias_gracia=7)
        datos.update(extra)
        return datos

    def crear(self, inquilino=None, propiedad=None, **extra):
        return services.crear_contrato(
            actor='admin', ip_origen='203.0.113.5', inquilino_id=(inquilino or self.inquilino).pk,
            propiedad_id=(propiedad or self.propiedad).pk, datos=self.datos(**extra), ahora=AHORA)

    def errores(self, **extra):
        with self.assertRaises(ErrorDeValidacion) as contexto:
            self.crear(**extra)
        return contexto.exception.errores

    def nueva_propiedad(self, alias=None):
        return services.registrar_propiedad(actor='admin', datos={'alias': alias or f'Propiedad {next(CONTADOR)}'}, ahora=AHORA)

    def contrato_directo(self, propiedad=None, inicio='2026-01-01', fin=None, **extra):
        """Un contrato en el estado que se pida, sin pasar por las validaciones de creación."""
        return Contrato.objects.create(
            inquilino=self.nuevo_inquilino(), propiedad=propiedad or self.nueva_propiedad(), destino='vivienda',
            fecha_inicio=d(inicio), fecha_fin=d(fin) if fin else None, moneda='CRC', **extra)


class PropiedadesTests(Base):
    def test_registrar_guarda_y_audita_sin_los_valores_de_direccion_ni_descripcion(self):
        p = services.registrar_propiedad(actor='admin', ip_origen='203.0.113.5', ahora=AHORA,
                                         datos={'alias': '  Casa 2 ', 'descripcion': 'Apto de Maria', 'direccion': 'Calle 5, San Jose'})
        p.refresh_from_db()
        self.assertEqual((p.alias, p.descripcion, p.direccion, p.inactiva), ('Casa 2', 'Apto de Maria', 'Calle 5, San Jose', False))
        evento = Auditoria.objects.get(accion='propiedad_registrada', registro_id=p.pk)
        self.assertEqual(sorted(evento.campos_modificados), ['alias', 'descripcion', 'direccion'])
        self.assertNotIn('Maria', str(evento.valor_nuevo))
        self.assertNotIn('Calle 5', str(evento.valor_nuevo))
        self.assertEqual(evento.valor_nuevo, {'alias': 'Casa 2'})

    def test_el_alias_es_obligatorio_largo_maximo_y_unico_sin_importar_mayusculas(self):
        for alias, mensaje in (('', 'obligatorio'), ('   ', 'obligatorio'), ('x' * 61, '60'), ('casa 1', 'Ya existe'), ('CASA 1', 'Ya existe')):
            with self.assertRaises(ErrorDeValidacion, msg=alias) as contexto:
                services.registrar_propiedad(actor='admin', datos={'alias': alias}, ahora=AHORA)
            self.assertIn(mensaje, contexto.exception.errores['alias'][0])
        self.assertEqual(Propiedad.objects.count(), 1)

    def test_actualizar_guarda_y_audita_solo_lo_que_cambia(self):
        services.actualizar_propiedad(self.propiedad.pk, actor='admin', datos={'alias': 'Casa 1', 'direccion': 'Otra'}, ahora=AHORA)
        self.propiedad.refresh_from_db()
        self.assertEqual(self.propiedad.direccion, 'Otra')
        self.assertEqual(Auditoria.objects.get(accion='propiedad_actualizada').campos_modificados, ['direccion'])
        antes = Auditoria.objects.count()
        services.actualizar_propiedad(self.propiedad.pk, actor='admin', datos={'alias': 'Casa 1'}, ahora=AHORA)   # sin cambios
        self.assertEqual(Auditoria.objects.count(), antes)

    def test_actualizar_no_deja_repetir_el_alias_de_otra_ni_campos_ajenos(self):
        otra = self.nueva_propiedad('Casa 9')
        with self.assertRaises(ErrorDeValidacion):
            services.actualizar_propiedad(otra.pk, actor='admin', datos={'alias': 'casa 1'}, ahora=AHORA)
        with self.assertRaises(ValueError):
            services.actualizar_propiedad(otra.pk, actor='admin', datos={'inactiva': True}, ahora=AHORA)

    def test_ca_63_no_se_inactiva_con_un_contrato_futuro_vigente_o_por_decidir(self):
        for inicio, fin in (('2027-01-01', None), ('2026-01-01', None), ('2026-01-01', '2026-06-30')):
            p = self.nueva_propiedad()
            self.contrato_directo(p, inicio, fin)
            with self.assertRaises(NoSePuedeInactivar, msg=(inicio, fin)) as contexto:
                services.marcar_inactiva(p.pk, actor='admin', ahora=AHORA)
            self.assertEqual(len(contexto.exception.motivos), 1)
            p.refresh_from_db()
            self.assertFalse(p.inactiva)

    def test_ca_63_sin_contratos_activos_se_inactiva_y_se_reactiva(self):
        p = self.nueva_propiedad()
        self.contrato_directo(p, '2025-01-01', '2025-12-31', cerrado_en=AHORA)       # finalizado
        self.contrato_directo(p, '2026-01-01', '2026-01-31', anulado_en=AHORA, motivo_anulacion='Error')   # anulado
        services.marcar_inactiva(p.pk, actor='admin', ahora=AHORA)
        p.refresh_from_db()
        self.assertTrue(p.inactiva)
        self.assertEqual(selectors.estado_de_la_propiedad(p, HOY), selectors.INACTIVA)
        with self.assertRaises(ErrorDeValidacion):
            services.marcar_inactiva(p.pk, actor='admin', ahora=AHORA)
        services.reactivar_propiedad(p.pk, actor='admin', ahora=AHORA)
        p.refresh_from_db()
        self.assertFalse(p.inactiva)
        with self.assertRaises(ErrorDeValidacion):
            services.reactivar_propiedad(p.pk, actor='admin', ahora=AHORA)
        self.assertEqual(sorted(Auditoria.objects.filter(entidad='propiedad', registro_id=p.pk).values_list('accion', flat=True)),
                         ['propiedad_inactivada', 'propiedad_reactivada', 'propiedad_registrada'])

    def test_una_propiedad_inactiva_no_admite_contratos_nuevos(self):
        p = self.nueva_propiedad()
        services.marcar_inactiva(p.pk, actor='admin', ahora=AHORA)
        self.assertIn('inactiva', self.errores(propiedad=p)['propiedad'][0])
        services.reactivar_propiedad(p.pk, actor='admin', ahora=AHORA)
        self.crear(propiedad=p)

    def test_listar_busca_por_alias_y_direccion(self):
        services.registrar_propiedad(actor='admin', datos={'alias': 'Local centro', 'direccion': 'Avenida 2'}, ahora=AHORA)
        self.assertEqual([p.alias for p in selectors.listar_propiedades(busqueda='centro')], ['Local centro'])
        self.assertEqual([p.alias for p in selectors.listar_propiedades(busqueda='avenida')], ['Local centro'])
        self.assertEqual(selectors.listar_propiedades().count(), 2)


class CarrerasYEntradasRarasTests(Base):
    def test_dos_altas_con_el_mismo_alias_a_la_vez_dan_un_error_claro(self):
        with patch('alquileres.services._validar_propiedad', return_value={'alias': 'Casa 1', 'descripcion': '', 'direccion': ''}):
            with self.assertRaises(ErrorDeValidacion) as contexto:
                services.registrar_propiedad(actor='admin', datos={'alias': 'Casa 1'}, ahora=AHORA)
        self.assertIn('Ya existe', contexto.exception.errores['alias'][0])

    def test_dos_cambios_de_alias_a_la_vez_dan_un_error_claro(self):
        otra = self.nueva_propiedad('Casa 7')
        with patch('alquileres.services._validar_propiedad', return_value={'alias': 'Casa 1'}):
            with self.assertRaises(ErrorDeValidacion):
                services.actualizar_propiedad(otra.pk, actor='admin', datos={'alias': 'Casa 1'}, ahora=AHORA)

    def test_una_renovacion_que_choca_a_la_vez_la_ataja_la_base(self):
        primero = self.crear(fecha_inicio=d('2027-01-01'), fecha_fin=d('2027-06-30')).contrato
        self.crear(inquilino=self.nuevo_inquilino(), fecha_inicio=d('2027-07-01'), fecha_fin=d('2027-12-31'))
        with patch('alquileres.services._solapados', return_value=Contrato.objects.none()):
            with self.assertRaises(ErrorDeValidacion) as contexto:
                services.renovar_contrato(primero.pk, actor='admin', nueva_fecha_fin=d('2027-08-01'), motivo='Prórroga', ahora=AHORA)
        self.assertIn('solapan', contexto.exception.errores['fechas'][0])
        primero.refresh_from_db()
        self.assertEqual(primero.fecha_fin, d('2027-06-30'))

    def test_el_dia_de_vencimiento_y_los_dias_de_gracia_no_numericos_se_rechazan(self):
        for campo, valor in (('dia_vencimiento', 'abc'), ('dia_vencimiento', 5.5), ('dia_vencimiento', True), ('dia_vencimiento', 0),
                             ('dias_gracia', 'x'), ('dias_gracia', 400)):
            self.assertIn(campo, self.errores(**{campo: valor}), msg=(campo, valor))
        self.crear(dia_vencimiento='15', dias_gracia='10')   # un texto numérico se acepta


class CrearContratoTests(Base):
    def test_ca_02_se_guarda_con_su_condicion_inicial_y_su_auditoria(self):
        r = self.crear()
        c = r.contrato
        c.refresh_from_db()
        self.assertEqual((c.inquilino, c.propiedad, c.destino, c.moneda, c.fecha_inicio, c.fecha_fin),
                         (self.inquilino, self.propiedad, 'vivienda', 'CRC', d('2027-01-01'), None))
        cond = c.condiciones.get()
        self.assertEqual((cond.tipo, cond.monto_mensual, cond.dia_vencimiento, cond.dias_gracia, cond.vigente_desde),
                         ('inicial', Decimal('300000.00'), 5, 7, d('2027-01-01')))
        evento = Auditoria.objects.get(accion='contrato_creado', registro_id=c.pk)
        self.assertEqual((evento.actor, evento.ip_origen), ('admin', '203.0.113.5'))
        self.assertIn('monto_mensual', evento.campos_modificados)

    def test_por_omision_el_dia_de_vencimiento_es_el_de_inicio_y_la_gracia_es_siete(self):
        c = self.crear(fecha_inicio=d('2027-03-17'), dia_vencimiento=None, dias_gracia=None).contrato
        cond = c.condiciones.get()
        self.assertEqual((cond.dia_vencimiento, cond.dias_gracia), (17, 7))

    def test_el_monto_acepta_texto_y_decimal_pero_no_float_ni_mas_de_dos_decimales(self):
        self.crear(monto_mensual='450000.50')
        for monto, texto in ((0, 'mayor que cero'), ('-5', 'mayor que cero'), ('abc', 'número válido'), (300000.5, 'decimal binario'),
                             ('10.123', 'dos decimales'), ('NaN', 'número válido'), (None, 'número válido')):
            self.assertIn(texto, self.errores(propiedad=self.nueva_propiedad(), monto_mensual=monto)['monto_mensual'][0], msg=repr(monto))

    def test_dia_gracia_moneda_destino_y_fechas_se_validan_y_se_informan_todos_a_la_vez(self):
        errores = self.errores(dia_vencimiento=32, dias_gracia=-1, moneda='EUR', destino='comercio', fecha_inicio=None)
        self.assertEqual(sorted(errores), ['destino', 'dia_vencimiento', 'dias_gracia', 'fecha_inicio', 'moneda'])
        self.assertIn('anterior', self.errores(fecha_inicio=d('2027-02-01'), fecha_fin=d('2027-01-31'))['fecha_fin'][0])
        self.assertIn('no es válida', self.errores(fecha_inicio='2027-01-01')['fecha_inicio'][0])

    def test_un_error_no_guarda_nada(self):
        antes = (Contrato.objects.count(), Auditoria.objects.count())
        self.errores(monto_mensual=0)
        self.assertEqual((Contrato.objects.count(), Auditoria.objects.count()), antes)

    def test_ca_67_sin_consentimiento_vigente_se_rechaza(self):
        servicios_de_inquilinos.revocar_consentimiento(self.inquilino.pk, actor='admin', ahora=AHORA)
        self.assertIn('consentimiento vigente', self.errores()['consentimiento'][0])
        self.assertEqual(Contrato.objects.count(), 0)

    def test_ca_78_sin_el_frente_se_rechaza_y_con_el_frente_se_acepta(self):
        sin_frente = self.nuevo_inquilino(con_frente=False)
        self.assertIn('Falta el frente', self.errores(inquilino=sin_frente)['frente'][0])
        sin_frente.refresh_from_db()
        self.assertTrue(sin_frente.activo)    # el inquilino se conserva
        un_documento(sin_frente, cara='reverso')
        self.assertIn('frente', self.errores(inquilino=sin_frente))   # el reverso solo no basta
        un_documento(sin_frente)
        self.crear(inquilino=sin_frente)

    def test_un_inquilino_desactivado_o_desasociado_no_admite_contratos(self):
        servicios_de_inquilinos.desactivar_inquilino(self.inquilino.pk, actor='admin', ahora=AHORA)
        self.assertIn('desactivado', self.errores()['inquilino'][0])
        otro = self.nuevo_inquilino()
        from inquilinos.models import Inquilino
        Inquilino.objects.filter(pk=otro.pk).update(nombre_completo=None, numero_documento=None, telefono=None, correo=None,
                                                    desasociado_en=AHORA)
        self.assertIn('desasociado', self.errores(inquilino=otro)['inquilino'][0])

    def test_un_inquilino_inexistente_o_una_propiedad_inexistente_lanzan_does_not_exist(self):
        from inquilinos.models import Inquilino
        with self.assertRaises(Inquilino.DoesNotExist):
            services.crear_contrato(actor='admin', inquilino_id=999999, propiedad_id=self.propiedad.pk, datos=self.datos(), ahora=AHORA)
        with self.assertRaises(Propiedad.DoesNotExist):
            services.crear_contrato(actor='admin', inquilino_id=self.inquilino.pk, propiedad_id=999999, datos=self.datos(), ahora=AHORA)

    def test_ca_24_el_relevo_exige_el_dia_siguiente_al_fin(self):
        self.crear(fecha_inicio=d('2026-03-10'), fecha_fin=d('2027-03-09'))
        otro = self.nuevo_inquilino()
        mensaje = self.errores(inquilino=otro, fecha_inicio=d('2027-03-09'))['fechas'][0]
        self.assertIn('del 2026-03-10 al 2027-03-09', mensaje)   # la comprobación previa dice con qué contrato choca
        self.assertIn('solapan', self.errores(inquilino=otro, fecha_inicio=d('2025-01-01'), fecha_fin=d('2026-03-10'))['fechas'][0])
        self.crear(inquilino=otro, fecha_inicio=d('2027-03-10'))            # el día siguiente: se acepta
        self.crear(inquilino=otro, fecha_inicio=d('2025-01-01'), fecha_fin=d('2026-03-09'))   # y el anterior que termina antes

    def test_un_contrato_abierto_bloquea_cualquier_inicio_posterior(self):
        self.crear(fecha_inicio=d('2026-03-10'))
        self.assertIn('solapan', self.errores(fecha_inicio=d('2040-01-01'))['fechas'][0])

    def test_un_contrato_anulado_no_cuenta_para_el_solape(self):
        primero = self.crear(fecha_inicio=d('2026-03-10')).contrato
        services.anular_contrato(primero.pk, actor='admin', motivo='Error de captura', ahora=AHORA)
        self.crear(fecha_inicio=d('2026-03-10'))

    def test_la_base_es_la_ultima_defensa_contra_dos_contratos_a_la_vez(self):
        self.crear(fecha_inicio=d('2026-03-10'))
        with patch('alquileres.services._solapados', return_value=Contrato.objects.none()):   # la comprobación previa no los ve
            self.assertIn('solapan', self.errores(fecha_inicio=d('2026-04-01'))['fechas'][0])

    def test_la_vigencia_menor_de_tres_anos_solo_advierte(self):
        for fin, advierte in ((d('2029-12-31'), False), (d('2030-01-01'), False), (d('2029-12-30'), True), (d('2027-06-30'), True), (None, False)):
            propiedad = self.nueva_propiedad()
            r = self.crear(propiedad=propiedad, fecha_inicio=d('2027-01-01'), fecha_fin=fin)
            self.assertEqual(bool(r.advertencias), advierte, fin)
            self.assertIsNotNone(r.contrato.pk)

    def test_las_fechas_pueden_ser_anteriores_a_hoy_para_cargar_contratos_existentes(self):
        self.assertIsNotNone(self.crear(fecha_inicio=d('2024-05-31')).contrato.pk)


class FinalizarContratoTests(Base):
    def contrato_con_obligaciones(self, inicio='2027-01-01', cuantas=4, importe='300000.00', moneda='CRC'):
        contrato = self.crear(fecha_inicio=d(inicio), moneda=moneda).contrato
        return contrato, [obligacion_del_periodo(contrato, n, importe) for n in range(cuantas)]

    def finalizar(self, contrato, fin, **extra):
        return services.finalizar_contrato(contrato.pk, actor='admin', ip_origen='203.0.113.5', fecha_fin=d(fin), ahora=AHORA, **extra)

    def test_registra_el_fin_cierra_el_contrato_y_audita(self):
        contrato = self.crear().contrato
        r = self.finalizar(contrato, '2027-12-31')
        contrato.refresh_from_db()
        self.assertEqual((contrato.fecha_fin, contrato.cerrado_en), (d('2027-12-31'), AHORA))
        evento = Auditoria.objects.get(accion='contrato_finalizado')
        self.assertEqual(evento.ip_origen, '203.0.113.5')
        self.assertEqual(r.contrato, contrato)

    def test_ca_31_las_obligaciones_posteriores_al_fin_sin_movimientos_se_anulan_con_auditoria(self):
        contrato, obligaciones = self.contrato_con_obligaciones()
        r = self.finalizar(contrato, '2027-02-28')   # fin = último día del segundo período
        self.assertEqual(r.obligaciones_anuladas, 2)
        for obligacion in obligaciones:
            obligacion.refresh_from_db()
        self.assertEqual([o.anulada_en is not None for o in obligaciones], [False, False, True, True])
        self.assertIn('finalizado', obligaciones[2].motivo_anulacion)
        self.assertEqual(Auditoria.objects.filter(accion='obligacion_anulada').count(), 2)

    def test_las_obligaciones_con_movimientos_posteriores_al_fin_se_conservan(self):
        contrato, obligaciones = self.contrato_con_obligaciones()
        movimientos.usar(ConMovimientos('100000', obligaciones_con_pagos=[obligaciones[2].pk]))
        r = self.finalizar(contrato, '2027-02-28')
        self.assertEqual(r.obligaciones_anuladas, 1)
        obligaciones[2].refresh_from_db()
        self.assertIsNone(obligaciones[2].anulada_en)

    def test_ca_10_el_historial_se_conserva(self):
        contrato, obligaciones = self.contrato_con_obligaciones()
        self.finalizar(contrato, '2027-02-10')
        self.assertEqual(Obligacion.objects.filter(contrato=contrato).count(), 4)
        self.assertEqual(contrato.condiciones.count(), 1)
        self.assertEqual(Contrato.objects.filter(pk=contrato.pk).count(), 1)

    def test_el_ultimo_periodo_se_prorratea_con_un_ajuste_inmutable(self):
        contrato, obligaciones = self.contrato_con_obligaciones()
        r = self.finalizar(contrato, '2027-02-10')   # febrero tiene 28 días: 300000 × 10 / 28 = 107142,857 → 107143
        self.assertEqual(selectors.importe_vigente(obligaciones[1]), Decimal('107143.00'))
        self.assertEqual(r.ajuste.tipo, AjusteObligacion.PRORRATEO_FIN)
        self.assertEqual(r.ajuste.importe_delta, Decimal('-192857.00'))
        self.assertIn('10 de 28 días', r.ajuste.motivo)
        self.assertEqual(selectors.importe_vigente(obligaciones[0]), Decimal('300000.00'))   # el primero no cambia
        self.assertEqual(obligaciones[1].importe_inicial, Decimal('300000.00'))               # el inicial nunca cambia
        self.assertEqual(Auditoria.objects.filter(accion='ajuste_prorrateo_registrado').count(), 1)

    def test_si_el_fin_es_el_ultimo_dia_del_periodo_no_hay_prorrateo(self):
        contrato, obligaciones = self.contrato_con_obligaciones()
        r = self.finalizar(contrato, '2027-02-28')
        self.assertIsNone(r.ajuste)
        self.assertEqual(selectors.importe_vigente(obligaciones[1]), Decimal('300000.00'))

    def test_un_ajuste_con_delta_cero_no_se_registra(self):
        contrato, obligaciones = self.contrato_con_obligaciones(importe='1.00')
        r = self.finalizar(contrato, '2027-02-27')    # 27/28 de 1 colón redondea a 1
        self.assertIsNone(r.ajuste)
        self.assertEqual(AjusteObligacion.objects.count(), 0)

    def test_dolares_se_prorratean_a_dos_decimales(self):
        contrato, obligaciones = self.contrato_con_obligaciones(importe='500.00', moneda='USD')
        self.finalizar(contrato, '2027-01-10')        # 500 × 10 / 31 = 161,29
        self.assertEqual(selectors.importe_vigente(obligaciones[0]), Decimal('161.29'))

    def test_no_deja_el_importe_por_debajo_de_lo_abonado_y_no_cambia_nada(self):
        contrato, obligaciones = self.contrato_con_obligaciones()
        movimientos.usar(ConMovimientos('200000', obligaciones_con_pagos=[obligaciones[1].pk]))
        with self.assertRaises(ErrorDeValidacion) as contexto:
            self.finalizar(contrato, '2027-02-10')    # quedaría en 107143 < 200000
        self.assertIn('por debajo de lo ya abonado', contexto.exception.errores['fecha_fin'][0])
        contrato.refresh_from_db()
        self.assertIsNone(contrato.cerrado_en)
        self.assertEqual(AjusteObligacion.objects.count(), 0)
        self.assertFalse(Obligacion.objects.filter(contrato=contrato, anulada_en__isnull=False).exists())

    def test_no_se_cierra_dos_veces_ni_se_alarga_ni_se_acepta_antes_del_inicio(self):
        contrato = self.crear(fecha_fin=d('2028-12-31')).contrato
        for fin, texto in (('2026-12-31', 'anterior'), ('2029-01-01', 'renovar')):
            with self.assertRaises(ErrorDeValidacion) as contexto:
                self.finalizar(contrato, fin)
            self.assertIn(texto, contexto.exception.errores['fecha_fin'][0])
        self.finalizar(contrato, '2028-06-30')    # acortar sí
        with self.assertRaises(ErrorDeValidacion) as contexto:
            self.finalizar(contrato, '2028-03-31')
        self.assertIn('ya está cerrado', contexto.exception.errores['contrato'][0])

    def test_un_contrato_anulado_no_se_finaliza(self):
        contrato = self.crear().contrato
        services.anular_contrato(contrato.pk, actor='admin', motivo='Error', ahora=AHORA)
        with self.assertRaises(ErrorDeValidacion):
            self.finalizar(contrato, '2027-12-31')

    def test_advierte_si_el_fin_dista_menos_de_tres_meses_de_hoy_sin_bloquear(self):
        for fin, advierte in (('2027-01-25', True), ('2027-01-26', False), ('2026-09-01', True), ('2028-01-01', False)):
            contrato = self.crear(propiedad=self.nueva_propiedad(), fecha_inicio=d('2026-01-01')).contrato
            self.assertEqual(bool(self.finalizar(contrato, fin).advertencias), advierte, fin)

    def test_la_fecha_es_obligatoria_y_debe_ser_una_fecha(self):
        contrato = self.crear().contrato
        for fin in (None, '2027-12-31'):
            with self.assertRaises(ErrorDeValidacion):
                services.finalizar_contrato(contrato.pk, actor='admin', fecha_fin=fin, ahora=AHORA)

    def test_estado_finalizado_cuando_el_fin_pasa_y_vigente_mientras_no(self):
        contrato = self.crear(fecha_inicio=d('2026-01-01')).contrato
        self.finalizar(contrato, '2026-12-31')
        contrato.refresh_from_db()
        self.assertEqual(selectors.estado_del_contrato(contrato, d('2026-12-31')), selectors.VIGENTE)
        self.assertEqual(selectors.estado_del_contrato(contrato, d('2027-01-01')), selectors.FINALIZADO)


class RenovarContratoTests(Base):
    def renovar(self, contrato, fin, motivo='Prórroga acordada', **extra):
        return services.renovar_contrato(contrato.pk, actor='admin', ip_origen='203.0.113.5', nueva_fecha_fin=fin, motivo=motivo,
                                         ahora=AHORA, **extra)

    def test_ca_32_un_contrato_por_decidir_pasa_a_vigente_al_renovarlo(self):
        contrato = self.crear(fecha_inicio=d('2026-01-01'), fecha_fin=d('2026-06-30')).contrato
        self.assertEqual(selectors.estado_del_contrato(contrato, HOY), selectors.POR_DECIDIR)
        self.renovar(contrato, d('2027-06-30'))
        contrato.refresh_from_db()
        self.assertEqual((contrato.fecha_fin, selectors.estado_del_contrato(contrato, HOY)), (d('2027-06-30'), selectors.VIGENTE))
        evento = Auditoria.objects.get(accion='contrato_renovado')
        self.assertEqual((evento.valor_anterior['fecha_fin'], evento.valor_nuevo['fecha_fin']), ('2026-06-30', '2027-06-30'))
        self.assertEqual(evento.valor_nuevo['motivo'], 'Prórroga acordada')

    def test_se_puede_quitar_la_fecha_de_fin(self):
        contrato = self.crear(fecha_fin=d('2027-12-31')).contrato
        self.renovar(contrato, None)
        contrato.refresh_from_db()
        self.assertIsNone(contrato.fecha_fin)

    def test_rechazos(self):
        contrato = self.crear(fecha_fin=d('2027-12-31')).contrato
        casos = [(d('2027-12-31'), 'Prórroga', 'nueva_fecha_fin'), (d('2027-06-30'), 'Prórroga', 'nueva_fecha_fin'),
                 (d('2028-12-31'), '  ', 'motivo')]
        for fin, motivo, campo in casos:
            with self.assertRaises(ErrorDeValidacion, msg=campo) as contexto:
                self.renovar(contrato, fin, motivo)
            self.assertIn(campo, contexto.exception.errores)
        abierto = self.crear(propiedad=self.nueva_propiedad()).contrato
        with self.assertRaises(ErrorDeValidacion) as contexto:
            self.renovar(abierto, d('2030-01-01'))
        self.assertIn('ya es abierto', contexto.exception.errores['contrato'][0])

    def test_un_contrato_cerrado_o_anulado_no_se_renueva(self):
        cerrado = self.crear(fecha_fin=d('2027-12-31')).contrato
        services.finalizar_contrato(cerrado.pk, actor='admin', fecha_fin=d('2027-12-31'), ahora=AHORA)
        with self.assertRaises(ErrorDeValidacion) as contexto:
            self.renovar(cerrado, d('2028-12-31'))
        self.assertIn('cerrado', contexto.exception.errores['contrato'][0])
        anulado = self.crear(propiedad=self.nueva_propiedad(), fecha_fin=d('2027-12-31')).contrato
        services.anular_contrato(anulado.pk, actor='admin', motivo='Error', ahora=AHORA)
        with self.assertRaises(ErrorDeValidacion):
            self.renovar(anulado, d('2028-12-31'))

    def test_no_se_renueva_hasta_solapar_con_el_contrato_siguiente(self):
        primero = self.crear(fecha_inicio=d('2027-01-01'), fecha_fin=d('2027-06-30')).contrato
        self.crear(inquilino=self.nuevo_inquilino(), fecha_inicio=d('2027-07-01'), fecha_fin=d('2027-12-31'))
        with self.assertRaises(ErrorDeValidacion) as contexto:
            self.renovar(primero, d('2027-07-01'))
        self.assertIn('solapan', contexto.exception.errores['fechas'][0])
        with self.assertRaises(ErrorDeValidacion):
            self.renovar(primero, None)
        primero.refresh_from_db()
        self.assertEqual(primero.fecha_fin, d('2027-06-30'))


class AnularContratoTests(Base):
    def test_ca_62_anula_el_contrato_y_sus_obligaciones_y_libera_las_fechas(self):
        contrato = self.crear().contrato
        obligaciones = [obligacion_del_periodo(contrato, n) for n in range(3)]
        r = services.anular_contrato(contrato.pk, actor='admin', ip_origen='203.0.113.5', motivo='  Error de captura ', ahora=AHORA)
        contrato.refresh_from_db()
        self.assertEqual((contrato.anulado_en, contrato.motivo_anulacion, r.obligaciones_anuladas), (AHORA, 'Error de captura', 3))
        for o in obligaciones:
            o.refresh_from_db()
            self.assertIsNotNone(o.anulada_en)
        self.assertEqual(selectors.estado_del_contrato(contrato, HOY), selectors.ANULADO)
        self.crear(fecha_inicio=d('2027-01-01'))      # otro contrato puede ocupar esas fechas
        self.assertEqual(Auditoria.objects.filter(accion='contrato_anulado').count(), 1)
        self.assertEqual(Auditoria.objects.filter(accion='obligacion_anulada').count(), 3)

    def test_ca_62_con_movimientos_validos_se_rechaza_y_propone_finalizar(self):
        contrato = self.crear().contrato
        movimientos.usar(ConMovimientos(contrato_con_pagos=True))
        with self.assertRaises(ErrorDeValidacion) as contexto:
            services.anular_contrato(contrato.pk, actor='admin', motivo='Error', ahora=AHORA)
        self.assertIn('se finaliza', contexto.exception.errores['contrato'][0])
        contrato.refresh_from_db()
        self.assertIsNone(contrato.anulado_en)

    def test_ca_62_sin_motivo_no_se_anula_y_no_se_anula_dos_veces(self):
        contrato = self.crear().contrato
        for motivo in ('', '   ', None):
            with self.assertRaises(ErrorDeValidacion) as contexto:
                services.anular_contrato(contrato.pk, actor='admin', motivo=motivo, ahora=AHORA)
            self.assertIn('motivo', contexto.exception.errores)
        services.anular_contrato(contrato.pk, actor='admin', motivo='Error', ahora=AHORA)
        with self.assertRaises(ErrorDeValidacion):
            services.anular_contrato(contrato.pk, actor='admin', motivo='Otra vez', ahora=AHORA)


class SustituirInquilinoTests(Base):
    def sustituir(self, fin, inicio_nuevo, otro=None):
        return services.sustituir_inquilino(
            self.contrato.pk, actor='admin', fecha_fin=d(fin), inquilino_id=(otro or self.nuevo_inquilino()).pk,
            datos=self.datos(fecha_inicio=d(inicio_nuevo)), ahora=AHORA)

    def setUp(self):
        super().setUp()
        self.contrato = self.crear(fecha_inicio=d('2026-03-10')).contrato
        obligacion_del_periodo(self.contrato, 0)

    def test_ca_24_el_nuevo_empieza_el_dia_siguiente_y_ambos_conservan_su_historial(self):
        cierre, nuevo = self.sustituir('2027-03-09', '2027-03-10')
        self.contrato.refresh_from_db()
        self.assertEqual((self.contrato.fecha_fin, nuevo.contrato.propiedad), (d('2027-03-09'), self.propiedad))
        self.assertNotEqual(nuevo.contrato.inquilino, self.contrato.inquilino)
        self.assertEqual(self.contrato.obligaciones.count(), 1)
        self.assertEqual(Contrato.objects.filter(propiedad=self.propiedad).count(), 2)

    def test_ca_24_si_el_nuevo_empieza_el_mismo_dia_del_fin_se_rechaza_y_el_anterior_no_se_cierra(self):
        with self.assertRaises(ErrorDeValidacion) as contexto:
            self.sustituir('2027-03-09', '2027-03-09')
        self.assertIn('fechas', contexto.exception.errores)
        self.contrato.refresh_from_db()
        self.assertIsNone(self.contrato.fecha_fin)
        self.assertIsNone(self.contrato.cerrado_en)
        self.assertEqual(Contrato.objects.count(), 1)
        self.assertFalse(Auditoria.objects.filter(accion='contrato_finalizado').exists())

    def test_el_nuevo_inquilino_debe_tener_su_frente_y_su_consentimiento(self):
        with self.assertRaises(ErrorDeValidacion) as contexto:
            self.sustituir('2027-03-09', '2027-03-10', otro=self.nuevo_inquilino(con_frente=False))
        self.assertIn('frente', contexto.exception.errores)
        self.contrato.refresh_from_db()
        self.assertIsNone(self.contrato.cerrado_en)


class EstadosTests(Base):
    CASOS = [
        ('futuro', '2026-12-01', None, {}),
        ('vigente', '2026-01-01', None, {}),
        ('vigente', '2026-01-01', '2027-06-30', {}),
        ('vigente', '2026-01-01', '2026-10-26', {}),                       # el fin es hoy: aún vigente
        ('por_decidir', '2026-01-01', '2026-10-25', {}),
        ('finalizado', '2026-01-01', '2026-10-25', {'cerrado_en': AHORA}),
        ('vigente', '2026-01-01', '2027-06-30', {'cerrado_en': AHORA}),    # cerrado con fin futuro: aún vigente
        ('anulado', '2026-01-01', None, {'anulado_en': AHORA, 'motivo_anulacion': 'Error'}),
        ('anulado', '2026-12-01', None, {'anulado_en': AHORA, 'motivo_anulacion': 'Error'}),
    ]

    def test_el_estado_derivado_y_la_consulta_coinciden_en_todos_los_casos(self):
        for esperado, inicio, fin, extra in self.CASOS:
            contrato = self.contrato_directo(inicio=inicio, fin=fin, **extra)
            self.assertEqual(selectors.estado_del_contrato(contrato, HOY), esperado, (inicio, fin, extra))
            for estado in selectors.ESTADOS_DE_CONTRATO:
                en_consulta = selectors.contratos_en_estado(estado, hoy=HOY).filter(pk=contrato.pk).exists()
                self.assertEqual(en_consulta, estado == esperado, (esperado, estado, inicio, fin))

    def test_estado_de_la_propiedad_y_su_contrato_vigente(self):
        p = self.nueva_propiedad()
        self.assertEqual(selectors.estado_de_la_propiedad(p, HOY), selectors.DISPONIBLE)
        self.contrato_directo(p, '2026-12-01')                       # futuro: sigue disponible
        self.assertEqual(selectors.estado_de_la_propiedad(p, HOY), selectors.DISPONIBLE)
        self.assertIsNone(selectors.contrato_vigente_de_la_propiedad(p, HOY))
        otra = self.nueva_propiedad()
        vigente = self.contrato_directo(otra, '2026-01-01')
        self.assertEqual(selectors.estado_de_la_propiedad(otra, HOY), selectors.OCUPADA)
        self.assertEqual(selectors.contrato_vigente_de_la_propiedad(otra, HOY), vigente)

    def test_una_propiedad_con_un_contrato_por_decidir_sigue_ocupada(self):
        p = self.nueva_propiedad()
        self.contrato_directo(p, '2026-01-01', '2026-06-30')
        self.assertEqual(selectors.estado_de_la_propiedad(p, HOY), selectors.OCUPADA)


class BloqueoDeDesactivarTests(Base):
    """CA-29: el bloqueo real por contrato (el de saldos pendientes es de la E3)."""

    def hoy(self):
        return selectors.hoy_local()

    def test_un_inquilino_con_contrato_vigente_no_se_desactiva(self):
        self.contrato_con(self.inquilino, self.hoy() - timedelta(days=30), None)
        with self.assertRaises(NoSePuedeDesactivar) as contexto:
            servicios_de_inquilinos.desactivar_inquilino(self.inquilino.pk, actor='admin', ahora=AHORA)
        self.assertIn('contrato vigente', contexto.exception.motivos[0])
        self.assertIn('Casa 1', contexto.exception.motivos[0])
        self.inquilino.refresh_from_db()
        self.assertTrue(self.inquilino.activo)

    def contrato_con(self, inquilino, inicio, fin, **extra):
        return Contrato.objects.create(inquilino=inquilino, propiedad=self.propiedad, destino='vivienda', fecha_inicio=inicio,
                                       fecha_fin=fin, moneda='CRC', **extra)

    def test_futuro_o_por_decidir_tambien_bloquean(self):
        for inicio, fin in ((self.hoy() + timedelta(days=30), None), (self.hoy() - timedelta(days=90), self.hoy() - timedelta(days=1))):
            inquilino = self.nuevo_inquilino()
            self.contrato_con(inquilino, inicio, fin)
            self.propiedad = self.nueva_propiedad()
            with self.assertRaises(NoSePuedeDesactivar, msg=(inicio, fin)):
                servicios_de_inquilinos.desactivar_inquilino(inquilino.pk, actor='admin', ahora=AHORA)

    def test_con_el_contrato_finalizado_o_anulado_ya_se_desactiva(self):
        cerrado = self.nuevo_inquilino()
        self.contrato_con(cerrado, self.hoy() - timedelta(days=90), self.hoy() - timedelta(days=1), cerrado_en=AHORA)
        self.propiedad = self.nueva_propiedad()
        anulado = self.nuevo_inquilino()
        self.contrato_con(anulado, self.hoy() - timedelta(days=90), None, anulado_en=AHORA, motivo_anulacion='Error')
        for inquilino in (cerrado, anulado):
            servicios_de_inquilinos.desactivar_inquilino(inquilino.pk, actor='admin', ahora=AHORA)
            inquilino.refresh_from_db()
            self.assertFalse(inquilino.activo)

    def test_sin_contratos_se_desactiva_como_antes(self):
        servicios_de_inquilinos.desactivar_inquilino(self.inquilino.pk, actor='admin', ahora=AHORA)

    def test_finalizar_el_contrato_vencido_libera_al_inquilino(self):
        contrato = self.crear(fecha_inicio=self.hoy() - timedelta(days=200), fecha_fin=self.hoy() - timedelta(days=10)).contrato
        with self.assertRaises(NoSePuedeDesactivar):
            servicios_de_inquilinos.desactivar_inquilino(self.inquilino.pk, actor='admin', ahora=AHORA)
        services.finalizar_contrato(contrato.pk, actor='admin', fecha_fin=contrato.fecha_fin, ahora=AHORA)
        servicios_de_inquilinos.desactivar_inquilino(self.inquilino.pk, actor='admin', ahora=AHORA)


class ProveedorDeMovimientosTests(Base):
    def test_por_omision_no_hay_movimientos(self):
        contrato = self.crear().contrato
        obligacion = obligacion_del_periodo(contrato, 0)
        self.assertFalse(movimientos.obligacion_tiene_movimientos_validos(obligacion))
        self.assertFalse(movimientos.contrato_tiene_movimientos_validos(contrato))
        self.assertEqual(movimientos.abonos_validos(obligacion), Decimal('0'))

    def test_se_reemplaza_y_se_restablece(self):
        contrato = self.crear().contrato
        movimientos.usar(ConMovimientos(contrato_con_pagos=True))
        self.assertTrue(movimientos.contrato_tiene_movimientos_validos(contrato))
        movimientos.restablecer()
        self.assertFalse(movimientos.contrato_tiene_movimientos_validos(contrato))


class AuditoriaSinDatosPersonalesTests(Base):
    def test_ninguna_operacion_de_contrato_deja_datos_personales_en_la_auditoria(self):
        contrato = self.crear().contrato
        services.finalizar_contrato(contrato.pk, actor='admin', fecha_fin=d('2028-12-31'), ahora=AHORA)
        todo = str(list(Auditoria.objects.values()))
        for personal in (self.inquilino.nombre_completo, self.inquilino.numero_documento):
            self.assertNotIn(personal, todo)
