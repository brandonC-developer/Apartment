# Actualización 2026-10-24 (v) — E1, grupo E: reducción de la fotografía en el navegador

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/inquilinos/`](../../../src/inquilinos/static/inquilinos/reducir_fotografia.js), [`src/despliegue/`](../../../src/despliegue/desplegar.sh), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS RF-50, RF-02; CA-73, CA-74, CA-83; decisión 4 de la E1 (estáticos, actualización [2026-10-24 (q)](../2026-10-24q_decisiones-e1/CAMBIOS.md)); instrucción del solicitante: «sí, escribe el grupo E» (24-oct-2026)
**Estado:** implementado y probado; no aprobado

## 1. Qué se escribió
| Pieza | Qué hace |
|---|---|
| `static/inquilinos/reducir_fotografia.js` | Sin bibliotecas ni código en línea. Lado mayor de 2048 px sin ampliar; JPEG a 0,85 y, si pasa de 2 MB, 0,80, 0,75 y 0,70; si aun así pasa de 5 MiB reduce el lado; conserva la orientación; fondo blanco para PNG con transparencia; si no puede reducir, envía el original solo si es JPEG o PNG de hasta 5 MiB y si no avisa antes de enviar; un archivo por petición con el token CSRF |
| `templates/inquilinos/fotografias.html` y ruta `GET /inquilinos/<id>/fotografias/` | Página mínima, con sesión, con un formulario por cara que usa el script (la pantalla completa es el grupo F) |
| `STATIC_ROOT` (`SGA_ESTATICOS`, por defecto `/opt/sga/static`) | Carpeta de `collectstatic`, fuera del código y de los documentos |
| Nginx `location /static/` | `alias /opt/sga/static/`, sin lista de archivos, `nosniff`, caché de 1 hora; es el único `alias` permitido (lo exige una prueba) |
| `desplegar.sh` / `verificar.sh` | Ejecuta `collectstatic` como root; verifica en WSL el tipo, las cabeceras, que la aplicación no escribe en la carpeta, seis intentos de salir de `/static/` y que los documentos no salen por ahí |
| `requirements-pruebas.txt` | `selenium==4.50.0`, solo para pruebas; la integración continua lo instala |
| `tests_navegador.py` | 11 pruebas con un navegador real (Chrome, Edge o Firefox; `SGA_NAVEGADOR` lo fuerza); se omiten donde no hay |

## 2. Resultados medidos (CA-73)
Foto sintética de 4032x3024 con ruido: **6,44 MiB → 1,47 MiB**, 2048x1536, calidad 0,85, JPEG. Una imagen de 1200x800 no se amplía. La orientación EXIF 6 se conserva. Una imagen enorme termina siempre en 5 MiB o menos. **Son imágenes sintéticas: el peso con fotos reales sigue pendiente (grupo G).**

## 3. Hallazgos
1. **La prueba de las plantillas prohibía todo `<script>`.** Se cambió para admitir un `<script src>` propio y seguir rechazando código en línea, estilos y manejadores.
2. **La prueba del `alias` de Nginx debía cambiar:** de «ninguno» a «solo `/opt/sga/static/`». Una barra mal emparejada abre `..` (la mutación se detecta).
3. **Django normaliza `STATIC_URL`** a `/static/`; la prueba lo refleja.
4. **En WSL no hay navegador:** allí las 11 pruebas se omiten y se ejecutan en Windows y, si el ejecutor trae Chrome, en la integración continua (**no lo he verificado**; la ejecución de GitHub hay que revisarla).

## 4. Propuestas del asistente (sin aprobar)
- Calidades intermedias 0,80 y 0,75 y lado mínimo de 600 px al reducir (RF-50 solo fija 0,85 y 0,70).
- Fondo blanco para PNG con transparencia.
- Respuesta de la subida en JSON y estados en `data-estado` para poder probar.

## 5. Verificación
- **368 pruebas pasan en Windows** (Python 3.12), incluidas las 11 del navegador en Chrome y en Edge. **En WSL (Python 3.14.4) se ejecutan 357** y las 11 del navegador se omiten.
- **Mutaciones, todas detectadas (7):** ampliar imágenes pequeñas, ignorar la orientación, quitar el fondo blanco, enviar el original de más de 5 MiB, calidad inicial 0,95, `alias` sin la barra final y `innerHTML` en el script.
- **Despliegue real en WSL:** `desplegar.sh`, `verificar.sh` («sin fallos», con la sección nueva de estáticos) y `probar.sh`.

## 6. Qué no está hecho
Las pantallas (grupo F), la medición con fotos reales y la comprobación manual del navegador sin lienzo (grupo G), y confirmar en GitHub que el ejecutor corre las pruebas del navegador. **0 de 8 CA de la E1 marcados.**

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
