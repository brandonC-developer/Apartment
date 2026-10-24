# Actualización 2026-10-24 (k) — Fin de línea LF para los archivos de configuración

**Fecha:** 2026-10-24
**Documentos afectados:** [`.gitattributes`](../../../.gitattributes) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** observación del asistente al cerrar la [actualización 2026-10-24 (j)](../2026-10-24j_despliegue-etapa-a-wsl/CAMBIOS.md); instrucción del solicitante: «sí, añade el .gitattributes» (24-oct-2026)
**Estado:** aplicado; no aprobado

## 1. Qué cambió
`.gitattributes` fija `eol=lf` también para `*.conf`, `*.service`, `*.socket` y `*.timer`, además de `*.sh` y `*.sql` (ya estaban). El repositorio se trabaja en Windows con conversión automática de fin de línea (`core.autocrlf` en verdadero), así que sin esta regla una copia clonada en Windows podría dejar esos archivos con CRLF. `desplegar.sh` los copia tal cual a Linux, donde un CRLF puede hacer fallar una unidad de systemd o una directiva de Nginx.

## 2. Verificación
- `git ls-files --eol` sobre `src/despliegue/` y `src/respaldo/`: los 16 archivos afectados están en LF en el índice y en la copia de trabajo, con el atributo `eol=lf` aplicado.
- `git add --renormalize .` no modificó ningún otro archivo, es decir, no había archivos con CRLF en el índice.
- Límite: no se clonó el repositorio en un Windows limpio para ver el efecto; la comprobación es sobre el índice y esta copia de trabajo.

## 3. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
