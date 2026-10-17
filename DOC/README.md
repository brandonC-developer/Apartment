# Documentación — Sistema de Gestión de Alquileres (SGA)

**Estado general:** ningún documento está aprobado. Todos son borradores.

## Mapa de fases

| Fase | Carpeta | Documento vigente | Estado |
|---|---|---|---|
| 1. Especificación de requisitos (ERS) | `fase-1-ers/` | `ERS_SGA_001_v1.5_borrador.md` | Borrador; pendiente de validación legal y aprobación |
| 2. Arquitectura de software | `fase-2-arquitectura/` | `DAS_SGA_001_v0.4_borrador.md` | Borrador; depende de la ERS |
| 3. Diseño técnico | `fase-3-diseno-tecnico/` | — | No iniciada |
| 4. Estrategia y plan de pruebas | `fase-4-pruebas/` | — | No iniciada |
| 5. Plan de implementación | `fase-5-implementacion/` | — | No iniciada |
| 6. Despliegue y operación | `fase-6-despliegue-operacion/` | — | No iniciada |

Carpetas transversales:
- `legal/` — resumen para el abogado y, cuando lleguen, los dictámenes.
- `metodologia/` — evaluación de la metodología de seis fases y la plantilla de registro de cambios.
- `actualizaciones/` — un registro por cada actualización, con el motivo, los cambios, las decisiones y la evidencia.
- `herramientas/` — `verificar_coherencia.ps1`: comprueba que los identificadores citados estén definidos y que los enlaces entre archivos existan. Ejecutar con `powershell -File DOC\herramientas\verificar_coherencia.ps1`.

## Convenciones

1. **Un solo lugar por documento.** Cada versión vive en la carpeta de su fase con el nombre `PREFIJO_VERSION_estado.md`. Una versión aprobada o reemplazada **no se edita**; los cambios van en una versión nueva.
2. **Cada actualización tiene su carpeta** en `actualizaciones/AAAA-MM-DD_<documentos y versiones>/` con un `CAMBIOS.md` basado en `metodologia/plantilla_CAMBIOS.md`. Esa carpeta enlaza los documentos de las carpetas de fase; no los copia.
3. **La trazabilidad empieza en el origen:** cada cambio de requisito indica la pregunta, la respuesta y la decisión que lo originó.
4. **Las decisiones pendientes** usan identificadores únicos (DP-nn) comunes a la ERS y al DAS.
5. **Ninguna fase se da por cerrada** hasta tener responsable, fecha y aceptación formal en su registro de aprobación.

## Historial de actualizaciones

| Fecha | Carpeta | Resumen |
|---|---|---|
| 2026-10-14 | `actualizaciones/2026-10-14_ERS-v1.4_DAS-v0.3/` | ERS v1.4 y DAS v0.3 |
| 2026-10-17 | `actualizaciones/2026-10-17_ERS-v1.5_DAS-v0.4/` | ERS v1.5 y DAS v0.4; obligaciones legales; revisión de coherencia |

## Pendiente de recomendar

Esta carpeta **no es un repositorio Git**. Las fuentes consultadas (`metodologia/EVALUACION_METODOLOGIA_v1.md`, ajuste 5) recomiendan mantener la documentación bajo control de versiones con revisión de cambios. Hasta entonces, las versiones se distinguen por nombre de archivo.
