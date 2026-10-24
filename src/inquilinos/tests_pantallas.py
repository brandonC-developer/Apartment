"""Pantallas de los inquilinos (RF-01, RF-03, RF-04, RF-05, RF-39; CA-01, CA-25, CA-29, CA-67). Necesitan PostgreSQL."""
import re
import tempfile
from unittest.mock import patch
from datetime import timedelta

from django.test import Client, override_settings
from django.utils import timezone

from nucleo.models import Auditoria

from . import bloqueos, services
from .models import Consentimiento, DocumentoIdentidad, Inquilino, TextoConsentimiento
from .tests import AHORA
from .tests_fotografias import Navegador, a_bytes, degradado
from .tests_servicios import DATOS


class Pantallas(Navegador):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.enterContext(override_settings(RAIZ_DOCUMENTOS=carpeta.name))
        self.texto = TextoConsentimiento.objects.create(
            version=1, contenido='Primera línea\nSegunda línea', borrador=True, vigente_desde=AHORA)
        self.entrar()

    def registrar(self, **cambios):
        datos = {**DATOS, **cambios}
        return services.registrar_inquilino(actor='admin', datos=datos, texto=self.texto, medio='fisico', ahora=AHORA)

    def formulario(self, **cambios):
        return {**DATOS, 'telefono': '', 'correo': '', 'medio': 'fisico', 'otorgado_en': '', 'confirma': '1', **cambios}


class ListaTests(Pantallas):
    def test_lista_con_busqueda_estado_y_sin_frente(self):
        ana = self.registrar(nombre_completo='Ana Mora', numero_documento='1-0001', correo='ana@ejemplo.cr')
        beto = self.registrar(nombre_completo='Beto Solano', numero_documento='2-0002', telefono='8888 0000')
        services.subir_fotografia(ana.pk, cara='frente', contenido=a_bytes(degradado(), 'JPEG'), actor='admin')
        services.desactivar_inquilino(beto.pk, actor='admin')
        html = self.client.get('/inquilinos/').content.decode()
        self.assertIn('Ana Mora', html)
        self.assertNotIn('Beto Solano', html)
        self.assertIn('Con frente', html)
        self.assertIn('Beto Solano', self.client.get('/inquilinos/?estado=inactivos').content.decode())
        self.assertIn('Sin frente', self.client.get('/inquilinos/?estado=todos').content.decode())
        solo_sin_frente = self.client.get('/inquilinos/?estado=todos&sin_frente=1').content.decode()
        self.assertIn('Beto Solano', solo_sin_frente)
        self.assertNotIn('Ana Mora', solo_sin_frente)
        self.assertIn('Ana Mora', self.client.get('/inquilinos/?q=ana@ejemplo').content.decode())
        self.assertIn('Ningún inquilino coincide', self.client.get('/inquilinos/?q=zzzz').content.decode())

    def test_un_estado_desconocido_cae_en_activos_y_no_da_error(self):
        self.registrar()
        r = self.client.get('/inquilinos/?estado=cualquiera&pagina=abc')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Nombre Apellido', r.content.decode())

    def test_el_nombre_se_escapa(self):
        self.registrar(nombre_completo='<script>alert(1)</script>')
        html = self.client.get('/inquilinos/').content.decode()
        self.assertNotIn('<script>alert', html)
        self.assertIn('&lt;script&gt;', html)

    def test_pagina_de_cincuenta(self):
        for n in range(53):
            self.registrar(nombre_completo=f'Persona {n:02d}', numero_documento=f'9-{n:04d}')
        r = self.client.get('/inquilinos/')
        self.assertEqual(len(re.findall(r'<tr>\s*<th scope="row">', r.content.decode())), 50)
        self.assertIn('Página 1 de 2', r.content.decode())
        self.assertIn('Persona 52', self.client.get('/inquilinos/?pagina=2').content.decode())

    def test_no_se_guarda_en_cache(self):
        self.assertIn('no-store', self.client.get('/inquilinos/')['Cache-Control'])


