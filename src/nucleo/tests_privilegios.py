"""Roles y privilegios de la base (ADR-027, ADR-031 decisión 3, ADR-032 decisión 12; condición 4).

Necesitan PostgreSQL y un usuario de conexión que pueda crear roles (en la integración continua, el
superusuario del servicio). Se prueba de verdad: se crean roles de prueba, se aplica el archivo de
privilegios y se ejecuta SQL «como» cada rol con SET ROLE, incluida la edición directa de la
auditoría, que ni Django ni sus guardas intervienen.
"""
from django.db import ProgrammingError, connection, transaction
from django.test import TestCase, override_settings

from nucleo import auditoria, privilegios
from nucleo.models import Auditoria
from sga.privilegios import PRIVILEGIOS

ROLES = {'dueno': 'sga_t_dueno', 'app': 'sga_t_app', 'respaldos': 'sga_t_respaldos'}


def puede_crear_roles():
    with connection.cursor() as c:
        c.execute('SELECT rolsuper OR rolcreaterole FROM pg_roles WHERE rolname = current_user')
        return c.fetchone()[0]


class ArchivoDePrivilegiosTests(TestCase):
    def test_cada_tabla_tiene_su_entrada(self):
        """ADR-031: una tabla nueva sin entrada falla visible, y esta prueba la delata."""
        sin_entrada = privilegios.tablas_existentes() - set(PRIVILEGIOS)
        self.assertEqual(sin_entrada, set(), f'Tablas sin entrada en sga/privilegios.py: {sorted(sin_entrada)}')

    def test_ninguna_entrada_apunta_a_una_tabla_que_no_existe(self):
        self.assertEqual(set(PRIVILEGIOS) - privilegios.tablas_existentes(), set())

    def test_el_rol_de_la_aplicacion_nunca_recibe_privilegios_peligrosos(self):
        for tabla, entrada in PRIVILEGIOS.items():
            self.assertFalse({'TRUNCATE', 'REFERENCES', 'TRIGGER', 'ALL'} & set(entrada.get('tabla', ())), tabla)

    def test_r12_las_tablas_de_solo_insercion_no_tienen_update_ni_delete(self):
        self.assertEqual(set(PRIVILEGIOS['nucleo_auditoria']['tabla']), {'SELECT', 'INSERT'})

    def test_una_conexion_por_peticion(self):
        """ADR-029."""
        from django.conf import settings
        self.assertEqual(settings.DATABASES['default']['CONN_MAX_AGE'], 0)

    def test_las_sentencias_son_idempotentes_y_no_dependen_del_orden_de_entrada(self):
        with override_settings(ROLES_BD=ROLES):
            self.assertEqual(privilegios.sentencias(), privilegios.sentencias())


