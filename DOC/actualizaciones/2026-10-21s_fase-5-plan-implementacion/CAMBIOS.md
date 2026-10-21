# Actualización 2026-10-21 (s) — Fase 5: plan de implementación v0.1

**Fecha:** 2026-10-21
**Documentos afectados:** [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) (nuevo); README de la [fase 5](../../fase-5-implementacion/README.md) y [DOC/README.md](../../README.md); además, ediciones en su sitio por la regla de contratos anulados: [ERS v1.9](../../fase-1-ers/ERS_SGA_001_v1.9_borrador.md) (RN-02), [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md) (ADR-031), [Modelo de datos v0.4](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.4_borrador.md) (R2 y sección 13) y [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md)
**Estado:** borrador; no aprobado

## 1. Decisiones del solicitante
| # | Pregunta | Decisión | Recomendación |
|---|---|---|---|
| 1 | ¿Un contrato anulado cuenta para el solape de fechas (RN-02)? | **No cuenta** (regla de negocio; no validada por abogado) | Igual |
| 2 | ¿Con qué criterio se ordenan las entregas? | Esqueleto andante primero y rebanadas verticales por riesgo y dependencia | Igual |

## 2. Qué se creó
- **Plan de implementación v0.1 (PIM-SGA-001):** siete entregas más una fase posterior; cada una con aplicaciones, contenido, requisitos funcionales y no funcionales, criterios de aceptación y criterio de salida.
- **Trazabilidad comprobada:** los 47 RF y los 61 CA aparecen exactamente una vez en la tabla de entregas, y los 18 RNF al menos una vez (RNF-06 se añadió a la E0 al comprobarlo).
- **Hallazgos HI-01 a HI-03:** la E0 no puede enviar avisos de seguridad por correo (llegan en la E4); CA-47 se reparte entre E0 y E4; un solo desarrollador sin revisión independiente.

## 2b. Script
`verificar_coherencia.ps1` se amplió para incluir el plan de implementación: citas, base declarada, vigencia, README de la fase 5 y que cada RF y CA conste exactamente una vez en la tabla de entregas. Prueba negativa en una copia temporal con tres fallos introducidos a propósito (una base desactualizada, un RF sin entrega y un RF repetido): los detectó. La copia se borró.

## 3. Fuentes
Fowler, MonolithFirst (por resumen); esqueleto andante de Cockburn (solo resultados de búsqueda, fuentes secundarias; el Agile Alliance dio 404). Sin estudios universitarios.

## 4. Límites
- Los criterios de salida, la agrupación en entregas y el orden interno son propuesta del asistente; el solicitante solo decidió el principio de orden.
- No hay estimaciones de tiempo ni de esfuerzo.
- El plan de carga inicial de datos queda pendiente.

## 5. Pendientes (sección 8 del plan)
Definición de "terminado"; plan de carga inicial; entornos, tamaño y región del Droplet; versiones de Python y Django; registro de avance y regla ante una entrega Alta incompleta; revisión por otra persona.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.