class RegistroTests(Pantallas):
    def test_muestra_el_texto_y_avisa_que_es_borrador(self):
        html = self.client.get('/inquilinos/nuevo/').content.decode()
        self.assertIn('Primera línea', html)
        self.assertIn('versión 1', html)
        self.assertIn('borrador sin validar por un abogado', html)
        self.assertIn('name="confirma"', html)

    @patch('inquilinos.pantallas.selectors.texto_vigente', return_value=None)
    def test_sin_texto_cargado_no_deja_registrar(self, _):
        self.assertIn('Todavía no hay un texto informativo', self.client.get('/inquilinos/nuevo/').content.decode())
        r = self.client.post('/inquilinos/nuevo/', self.formulario())
        self.assertEqual((r.status_code, Inquilino.objects.count()), (200, 0))

    def test_registra_con_su_consentimiento_y_auditoria(self):
        r = self.client.post('/inquilinos/nuevo/', self.formulario(telefono='8888 0000', correo='a@b.cr'))
        inquilino = Inquilino.objects.get()
        self.assertRedirects(r, f'/inquilinos/{inquilino.pk}/', fetch_redirect_response=False)
        consentimiento = Consentimiento.objects.get()
        self.assertEqual((consentimiento.texto_id, consentimiento.medio, consentimiento.inquilino_id), (self.texto.pk, 'fisico', inquilino.pk))
        self.assertEqual(sorted(Auditoria.objects.values_list('accion', flat=True)), ['consentimiento_otorgado', 'inquilino_registrado'])
        self.assertIn('Inquilino registrado', self.client.get(f'/inquilinos/{inquilino.pk}/').content.decode())

    def test_exige_la_confirmacion_del_consentimiento_y_no_guarda_nada(self):
        r = self.client.post('/inquilinos/nuevo/', self.formulario(confirma=''))
        self.assertEqual(r.status_code, 400)
        self.assertIn('Confirme que se mostró el texto', r.content.decode())
        self.assertEqual((Inquilino.objects.count(), Consentimiento.objects.count(), Auditoria.objects.count()), (0, 0, 0))

    def test_exige_el_medio_y_conserva_lo_escrito(self):
        r = self.client.post('/inquilinos/nuevo/', self.formulario(medio='', nombre_completo='Lo escrito'))
        self.assertEqual(r.status_code, 400)
        self.assertIn('value="Lo escrito"', r.content.decode())
        self.assertEqual(Inquilino.objects.count(), 0)

    def test_errores_de_los_datos_se_muestran_junto_al_campo(self):
        r = self.client.post('/inquilinos/nuevo/', self.formulario(nombre_completo='', correo='no-es-correo', telefono='12'))
        html = r.content.decode()
        self.assertEqual(r.status_code, 400)
        for esperado in ('El nombre completo es obligatorio.', 'El correo no es una dirección válida.', 'El teléfono debe tener'):
            self.assertIn(esperado, html)
        self.assertEqual(Inquilino.objects.count(), 0)

    def test_la_fecha_futura_o_mal_escrita_se_rechaza(self):
        manana = (timezone.localdate() + timedelta(days=1)).isoformat()
        for valor, mensaje in ((manana, 'no puede ser futura'), ('31/02/2026', 'no es válida')):
            r = self.client.post('/inquilinos/nuevo/', self.formulario(otorgado_en=valor))
            self.assertEqual(r.status_code, 400, valor)
            self.assertIn(mensaje, r.content.decode())
        self.assertEqual(Inquilino.objects.count(), 0)

    def test_una_fecha_pasada_se_guarda_a_mediodia_y_la_de_hoy_nunca_es_futura(self):
        self.client.post('/inquilinos/nuevo/', self.formulario(otorgado_en='2026-01-15'))
        self.client.post('/inquilinos/nuevo/', self.formulario(numero_documento='2-2', otorgado_en=timezone.localdate().isoformat()))
        antes, hoy = Consentimiento.objects.order_by('otorgado_en')
        local = timezone.localtime(antes.otorgado_en)
        self.assertEqual((local.date().isoformat(), local.hour), ('2026-01-15', 12))
        self.assertLessEqual(hoy.otorgado_en, timezone.now())

    def test_documento_duplicado_avisa_y_solo_guarda_si_se_confirma(self):
        existente = self.registrar()
        r = self.client.post('/inquilinos/nuevo/', self.formulario(nombre_completo='Otra Persona'))
        self.assertEqual(r.status_code, 200)
        self.assertIn('Ya hay un inquilino activo con este documento', r.content.decode())
        self.assertIn(f'/inquilinos/{existente.pk}/', r.content.decode())
        self.assertEqual(Inquilino.objects.count(), 1)
        r = self.client.post('/inquilinos/nuevo/', self.formulario(nombre_completo='Otra Persona', confirmar_duplicado='1'))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Inquilino.objects.count(), 2)

    def test_campos_que_no_son_del_formulario_se_ignoran(self):
        self.client.post('/inquilinos/nuevo/', self.formulario(activo='', desasociado_en='2026-01-01', id='99'))
        inquilino = Inquilino.objects.get()
        self.assertTrue(inquilino.activo)
        self.assertIsNone(inquilino.desasociado_en)
        self.assertNotEqual(inquilino.pk, 99)


