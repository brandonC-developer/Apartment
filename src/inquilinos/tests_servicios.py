"""Servicios y lecturas de la E1, grupo B (RF-01, RF-03, RF-04, RF-05; CA-01, CA-25, CA-29, CA-53). Necesitan PostgreSQL."""
from datetime import datetime, timedelta, timezone as utc
from unittest.mock import patch

from django.test import TestCase

from nucleo.models import Auditoria

from . import bloqueos, selectors, services
from .models import Consentimiento, DocumentoIdentidad, Inquilino, TextoConsentimiento
from .services import DocumentoDuplicado, ErrorDeValidacion, NoSePuedeDesactivar
from .tests import AHORA, un_documento, un_inquilino

DATOS = dict(nombre_completo='Nombre Apellido', tipo_documento='cedula', numero_documento='1-1111-1111')


class Base(TestCase):
    def setUp(self):
        self.texto = TextoConsentimiento.objects.create(version=1, contenido='Texto', vigente_desde=AHORA)

    def registrar(self, **extra):
        argumentos = dict(actor='admin', ip_origen='203.0.113.5', datos=dict(DATOS), texto=self.texto,
                          medio='fisico', ahora=AHORA)
        argumentos.update(extra)
        return services.registrar_inquilino(**argumentos)


class RegistrarTests(Base):
    def test_se_guarda_con_los_campos_obligatorios_y_el_consentimiento_sin_telefono_ni_correo(self):
        """CA-01."""
        i = self.registrar()
        i.refresh_from_db()
        self.assertIsNotNone(i.pk)
        self.assertEqual((i.nombre_completo, i.tipo_documento, i.numero_documento), ('Nombre Apellido', 'cedula', '1-1111-1111'))
        self.assertTrue(i.activo)
        self.assertIsNone(i.telefono)
        self.assertIsNone(i.correo)
        self.assertEqual(i.documentos.count(), 0)  # sin fotografía todavía
        c = i.consentimientos.get()
        self.assertEqual((c.texto, c.medio, c.otorgado_en, c.vigente), (self.texto, 'fisico', AHORA, True))

    def test_con_telefono_y_correo(self):
        i = self.registrar(datos=dict(DATOS, telefono='+506 8888-0000', correo=' persona@ejemplo.cr '))
        self.assertEqual((i.telefono, i.correo), ('+506 8888-0000', 'persona@ejemplo.cr'))

    def test_falta_un_campo_obligatorio_no_se_guarda_nada(self):
        for campo in ('nombre_completo', 'tipo_documento', 'numero_documento'):
            for vacio in ('', '   ', None):
                with self.assertRaises(ErrorDeValidacion, msg=f'{campo}={vacio!r}') as e:
                    self.registrar(datos=dict(DATOS, **{campo: vacio}))
                self.assertIn(campo, e.exception.errores)
        self.assertEqual((Inquilino.objects.count(), Consentimiento.objects.count(), Auditoria.objects.count()), (0, 0, 0))

    def test_sin_consentimiento_o_con_un_medio_o_fecha_invalidos_no_se_guarda(self):
        casos = [({'texto': None}, 'consentimiento'), ({'texto': 'version 1'}, 'consentimiento'),
                 ({'medio': 'verbal'}, 'medio'), ({'medio': None}, 'medio'),
                 ({'otorgado_en': AHORA + timedelta(days=1)}, 'otorgado_en')]
        for extra, campo in casos:
            with self.assertRaises(ErrorDeValidacion, msg=str(extra)) as e:
                self.registrar(**extra)
            self.assertIn(campo, e.exception.errores)
        self.assertEqual((Inquilino.objects.count(), Consentimiento.objects.count()), (0, 0))

    def test_formato_del_telefono_y_del_correo_y_largos(self):
        for campo, malo in (('telefono', 'abc'), ('telefono', '12345'), ('telefono', '8888-8888 ext 9'),
                            ('correo', 'sin-arroba'), ('correo', 'a@b'), ('correo', 'a' * 250 + '@ejemplo.cr'),
                            ('nombre_completo', 'x' * 201), ('numero_documento', '9' * 61)):
            with self.assertRaises(ErrorDeValidacion, msg=f'{campo}={malo}') as e:
                self.registrar(datos=dict(DATOS, **{campo: malo}))
            self.assertIn(campo, e.exception.errores)
        self.assertEqual(Inquilino.objects.count(), 0)

    def test_los_espacios_de_los_extremos_se_quitan(self):
        i = self.registrar(datos=dict(DATOS, nombre_completo='  Nombre Apellido  ', numero_documento=' 1-1111-1111 '))
        self.assertEqual((i.nombre_completo, i.numero_documento), ('Nombre Apellido', '1-1111-1111'))

    def test_el_documento_duplicado_advierte_antes_de_guardar_y_se_puede_confirmar(self):
        """CA-25."""
        primero = self.registrar()
        with self.assertRaises(DocumentoDuplicado) as e:
            self.registrar()
        self.assertEqual(e.exception.duplicados, [primero])
        self.assertEqual(Inquilino.objects.count(), 1)  # no se guardó
        segundo = self.registrar(confirmar_duplicado=True)
        self.assertEqual(Inquilino.objects.count(), 2)
        self.assertNotEqual(primero.pk, segundo.pk)

    def test_solo_cuentan_los_activos_del_mismo_tipo_y_numero(self):
        inactivo = self.registrar()
        Inquilino.objects.filter(pk=inactivo.pk).update(activo=False)
        self.registrar()  # el otro está inactivo: sin advertencia
        self.registrar(datos=dict(DATOS, tipo_documento='dimex'), confirmar_duplicado=False)  # otro tipo
        self.assertEqual(Inquilino.objects.count(), 3)

    def test_auditoria_sin_valores_personales_pero_con_lo_que_no_lo_es(self):
        """CA-53 en el registro."""
        self.registrar(datos=dict(DATOS, telefono='8888-8888', correo='persona@ejemplo.cr'))
        eventos = {a.accion: a for a in Auditoria.objects.all()}
        self.assertEqual(set(eventos), {'inquilino_registrado', 'consentimiento_otorgado'})
        r = eventos['inquilino_registrado']
        self.assertEqual((r.actor, r.ip_origen, r.entidad, r.ocurrido_en), ('admin', '203.0.113.5', 'inquilino', AHORA))
        self.assertEqual(set(r.campos_modificados),
                         {'nombre_completo', 'tipo_documento', 'numero_documento', 'telefono', 'correo', 'activo'})
        todo = str(list(Auditoria.objects.values()))
        for dato in ('Nombre Apellido', '1-1111-1111', '8888-8888', 'persona@ejemplo.cr'):
            self.assertNotIn(dato, todo)
        self.assertEqual(r.valor_nuevo, {'activo': True})
        self.assertEqual(eventos['consentimiento_otorgado'].valor_nuevo, {'texto_version': 1, 'medio': 'fisico'})

    def test_es_atomico_si_la_auditoria_falla_no_queda_nada(self):
        with patch('inquilinos.services.auditoria.registrar', side_effect=RuntimeError('falla')):
            with self.assertRaises(RuntimeError):
                self.registrar()
        self.assertEqual((Inquilino.objects.count(), Consentimiento.objects.count(), Auditoria.objects.count()), (0, 0, 0))


