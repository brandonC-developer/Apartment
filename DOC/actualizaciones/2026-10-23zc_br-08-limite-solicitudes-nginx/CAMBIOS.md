# Actualización 2026-10-23 (zc) — BR-08: límite de solicitudes por IP en Nginx (propuesta 14) y riesgo AM-04

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el DAS (ADR-032), el modelo de amenazas (versión nueva) y el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** brecha BR-08 y amenazas AM-01, AM-04 y AM-10 del [modelo de amenazas v0.1](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.1_borrador.md); es la propuesta 14 de la [actualización 2026-10-22 (b)](../2026-10-22b_endurecimiento-nginx-gunicorn-postgresql/CAMBIOS.md) y estaba prevista en la [actualización 2026-10-23 (t)](../2026-10-23t_endurecimiento-06-django/CAMBIOS.md). Sigue a la [BR-04](../2026-10-23zb_br-04-dependencias-python/CAMBIOS.md)
**Estado:** decisiones registradas; documentos sin cambiar; no aprobado

## 1. Corrección a lo dicho antes
En la [actualización 2026-10-23 (t)](../2026-10-23t_endurecimiento-06-django/CAMBIOS.md) y en el modelo de amenazas se presentó el límite por IP de Nginx como mitigación de **AM-04** (usar el contador por cuenta de RF-27 para dejar fuera al administrador). **No lo es:** con cinco fallos la cuenta entra en espera aunque Nginx limite la tasa, y un atacante con varias IP lo esquiva. El límite de Nginx solo frena la fuerza bruta desde una IP y los abusos groseros. Lo que reduce AM-04 es el diseño de RF-27 y CA-68: espera con tope de una hora, sin bloqueo permanente y con el restablecimiento de contraseña siempre disponible.

## 2. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Qué rutas se limitan y con qué tasas? | "Dos zonas: autenticación 6 por minuto y general 10 por segundo" (recomendada por el asistente) | `limit_req_zone` por `$binary_remote_addr`: **zona de autenticación** (inicio de sesión, segundo factor, código de recuperación, solicitud y confirmación del restablecimiento) con `rate=6r/m`, `burst=6`, `nodelay`; **zona general** (el resto) con `rate=10r/s`, `burst=30`, `nodelay`. Cada zona de `1m`. Las tasas son propuesta del asistente, sin fuente, y se calibran en la etapa B |
| 2 | ¿Cómo responde Nginx y cómo se calibra? | "429, registro warn y modo de prueba antes de activar" (recomendada) | `limit_req_status 429`, `limit_req_log_level warn`, y `limit_req_dry_run on` durante las pruebas de la etapa B hasta comprobar los números; el paso a modo real queda como tarea de la fase 6; los rechazos de la zona de autenticación se revisan una vez al año |
| 3 | ¿Aceptas el riesgo AM-04? | "Aceptarlo como está, con el restablecimiento disponible" (recomendada) | **RF-27 y CA-68 sin cambios**; AM-04 queda como **riesgo residual medio aceptado por el solicitante** (23-oct-2026). No se cambia el contador a IP y cuenta, no se usa cookie de dispositivo ni CAPTCHA |

## 3. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Nginx, módulo `limit_req`: https://nginx.org/en/docs/http/ngx_http_limit_req_module.html | Documentación oficial | Leída por resumen (WebFetch, 23-oct-2026) | Sintaxis de `limit_req_zone` y `limit_req` (`rate`, `burst`, `nodelay`, `delay`); `10m` guarda unas 16 000 direcciones; `limit_req_status` (503 por defecto), `limit_req_log_level` (`error` por defecto), `limit_req_dry_run` (desde 1.17.1); `limit_req` por `location` | Versión de Nginx de Ubuntu 26.04 sin verificar |
| OWASP, Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | Guía de experto reconocido | Leída por resumen (23-oct-2026) | El contador debe asociarse a la cuenta y no a la IP; bloqueo exponencial; CAPTCHA como defensa en profundidad; el bloqueo puede usarse para denegación de servicio y una mitigación es dejar disponible el flujo de contraseña olvidada | **No trata la limitación por IP** |
| RFC 6585, código 429 | Especificación | **De memoria del asistente; no se verificó en esta sesión** | — | — |
| ERS v1.14, RF-27 y CA-68; DAS v0.12, ADR-032 | Documentos del proyecto | Releídos | Contador por cuenta, espera de 1 min a 1 h, sin bloqueo permanente, restablecimiento disponible | — |

## 4. Lo que propone el asistente y el solicitante no decidió
- Las tasas y el tamaño de las zonas, y qué rutas entran en la zona de autenticación.
- Que 429 y `warn` sean la respuesta y el nivel de registro.
- Que la revisión de rechazos sea anual.

## 5. Qué no se hizo
- No se configuró Nginx; es etapa B.
- No se probó que 6 por minuto no moleste al uso normal (inicio de sesión de dos o tres solicitudes).
- No se verificó la versión de Nginx de Ubuntu 26.04 ni que traiga `limit_req_dry_run`.
- No se investigó CAPTCHA ni se evaluó fail2ban u otra herramienta que actúe sobre los registros.
- Un atacante distribuido o persistente puede seguir dejando la cuenta en espera de forma intermitente: es el riesgo que el solicitante acepta.
- No se cambió RF-27, CA-68 ni la ERS.

## 6. Qué falta hacer
1. DAS: añadir la configuración al ADR-032 (versión nueva o ajuste consolidado).
2. Modelo de amenazas v0.2: BR-08 cerrada; AM-04 con riesgo residual **aceptado** y la corrección de la sección 1; AM-01 y AM-10 ajustadas.
3. Fase 6: configuración de Nginx, calibración con el modo de prueba y paso a modo real.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