class FichaTests(Pantallas):
    def test_muestra_datos_consentimiento_y_aviso_de_falta_el_frente(self):
        inquilino = self.registrar(telefono='8888 0000', correo='a@b.cr')
        html = self.client.get(f'/inquilinos/{inquilino.pk}/').content.decode()
        for esperado in ('Nombre Apellido', '1-1111-1111', '8888 0000', 'a@b.cr', 'Falta el frente del documento',
                         'Versión 1 (borrador sin validar por un abogado)', 'vigente', 'Revocar el consentimiento',
                         f'/inquilinos/{inquilino.pk}/fotografias/', 'Editar datos', 'Desactivar'):
            self.assertIn(esperado, html)

    def test_con_el_frente_cargado_ya_no_avisa_y_enlaza_ver_y_descargar(self):
        inquilino = self.registrar()
        documento = services.subir_fotografia(inquilino.pk, cara='frente', contenido=a_bytes(degradado(), 'JPEG'), actor='admin')
        html = self.client.get(f'/inquilinos/{inquilino.pk}/').content.decode()
        self.assertNotIn('Falta el frente del documento', html)
        self.assertIn(f'/inquilinos/documentos/{documento.pk}/ver/', html)
        self.assertIn(f'/inquilinos/documentos/{documento.pk}/descargar/', html)
        self.assertNotIn(documento.referencia_archivo, html)   # el nombre del archivo no se muestra

    def test_inexistente_da_404(self):
        for ruta in ('', 'editar/', 'desactivar/', 'reactivar/', 'consentimiento/revocar/'):
            self.assertEqual(self.client.get(f'/inquilinos/999999/{ruta}').status_code, 404, ruta)

    def test_un_inquilino_desasociado_no_ofrece_acciones(self):
        inquilino = self.registrar()
        Inquilino.objects.filter(pk=inquilino.pk).update(
            nombre_completo=None, numero_documento=None, telefono=None, correo=None, desasociado_en=timezone.now())
        html = self.client.get(f'/inquilinos/{inquilino.pk}/').content.decode()
        self.assertIn('Inquilino desasociado', html)
        self.assertNotIn('Editar datos', html)
        self.assertEqual(self.client.get(f'/inquilinos/{inquilino.pk}/editar/').status_code, 409)
        self.assertEqual(self.client.post(f'/inquilinos/{inquilino.pk}/desactivar/').status_code, 409)


class EdicionTests(Pantallas):
    def test_trae_los_valores_y_guarda_solo_lo_que_cambia(self):
        inquilino = self.registrar(telefono='8888 0000')
        self.assertIn('value="8888 0000"', self.client.get(f'/inquilinos/{inquilino.pk}/editar/').content.decode())
        r = self.client.post(f'/inquilinos/{inquilino.pk}/editar/', self.formulario(telefono='7777 1111'))
        self.assertRedirects(r, f'/inquilinos/{inquilino.pk}/')
        inquilino.refresh_from_db()
        self.assertEqual(inquilino.telefono, '7777 1111')
        evento = Auditoria.objects.get(accion='inquilino_actualizado')
        self.assertEqual(evento.campos_modificados, ['telefono'])
        self.assertNotIn('7777', str(list(Auditoria.objects.values())))    # el valor personal no se audita

    def test_errores_no_guardan(self):
        inquilino = self.registrar()
        r = self.client.post(f'/inquilinos/{inquilino.pk}/editar/', self.formulario(nombre_completo=' '))
        self.assertEqual(r.status_code, 400)
        self.assertIn('El nombre completo es obligatorio.', r.content.decode())
        inquilino.refresh_from_db()
        self.assertEqual(inquilino.nombre_completo, 'Nombre Apellido')

    def test_el_estado_y_la_desasociacion_no_se_cambian_por_aqui(self):
        inquilino = self.registrar()
        self.client.post(f'/inquilinos/{inquilino.pk}/editar/', self.formulario(activo='', desasociado_en='2026-01-01'))
        inquilino.refresh_from_db()
        self.assertTrue(inquilino.activo)
        self.assertIsNone(inquilino.desasociado_en)

    def test_cambiar_a_un_documento_ya_usado_avisa(self):
        self.registrar()
        otro = self.registrar(nombre_completo='Otro', numero_documento='5-5555')
        r = self.client.post(f'/inquilinos/{otro.pk}/editar/', self.formulario(nombre_completo='Otro', numero_documento='1-1111-1111'))
        self.assertIn('Ya hay un inquilino activo con este documento', r.content.decode())
        otro.refresh_from_db()
        self.assertEqual(otro.numero_documento, '5-5555')
        r = self.client.post(f'/inquilinos/{otro.pk}/editar/', self.formulario(
            nombre_completo='Otro', numero_documento='1-1111-1111', confirmar_duplicado='1'))
        self.assertEqual(r.status_code, 302)


