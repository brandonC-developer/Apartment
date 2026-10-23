# Actualización 2026-10-23 — HT-11: contenido del perfil de la propiedad

**Fecha:** 2026-10-23
**Documentos afectados (editado en su sitio, borrador vigente no aprobado):** [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md) (fila HT-11 y pendiente 8); [DOC/README.md](../../README.md)
**Origen:** hallazgo HT-11 de la [actualización 2026-10-22 (k)](../2026-10-22k_alineacion-ERS-v1.11/CAMBIOS.md)
**Estado:** borrador; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Qué muestra el perfil de cada propiedad? | "Datos + contrato vigente + 2 acciones" (recomendada por el asistente) | Datos de RF-06, inquilino y contrato vigente, y las acciones "Agregar cédula" (RF-51) y "Foto del contrato" (RF-52). Sin historial de contratos en la v1 |
| 2 | ¿Qué pasa con los botones si no hay contrato vigente (libre o solo contrato futuro)? | "Desactivados con aviso" (recomendada) | Botones visibles y desactivados con el aviso "No hay contrato vigente"; coincide con RF-51/RF-52 |
| 3 | ¿Cómo se comporta "Agregar cédula" si ya existe? | "Reemplazo con aviso" (recomendada) | Con cédula activa en esa cara el botón dice "Reemplazar"; la anterior se marca eliminada (R25, probada el 22-oct-2026) |

## 2. Lo que propone el asistente y el solicitante no decidió
- Los textos exactos de los botones y avisos.
- Que la zona temporal (HT-10) sirva también para la fotografía del contrato (ya en el modelo v0.5).

## 3. Qué no se hizo
- No se cambió la ERS: las tres decisiones son coherentes con RF-51/RF-52 y CA-75 a CA-77. Si se quiere un criterio de aceptación de "botones desactivados sin contrato vigente" o del reemplazo, iría en una ERS v1.12.
- No se diseñó la pantalla (maquetación); queda para la E2.
- DP-28, DP-29, DP-27 siguen abiertas.

## 4. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
