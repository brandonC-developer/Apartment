# Actualización 2026-10-22 (f) — ERS v1.10: reducción de la fotografía en el navegador

**Fecha:** 2026-10-22
**Documentos afectados:** [ERS v1.10](../../fase-1-ers/ERS_SGA_001_v1.10_borrador.md) (nueva; reemplaza a la [v1.9](../../fase-1-ers/ERS_SGA_001_v1.9_borrador.md), que no se edita), [README de la fase 1](../../fase-1-ers/README.md) y [DOC/README.md](../../README.md)
**Origen:** [2026-10-22 (d)](../2026-10-22d_limite-subida-foto-cedula/CAMBIOS.md) y [2026-10-22 (e)](../2026-10-22e_decision-limite-subida/CAMBIOS.md)
**Estado:** borrador; no aprobado

## 1. Motivo
El solicitante decidió reducir la fotografía del documento en el navegador con un canvas y enviar el frente y el reverso por separado, y pidió redactar la ERS v1.10 (22-oct-2026).

## 2. Cambios
| Dónde | Cambio |
|---|---|
| Control del documento | Versión 1.10, fecha 22-oct-2026, nota de control y fila de historial |
| RF-02 | Nota: un archivo por petición; el servidor aplica siempre 5 MB y el tipo real. La regla no cambia |
| **RF-50 (nuevo)** | Reducir la fotografía en el navegador: lado mayor de 2048 px sin ampliar, JPEG con calidad 0,85, objetivo de 2 MB, calidad mínima de 0,70, tope de 5 MB, orientación conservada; si no se puede reducir, original solo si es JPEG o PNG de hasta 5 MB. No es un control de seguridad |
| **CA-73 (nuevo)** | Reducción de 4032 × 3024 px y 6 MB a 2048 × 1536 px y no más de 5 MB; el peso real con tres teléfonos se registra en E1, sin rechazar por superar 2 MB |
| **CA-74 (nuevo)** | Envío sin reducción, rechazo en el servidor de lo que pase de 5 MB o no sea JPEG o PNG, y un archivo por petición |
| Sección 2.3 | La carga de la fotografía menciona RF-50 y un archivo por petición |
| Sección 2.5 | Nuevo supuesto S-03 (navegador con JavaScript, canvas y JPEG) |
| Sección 11 | El riesgo del servidor propio recoge que el endurecimiento se investigó |
| Sección 12 | Nueva DP-27 (metadatos de la imagen); nueva sección 12.1c con la decisión; nueva casilla en la lista de aprobación |
| Matriz (sección 10) | Fila "Registrar inquilinos y cédulas": RF-50, CA-73 y CA-74 |
| Totales | 50 RF y 74 CA (antes 49 y 72). RN, RNF, OL, ADR y RE no cambian; DP pasa de 26 a 27 |

## 3. Trazabilidad
| Pregunta | Respuesta | Decisión | Dónde |
|---|---|---|---|
| ¿Se adopta la cifra propuesta? | "Sí, adoptarla" (22-oct-2026) | 2048 px, calidad 0,85, objetivo de 2 MB, tope de 5 MB | RF-50, CA-73 |
| ¿Frente y reverso en una o dos peticiones? | "Por separado" | Un archivo por petición | RF-02, CA-74 |
| ¿Se comprime en el navegador con un canvas? | "se hace una compresión de canvas" | Reducción en el navegador | RF-50 |

## 4. Lo que propone el asistente y el solicitante no decidió
- Los **pasos intermedios** de calidad entre 0,85 y 0,70 y la regla de **reducir el lado mayor** si, con 0,70, el archivo aún pasa de 5 MB (el solicitante adoptó las cifras, no esa redacción).
- Escribir **RF-50 en términos verificables** y los ejemplos numéricos de CA-73 (4032 × 3024 px y 6 MB son un ejemplo del asistente, no una medición).
- **DP-27** y **S-03**.
- No se asignó prioridad al RF-50 porque los requisitos de la ERS no la muestran por requisito en el texto.

## 5. Lo que no se verificó
Los tamaños resultantes de la reducción (no hay mediciones); que re-codificar con canvas elimine los metadatos; el límite del canvas en iOS; el soporte de JPEG en los navegadores objetivo. Las fuentes y sus limitaciones están en la [actualización (d)](../2026-10-22d_limite-subida-foto-cedula/CAMBIOS.md).

## 6. Documentos que quedan desalineados (no se tocaron en esta actualización)
El script de coherencia lo señala (11 problemas, todos de este tipo):
- **DAS v0.11, modelo de datos v0.4, diseño técnico v0.7, estrategia de pruebas v0.3, plan de implementación v0.1 y lista de verificación v0.1:** declaran la ERS v1.9 como base.
- **Estrategia de pruebas:** CA-73 y CA-74 sin asignar.
- **Plan de implementación:** RF-50, CA-73 y CA-74 sin entrega (la lógica es de la entrega E1, Inquilinos).
- **DAS:** falta el JavaScript mínimo en una interfaz renderizada por el servidor (ADR-022) y el límite de 6m de Nginx (propuesta 22 de la actualización (d)).
- **Diseño técnico:** falta la subida del frente y del reverso por separado.
- **DOC/README.md:** la tabla de fases se actualiza con esta actualización.
- **Resuelto en la [actualización 2026-10-22 (g)](../2026-10-22g_alineacion-ERS-v1.10/CAMBIOS.md).**

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
