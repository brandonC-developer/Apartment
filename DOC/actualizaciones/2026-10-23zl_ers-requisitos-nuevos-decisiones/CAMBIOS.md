# Actualización 2026-10-23 (zl) — Requisitos nuevos de la ERS: decisiones previas a su redacción

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado ni creado; la ERS v1.15 con los tres requisitos se redacta en una actualización posterior. [DOC/README.md](../../README.md)
**Origen:** requisitos que piden las decisiones de seguridad del 23-oct-2026 y no existen en la [ERS v1.14](../../fase-1-ers/ERS_SGA_001_v1.14_borrador.md): aviso de fallo del respaldo ([actualización (zi)](../2026-10-23zi_salida-firewall-y-hora-respaldo/CAMBIOS.md)), segundo factor de las cuentas externas ([BR-01](../2026-10-23y_br-01-cuentas-proveedores/CAMBIOS.md) y [BR-12](../2026-10-23ze_br-12-correo-del-administrador/CAMBIOS.md)) y correo autenticado ([BR-02](../2026-10-23z_br-02-autenticacion-correo/CAMBIOS.md)); el DAS v0.14 los menciona como pendientes
**Estado:** decisiones registradas; ERS sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Cómo se registra el aviso de fallo del respaldo? | "RF-53 y CA-79 nuevos, aparte de RF-49" (recomendada por el asistente) | **RF-53** (vigilar el respaldo diario) y **CA-79**, sin tocar RF-49 ni CA-72; mismo reintentador; entrega E4. El respaldo escribe una marca solo cuando la subida terminó bien; si el último respaldo correcto tiene más de 26 horas hay aviso registrado, alerta web persistente y correo, sin repetir el correo en cada comprobación. No cubre un servidor caído ni comprueba la restauración |
| 2 | ¿El segundo factor de las cuentas externas pasa a ser un requisito? | "RNF-19 y CA-80 (inspección), como control de la fase 6" (recomendada) | **RNF-19** (protección de las cuentas de servicios externos) y **CA-80**, por inspección del registro de cuentas; mismo patrón que RNF-18 (entregable de la fase 6, no función del sistema); no cita una obligación legal |
| 3 | ¿El correo autenticado pasa a ser un requisito? | "RNF-20 y CA-81, verificados en la etapa B" (recomendada) | **RNF-20** (autenticación del correo saliente) y **CA-81**, verificados con las cabeceras de los tres tipos de correo y con el registro `_dmarc`, en la etapa B; no cita una obligación legal |

Totales previstos tras redactarlos: **53 RF, 20 RNF y 81 CA** (hoy 52 RF, 18 RNF y 78 CA).

## 2. Borradores aprobados en lo esencial
Los textos que el solicitante vio al decidir son la base de la redacción:
- **RF-53 — Vigilar el respaldo diario:** comprobar con el reintentador que el último respaldo correcto tiene menos de 26 horas; si no, aviso, alerta web persistente y correo sin repetir; no detecta un servidor caído ni comprueba la restauración.
- **RNF-19 — Protección de las cuentas de servicios externos:** mejor segundo factor disponible (nunca SMS), dos factores, códigos de respaldo fuera del dispositivo, un solo usuario administrador, dirección dedicada para las cuentas de proveedores, registro de cuentas sin secretos con revisión anual y bloqueo de transferencia del dominio.
- **RNF-20 — Autenticación del correo saliente:** subdominio de envío dedicado con SPF y DKIM, DMARC de `p=none` a `p=reject` tras comprobar los tres tipos de correo, reportes a la dirección dedicada, dominio raíz sin enviar correo.
- **CA-79, CA-80 y CA-81** con los criterios descritos en las preguntas.

## 3. Fuentes
| Fuente | Cómo se validó | Qué respalda |
|---|---|---|
| ERS v1.14: RF-49, CA-72, RNF-14, RNF-18, regla de IDs de CLAUDE.md | Releídos | Patrón del requisito de vigilancia; precedente de RNF-18 como entregable de la fase 6; los IDs no se reutilizan ni cambian de significado |
| Resend (DMARC), RFC 7489, requisitos de remitentes de Google | Leídas por resumen (actualización (z)) | Fundamento técnico de RNF-20 |
| Libro de SRE de Google, emergencia | Leído por resumen | Solo respalda probar la recuperación; **no habla de vigilar respaldos** |
| ISO/IEC/IEEE 29148 | **No leída** (de pago) | No se cita para clasificar los requisitos |

## 4. Lo que propone el asistente y el solicitante no decidió
- Las **26 horas**, el patrón de vigilancia, la prioridad y la entrega E4 de RF-53.
- La clasificación de RNF-19 y RNF-20 como requisitos no funcionales: se apoya solo en el precedente de RNF-18.
- Los textos exactos y los criterios de aceptación finales.
- **Otras decisiones de seguridad de hoy no tienen requisito propio** y quedan en el DAS (ADR-032): plazos de actualización de las dependencias, custodia de la clave del respaldo y límite de solicitudes. No se preguntó si deben serlo; quedan cubiertas de forma general por RNF-14.

## 5. Qué no se hizo
- No se redactó la ERS v1.15 ni se actualizaron la matriz, la estrategia de pruebas, el plan ni el registro de avance.
- No se diseñó cómo la aplicación lee la marca del respaldo.
- No se asignó prioridad ni se verificó que RNF-19 o RNF-20 se puedan comprobar antes de la etapa B.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
