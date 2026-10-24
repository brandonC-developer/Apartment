-- Roles y base de datos del SGA (ADR-027, ADR-032 decisión 12). Idempotente.
--
-- Lo ejecuta una sola vez el usuario `postgres` del sistema, por el socket Unix (autenticación peer):
--   sudo -u postgres psql -v ON_ERROR_STOP=1 \
--     -v rol_dueno=sga_dueno -v rol_app=sga_app -v rol_respaldos=sga_respaldos -v base=sga \
--     -f src/db/roles.sql
--
-- Tres roles con LOGIN y sin contraseña (se entra por peer con el usuario del sistema del mismo
-- nombre, o con un mapa de nombres); ninguno es superusuario ni puede crear roles o bases.
-- Los nombres de los roles son propuesta del asistente. Los privilegios por tabla los concede
-- después `manage.py aplicar_privilegios`, que ejecuta el rol dueño tras cada `migrate`.

SELECT format('CREATE ROLE %I LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION', r)
FROM (VALUES (:'rol_dueno'), (:'rol_app'), (:'rol_respaldos')) AS roles(r)
WHERE NOT EXISTS (SELECT FROM pg_roles WHERE rolname = r)
\gexec

-- La base es del rol dueño: solo él puede crear tablas (migraciones); la aplicación no es dueña.
SELECT format('CREATE DATABASE %I OWNER %I ENCODING ''UTF8''', :'base', :'rol_dueno')
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = :'base')
\gexec
SELECT format('ALTER DATABASE %I OWNER TO %I', :'base', :'rol_dueno')
\gexec

-- El respaldo solo lee: rol predefinido de lectura y sesiones de solo lectura.
SELECT format('GRANT pg_read_all_data TO %I', :'rol_respaldos')
\gexec
SELECT format('ALTER ROLE %I SET default_transaction_read_only = on', :'rol_respaldos')
\gexec