class DesactivarYReactivarTests(Pantallas):
    def test_pide_confirmacion_y_el_get_no_cambia_nada(self):
        inquilino = self.registrar()
        r = self.client.get(f'/inquilinos/{inquilino.pk}/desactivar/')
        self.assertIn('No se borra nada', r.content.decode())
        inquilino.refresh_from_db()
        self.assertTrue(inquilino.activo)
        self.assertEqual(Auditoria.objects.filter(accion='inquilino_desactivado').count(), 0)

    def test_desactiva_sin_borrar_nada_y_reactiva(self):
        inquilino = self.registrar()
        documento = services.subir_fotografia(inquilino.pk, cara='frente', contenido=a_bytes(degradado(), 'JPEG'), actor='admin')
        self.assertRedirects(self.client.post(f'/inquilinos/{inquilino.pk}/desactivar/'), f'/inquilinos/{inquilino.pk}/')
        inquilino.refresh_from_db()
        self.assertFalse(inquilino.activo)
        self.assertTrue(DocumentoIdentidad.objects.filter(pk=documento.pk, eliminado_en__isnull=True).exists())
        self.assertIn('Reactivar', self.client.get(f'/inquilinos/{inquilino.pk}/').content.decode())
        self.assertRedirects(self.client.post(f'/inquilinos/{inquilino.pk}/reactivar/'), f'/inquilinos/{inquilino.pk}/')
        inquilino.refresh_from_db()
        self.assertTrue(inquilino.activo)

    def test_un_motivo_registrado_bloquea_y_se_muestra(self):
        """CA-29: el mecanismo; el motivo real (contrato vigente, saldos) lo aportan la E2 y la E3."""
        inquilino = self.registrar()
        comprobacion = lambda i: ['Tiene un contrato vigente.']   # noqa: E731
        bloqueos.registrar(comprobacion)
        self.addCleanup(bloqueos.quitar, comprobacion)
        r = self.client.post(f'/inquilinos/{inquilino.pk}/desactivar/')
        self.assertEqual(r.status_code, 409)
        self.assertIn('Tiene un contrato vigente.', r.content.decode())
        inquilino.refresh_from_db()
        self.assertTrue(inquilino.activo)

    def test_desactivar_dos_veces_o_reactivar_un_activo_da_conflicto(self):
        inquilino = self.registrar()
        self.assertEqual(self.client.post(f'/inquilinos/{inquilino.pk}/reactivar/').status_code, 409)
        self.client.post(f'/inquilinos/{inquilino.pk}/desactivar/')
        self.assertEqual(self.client.post(f'/inquilinos/{inquilino.pk}/desactivar/').status_code, 409)

    def test_reactivar_con_el_documento_en_uso_avisa(self):
        viejo = self.registrar()
        services.desactivar_inquilino(viejo.pk, actor='admin')
        self.registrar(nombre_completo='Nuevo')
        r = self.client.post(f'/inquilinos/{viejo.pk}/reactivar/')
        self.assertIn('Ya hay un inquilino activo con este documento', r.content.decode())
        viejo.refresh_from_db()
        self.assertFalse(viejo.activo)
        self.assertEqual(self.client.post(f'/inquilinos/{viejo.pk}/reactivar/', {'confirmar_duplicado': '1'}).status_code, 302)


