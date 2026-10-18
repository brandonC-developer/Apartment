# Documentación — Sistema de Gestión de Alquileres (SGA)

**Estado general:** ningún documento está aprobado. Todos son borradores.

## Mapa de fases

| Fase | Carpeta | Documento vigente | Estado |
|---|---|---|---|
| 1. Especificación de requisitos (ERS) | `fase-1-ers/` | `ERS_SGA_001_v1.8_borrador.md` | Borrador; pendiente de validación legal y aprobación |
| 2. Arquitectura de software | `fase-2-arquitectura/` | `DAS_SGA_001_v0.7_borrador.md` | Borrador; depende de la ERS |
| 3. Diseño técnico | `fase-3-diseno-tecnico/` | `MODELO_DATOS_SGA_001_v0.3_borrador.md` | Iniciada; solo el modelo de datos, en borrador sin revisar |
| 4. Estrategia y plan de pruebas | `fase-4-pruebas/` | — | No iniciada |
| 5. Plan de implementación | `fase-5-implementacion/` | — | No iniciada |
| 6. Despliegue y operación | `fase-6-despliegue-operacion/` | — | No iniciada |

Carpetas transversales:
- `legal/` — resumen para el abogado y, cuando lleguen, los dictámenes.
- `metodologia/` — evaluación de la metodología de seis fases y la plantilla de registro de cambios.
- `actualizaciones/` — un registro por cada actualización, con el motivo, los cambios, las decisiones y la evidencia.
- `.claude/skills/recomendacion-buenas-practicas/` (en la raíz del proyecto, fuera de `DOC/`) — skill con el modo de trabajo para recomendaciones.
- `herramientas/` — `verificar_coherencia.ps1`: comprueba que los identificadores citados en la ERS, el DAS y el modelo de datos estén definidos y que los enlaces entre archivos existan. Ejecutar con `powershell -File DOC\herramientas\verificar_coherencia.ps1`.

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
| 2026-10-17 (b) | `actualizaciones/2026-10-17b_ERS-v1.6_DAS-v0.5/` | ERS v1.6 y DAS v0.5; cierre de DP-22, DP-24 y DP-25 |
| 2026-10-17 (c) | `actualizaciones/2026-10-17c_ERS-v1.7_DAS-v0.6/` | ERS v1.7 y DAS v0.6; cierre de DP-07 y DP-08, DP-04 diferida; modelo de datos v0.1 y v0.2 con prueba en PostgreSQL; hallazgos H1 a H13 |
| 2026-10-17 (d) | `actualizaciones/2026-10-17d_ERS-v1.8_DAS-v0.7/` | ERS v1.8 y DAS v0.7; cierre de DP-14, DP-23 y DP-26; H4 provisional; lectura del Reglamento 37554-JP (OL-19 a OL-21); resumen para el abogado v2 |

## Pendiente de recomendar

El proyecto ya tiene un repositorio Git en la raíz creado por el solicitante (verificado antes; ningún cambio de esta documentación se ha confirmado ni subido todavía). Las fuentes consultadas (`metodologia/EVALUACION_METODOLOGIA_v1.md`, ajuste 5) recomiendan mantener la documentación bajo control de versiones con revisión de cambios. Hasta entonces, las versiones se distinguen por nombre de archivo.
