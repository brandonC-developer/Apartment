# Actualización 2026-10-17 (e) — QA de vigencia de los documentos

**Fecha:** 17 de octubre de 2026
**Documentos revisados:** todos los `.md`, el script y la skill (37 archivos versionados al inicio). Vigentes: [ERS v1.8](../../fase-1-ers/ERS_SGA_001_v1.8_borrador.md), [DAS v0.7](../../fase-2-arquitectura/DAS_SGA_001_v0.7_borrador.md), [modelo de datos v0.3](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.3_borrador.md).
**Estado:** correcciones aplicadas sobre los tres vigentes (siguen siendo borradores) y sobre los README. No se creó versión nueva de la ERS, el DAS ni el modelo: son correcciones de completitud sin cambio de reglas; el historial queda en Git y en sus tablas de versiones.

## 1. Método

1. Inventario de archivos frente a los README de cada fase y a `DOC/README.md`.
2. Búsqueda de referencias a versiones anteriores dentro de los documentos vigentes.
3. Búsqueda de rangos y conteos obsoletos (OL-01 a OL-18, CA-01 a CA-50, etc.).
4. Contraste de cifras clave entre ERS, DAS, modelo y resumen legal (15 caracteres, 24 h, 1 h, 30 y 120 días, cinco días hábiles, tres abonos, 07:00, cinco intentos, 50 propiedades, 35 días, siete días, diez años).
5. Contraste de cobertura: cada requisito nuevo (RF-46, RNF-18, OL-19 a OL-21) debe aparecer en alcance, entidades, módulos, riesgos, lista de revisión y referencias.
6. Ejecución del script de coherencia, antes y después.

## 2. Estado de Git

Al empezar, el árbol de trabajo estaba limpio y sincronizado con `origin/main` (0 commits por delante o por detrás); los 37 archivos estaban versionados. No se verificó la visibilidad del repositorio remoto. **Las correcciones de esta actualización están sin confirmar.**

## 3. Hallazgos y corrección

| # | Hallazgo (documento desactualizado) | Gravedad | Corrección |
|---|---|---|---|
| Q1 | ERS 7.1 no tenía la entidad Incidente de seguridad, aunque RF-46 y el modelo v0.3 la usan; la entidad Auditoría seguía con la redacción anterior a H10 | Alta | Entidad añadida y Auditoría reescrita |
| Q2 | DAS: sin módulo ni entidad de incidentes (secciones 5, 6, 8) aunque existe ADR-021 | Alta | Módulo, bloque y entidad añadidos |
| Q3 | ERS 2.3 (alcance) sin gestión de incidentes | Media | Viñeta añadida |
| Q4 | ERS lista de revisión (sección 14) sin seguridad, restauración ni asesor legal | Media | Tres casillas añadidas |
| Q5 | ERS sección 16 sin el Reglamento 37554-JP, que sí se usó | Media | Referencia 4b añadida |
| Q6 | ERS sección 11 sin riesgo de incidente sin aviso | Baja | Fila añadida |
| Q7 | README fase 4 citaba CA-01 a CA-50 de la ERS v1.5 | Media | CA-01 a CA-57 de la ERS v1.8 |
| Q8 | README fase 5 citaba ERS v1.5, DAS v0.4 y "elección de proveedor de WhatsApp" (DP-04 está diferida) | Media | Corregido |
| Q9 | README fase 6 citaba DAS v0.4 y presentaba DP-07 y DP-08 como abiertas; faltaban endurecimiento, documento de seguridad e incidentes | Alta | Corregido |
| Q10 | `DOC/README.md` decía que nada se había confirmado en Git y tenía un título "Pendiente de recomendar" obsoleto | Media | Corregido; se añade advertencia sobre visibilidad |
| Q11 | Evaluación de la metodología hablaba de faltantes del DAS v0.4 ya cubiertos | Baja | Nota de actualización al inicio; el cuerpo no se reescribe |
| Q12 | Resumen legal v2 no mencionaba el servidor propio, la exposición por internet ni el proyecto aparte de WhatsApp, relevantes para B6 y la transferencia de datos | Media | Dos viñetas en la sección 1 |
| Q13 | Modelo v0.3: hallazgos H1 a H3, H9 y H10 aún decían "deben incorporarse"; H7 y H8 sin estado | Media | Estado de cada hallazgo actualizado |
| Q14 | DAS citaba el modelo v0.2 como evidencia sin aclarar que la v0.3 es la vigente | Baja | Aclaración añadida |
| Q15 | CLAUDE.md no listaba el prefijo RE entre los identificadores | Baja | Añadido |
| Q16 | El script no comprobaba el prefijo RE, ni que el README marque la última versión como vigente, ni la versión del encabezado, ni CAMBIOS.md en cada actualización | Media | Script ampliado y probado con una falla provocada (README alterado, detectada, restaurado) |

## 4. Consistencia de cifras entre documentos

Sin discrepancias entre ERS, DAS, modelo y resumen legal en las cifras revisadas (paso 4). La regla de pago anticipado del resumen legal (A11) coincide con RN-15 y OL-11.

## 5. Verificación

`verificar_coherencia.ps1` sin problemas tras las correcciones (RNF 18, RF 46, RN 30, CA 57, OL 21, DP 26, ADR 21, RE 11; vigencia y CAMBIOS.md correctos; sin enlaces rotos). **Límites:** el script no comprueba lógica ni redacción; el contraste de cifras (paso 4) es una búsqueda por texto, no una lectura completa de cada documento; no hubo revisión por otra persona.

## 6. Lo que este QA no cubre

- Las versiones anteriores y el cuestionario se tratan como históricos y no se revisaron línea por línea.
- Las leyes no se contrastaron de nuevo con el SCIJ (no se puede leer el visor).
- No se probaron las entidades de incidentes en una base de datos.
- Ningún documento tiene validación legal ni aprobación.

## 7. Aprobación

| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | brandonC-developer | Pendiente | Pendiente |
