# Actualización 2026-10-23 (c) — Unidad del tope de subida de 5 MB

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorpora en la ERS v1.12 (pendiente de redactar). [DOC/README.md](../../README.md)
**Origen:** pendiente de la [actualización 2026-10-22 (m)](../2026-10-22m_prueba-modelo-v0.5/CAMBIOS.md) ("no está fijada la unidad") y RF-02 de la ERS v1.11
**Estado:** decisión registrada; documentos sin cambiar; no aprobado

## 1. Pregunta, respuesta y decisión
| Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|
| ¿Qué unidad fijamos para el tope de subida del servidor? | "5 MiB = 5 242 880 bytes" (recomendada por el asistente) | El tope del servidor es **5 242 880 bytes (5 MiB)**; la ERS lo escribirá con la cifra en bytes |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| NIST, prefijos binarios: https://physics.nist.gov/cuu/Units/binary.html | Organismo de metrología | Leída por resumen (WebFetch, 23-oct-2026) | 1 MB = 1 000 000 B; 1 MiB = 1 048 576 B | Resumen, no lectura completa |
| nginx, sintaxis del archivo de configuración: https://nginx.org/en/docs/syntax.html | Documentación oficial | Leída por resumen (WebFetch, 23-oct-2026) | Los tamaños admiten los sufijos `k` y `m` | **No dice cuántos bytes son**; que 1m = 1 048 576 no se verificó. Por eso la ERS fija la cifra en bytes |

## 3. Lo que propone el asistente y el solicitante no decidió
- Que Nginx quede en `6m` (propuesta de la actualización 2026-10-22 (d)): con cualquier lectura del sufijo queda por encima de 5 242 880 bytes; no se midió la sobrecarga del formulario.
- El argumento de que el explorador de Windows muestra tamaños en base 1024 es criterio del asistente, no una fuente leída.

## 4. Qué no se hizo
- **No se editó la ERS v1.11.** RF-02, CA-74, CA-76, S-03 y otros dicen "5 MB"; deben pasar a "5 MiB (5 242 880 bytes)" en la ERS v1.12, junto con lo demás que se decida. Hasta entonces la ERS vigente es ambigua en este punto.
- No se midió el comportamiento real de Nginx ni de Django con un archivo en el límite; se hace en E1.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
