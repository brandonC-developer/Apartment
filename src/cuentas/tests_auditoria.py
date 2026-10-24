"""Auditoría de la autenticación y su consulta (RF-28, CA-68, CA-70, CA-71, HI-01). Necesitan PostgreSQL."""
import re
from datetime import timedelta
from io import StringIO
from unittest.mock import patch

import pyotp
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone

from nucleo import auditoria
from nucleo.models import Auditoria

from . import autenticacion
from .models import Administrador
from .tests import CLAVE_A, CONTRASENA


def acciones():
    return list(Auditoria.objects.order_by('id').values_list('accion', flat=True))


@override_settings(CLAVES_CIFRADO=[CLAVE_A])
class AuditoriaDeAutenticacionTests(TestCase):
    def setUp(self):
        self.secreto = pyotp.random_base32()
        self.admin = Administrador.objects.crear_administrador('admin', CONTRASENA)
        self.admin.fijar_secreto_segundo_factor(self.secreto)
        self.admin.segundo_factor_activo = True
        self.admin.save()

    def entrar(self, contrasena=CONTRASENA, usuario='admin', **extra):
        return self.client.post('/entrar/', {'usuario': usuario, 'contrasena': contrasena}, **extra)

    def codigo(self, codigo=None):
        return self.client.post('/entrar/codigo/', {'codigo': codigo or pyotp.TOTP(self.secreto).now()})

    def iniciar(self, **extra):
        Administrador.objects.update(ultimo_intervalo_totp=None)  # varios inicios en el mismo intervalo
        self.entrar(**extra)
        self.codigo()

    def test_un_fallo_y_un_inicio_correcto_constan_con_fecha_hora_e_ip(self):
        antes = timezone.now()
        self.entrar('mal', REMOTE_ADDR='203.0.113.5')
        self.iniciar(REMOTE_ADDR='203.0.113.5')
        fallido = Auditoria.objects.get(accion='inicio_sesion_fallido')
        correcto = Auditoria.objects.get(accion='inicio_sesion')
        self.assertEqual(fallido.ip_origen, '203.0.113.5')
        self.assertEqual(correcto.actor, 'admin')
        self.assertEqual(correcto.registro_id, self.admin.pk)
        for r in (fallido, correcto):
            self.assertGreaterEqual(r.ocurrido_en, antes)

    def test_no_se_guarda_lo_escrito_en_usuario_ni_ningun_secreto(self):
        escrito = 'ContrasenaEscritaEnUsuario9'
        self.entrar('contrasenaMala777', usuario=escrito)
        self.entrar()
        self.codigo('000000')
        self.codigo('ZZZZZ-ZZZZZ')
        codigo_valido = pyotp.TOTP(self.secreto).now()
        self.codigo(codigo_valido)
        todo = ' '.join(
            f'{r.accion}|{r.entidad}|{r.actor}|{r.ip_origen}|{r.campos_modificados}|{r.valor_anterior}|{r.valor_nuevo}'
            for r in Auditoria.objects.all())
        for secreto in (escrito, 'contrasenaMala777', CONTRASENA, '000000', 'ZZZZZ-ZZZZZ', codigo_valido, self.secreto):
            self.assertNotIn(secreto, todo)
        self.assertEqual(Auditoria.objects.filter(actor='anonimo').count(), 1)

    def test_cierre_de_sesion(self):
        self.iniciar()
        self.client.post('/salir/')
        self.assertEqual(acciones()[-1], 'cierre_sesion')

    def test_codigo_de_recuperacion_deja_dos_eventos(self):
        recuperacion = autenticacion.emitir_codigos_recuperacion(self.admin, CONTRASENA)[0]
        self.entrar()
        self.codigo(recuperacion)
        self.assertEqual(acciones(), ['codigo_recuperacion_usado', 'inicio_sesion'])

    def test_cinco_fallos_dejan_un_solo_evento_de_alerta_y_la_espera_no_se_registra(self):
        for _ in range(5):
            self.entrar('mal')
        self.entrar('mal')  # sexto: en espera
        self.assertEqual(acciones().count('inicio_sesion_fallido'), 5)
        self.assertEqual(acciones().count('cinco_fallos_seguidos'), 1)

    def test_la_pantalla_de_inicio_muestra_los_avisos_desde_el_inicio_anterior(self):
        self.iniciar()
        self.client.post('/salir/')
        # Cinco fallos mientras no hay sesión, y luego una espera de más de un minuto.
        for _ in range(5):
            self.entrar('mal')
        Administrador.objects.update(espera_hasta=None)
        self.iniciar()
        r = self.client.get('/')
        self.assertContains(r, 'Avisos de seguridad')
        self.assertContains(r, 'cinco_fallos_seguidos')
        self.client.post('/salir/')
        self.iniciar()
        self.assertNotContains(self.client.get('/'), 'Avisos de seguridad')

    def test_sin_inicio_anterior_se_muestran_todos(self):
        auditoria.registrar('segundo_factor_rescatado', 'administrador', actor='servidor')
        self.iniciar()
        self.assertContains(self.client.get('/'), 'segundo_factor_rescatado')


