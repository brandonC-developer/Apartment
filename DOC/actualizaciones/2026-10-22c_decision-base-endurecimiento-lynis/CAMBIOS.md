# Actualización 2026-10-22 (c) — Decisión: base del endurecimiento sin el PDF de CIS y uso de Lynis

**Fecha:** 2026-10-22
**Documentos afectados:** [README de la fase 6](../../fase-6-despliegue-operacion/README.md) y [DOC/README.md](../../README.md). No se edita ningún documento versionado.
**Origen:** [2026-10-22 (b), sección 5 y 6](../2026-10-22b_endurecimiento-nginx-gunicorn-postgresql/CAMBIOS.md)
**Estado:** registro de decisiones del solicitante; no es aprobación de ningún documento.

## 1. Motivo
Tras la investigación de endurecimiento, el solicitante respondió las dos primeras preguntas abiertas.

## 2. Decisiones del solicitante (22-oct-2026)
| Pregunta | Respuesta | Decisión | Quién |
|---|---|---|---|
| ¿Se usa el PDF de CIS como base del endurecimiento? | "opción B" | **Opción B:** no depender del PDF de CIS. La base es la documentación oficial ya leída (Ubuntu, Nginx, Gunicorn, PostgreSQL, Django, systemd), OWASP y NIST SP 800-123 | Solicitante |
| ¿Se acepta Lynis como herramienta de auditoría? | "acepto Lynis" | **Lynis** (GPL) se usará para auditar el servidor y dejar un informe como evidencia | Solicitante |

## 3. Consecuencias (derivadas por el asistente)
- **No se afirmará conformidad con CIS** en ningún documento mientras no se lean sus controles; las propuestas 1 y 2 de la actualización 2026-10-22 quedan sustituidas por esta decisión.
- Las propuestas 3 a 9 y 11 a 18 de las dos actualizaciones anteriores **siguen siendo propuestas del asistente**: el solicitante no las ha decidido.
- La licencia de uso comercial del PDF de CIS deja de ser un bloqueo; no se resolvió y no se reabre salvo que el solicitante lo pida.
- **Lynis no está validado en Ubuntu 26.04** (fuente L1: página del proveedor, sin instalación). Hay que probarlo en la WSL de la etapa A y registrar la versión, la fecha y el resultado antes de apoyarse en su informe.
- Un informe de Lynis no sustituye la revisión por otra persona (DP-23).

## 4. Pendientes
- **Límite de tamaño de subida** de la foto de la cédula (valor de diseño): sin decidir.
- Probar Lynis y verificar los valores por defecto de Ubuntu 26.04 en la etapa A.
- Decidir cuáles de las propuestas 3 a 9 y 11 a 18 se adoptan, y reflejarlas en una versión nueva del DAS y en el procedimiento de la fase 6.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
