# Actualización 2026-10-21 (z) — Revisión por otra persona (DP-23)

**Fecha:** 2026-10-21
**Documentos afectados (editado en su sitio, porque no está reemplazado ni aprobado):** [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) (sección 3.3 nueva, sección 4, HI-03, sección 8), README de la [fase 5](../../fase-5-implementacion/README.md) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Decisión
| # | Pregunta | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | ¿Cómo se resuelve la revisión por otra persona (DP-23)? | Persona distinta obligatoria para lo crítico antes de cargar datos reales; el resto con autorevisión y herramientas | Igual |

## 2. Qué es "crítico" (propuesta del asistente)
Seguridad y datos personales (ADR-003, 024, 026 y 027; RF-26 a RF-28, RF-40, RF-41 y RF-45; RNF-14 y RNF-15) y el modelo financiero (R1 a R19, RN-18, bloqueo de fila y saldos). Con lista de verificación y registro de hallazgos.

## 3. Fuentes
NIST SP 800-218 (SSDF), prácticas PW.2.1 y PW.7.1: encontradas solo en páginas de terceros que reproducen el texto de NIST; el PDF de NIST se descargó pero no se pudo leer (sin `pdftoppm`) y la página oficial solo da el resumen. Es un marco para organizaciones, usado como referencia.

## 4. Límites
- **No hay persona designada.** La condición de la sección 4 no se da por cumplida hasta que exista y revise.
- La combinación de revisión humana y herramientas, y qué es crítico, son propuesta del asistente.
- Ninguna revisión hecha por el asistente es independiente: el asistente redactó los documentos.
- La lista de verificación aún no está preparada.

## 5. Pendientes del plan
Designar a la persona revisora; preparar la lista de verificación; versiones exactas (micro) y forma de instalar Django; del plan de carga: formato del origen, consentimiento de los inquilinos actuales y fecha.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.