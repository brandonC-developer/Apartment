# Actualización 2026-10-23 (zh) — Endurecimiento, medidas 11 y 13: Gunicorn y Nginx

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el DAS (ADR-032, ADR-029 y ADR-023) y en el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** propuestas 11 y 13 de la [actualización 2026-10-22 (b)](../2026-10-22b_endurecimiento-nginx-gunicorn-postgresql/CAMBIOS.md); sigue a la [medida de PostgreSQL (zg)](../2026-10-23zg_endurecimiento-07-postgresql/CAMBIOS.md) y a las decisiones del [DAS v0.13](../../fase-2-arquitectura/DAS_SGA_001_v0.13_borrador.md)
**Estado:** decisiones registradas; documentos sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 (propuesta 11) | ¿Cómo se crea y protege el socket de Gunicorn? | "Socket de systemd con 0660 y grupo de Nginx, sin TCP" (recomendada por el asistente) | Un archivo `gunicorn.socket` de systemd crea el socket con `SocketUser` el usuario de la aplicación, `SocketGroup` el grupo de Nginx y `SocketMode=0660`; Gunicorn escucha solo ahí, sin puerto TCP. `forwarded_allow_ips` queda con su valor por defecto y se prueba en la etapa A que Django detecta la conexión segura; si no, se pasa a `'*'` solo porque el socket es la única entrada |
| 2 (propuesta 11) | ¿Cuántos procesos y qué límites usa Gunicorn? | "3 workers sync, timeout 30, max_requests 1000" (recomendada) | `workers=3`, `worker_class` `sync`, `timeout=30`, `max_requests=1000`, `max_requests_jitter=100`; límites de petición (`limit_request_line`, `limit_request_fields`, `limit_request_field_size`) con sus valores por defecto. Cierra el pendiente de ADR-029 sobre el número de procesos |
| 3 (propuesta 13) | ¿Qué cabeceras y ajustes usa Nginx hacia Gunicorn? | "server_tokens off y cabeceras sustituidas, amortiguación y 30 s" (recomendada) | `server_tokens off`; `Host $host`; `X-Forwarded-For $remote_addr` y `X-Forwarded-Proto $scheme`, **sustituyendo lo que mande el cliente**; `proxy_buffering on`; `proxy_connect_timeout 10s` y `proxy_read_timeout 30s` (más alto solo en la ruta de subida si la prueba lo exige); la IP de origen de la auditoría sale de `X-Forwarded-For` |

## 2. Hallazgos
- **`umask` por defecto de Gunicorn:** vale `0` y se aplica "a los archivos que escribe Gunicorn, incluidos los sockets Unix"; un socket creado por Gunicorn con ese valor no quedaría restringido. Por eso el socket lo crea systemd. Es una inferencia del asistente de la documentación, no probada.
- **Con socket Unix, `REMOTE_ADDR` queda vacío:** la IP de la auditoría solo puede venir de `X-Forwarded-For`, que es fiable porque Nginx lo sustituye (ADR-032, sin proxy de Cloudflare).
- **Interacción con ADR-032:** la decisión 4 preveía `RuntimeDirectory=` para el directorio del socket; con un socket de systemd se declara de otra manera. Ajuste menor, sin probar.

## 3. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Gunicorn, despliegue: https://gunicorn.org/deploy/ | Documentación oficial | Leída por resumen (WebFetch, 23-oct-2026) | Socket Unix detrás de Nginx; `REMOTE_ADDR` vacío; `gunicorn.socket` con `SocketUser`, `SocketGroup`, `SocketMode`; `forwarded_allow_ips` y la advertencia de `'*'`; amortiguación de clientes lentos con workers `sync`; ejemplos con 3 workers, sin fórmula | — |
| Gunicorn, ajustes: https://gunicorn.org/reference/settings/ | Documentación oficial | Leída por resumen (23-oct-2026) | Valores por defecto de `workers`, `timeout`, `max_requests`, `forwarded_allow_ips`, `umask` (`0`) y los límites de petición | La versión de Gunicorn de Ubuntu 26.04 no se verificó |
| Nginx, `server_tokens`: https://nginx.org/en/docs/http/ngx_http_core_module.html#server_tokens | Documentación oficial | Leída por resumen (23-oct-2026) | `on` por defecto; `off` oculta la versión de la cabecera `Server` y de las páginas de error; ocultar la versión no protege por sí solo | — |
| Nginx, módulo `proxy`: https://nginx.org/en/docs/http/ngx_http_proxy_module.html | Documentación oficial | Leída por resumen (23-oct-2026) | `proxy_buffering on` por defecto; `Host` y `Connection` por defecto; tiempos de 60 s; sintaxis de `proxy_pass` con socket Unix | La versión de Nginx de Ubuntu 26.04 no se verificó |
| DAS v0.13, ADR-013, ADR-023, ADR-029 y ADR-032 | Documentos del proyecto | Releídos | Droplet de 2 GiB y 1 vCPU; una conexión por petición; proceso de Gunicorn por decidir en la fase 6; sin proxy de Cloudflare | — |

## 4. Lo que propone el asistente y el solicitante no decidió
- Los valores numéricos: 3 workers, `timeout` de 30 s, `max_requests` de 1 000 y su jitter, y los tiempos del proxy de 10 s y 30 s.
- Cambiar `forwarded_allow_ips` a `'*'` si la prueba lo exige.
- Los nombres del archivo del socket, del usuario y del grupo de Nginx.

## 5. Qué no se hizo
- No se configuró nada; es etapa A.
- **No se verificó** que Gunicorn confíe en las cabeceras `X-Forwarded-*` que llegan por un socket Unix, ni que Django lea la IP de `X-Forwarded-For` sin configuración extra.
- No se midió el consumo de memoria de tres workers en 2 GiB ni el tiempo de una subida de 5 MiB.
- No se definió una ruta de subida con un tiempo mayor.
- No se verificó la versión de Nginx ni de Gunicorn de Ubuntu 26.04.

## 6. Estado de las medidas de endurecimiento (actualizado)
Con esta actualización quedan decididas **todas las medidas de endurecimiento propuestas el 22-oct-2026, salvo la 9** (revisión crítica con otra persona antes de datos reales), que depende de alguien externo. Quedan, además, pendientes que no son medidas numeradas: cifrados TLS, registro CAA, política de contenido (CSP), regla de salida de los firewalls, hora del respaldo y `Automatic-Reboot-WithUsers`.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
