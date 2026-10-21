# Actualización 2026-10-21 (x) — Versiones de Python y Django

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado):** [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md) (ADR-022, referencia 35), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) (sección 5.2, sección 8), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md) (pendientes), README de la [fase 5](../../fase-5-implementacion/README.md) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Decisión
| # | Pregunta | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | ¿Qué versiones de Python y Django se usan? | Django 5.2 LTS con el Python 3.14 del sistema (Ubuntu 26.04) | Igual |

Esta decisión reemplaza la preferencia de la v0.10 por la 6.2 LTS: esta no estará publicada hasta abril de 2027.

## 2. Fuentes (por resumen, 21-oct-2026)
- Django, descargas: 5.2 LTS (última 5.2.18) con soporte ampliado hasta abril de 2028; 6.0 hasta abril de 2027; 6.1 hasta diciembre de 2027; 6.2 LTS prevista para abril de 2027, hasta abril de 2030.
- Django, FAQ de instalación: la 5.2 admite Python 3.10 a 3.14 (la 3.14 desde la 5.2.8); recomienda la última versión de Python 3.
- Python, guía de versiones: la 3.14 sale en octubre de 2025 y su fin de vida programado es octubre de 2030 (las fechas programadas pueden cambiar).
- Ubuntu 26.04, resumen para usuarios LTS: Python 3.14, PostgreSQL 18 y Django 5.2 LTS. No dice cuál es el `python3` por defecto.

## 3. Límites
- `packages.ubuntu.com` no se pudo abrir, así que no se confirmó el `python3` por defecto ni el paquete exacto de PostgreSQL 18 en esa versión.
- Que el Django 5.2 de Ubuntu sea el que se use no se decidió; se propone `pip` en un entorno virtual para fijar la versión.
- Que el salto de la 5.2 a la 6.2 sea sencillo es de memoria del asistente.

## 4. Pendientes del plan
Registro de avance y regla ante una entrega Alta incompleta; revisión por otra persona; versiones exactas (micro) y forma de instalar Django; del plan de carga: formato del origen, consentimiento de los inquilinos actuales y fecha.

## 5. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.