class ActualizarTests(Base):
    def setUp(self):
        super().setUp()
        self.inquilino = self.registrar(datos=dict(DATOS, telefono='8888-8888'))
        Auditoria.objects.all()  # el registro ya dejó sus dos eventos
        self.antes = Auditoria.objects.count()

    def actualizar(self, **datos):
        return services.actualizar_inquilino(self.inquilino.pk, actor='admin', ip_origen='203.0.113.5', datos=datos,
                                             ahora=AHORA + timedelta(hours=1))

    def test_cambiar_el_telefono_deja_que_cambio_quien_y_cuando_pero_no_los_valores(self):
        """CA-53."""
        self.actualizar(telefono='7777-7777')
        r = Auditoria.objects.get(accion='inquilino_actualizado')
        self.assertEqual((r.campos_modificados, r.actor, r.ocurrido_en, r.registro_id),
                         (['telefono'], 'admin', AHORA + timedelta(hours=1), self.inquilino.pk))
        self.assertIsNone(r.valor_anterior)
        self.assertIsNone(r.valor_nuevo)
        self.assertNotIn('8888', str(list(Auditoria.objects.values())))
        self.assertNotIn('7777', str(list(Auditoria.objects.values())))
        self.inquilino.refresh_from_db()
        self.assertEqual(self.inquilino.telefono, '7777-7777')

    def test_sin_cambios_no_se_escribe_nada_ni_se_audita(self):
        self.actualizar(telefono='8888-8888', nombre_completo='Nombre Apellido')
        self.assertEqual(Auditoria.objects.count(), self.antes)

    def test_se_puede_borrar_el_telefono(self):
        self.actualizar(telefono='')
        self.inquilino.refresh_from_db()
        self.assertIsNone(self.inquilino.telefono)

    def test_solo_se_validan_los_campos_enviados(self):
        self.actualizar(nombre_completo='Otro Nombre')
        with self.assertRaises(ErrorDeValidacion) as e:
            self.actualizar(correo='malo')
        self.assertEqual(set(e.exception.errores), {'correo'})
        with self.assertRaises(ErrorDeValidacion):
            self.actualizar(nombre_completo='   ')
        self.inquilino.refresh_from_db()
        self.assertEqual(self.inquilino.nombre_completo, 'Otro Nombre')

    def test_un_campo_ajeno_se_rechaza(self):
        for campo in ('activo', 'desasociado_en', 'id'):
            with self.assertRaises(ValueError):
                self.actualizar(**{campo: 1})

    def test_cambiar_la_identificacion_a_la_de_otro_activo_advierte_y_se_puede_confirmar(self):
        otro = self.registrar(datos=dict(DATOS, numero_documento='2-2222-2222'))
        with self.assertRaises(DocumentoDuplicado) as e:
            self.actualizar(numero_documento='2-2222-2222')
        self.assertEqual(e.exception.duplicados, [otro])
        self.inquilino.refresh_from_db()
        self.assertEqual(self.inquilino.numero_documento, '1-1111-1111')
        services.actualizar_inquilino(self.inquilino.pk, actor='admin', datos={'numero_documento': '2-2222-2222'},
                                      confirmar_duplicado=True)
        self.inquilino.refresh_from_db()
        self.assertEqual(self.inquilino.numero_documento, '2-2222-2222')

    def test_no_se_advierte_contra_si_mismo(self):
        self.actualizar(tipo_documento='cedula', nombre_completo='Nuevo Nombre')
        self.actualizar(numero_documento='1-1111-1111')  # mismo valor: sin cambio

    def test_un_desasociado_no_se_modifica(self):
        Inquilino.objects.filter(pk=self.inquilino.pk).update(
            nombre_completo=None, numero_documento=None, telefono=None, correo=None, desasociado_en=AHORA)
        with self.assertRaises(ErrorDeValidacion):
            self.actualizar(nombre_completo='Otro')

    def test_la_actualizacion_es_atomica(self):
        with patch('inquilinos.services.auditoria.registrar', side_effect=RuntimeError('falla')):
            with self.assertRaises(RuntimeError):
                self.actualizar(telefono='7777-7777')
        self.inquilino.refresh_from_db()
        self.assertEqual(self.inquilino.telefono, '8888-8888')


