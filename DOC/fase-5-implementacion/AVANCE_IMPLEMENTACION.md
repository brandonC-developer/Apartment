# Registro de avance de la implementación

**Identificador:** AVA-SGA-001
**Estado:** registro vivo, solo de adiciones; no es un documento versionado ni aprobado
**Creado:** 21 de octubre de 2026
**Plan:** [Plan de implementación v0.1](PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md)

Este archivo registra el avance real de las entregas del plan. **La E0 se inició el 23-oct-2026 por instrucción del solicitante, sin que la ERS ni la arquitectura estén aprobadas** (actualización 2026-10-23 (zy)); las demás entregas figuran como *no iniciada*.

## Reglas (decisión del solicitante, 21-oct-2026)
1. **Una entrega a la vez.** No se empieza la siguiente hasta que la actual cumpla la definición de terminado (sección 3.1 del plan). Como máximo una entrega está *en curso* o *bloqueada*.
2. **Estados:** *no iniciada*, *en curso*, *terminada* o *bloqueada*.
3. **Bloqueada:** una entrega con una prueba de prioridad Alta pendiente queda *bloqueada*, nunca *terminada*. Las únicas salidas son completarla o un cambio de alcance escrito (nueva versión del plan y un `CAMBIOS.md` con la decisión del solicitante), como ocurrió con RF-37. Una prueba Alta no se difiere por decisión de la entrega.
4. **Media y Baja:** una prueba Media solo se difiere con aceptación escrita del solicitante; una Baja puede diferirse. Toda diferida se anota en la columna de desviaciones.
5. **Solo adiciones:** cada cambio de estado agrega una línea al historial de la sección 3; no se borran ni se reescriben líneas anteriores.

## Entregas
| Entrega | Estado | Inicio | Fin | Condiciones de terminado cumplidas (de 9) | CA aprobados / asignados | Desviaciones y enlace a su CAMBIOS |
|---|---|---|---|---|---|---|
| E0 Esqueleto | en curso | 2026-10-23 | — | 0 | 0 / 8 | Iniciada sin ERS ni DAS aprobados, por instrucción del solicitante ([actualización 2026-10-23 (zy)](../actualizaciones/2026-10-23zy_inicio-implementacion-e0/CAMBIOS.md)); solo el esqueleto del proyecto, sin CA aprobados |
| E1 Inquilinos | no iniciada | — | — | 0 | 0 / 8 | Alcance ampliado el 22 y 23-oct-2026: CA-73, CA-74 y CA-83 ([actualización 2026-10-23zt](../actualizaciones/2026-10-23zt_alineacion-ERS-v1.16/CAMBIOS.md) y [actualización 2026-10-22f](../actualizaciones/2026-10-22f_ERS-v1.10/CAMBIOS.md)) |
| E2 Contratos y obligaciones | no iniciada | — | — | 0 | 0 / 25 | Alcance ampliado el 22 y 23-oct-2026: CA-75, CA-76, CA-77, CA-78 y CA-82 ([actualización 2026-10-23zt](../actualizaciones/2026-10-23zt_alineacion-ERS-v1.16/CAMBIOS.md), [actualización 2026-10-22j](../actualizaciones/2026-10-22j_ERS-v1.11/CAMBIOS.md) y [2026-10-23e](../actualizaciones/2026-10-23e_ERS-v1.12/CAMBIOS.md)) |
| E3 Movimientos y depósitos | no iniciada | — | — | 0 | 0 / 17 | — |
| E4 Notificaciones y cuenta | no iniciada | — | — | 0 | 0 / 13 | Alcance ampliado el 23-oct-2026: CA-79 ([actualización 2026-10-23zm](../actualizaciones/2026-10-23zm_alineacion-ERS-v1.15/CAMBIOS.md)) |
| E5 Calendario y privacidad | no iniciada | — | — | 0 | 0 / 8 | — |
| E6 Etapa B y salida | no iniciada | — | — | 0 | 0 / 2 | Alcance ampliado el 23-oct-2026: CA-80 y CA-81 ([actualización 2026-10-23zm](../actualizaciones/2026-10-23zm_alineacion-ERS-v1.15/CAMBIOS.md)) |

## Historial de cambios de estado
| Fecha | Entrega | Cambio | Motivo o enlace |
|---|---|---|---|
| 2026-10-21 | Todas | Creación del registro; todas *no iniciada* | [Actualización 2026-10-21 (y)](../actualizaciones/2026-10-21y_registro-de-avance/CAMBIOS.md) |
| 2026-10-22 | E1 | Alcance ampliado: CA asignados de 5 a 7 (CA-73 y CA-74); la entrega sigue *no iniciada* | [Actualización 2026-10-22 (f)](../actualizaciones/2026-10-22f_ERS-v1.10/CAMBIOS.md) |
| 2026-10-22 | E2 | Alcance ampliado: CA asignados de 20 a 23 (CA-75, CA-76 y CA-77); la entrega sigue *no iniciada* | [Actualización 2026-10-22 (j)](../actualizaciones/2026-10-22j_ERS-v1.11/CAMBIOS.md) |
| 2026-10-23 | E2 | Alcance ampliado: CA asignados de 23 a 24 (CA-78); la entrega sigue *no iniciada* | [Actualización 2026-10-23 (e)](../actualizaciones/2026-10-23e_ERS-v1.12/CAMBIOS.md) |
| 2026-10-23 | E4 | Alcance ampliado: CA asignados de 12 a 13 (CA-79); la entrega sigue *no iniciada* | [Actualización 2026-10-23 (zm)](../actualizaciones/2026-10-23zm_alineacion-ERS-v1.15/CAMBIOS.md) |
| 2026-10-23 | E6 | Alcance ampliado: pasa de sin CA a 2 CA (CA-80 y CA-81); la entrega sigue *no iniciada* | [Actualización 2026-10-23 (zm)](../actualizaciones/2026-10-23zm_alineacion-ERS-v1.15/CAMBIOS.md) |
| 2026-10-23 | E1 | Alcance ampliado: CA asignados de 7 a 8 (CA-83); la entrega sigue *no iniciada* | [Actualización 2026-10-23 (zt)](../actualizaciones/2026-10-23zt_alineacion-ERS-v1.16/CAMBIOS.md) |
| 2026-10-23 | E2 | Alcance ampliado: CA asignados de 24 a 25 (CA-82); la entrega sigue *no iniciada* | [Actualización 2026-10-23 (zt)](../actualizaciones/2026-10-23zt_alineacion-ERS-v1.16/CAMBIOS.md) |
| 2026-10-23 | E0 | Pasa a *en curso*: esqueleto del proyecto Django en `src/` (sin modelos, migraciones ni pantallas) | [Actualización 2026-10-23 (zy)](../actualizaciones/2026-10-23zy_inicio-implementacion-e0/CAMBIOS.md) |
