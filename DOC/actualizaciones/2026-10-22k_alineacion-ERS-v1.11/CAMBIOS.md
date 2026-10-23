# Actualización 2026-10-22 (k) — Alineación de los documentos con la ERS v1.11

**Fecha:** 2026-10-22
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado; mismo criterio que la [actualización 2026-10-22 (g)](../2026-10-22g_alineacion-ERS-v1.10/CAMBIOS.md)):** [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md), [Modelo de datos v0.4](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.4_borrador.md), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md), [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md), el [registro de avance](../../fase-5-implementacion/AVANCE_IMPLEMENTACION.md), los README de las fases 1 a 5 y [DOC/README.md](../../README.md)
**Origen:** [2026-10-22 (j)](../2026-10-22j_ERS-v1.11/CAMBIOS.md)
**Estado:** borrador; no aprobado

## 1. Motivo
Tras publicar la ERS v1.11, seis documentos declaraban la v1.10 como base y faltaban RF-51, RF-52 y CA-75 a CA-77 en la estrategia de pruebas y el plan (14 problemas del script). El solicitante pidió alinearlos (22-oct-2026).

## 2. Cambios
| Documento | Cambio |
|---|---|
| DAS v0.11 | Base ERS v1.11; la viñeta de archivos privados recoge la fotografía del contrato (misma reducción y zona temporal, consulta auditada como propuesta, DP-28 y DP-29 abiertas); fila nueva en la trazabilidad; nota en el historial. **Sin ADR nuevos ni cambios de stack** |
| Modelo de datos v0.4 | Base ERS v1.11. **Solo una nota:** la entidad Documento del contrato y el registro de archivos temporales **no están en el modelo**; se añaden en una versión nueva (v0.5) |
| Diseño técnico v0.7 | Base ERS v1.11; dos operaciones nuevas en la tabla de permisos (RF-51 y RF-52); flujo F-10; **nuevo hallazgo HT-11** (el perfil de la propiedad no está diseñado); pendiente 8 |
| Estrategia de pruebas v0.3 | Base ERS v1.11; CA-75 (Media), CA-76 y CA-77 (Alta) asignados; recuento 77 de 77 |
| Plan de implementación v0.1 | Base ERS v1.11; RF-51, RF-52 y CA-75 a CA-77 en la **E2**; riesgo nuevo HI-08 |
| Lista de verificación v0.1 | Base ERS v1.11; nota de que la fotografía del contrato entra en el área 3 por analogía; sin puntos nuevos |
| Registro de avance | E2 pasa de 0/20 a 0/23 CA; línea nueva en el historial |

## 3. Corrección a lo anunciado
En la [actualización (j)](../2026-10-22j_ERS-v1.11/CAMBIOS.md) se propuso asignar RF-51 y CA-75 a la E1. **Se asignaron a la E2**: el perfil de la propiedad y el contrato vigente no existen hasta la E2, y no se puede probar la acción sin ellos. La E1 entrega el mecanismo de subida de la cédula y la zona temporal. La asignación es propuesta del asistente.

## 4. Lo que propone el asistente y el solicitante no decidió
- Asignar RF-51 y RF-52 a la **E2**, y los niveles y prioridades de CA-75 (Media), CA-76 y CA-77 (Alta).
- El flujo **F-10** y las filas de permisos de RF-51 y RF-52 del diseño técnico.
- **HT-11:** contenido del perfil de la propiedad; la zona temporal (HT-10) cubriendo la fotografía del contrato.

## 5. Qué no se hizo
- **No se creó la versión v0.5 del modelo de datos** ni la entidad Documento del contrato: es una versión nueva pendiente.
- No se resolvieron HT-11, DP-28 ni DP-29; no se añadió ningún ADR.
- La cifra de reducción de la fotografía del contrato no existe; se mide en la E2 con fotos reales (HI-08).
- El script comprueba identificadores, enlaces, bases y cobertura, no el contenido; se revisaron a mano las diferencias de Git.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`: sin problemas (52 RF y 77 CA con matriz, pruebas y plan completos; 7 entregas registradas, ninguna en curso).

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
