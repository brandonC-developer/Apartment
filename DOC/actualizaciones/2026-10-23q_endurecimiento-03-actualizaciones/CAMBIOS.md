# Actualización 2026-10-23 (q) — Endurecimiento, medida 3: actualizaciones automáticas (propuesta 5)

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en una versión nueva del DAS y en el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** propuesta 5 de la [actualización 2026-10-22](../2026-10-22_investigacion-endurecimiento-servidor/CAMBIOS.md); sigue a la [medida 4 (firewall)](../2026-10-23p_endurecimiento-02-firewall/CAMBIOS.md)
**Estado:** decisión registrada; documentos sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Se permite el reinicio automático cuando una actualización de seguridad lo requiera? | "Sí, en una hora fija de madrugada" (recomendada por el asistente) | `unattended-upgrades` aplica las actualizaciones de seguridad (comportamiento por defecto de Ubuntu) y el servidor se reinicia solo cuando una actualización lo requiera |
| 2 | ¿A qué hora se reinicia? | "04:00 hora de Costa Rica" (recomendada) | 04:00 hora de Costa Rica (10:00 UTC; Costa Rica no tiene horario de verano). La hora se fija en UTC o con la zona del servidor en `America/Costa_Rica` |
| 3 | ¿Cómo te enteras de un error? | "Correo solo si hay error, por SMTP de Resend" (recomendada) | `Unattended-Upgrade::Mail` a la dirección del solicitante con `MailReport` `only-on-error`, mediante un cliente de correo mínimo que envíe por el SMTP de Resend con una API key propia del servidor (distinta de la de la aplicación). El registro en `/var/log/unattended-upgrades/` queda como respaldo |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Canonical, actualizaciones automáticas: https://ubuntu.com/server/docs/how-to/software/automatic-updates/ | Documentación del proveedor | Leída por resumen (WebFetch, 23-oct-2026) | Actualizaciones de seguridad automáticas por defecto; `Automatic-Reboot` (false por defecto), `Automatic-Reboot-Time` (`hh:mm` local; "now" por defecto), `Automatic-Reboot-WithUsers` (true por defecto); `Mail` vacío y `MailReport` (`always`, `only-on-error`, `on-change`); `needrestart` reinicia los servicios afectados desde Ubuntu 24.04; archivos `50unattended-upgrades` y `20auto-upgrades` | No menciona Livepatch; la página puede corresponder a una versión anterior a 26.04, sin verificar |
| Resend, enviar por SMTP: https://resend.com/docs/send-with-smtp | Documentación del proveedor | Leída por resumen (23-oct-2026) | SMTP en `smtp.resend.com` (puertos 25, 465, 587, 2465, 2587), usuario `resend`, contraseña = API key, dominio verificado; mismos límites que la API | **Sin registros del servidor SMTP para depurar**; los correos por SMTP aparecen en la tabla de emails del panel |
| DAS v0.11, ADR-013, ADR-026 y RNF-09 | Documentos del proyecto | Releídos | Temporizador del proceso diario con `Persistent=yes`; correo con Resend; pérdida tolerable de 24 horas | — |

## 3. Lo que propone el asistente y el solicitante no decidió
- Que un corte de uno o dos minutos de madrugada sea aceptable, y que reiniciar sin supervisión también lo sea: criterio del asistente (decisión de negocio, aceptada por el solicitante).
- La hora de las 04:00 como relación con el proceso diario de las 07:00 y el respaldo.
- Instalar un cliente de correo mínimo y una API key propia para el servidor: no se eligió el programa ni se probó con Resend.
- `Automatic-Reboot-WithUsers`: no se decidió; el valor por defecto reinicia aunque haya una sesión abierta (quedaría una sesión de SSH cortada).

## 4. Qué no se hizo
- No se aplicó nada: no hay servidor.
- **La hora del respaldo diario sigue sin fijarse** en el DAS; debe terminar antes de las 04:00 o empezar después.
- No se probó que `unattended-upgrades` envíe por el SMTP de Resend ni qué cliente de correo usar.
- No se verificó que un reinicio automático deje el servidor operativo (arranque de Nginx, Gunicorn y PostgreSQL); se prueba en la restauración de RNF-09 y en la etapa B.
- No se verificó el valor por defecto de `Automatic-Reboot` ni los demás en Ubuntu 26.04.

## 5. Estado de las medidas de endurecimiento (actualizado)
| N.º | Medida | Estado |
|---|---|---|
| 1 y 2 | Marco y verificación (CIS) | Sustituidas por la decisión de la actualización (c) |
| 3 | Acceso remoto por SSH | Decidida ([actualización (o)](../2026-10-23o_endurecimiento-01-acceso-ssh/CAMBIOS.md)) |
| 4 | Firewall | Decidida ([actualización (p)](../2026-10-23p_endurecimiento-02-firewall/CAMBIOS.md)), salvo la salida y los rangos de Cloudflare |
| **5** | **Actualizaciones automáticas y reinicio** | **Decidida (esta actualización)**, salvo `Automatic-Reboot-WithUsers` y la hora del respaldo |
| 6 y 12 | Servicios bajo usuarios sin privilegios y `systemd` | Pendiente |
| 7 | HTTPS y cabeceras | Pendiente |
| 8 | Django (`check --deploy`, `SECRET_KEY`, límite de intentos, archivos subidos) | Pendiente |
| 9 | Revisión crítica con otra persona antes de datos reales | Pendiente |
| 11 | Gunicorn por socket Unix | Pendiente |
| 13 y 14 | Nginx (`server_tokens`, hosts desconocidos, límite de intentos) | Pendiente (el tope de subida ya está decidido) |
| 15 a 18 | PostgreSQL (red, acceso, registro, contraseñas) | Pendiente |

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |

## 7. Corrección del 23-oct-2026 (hecha al plantear la medida 7)
Al releer el DAS (sección del correo, ADR-026) se vio que **DigitalOcean bloquea los puertos 25, 465 y 587 de los Droplets** (dato ya registrado allí). La página de Resend lista también los puertos **2465 (SMTPS) y 2587 (STARTTLS)**. Por tanto, el SMTP de la decisión 3 debe usar **2465 o 2587**, no 25, 465 ni 587. **No se verificó** que DigitalOcean deje pasar esos dos ni que `unattended-upgrades` funcione con ellos; se prueba en la etapa B. Si no funcionara, quedaría la opción de revisar el registro a mano (la alternativa que se descartó) o enviar el aviso por la API HTTPS de Resend con un guion propio, que no se diseñó.
