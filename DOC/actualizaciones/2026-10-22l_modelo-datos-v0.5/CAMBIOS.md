# Actualización 2026-10-22 (l) — Modelo de datos v0.5: documento del contrato y archivo temporal

**Fecha:** 2026-10-22
**Documentos afectados:** [Modelo de datos v0.5](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.5_borrador.md) (nuevo; reemplaza a la [v0.4](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.4_borrador.md), que no se edita). Editados en su sitio, por citar el modelo como base: [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md), [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md) y [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md); además el [README de la fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md)
**Origen:** [2026-10-22 (k)](../2026-10-22k_alineacion-ERS-v1.11/CAMBIOS.md), [(h)](../2026-10-22h_ht-10-zona-temporal/CAMBIOS.md) y [(j)](../2026-10-22j_ERS-v1.11/CAMBIOS.md)
**Estado:** borrador; no aprobado

## 1. Motivo
Tras la ERS v1.11 y la decisión de la zona temporal (HT-10), el modelo v0.4 no tenía dónde guardar la fotografía del contrato ni los archivos temporales. El solicitante pidió redactar la v0.5 (22-oct-2026).

## 2. Cambios en el modelo
| Elemento | Cambio | Origen |
|---|---|---|
| **`DOCUMENTO_CONTRATO` (nueva)** | `id`, `contrato_id`, `orden`, `referencia_archivo`, `tipo_real_archivo`, `tamano_bytes`, `creado_en`. Una fotografía por fila; asociada al contrato. **Sin `eliminado_en`**: la conservación depende de DP-28 | RF-52 |
| **`ARCHIVO_TEMPORAL` (nueva)** | Zona temporal: hash del identificador, destino, cara, archivo, tipo y tamaño, hash de la sesión (propuesta), `creado_en`, `expira_en` (24 horas), `usado_en`, `eliminado_en` | HT-10, decisión del solicitante del 22-oct-2026 |
| `ACCESO_DOCUMENTO` | Dos referencias excluyentes: `documento_id` y `documento_contrato_id` (R23) | RF-45, RF-52 (auditoría de la consulta del contrato: propuesta) |
| Restricciones | R11 ampliada; nuevas R22 (orden único por contrato), R23, R24 (un solo uso y caducidad) y R25 (una fila activa por cara) | — |
| Secciones 6 a 8, 11 a 13 | Retención (DP-28 pendiente; el temporal se elimina a las 24 horas), dos transacciones nuevas, trazabilidad, tipos físicos y lo no probado | — |
| Hallazgos | H15 (fotografía del contrato), H16 (zona temporal), H17 (una fotografía por cara) | — |

## 3. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido por el solicitante (22-oct-2026):** la fotografía del contrato asociada al contrato; la zona temporal con identificador de un solo uso; la caducidad de 24 horas.
- **Propuesta del asistente, sin decidir:**
  - Los atributos de `DOCUMENTO_CONTRATO` y `ARCHIVO_TEMPORAL`, incluido el hash del identificador y el hash de la sesión (la ligadura a la sesión sigue sin decidir).
  - Guardar `tipo_real_archivo` y `tamano_bytes` también en el contrato, igual que en la cédula.
  - Que `ACCESO_DOCUMENTO` use dos referencias y no una tabla aparte.
  - **R25**: una fila activa por cara de la cédula (la ERS no lo dice con claridad).

## 4. Lo que no se hizo
- **No se probó en PostgreSQL.** La prueba de la sección 12 es de versiones anteriores; las entidades nuevas y R22 a R25 **no están probadas**.
- **No se añadió ningún ADR** ni se tocó el DAS salvo una referencia.
- DP-28 (conservación, eliminación y desasociación de la fotografía del contrato) y DP-29 (número de fotografías y cifras de reducción) siguen abiertas; el modelo no las resuelve.
- El modelo sigue siendo lógico: los tipos físicos de las columnas nuevas se confirman con `sqlmigrate`.
- Los documentos que citaban el modelo v0.4 como base se actualizaron solo en su referencia; no se releyeron enteros.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
- **Seguimiento:** probado el 22-oct-2026; ver la [actualización 2026-10-22 (m)](../2026-10-22m_prueba-modelo-v0.5/CAMBIOS.md).
