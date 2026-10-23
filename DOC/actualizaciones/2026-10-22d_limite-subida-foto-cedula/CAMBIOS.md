# Actualización 2026-10-22 (d) — Límite de subida de la foto de la cédula y compresión en el navegador

**Fecha:** 2026-10-22
**Documentos afectados:** [README de la fase 6](../../fase-6-despliegue-operacion/README.md) y [DOC/README.md](../../README.md). No se edita ningún documento versionado.
**Continúa:** [2026-10-22 (b), pregunta abierta de tamaño de subida](../2026-10-22b_endurecimiento-nginx-gunicorn-postgresql/CAMBIOS.md)
**Estado:** investigación con **propuesta del asistente**; el solicitante aún no la decide.

## 1. Motivo y dato del solicitante
Se pidió una cifra con fundamento para `client_max_body_size` de Nginx. El solicitante aclaró (22-oct-2026): **se toma la foto y se comprime en el navegador con un canvas** para reducir el tamaño antes de subirla. Esa compresión **no está en la ERS v1.9 ni en el DAS v0.11**; es un requisito nuevo que el solicitante aún no ha formalizado.

**Lo que ya estaba decidido:** RF-02 (ERS v1.9) fija "JPEG y PNG, hasta 5 MB", con verificación del tipo real del archivo; el DAS v0.11 (sección 5) y el diseño técnico v0.7 lo repiten. El frente de la cédula es obligatorio y el reverso opcional (ERS, alcance). **El límite de 5 MB por archivo no se cambia en esta propuesta.**

## 2. Registro de fuentes
Consultadas el 22-oct-2026. WebFetch convierte la página a texto y una herramienta responde a una pregunta (no es lectura íntegra del asistente).

| # | Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|---|
| M1 | MDN, [HTMLCanvasElement.toBlob()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob) | Documentación de referencia | Página abierta | El tipo por defecto es `image/png` y también se usa si el pedido no se soporta; `quality` va de 0 a 1 y solo vale para formatos con pérdida (JPEG, WebP); el `callback` puede recibir `null`; la página no dice cuál es la calidad por defecto ni menciona límites de tamaño | JPEG y WebP "no en todos los navegadores" según la página |
| M2 | MDN, [CanvasRenderingContext2D.drawImage()](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/drawImage) | Documentación de referencia | Página abierta | En algunos navegadores antiguos `drawImage()` ignora la orientación EXIF, "especialmente en iOS"; hay que detectarla y corregirla | No dice nada del tamaño máximo del canvas |
| M3 | MDN, [image-orientation](https://developer.mozilla.org/en-US/docs/Web/CSS/image-orientation) | Documentación de referencia | Leída en parte (100 000 de 129 735 caracteres) | Por defecto (`from-image`) los navegadores rotan según EXIF, disponible desde abril de 2020 | Es una propiedad de CSS; no se verificó que `drawImage` en un canvas se comporte igual en los navegadores actuales |
| D1 | Django, [Settings](https://docs.djangoproject.com/en/5.2/ref/settings/) | Documentación oficial | Leída en parte (100 000 de 158 456 caracteres) | `FILE_UPLOAD_MAX_MEMORY_SIZE` por defecto 2,5 MB: por encima el archivo pasa al disco; `DATA_UPLOAD_MAX_MEMORY_SIZE` (2,5 MB) **excluye** los archivos; `DATA_UPLOAD_MAX_NUMBER_FILES` 100 | No dicen que Django limite el tamaño de un archivo subido: ese límite lo pone la aplicación (RF-02) |
| N1 | Nginx, [ngx_http_core_module](https://nginx.org/en/docs/http/ngx_http_core_module.html) (leído el 22-oct-2026, ver [2026-10-22 (b)](../2026-10-22b_endurecimiento-nginx-gunicorn-postgresql/CAMBIOS.md)) | Documentación oficial | Página abierta | `client_max_body_size` por defecto 1m; al superarlo responde 413 y "los navegadores no pueden mostrar correctamente este error"; se puede subir solo en una ubicación | — |
| V1 | Argos Identity, [mejores prácticas de imagen de documento](https://developers.argosidentity.com/en/verify/global_id_recognition/id_image_best_practice) | **Tercero** (proveedor de verificación de identidad) | Página abierta | Resolución mínima 300 DPI y recomendada 600 DPI; JPEG con calidad de 80 a 90 % y no comprimir por debajo del 70 %; tamaño recomendado 1 a 5 MB, óptimo 2 a 3 MB, máximo 50 MB | Es un proveedor comercial para su propio servicio, no un estándar; sirve como referencia, no como norma |
| V2 | Resultados de búsqueda sobre captura de documentos (Smile ID, Argos, Kairos) | Terceros, **solo resultados de búsqueda** | No se abrió: la página de Smile ID devolvió "no encontrada" | Los resultados citan "al menos 1000 píxeles a lo ancho de la tarjeta" (Smile ID), 640×480 mínimo y 1920×1080 recomendado, y archivos de 1 a 5 MB | **Sin validar.** No se encontró un estándar (ISO, NIST) específico para la captura de cédulas |
| V3 | pqina, [Canvas area exceeds the maximum limit](https://pqina.nl/blog/canvas-area-exceeds-the-maximum-limit/) | Blog técnico (apoyo) | Solo resultados de búsqueda | Safari reportaba un tope de 16 777 216 píxeles por canvas y fallos silenciosos (lienzo en blanco) con fotos grandes | Fuente de 2022; no hay confirmación de WebKit para versiones actuales: **probar en un iPhone real** |

**No se verificó:** el tamaño real de una foto de teléfono (no hay fuente leída; no se midió); el tamaño resultante tras comprimir (**no se midió**); si re-codificar con canvas elimina los metadatos EXIF (por ejemplo, la ubicación); el soporte de `toBlob` con JPEG en los navegadores objetivo.

## 3. Cálculo
La cédula costarricense, como tarjeta de identificación, mide aproximadamente 85,6 × 54 mm (tamaño ISO/IEC 7810 ID-1; **medida no verificada en esta sesión**).

| Cálculo | Resultado |
|---|---|
| 300 DPI × 85,6 mm ÷ 25,4 mm/pulgada | ≈ 1011 píxeles a lo ancho de la tarjeta |
| 600 DPI × 85,6 mm ÷ 25,4 | ≈ 2022 píxeles |
| Tarjeta ocupando ~70 % del ancho de la foto (propuesta) con 1011 px | foto de ≈ 1444 px de lado largo como mínimo |
| Lado largo de 2048 px con la tarjeta ocupando 70 % | ≈ 1434 px a lo ancho de la tarjeta ≈ 425 DPI efectivos |

Con 2048 px de lado largo se supera el mínimo de 300 DPI de V1 y se queda por debajo de los 600 DPI recomendados por ese proveedor, que sirven para extracción automática; aquí la persona administradora lee la imagen, no un programa.

**Tamaño del archivo (estimación sin medir):** un JPEG de ~3 megapíxeles (2048×1536) con calidad de 0,85 suele quedar del orden de uno a pocos megabytes; el rango real depende del contenido y **debe medirse con fotos reales de tres teléfonos distintos en la entrega E1**. V1 da 2 a 3 MB como óptimo y 5 MB como tope recomendado, compatible con el límite vigente.

## 4. Propuesta del asistente (ninguna decidida)
| N.º | Propuesta | Fundamento |
|---|---|---|
| 19 | **Límite de aplicación sin cambio: 5 MB por archivo** (RF-02), validado en el servidor; la compresión del navegador **no es un control de seguridad** (puede omitirse o fallar) | RF-02; D1 |
| 20 | **Compresión en el navegador:** lado largo máximo de **2048 px**, JPEG con calidad **0,85**, objetivo ≤ 2 MB; si no baja de 5 MB, reducir la calidad en pasos hasta **0,70** y después el lado largo; no bajar de 0,70 | V1, cálculo de la sección 3; los pasos y el objetivo son de diseño |
| 21 | **Pedir `image/jpeg` explícitamente** y comprobar el tipo del resultado: sin eso `toBlob` entrega PNG, mucho más pesado; si el navegador no soporta JPEG, subir el original si pesa ≤ 5 MB y, si no, avisar | M1 |
| 22 | **Nginx:** `client_max_body_size` de **6m** en la ruta de subida de un archivo; si el frente y el reverso van en una sola petición, **11m** (2 × 5 MB más sobrecarga del formulario); 1m (el valor por defecto) en todo lo demás. Evita el 413 sin explicación que el navegador no muestra bien: comprobar el tamaño en el navegador antes de enviar | N1; los márgenes de 1 MB sobre el límite son de diseño |
| 23 | **Django:** dejar `FILE_UPLOAD_MAX_MEMORY_SIZE` en su valor por defecto (los archivos grandes pasan a disco) y mantener la validación de RF-02 | D1 |
| 24 | **Pruebas en teléfonos reales** (al menos un iPhone y dos Android) con fotos de cédula: orientación, lienzo en blanco, tamaño final y legibilidad; mide el tamaño real y confirma o cambia 2048 px y 0,85 | M2, M3, V3 |
| 25 | **Formalizar la compresión** en una versión nueva de la ERS (requisito y criterio de aceptación) y en el DAS (JavaScript mínimo en una interfaz renderizada por el servidor, ADR-022); hoy no existe | Regla 4 de CLAUDE.md |

## 5. Costo y riesgo
- Sin costo de licencia. El riesgo principal es el comportamiento de los navegadores móviles (orientación, límite del canvas en iOS), que solo se confirma probando.
- Comprimir reduce el peso de la foto y el espacio en disco y en los respaldos; no sustituye la minimización de datos de la Ley 8968 (pendiente de abogado, DP-17).

## 6. Decisiones y preguntas
| Pregunta | Respuesta | Decisión |
|---|---|---|
| ¿Se comprime en el navegador con un canvas? | "se hace una compresión de canvas para reducir el tamaño" (22-oct-2026) | Dato del solicitante; sin requisito ni criterio escritos |
| ¿Cifra del límite de subida? | Pendiente | Pendiente; propuestas 19 a 25 |

## 7. Pendientes
- Decidir las propuestas 19 a 25.
- Medir el tamaño real de fotos y de su versión comprimida en la entrega E1.
- Verificar si la re-codificación elimina el EXIF.

## 8. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
