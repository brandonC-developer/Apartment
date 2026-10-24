"""Modelos de la E1 (grupo A): restricciones del modelo de datos v0.7 y protección de las filas. Necesitan PostgreSQL."""
from datetime import datetime, timedelta, timezone as utc

from django.db import IntegrityError, connection, transaction
from django.test import TestCase
from django.utils import timezone

from nucleo.models import RegistroInmutable

from .models import (
    TAMANO_MAXIMO, AccesoDocumento, Consentimiento, DocumentoIdentidad, Inquilino, TextoConsentimiento)

AHORA = datetime(2026, 10, 24, 12, 0, 0, tzinfo=utc.utc)


def un_inquilino(**extra):
    datos = dict(nombre_completo='Nombre Apellido', tipo_documento='cedula', numero_documento='1-1111-1111')
    datos.update(extra)
    return Inquilino.objects.create(**datos)


def un_documento(inquilino, cara='frente', n=[0], **extra):
    n[0] += 1
    datos = dict(inquilino=inquilino, cara=cara, referencia_archivo=f'ref-{n[0]}', tipo_real_archivo='image/jpeg',
                 tamano_bytes=1000)
    datos.update(extra)
    return DocumentoIdentidad.objects.create(**datos)


class InquilinoTests(TestCase):
    def test_se_guarda_con_los_datos_obligatorios_y_sin_telefono_ni_correo(self):
        i = un_inquilino()
        i.refresh_from_db()
        self.assertTrue(i.activo)
        self.assertIsNone(i.telefono)
        self.assertIsNone(i.correo)
        self.assertEqual(str(i), 'Nombre Apellido')

    def test_nombre_y_numero_de_documento_son_obligatorios(self):
        for extra in (dict(nombre_completo=None), dict(nombre_completo=''), dict(numero_documento=None),
                      dict(numero_documento='')):
            with self.assertRaises(IntegrityError, msg=str(extra)), transaction.atomic():
                un_inquilino(**extra)

    def test_el_tipo_de_documento_debe_ser_uno_de_los_cuatro(self):
        for tipo in ('cedula', 'dimex', 'pasaporte', 'otro'):
            un_inquilino(tipo_documento=tipo, numero_documento=tipo)
        with self.assertRaises(IntegrityError), transaction.atomic():
            un_inquilino(tipo_documento='licencia')

    def test_un_documento_repetido_no_se_bloquea_en_la_base_es_una_advertencia(self):
        un_inquilino()
        un_inquilino()  # RF-01 / CA-25: advertencia en el servicio, no restricción de la tabla
        self.assertEqual(Inquilino.objects.count(), 2)

    def test_un_inquilino_desasociado_no_conserva_datos_personales(self):
        i = un_inquilino()
        Inquilino.objects.filter(pk=i.pk).update(
            nombre_completo=None, numero_documento=None, telefono=None, correo=None, desasociado_en=AHORA)
        i.refresh_from_db()
        self.assertEqual(str(i), f'Inquilino {i.pk} (desasociado)')
        for campo in ('nombre_completo', 'numero_documento', 'telefono', 'correo'):
            with self.assertRaises(IntegrityError, msg=campo), transaction.atomic():
                Inquilino.objects.filter(pk=i.pk).update(**{campo: 'dato'})

    def test_un_inquilino_no_desasociado_no_puede_perder_su_nombre(self):
        i = un_inquilino()
        with self.assertRaises(IntegrityError), transaction.atomic():
            Inquilino.objects.filter(pk=i.pk).update(nombre_completo=None)


