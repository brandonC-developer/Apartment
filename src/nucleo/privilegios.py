"""Aplicación idempotente de los privilegios de la base (ADR-027, ADR-031 decisión 3, ADR-032
decisión 12). La ejecuta el rol dueño después de cada `migrate`."""
from django.conf import settings
from django.db import connection

from sga.privilegios import PRIVILEGIOS


def sentencias(roles=None, privilegios=None, base=None):
    """Lista de sentencias SQL que dejan los privilegios exactamente como dice el archivo."""
    roles = roles or settings.ROLES_BD
    privilegios = privilegios if privilegios is not None else PRIVILEGIOS
    q = connection.ops.quote_name
    app, respaldos, dueno = q(roles['app']), q(roles['respaldos']), q(roles['dueno'])
    base = q(base or connection.settings_dict['NAME'])
    todas = f'{dueno}, {app}, {respaldos}'
    sql = [
        # ADR-032, decisión 12: nadie entra a la base ni crea objetos sin que se le conceda.
        f'REVOKE CONNECT, TEMPORARY ON DATABASE {base} FROM PUBLIC',
        f'GRANT CONNECT, TEMPORARY ON DATABASE {base} TO {todas}',
        'REVOKE CREATE ON SCHEMA public FROM PUBLIC',
        f'GRANT USAGE ON SCHEMA public TO {app}, {respaldos}',
    ]
    for tabla, entrada in sorted(privilegios.items()):
        t = q(tabla)
        # Se parte de cero para que el resultado no dependa de lo concedido antes (idempotencia).
        sql.append(f'REVOKE ALL ON TABLE {t} FROM {app}')
        if entrada.get('tabla'):
            sql.append(f"GRANT {', '.join(entrada['tabla'])} ON TABLE {t} TO {app}")
        for privilegio, columnas in entrada.get('columnas', {}).items():
            lista = ', '.join(q(c) for c in columnas)
            sql.append(f'GRANT {privilegio} ({lista}) ON TABLE {t} TO {app}')
    return sql


def tablas_existentes():
    """Tablas de los modelos instalados más la de migraciones, que no tiene modelo registrado."""
    with connection.cursor():
        return set(connection.introspection.django_table_names(only_existing=True)) | {'django_migrations'}


def aplicar(**kwargs):
    with connection.cursor() as cursor:
        for instruccion in sentencias(**kwargs):
            cursor.execute(instruccion)
