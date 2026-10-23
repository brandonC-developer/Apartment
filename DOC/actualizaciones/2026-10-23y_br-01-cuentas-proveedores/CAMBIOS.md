# Actualización 2026-10-23 (y) — BR-01: protección de las cuentas de los proveedores

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en una ERS nueva (requisito), el DAS (ADR-032 o uno nuevo), el modelo de amenazas (versión nueva) y el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** brecha BR-01 y amenazas AM-03 y AM-23 del [modelo de amenazas v0.1](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.1_borrador.md), de la [actualización 2026-10-23 (x)](../2026-10-23x_modelo-amenazas-v0.1/CAMBIOS.md)
**Estado:** decisiones registradas; documentos sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Qué segundo factor se exige en las cuentas de los proveedores? | "El mejor disponible en cada uno, nunca SMS" (recomendada por el asistente) | Llave de seguridad o passkey en Cloudflare y GitHub; app autenticadora en DigitalOcean y Resend (no se verificó otra cosa en ellos); nunca SMS; dos factores registrados por cuenta y códigos de respaldo guardados fuera del dispositivo |
| 2 | ¿Con qué correo se registran? | "Una dirección dedicada, distinta de las dos de avisos" (recomendada) | Una dirección dedicada solo a las cuentas de los proveedores (Cloudflare, DigitalOcean, Resend y GitHub), distinta de las dos direcciones de avisos de seguridad de la aplicación (ADR-026), con el mismo nivel de protección: llave de seguridad o passkey, dos factores y códigos de respaldo |
| 3 | ¿Qué se deja por escrito para la operación? | "Registro de cuentas + bloqueo del dominio + un solo usuario + revisión anual" (recomendada) | En la fase 6: un registro de cuentas (correo de recuperación, factores registrados, dónde están los códigos de respaldo y cómo se recupera cada cuenta; **sin contraseñas ni códigos**); bloqueo de transferencia del dominio activo en Cloudflare Registrar; un solo usuario administrador por cuenta, sin invitados; revisión una vez al año junto con la rotación de secretos (ADR-032) |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Cloudflare, autenticación en dos pasos: https://developers.cloudflare.com/fundamentals/user-profiles/2fa/ | Documentación del proveedor | Leída por resumen (WebFetch, 23-oct-2026) | TOTP, llaves de seguridad y correo (sin SMS); recomienda al menos dos factores y códigos de respaldo | Otra URL de Cloudflare sobre protección de la cuenta devolvió 404 |
| GitHub, acerca de 2FA: https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-two-factor-authentication | Documentación del proveedor | Leída por resumen (23-oct-2026) | TOTP, SMS, llaves de seguridad, passkeys y GitHub Mobile; obligatorio para quienes contribuyen código (desde 2023) | No ordena los métodos por seguridad |
| DigitalOcean, 2FA: https://docs.digitalocean.com/products/accounts/security/2fa/ | Documentación del proveedor | Leída por resumen (23-oct-2026) | App autenticadora (recomendada) y SMS; códigos de respaldo de un solo uso; recuperación por soporte | **No menciona llaves de seguridad**; puede que existan y la página no las liste |
| Resend, cómo añadir MFA: https://resend.com/docs/knowledge-base/how-can-i-add-mfa | Documentación del proveedor | **Solo por resultados de búsqueda** (la página no se abrió) | Solo app autenticadora; se activa por cuenta; no se puede exigir al equipo | No se encontraron llaves de seguridad ni códigos de respaldo; no es lectura de la página |
| OWASP, Multifactor Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html | Guía de experto reconocido | Leída por resumen (23-oct-2026) | FIDO2/WebAuthn es lo más sólido y resiste el phishing; TOTP, SMS y correo son vulnerables al phishing en tiempo real; la NIST clasifica SMS y llamadas como restringidos; códigos de respaldo y varios tipos de factor; la recuperación es un proceso de alto riesgo; notificar por un canal distinto | — |
| Cloudflare, transferencias de dominio (varias páginas): https://developers.cloudflare.com/registrar/domain-transfers | Documentación del proveedor | **Solo resultados de búsqueda** | El bloqueo de registrador impide transferencias no autorizadas; quien tenga rol de superadministrador o administrador de la zona puede desbloquear y obtener códigos de autorización | **No se encontró** que Cloudflare exija el segundo factor para cambiar el bloqueo |
| CISA, MFA resistente al phishing | Guía oficial | **No se pudo leer**: el enlace devolvió 404 y el PDF vino ilegible | — | No se cita para nada |

## 3. Lo que propone el asistente y el solicitante no decidió
- Que un solo usuario por cuenta y la revisión anual sean la medida adecuada: criterio del asistente, sin fuente.
- Papel en un lugar seguro como lugar de los códigos de respaldo: ejemplo del asistente. Un gestor de contraseñas es una alternativa que no se investigó.
- El nombre de la dirección dedicada y su proveedor: sin decidir.
- Que el segundo factor de los proveedores se adopte como **requisito** (RF o RNF) de la ERS y no solo como decisión del DAS: sin decidir.

## 4. Qué no se hizo
- No se editó ningún documento ni se creó la dirección ni se activó ningún factor; no hay cuentas todavía (etapa B).
- No se verificó si DigitalOcean ofrece llaves de seguridad ni si Resend ofrece códigos de respaldo.
- No se verificó que Cloudflare exija el segundo factor al cambiar el bloqueo de un dominio.
- El modelo de amenazas sigue diciendo que AM-23 no tiene ningún requisito; se actualiza en una versión nueva.
- Un factor TOTP (DigitalOcean, Resend) sigue siendo vulnerable al phishing en tiempo real: riesgo residual que queda registrado y **no aceptado**.

## 5. Qué falta hacer
1. Decidir si esto pasa a la ERS como requisito (versión nueva) y a cuál ADR del DAS.
2. Modelo de amenazas v0.2: BR-01 cerrada, AM-23 con su nueva respuesta y el riesgo residual recalculado.
3. Fase 6: el registro de cuentas y el procedimiento de recuperación.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
