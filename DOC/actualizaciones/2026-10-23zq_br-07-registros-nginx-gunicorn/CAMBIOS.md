# Actualización 2026-10-23 (zq) — BR-07: qué registran Nginx y Gunicorn, y por cuánto tiempo

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el DAS (ADR-032, pendiente "rotación y retención de los registros"; ADR-017), el modelo de amenazas (versión nueva: BR-07, AM-26) y el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** brecha BR-07 y amenaza AM-26 del [modelo de amenazas v0.3](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.3_borrador.md); PostgreSQL ya decidido en la [actualización (zg)](../2026-10-23zg_endurecimiento-07-postgresql/CAMBIOS.md)
**Estado:** decisión registrada; documentos sin cambiar; no aprobado

## 1. Pregunta, respuesta y decisión
| Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|
| ¿Qué registran Nginx y Gunicorn y por cuánto tiempo? | "Formato propio sin parámetros, 14 días" (recomendada por el asistente) | **Nginx:** formato propio con IP, hora, método, ruta (`$uri`, sin la cadena de consulta), estado, bytes y tiempo de respuesta; no se usa `combined`. **Gunicorn:** sin registro de acceso (lo hace Nginx); registro de errores a journald. **Rotación diaria y 14 días** para el registro de Nginx; con `postrotate` que avisa a Nginx (señal USR1) |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Documentación de Gunicorn (ajustes): https://docs.gunicorn.org/en/21.0.1/settings.html | Documentación del proveedor | **Solo resultados de búsqueda** | El registro de acceso solo funciona si se indica `accesslog`; el registro de errores sale por defecto a stderr; `capture_output` está apagado | Versión 21.0.1; no se comprobó la que traerá Ubuntu 26.04 |
| OWASP, Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | Guía de experto reconocido | **No se abrió**; extractos y réplicas de terceros en resultados de búsqueda | No registrar de más ni de menos; no guardar información sensible; los datos en cadenas de consulta GET pueden registrar valores sensibles | **No se encontró su guía de retención**; el plazo de 14 días no tiene fuente |
| Guía de DigitalOcean sobre registros y rotación de Nginx en Ubuntu: https://digitalocean.com/community/articles/how-to-configure-logging-and-log-rotation-in-nginx-on-an-ubuntu-vps | Tutorial del proveedor | **Solo resultados de búsqueda** | `combined` es el formato por defecto; `logrotate` viene instalado y Nginx trae su archivo en `/etc/logrotate.d/nginx`; hace falta avisar a Nginx tras rotar | Que el paquete rote 14 días **no se confirmó** (de memoria) |
| Que `$request` incluya la cadena de consulta y `$uri` no | Conocimiento del asistente | **No verificado** en la documentación de Nginx | Motivo del formato propio | A comprobar en la etapa A |

## 3. Lo que propone el asistente y el solicitante no decidió
- Los **14 días** y la rotación diaria: sin fuente; deben conciliarse con la retención de datos (DP-18) y con el plazo para investigar un incidente (RF-46).
- Los campos exactos del formato, incluido el tiempo de respuesta.
- Que la búsqueda del inquilino pueda viajar en la URL: no se revisó el diseño de RF-03; si se envía por `POST`, el motivo pierde fuerza (el formato propio sigue siendo válido).
- Que la IP en el registro de Nginx sea un dato personal sujeto a la Ley 8968: **sin dictamen** (DP-17, DP-19).

## 4. Qué no se hizo
- No se escribió la configuración de Nginx ni el formato; no se verificó en Ubuntu 26.04 la rotación por defecto.
- No se decidió la rotación y retención del registro de errores de journald, del de auditoría de la aplicación ni del de PostgreSQL.
- No se actualizaron el DAS ni el modelo de amenazas.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
