# Actualización 2026-10-22 (i) — Cédula desde el perfil de la propiedad y foto del contrato

**Fecha:** 2026-10-22
**Documentos afectados:** solo [DOC/README.md](../../README.md). **Ninguna ERS, DAS ni otro documento se modificó**: esta actualización registra decisiones del solicitante que cambian el alcance y que aún no están en los requisitos.
**Estado:** registro de decisiones del solicitante; no es aprobación de ningún documento.

## 1. Motivo
El solicitante indicó que en el perfil de cada apartamento hay un botón para agregar la cédula por medio de una fotografía, o al tomar la fotografía del contrato (22-oct-2026). Los documentos vigentes (ERS v1.10, DAS v0.11, diseño técnico v0.7, modelo de datos v0.4) no mencionan ni un perfil de propiedad con ese botón ni la fotografía del contrato; hoy la cédula se carga en la ficha del inquilino (RF-01).

## 2. Preguntas, respuestas y decisiones
| Pregunta | Respuesta del solicitante | Decisión |
|---|---|---|
| ¿Dónde queda la foto de la cédula? | "Botón en el perfil de la propiedad, y se guarda en el inquilino" (opción recomendada por el asistente) | La cédula se agrega desde el perfil de la propiedad como atajo; **la foto sigue siendo del inquilino**. No cambian el modelo ni la retención de cinco años (RN-24) |
| ¿La foto del contrato es un documento nuevo que el sistema guarda? | "Sí, foto del contrato asociada al contrato" (recomendada) | **Requisito nuevo:** fotografía del contrato asociada al contrato, con controles de privacidad equivalentes a los de la cédula |
| ¿La foto del contrato se reduce en el navegador y pasa por la zona temporal? | "Sí, igual que la cédula pero con otra cifra a medir" | Misma mecánica (reducción en el navegador, zona temporal con identificador de un solo uso, HT-10); **la cifra de la foto del contrato no se fijó** y se mide con fotos reales en la entrega E1 |

## 3. Qué falta para llevarlo a los documentos (no hecho)
Estas cuestiones **no están decididas** y las propone el asistente:
- **ERS (versión nueva, v1.11):** requisito para el botón en el perfil de la propiedad (¿qué inquilino? el del contrato vigente, y qué pasa si no hay contrato o hay varios); requisito para la fotografía del contrato (formatos, tamaño, una o varias páginas) y sus criterios de aceptación; definir "perfil de la propiedad" (hoy RF-06 no lo describe).
- **Retención y privacidad:** la fotografía del contrato contiene datos personales del inquilino y del arrendador. Su plazo de conservación, su inclusión en la desasociación (RF-41), en la exportación del titular (RF-40) y en la auditoría de acceso (RF-45) están sin decidir; la retención de cinco años de RN-24 (OL-14) es de la fotografía de la cédula, no del contrato; las obligaciones de conservación contables o del contrato son de DP-18, con el abogado.
- **Modelo de datos y diseño técnico:** entidad para los documentos del contrato; ampliar la zona temporal (HT-10) a este tipo de archivo; operaciones y permisos.
- **Pruebas y plan:** criterios nuevos, y medir en E1 la cifra de reducción de un contrato (un contrato tiene texto pequeño y puede requerir más de 2048 px).
- **Dato sin decidir:** si "al tomar la fotografía del contrato" significa que se extrae o se separa la cédula de la misma imagen, o solo que ambas se agregan desde el mismo botón. **Preguntar al solicitante.**

## 4. Verificación
No se modificaron documentos versionados; la verificación de coherencia aplica cuando se redacte la ERS v1.11.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
