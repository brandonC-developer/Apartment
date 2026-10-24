# Actualización 2026-10-24 (g) — Roles de PostgreSQL y archivo de privilegios

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/db/roles.sql`](../../../src/db/roles.sql), [`src/sga/privilegios.py`](../../../src/sga/privilegios.py), [`src/nucleo/`](../../../src/nucleo/privilegios.py), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** DAS v0.15, ADR-027 (tres roles, `peer`, R12), ADR-031 decisión 3 (archivo de privilegios idempotente tras cada migración y prueba de tablas contra el archivo), ADR-032 decisión 12 (`CONNECT` y `TEMPORARY`); plan, condición 4 de terminado; instrucción del solicitante: «sí, escribe los roles y el archivo de privilegios» (24-oct-2026)
**Estado:** implementado y probado en un PostgreSQL desechable; no aprobado

## 1. Qué se escribió
| Archivo | Contenido |
|---|---|
| `db/roles.sql` | Crea, de forma idempotente y con `psql`, los tres roles (`LOGIN`, sin contraseña, sin superusuario, sin crear roles ni bases), la base con el rol dueño como propietario, la lectura total para el rol de respaldos (`pg_read_all_data`) y sesiones de solo lectura para él |
| `sga/privilegios.py` | **El archivo de privilegios**: una entrada por tabla con los privilegios del rol de la aplicación; una tabla sin entrada queda sin acceso |
| `nucleo/privilegios.py` y `manage.py aplicar_privilegios` | Aplica el archivo (parte de `REVOKE ALL` y concede lo que consta), revoca `CONNECT`/`TEMPORARY` a `PUBLIC`, los concede a los tres roles y quita `CREATE` en `public` a `PUBLIC`; avisa de las tablas sin entrada; `--mostrar` imprime el SQL |
| `sga/settings.py` | `ROLES_BD` (nombres por variable de entorno) |
| `nucleo/tests_privilegios.py` | 19 pruebas |

## 2. Privilegios concedidos al rol de la aplicación
| Tabla | Privilegios |
|---|---|
| `nucleo_auditoria` | `SELECT`, `INSERT` (R12) |
| `nucleo_organizacion` | `SELECT`, `INSERT`, `UPDATE` |
| `cuentas_administrador` | `SELECT`, `INSERT`, `UPDATE` (sin `DELETE`) |
| `cuentas_codigorecuperacion` | `SELECT`, `INSERT`, `DELETE`; `UPDATE` solo de la columna `usado_en` |
| `django_session` | `SELECT`, `INSERT`, `UPDATE`, `DELETE` |
| `django_migrations`, `django_content_type`, `auth_permission`, `auth_group`, `auth_group_permissions` | ninguno (solo el rol dueño) |

Nunca se concede `TRUNCATE`, `REFERENCES`, `TRIGGER` ni la propiedad de una tabla.

## 3. Propuestas del asistente (sin aprobar)
- **Formato del archivo de privilegios:** un módulo de Python y no un script SQL (el ADR-031 dejó el formato pendiente), para poder comparar sus entradas con las tablas reales.
- **Nombres de los roles:** `sga_dueno`, `sga_app` y `sga_respaldos`, configurables por variable de entorno.
- **Desviación del ADR-027:** `DELETE` sobre `cuentas_codigorecuperacion`. La propuesta del ADR era solo `UPDATE` de `usado_en`, pero emitir códigos nuevos y el rescate borran los anteriores (la ERS pide invalidarlos). Alternativa si se prefiere no dar `DELETE`: marcar los códigos invalidados con una columna propia en lugar de borrarlos.
- `INSERT` sobre `nucleo_organizacion` solo por si la fila faltara; `SELECT` y `UPDATE` sobre `cuentas_administrador` por el contador de intentos y `last_login`.
- El rol de respaldos usa `pg_read_all_data` y no recibe privilegios por tabla.

## 4. Verificación
- **140 pruebas pasan** (19 nuevas) en PostgreSQL 18 desechable (ya borrado), Python 3.12 en Windows. Las de roles corren en una transacción con roles de prueba y `SET ROLE`, y se omiten si el usuario de conexión no puede crear roles.
- Se prueba: una entrada por tabla y ninguna entrada huérfana; el rol de la aplicación inserta y lee la auditoría pero es rechazado en `UPDATE`, `DELETE` y `TRUNCATE` con SQL directo (sin Django); no borra la cuenta; solo cambia `usado_en` en los códigos; no lee las tablas de Django; no crea, altera ni borra objetos; una tabla sin entrada no da acceso; el rol de respaldos lee todo y no escribe nada; `PUBLIC` no puede conectarse; aplicar dos veces deja el mismo estado y **quita lo concedido a mano**.
- **Mutaciones manuales:** dar `UPDATE` a la auditoría, quitar una entrada, permitir editar `hash_codigo`, no revocar a `PUBLIC` hicieron fallar sus pruebas. Quitar el `REVOKE ALL` **no** fallaba: se agregó una prueba (que retire lo concedido a mano) y entonces sí falló; se restauró el código.
- **Recorrido real con el rol de la aplicación** (base `sga_e2e` creada con `roles.sql`, migrada y con privilegios aplicados por el rol dueño): registro del segundo factor con token, inicio de sesión, pantalla de auditoría, inicio con código de recuperación, cierre de sesión y rescate, todo con la conexión del rol `sga_app`; `UPDATE` y `DELETE` sobre la auditoría y la lectura de `django_migrations` fueron rechazados. `roles.sql` se ejecutó dos veces sin error.
- **`pg_dump` y `pg_dumpall --globals-only --no-role-passwords` con el rol de respaldos funcionaron** sin ser superusuario (30 704 bytes y 1 121 bytes en la base de prueba), lo que el ADR-027 dejaba «no confirmado». Límite: PostgreSQL 18 en Windows con autenticación `trust`; hay que repetirlo con `peer` en WSL.

## 5. Qué no está hecho
- **Autenticación `peer`, `pg_hba.conf`, `listen_addresses = ''`, grupo del socket y usuarios del sistema** (ADR-032 d12): son del servidor y se prueban en WSL. Las pruebas usaron `trust` y `SET ROLE`.
- Las tablas de movimientos, ajustes y accesos a documentos no existen aún; cada entrega agrega sus entradas y repite la prueba de R12.
- Cómo ejecuta el administrador las migraciones como rol dueño (`sudo -u`, sin verificar) y su procedimiento en la fase 6.
- Respaldo cifrado y su restauración, WSL y CI. 0 de 8 CA de la E0 cumplidos.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