class RevocacionTests(Pantallas):
    def test_el_get_solo_explica_y_el_post_revoca_sin_tocar_datos(self):
        inquilino = self.registrar(telefono='8888 0000')
        documento = services.subir_fotografia(inquilino.pk, cara='frente', contenido=a_bytes(degradado(), 'JPEG'), actor='admin')
        antes = list(Inquilino.objects.values())
        r = self.client.get(f'/inquilinos/{inquilino.pk}/consentimiento/revocar/')
        self.assertIn('no tiene efecto retroactivo', r.content.decode())
        self.assertTrue(Consentimiento.objects.get().vigente)
        self.assertRedirects(self.client.post(f'/inquilinos/{inquilino.pk}/consentimiento/revocar/'), f'/inquilinos/{inquilino.pk}/')
        self.assertFalse(Consentimiento.objects.get().vigente)
        self.assertEqual(list(Inquilino.objects.values()), antes)          # CA-67: ningún dato cambia
        self.assertTrue(DocumentoIdentidad.objects.filter(pk=documento.pk, eliminado_en__isnull=True).exists())
        html = self.client.get(f'/inquilinos/{inquilino.pk}/').content.decode()
        self.assertIn('Consentimiento revocado.', html)
        self.assertNotIn('Revocar el consentimiento', html)
        self.assertEqual(Auditoria.objects.filter(accion='consentimiento_revocado').count(), 1)

    def test_sin_consentimiento_vigente_no_se_pueden_subir_fotografias(self):
        inquilino = self.registrar()
        self.client.post(f'/inquilinos/{inquilino.pk}/consentimiento/revocar/')
        r = self.client.post(f'/inquilinos/{inquilino.pk}/fotografias/frente/', {'archivo': _jpeg()})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(DocumentoIdentidad.objects.count(), 0)

    def test_revocar_dos_veces_da_conflicto(self):
        inquilino = self.registrar()
        self.client.post(f'/inquilinos/{inquilino.pk}/consentimiento/revocar/')
        r = self.client.post(f'/inquilinos/{inquilino.pk}/consentimiento/revocar/')
        self.assertEqual(r.status_code, 409)
        self.assertIn('no tiene un consentimiento vigente', r.content.decode())


def _jpeg():
    from django.core.files.uploadedfile import SimpleUploadedFile
    return SimpleUploadedFile('f.jpg', a_bytes(degradado(), 'JPEG'), content_type='image/jpeg')


class SeguridadDeLasPantallasTests(Pantallas):
    RUTAS_POST = ('nuevo/', '{id}/editar/', '{id}/desactivar/', '{id}/reactivar/', '{id}/consentimiento/revocar/')

    def test_todo_envio_sin_token_csrf_se_rechaza_y_no_cambia_nada(self):
        inquilino = self.registrar()
        cliente = Client(enforce_csrf_checks=True)
        self.entrar(cliente)
        antes = (Inquilino.objects.count(), list(Inquilino.objects.values()), Auditoria.objects.count())
        for ruta in self.RUTAS_POST:
            r = cliente.post('/inquilinos/' + ruta.format(id=inquilino.pk), self.formulario())
            self.assertEqual(r.status_code, 403, ruta)
        self.assertEqual((Inquilino.objects.count(), list(Inquilino.objects.values()), Auditoria.objects.count()), antes)

    def test_cada_formulario_lleva_su_token(self):
        inquilino = self.registrar()
        for ruta in ('nuevo/', f'{inquilino.pk}/editar/', f'{inquilino.pk}/desactivar/', f'{inquilino.pk}/consentimiento/revocar/'):
            self.assertIn('csrfmiddlewaretoken', self.client.get('/inquilinos/' + ruta).content.decode(), ruta)

    def test_los_metodos_no_admitidos_responden_405(self):
        inquilino = self.registrar()
        self.assertEqual(self.client.post('/inquilinos/').status_code, 405)
        self.assertEqual(self.client.post(f'/inquilinos/{inquilino.pk}/').status_code, 405)
        self.assertEqual(self.client.put(f'/inquilinos/{inquilino.pk}/desactivar/').status_code, 405)

    def test_ninguna_pantalla_se_guarda_en_cache(self):
        inquilino = self.registrar()
        for ruta in ('', 'nuevo/', f'{inquilino.pk}/', f'{inquilino.pk}/editar/', f'{inquilino.pk}/desactivar/'):
            self.assertIn('no-store', self.client.get('/inquilinos/' + ruta)['Cache-Control'], ruta)


class AuditoriaDeLasPantallasTests(Pantallas):
    def test_cada_accion_queda_con_su_actor_y_su_ip(self):
        self.client.post('/inquilinos/nuevo/', self.formulario())
        pk = Inquilino.objects.get().pk
        self.client.post(f'/inquilinos/{pk}/editar/', self.formulario(telefono='8888 0000'))
        self.client.post(f'/inquilinos/{pk}/desactivar/')
        self.client.post(f'/inquilinos/{pk}/reactivar/')
        self.client.post(f'/inquilinos/{pk}/consentimiento/revocar/')
        acciones = sorted(Auditoria.objects.values_list('accion', flat=True))
        self.assertEqual(acciones, sorted([
            'inquilino_registrado', 'consentimiento_otorgado', 'inquilino_actualizado', 'inquilino_desactivado',
            'inquilino_reactivado', 'consentimiento_revocado']))
        self.assertEqual(set(Auditoria.objects.values_list('actor', flat=True)), {'admin'})
        self.assertEqual(set(Auditoria.objects.values_list('ip_origen', flat=True)), {'127.0.0.1'})