class DesactivarTests(Base):
    def setUp(self):
        super().setUp()
        self.inquilino = self.registrar()
        self.addCleanup(lambda: [bloqueos.quitar(f) for f in list(bloqueos._comprobaciones)])

    def desactivar(self):
        return services.desactivar_inquilino(self.inquilino.pk, actor='admin', ip_origen='203.0.113.5', ahora=AHORA)

    def test_sin_motivos_de_bloqueo_se_desactiva_sin_borrar_nada_y_se_audita(self):
        un_documento(self.inquilino)
        self.desactivar()
        self.inquilino.refresh_from_db()
        self.assertFalse(self.inquilino.activo)
        self.assertEqual((self.inquilino.consentimientos.count(), self.inquilino.documentos.count()), (1, 1))  # historial
        r = Auditoria.objects.get(accion='inquilino_desactivado')
        self.assertEqual((r.valor_anterior, r.valor_nuevo, r.campos_modificados), ({'activo': True}, {'activo': False}, ['activo']))

    def test_un_motivo_de_bloqueo_lo_impide_y_no_deja_rastro(self):
        """CA-29, el mecanismo: la E2 y la E3 registran las comprobaciones reales."""
        bloqueos.registrar(lambda inquilino: ['Tiene un contrato vigente.'])
        antes = Auditoria.objects.count()
        with self.assertRaises(NoSePuedeDesactivar) as e:
            self.desactivar()
        self.assertEqual(e.exception.motivos, ['Tiene un contrato vigente.'])
        self.inquilino.refresh_from_db()
        self.assertTrue(self.inquilino.activo)
        self.assertEqual(Auditoria.objects.count(), antes)

    def test_los_motivos_de_varias_comprobaciones_se_juntan(self):
        bloqueos.registrar(lambda i: ['Contrato vigente.'])
        bloqueos.registrar(lambda i: [])
        bloqueos.registrar(lambda i: ['Saldos pendientes.'])
        with self.assertRaises(NoSePuedeDesactivar) as e:
            self.desactivar()
        self.assertEqual(e.exception.motivos, ['Contrato vigente.', 'Saldos pendientes.'])

    def test_la_comprobacion_recibe_al_inquilino_y_registrarla_dos_veces_no_la_duplica(self):
        recibidos = []

        def comprobacion(inquilino):
            recibidos.append(inquilino.pk)
            return []
        bloqueos.registrar(comprobacion)
        bloqueos.registrar(comprobacion)
        self.desactivar()
        self.assertEqual(recibidos, [self.inquilino.pk])

    def test_ya_desactivado_y_reactivar(self):
        self.desactivar()
        with self.assertRaises(ErrorDeValidacion):
            self.desactivar()
        services.reactivar_inquilino(self.inquilino.pk, actor='admin')
        self.inquilino.refresh_from_db()
        self.assertTrue(self.inquilino.activo)
        self.assertEqual(Auditoria.objects.filter(accion='inquilino_reactivado').count(), 1)
        with self.assertRaises(ErrorDeValidacion):
            services.reactivar_inquilino(self.inquilino.pk, actor='admin')

    def test_reactivar_advierte_si_otro_activo_usa_ahora_el_documento(self):
        self.desactivar()
        otro = self.registrar()
        with self.assertRaises(DocumentoDuplicado) as e:
            services.reactivar_inquilino(self.inquilino.pk, actor='admin')
        self.assertEqual(e.exception.duplicados, [otro])
        services.reactivar_inquilino(self.inquilino.pk, actor='admin', confirmar_duplicado=True)

    def test_un_desasociado_no_se_reactiva(self):
        Inquilino.objects.filter(pk=self.inquilino.pk).update(
            activo=False, nombre_completo=None, numero_documento=None, telefono=None, correo=None, desasociado_en=AHORA)
        with self.assertRaises(ErrorDeValidacion):
            services.reactivar_inquilino(self.inquilino.pk, actor='admin')


