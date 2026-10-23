# Actualización 2026-10-23 (z) — BR-02: autenticación del correo del dominio (SPF, DKIM, DMARC)

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el DAS (ADR-026 o ADR-032), el modelo de amenazas (versión nueva) y el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** brecha BR-02 y amenaza AM-21 del [modelo de amenazas v0.1](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.1_borrador.md); sigue a la [BR-01](../2026-10-23y_br-01-cuentas-proveedores/CAMBIOS.md)
**Estado:** decisiones registradas; documentos sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Desde qué dominio envía el sistema el correo? | "Un subdominio dedicado, la raíz no envía" (recomendada por el asistente) | El sistema envía desde un subdominio dedicado (nombre propuesto por el asistente: `avisos.<dominio>`) verificado en Resend; el dominio raíz no envía correo |
| 2 | ¿Cómo se activa DMARC? | "p=none con reportes en las pruebas y p=reject al verificar" (recomendada) | Registro TXT en `_dmarc` del dominio raíz; en las pruebas de la etapa B, `p=none` con reportes (`rua`); cuando los tres tipos de correo (aviso de seguridad, resumen diario y enlace de restablecimiento) lleguen con `dmarc=pass`, `p=reject` en la raíz, que el subdominio hereda (`sp` sin indicar). Se omite `quarantine` (criterio del asistente: un solo remitente y tres destinatarios) |
| 3 | ¿A dónde llegan los reportes de DMARC? | "A la dirección dedicada de proveedores, revisados a mano" (recomendada) | `rua` apunta a la dirección dedicada a las cuentas de los proveedores (decisión de la BR-01), distinta de las dos de avisos; se revisan a mano durante las pruebas de la etapa B y luego una vez al año; no se usa un servicio de terceros que los procese |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Resend, dominios: https://resend.com/docs/dashboard/domains/introduction | Documentación del proveedor | Leída por resumen (WebFetch, 23-oct-2026) | Recomienda enviar desde uno o más subdominios para aislar la reputación (ejemplo `updates.example.com`) | **No lista los registros DNS de verificación**; los remite a otra guía no leída |
| Resend, DMARC: https://resend.com/docs/dashboard/domains/dmarc | Documentación del proveedor | Leída por resumen (23-oct-2026) | Un dominio verificado ya cumple SPF y DKIM; registro TXT en `_dmarc`; empezar con `p=none` y `rua`; probar y revisar `dmarc=pass`; pasar a `quarantine` y luego a `reject`; mantener `rua`; cumple si pasa SPF o DKIM | Aconseja pasar por `quarantine`; omitirlo es criterio del asistente |
| RFC 7489, DMARC: https://www.rfc-editor.org/rfc/rfc7489.html | Especificación | Leída por resumen, **hasta el carácter 100 000 de 176 958** | DMARC usa SPF y DKIM y exige alineación con el `From`; políticas `none`, `quarantine`, `reject`; `pct`; `sp` para subdominios (hereda `p` si falta); reportes agregados `rua` y registro `_report._dmarc` para destinos de otro dominio | Es **Informational**, no un estándar de Internet; parte final no leída |
| Google, requisitos de remitentes: https://support.google.com/a/answer/81126 | Documentación del proveedor | Leída por resumen (23-oct-2026) | Todo remitente debe configurar SPF o DKIM; los masivos (más de 5 000 al día) también DMARC, con política mínima `none`; alineación con el dominio del `From`; claves DKIM de al menos 1024 bits, 2048 recomendado | Aplica a Gmail; el volumen del proyecto no llega al umbral, se cita como referencia |
| dmarc.org, resumen | Organización del estándar | **No se pudo abrir** (conexión rechazada) | — | No se cita |

## 3. Lo que propone el asistente y el solicitante no decidió
- El nombre del subdominio (`avisos.<dominio>`) y que el dominio raíz no envíe correo.
- Omitir `quarantine`.
- Revisar los reportes a mano y no usar un servicio de terceros: **no se investigó** ninguno.
- Que el receptor (los proveedores de las tres direcciones) respete DMARC: **no se verificó**.

## 4. Qué no se hizo
- No se compró el dominio ni se publicó ningún registro; es etapa B.
- No se verificaron los registros exactos de SPF y DKIM de Resend (la guía "Add a domain" no se leyó).
- No se probó que el correo de Resend llegue con `dmarc=pass`.
- No se consideraron MTA-STS ni TLS-RPT.
- El modelo de amenazas sigue sin reflejar esto: AM-21 cambia de respuesta en una versión nueva (v0.2).

## 5. Qué falta hacer
1. ERS o DAS: decidir si el correo autenticado pasa a ser un requisito y en qué ADR se documenta.
2. Modelo de amenazas v0.2: BR-02 cerrada, AM-21 con su respuesta y el riesgo residual recalculado.
3. Fase 6: registros DNS, pruebas con cabeceras y revisión de reportes.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
