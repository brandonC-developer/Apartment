# Actualización 2026-10-26 (b) — E1, grupo G: muestras públicas de teléfonos y un defecto real con los JPEG «MPO»

**Fecha:** 2026-10-26
**Documentos afectados:** código en [`src/inquilinos/imagenes.py`](../../../src/inquilinos/imagenes.py) y [`tests_imagenes.py`](../../../src/inquilinos/tests_imagenes.py), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS RF-02, RF-50; CA-73, CA-74, CA-82, CA-83; pregunta del solicitante: «no tengo iPhone y solo un teléfono; ¿no existe documentación o imágenes para descargar para hacer estas pruebas, según buenas prácticas?» (26-oct-2026); actualización [2026-10-26 (a)](../2026-10-26a_e1-grupo-g-medicion-de-fotografias/CAMBIOS.md)
**Estado:** defecto corregido y probado; la medición con muestras públicas está hecha; **CA-73 y CA-82 no se marcan** hasta que el solicitante decida el punto 5; no aprobado

## 1. ¿Existen fotos de teléfonos para probar? Sí; fuentes y cómo se validaron
| Fuente | Cómo se validó | Qué hay | Limitaciones |
|---|---|---|---|
| [Wikimedia Commons, categorías «Taken with iPhone 14 Pro», «Taken with Samsung Galaxy S23», «Taken with Google Pixel 8»](https://commons.wikimedia.org/wiki/Category:Taken_with_iPhone) | **Consultada por su API y descargados los archivos**; el modelo, el GPS, el XMP y los píxeles se comprobaron abriendo cada archivo; la licencia y el autor son los de los metadatos de Commons | Fotos originales de miles de usuarios, cada una con su licencia | Un usuario pudo editar el archivo antes de subirlo; no son mis fotos ni las del solicitante; no leí cada página de descripción completa |
| [ianare/exif-samples](https://github.com/ianare/exif-samples) | Solo resultados de búsqueda (no se abrió el repositorio) | Muestras de EXIF, **archivado**, en su mayoría cámaras antiguas, no iPhone ni Android | Sin licencia clara en el repositorio; cada imagen remite a Commons |
| [HEIC Digital, muestras](https://heic.digital/samples/) | Solo resultados de búsqueda | HEIC de un iPhone 12 Pro y un Galaxy A32 | Sin licencia específica; no se descargó |
| [Nokia HEIF](https://github.com/nokiatech/heif/wiki) | Solo resultados de búsqueda | Archivos de conformidad HEIF | Con derechos de autor de Nokia; no son fotos de teléfono |

No encontré documentación oficial que diga «así se prueba una subida con fotos de teléfono»: la práctica de los proyectos open source que revisé (Compressor.js) es probar con originales reales de varios modelos; aquí se hizo con muestras públicas.

## 2. Las muestras usadas (descargadas fuera del repositorio; no se versionan)
| Archivo de Commons | Autor y licencia | Teléfono (EXIF) | Original | SHA-256 (primeros 16) |
|---|---|---|---|---|
| `106 Fentiman Road.jpg` | Secretlondon, CC BY-SA 4.0 | Apple iPhone 14 Pro, iOS 16.0.2 | MPO 3024x4032, 4,08 MiB | `6dcab408e8cabfa8` |
| `1-157th Mountain Infantry Battalion Repels (7822014).jpg` | U.S. Army 345 MPAD, Sgt. Andrew Valles, dominio público | Apple iPhone 14 Pro, iOS 16.4.1 | MPO 4032x3024, 5,36 MiB, con GPS | `efeaceb40a15028f` |
| `20241207 123129 Little Free Library 96 Atlas Ave.jpg` | ArthurGron, CC0 | Samsung Galaxy S23 | JPEG 4000x3000, 7,83 MiB, con GPS | `bd78857ebc30a99d` |
| `Abandoned Jones New York Country store at the Circle Factory Outlet Center.jpg` | ForeverFlying, CC BY 4.0 | Google Pixel 8 (HDR+) | JPEG 8160x6144 (50 MP), 12,75 MiB, con GPS y XMP | `b85af3bb70b14fde` |

## 3. Medición con el script del navegador (Chrome 155, `medir_reduccion.py`)
| Muestra | Enviado | Peso | Del original | Metadatos enviados |
|---|---|---|---|---|
| iPhone 14 Pro (Fentiman) | JPEG 1536x2048, calidad 0,85 | **0,81 MiB** | 20 % | sin GPS ni EXIF; perfil ICC sí |
| iPhone 14 Pro (Ejército) | JPEG 2048x1536, calidad 0,85 | **1,28 MiB** | 24 % | sin GPS ni EXIF |
| Galaxy S23 | JPEG 2048x1536, calidad 0,85 | **0,36 MiB** | 5 % | sin GPS ni EXIF |
| Pixel 8 (50 MP) | JPEG 2048x1542, calidad 0,85 | **0,71 MiB** | 6 % | sin GPS ni EXIF |

Las cuatro quedan **por debajo de 2 MB** (objetivo de RF-50) y de 5 MiB, sin bajar de la calidad 0,85. El servidor aceptó los cuatro resultados. Una cédula con texto fino pesará distinto que estas escenas: sigue haciendo falta **una foto de un documento** de verdad.

## 4. Defecto encontrado y corregido
1. **Un JPEG de iPhone, Pixel o Samsung recientes provocaba un error 500, no un rechazo limpio.** Pillow los identifica como «MPO» (un JPEG con varias imágenes: miniatura, mapa de profundidad o de ganancia HDR) y `procesar_imagen` tenía solo `JPEG` y `PNG` en su tabla: `KeyError: 'MPO'`. **Mis pruebas sintéticas nunca generaron un MPO; las fotos reales lo mostraron en el primer intento.** Es el caso normal de una foto de iPhone 14 Pro que ya pesa menos de 5 MiB y llega sin pasar por la reducción (por ejemplo, si el navegador no puede reducir).
2. **Segundo defecto escondido tras el primero:** Pillow no admite `quality="keep"` con un MPO (`ValueError`). Ahora el MPO se vuelve a codificar a calidad 90 (propuesta mía).
3. **Qué hace ahora:** se acepta como JPEG, se guarda **solo la primera imagen** con la orientación aplicada y sin metadatos ni el bloque de varias imágenes (se prueba que `MPF` y la marca del teléfono no quedan). Un MPO truncado se rechaza como cualquier JPEG.
4. **Pruebas:** 2 nuevas; sin la línea `'MPO': 'image/jpeg'` la nueva falla (mutación detectada). **406 pruebas pasan en Windows y 395 en WSL** (Python 3.14.4); `verificar.sh` sin fallos. *Corrección posterior:* esa corrida de WSL se hizo con Pillow 12.3.0 porque `dpkg` estaba interrumpido y el despliegue no reinstaló nada sin avisar; se repitió con Pillow 13.0.0 (actualización [2026-10-26 (c)](../2026-10-26c_pillow-13-pip-audit/CAMBIOS.md)).

## 5. Decisión que es tuya (pendiente)
El criterio de salida de la E1 dice «un iPhone y dos Android». Tú tienes un solo teléfono. **Propuesta (recomendada):** aceptar como evidencia (a) las 4 muestras públicas (2 iPhone 14 Pro, 1 Galaxy S23, 1 Pixel 8) **más** (b) una foto de **un documento** tomada con tu teléfono, sin enviarla por WhatsApp. Es menos que el criterio original pero cubre los tres fabricantes, el formato MPO y un archivo de 50 MP. **Riesgo:** una foto de un tercero puede haber sido editada y no cubre el selector de archivos del iPhone (HEIC a JPEG), que queda sin verificar y se anota como riesgo conocido. Hasta tu respuesta, **CA-73 y CA-82 no se marcan**.

## 6. Qué no está hecho
La decisión del punto 5, la foto de tu teléfono, la comprobación manual del navegador sin lienzo, el cierre de la E1 con sus nueve condiciones y la revisión de GitHub Actions.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
