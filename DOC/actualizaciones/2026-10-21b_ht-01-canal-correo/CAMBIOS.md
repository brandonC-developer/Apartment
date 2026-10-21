# Actualización 2026-10-21 (b) — Diseño técnico v0.4 (HT-01 y canal de correo)

**Fecha:** 2026-10-21
**Documentos afectados:** [Diseño técnico v0.4](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.4_borrador.md); README de la [fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md)
**Versión anterior:** [Diseño técnico v0.3](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.3_borrador.md) (se conserva sin cambios)
**Estado:** borrador; no aprobado

## 1. Motivo
Hallazgo HT-01: ¿se define ahora el punto de recepción de estados de entrega de WhatsApp? La respuesta del solicitante cambió el alcance de las notificaciones de la v1.

## 2. Cambios
| ID | Tipo | Descripción | Origen |
|---|---|---|---|
| DTE 3.7 | añadido | Notificaciones al administrador por correo en la v1 | P1 y P2 |
| DTE 3.3 | modificado | WhatsApp pasa a futuro; se conserva el contrato | P2 |
| DTE 3.3 | corregido | Decía "teléfono del inquilino"; RF-44 dice que el destinatario es el administrador (error mío de la v0.1) | Revisión de RF-44 |
| DTE 1, 2, 6 (HT-01), 7 | modificado | Estado de interfaces, fuente de Meta, HT-01 resuelto | — |

## 3. Impacto
Cambio de alcance **no reflejado todavía en la ERS ni el DAS**:
- **ERS:** sección 2.4 (excluye el correo como canal), RF-23, RF-24, RF-44, CA-09 y la matriz; y la excepción HT-09 se amplía.
- **DAS:** ADR-008 (canal), ADR-013 y ADR-026 (reintentos también para estas notificaciones). DP-04 sigue diferida.
- **Legal:** RF-44 y OL-17 están redactados para WhatsApp; su aplicación al correo es propuesta para el abogado (DP-17).
- **Pruebas:** CA-09 y las pruebas de notificación cambian de canal.

## 4. Decisiones
| # | Pregunta | Respuesta del solicitante | Recomendación del asistente |
|---|---|---|---|
| P1 | ¿Se define ahora el punto de recepción de estados de WhatsApp o se espera al proveedor? | "Por el momento solo se utilizará correo, a futuro WhatsApp" | Esperar al proveedor; diseñar sin el punto |
| P2 | ¿Significa que en la v1 los recordatorios y alertas al administrador salen por correo y WhatsApp queda para el futuro? | Sí: v1 con notificación web y correo al administrador; WhatsApp después | Igual (opción recomendada) |

Efecto: HT-01 desaparece de la v1; no hay punto de entrada desde el exterior.

**Propuestas del asistente, no decididas:** destinatario (la dirección del administrador), límites de contenido del correo iguales a RF-44, reintentos de RF-24.

**Pendientes:** lo anterior; dominio y direcciones; confirmar volumen frente al plan gratuito de Resend.

## 5. Evidencia y fuentes
- Meta, documentación de webhooks de WhatsApp Business Platform, consultada el 21-oct-2026: leída por resumen. Confirma webhooks con reintentos de hasta 7 días y duplicados; no confirma verificación del remitente ni consulta sin webhook.
- Búsqueda web: resultados de terceros que no resolvieron si Meta ofrece consulta de estado; no se cita como hecho.
- Límites de Resend (100 al día, 3.000 al mes): de la sesión anterior, por resumen, sin reverificar hoy.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`. No revisa el diseño técnico.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
