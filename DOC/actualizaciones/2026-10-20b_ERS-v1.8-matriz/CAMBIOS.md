# Actualización 2026-10-20 (b) — Corrección de la matriz de trazabilidad de la ERS v1.8

**Fecha:** 20 de octubre de 2026
**Documentos afectados:** [ERS v1.8](../../fase-1-ers/ERS_SGA_001_v1.8_borrador.md) (sección 10 e historial de versiones), [README de la fase 4](../../fase-4-pruebas/README.md) y [DOC/README.md](../../README.md).
**Versión anterior:** la misma ERS v1.8 antes de la corrección (queda en Git). No se creó versión nueva: es una corrección de completitud sin cambio de reglas ni de requisitos, igual que la [actualización 2026-10-17e](../2026-10-17e_QA-documentos/CAMBIOS.md). Decisión del solicitante: corregir en la v1.8.
**Estado:** borrador; no aprobado.

## 1. Motivo
Validación previa a la fase 4 (20-oct-2026): nueve requisitos definidos en la ERS no aparecían en la matriz de la sección 10. El script de coherencia no lo detecta porque solo comprueba que los IDs citados estén definidos, no que los definidos estén en la matriz.

## 2. Cambios
| ID | Tipo | Descripción | Origen (pregunta → respuesta) |
|---|---|---|---|
| M1 | modificado | RN-10 añadido a "Administrar propiedades y contratos" (ya cita CA-10) | "verifica y validado todo antes de la fase 4" → hallazgo; "corrige la matriz en la v1.8" |
| M2 | modificado | RN-15 añadido a "Generar obligaciones sin duplicados" (CA-30), con la salvedad de que solo cubre la generación a 30 días | Ídem |
| M3 | modificado | RN-25 añadido a "Restringir acceso y auditar" (ya cita CA-13) | Ídem |
| M4 | añadido | Fila "Requisitos no funcionales sin criterio de aceptación": RNF-05, RNF-07, RNF-08, RNF-09, RNF-10, RNF-11, verificados en la fase 4 | Ídem |
| M5 | modificado | Fila de la v1.8 en el historial de versiones | Regla 3 de `CLAUDE.md` |

## 3. Impacto
Solo trazabilidad. No cambia ningún requisito, regla ni criterio, ni identificadores.

## 4. Decisiones
Ninguna resuelta. **Pendiente (hallazgo):** la segunda mitad de RN-15 (no aceptar movimientos sobre obligaciones de períodos que aún no inician, salvo el inmediato siguiente) no tiene criterio de aceptación. Un CA nuevo sería un cambio de contenido: se propone decidirlo en la fase 4 o en la próxima versión de la ERS.

## 5. Evidencia y fuentes
Lectura de las secciones 8, 9 y 10 de la ERS v1.8. Los RNF se marcan "sin CA" por no haber ningún criterio de la sección 9 que los cubra (búsqueda por texto); no se probó nada.

## 6. Verificación
Comprobación de rangos expandidos de la matriz frente a las definiciones (46 RF, 30 RN, 18 RNF, 57 CA) y `powershell -File DOC\herramientas\verificar_coherencia.ps1`. Limitación: no se verificó que cada CA pruebe realmente el requisito asignado, porque los CA no citan IDs en su cuerpo. Revisión de pares: no realizada.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | brandonC-developer | Pendiente | Pendiente |