class TextoYConsentimientoTests(TestCase):
    def setUp(self):
        self.inquilino = un_inquilino()
        self.texto = TextoConsentimiento.objects.create(version=1, contenido='Texto de prueba', vigente_desde=AHORA)

    def test_cada_version_es_unica_y_con_contenido_y_nace_como_borrador(self):
        self.assertTrue(self.texto.borrador)
        self.assertIn('borrador sin validar', str(self.texto))
        with self.assertRaises(IntegrityError), transaction.atomic():
            TextoConsentimiento.objects.create(version=1, contenido='otro', vigente_desde=AHORA)
        with self.assertRaises(IntegrityError), transaction.atomic():
            TextoConsentimiento.objects.create(version=2, contenido='', vigente_desde=AHORA)
        validado = TextoConsentimiento.objects.create(version=2, contenido='validado', borrador=False, vigente_desde=AHORA)
        self.assertEqual(str(validado), 'Versión 2')

    def test_una_version_del_texto_no_se_edita_ni_se_borra(self):
        self.texto.contenido = 'cambiado'
        with self.assertRaises(RegistroInmutable):
            self.texto.save()
        with self.assertRaises(RegistroInmutable):
            self.texto.save(update_fields=['contenido'])
        with self.assertRaises(RegistroInmutable):
            self.texto.delete()
        with self.assertRaises(RegistroInmutable):
            TextoConsentimiento.objects.all().update(contenido='x')
        with self.assertRaises(RegistroInmutable):
            TextoConsentimiento.objects.all().delete()
        self.assertEqual(TextoConsentimiento.objects.get().contenido, 'Texto de prueba')

    def test_el_consentimiento_apunta_a_la_version_mostrada_y_no_deja_borrar_la_version(self):
        c = Consentimiento.objects.create(inquilino=self.inquilino, texto=self.texto, medio='fisico', otorgado_en=AHORA)
        self.assertTrue(c.vigente)
        with self.assertRaises(RegistroInmutable):
            self.texto.delete()
        with self.assertRaises(IntegrityError), transaction.atomic():
            TextoConsentimiento.objects.filter(pk=self.texto.pk)._raw_delete(TextoConsentimiento.objects.db)
            connection.check_constraints()  # las claves foráneas de Django se comprueban al confirmar

    def test_el_medio_es_fisico_o_electronico(self):
        for medio in ('fisico', 'electronico'):
            Consentimiento.objects.create(inquilino=self.inquilino, texto=self.texto, medio=medio, otorgado_en=AHORA)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Consentimiento.objects.create(inquilino=self.inquilino, texto=self.texto, medio='verbal', otorgado_en=AHORA)

    def test_solo_se_puede_registrar_la_revocacion_y_no_antes_del_consentimiento(self):
        c = Consentimiento.objects.create(inquilino=self.inquilino, texto=self.texto, medio='fisico', otorgado_en=AHORA)
        c.medio = 'electronico'
        with self.assertRaises(RegistroInmutable):
            c.save()
        with self.assertRaises(RegistroInmutable):
            c.save(update_fields=['medio'])
        with self.assertRaises(RegistroInmutable):
            Consentimiento.objects.filter(pk=c.pk).update(medio='electronico')
        with self.assertRaises(RegistroInmutable):
            c.delete()
        c.refresh_from_db()
        c.revocado_en = AHORA - timedelta(days=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            c.save(update_fields=['revocado_en'])
        c.refresh_from_db()
        c.revocado_en = AHORA + timedelta(days=1)
        c.save(update_fields=['revocado_en'])
        c.refresh_from_db()
        self.assertFalse(c.vigente)


class DocumentoIdentidadTests(TestCase):
    def setUp(self):
        self.inquilino = un_inquilino()

    def test_una_sola_fotografia_activa_por_cara(self):
        frente = un_documento(self.inquilino, 'frente')
        un_documento(self.inquilino, 'reverso')  # el reverso es otra cara
        with self.assertRaises(IntegrityError), transaction.atomic():
            un_documento(self.inquilino, 'frente')
        frente.eliminado_en = timezone.now()
        frente.save(update_fields=['eliminado_en'])
        nueva = un_documento(self.inquilino, 'frente')  # reemplazo: la anterior ya está eliminada
        self.assertTrue(nueva.activo)
        self.assertFalse(DocumentoIdentidad.objects.get(pk=frente.pk).activo)
        self.assertEqual(DocumentoIdentidad.objects.filter(inquilino=self.inquilino, eliminado_en__isnull=True).count(), 2)

    def test_dos_inquilinos_pueden_tener_su_propio_frente(self):
        un_documento(self.inquilino, 'frente')
        un_documento(un_inquilino(numero_documento='2'), 'frente')

    def test_peso_y_tipo_real_son_los_de_r27(self):
        for peso in (1, TAMANO_MAXIMO):
            un_documento(self.inquilino, 'reverso', tamano_bytes=peso, eliminado_en=AHORA)
        for peso in (0, TAMANO_MAXIMO + 1):
            with self.assertRaises(IntegrityError, msg=str(peso)), transaction.atomic():
                un_documento(self.inquilino, 'reverso', tamano_bytes=peso)
        un_documento(self.inquilino, 'reverso', tipo_real_archivo='image/png', eliminado_en=AHORA)
        for tipo in ('image/gif', 'application/pdf', 'text/html', ''):
            with self.assertRaises(IntegrityError, msg=tipo), transaction.atomic():
                un_documento(self.inquilino, 'reverso', tipo_real_archivo=tipo)

    def test_la_cara_es_frente_o_reverso(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            un_documento(self.inquilino, 'lateral')

    def test_la_referencia_del_archivo_no_se_repite(self):
        un_documento(self.inquilino, 'frente', referencia_archivo='igual')
        with self.assertRaises(IntegrityError), transaction.atomic():
            un_documento(self.inquilino, 'reverso', referencia_archivo='igual')

    def test_solo_se_puede_marcar_como_eliminado(self):
        d = un_documento(self.inquilino)
        d.tamano_bytes = 5
        with self.assertRaises(RegistroInmutable):
            d.save()
        with self.assertRaises(RegistroInmutable):
            d.save(update_fields=['tamano_bytes'])
        with self.assertRaises(RegistroInmutable):
            DocumentoIdentidad.objects.filter(pk=d.pk).update(referencia_archivo='otra')
        with self.assertRaises(RegistroInmutable):
            d.delete()
        with self.assertRaises(RegistroInmutable):
            DocumentoIdentidad.objects.all().delete()
        DocumentoIdentidad.objects.filter(pk=d.pk).update(eliminado_en=AHORA)
        self.assertFalse(DocumentoIdentidad.objects.get(pk=d.pk).activo)

    def test_no_se_puede_borrar_al_inquilino_con_documentos_ni_consentimientos(self):
        un_documento(self.inquilino)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Inquilino.objects.filter(pk=self.inquilino.pk)._raw_delete(Inquilino.objects.db)
            connection.check_constraints()


class AccesoDocumentoTests(TestCase):
    def setUp(self):
        self.documento = un_documento(un_inquilino())

    def test_registra_quien_cuando_y_que_accion_sin_la_imagen(self):
        a = AccesoDocumento.objects.create(documento=self.documento, actor='admin', accion='consulta', ocurrido_en=AHORA)
        a.refresh_from_db()
        self.assertEqual((a.actor, a.accion, a.ocurrido_en), ('admin', 'consulta', AHORA))
        campos = {f.name for f in AccesoDocumento._meta.get_fields()}
        self.assertEqual(campos, {'id', 'documento', 'actor', 'accion', 'ocurrido_en'})  # ningún campo de contenido

    def test_la_accion_es_consulta_o_descarga(self):
        AccesoDocumento.objects.create(documento=self.documento, actor='a', accion='descarga', ocurrido_en=AHORA)
        with self.assertRaises(IntegrityError), transaction.atomic():
            AccesoDocumento.objects.create(documento=self.documento, actor='a', accion='copia', ocurrido_en=AHORA)

    def test_solo_insercion(self):
        a = AccesoDocumento.objects.create(documento=self.documento, actor='a', accion='consulta', ocurrido_en=AHORA)
        a.actor = 'otro'
        for operacion in (a.save, lambda: a.save(update_fields=['actor']), a.delete,
                          lambda: AccesoDocumento.objects.all().update(actor='x'),
                          lambda: AccesoDocumento.objects.all().delete()):
            with self.assertRaises(RegistroInmutable):
                operacion()
        self.assertEqual(AccesoDocumento.objects.get().actor, 'a')
