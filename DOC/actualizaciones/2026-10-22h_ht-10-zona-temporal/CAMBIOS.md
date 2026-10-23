# Actualización 2026-10-22 (h) — HT-10: archivos de la cédula en una zona temporal con identificador de un solo uso

**Fecha:** 2026-10-22
**Documentos afectados (editados en su sitio; ninguno está reemplazado ni aprobado):** [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Modelo de datos v0.4](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.4_borrador.md), [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md), [README de la fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md)
**Origen:** hallazgo HT-10 de la [actualización 2026-10-22 (g)](../2026-10-22g_alineacion-ERS-v1.10/CAMBIOS.md)
**Estado:** borrador; no aprobado

## 1. Motivo
Al enviar el frente y el reverso de la cédula en peticiones separadas (decisión del 22-oct-2026), cada archivo llega antes de que exista el inquilino. El paso 4 del flujo F-01 del diseño técnico ("una transacción, sin archivos huérfanos") no se cumplía.

## 2. Pregunta, respuesta y decisión
| Pregunta | Opciones del asistente | Respuesta del solicitante | Decisión |
|---|---|---|---|
| ¿Cómo se reciben los archivos antes de crear el inquilino? | Zona temporal con identificador de un solo uso, o crear primero el inquilino en un estado provisional | "zona temporal con identificador de un solo uso" (22-oct-2026) | **Zona temporal privada**, fuera de la raíz web, con nombre aleatorio y sin enlace público; cada archivo devuelve un identificador de un solo uso. Al guardar el inquilino, en una transacción, se asocian los archivos y se mueven a su ubicación definitiva |
| ¿Cuánto se conserva un archivo temporal no asociado? | 24 horas (recomendado), 1 hora, 7 días | "24 horas" (recomendado por el asistente; fundamento: coincide con el cierre total de sesión de 24 horas del DAS) | Un proceso elimina lo no asociado a las 24 horas |

## 3. Cambios
| Documento | Cambio |
|---|---|
| Diseño técnico v0.7 | F-01 pasos 4 y 5 reescritos; HT-10 pasa a *resuelto*; pendiente 7 actualizado |
| Modelo de datos v0.4 | Nota: **el modelo aún no tiene la entidad o el registro de archivos temporales**; se añade en una versión nueva |
| DAS v0.11 | La viñeta de seguridad de archivos recoge la zona temporal y la caducidad |
| Plan de implementación v0.1 | HI-07 pasa a *decidido*, con lo que falta antes de la E1 |

## 4. Lo que queda por decidir o hacer
- **Propuesta del asistente, sin decidir:** que el identificador quede **ligado a la sesión del administrador** (un tercero con el identificador no podría usarlo) y que **caduque también al usarse**, aunque no hayan pasado las 24 horas.
- **Modelo de datos:** entidad o registro de archivos temporales (identificador, ruta, fecha de carga, sesión); requiere una versión nueva del modelo (v0.5).
- **ERS:** no tiene un criterio de aceptación para la caducidad ni para el identificador de un solo uso. Si el solicitante lo quiere, sería un CA nuevo en una ERS v1.11; hoy CA-74 solo cubre un archivo por petición.
- **Auditoría y retención:** si la carga o la eliminación de un archivo temporal se audita (RF-45 audita la consulta de cédulas, no la carga) y si el respaldo diario debe excluir la zona temporal. Sin decidir.
- **Prueba:** la caducidad y el identificador de un solo uso no tienen caso de prueba asignado en la estrategia de pruebas.
- **Legal:** una cédula pendiente de asociar es un dato personal guardado hasta 24 horas; el abogado no se ha pronunciado (DP-17).

## 5. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`: ver el resultado en la respuesta de la sesión.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
