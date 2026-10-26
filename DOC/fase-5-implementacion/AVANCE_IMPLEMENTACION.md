# Registro de avance de la implementación

**Identificador:** AVA-SGA-001
**Estado:** registro vivo, solo de adiciones; no es un documento versionado ni aprobado
**Creado:** 21 de octubre de 2026
**Plan:** [Plan de implementación v0.1](PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md)

Este archivo registra el avance real de las entregas del plan. **La E0 se inició el 23-oct-2026 por instrucción del solicitante, sin que la ERS ni la arquitectura estén aprobadas** (actualización 2026-10-23 (zy)) y **se dio por terminada el 24-oct-2026** (actualización 2026-10-24 (n)); **la E1 se inició el 24-oct-2026** por autorización expresa del solicitante (actualización 2026-10-24 (p)); las demás entregas figuran como *no iniciada* y **no se pueden empezar sin su autorización expresa** (CLAUDE.md).

## Reglas (decisión del solicitante, 21-oct-2026)
1. **Una entrega a la vez.** No se empieza la siguiente hasta que la actual cumpla la definición de terminado (sección 3.1 del plan). Como máximo una entrega está *en curso* o *bloqueada*.
2. **Estados:** *no iniciada*, *en curso*, *terminada* o *bloqueada*.
3. **Bloqueada:** una entrega con una prueba de prioridad Alta pendiente queda *bloqueada*, nunca *terminada*. Las únicas salidas son completarla o un cambio de alcance escrito (nueva versión del plan y un `CAMBIOS.md` con la decisión del solicitante), como ocurrió con RF-37. Una prueba Alta no se difiere por decisión de la entrega.
4. **Media y Baja:** una prueba Media solo se difiere con aceptación escrita del solicitante; una Baja puede diferirse. Toda diferida se anota en la columna de desviaciones.
5. **Solo adiciones:** cada cambio de estado agrega una línea al historial de la sección 3; no se borran ni se reescriben líneas anteriores.

