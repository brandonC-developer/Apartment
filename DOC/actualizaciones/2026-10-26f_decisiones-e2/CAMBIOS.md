# Actualización 2026-10-26 (f) — Decisiones de la E2

**Fecha:** 2026-10-26
**Documentos afectados:** [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md) y [DOC/README.md](../../README.md). No cambia código ni ningún documento de las fases.
**Origen:** hallazgo de la E1 ([2026-10-24 (r)](../2026-10-24r_e1-grupo-a-modelos/CAMBIOS.md), sección 4) y modelo de datos v0.7 (R23, H15); inicio de la E2 ([2026-10-26 (e)](../2026-10-26e_inicio-e2/CAMBIOS.md))
**Estado:** decisión registrada; no aprobada

## Decisión 1 — Acceso a la fotografía del contrato
**Pregunta:** el modelo de datos hace que `ACCESO_DOCUMENTO` apunte a la cédula (`inquilinos`) o a la fotografía de un contrato (`alquileres`), pero `alquileres` depende de `inquilinos` (ADR-030): una clave foránea de `inquilinos` hacia `alquileres` crearía un ciclo de migraciones. ¿Cómo se registra el acceso a la fotografía del contrato (RF-52, CA-77)?

**Opciones:**
| Opción | Qué implica |
|---|---|
| **a) Tabla propia en `alquileres` (recomendada por el asistente)** | `AccesoDocumentoContrato` con su clave foránea al `DocumentoContrato`, solo `SELECT` e `INSERT`; la cédula no cambia |
| b) Aplicación neutra con referencia genérica | Un solo lugar para los accesos, sin clave foránea (la base no garantiza que el documento exista) y obliga a migrar la tabla de la E1 |
| c) Referencia sin clave foránea en `inquilinos` | Lo más rápido; la integridad depende del código |

**Fuente (validada por resumen):** [Django 5.2, Migraciones](https://docs.djangoproject.com/en/5.2/topics/migrations/) dice que una `ForeignKey` hacia otra app produce una dependencia entre sus migraciones y que un `CircularDependencyError` se resuelve sacando una de las claves del lazo; no trata los ciclos entre apps en general (limitación de la fuente).

**Respuesta del solicitante:** «Tabla propia en alquileres (Recomendado)».

**Decisión:** `alquileres.AccesoDocumentoContrato` con clave foránea a `DocumentoContrato`, solo `SELECT` e `INSERT` en el rol de la aplicación, con una prueba de privilegios. **R23 deja de ser una restricción de una sola tabla y pasa a cumplirse por construcción** (una clave foránea por tabla); queda anotado para la próxima versión del modelo de datos (v0.8, pendiente). La consulta de todos los accesos (cédula y contrato) usará las dos tablas.

## Pendiente
Ninguna otra decisión bloquea el grupo A. DP-28 (conservación de la fotografía del contrato) sigue abierta: no se borra ni desasocia hasta que se decida. Las cifras de reducción de la fotografía del contrato (DP-29) se miden en el grupo H.

## Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
