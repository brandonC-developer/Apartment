# Actualización 2026-10-17 (b) — ERS v1.6 y DAS v0.5

**Fecha:** 17 de octubre de 2026
**Documentos:** [ERS v1.6](../../fase-1-ers/ERS_SGA_001_v1.6_borrador.md) · [DAS v0.5](../../fase-2-arquitectura/DAS_SGA_001_v0.5_borrador.md)
**Versión anterior:** [actualización 2026-10-17](../2026-10-17_ERS-v1.5_DAS-v0.4/CAMBIOS.md) (ERS v1.5, DAS v0.4; se conservan sin cambios)
**Estado:** borrador; sin aprobación del negocio ni validación legal

## 1. Motivo

Cerrar las decisiones del propietario que bloqueaban la aprobación de la ERS (DP-22 a DP-25 y DP-14), siguiendo la lista de pasos de la sesión.

## 2. Decisiones del solicitante (17-oct-2026)

| ID | Pregunta | Respuesta | Dónde queda |
|---|---|---|---|
| DP-24 | ¿Cuándo vence el pago de un período? | Día de vencimiento configurable (1 a 31); por defecto, el día de inicio del período. Confirma RN-05. | ERS RF-07, RN-05, S-01; DAS 7.1 |
| DP-25 | ¿Qué incluye el saldo de apertura? | Todo lo adeudado hasta hoy, incluido el período en curso; las alertas comienzan desde la carga, no retroactivamente. | ERS RF-43 |
| DP-22 | ¿Cómo conoce el sistema el tope legal del reajuste? | El administrador lo digita en cada reajuste con su fuente; el sistema advierte sin bloquear y conserva ambos. Tras una explicación detallada del art. 67. | ERS RF-10, CA-51; DAS 7.4 |
| DP-23 | ¿Quién es propietario del producto y aprobador? | El solicitante, ambos roles. **Falta registrar el nombre.** | ERS control del documento y registro de aprobación |
| DP-14 | ¿Qué hacemos con P11? | El solicitante la recuperará y la escribirá. **Sigue abierta; todavía no hay enunciado ni respuesta.** | ERS DP-14 |

## 3. Cambios en los documentos

- **ERS v1.6:** copia de la v1.5 con las ediciones de RF-07, RF-10, RF-43, RN-05 y S-01; nuevo criterio CA-51 y su entrada en la matriz; DP-22, DP-24 y DP-25 pasan a "resueltas"; DP-23 queda acotada al registro del nombre y a la designación de los otros roles.
- **DAS v0.5:** copia de la v0.4 con la referencia a la ERS v1.6, la regla de vencimiento confirmada, el reajuste con tope y fuente, y la tabla de decisiones actualizada.

## 4. Pendientes

| ID | Decisión | Responsable |
|---|---|---|
| DP-14 | Pregunta P11 | Propietario |
| DP-23 | Nombre del propietario del producto; responsable de requisitos y responsable técnico | Propietario |
| DP-01, DP-17 a DP-21 | Validación legal (resumen para el abogado preparado, no enviado) | Abogado |
| DP-04, DP-07, DP-08 | Proveedor de WhatsApp, respaldo y exposición pública | Propietario y responsable técnico |

## 5. Verificación

Se comprobó con una copia temporal del script de coherencia (el archivo `herramientas/verificar_coherencia.ps1` ya no existía en disco al terminar esta actualización; se restauró después y pasa con el mismo resultado): todos los identificadores RF, RN, RNF, CA, OL, DP y ADR citados en la ERS v1.6 y el DAS v0.5 están definidos y no hay enlaces rotos entre archivos `.md`. No hay revisión de pares.

## 6. Aprobación

| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | El solicitante (nombre por registrar) | Pendiente | Pendiente |
