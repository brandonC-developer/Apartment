# Actualización 2026-10-24 (u) — E1, grupo D: fotografías del documento en el servidor

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/inquilinos/`](../../../src/inquilinos/imagenes.py), [`src/despliegue/`](../../../src/despliegue/desplegar.sh), [`src/requirements.txt`](../../../src/requirements.txt), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS RF-01, RF-02, RF-03, RF-39, RF-45; CA-11, CA-26, CA-74, CA-83; ADR-003; BR-05 y BR-06; decisión 2 de la E1 (actualización [2026-10-24 (q)](../2026-10-24q_decisiones-e1/CAMBIOS.md)); instrucción del solicitante: «sí, escribe el grupo D» (24-oct-2026)
**Estado:** implementado y probado en Windows y en el despliegue real de WSL; no aprobado

## 1. Qué se escribió
| Pieza | Qué hace |
|---|---|
| `requirements.txt` | `pillow==12.3.0` (publicada el 2026-07-01; la 13.0.0 tenía 8 días) |
| `imagenes.procesar_imagen` | Valida y **vuelve a escribir** cada imagen: tipo real por el contenido, 5 242 880 bytes, tope de 60 millones de píxeles **antes** de decodificar, decodificación completa, orientación aplicada y archivo nuevo sin metadatos (se conserva el perfil de color) |
| `almacenamiento` | Archivos en `RAIZ_DOCUMENTOS/cedulas` con nombre UUID, `O_EXCL`, 0640; solo acepta referencias con la forma que genera él mismo |
| `services.subir_fotografia` | Un archivo por llamada, con el consentimiento vigente (RF-39); guarda, marca la anterior como eliminada, audita (`fotografia_subida` o `fotografia_reemplazada`) y, si algo falla, borra el archivo nuevo |
| `services.registrar_acceso` y `views` | Entrega la imagen solo con sesión; registra quién, cuándo y qué acción, sin la imagen; si el registro falla, no entrega |
| Rutas | `POST /inquilinos/<id>/fotografias/<cara>/` (JSON), `GET /inquilinos/documentos/<id>/ver/` y `.../descargar/` |
| Nginx | `client_max_body_size` de 6 MiB solo en la ruta de subida y 1 MiB en el resto |
| Despliegue | La carpeta de documentos con el bit setgid (2750) y la verificación real con una subida por HTTPS |

## 2. Hallazgos (cosas que no eran como supuse)
1. **`quality="keep"` de Pillow no es una transcodificación sin pérdida.** Reutiliza las tablas de calidad, pero vuelve a codificar desde los píxeles: en una imagen sintética muy ruidosa la diferencia media fue de unos 2 a 3 niveles de 255 y el peso casi no cambió. No lo describí así al decidirlo. Se corrigió el comentario y la prueba; **la pérdida con fotos reales se medirá en el grupo G**.
2. **El perfil ICC se conserva** (no es un dato personal y mantiene los colores de las fotos de un iPhone). Es propuesta mía; si prefieres quitarlo también, es un cambio de una línea.
3. **Pillow copia el comentario del JPEG desde `info`**: hubo que vaciar `info` para que no pasara. Está probado.
4. **Una de mis pruebas dependía de la versión de zlib** (pasaba en Windows y fallaba en Linux): ahora simula la reescritura.
5. **Escribir scripts de shell desde Python en Windows los deja con fin de línea CRLF** y no corren en Linux. Pasó con `verificar.sh` y se detectó al ejecutarlo en WSL. El `.gitattributes` evita que llegue al repositorio, pero la copia de trabajo hay que mantenerla en LF: se convirtieron los archivos afectados y desde ahora esos archivos se escriben con `newline='\n'`.

## 3. Propuestas del asistente (sin aprobar)
- **Reemplazar una fotografía borra su archivo del disco** al confirmar la transacción (la fila queda con `eliminado_en`). La ERS dice «se marca como eliminada»; borrar el archivo sigue el principio de no guardar lo que ya no se necesita. Un respaldo anterior sí la conservará hasta que venza su retención.
- Nombre del archivo entregado: `documento-<id>.jpg`, sin datos personales.
- Entregar la cédula con `Cache-Control: private, no-store`.
- Responder la subida con JSON (la usará el script del navegador del grupo E); las pantallas del grupo F lo mostrarán.
- El tope de 60 millones de píxeles (decisión 2 de la E1).

## 4. Verificación
- **347 pruebas pasan** (50 nuevas) en Windows con Python 3.12 y **en WSL con Python 3.14.4, sin ninguna omitida**. Las de la imagen cubren: JPEG y PNG válidos, tipos falsos (GIF, BMP, TIFF, PDF, HTML, ejecutable), vacío y demasiado grande, **archivos truncados o dañados (CA-83)**, una bomba de descompresión de 200 millones de píxeles, **metadatos (ubicación GPS, cámara, comentario, XMP y bloques de texto de PNG) ausentes del archivo guardado**, datos añadidos al final del archivo (`<?php ...`), orientación, perfil de color y los modos de color habituales. Las del almacenamiento: nombres aleatorios y referencias con `..`, barras, mayúsculas o extensiones raras. Las de los servicios y las vistas: consentimiento, un archivo rechazado que no descarta el otro (**CA-74, CA-83**), reemplazo, fallos de base o de disco sin huérfanos, token CSRF, sesión, una sola petición por archivo, **entrega sin sesión negada (CA-11)**, ninguna URL pública, **cada consulta registrada (CA-26)**, cabeceras y que sin el registro no se entrega.
- **Mutaciones manuales, todas detectadas:** quitar la sesión de la vista, no registrar el acceso, no exigir el consentimiento, guardar el original, no borrar el huérfano, aceptar cualquier referencia, quitar el tope de píxeles y de peso, y dejar el comentario del JPEG. (La de la referencia no se aplicó a la primera; se repitió bien.)
- **Recorrido real en WSL por HTTPS** (`verificar.sh`): subida de una cédula con ubicación GPS → 201; el archivo guardado no tiene los metadatos, es 0640 de `sga_app` con el grupo del respaldo (setgid); con sesión se entrega la imagen guardada con `no-store`; **sin sesión, 302**; dos consultas dejan dos accesos; **Nginx admite un cuerpo de más de 1 MiB en la ruta de subida (201) y rechaza más de 6 MiB (413) y más de 1 MiB en las demás rutas (413)**. El servicio de Gunicorn endurecido (1.5 OK) funciona con Pillow. Los datos y archivos de prueba se borran al terminar.

## 5. Qué no está hecho
El script de reducción del navegador (grupo E), las pantallas (F) y la medición con fotos reales (G): el peso tras la reducción, la pérdida de calidad y los metadatos que dejan los teléfonos (CA-73, CA-82). **0 de 8 CA de la E1.**

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
