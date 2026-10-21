# Actualización 2026-10-21 (y) — Registro de avance de la implementación

**Fecha:** 2026-10-21
**Documentos afectados:** [AVANCE_IMPLEMENTACION.md](../../fase-5-implementacion/AVANCE_IMPLEMENTACION.md) (nuevo), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) (sección 3.2 nueva, sección 8; editado en su sitio porque no está reemplazado ni aprobado), README de la [fase 5](../../fase-5-implementacion/README.md), [DOC/README.md](../../README.md) y `herramientas/verificar_coherencia.ps1`
**Estado:** borrador; no aprobado

## 1. Decisión
| # | Pregunta | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | ¿Cómo se registra el avance y qué pasa si una entrega no completa una prueba Alta? | Una entrega a la vez, registro de avance y bloqueo si falta una prueba Alta | Igual |

## 2. Qué se creó
- **AVANCE_IMPLEMENTACION.md:** registro vivo, solo de adiciones, con las siete entregas en estado *no iniciada*, las reglas y un historial. Es propuesta del asistente en su forma; la decisión del solicitante es la regla.
- **Cifras comprobadas:** los CA asignados por entrega (4, 5, 17, 17, 10 y 6; la E6 sin CA) coinciden con la tabla del plan.
- **Script:** nueva comprobación 9: cada entrega del plan consta en el registro con un estado válido y como máximo una está *en curso* o *bloqueada*.

## 3. Fuentes (por resumen, 21-oct-2026)
Kanban Guide (límite de trabajo en curso y políticas explícitas) y Scrum Guide (lo que no cumple la definición de terminado no se entrega). Guías de metodologías ágiles usadas como referencia de concepto; ninguna habla de equipos de una sola persona.

## 4. Límites
- La regla "una Alta no se difiere por decisión de la entrega" es consecuencia de la regla de la estrategia de pruebas ya decidida; no tiene fuente externa.
- Las columnas del registro y los estados son propuesta del asistente.
- El script comprueba los estados y el límite de una entrega activa, no que las condiciones de terminado se hayan cumplido de verdad.

## 5. Pendientes del plan
Revisión por otra persona (DP-23); versiones exactas (micro) y forma de instalar Django; del plan de carga: formato del origen, consentimiento de los inquilinos actuales y fecha.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`, más una prueba negativa en una copia temporal.