## Entregas
| Entrega | Estado | Inicio | Fin | Condiciones de terminado cumplidas (de 9) | CA aprobados / asignados | Desviaciones y enlace a su CAMBIOS |
|---|---|---|---|---|---|---|
| E0 Esqueleto | terminada | 2026-10-23 | 2026-10-24 | 9 | 7 / 8 | Iniciada sin ERS ni DAS aprobados, por instrucción del solicitante ([actualización 2026-10-23 (zy)](../actualizaciones/2026-10-23zy_inicio-implementacion-e0/CAMBIOS.md)); **terminada el 24-oct-2026** ([actualización 2026-10-24 (n)](../actualizaciones/2026-10-24n_cierre-e0/CAMBIOS.md)). **CA-18: su parte de contratos en USD se difiere a la E2 por aceptación escrita del solicitante** (prioridad Media). CA-68, CA-69 y CA-70 verificados sin el correo (HI-01, HI-05): el envío a las dos direcciones se verifica en la E4. Sin revisión por otra persona (plan, sección 3.3) |
| E1 Inquilinos | terminada | 2026-10-24 | 2026-10-26 | 9 | 8 / 8 | Alcance ampliado el 22 y 23-oct-2026: CA-73, CA-74 y CA-83 ([actualización 2026-10-23zt](../actualizaciones/2026-10-23zt_alineacion-ERS-v1.16/CAMBIOS.md) y [actualización 2026-10-22f](../actualizaciones/2026-10-22f_ERS-v1.10/CAMBIOS.md)); **iniciada el 24-oct-2026 por autorización expresa del solicitante** ([actualización 2026-10-24 (p)](../actualizaciones/2026-10-24p_inicio-e1/CAMBIOS.md)). **CA-29: su bloqueo real (contrato vigente en la E2, saldos pendientes en la E3) se difiere por aceptación escrita del solicitante** (prioridad Media; la E1 entrega el mecanismo y lo prueba con una comprobación falsa) ([actualización 2026-10-24 (q)](../actualizaciones/2026-10-24q_decisiones-e1/CAMBIOS.md)); **terminada el 26-oct-2026** ([actualización 2026-10-26 (d)](../actualizaciones/2026-10-26d_cierre-e1/CAMBIOS.md)): CA-29 solo en su mecanismo (bloqueo real en la E2 y la E3) y CA-73 con muestras públicas de teléfonos más una foto del solicitante, ambas desviaciones aceptadas por él |
| E2 Contratos y obligaciones | no iniciada | — | — | 0 | 0 / 25 | Alcance ampliado el 22 y 23-oct-2026: CA-75, CA-76, CA-77, CA-78 y CA-82 ([actualización 2026-10-23zt](../actualizaciones/2026-10-23zt_alineacion-ERS-v1.16/CAMBIOS.md), [actualización 2026-10-22j](../actualizaciones/2026-10-22j_ERS-v1.11/CAMBIOS.md) y [2026-10-23e](../actualizaciones/2026-10-23e_ERS-v1.12/CAMBIOS.md)); recibe de la E0 la parte de contratos en USD de CA-18 ([actualización 2026-10-24 (n)](../actualizaciones/2026-10-24n_cierre-e0/CAMBIOS.md)); recibe de la E1 el bloqueo de desactivar con contrato vigente (CA-29) ([actualización 2026-10-24 (q)](../actualizaciones/2026-10-24q_decisiones-e1/CAMBIOS.md)) |
| E3 Movimientos y depósitos | no iniciada | — | — | 0 | 0 / 17 | —; recibe de la E1 el bloqueo de desactivar con saldos pendientes (CA-29) ([actualización 2026-10-24 (q)](../actualizaciones/2026-10-24q_decisiones-e1/CAMBIOS.md)) |
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
| 2026-10-24 | E0 | Pasa a *terminada*: 9 de 9 condiciones y 7 de 8 CA (CA-18 con su parte de contratos diferida a la E2 por aceptación del solicitante) | [Actualización 2026-10-24 (n)](../actualizaciones/2026-10-24n_cierre-e0/CAMBIOS.md) |
| 2026-10-24 | E2 | Alcance: recibe la parte de contratos en USD de CA-18; la entrega sigue *no iniciada* | [Actualización 2026-10-24 (n)](../actualizaciones/2026-10-24n_cierre-e0/CAMBIOS.md) |
| 2026-10-24 | E0 | Sin cambio de estado: tras el cierre se halló y corrigió un defecto de seguridad que el asistente clasifica **Media** (códigos de recuperación guardados con SHA-256 sin sal; NIST SP 800-63B pide sal y un hash de contraseñas) y se registraron cinco decisiones del solicitante. La condición 9 se refiere a defectos Alta; el solicitante puede reclasificarlo | [Actualización 2026-10-24 (o)](../actualizaciones/2026-10-24o_decisiones-abiertas-e0/CAMBIOS.md) |
| 2026-10-24 | E1 | Pasa a *en curso*: autorización expresa del solicitante («sí, autorizo la E1») | [Actualización 2026-10-24 (p)](../actualizaciones/2026-10-24p_inicio-e1/CAMBIOS.md) |
| 2026-10-24 | E1 | Alcance: CA-29 se cumple en la E1 solo en el mecanismo; el bloqueo real pasa a la E2 y la E3 por aceptación del solicitante; la entrega sigue *en curso* | [Actualización 2026-10-24 (q)](../actualizaciones/2026-10-24q_decisiones-e1/CAMBIOS.md) |
| 2026-10-26 | E1 | Pasa a *terminada*: 9 de 9 condiciones y 8 de 8 CA (CA-29 solo en su mecanismo; CA-73 con la desviación aceptada) | [Actualización 2026-10-26 (d)](../actualizaciones/2026-10-26d_cierre-e1/CAMBIOS.md) |
