# Actualización 2026-10-26 (a) — E1, grupo G: herramienta de medición y buenas prácticas por dispositivo

**Fecha:** 2026-10-26
**Documentos afectados:** código en [`src/despliegue/medir_reduccion.py`](../../../src/despliegue/medir_reduccion.py), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS RF-02, RF-50; CA-73, CA-82; criterio de salida de la E1 (peso de fotos reales de un iPhone y dos Android); instrucciones del solicitante: «sí, escribe el grupo G» y «utiliza esto [la carpeta `img`] y aplica buenas prácticas según estudios de internet y proyectos open source parecidos sobre cómo se tratan los formatos de imagen según el dispositivo» (26-oct-2026)
**Estado:** herramienta escrita y probada; **la medición con fotos reales NO está hecha**; no aprobado

## 1. Lo que contiene la carpeta `img/` (y por qué no basta)
| Archivo | Qué es | ¿Sirve para el criterio? |
|---|---|---|
| `Untitled diagram-…png` | Diagrama PNG 2477x2625 con transparencia | No: no es una foto de teléfono |
| `WebBackend Application Flow-…png` | Diagrama PNG 7490x2785 con transparencia | No |
| `WhatsApp Image 2026-10-13…jpeg` | JPEG 1137x520, **sin EXIF** y con perfil ICC | No: WhatsApp ya lo recomprimió y le quitó los metadatos |

Ninguna es la foto original de un iPhone ni de un Android. Para el criterio de salida hacen falta **tres originales sin editar** (en el iPhone, enviados por cable o «Más compatible» y no por WhatsApp). La carpeta `img/` **no está en Git** y no se agrega: son archivos del solicitante.

## 2. Qué se escribió
`src/despliegue/medir_reduccion.py CARPETA [--guardar SALIDA]`: abre un navegador real (Chrome, Edge o Firefox), carga el **mismo script** que usa la aplicación y, por cada imagen de la carpeta, imprime tipo, píxeles, peso, si trae GPS, orientación, perfil de color y nombres de etiquetas EXIF (**sin valores**), y luego lo que enviaría el script: peso, píxeles, calidad, si cumple los 2 MB y los 5 MiB y qué metadatos conserva. No sube nada ni copia las fotos.

## 3. Medición de lo que sí había (Chrome 155; solo prueba la herramienta, **no es CA-73**)
| Imagen | Original | Enviado | Peso |
|---|---|---|---|
| Diagrama 1 | PNG 2477x2625, 0,33 MiB | JPEG 1933x2048, calidad 0,85 | 0,15 MiB (46 %) |
| Diagrama 2 | PNG 7490x2785, 0,79 MiB | JPEG 2048x762, calidad 0,85 | 0,10 MiB (12 %) |
| Imagen de WhatsApp | JPEG 1137x520, 0,33 MiB | JPEG 1137x520, calidad 0,85 | 0,26 MiB (79 %) |

Los PNG con transparencia salen con fondo blanco y el lado mayor se reduce a 2048. El JPEG del navegador trae un perfil sRGB y ninguna etiqueta EXIF ni GPS.

