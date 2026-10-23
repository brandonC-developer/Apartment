# Actualización 2026-10-22 (e) — Decisión: límite de subida de la foto de la cédula

**Fecha:** 2026-10-22
**Documentos afectados:** [README de la fase 6](../../fase-6-despliegue-operacion/README.md) y [DOC/README.md](../../README.md). No se edita ningún documento versionado.
**Origen:** [2026-10-22 (d)](../2026-10-22d_limite-subida-foto-cedula/CAMBIOS.md), propuestas 19 a 25
**Estado:** registro de decisiones del solicitante; no es aprobación de ningún documento.

## 1. Decisiones del solicitante (22-oct-2026)
| Pregunta | Respuesta | Decisión | Quién |
|---|---|---|---|
| ¿Se adopta la cifra propuesta? (servidor 5 MB por archivo; navegador con lado largo de 2048 px, JPEG con calidad 0,85, objetivo ≤ 2 MB y sin bajar de 0,70; Nginx 6m en la ruta de subida) | "Sí, adoptarla" | **Adoptada** como valores de diseño. Propuestas 19 a 23 de la actualización (d) pasan a decisión del solicitante | Solicitante |
| ¿Frente y reverso se suben en una sola petición o por separado? | "Por separado" | **Por separado:** una petición por archivo; `client_max_body_size` de **6m** en esa ruta (no 11m) y 1m en el resto | Solicitante |

## 2. Consecuencias (derivadas por el asistente)
- **Siguen siendo propuestas, no decididas:** la 24 (pruebas en teléfonos reales) y la 25 (formalizar la compresión en la ERS y el DAS). La compresión en el navegador **sigue sin estar en la ERS v1.9 ni en el DAS v0.11**: hasta una versión nueva, la única regla vigente de los documentos es RF-02 (JPEG y PNG, hasta 5 MB).
- Por la decisión de subir cada archivo por separado, el diseño técnico debe reflejar dos operaciones de subida (frente obligatorio, reverso opcional); esto no está aún en el diseño técnico v0.7.
- Los valores 2048 px y 0,85 son **de diseño, sin medir**: se confirman con fotos reales en la entrega E1 (propuesta 24) y pueden cambiar.
- Falta verificar si re-codificar con canvas elimina los metadatos EXIF.

## 3. Pendientes
- Redactar en una versión nueva de la ERS el requisito y el criterio de aceptación de la compresión, y en el DAS el JavaScript mínimo (ADR-022).
- Pruebas en un iPhone y dos Android.
- Reflejar la subida por separado en una versión nueva del diseño técnico.

## 4. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
