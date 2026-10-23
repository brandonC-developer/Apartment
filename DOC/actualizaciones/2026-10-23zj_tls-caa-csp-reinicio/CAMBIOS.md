# Actualización 2026-10-23 (zj) — Cifrados TLS, registro CAA, política de contenido (CSP) y reinicio con sesiones abiertas

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; las decisiones se incorporarán en el DAS (ADR-032, decisiones 3 y 5), el modelo de amenazas (versión nueva: AM-12, AM-23, AM-28 y BR-11) y el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** pendientes de ADR-032 en el [DAS v0.13](../../fase-2-arquitectura/DAS_SGA_001_v0.13_borrador.md) ("cifrados TLS, registro CAA y política de contenido (CSP)", "`Automatic-Reboot-WithUsers`") y brecha BR-11 del [modelo de amenazas v0.2](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.2_borrador.md); sigue a la [actualización (zi)](../2026-10-23zi_salida-firewall-y-hora-respaldo/CAMBIOS.md)
**Estado:** decisiones registradas; documentos sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Qué cifrados acepta el servidor? | "Política OWASP ahora; lista literal del generador vigente al montar" (recomendada por el asistente) | TLS 1.3 y 1.2; en 1.2 solo ECDHE con cifrado autenticado (AES-GCM o ChaCha20-Poly1305), sin CBC, sin transporte de clave RSA y sin DH estático. La lista exacta de `ssl_ciphers` se toma del generador vigente (configurator.tlsref.org) en la etapa B, se comprueba contra esos criterios y se registra en la fase 6; se verifica con un escáner externo (cuál, sin investigar) |
| 2 | ¿Qué registro CAA se publica? | "issue letsencrypt.org + accounturi + http-01" (recomendada) | En la raíz del dominio: `issue "letsencrypt.org"` con el `accounturi` de la cuenta ACME y `validationmethods=http-01`; sin `issuewild`. Se crea **después** de la primera emisión, cuando exista el identificador de la cuenta. Si se pierde la cuenta ACME, hay que actualizar el registro para poder renovar: se anota en la recuperación de la fase 6 |
| 3 | ¿Qué política de contenido (CSP) se adopta? | "Política estricta fija con middleware propio, primero en Report-Only" (recomendada) | Un middleware propio de Django envía `default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' blob:; connect-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'; object-src 'none'`. Sin scripts ni estilos en línea en las plantillas. En la etapa A se despliega como `Content-Security-Policy-Report-Only` y, tras corregir lo que muestre la consola, pasa a modo de bloqueo. `data:` solo si la reducción de fotografías lo necesita. Sin biblioteca de terceros |
| 4 | ¿Se reinicia a las 04:00 aunque haya una sesión de SSH abierta? | "No: Automatic-Reboot-WithUsers en false" (recomendada) | `Automatic-Reboot-WithUsers` en `false`: con una sesión abierta a las 04:00 el reinicio se aplaza a la noche siguiente. Las sesiones de la aplicación web no cuentan |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Nginx, módulo `ssl`: https://nginx.org/en/docs/http/ngx_http_ssl_module.html | Documentación oficial | Leída por resumen (WebFetch, 23-oct-2026) | `ssl_protocols` por defecto `TLSv1.2 TLSv1.3` (desde la 1.23.4); `ssl_ciphers` por defecto `HIGH:!aNULL:!MD5` | Versión de Nginx de Ubuntu 26.04 sin verificar; qué suites incluye ese valor en Ubuntu es deducción del asistente |
| OWASP, TLS Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html | Guía de experto reconocido | Leída por resumen (23-oct-2026) | AEAD en TLS 1.3 y 1.2; evitar CBC; desactivar `TLS_RSA_*` y DH estático; forward secrecy con ECDHE | **No da una lista concreta**; no trata OCSP stapling ni `ssl_prefer_server_ciphers` |
| Mozilla, `ssl-config-generator`: https://github.com/mozilla/ssl-config-generator | Herramienta | Página leída por resumen (23-oct-2026) | Archivado el 28-may-2026 (solo lectura); el proyecto pasó a un grupo comunitario (configurator.tlsref.org) | **No pude abrir los perfiles** ni el generador nuevo; no sé quién lo mantiene |
| Let's Encrypt, CAA: https://letsencrypt.org/docs/caa/ | Documentación del proveedor | Leída por resumen (23-oct-2026) | Sin CAA cualquier CA pública puede emitir; `issue "letsencrypt.org"`; `accounturi` limita a una cuenta ACME; `validationmethods` limita los métodos; reintenta si la consulta falla | Que Certbot use `http-01` con Nginx es supuesto del asistente |
| Cloudflare, tipos de registro DNS: https://developers.cloudflare.com/dns/manage-dns-records/reference/dns-record-types/ | Documentación del proveedor | Leída por resumen (23-oct-2026) | Define el CAA en una línea | No detalla campos ni dice si Cloudflare añade CAA solo |
| OWASP, CSP Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html | Guía de experto reconocido | Leída por resumen (23-oct-2026) | Política estricta sin `'unsafe-inline'`; `frame-ancestors`, `form-action`, `base-uri`, `object-src`; desplegar con Report-Only; CSP es defensa en profundidad | La política concreta es del asistente |
| MDN, CSP: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP | Documentación de referencia | Leída por resumen (23-oct-2026) | Cabeceras y directivas; `'self'`; Report-Only | La herramienta marcó como conocimiento general (no del artículo) lo de `data:`, `blob:`, `connect-src` y `form-action` |
| Canonical, actualizaciones automáticas: https://ubuntu.com/server/docs/how-to/software/automatic-updates/ | Documentación del proveedor | Leída por resumen (actualización (q)) | `Automatic-Reboot-WithUsers` vale `true` por defecto | No dice si avisa de que aplazó el reinicio |
| OWASP, Django Security Cheat Sheet | Guía de experto reconocido | Leída en la investigación del 22-oct-2026 | Django 5.2 no trae CSP integrada (sí desde la 6.0) | — |