## 4. Buenas prácticas por dispositivo: fuentes y qué cambia
| Fuente | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|
| [Apple Soporte 116944](https://support.apple.com/en-us/116944) | Leída (resumen de la herramienta) | «Más compatible» captura JPEG y no HEIF; al compartir con equipos que no lo admiten Apple puede convertir a JPEG; en transferencia USB puede convertir salvo «Conservar originales» | Es el resumen de la herramienta, no el texto completo |
| [MDN, createImageBitmap](https://developer.mozilla.org/en-US/docs/Web/API/Window/createImageBitmap) | Leída (resumen) | `imageOrientation: "from-image"` es el valor por defecto y aplica la orientación EXIF | No se vio la tabla de compatibilidad por navegador |
| [Compressor.js](https://github.com/fengyuanchen/compressorjs) (proyecto open source de compresión en navegador) | Leída (resumen) | Recomienda lados de 4096 o menos por los límites del lienzo; avisa de que hay JPEG con orientación no estándar y de que con archivos de ~10 MB hay que cuidar la memoria; quita el EXIF por defecto; la calidad 0,6–0,8 es el equilibrio habitual; no resuelve la transparencia (el ejemplo rellena de blanco) | Es documentación del proyecto, no un estudio |
| [Hilo de Apple Developer Forums sobre Safari 17](https://developer.apple.com/forums/thread/743049), [comentario en Hacker News](https://hn.svelte.dev/item/23261216), [heic-normalize](https://libraries.io/npm/heic-normalize) | **Solo resultados de búsqueda; no se abrieron** | Con `accept="image/jpeg,image/png"` Safari entrega JPEG a quien elige una foto HEIC (relato de un desarrollador, de hace años); en Safari 17+ incluir `image/heic` en `accept` renombra archivos; solo Safari 17+ decodifica HEIC y los demás navegadores necesitan una biblioteca (heic2any) | Anécdotas y foros; **no hay documentación oficial de Apple sobre la conversión en el selector** |
| Páginas sobre Ultra HDR ([Android Developers](https://developer.android.com/media/grow/ultra-hdr/edit) y otras) | **Solo resultados de búsqueda; no se abrieron** | Ultra HDR es un JPEG con un mapa de ganancia; los sitios que vuelven a codificar la imagen lo pierden | No dicen qué hace el lienzo del navegador |

No encontré **estudios universitarios** sobre este punto; lo anterior es documentación de proveedores y de proyectos open source, y lo marco como tal.

## 5. Qué dice esto del diseño actual (hallazgos y propuestas, sin aprobar)
1. **HEIC (iPhone con «Alta eficiencia»).** El script no lo decodifica y el servidor lo rechaza (RF-02 admite JPEG y PNG). El campo `accept` no incluye `image/heic`, que es lo que evita el problema de Safari 17. La ruta práctica es que el selector de iOS entregue JPEG; **está sin verificar con un iPhone real**. *Propuesta:* no agregar una biblioteca de HEIC (rompe «sin bibliotecas» y pesa mucho); si el iPhone entrega HEIC, el mensaje ya pide JPEG o PNG; se puede sumar la indicación «en el iPhone: Ajustes → Cámara → Formatos → Más compatible».
2. **Android con Ultra HDR o cámaras de 50 a 200 megapíxeles.** El lienzo y el servidor vuelven a codificar, así que el mapa de ganancia se pierde: la foto queda en SDR, aceptable para una cédula. El riesgo real es la **memoria** con originales enormes (Compressor.js lo advierte); el script ya reduce a 2048 px, pero decodifica la imagen completa. *Propuesta:* medir con una foto de la mayor resolución y, si falla, decodificar ya reducida con las opciones de `createImageBitmap` (`resizeWidth` y `resizeHeight`).
3. **Orientación.** `from-image` es el valor por defecto y es lo correcto; los JPEG con valores no estándar siguen siendo un riesgo menor, que la medición debe incluir.
4. **Color.** El JPEG del navegador sale con perfil sRGB: una foto en un espacio más amplio (Display P3 de un iPhone) se convierte; no lo medí.
5. **Metadatos.** El navegador ya quita EXIF y GPS y el servidor los vuelve a quitar (dos barreras). La medición con fotos reales debe confirmarlo.

## 6. Qué falta
- **Decisión tuya:** ¿cómo conseguimos las tres fotos originales? (iPhone por cable o AirDrop a un PC, y dos Android por cable o «compartir» sin WhatsApp). Con ellas corro `medir_reduccion.py`, registro peso, calidad y metadatos y, solo entonces, marco CA-73 y CA-82.
- Comprobación manual del navegador sin lienzo y cierre de la E1 con las nueve condiciones: dependen de lo anterior y **no se cerraron**.
- GitHub Actions: el resultado lo confirma el solicitante.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
