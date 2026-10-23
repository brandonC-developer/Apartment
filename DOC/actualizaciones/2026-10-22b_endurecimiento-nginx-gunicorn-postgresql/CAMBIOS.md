# Actualización 2026-10-22 (b) — Endurecimiento de Nginx, Gunicorn y PostgreSQL; replanteo del PDF de CIS

**Fecha:** 2026-10-22
**Documentos afectados:** [README de la fase 6](../../fase-6-despliegue-operacion/README.md) y [DOC/README.md](../../README.md). No se edita ningún documento versionado.
**Continúa:** [2026-10-22 investigación del endurecimiento](../2026-10-22_investigacion-endurecimiento-servidor/CAMBIOS.md)
**Estado:** investigación; las recomendaciones son **propuestas del asistente**, ninguna está decidida ni aprobada.

## 1. Motivo
El solicitante pidió investigar Nginx, Gunicorn y PostgreSQL y replantear el uso del PDF de CIS (propuesta 2 de la actualización anterior).

## 2. Registro de fuentes
Consultadas el 22-oct-2026 con WebFetch (la página se convierte a texto y una herramienta responde a una pregunta; no es lectura íntegra por el asistente). Los ejemplos de código que la herramienta añadió y que **no** están en la página se descartaron o se marcan como "ejemplo del asistente".

| # | Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|---|
| G1 | Gunicorn, [Deploying Gunicorn](https://gunicorn.org/deploy/) | Documentación oficial | Página abierta | Ejecutar detrás de un proxy; con workers síncronos el proxy debe almacenar en búfer a los clientes lentos o hay riesgo de denegación de servicio; Nginx cierra la conexión si el `Host` no coincide; `forwarded-allow-ips` debe listar solo los proxies (`'*'` es peligroso si alguien llega directo a Gunicorn); con socket Unix `REMOTE_ADDR` queda vacío; unidad de socket con `SocketUser`, `SocketGroup` y `SocketMode=0660`; sugiere `DynamicUser=true` y `ProtectSystem=strict` | Los usuarios del ejemplo son de relleno (`someuser`) |
| G2 | Gunicorn, [Settings](https://gunicorn.org/reference/settings/) | Documentación oficial | Página abierta | Valores por defecto: `forwarded_allow_ips` `127.0.0.1,::1`; `limit_request_line` 4094; `limit_request_fields` 100; `limit_request_field_size` 8190; `timeout` 30; `max_requests` 0; `umask` 0 | La versión de Gunicorn de la página no se verificó contra la que instalará Ubuntu 26.04 |
| N1 | Nginx, [ngx_http_core_module](https://nginx.org/en/docs/http/ngx_http_core_module.html) | Documentación oficial | Página abierta | Valores por defecto: `server_tokens on`, `client_max_body_size 1m`, `client_body_timeout 60s`, `client_header_timeout 60s`, `keepalive_timeout 75s`, `large_client_header_buffers 4 8k`; `return 444` cierra la conexión sin respuesta (la directiva `return` se define en otro módulo, no leído) | — |
| N2 | Nginx, [ngx_http_limit_req_module](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html) | Documentación oficial | Página abierta | Sintaxis de `limit_req_zone`, `limit_req`, `burst`, `nodelay`; `limit_req_status` por defecto 503 | El ejemplo de protección del inicio de sesión lo construyó la herramienta, no la página |
| P1 | PostgreSQL, [pg_hba.conf](https://www.postgresql.org/docs/18/auth-pg-hba-conf.html) | Documentación oficial | Página abierta | Sin registro `local` se deniegan los sockets Unix; `peer` solo para conexiones locales; `scram-sha-256` es el método de contraseña; se usa el primer registro que coincide, sin alternativas; `trust` permite entrar como cualquier usuario; `md5` está en desuso; vista `pg_hba_file_rules` para comprobar errores; además hace falta el privilegio `CONNECT` | — |
| P2 | PostgreSQL, [Privilegios](https://www.postgresql.org/docs/18/ddl-priv.html) | Documentación oficial | Página abierta | `PUBLIC` recibe por defecto `CONNECT` y `TEMPORARY` en la base y `EXECUTE` en funciones; el dueño puede revocarlos; `ALTER DEFAULT PRIVILEGES` cambia lo que reciben los objetos futuros | Los bloques de SQL de "endurecimiento" que acompañaban el resumen son de la herramienta, no de la página |
| P3 | PostgreSQL, [Notas de la versión 15](https://www.postgresql.org/docs/18/release-15.html) | Documentación oficial | Página abierta | Desde la 15 `PUBLIC` ya no tiene `CREATE` en el esquema `public` de bases nuevas; el dueño pasa a `pg_database_owner`; una restauración conserva los permisos anteriores | — |
| P4 | PostgreSQL, [Conexión](https://www.postgresql.org/docs/18/runtime-config-connection.html) | Documentación oficial | Página abierta | `listen_addresses` por defecto `localhost` (vacío = solo sockets Unix); `unix_socket_permissions` por defecto `0777` ("cualquiera puede conectar"), alternativas `0770` y `0700`; `password_encryption` por defecto `scram-sha-256`; `ssl` por defecto `off`; `ssl_min_protocol_version` `TLSv1.2` | Los valores por defecto de Ubuntu/Debian pueden diferir de los del código fuente: **sin verificar** |
| P5 | PostgreSQL, [Registro](https://www.postgresql.org/docs/18/runtime-config-logging.html) | Documentación oficial | Página abierta | Por defecto no se registran conexiones, desconexiones ni sentencias; `log_statement` "puede revelar datos sensibles e incluso contraseñas en texto claro"; `log_parameter_max_length` por defecto -1 (registra completos) | La configuración "ilustrativa" que traía el resumen es de la herramienta |
| C1 | CIS, [Benchmark de PostgreSQL](https://www.cisecurity.org/benchmark/postgresql) | Estándar | Página abierta; PDF no abierto | Existe el benchmark para PostgreSQL 18 (1.0.0) | No se leyeron los controles |
| C2 | CIS, [Benchmark de NGINX](https://www.cisecurity.org/benchmark/nginx) | Estándar | Página abierta; PDF no abierto | Existe NGINX 3.1.0; la página lo marca "CIS SecureSuite Members Only" | No se leyeron los controles; el acceso libre del PDF queda en duda |
| C3 | CIS, [Descarga de benchmarks](https://learn.cisecurity.org/benchmarks) | Estándar | Página abierta | Hay que llenar un formulario (nombre, organización, sector, cargo, correo, país) y aceptar el aviso de privacidad; "gratis, uso no comercial"; la página no define "uso comercial" ni ofrece licencia comercial | Términos del PDF mismo sin leer |
| L1 | CISOfy, [Lynis](https://cisofy.com/lynis/) | Herramienta de auditoría (GPL) | Página abierta; no se instaló ni ejecutó | Auditor de seguridad de código abierto para Linux, con cientos de pruebas, informe y registro | No dice nada de uso comercial; no se verificó su cobertura de Ubuntu 26.04 |
| W1 | Búsqueda: guías de despliegue de Gunicorn (versiones 19.x y 20.x) | Resultados de búsqueda | Solo resultados | Confirma lo de G1 en versiones anteriores | No se usa como respaldo único |

**No se verificó:** los controles de los benchmarks CIS (ningún PDF abierto); los valores por defecto de los paquetes de Ubuntu 26.04 para Nginx, Gunicorn y PostgreSQL; ninguna guía de endurecimiento propia de Nginx (el proveedor no publica una; no se buscó una de terceros reconocida); documentación de systemd sobre `RestrictAddressFamilies`.

## 3. Hallazgos
- **N1.** Con el diseño ya decidido (ADR-029: conexión por socket local; ADR-027: roles con autenticación `peer`), la superficie de PostgreSQL ya es mínima: sin contraseñas y sin TCP. Lo que falta es confirmarlo en el servidor (`listen_addresses`, `pg_hba.conf`, permisos del socket).
- **N2.** El `unix_socket_permissions` por defecto es `0777` en el código fuente (P4). Con `peer` solo entra el usuario del sistema que coincide con el rol, pero conviene estrecharlo; el valor que usa Ubuntu no se verificó.
- **N3.** Gunicorn por socket Unix deja `REMOTE_ADDR` vacío (G1): la IP del cliente para la auditoría (RF de eventos de seguridad) debe leerse de `X-Forwarded-For` que ponga Nginx, y Django solo debe confiar en esa cabecera tras Nginx.
- **N4.** Los límites por defecto de Gunicorn y Nginx (G2, N1) ya son razonables; el riesgo no está en los valores sino en dejar Gunicorn alcanzable sin Nginx.
- **N5.** PostgreSQL no registra conexiones por defecto (P5): sin cambio no habría rastro de accesos al servidor de base de datos.

## 4. Recomendaciones (propuestas del asistente; ninguna decidida)
| N.º | Propuesta | Fundamento |
|---|---|---|
| 11 | **Gunicorn:** escuchar solo en un socket Unix, con `SocketMode=0660` y el grupo del usuario de Nginx; `forwarded_allow_ips` solo para el socket local; dejar los límites de solicitud por defecto | G1, G2 |
| 12 | **Gunicorn y systemd:** usuario sin privilegios (o `DynamicUser=true`) y `ProtectSystem=strict`, ya propuestos en la recomendación 6 anterior | G1, F15 |
| 13 | **Nginx:** `server_tokens off`; bloque por defecto que cierre con `return 444` los `Host` desconocidos (la guía de Gunicorn y la de Django lo piden); `client_max_body_size` ajustado al tamaño de la foto de la cédula (valor de diseño pendiente) y más alto solo en la ruta que sube archivos; búfer de proxy activado | N1, G1, F11 |
| 14 | **Nginx, límite de intentos:** `limit_req` en la ruta de inicio de sesión y de restablecimiento, además del bloqueo de cuenta de la aplicación. Cuál de las dos capas manda es decisión de diseño | N2 |
| 15 | **PostgreSQL, red:** `listen_addresses = ''` (solo socket) y `unix_socket_permissions` en `0770` con el grupo adecuado, confirmando antes qué valor trae Ubuntu | P4 |
| 16 | **PostgreSQL, acceso:** `pg_hba.conf` solo con registros `local` y `peer` para los tres roles del ADR-027, sin `trust`; comprobar con `pg_hba_file_rules`; revocar `CONNECT` y `TEMPORARY` a `PUBLIC` y `CREATE` en `public` | P1, P2, P3 |
| 17 | **PostgreSQL, registro:** registrar conexiones y desconexiones; **no** usar `log_statement = all` (revela datos, incluso contraseñas); decidir si `ddl` basta | P5 |
| 18 | **Contraseñas de base de datos:** si alguna vez hay una, `scram-sha-256` (ya es el valor por defecto) | P1, P4 |

## 5. Replanteo del PDF de CIS
Lo que se supo después de la investigación anterior:
- Descargar el PDF exige llenar un formulario con datos personales; yo no puedo hacerlo por el solicitante.
- La descarga es "gratis para uso no comercial" (C3), y la página no dice qué es "uso comercial". El SGA gestiona alquileres del propio solicitante: **si eso cuenta como comercial es una pregunta de licencia, no técnica**, y no la resuelve el asistente.
- Los benchmarks de NGINX figuran como "solo miembros" (C2); el de PostgreSQL 18 y el de Ubuntu 26.04 existen (C1, F1) pero no están leídos.

| Opción | Qué implica | Costo y riesgo |
|---|---|---|
| A. Descargar los tres PDF | Formulario personal y aceptar el uso no comercial | Duda de licencia; el de NGINX quizá no sea accesible |
| B. **No depender del PDF (propuesta del asistente)** | Usar la documentación oficial ya leída (Ubuntu, Nginx, Gunicorn, PostgreSQL, Django, systemd), OWASP y NIST como base, y **Lynis** (GPL) para auditar el servidor y dejar un informe como evidencia | Sin los controles numerados de CIS; Lynis no se ha probado en 26.04 |
| C. Pedir licencia o membresía a CIS | Contacto con CIS; costo no verificado | Dinero y trámite antes de empezar |

**Propuesta:** B ahora, y A solo si el solicitante decide que su uso es no comercial; si no, C se reevalúa cuando haya presupuesto. En cualquier caso, **no se afirma conformidad con CIS** mientras no se lean sus controles.

## 6. Decisiones y preguntas
| Pregunta | Respuesta | Decisión |
|---|---|---|
| ¿Se usa el PDF de CIS como base? | Pendiente | Ninguna |
| ¿Se acepta Lynis como herramienta de auditoría? | Pendiente | Ninguna |
| ¿Cuál es el límite de tamaño de subida (foto de la cédula)? | Pendiente | Ninguna (valor de diseño) |

## 7. Pendientes
- Verificar en una instalación real los valores por defecto de Ubuntu 26.04 (`listen_addresses`, socket, `pg_hba.conf`, versiones de Nginx y Gunicorn); se puede hacer en la WSL de la etapa A.
- Probar Lynis en esa instalación y registrar el resultado.
- Reflejar lo que se decida en una versión nueva del DAS y en el procedimiento de la fase 6.

## 8. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
