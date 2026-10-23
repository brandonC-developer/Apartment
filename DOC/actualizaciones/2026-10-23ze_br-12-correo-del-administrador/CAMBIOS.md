# Actualización 2026-10-23 (ze) — BR-12: segundo factor en el correo del administrador

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el modelo de amenazas (versión nueva), el DAS (ADR-026 o ADR-032), la ERS (si pasa a requisito) y el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** brecha BR-12 y amenaza AM-03 del [modelo de amenazas v0.2](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.2_borrador.md), de la [actualización 2026-10-23 (zd)](../2026-10-23zd_modelo-amenazas-v0.2/CAMBIOS.md); sigue la lógica de la [BR-01](../2026-10-23y_br-01-cuentas-proveedores/CAMBIOS.md)
**Estado:** decisión registrada; documentos sin cambiar; no aprobado

## 1. Pregunta, respuesta y decisión
| Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|
| ¿Se exige segundo factor en las dos direcciones de correo del administrador? | "Sí, el mejor disponible, como en BR-01" (recomendada por el asistente) | En las dos direcciones de avisos de seguridad (ADR-026), una de las cuales recibe el enlace de restablecimiento, se exige el mejor segundo factor disponible (llave de seguridad o passkey donde exista; si no, app autenticadora; nunca SMS), dos factores registrados y códigos de respaldo guardados fuera del dispositivo. La dirección dedicada a las cuentas de los proveedores ya queda cubierta por BR-01 |

## 2. Cuánto pesa el riesgo (análisis del asistente)
Quien controle el buzón **no entra solo** a la aplicación: el enlace de restablecimiento solo permite fijar una contraseña nueva y el acceso sigue exigiendo el TOTP (CA-59). Podría cambiar la contraseña y dejar fuera al administrador, leer los avisos y el resumen diario (con datos mínimos, RF-44) o borrar un aviso (el otro buzón también lo recibe). Por eso AM-03 es de nivel medio y no alto.

## 3. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| OWASP, Forgot Password Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html | Guía de experto reconocido | Leída por resumen (WebFetch, 23-oct-2026) | Token de un solo uso, corto y largo; invalidar los pendientes; no iniciar sesión automáticamente; avisar por correo sin la contraseña | **No analiza la seguridad del buzón ni menciona MFA para el correo** |
| OWASP, Multifactor Authentication Cheat Sheet | Guía de experto reconocido | Leída por resumen (actualización (y)) | El correo es vulnerable al phishing en tiempo real; la recuperación de cuenta es un proceso de alto riesgo; códigos de respaldo y varios factores | No exige proteger el buzón de recuperación |
| ERS v1.14 (RF-27, CA-59) y DAS v0.12 (ADR-026) | Documentos del proyecto | Releídos | El enlace va a `correo_admin` y no inicia sesión; avisos a dos direcciones; el acceso sigue exigiendo TOTP | — |

**No encontré una fuente que exija proteger el buzón de recuperación.** La decisión se apoya en el modelo de amenazas y en el criterio de coherencia con BR-01, no en una norma.

## 4. Lo que propone el asistente y el solicitante no decidió
- Que lo mismo valga para las dos direcciones y no solo para la que recibe el enlace.
- Qué dirección recibe el enlace de restablecimiento (hoy `correo_admin`, sin decidir cuál de las dos).

## 5. Qué no se hizo
- **No se sabe qué proveedores son las dos direcciones** (solo que son distintos, ADR-026): no se verificó qué segundo factor ofrecen. Si alguno no ofrece uno razonable, habrá que cambiarlo; no se evaluó.
- No se activó ningún factor ni se verificó nada: son cuentas del solicitante, fuera del repositorio.
- No se cambió la ERS: sigue sin haber un requisito sobre las cuentas de correo, de los proveedores ni de ningún otro servicio externo.
- Con una sola persona (DP-23), perder el acceso al buzón también pierde el restablecimiento: riesgo anotado, no resuelto.

## 6. Qué falta hacer
1. Modelo de amenazas v0.3: BR-12 cerrada; AM-03 con su control nuevo.
2. Decidir si el segundo factor de las cuentas de correo, de los proveedores y de las del solicitante pasa a **un requisito de la ERS** y a cuál ADR del DAS.
3. Fase 6: incluir las dos direcciones en el registro de cuentas (BR-01).

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
