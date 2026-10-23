# Actualización 2026-10-23 (zp) — BR-06: análisis antivirus de las fotografías

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el DAS (ADR-003, pendiente "análisis antivirus"), el modelo de amenazas (versión nueva: BR-06, AM-07) y la ERS (RF-02, si se añade la decodificación como criterio). [DOC/README.md](../../README.md)
**Origen:** brecha BR-06 y amenaza AM-07 del [modelo de amenazas v0.3](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.3_borrador.md); pendiente de ADR-003 en el [DAS v0.14](../../fase-2-arquitectura/DAS_SGA_001_v0.14_borrador.md)
**Estado:** decisión registrada; documentos sin cambiar; no aprobado

## 1. Pregunta, respuesta y decisión
| Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|
| ¿Se añade un análisis antivirus a las fotografías subidas (solo JPEG y PNG)? | "No antivirus; validar y decodificar la imagen" (recomendada por el asistente) | **No se instala antivirus.** Además de la lista blanca y la verificación del tipo real (RF-02, ADR-003), el servidor decodifica la imagen completa con la biblioteca de imágenes y rechaza el archivo si falla; nombre aleatorio, fuera de la raíz web y nunca ejecutable. Se reevalúa si algún día se aceptan otros formatos (por ejemplo, PDF) |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| OWASP, File Upload Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet | Guía de experto reconocido | **Solo resultados de búsqueda** (extractos citados por el buscador; no se abrió la página) | Pasar el archivo por antivirus o sandbox "si está disponible"; para imágenes, reescribirlas destruye el contenido malicioso inyectado; ningún control basta solo | Sin el texto completo; el extracto de la reescritura se leyó de segunda mano |
| Documentación de ClamAV (Docker): https://docs.clamav.net/manual/Installing/Docker.html | Documentación del proveedor | **Solo resultados de búsqueda** | Mínimo 3 GiB y preferible 4 GiB de RAM; más de 1,2 GiB solo para cargar las firmas; hasta 2,4 GiB al recargarlas | Fechada en 2020 según el buscador; habla de contenedores; no se verificó contra la versión actual |
| OPSWAT, Glasswall y similares | Proveedores de productos de escaneo | Solo resultados de búsqueda | Nada: son publicidad de sus productos; no se usan | — |

## 3. Lo que propone el asistente y el solicitante no decidió
- Que decodificar la imagen sea suficiente: es criterio del asistente, apoyado en un extracto de OWASP; **no se midió** cuántas fallas de bibliotecas de imágenes hay ni se verificó la biblioteca concreta (la cubren las actualizaciones de BR-04).
- Qué biblioteca decodifica la imagen y si se comparte con la eliminación de metadatos de la [actualización (zo)](../2026-10-23zo_br-05-metadatos-imagenes/CAMBIOS.md); si el servidor re-codifica por completo, cubriría ambas cosas, pero esa decisión no se tomó.
- El tamaño del Droplet no se cambia: la comparación de costos de subirlo no se hizo.

## 4. Qué no se hizo
- No se consultó el texto completo de OWASP ni la versión actual de la documentación de ClamAV.
- No se actualizaron ADR-003, el modelo de amenazas ni la ERS.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
