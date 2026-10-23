# Actualización 2026-10-23 (m) — Modelo de datos v0.7: máximo de 10 fotografías por contrato

**Fecha:** 2026-10-23
**Documentos afectados:** [Modelo de datos v0.7](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.7_borrador.md) (nuevo; reemplaza a la [v0.6](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.6_borrador.md), que se conserva con su nota del 23-oct-2026). Editados en su sitio, por citar el modelo como base: [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) y [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md); además el [README de la fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md)
**Origen:** [2026-10-23 (l)](../2026-10-23l_ERS-v1.14/CAMBIOS.md) y [(k)](../2026-10-23k_dp-29-fotos-contrato/CAMBIOS.md); el solicitante pidió redactar la v0.7 (23-oct-2026)
**Estado:** borrador; no aprobado; probado en PostgreSQL el mismo día (actualización (n))

## 1. Cambios en el modelo
| Elemento | Cambio | Origen |
|---|---|---|
| `DOCUMENTO_CONTRATO.orden` | Entero de 1 a 10 | Decisión del solicitante (máximo de 10), ERS v1.14, RF-52 |
| **R28 (nueva)** | `orden` entre 1 y 10, junto con R22 (a lo sumo 10 fotografías por contrato); el servicio rechaza la número 11 con un mensaje antes de insertar, con el contrato ya bloqueado (H18); el `CHECK` es la segunda defensa | RF-52, CA-76, DP-29; el `CHECK` es propuesta del asistente |
| Sección 7 | La transacción "Agregar la fotografía del contrato" rechaza si ya hay 10 | CA-76 |
| Sección 13 | `orden` como `smallint` con `CHECK` (propuesta, por confirmar con `sqlmigrate`) | — |
| **H20 (nuevo)** | Si DP-28 permitiera borrar una fotografía, `max(orden) + 1` podría superar 10 con menos de 10 fotografías o dejar huecos; propuesta: contar las filas y reutilizar el menor `orden` libre. Abierto | DP-28 |
| Control del documento | Fila 0.7; la fila 0.6 pasa a "probado el mismo día"; la nota de la v0.6 se retira de la v0.7 | — |

El resto del modelo no cambia.

## 2. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido (23-oct-2026):** el máximo de 10 fotografías por contrato.
- **Propuesta del asistente, sin decidir:** que se exprese también como `CHECK`; el tipo `smallint`; la salida de H20.

## 3. Qué no se hizo
- **No se probó en PostgreSQL.** R28 (el `CHECK`, el rechazo de la número 11 y que las 10 anteriores se conserven) y H20 no están probados. La prueba de la v0.6 sigue valiendo para lo que no cambió.
- No se resolvió DP-28 ni DP-27; las cifras definitivas de reducción (DP-29) se miden en la E2.
- Los tipos físicos se confirman con `sqlmigrate`. Es autoverificación del asistente, no revisión por otra persona (DP-23).

## 4. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
- **Seguimiento:** probado el 23-oct-2026; ver la [actualización 2026-10-23 (n)](../2026-10-23n_prueba-modelo-v0.7/CAMBIOS.md). La sección 3 se escribió antes de esa prueba.