@override_settings(ROLES_BD=ROLES)
class RolesYPrivilegiosTests(TestCase):
    """Los roles se crean dentro de la transacción de la clase y se deshacen solos al terminar."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not puede_crear_roles():
            cls.tearDownClass()
            from unittest import SkipTest
            raise SkipTest('El usuario de conexión no puede crear roles.')

    @classmethod
    def setUpTestData(cls):
        with connection.cursor() as c:
            for rol in ROLES.values():
                c.execute(f'CREATE ROLE {rol} NOLOGIN')
            c.execute(f'GRANT pg_read_all_data TO {ROLES["respaldos"]}')
            c.execute(f'GRANT USAGE ON SCHEMA public TO {ROLES["app"]}, {ROLES["respaldos"]}')
        privilegios.aplicar()
        auditoria.registrar('semilla', 'prueba', actor='admin')

    def como(self, rol, sql, params=None):
        """Ejecuta `sql` con los privilegios del rol; devuelve las filas o lanza ProgrammingError."""
        with connection.cursor() as c:
            c.execute(f'SET LOCAL ROLE {ROLES[rol]}')
            try:
                with transaction.atomic():
                    c.execute(sql, params)
                    return c.fetchall() if c.description else None
            finally:
                c.execute('RESET ROLE')

    def rechazado(self, rol, sql, params=None):
        with self.assertRaises(ProgrammingError, msg=sql) as contexto:
            self.como(rol, sql, params)
        self.assertRegex(str(contexto.exception), 'permission denied|must be owner')

    # --- R12 sobre la auditoría
    def test_la_aplicacion_inserta_y_lee_la_auditoria(self):
        self.como('app', "INSERT INTO nucleo_auditoria (entidad, actor, tipo_actor, accion, ocurrido_en, "
                         "campos_modificados) VALUES ('x', 'a', 'administrador', 'prueba_rol', now(), '[]')")
        self.assertGreaterEqual(self.como('app', 'SELECT count(*) FROM nucleo_auditoria')[0][0], 2)

    def test_la_aplicacion_no_puede_editar_ni_borrar_la_auditoria_ni_saltandose_django(self):
        self.rechazado('app', "UPDATE nucleo_auditoria SET accion = 'borrada'")
        self.rechazado('app', 'DELETE FROM nucleo_auditoria')
        self.rechazado('app', 'TRUNCATE nucleo_auditoria')
        self.assertEqual(Auditoria.objects.filter(accion='borrada').count(), 0)

    # --- el resto de las tablas
    def test_cuenta_administradora(self):
        self.como('app', 'SELECT count(*) FROM cuentas_administrador')
        self.rechazado('app', 'DELETE FROM cuentas_administrador')

    def test_codigos_de_recuperacion_solo_cambian_su_marca_de_uso(self):
        self.como('app', 'UPDATE cuentas_codigorecuperacion SET usado_en = now()')
        self.rechazado('app', "UPDATE cuentas_codigorecuperacion SET hash_codigo = 'x'")
        self.como('app', 'DELETE FROM cuentas_codigorecuperacion')

    def test_sesiones_se_pueden_borrar(self):
        self.como('app', 'DELETE FROM django_session')

    def test_organizacion_se_lee_y_se_actualiza_pero_no_se_borra(self):
        self.como('app', "UPDATE nucleo_organizacion SET zona_horaria = 'America/Costa_Rica'")
        self.rechazado('app', 'DELETE FROM nucleo_organizacion')

    def test_las_tablas_de_django_son_solo_del_rol_dueno(self):
        for tabla in ('django_migrations', 'django_content_type', 'auth_permission', 'auth_group'):
            self.rechazado('app', f'SELECT * FROM {tabla}')

    def test_la_aplicacion_no_crea_ni_destruye_objetos(self):
        self.rechazado('app', 'CREATE TABLE intruso (id int)')
        self.rechazado('app', 'DROP TABLE nucleo_auditoria')
        self.rechazado('app', 'ALTER TABLE nucleo_auditoria ADD COLUMN x int')

    def test_una_tabla_sin_entrada_no_da_ningun_privilegio(self):
        with connection.cursor() as c:
            c.execute('CREATE TABLE tabla_nueva_sin_entrada (id int)')
        privilegios.aplicar()
        self.rechazado('app', 'SELECT * FROM tabla_nueva_sin_entrada')

    # --- respaldos
    def test_el_rol_de_respaldos_lee_todo_y_no_escribe_nada(self):
        for tabla in PRIVILEGIOS:
            self.como('respaldos', f'SELECT count(*) FROM {tabla}')
        self.rechazado('respaldos', "UPDATE nucleo_organizacion SET zona_horaria = 'x'")
        self.rechazado('respaldos', 'DELETE FROM nucleo_auditoria')
        self.rechazado('respaldos', "INSERT INTO nucleo_auditoria (entidad, actor, tipo_actor, accion, ocurrido_en, "
                                    "campos_modificados) VALUES ('x', 'a', 'administrador', 'r', now(), '[]')")

    # --- base y esquema
    def test_public_no_puede_conectarse_y_los_tres_roles_si(self):
        with connection.cursor() as c:
            c.execute('SELECT datacl::text FROM pg_database WHERE datname = current_database()')
            acl = c.fetchone()[0]
        self.assertIn(f'{ROLES["app"]}=Tc/', acl)
        self.assertIn(f'{ROLES["respaldos"]}=Tc/', acl)
        self.assertIn(f'{ROLES["dueno"]}=Tc/', acl)
        self.assertFalse([e for e in acl.strip('{}').split(',') if e.startswith('=')])  # sin entrada de PUBLIC

    def test_aplicar_dos_veces_deja_lo_mismo(self):
        def acls():
            with connection.cursor() as c:
                c.execute("SELECT relname, relacl::text, (SELECT string_agg(attname || ':' || attacl::text, ',' "
                          "ORDER BY attname) FROM pg_attribute WHERE attrelid = pg_class.oid AND attacl IS NOT NULL) "
                          "FROM pg_class WHERE relname LIKE ANY (ARRAY['nucleo_%%', 'cuentas_%%', 'django_%%', "
                          "'auth_%%']) AND relkind = 'r' ORDER BY relname")
                return c.fetchall()
        antes = acls()
        privilegios.aplicar()
        privilegios.aplicar()
        self.assertEqual(acls(), antes)

    def test_aplicar_quita_lo_que_el_archivo_no_concede(self):
        """Idempotencia estricta: un privilegio concedido a mano se retira al volver a aplicar."""
        with connection.cursor() as c:
            c.execute(f'GRANT UPDATE, DELETE ON nucleo_auditoria TO {ROLES["app"]}')
            c.execute(f'GRANT TRUNCATE ON nucleo_organizacion TO {ROLES["app"]}')
        self.como('app', "UPDATE nucleo_auditoria SET accion = accion")  # el exceso existe...
        privilegios.aplicar()
        self.rechazado('app', "UPDATE nucleo_auditoria SET accion = accion")  # ...y desaparece
        self.rechazado('app', 'DELETE FROM nucleo_auditoria')
        self.rechazado('app', 'TRUNCATE nucleo_organizacion')