@override_settings(CLAVES_CIFRADO=[CLAVE_A])
class ConsultaDeAuditoriaTests(TestCase):
    def setUp(self):
        self.secreto = pyotp.random_base32()
        self.admin = Administrador.objects.crear_administrador('admin', CONTRASENA)
        self.admin.fijar_secreto_segundo_factor(self.secreto)
        self.admin.segundo_factor_activo = True
        self.admin.save()

    def iniciar(self):
        Administrador.objects.update(ultimo_intervalo_totp=None)
        self.client.post('/entrar/', {'usuario': 'admin', 'contrasena': CONTRASENA})
        self.client.post('/entrar/codigo/', {'codigo': pyotp.TOTP(self.secreto).now()})

    def test_exige_sesion(self):
        r = self.client.get('/auditoria/')
        self.assertRedirects(r, '/entrar/?next=/auditoria/', fetch_redirect_response=False)

    def test_muestra_los_eventos_y_filtra_por_tipo_actor_entidad_y_fecha(self):
        self.client.post('/entrar/', {'usuario': 'x', 'contrasena': 'mal'})
        self.iniciar()
        r = self.client.get('/auditoria/')
        self.assertContains(r, 'inicio_sesion_fallido')
        self.assertContains(r, 'inicio_sesion')
        r = self.client.get('/auditoria/', {'accion': 'inicio_sesion_fallido'})
        self.assertContains(r, 'anonimo')
        self.assertNotContains(r, '<td>inicio_sesion</td>')
        r = self.client.get('/auditoria/', {'actor': 'admin'})
        self.assertNotContains(r, 'anonimo')
        r = self.client.get('/auditoria/', {'entidad': 'otra'})
        self.assertContains(r, 'Sin registros')
        hoy = timezone.localdate()
        self.assertContains(self.client.get('/auditoria/', {'desde': hoy.isoformat(), 'hasta': hoy.isoformat()}),
                            'inicio_sesion')
        manana = (hoy + timedelta(days=1)).isoformat()
        self.assertContains(self.client.get('/auditoria/', {'desde': manana}), 'Sin registros')
        self.assertContains(self.client.get('/auditoria/', {'desde': 'basura'}), 'inicio_sesion')

    def test_es_de_solo_lectura_y_consultarla_no_genera_registros(self):
        self.iniciar()
        total = Auditoria.objects.count()
        self.client.get('/auditoria/')
        self.client.get('/auditoria/', {'accion': 'inicio_sesion'})
        self.assertEqual(Auditoria.objects.count(), total)
        for metodo in (self.client.post, self.client.put, self.client.delete):
            self.assertEqual(metodo('/auditoria/').status_code, 405)
        self.assertEqual(Auditoria.objects.count(), total)

    def test_pagina_de_a_50(self):
        self.iniciar()
        for _ in range(60):
            auditoria.registrar('relleno', 'prueba', actor='admin')
        r = self.client.get('/auditoria/', {'accion': 'relleno'})
        self.assertContains(r, 'Página 1 de 2')
        self.assertContains(r, 'accion=relleno&amp;pagina=2')
        self.assertContains(self.client.get('/auditoria/', {'accion': 'relleno', 'pagina': 2}), 'Página 2 de 2')


@override_settings(CLAVES_CIFRADO=[CLAVE_A])
class AuditoriaDelRegistroYDeLosComandosTests(TestCase):
    def test_el_registro_del_segundo_factor_deja_sus_tres_eventos(self):
        admin = Administrador.objects.crear_administrador('admin', CONTRASENA)
        token = autenticacion.emitir_token_registro(admin)
        self.client.post('/entrar/', {'usuario': 'admin', 'contrasena': CONTRASENA})
        self.client.post('/entrar/registro/', {'token': 'mal'})
        self.client.post('/entrar/registro/', {'token': token})
        r = self.client.get('/entrar/registro/')
        secreto = re.search(r'<code>([A-Z2-7]{32})</code>', r.content.decode()).group(1)
        self.client.post('/entrar/registro/', {'codigo': pyotp.TOTP(secreto).now()})
        self.assertEqual(acciones(), [
            'inicio_sesion_fallido', 'segundo_factor_registrado', 'codigos_emitidos', 'inicio_sesion'])
        self.assertNotIn(token, str(list(Auditoria.objects.values())))

    def test_los_comandos_dejan_constancia(self):
        with patch('cuentas.management.commands.crear_administrador.getpass', side_effect=[CONTRASENA, CONTRASENA]):
            call_command('crear_administrador', usuario='admin', stdout=StringIO())
        call_command('rescatar_segundo_factor', confirmar=True, stdout=StringIO())
        self.assertEqual(acciones(), ['cuenta_creada', 'segundo_factor_rescatado'])
        self.assertEqual(set(Auditoria.objects.values_list('actor', flat=True)), {'servidor'})
