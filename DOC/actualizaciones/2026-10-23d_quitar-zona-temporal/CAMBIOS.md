# Actualización 2026-10-23 (d) — Se quita la zona temporal de archivos (reemplaza a HT-10)

**Fecha:** 2026-10-23
**Documentos afectados:** solo la fila HT-10 y la nota del pendiente 7 del [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md) (remisión a esta decisión) y [DOC/README.md](../../README.md). **La ERS v1.11, el DAS v0.11 y el modelo v0.5 NO se editaron**: siguen describiendo la zona temporal hasta redactar la ERS v1.12 y el modelo v0.6
**Origen:** pregunta del solicitante del 23-oct-2026 ("¿es realmente necesaria una zona temporal?"), a raíz de la pregunta pendiente sobre `sesion_hash`
**Estado:** decisión registrada; documentos pendientes de alinear; no aprobado

## 1. Preguntas, respuestas y decisión
| Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|
| ¿Dónde usamos la zona temporal? (primera pregunta: solo en F-01 / los tres usos / quitarla) | "si la quitamos???" (pidió explicación) | El asistente explicó cómo quedaría sin ella y cambió su recomendación |
| ¿Quitamos la zona temporal y registramos el inquilino antes de subir las fotos? | "Quitarla, sin contrato hasta tener el frente" (recomendada por el asistente) | **Se quita.** El registro es en dos pasos: se guarda el inquilino (datos y consentimiento) y luego se suben el frente y el reverso a su ficha, directo, como en RF-51. El inquilino puede guardarse sin frente, **pero no se le puede asignar un contrato hasta subirlo** |

## 2. Qué deja de existir y qué queda
- **Se retira:** la entidad `ARCHIVO_TEMPORAL`, el identificador de un solo uso, R24, H16, el proceso de limpieza de 24 h, y la pregunta de `sesion_hash` y de si la zona temporal entra en los respaldos. HT-10 queda **reemplazada** por esta decisión.
- **Queda:** R22 (orden único de las fotos del contrato) con el bloqueo del contrato (H18, adoptado en la [actualización (b)](../2026-10-23b_h18-bloqueo-contrato/CAMBIOS.md)), R23, R25 y `DOCUMENTO_CONTRATO`.
- **Mejora:** el consentimiento (RF-39) se registra siempre antes de cualquier fotografía.

## 3. Lo que propone el asistente y el solicitante no decidió
- La regla "no se asigna contrato hasta tener el frente" es propuesta del asistente, aceptada por el solicitante; **sin fuente**, es criterio de diseño. Falta decidir: si hay lista de "inquilinos sin frente", cuánto tiempo puede estar así y qué se hace con los abandonados.
- Cómo se evita un archivo huérfano si falla el guardado (propuesta: escribir el archivo, insertar la fila y, si falla, borrar el archivo en la misma petición).
- Fuente consultada: OWASP, Guía de subida de archivos (https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html), leída por resumen el 23-oct-2026: respalda subida solo a usuarios autorizados, almacenamiento fuera de la raíz web y nombres generados por el servidor; **no describe zona temporal ni cuarentena**, así que la decisión es de diseño, no una práctica citada.

## 4. Qué falta hacer (no se hizo)
1. **ERS v1.12:** RF-01 (cuándo es obligatorio el frente), RF-02 (nota de peticiones), el criterio de aceptación del registro, el tope de 5 MiB ([actualización (c)](../2026-10-23c_unidad-tope-5mb/CAMBIOS.md)), y retirar la zona temporal de RF-50/RF-52 y de la sección 12.
2. **Modelo v0.6:** sin `ARCHIVO_TEMPORAL`, R24 ni H16; la regla de contrato sin frente; ajustar la prueba (36 + 5 comprobaciones, varias dejan de aplicar).
3. **DAS v0.11, diseño técnico (F-01, F-10), estrategia de pruebas y plan:** quitar la zona temporal y la prueba de concurrencia de R24.
4. Hasta entonces, **los documentos se contradicen** con esta decisión; la ERS v1.11 y el modelo v0.5 describen la zona temporal.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
