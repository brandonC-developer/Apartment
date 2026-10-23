# Actualización 2026-10-23 (zo) — BR-05: metadatos de las fotografías (DP-27)

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el modelo de amenazas (versión nueva: BR-05, AM-09), la ERS (resolver DP-27 y quizá un criterio nuevo), el DAS (ADR-003) y el diseño técnico. [DOC/README.md](../../README.md)
**Origen:** brecha BR-05 y amenaza AM-09 del [modelo de amenazas v0.3](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.3_borrador.md); DP-27 y RF-50 de la [ERS v1.15](../../fase-1-ers/ERS_SGA_001_v1.15_borrador.md)
**Estado:** decisión registrada; documentos sin cambiar; no aprobado

## 1. Pregunta, respuesta y decisión
| Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|
| ¿Cómo se tratan los metadatos de las fotografías (por ejemplo, la ubicación GPS) que el navegador pueda dejar en el archivo? | "Probar en E2 y quitar en servidor si quedan" (recomendada por el asistente) | En la entrega E2 se mide, con un iPhone y dos teléfonos Android, si la reducción del navegador (RF-50, RF-52) elimina los metadatos. Si queda alguno, **o** si se usa el original de respaldo de RF-50 (el navegador no pudo reducirla), el servidor los elimina al guardar el archivo. Si la prueba muestra que siempre se eliminan, solo el camino del original queda cubierto por el servidor |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Discusión WHATWG "Add EXIF metadata support in Canvas.toBlob?" (2013): https://lists.whatwg.org/pipermail/whatwg-whatwg.org/2013-June/081990.html | Lista de correo de un organismo de estándares | **Solo resultados de búsqueda** (23-oct-2026); no se abrió | Un editor de imágenes que re-codifica con `toBlob` pierde todos los metadatos; el error W3C que pedía conservarlos se cerró como WONTFIX | De 2013; no es la especificación vigente ni se probó en navegadores actuales |
| Documentación de Bright (EXIF Metadata Leakage) y la de django-filer (validación de archivos): https://docs.brightsec.com/docs/exif-metadata-leakage, https://django-filer.readthedocs.io/en/3.5.0/validation.html | Terceros | **Solo resultados de búsqueda** | La reducción en el navegador no es una frontera de seguridad (una petición directa la omite); re-codificar en el servidor es el método habitual para quitar metadatos | Blogs y documentación de terceros; no se leyeron completos |
| OWASP, File Upload Cheat Sheet | Guía de experto reconocido | **No encontrada ni leída** en esta búsqueda | Nada: no se cita para esta decisión | — |

## 3. Lo que propone el asistente y el solicitante no decidió
- Qué biblioteca elimina los metadatos y si se re-codifica o se quitan solo los segmentos de metadatos: no se investigó. Re-codificar dos veces puede restar nitidez a la cédula; no se midió.
- Si el máximo de nitidez exige conservar la orientación (el tag de orientación se pierde al re-codificar; RF-50 ya pide conservar la orientación visible).
- Si hace falta un criterio de aceptación nuevo o ampliar CA-73, CA-74 o CA-77.

## 4. Qué no se hizo
- No se resolvió DP-27 en la ERS (requiere una v1.16) ni se actualizó el modelo de amenazas (v0.4).
- No se probó nada con fotos reales ni con navegadores actuales.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