## 3. Lo que propone el asistente y el solicitante no decidió
- **La política CSP concreta**, que no se verificó con la interfaz real: puede romper formularios o la reducción de fotografías.
- Que `blob:` sea suficiente para la vista previa y que `data:` no haga falta.
- `validationmethods=http-01`: supuesto de que Certbot usa ese método.
- Qué escáner externo comprueba los cifrados: sin investigar.
- Que OCSP stapling quede sin decidir: no se trató.

## 4. Qué no se hizo
- No se instaló ni configuró nada; no hay servidor, dominio ni cuenta ACME.
- No se escribió la lista literal de cifrados: depende de un generador que no se pudo abrir.
- No se probó que un `accounturi` rompa la renovación al reinstalar Certbot; se anota como riesgo.
- No se escribió el middleware de CSP ni las plantillas.
- No se comprobó si `unattended-upgrades` avisa al aplazar un reinicio por una sesión abierta; una sesión olvidada puede aplazarlo indefinidamente.
- BR-11 (CSP) queda decidida en el sentido de esta actualización, pero el modelo de amenazas todavía la lista como abierta.

## 5. Estado de los pendientes de ADR-032
Quedan **cerrados**: cifrados TLS, registro CAA, política de contenido (CSP), regla de salida de los firewalls (actualización (zi)), hora del respaldo (zi) y `Automatic-Reboot-WithUsers`. Siguen abiertos: OCSP stapling (no tratado), la revisión crítica con otra persona (medida 9), la auditoría con Lynis en la etapa B y las brechas BR-05, 06, 07, 09 y 10 del modelo de amenazas.

## 6. Qué falta hacer
1. DAS v0.14: incorporar las decisiones de PostgreSQL, Gunicorn, Nginx, la salida, la hora del respaldo, el aviso de fallo, los cifrados, el CAA, la CSP y el reinicio.
2. ERS: requisitos nuevos (segundo factor de las cuentas, correo autenticado, aviso de fallo del respaldo).
3. Modelo de amenazas v0.3: BR-11 y BR-12 cerradas; AM-12, AM-23, AM-25 y AM-28 con los controles nuevos.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