class LecturasTests(Base):
    def setUp(self):
        super().setUp()
        self.ana = self.registrar(datos=dict(DATOS, nombre_completo='Ana Mora', numero_documento='1-0001', telefono='8888-1111',
                                             correo='ana@ejemplo.cr'))
        self.beto = self.registrar(datos=dict(DATOS, nombre_completo='Beto Solís', numero_documento='2-0002'))
        self.carla = self.registrar(datos=dict(DATOS, nombre_completo='Carla Vega', numero_documento='3-0003'))
        un_documento(self.ana, 'frente')
        un_documento(self.beto, 'reverso')  # solo reverso: cuenta como «sin frente»

    def nombres(self, **filtros):
        return [i.nombre_completo for i in selectors.listar_inquilinos(**filtros)]

    def test_lista_por_defecto_los_activos_en_orden_y_con_tiene_frente(self):
        lista = list(selectors.listar_inquilinos())
        self.assertEqual([i.nombre_completo for i in lista], ['Ana Mora', 'Beto Solís', 'Carla Vega'])
        self.assertEqual([i.tiene_frente for i in lista], [True, False, False])

    def test_una_sola_consulta(self):
        with self.assertNumQueries(1):
            list(selectors.listar_inquilinos(busqueda='a', sin_frente=True))

    def test_busca_por_nombre_documento_telefono_y_correo_sin_distinguir_mayusculas(self):
        self.assertEqual(self.nombres(busqueda='ANA'), ['Ana Mora'])
        self.assertEqual(self.nombres(busqueda='2-0002'), ['Beto Solís'])
        self.assertEqual(self.nombres(busqueda='8888'), ['Ana Mora'])
        self.assertEqual(self.nombres(busqueda='ejemplo.cr'), ['Ana Mora'])
        self.assertEqual(self.nombres(busqueda='  vega '), ['Carla Vega'])
        self.assertEqual(self.nombres(busqueda='nadie'), [])
        self.assertEqual(len(self.nombres(busqueda='')), 3)

    def test_la_busqueda_no_es_inyectable(self):
        self.assertEqual(self.nombres(busqueda="'; DROP TABLE inquilinos_inquilino; --"), [])
        self.assertEqual(Inquilino.objects.count(), 3)

    def test_filtro_sin_frente_incluye_al_que_solo_tiene_reverso_y_a_quien_no_tiene_nada(self):
        self.assertEqual(self.nombres(sin_frente=True), ['Beto Solís', 'Carla Vega'])
        self.assertEqual(self.nombres(sin_frente=True, busqueda='carla'), ['Carla Vega'])

    def test_un_frente_reemplazado_y_eliminado_deja_al_inquilino_sin_frente(self):
        DocumentoIdentidad.objects.filter(inquilino=self.ana, cara='frente').update(eliminado_en=AHORA)
        self.assertEqual(self.nombres(sin_frente=True), ['Ana Mora', 'Beto Solís', 'Carla Vega'])
        un_documento(self.ana, 'frente')
        self.assertEqual(self.nombres(sin_frente=True), ['Beto Solís', 'Carla Vega'])

    def test_estados_y_desasociados(self):
        services.desactivar_inquilino(self.carla.pk, actor='admin')
        self.assertEqual(self.nombres(), ['Ana Mora', 'Beto Solís'])
        self.assertEqual(self.nombres(estado='inactivos'), ['Carla Vega'])
        self.assertEqual(len(self.nombres(estado='todos')), 3)
        Inquilino.objects.filter(pk=self.beto.pk).update(
            nombre_completo=None, numero_documento=None, telefono=None, correo=None, desasociado_en=AHORA)
        self.assertEqual(self.nombres(estado='todos'), ['Ana Mora', 'Carla Vega'])
        with self.assertRaises(ValueError):
            selectors.listar_inquilinos(estado='otros')

    def test_ficha(self):
        ficha = selectors.obtener_ficha(self.ana.pk)
        self.assertEqual(ficha['inquilino'], self.ana)
        self.assertEqual(ficha['consentimiento'].texto, self.texto)
        self.assertFalse(ficha['falta_frente'])
        self.assertEqual(ficha['frente'].cara, 'frente')
        self.assertIsNone(ficha['reverso'])
        ficha = selectors.obtener_ficha(self.beto.pk)
        self.assertTrue(ficha['falta_frente'])
        self.assertIsNone(ficha['frente'])
        self.assertEqual(ficha['reverso'].cara, 'reverso')
        with self.assertRaises(Inquilino.DoesNotExist):
            selectors.obtener_ficha(999999)

    def test_la_ficha_solo_muestra_las_fotografias_activas_y_el_ultimo_consentimiento(self):
        DocumentoIdentidad.objects.filter(inquilino=self.ana, cara='frente').update(eliminado_en=AHORA)
        nuevo = un_documento(self.ana, 'frente', referencia_archivo='nueva')
        segundo = TextoConsentimiento.objects.create(version=2, contenido='v2', vigente_desde=AHORA)
        Consentimiento.objects.create(inquilino=self.ana, texto=segundo, medio='electronico',
                                      otorgado_en=AHORA + timedelta(days=1))
        ficha = selectors.obtener_ficha(self.ana.pk)
        self.assertEqual(ficha['frente'], nuevo)
        self.assertEqual(ficha['consentimiento'].texto, segundo)
        self.assertEqual(len(ficha['consentimientos']), 2)

    def test_texto_vigente_es_la_version_mas_reciente(self):
        self.assertEqual(selectors.texto_vigente(), self.texto)
        nuevo = TextoConsentimiento.objects.create(version=3, contenido='v3', vigente_desde=AHORA)
        TextoConsentimiento.objects.create(version=2, contenido='v2', vigente_desde=AHORA)
        self.assertEqual(selectors.texto_vigente(), nuevo)
        TextoConsentimiento.objects.all()  # sin versiones no hay texto: se prueba en la ficha de registro (grupo C)
