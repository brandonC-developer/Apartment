# Actualización 2026-10-21 (ac) — Repaso final de coherencia global y limpieza de archivos

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado):** [ERS v1.9](../../fase-1-ers/ERS_SGA_001_v1.9_borrador.md), [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md), [Modelo de datos v0.4](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.4_borrador.md), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md), los README de las fases 1, 3, 4 y 6, y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Motivo
Tras la revisión por módulos ([2026-10-21 (ab)](../2026-10-21ab_revision-por-modulos/CAMBIOS.md)) se añadieron 2 requisitos y 11 criterios de aceptación y se modificaron muchos textos. El solicitante pidió un repaso final de coherencia global y eliminar los archivos basura o innecesarios.

## 2. Método
- Script `verificar_coherencia.ps1` (IDs, enlaces, vigencia, base declarada, cobertura de la matriz, de la estrategia de pruebas y del plan, estados del registro de avance).
- Búsqueda manual en los documentos vigentes de frases que el script no ve: recuentos antiguos (de RF, CA, eventos de seguridad y ADR), frases de "pendiente" ya resueltas, restos de WhatsApp como canal de la v1, README desactualizados y descripciones de entregas.
- Fin de línea y búsqueda de restos del daño del incidente de la actualización 2026-10-21 (j).

## 3. Correcciones
| Dónde | Qué estaba desactualizado | Corrección |
|---|---|---|
| DAS v0.11 (encabezado, sección 5 y estado) | Rangos "ADR-022 a ADR-026" | "ADR-022 a ADR-031" y se nombran los temas nuevos |
| Diseño técnico v0.7 (HT-05 y sección 7) | "Cuatro eventos"; pendientes ya resueltos (HT-01, HT-03, HT-08) | Se anota la ampliación a siete eventos y el estado real de los pendientes |
| Estrategia de pruebas v0.3 (sección 11, decisión 6) | "CA en la próxima ERS" | "Hecho: CA-58 en la ERS v1.9" |
| Modelo de datos v0.4 (registro de aprobación) | "Por designar (DP-23)" | brandonC-developer (DP-23: ocupa los tres roles) |
| ERS v1.9 (historial, sección 2.3 y entidades) | La fila 1.9 y el alcance no recogían RF-48, RF-49 ni CA-62 a CA-72 | Se completan la fila 1.9, la lista de lo incluido y las filas de Inquilino y Notificación |
| README de la fase 1 | Decía que DAS, modelo de datos, diseño técnico y pruebas seguían alineados con la v1.8 | Ahora los lista alineados con la v1.9 |
| README de la fase 3 | "WhatsApp espera a DP-04" como bloqueo | WhatsApp fuera de la v1; sin bloqueos |
| README de la fase 4 | "CA-58 a CA-61" | "CA-58 a CA-72" |
| README de la fase 6 | "ADR-023 a ADR-026" y sin el contexto de la fase 5 | "ADR-023 a ADR-031"; se añade el contexto de las etapas A y B y sus pendientes |
| Plan de implementación | Las descripciones de las entregas no recogían los requisitos nuevos | Se completan E0, E1, E2, E4 y E5 |
| DAS v0.11, sección 8 | Sin las entidades `TEXTO_CONSENTIMIENTO` y `TOKEN_RESTABLECIMIENTO` | Se añaden |

## 4. Archivos eliminados
| Archivo | Motivo | ¿Recuperable? |
|---|---|---|
| `actualizaciones/2026-10-17c_ERS-v1.7_DAS-v0.6/DAS_secciones_nuevas_BORRADOR.md` | Borrador de trabajo que se declaraba ya incorporado en el DAS v0.6 (secciones 1.1, 4.1 y anexo B); ningún archivo lo enlazaba ni lo citaba | Sí, está en el historial de Git (commit `6d758cc`) |
| Carpeta de trabajo temporal de la sesión (fuera del proyecto): scripts de auditoría, fragmentos de texto, el texto extraído de las leyes y una copia reconstruida del README | Andamios del asistente, sin valor para el proyecto | No hace falta |

**Se conservaron, a propósito:** las versiones anteriores de la ERS, el DAS, el modelo de datos, el diseño técnico y la estrategia de pruebas (la regla 2 de `CLAUDE.md` lo exige); los dos resúmenes para el abogado; el cuestionario de cierre y la evidencia de la prueba en PostgreSQL (los citan varias actualizaciones y documentos); la plantilla y la evaluación de la metodología. Antes de eliminar se comprobó que no hay archivos temporales, copias de respaldo, carpetas vacías ni archivos ignorados en el proyecto.

## 5. Estado final
49 RF, 30 RN, 18 RNF, 72 CA, 21 OL, 26 DP, 31 ADR y 11 RE, todos definidos; sin enlaces rotos; sin documentos desalineados con la ERS v1.9 ni el DAS v0.11 según el script.

## 6. Límites
- El repaso manual fue por búsqueda de frases y lectura de las secciones afectadas; no se releyó cada documento completo (la ERS tiene más de 100 KB).
- Contradicciones de fondo entre reglas que no comparten palabras clave podrían escapar a esta comprobación; la revisión por otra persona (plan, sección 3.3) es la que debe cubrirlas.
- La validación legal sigue declarada por el solicitante, sin dictamen.

## 7. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`: sin problemas.