# Actualización 2026-10-21 (t) — Plan de implementación: definición de terminado

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque no está reemplazado ni aprobado):** [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) (sección 3.1 nueva, sección 8), README de la [fase 5](../../fase-5-implementacion/README.md) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Decisión
| # | Pregunta | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | ¿Qué significa "terminado" para cada entrega? | Lista común de nueve condiciones más el criterio de salida propio de cada entrega | Igual |

## 2. Lista
Las nueve condiciones (pruebas de los CA, integración continua, script de coherencia, archivo de privilegios, revisión de código sin cubrir, despliegue de pruebas, sin datos personales en registros, documentación y trazabilidad, sin defectos Alta) constan en la sección 3.1 del plan. Cuatro vienen de decisiones previas (EPP, ADR-025, ADR-027 y ADR-031, R14); las demás son propuesta del asistente.

## 3. Fuente
Scrum Guide (scrumguides.org), leída por resumen el 21-oct-2026: define la "definición de terminado" como una descripción formal del estado del incremento, que da transparencia, y dice que lo que no la cumple no se entrega. Es una guía de Scrum; se usa solo como referencia de concepto.

## 4. Límites
- Los criterios de salida propios de cada entrega siguen siendo propuesta del asistente.
- La condición 9 (sin defectos Alta abiertos) es propuesta del asistente sin fuente.

## 5. Pendientes del plan
Plan de carga inicial de datos; entornos, tamaño y región del Droplet; versiones de Python y Django; registro de avance y regla ante una entrega Alta incompleta; revisión por otra persona.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.