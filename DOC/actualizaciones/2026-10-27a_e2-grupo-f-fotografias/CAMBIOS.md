# Actualización 2026-10-27 (a) — E2, grupo F: fotografías del contrato y cédula desde el perfil

**Fecha:** 2026-10-27
**Documentos afectados:** código en [`src/alquileres/fotografias.py`](../../../src/alquileres/fotografias.py), [`views.py`](../../../src/alquileres/views.py), [`urls.py`](../../../src/alquileres/urls.py), sus plantillas, `inquilinos/almacenamiento.py`, el script de reducción y la configuración de Nginx; [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS RF-51, RF-52, RF-02, RF-45, RF-50; CA-75, CA-76, CA-77, CA-82; DP-28 y DP-29 (abiertas); modelo de datos v0.7 (R22, R23, R28); instrucción del solicitante: «escribe grupo F»
**Estado:** implementado y probado; no aprobado

## 1. Qué se escribió
| Pieza | Qué hace |
|---|---|
| `fotografias.subir_fotografia_del_contrato` | **RF-52, CA-76:** hasta 10 fotografías por contrato, numeradas de 1 a 10, un archivo por petición; la número 11 se rechaza con un mensaje que dice el máximo y se conservan las 10. Bloquea la fila del contrato (dos subidas simultáneas no pasan de 10) y la base lo vuelve a comprobar. El servidor valida el tipo real, el peso y reescribe el archivo sin metadatos; si la base falla, el archivo se borra. No crea ni modifica la cédula, ni al revés |
| Almacenamiento | Subcarpeta privada `contratos`, separada de `cedulas`, con nombre aleatorio; solo se admiten esas dos subcarpetas |
| Entrega | **CA-77:** solo con sesión, sin URL pública; cada consulta o descarga queda en `AccesoDocumentoContrato` (actor, fecha y hora, acción) sin la imagen; si el registro falla no se entrega |
| `fotografias.subir_cedula_desde_la_propiedad` | **RF-51, CA-75:** agrega o reemplaza una cara de la cédula del inquilino del contrato vigente; queda en la ficha del inquilino con las reglas de siempre (consentimiento, validación, auditoría) y no en la propiedad. Sin contrato vigente: «No hay contrato vigente.» |
| `selectors.cedula_en_el_perfil` | Por cara, «Agregar» o «Reemplazar» según haya una fotografía activa; sin contrato vigente la acción va desactivada con el aviso |
| Reducción en el navegador | El formulario del contrato declara `data-lado-maximo="3508"` y el script parte de ese lado; la cédula sigue en 2048 px. Un valor ausente o fuera de rango se ignora |
| Nginx | Los 6 MiB de cuerpo solo en las tres rutas de subida (ficha, contrato y cédula desde la propiedad) |
| Páginas mínimas | `contratos/<id>/fotografias/` y `propiedades/<id>/cedula/`, funcionales y sin estilos; el perfil completo es del grupo G |

## 2. Propuestas del asistente (sin aprobar)
1. **Una fotografía de contrato no exige consentimiento del inquilino**: RF-52 no lo pide y es un documento del contrato, no de la persona. Dime si el abogado opina otra cosa (DP-17).
2. **Se aceptan fotografías en contratos finalizados**, no en anulados.
3. **«Contrato vigente» incluye el contrato por decidir** (la fecha de fin pasó sin cierre), igual que en el perfil de la propiedad del grupo C.
4. **No se pueden borrar fotografías del contrato**: la conservación depende de DP-28, todavía abierta; la tabla no tiene marca de eliminación.
5. **Auditoría de la subida:** registra el orden y no la imagen ni su nombre.

## 3. Lo que no se hizo
- **Medición con fotos reales de teléfono** y las cifras definitivas de reducción (DP-29, CA-82): grupo H. Hoy el contrato parte de 3508 px y calidad 0,85; el peso objetivo y los pasos de calidad siguen siendo los de la cédula hasta medir.
- Pantallas del perfil de la propiedad con estas secciones integradas (grupo G).

## 4. Verificación
- **731 pruebas encontradas: en Windows (Python 3.12) pasan, con 14 omitidas; en WSL (Python 3.14.4) corren 717 sin fallos.** `verificar.sh` sin fallos, con la comprobación nueva de que `/static/contratos/` no sirve archivos.
- **Navegador real (Selenium):** una foto de 4032×3024 enviada desde el formulario del contrato llega de 3508×2631; la cédula desde el perfil llega de 2048×1536; una imagen menor no se amplía. Estas pruebas no corren en WSL (sin navegador).
- **Mutaciones, 18 probadas y 17 detectadas:** límite de 10, numeración, subcarpeta, bloqueo de la fila, contrato vigente exigido, borrado del archivo huérfano, acción «Reemplazar», acción desactivada, aviso, un solo archivo, registro del acceso, descarga como adjunto, lado de partida, sesión obligatoria, script, ruta de Nginx y subcarpetas admitidas (esta sobrevivió y se cubrió con dos pruebas). **Una sobrevive y es equivalente:** la comprobación de peso de la vista, porque el servicio rechaza lo mismo con el mismo mensaje; queda como defensa previa a leer el archivo.

## 5. Qué no está hecho
Pantallas (G) y medición y cierre (H). 0 de 25 CA de la E2 marcados.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
