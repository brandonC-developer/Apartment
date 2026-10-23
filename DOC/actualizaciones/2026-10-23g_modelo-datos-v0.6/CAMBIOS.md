# Actualización 2026-10-23 (g) — Modelo de datos v0.6: sin zona temporal

**Fecha:** 2026-10-23
**Documentos afectados:** [Modelo de datos v0.6](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.6_borrador.md) (nuevo; reemplaza a la [v0.5](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.5_borrador.md), que se conserva con su nota del 23-oct-2026). Editados en su sitio, por citar el modelo como base: [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md), [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md) y [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md); además el [README de la fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md)
**Origen:** [2026-10-23 (d)](../2026-10-23d_quitar-zona-temporal/CAMBIOS.md), [(e)](../2026-10-23e_ERS-v1.12/CAMBIOS.md) y [(f)](../2026-10-23f_alineacion-ERS-v1.12/CAMBIOS.md); el solicitante pidió redactar la v0.6 (23-oct-2026)
**Estado:** borrador; no aprobado; probado en PostgreSQL el mismo día (actualización (h))

## 1. Cambios en el modelo
| Elemento | Cambio | Origen |
|---|---|---|
| **`ARCHIVO_TEMPORAL`** | Se retira (entidad, diagrama, retención, trazabilidad y tipos físicos) | Decisión del solicitante, 23-oct-2026 |
| **R24** | Retirada; el número no se reutiliza. Desaparecen `sesion_hash` y el proceso de limpieza de 24 horas | Ídem |
| H16 | Queda como histórico, reemplazado por H19 | — |
| **R26 (nueva)** | Un contrato solo se crea si el inquilino tiene el frente de la fotografía cargado; lo aplica el servicio en la misma transacción | RF-07, CA-78; regla propuesta por el asistente y aceptada por el solicitante, sin fuente |
| **R27 (nueva)** | `tamano_bytes` entre 1 y 5 242 880 y `tipo_real_archivo` JPEG o PNG, como `CHECK` | RF-02 con 5 MiB; el `CHECK` es propuesta del asistente |
| R11 | Sin `ARCHIVO_TEMPORAL` | — |
| `DOCUMENTO_IDENTIDAD` | El frente se exige antes de crear un contrato, no para guardar al inquilino; sube directo a la ficha | RF-01, RF-03 |
| Sección 5 | Derivado nuevo: "inquilino con frente cargado" | CA-78, DP-30 |
| Sección 7 | Transacciones nuevas: registrar inquilino sin fotos, agregar o reemplazar la fotografía del documento, crear contrato; la de la fotografía del contrato empieza con el bloqueo del contrato | HT-11, H18 |
| **H18** | Pasa de propuesta a **adoptado** (decisión del solicitante, [actualización (b)](../2026-10-23b_h18-bloqueo-contrato/CAMBIOS.md)) | — |
| **H19 (nuevo)** | Sin zona temporal: inquilinos sin frente (DP-30) y posible archivo huérfano si falla la base | — |
| Sección 12.1 | Se marca como histórica: qué sigue aplicando y qué no | — |

## 2. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido (23-oct-2026):** quitar la zona temporal; el contrato solo con el frente cargado; el bloqueo del contrato (H18); el tope de 5 MiB.
- **Propuesta del asistente, sin decidir:** que R26 la aplique el servicio y no la base; el `CHECK` de R27; borrar el archivo recién escrito si falla la base (H19b), con un barrido periódico como alternativa; el orden de las transacciones de la sección 7.

## 3. Qué no se hizo
- **No se probó en PostgreSQL.** Las pruebas de la v0.5 (22-oct-2026) siguen aplicando solo en parte: R22, R23, R25, R12 sobre `ACCESO_DOCUMENTO`, la derivación de RF-51 y la concurrencia de R22/H18 no cambian; R26, R27, el borrado del archivo huérfano y la creación de contrato sin frente **no están probados**.
- No se añadió ningún ADR. No se resolvieron DP-28, DP-29, DP-30 ni DP-27.
- Los tipos físicos se confirman con `sqlmigrate` (sección 13).
- Es autoverificación del asistente, no revisión por otra persona (DP-23).

## 4. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
- **Seguimiento:** probado el 23-oct-2026; ver la [actualización 2026-10-23 (h)](../2026-10-23h_prueba-modelo-v0.6/CAMBIOS.md). Las secciones 2 y 3 se escribieron antes de esa prueba.
