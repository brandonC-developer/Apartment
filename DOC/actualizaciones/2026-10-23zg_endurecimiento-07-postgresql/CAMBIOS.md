# Actualización 2026-10-23 (zg) — Endurecimiento, medidas 15 a 18: PostgreSQL

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el DAS (ADR-032, ADR-027, ADR-031), el modelo de amenazas (versión nueva) y el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** propuestas 15, 16, 17 y 18 de la [actualización 2026-10-22 (b)](../2026-10-22b_endurecimiento-nginx-gunicorn-postgresql/CAMBIOS.md); sigue a la [medida de Django (t)](../2026-10-23t_endurecimiento-06-django/CAMBIOS.md) y a las decisiones del [DAS v0.13](../../fase-2-arquitectura/DAS_SGA_001_v0.13_borrador.md)
**Estado:** decisiones registradas; documentos sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 (propuesta 15) | ¿Cómo se alcanza la base de datos? | "Solo socket Unix, 0770 y grupo dedicado" (recomendada por el asistente) | `listen_addresses = ''` (PostgreSQL no escucha en ninguna red) y `unix_socket_permissions = 0770` con un `unix_socket_group` dedicado que contenga solo los usuarios del sistema que usan la base (aplicación, respaldos, administrador para las migraciones con `sudo -u`, y `postgres`) |
| 2 (propuesta 16) | ¿Cómo se restringe el acceso y los privilegios? | "Solo registros local con peer y revocar PUBLIC" (recomendada) | `pg_hba.conf` con **solo registros `local` con `peer`**: uno por cada uno de los tres roles sobre la base del sistema y uno para `postgres`; sin registros `host` y sin `trust`; si el usuario del sistema difiere del rol, un mapa en `pg_ident.conf`; se comprueba con `pg_hba_file_rules` antes de recargar. `CONNECT` y `TEMPORARY` se revocan a `PUBLIC` y se conceden a los tres roles, en el archivo de privilegios idempotente de ADR-031; se confirma que `PUBLIC` no tiene `CREATE` en el esquema `public` |
| 3 (propuesta 17) | ¿Qué registra la base de datos? | "Sin sentencias ni parámetros, consultas lentas y esperas, sin conexiones exitosas" (recomendada) | `log_statement = none`; `log_parameter_max_length = 0`; `log_min_duration_statement = 1000` ms; `log_lock_waits = on`; sin registrar conexiones exitosas ni desconexiones (los fallos de autenticación se registran siempre). **Cambia la propuesta 17 original**, que pedía registrar conexiones y desconexiones |
| 4 (propuesta 18) | ¿Qué política de contraseñas tienen los roles? | "Ninguna en producción; scram-sha-256 si hiciera falta" (recomendada) | Ningún rol de producción tiene contraseña, incluido `postgres`; si alguna vez hiciera falta, `scram-sha-256` y nunca `md5`; la integración continua usa su propia base con credenciales efímeras y distintas |

## 2. Hallazgos que cambiaron la propuesta
- **Propuesta 17:** con una conexión por petición (ADR-029) y el temporizador de cada minuto (ADR-013) habría más de 1 440 conexiones al día solo por el temporizador (cálculo del asistente); registrarlas escondería lo importante. Con `peer` cada conexión ya está atada a un usuario del sistema y los fallos salen siempre.
- **Trampa de `log_parameter_max_length`:** su valor por defecto (`-1`) escribe los parámetros completos en los registros de sentencias; activar las consultas lentas sin tocarlo habría puesto datos personales en el registro técnico (AM-26, RNF-14).

