# Actualización 2026-10-23 (b) — H18: bloqueo del contrato al ordenar las fotografías

**Fecha:** 2026-10-23
**Documentos afectados (editado en su sitio, borrador vigente no aprobado):** [Modelo de datos v0.5](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.5_borrador.md) (fila H18); [DOC/README.md](../../README.md)
**Origen:** hallazgo H18 de la [actualización 2026-10-22 (m)](../2026-10-22m_prueba-modelo-v0.5/CAMBIOS.md)
**Estado:** borrador; no aprobado

## 1. Pregunta, respuesta y decisión
| Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|
| ¿Adoptas bloquear la fila del contrato (`FOR UPDATE`) antes de calcular el orden de la fotografía? | "Sí, adoptarlo" (recomendada por el asistente) | La transacción "Agregar la fotografía del contrato" bloquea primero el contrato y después valida el archivo temporal (R24), siempre en ese orden |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| PostgreSQL 18, bloqueos explícitos: https://www.postgresql.org/docs/18/explicit-locking.html | Documentación oficial | Leída por resumen (WebFetch, 23-oct-2026) | `FOR UPDATE` impide que otras transacciones bloqueen, modifiquen o borren las filas hasta el fin de la transacción; quien llega después espera. Recomienda adquirir los bloqueos en un orden consistente | Resumen, no lectura completa. En `REPEATABLE READ`/`SERIALIZABLE` puede lanzar error si la fila cambió (el proyecto usa el nivel por defecto, `READ COMMITTED`, propuesta sin verificar con Django) |
| Documentación de Django, `select_for_update()` | Documentación oficial | Leída por resumen el 21-oct-2026 (HT-07); no se reabrió hoy | Es la técnica que usará la aplicación | — |
| Prueba propia, [`resultado_prueba_v0.5.txt`](../2026-10-22m_prueba-modelo-v0.5/evidencia/resultado_prueba_v0.5.txt) | Evidencia propia | Ejecutada el 22-oct-2026 | Sin bloqueo: error de R22; con bloqueo: órdenes 3 y 4 | Dos sesiones de `psql`, no Django |

## 3. Qué no se hizo
- No se probó con Django ni con carga.
- No se cambió la ERS, el DAS ni el diseño técnico: el diseño ya remite al modelo.

## 4. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
