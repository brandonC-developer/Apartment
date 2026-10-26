# Actualización 2026-10-26 (c) — Pillow 13.0.0 por el fallo de pip-audit en la integración continua

**Fecha:** 2026-10-26
**Documentos afectados:** [`src/requirements.txt`](../../../src/requirements.txt), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md) (sin cambio de casillas) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** fallo de «Vulnerabilidades de las dependencias (pip-audit)» en la integración continua (aviso del solicitante, 26-oct-2026); decisión 2 de la E1 (Pillow 12.3.0 y descarte de la 13.0.0 por tener 8 días, actualización [2026-10-24 (q)](../2026-10-24q_decisiones-e1/CAMBIOS.md)); ADR-032 sobre revisión de dependencias
**Estado:** corregido y verificado; no aprobado

## 1. Qué pasó
`pip-audit 2.10.1` reproducido localmente: **37 vulnerabilidades en Pillow 12.3.0, todas con corrección solo en 13.0.0**, publicadas del 19 al 22 de octubre de 2026 (después de fijar la versión). Las que revisé en [OSV](https://osv.dev) (consulta directa a su API; leí el título, no el texto completo de cada una) son de formatos que la aplicación no abre (GIF, BMP, JPEG 2000: el servidor solo abre JPEG y PNG), **salvo una que sí toca nuestra ruta**: «desbordamiento de memoria al escribir el comentario de un JPEG cuando un perfil ICC llena el búfer» (CVE-2026-96778), y el servidor guarda JPEG con el perfil ICC del archivo recibido. No revisé una por una las otras 31 que no listé.

## 2. Decisión del solicitante
Pregunta: «¿Qué hacemos?» · Respuesta: **«Subir a Pillow 13.0.0 (Recomendado)»** · Decisión: fijar `pillow==13.0.0` (publicada el 2026-10-16, 10 días antes) como **excepción a la regla de las dos semanas**, porque corrige vulnerabilidades en una dependencia que procesa archivos no confiables. Alternativas descartadas: ignorar las alertas (deja 37 vulnerabilidades conocidas) y, además, quitar el perfil ICC (cambia una decisión previa; no hace falta con el parche).

## 3. Verificación
- `pip-audit` con `requirements.txt`: **«No known vulnerabilities found»**.
- **406 pruebas pasan en Windows** (Python 3.12, Pillow 13.0.0) y **395 en WSL** (Python 3.14.4, Pillow 13.0.0, comprobado dentro del despliegue); `verificar.sh` sin fallos y Gunicorn con exposición 1,5 OK.
- Las cuatro muestras públicas de teléfono dan el mismo resultado que con 12.3.0 (0,81, 1,28, 0,36 y 0,71 MiB) y el MPO de iPhone se acepta.
- El 12.3.0 de las pruebas anteriores en WSL: el despliegue **no se reinstalaba** porque `dpkg` había quedado interrumpido (`E: dpkg was interrupted`) y mis comandos silenciaban la salida. Ejecuté `dpkg --configure -a` en la distribución Ubuntu (reparación estándar, sin quitar paquetes) y desplegué de nuevo. **Lección:** no silenciar la salida del despliegue; desde ahora compruebo la versión instalada en WSL.

## 4. Qué queda
La integración continua debe volver a verde: **lo confirma el solicitante tras el push**. La decisión 2 de la E1 queda corregida: Pillow **13.0.0**, no 12.3.0.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