## 3. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| PostgreSQL 18, conexión: https://www.postgresql.org/docs/18/runtime-config-connection.html | Documentación oficial | Leída por resumen (WebFetch, 23-oct-2026) | `listen_addresses` (`localhost` por defecto; vacío = solo sockets Unix); `unix_socket_permissions` (`0777` por defecto; `0770`, `0700`); `unix_socket_group`; independiente de la autenticación | Valores por defecto del código fuente: los de Ubuntu 26.04 no se verificaron |
| Ubuntu, instalación de PostgreSQL: https://ubuntu.com/server/docs/how-to/databases/install-postgresql/ | Documentación del proveedor | Leída por resumen (23-oct-2026) | `listen_addresses = localhost`; socket con `peer`; TCP con `scram-sha-256`; archivos en `/etc/postgresql/<versión>/main/` | Usa PostgreSQL 14 como ejemplo; no declara la versión de Ubuntu; no muestra las líneas de `pg_hba.conf` |
| PostgreSQL 18, `pg_hba.conf` y privilegios; notas de la versión 15 | Documentación oficial | Leídas por resumen en la investigación del 22-oct-2026 | Sin registro `local` se deniegan los sockets Unix; `peer` solo local; primer registro que coincide; `pg_hba_file_rules`; `PUBLIC` recibe `CONNECT` y `TEMPORARY`; sin `CREATE` en `public` desde la 15 | — |
| PostgreSQL 18, registro: https://www.postgresql.org/docs/18/runtime-config-logging.html | Documentación oficial | Leída por resumen (23-oct-2026) | Valores por defecto de `log_connections`, `log_statement`, `log_parameter_max_length` (`-1`), `log_parameter_max_length_on_error` (`0`), `log_min_duration_statement`, `log_lock_waits`; advertencia de que las sentencias pueden revelar datos sensibles | Dónde acaban los registros en Ubuntu 26.04 no se verificó |
| PostgreSQL 18, autenticación por contraseña: https://www.postgresql.org/docs/18/auth-password.html | Documentación oficial | Leída por resumen (23-oct-2026) | `scram-sha-256` es el más seguro; `md5` obsoleto; un rol sin contraseña falla siempre con autenticación por contraseña | — |
| DAS v0.13, ADR-013, ADR-027, ADR-029, ADR-031, ADR-032 | Documentos del proyecto | Releídos | `peer` sin contraseñas, una conexión por petición, temporizador de cada minuto, archivo de privilegios idempotente | — |

## 4. Lo que propone el asistente y el solicitante no decidió
- El umbral de 1 000 ms de las consultas lentas.
- Los nombres de los roles, del grupo del socket y de la base: sin decidir.
- Usar un mapa de `pg_ident.conf` o un usuario del sistema con el nombre del rol dueño para las migraciones: sin decidir (pendiente de ADR-027).
- La rotación y la retención de los registros: sin decidir (fase 6).

## 5. Qué no se hizo
- No se instaló ni configuró nada; es etapa A.
- No se verificó dónde pone Ubuntu 26.04 el socket, su grupo ni sus valores por defecto de `pg_hba.conf`.
- No se probó que el grupo del socket permita a todos los servicios conectarse.
- No se investigó cómo guarda GitHub las credenciales de la base de pruebas.
- No se comprobó si Lynis revisa las contraseñas de los roles.
- Sin el registro de conexiones, un acceso inesperado del rol dueño no deja rastro en PostgreSQL: queda el registro del sistema y la auditoría de la aplicación.

## 6. Estado de las medidas de endurecimiento (actualizado)
| N.º | Medida | Estado |
|---|---|---|
| 1 y 2 | Marco y verificación (CIS) | Sustituidas por la actualización (c) |
| 3 a 8 y 12 | SSH, firewall, actualizaciones, servicios y systemd, HTTPS y cabeceras, Django | Decididas ([actualizaciones (o) a (t)](../2026-10-23o_endurecimiento-01-acceso-ssh/CAMBIOS.md)), integradas en el DAS v0.13 |
| 9 | Revisión crítica con otra persona antes de datos reales | Pendiente |
| 11 | Gunicorn por socket Unix | Pendiente |
| 13 | Nginx (`server_tokens`) | Pendiente (el tope de subida, los hosts desconocidos y el límite de solicitudes ya están decididos) |
| **15 a 18** | **PostgreSQL** | **Decididas (esta actualización)** |

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
