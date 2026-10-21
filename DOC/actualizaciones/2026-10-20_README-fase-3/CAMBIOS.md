# Actualización 2026-10-20 — Corrección del README de la fase 3

**Fecha:** 20 de octubre de 2026
**Documentos afectados:** [README de la fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md). No cambia ningún documento versionado (ERS, DAS, modelo de datos).
**Estado:** corrección de un README; los documentos siguen siendo borradores.

## 1. Motivo
Revisión de "qué falta" pedida por el solicitante (20-oct-2026): el README de la fase 3 seguía citando la ERS v1.6 y el DAS v0.5, y atribuía el estilo de API a ADR-002.

## 2. Cambios
| ID | Tipo | Descripción | Origen (pregunta → respuesta) |
|---|---|---|---|
| F3-1 | modificado | Entradas: ERS v1.8 y DAS v0.7, con enlaces | "verifica que hace falta" → hallazgo; "corrige el README de la fase 3" |
| F3-2 | modificado | ADR-002 es persistencia (estado "Propuesto; motor pendiente", DAS v0.7 sección 13); no define el estilo de API, que no tiene ADR | Ídem |
| F3-3 | añadido | Fila en el historial de `DOC/README.md` | Regla 3 de `CLAUDE.md` |

## 3. Impacto
Solo documentación de navegación. No cambia requisitos, reglas ni identificadores.

## 4. Decisiones
Ninguna resuelta. **Pendiente (propuesta, no decidida):** crear un ADR para el estilo de API antes de los contratos de API de la fase 3.

## 5. Evidencia y fuentes
Lectura de [DAS v0.7](../../fase-2-arquitectura/DAS_SGA_001_v0.7_borrador.md) (ADR-001 y ADR-002; búsqueda de REST/GraphQL sin resultados sobre estilo de API).

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1` (resultado en la respuesta de la sesión). Revisión de pares: no realizada.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | brandonC-developer | Pendiente | Pendiente |
