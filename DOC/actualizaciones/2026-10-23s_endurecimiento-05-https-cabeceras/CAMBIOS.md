# Actualización 2026-10-23 (s) — Endurecimiento, medida 6: HTTPS y cabeceras (propuesta 7)

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en una versión nueva del DAS (ADR-023) y en el procedimiento de la fase 6. [DOC/README.md](../../README.md). Además, una **corrección** a la [medida 5](../2026-10-23q_endurecimiento-03-actualizaciones/CAMBIOS.md) (sección 7 nueva de esa actualización: puertos del SMTP)
**Origen:** propuesta 7 de la [actualización 2026-10-22](../2026-10-22_investigacion-endurecimiento-servidor/CAMBIOS.md); sigue a la [medida 4 y 5 (servicios y systemd)](../2026-10-23r_endurecimiento-04-servicios-systemd/CAMBIOS.md)
**Estado:** decisión registrada; documentos sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿El tráfico web pasa por el proxy de Cloudflare? | "No: DNS only con Certbot en el servidor" (recomendada por el asistente) | El registro del sitio queda en **DNS only** (sin proxy de Cloudflare) y el certificado lo emite Certbot (Let's Encrypt) en el servidor, como dice ADR-023. Los puertos 80 y 443 quedan abiertos al mundo en el firewall (cierra la duda sobre los rangos de Cloudflare de la [medida 4](../2026-10-23p_endurecimiento-02-firewall/CAMBIOS.md)). Se puede cambiar más adelante activando el proxy |
| 2 | ¿Qué versiones de TLS acepta el servidor? | "TLS 1.3 y 1.2" (recomendada) | TLS 1.3 y 1.2; sin 1.0, 1.1 ni compresión. Los conjuntos de cifrado **no se fijan hoy**: se toman de una referencia vigente al montar el servidor (etapa B) y se comprueban con un escáner externo |
| 3 | ¿Cómo se activa HSTS? | "En etapas, sin includeSubDomains ni preload" (recomendada) | `max-age` corto al empezar (propuesta del asistente: 300 segundos; la documentación de Django cita 3600 como ejemplo); cuando el HTTPS funcione bien en producción, 31 536 000 (un año). Sin `includeSubDomains` ni `preload` en la v1 |
| 4 | ¿Dónde se ponen las cabeceras y la redirección? | "Redirección y hosts en Nginx; cabeceras y cookies en Django" (recomendada) | **Nginx:** redirección de HTTP a HTTPS; bloque por defecto con `return 444` para un `Host` desconocido; `X-Forwarded-Proto` sobrescrito (no el que mande el cliente). **Django:** HSTS (`SECURE_HSTS_SECONDS`), `nosniff`, `Referrer-Policy`, `X-Frame-Options`, cookies de sesión y CSRF con `Secure`, y `SECURE_PROXY_SSL_HEADER` apuntando a esa cabecera, solo porque Nginx la sobrescribe |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Cloudflare, estado del proxy: https://developers.cloudflare.com/dns/proxy-status/ | Documentación del proveedor | Leída por resumen (WebFetch, 23-oct-2026) | Con proxy el tráfico pasa por Cloudflare, oculta la IP de origen y aplica DDoS, caché y WAF; sin proxy va directo y la IP es visible | Que Cloudflare "vea" las fotos de cédulas con el proxy es inferencia del asistente, y su relación con DP-19 queda sin dictamen |
| Cloudflare, modos SSL/TLS: https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/ | Documentación del proveedor | Leída por resumen (23-oct-2026) | Modos Off, Flexible, Full y Full (strict); recomienda Full o Full (strict) | Solo aplica si algún día se activa el proxy |
| OWASP, TLS Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html | Guía reconocida | Leída en la investigación del 22-oct-2026 | TLS 1.3 por defecto y 1.2 por compatibilidad; desactivar 1.0 y 1.1; sin compresión | La curva citada para Nginx exige un OpenSSL reciente, sin verificar |
| Mozilla, Server Side TLS: https://wiki.mozilla.org/Security/Server_Side_TLS | Guía reconocida | Página abierta el 23-oct-2026 | **Solo dice que el contenido se trasladó** a un Confluence interno y a docs.tlsref.org; última edición 11-jun-2026 | No se pudo leer el contenido de los perfiles |
| docs.tlsref.org: https://docs.tlsref.org/ | Guía comunitaria | Leída por resumen (23-oct-2026) | Existen los perfiles Modern e Intermediate | Sin detalles de versiones ni cifrados en lo leído |
| Certbot, uso: https://eff-certbot.readthedocs.io/en/stable/using.html | Documentación oficial | Leída por resumen (hasta el carácter 100 000 de 104 486) | `certbot renew` renueva cuando queda menos de un tercio de la vida; la renovación suele venir programada | No describe `options-ssl-nginx.conf` ni su configuración TLS |
| OWASP, HSTS Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html | Guía reconocida | Leída por resumen (23-oct-2026) | Ejemplo estable de 2 años; empezar con un `max-age` muy corto; `includeSubDomains` bloquea subdominios solo HTTP; `preload` tiene consecuencias permanentes | No da un número para el arranque |
| Django, middleware: https://docs.djangoproject.com/en/5.2/ref/middleware/ | Documentación oficial | Leída por resumen (23-oct-2026) | Ajustes `SECURE_HSTS_SECONDS`, `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_REFERRER_POLICY`, `SECURE_SSL_REDIRECT`, `SECURE_PROXY_SSL_HEADER` y `X_FRAME_OPTIONS`; HSTS empezar con poco (ejemplo 3600) y un año habitual; `SECURE_PROXY_SSL_HEADER` solo si el proxy elimina y reemplaza la cabecera | La herramienta indicó que los valores por defecto (HSTS 0, nosniff true, referrer `same-origin`, `X-Frame-Options` `DENY`) vienen de la referencia de ajustes y **no** de esta página; no se verificaron en ella |
| Django (lista de despliegue), OWASP Django Security Cheat Sheet, Gunicorn (Deploying) | Documentación oficial y guía | Leídas en las investigaciones del 22-oct-2026 | Redirección a HTTPS y rechazo de hosts desconocidos en el servidor web; cabeceras y cookies seguras; Nginx cierra la conexión si el `Host` no coincide | — |

## 3. Lo que propone el asistente y el solicitante no decidió
- Los valores `max-age` (300 s al inicio, un año al final).
- Que el proxy de Cloudflare se descarte por su relación con DP-19: es inferencia del asistente.
- Que la cabecera `X-Forwarded-Proto` sea la elegida para `SECURE_PROXY_SSL_HEADER`.
- **Pendientes explícitos, no decididos:** la política de contenido (CSP; Django 5.2 no la trae integrada y la aplicación usa algo de JavaScript propio, RF-50); el registro DNS **CAA**; los conjuntos de cifrado; y OCSP stapling.

## 4. Corrección que apareció al preparar esta medida
La decisión 3 de la medida 5 (correo de errores por el SMTP de Resend) debe usar los puertos **2465 o 2587**, porque DigitalOcean bloquea 25, 465 y 587 (dato ya recogido en el DAS). No se verificó que esos dos pasen. Está anotado en la [actualización (q)](../2026-10-23q_endurecimiento-03-actualizaciones/CAMBIOS.md).

## 5. Qué no se hizo
- No se aplicó nada: no hay servidor ni dominio.
- No se verificaron los valores por defecto de Django en su página de ajustes ni la configuración que instala el plugin de Nginx de Certbot.
- No se fijaron cifrados, CAA ni CSP.
- Que el sitio sirva solo HTTPS y que la redirección funcione se prueba en la etapa B.

## 6. Estado de las medidas de endurecimiento (actualizado)
| N.º | Medida | Estado |
|---|---|---|
| 1 y 2 | Marco y verificación (CIS) | Sustituidas por la decisión de la actualización (c) |
| 3 | Acceso remoto por SSH | Decidida ([actualización (o)](../2026-10-23o_endurecimiento-01-acceso-ssh/CAMBIOS.md)) |
| 4 | Firewall | Decidida ([actualización (p)](../2026-10-23p_endurecimiento-02-firewall/CAMBIOS.md)); la duda de Cloudflare queda cerrada por la decisión 1 de esta |
| 5 | Actualizaciones automáticas y reinicio | Decidida ([actualización (q)](../2026-10-23q_endurecimiento-03-actualizaciones/CAMBIOS.md)), con la corrección de puertos |
| 6 y 12 | Servicios bajo usuarios sin privilegios y `systemd` | Decididas ([actualización (r)](../2026-10-23r_endurecimiento-04-servicios-systemd/CAMBIOS.md)) |
| **7** | **HTTPS y cabeceras** | **Decidida (esta actualización)**, salvo cifrados, CAA y CSP |
| 8 | Django (`check --deploy`, `SECRET_KEY`, límite de intentos, archivos subidos) | Pendiente |
| 9 | Revisión crítica con otra persona antes de datos reales | Pendiente |
| 11 | Gunicorn por socket Unix | Pendiente |
| 13 y 14 | Nginx (`server_tokens`, hosts desconocidos, límite de intentos) | Pendiente (el tope de subida ya está decidido; el rechazo de hosts desconocidos quedó decidido aquí) |
| 15 a 18 | PostgreSQL (red, acceso, registro, contraseñas) | Pendiente |

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
