# Actualización 2026-10-21 (u) — Plan de implementación: carga inicial de datos

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque no está reemplazado ni aprobado):** [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) (sección 5 reescrita, E5 y sección 8), README de la [fase 5](../../fase-5-implementacion/README.md) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Decisión
| # | Pregunta | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | ¿Cómo se cargan los datos iniciales (inquilinos, contratos y saldos de apertura)? | Digitación por las pantallas del sistema, con conciliación contra los registros actuales; sin script de importación | Igual |

## 2. Procedimiento
Origen fuera del sistema y del repositorio; al menos dos ensayos con datos ficticios, uno con reversión; carga real con consentimiento registrado por inquilino (RF-39); conciliación de conteos y de saldos de apertura por contrato y total; respaldo completo previo como reversión; constancia de la carga sin datos personales. El procedimiento es propuesta del asistente; solo la decisión de digitar por las pantallas es del solicitante.

## 3. Fuentes
Solo resultados de búsqueda de nivel bajo (KPMG, Redwerk y glosarios de migración de datos): ensayos previos, conciliación de conteos, totales y saldos, tolerancia mínima y punto de reversión. Ninguna compara digitar con importar en un conjunto pequeño; esa elección es criterio del asistente, apoyado en el volumen de la ERS (hasta 50 propiedades, DP-06).

## 4. Límites
- Sin fuente de calidad: no hay norma ni estudio universitario consultado.
- El consentimiento de los inquilinos actuales (RF-39, DP-21) puede ser un obstáculo práctico de la carga; no lo resuelve esta decisión.
- Quien digita y quien concilia es la misma persona (DP-23).

## 5. Pendientes
Formato y ubicación de los registros de origen; consentimiento de los inquilinos actuales; cuándo se hace la carga real. Del plan, además: entornos, tamaño y región del Droplet; versiones de Python y Django; registro de avance y regla ante una entrega Alta incompleta; revisión por otra persona.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.