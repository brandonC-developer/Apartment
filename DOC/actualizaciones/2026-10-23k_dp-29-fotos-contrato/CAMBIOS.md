# Actualización 2026-10-23 (k) — DP-29: fotografías del contrato (máximo y cifras de partida)

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; las decisiones se incorporan en la ERS v1.14 y en el modelo de datos v0.7 (pendientes de redactar). [DOC/README.md](../../README.md)
**Origen:** DP-29 de la [ERS v1.13](../../fase-1-ers/ERS_SGA_001_v1.13_borrador.md) y RF-52
**Estado:** decisión registrada; documentos sin cambiar; **DP-29 sigue abierta en su segunda parte**; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Cuántas fotografías como máximo por contrato? | "10 por contrato" (recomendada por el asistente) | Máximo de **10** por contrato en la v1, constante del diseño que puede cambiar el solicitante |
| 2 | ¿Con qué cifras se empieza a medir la reducción de la foto del contrato? | "3508 px y calidad 0,85, a confirmar al medir" (recomendada) | Punto de partida de la medición en la entrega E2: lado mayor de **3508 px** y calidad **0,85**; el peso objetivo y los valores definitivos se fijan al medir con fotos reales (un iPhone y dos Android) |

**DP-29 queda dividida:** el número máximo (10) está **resuelto**; las cifras de reducción están **adoptadas como punto de partida** y siguen abiertas hasta medir en la E2. Hasta entonces RF-52 ya no dice que el punto de partida sean los valores de RF-50 (2048 px).

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| OWASP, File Upload Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html | Guía reconocida | Leída por resumen (23-oct-2026) | Subida solo a usuarios identificados, para poder aplicar límites a sus capacidades de subida | No dice cuántos archivos |
| Biblioteca de la Universidad de Illinois, mejores prácticas de OCR: https://guides.library.illinois.edu/OCR/bestpractices | Universidad | Leída por resumen (23-oct-2026) | 300 dpi recomendados para la precisión del OCR; las fuentes de 6 pt la reducen | Habla de escáneres y OCR, no de fotos con teléfono ni de lectura humana |
| Hyland OnBase, resolución de escaneo: https://docs.hyland.com/r/OnBase/Express-Scanning/Foundation-23.1/Express-Scanning/Express-Scanning-Best-Practices/Configuration/Scanning-Resolution | Documentación de un proveedor | Leída por resumen (23-oct-2026) | "Use a resolution of at least 300 dpi" para OCR u otros procesos posteriores | Un solo proveedor; no da un mínimo ni consecuencias |
| MIVAH / modelo de contrato de arrendamiento | — | Búsqueda sin resultado: no se encontró un modelo oficial; los resultados fueron plantillas de otros países | **No hay fuente para el número de páginas de un contrato** | El máximo de 10 es criterio del asistente |

## 3. Cálculos (con cifras de diseño, sin medir)
- 2048 px sobre una A4 (297 mm = 11,7 pulgadas) ≈ 175 ppp; 3508 px ≈ 300 ppp.
- Almacenamiento por 10 fotografías: ≈ 20 MB con el objetivo de 2 MB por foto y 50 MiB en el peor caso (tope de 5 MiB); para 50 contratos activos, ≈ 1 GB y ≈ 2,5 GiB. El peso con 3508 px es mayor y no está medido; los contratos finalizados se conservan según DP-28. El tamaño del disco del servidor no está fijado en el DAS.

## 4. Lo que propone el asistente y el solicitante no decidió
- Que el máximo se aplique con un `CHECK` de `orden` entre 1 y 10 y con rechazo en el servicio (modelo v0.7).
- Que 300 ppp (guías de OCR) sea la referencia para la legibilidad; no es una prueba para fotos con teléfono.
- El peso objetivo para el contrato (a medir).

## 5. Qué falta hacer (no se hizo)
- **ERS v1.14:** RF-52 con el máximo de 10 y las cifras de partida (3508 px, 0,85); DP-29 pasa a "máximo resuelto; cifras por medir en la E2"; CA-76 con el rechazo de la fotografía número 11.
- **Modelo v0.7:** límite de 10 en `DOCUMENTO_CONTRATO` y su prueba.
- **Estrategia de pruebas y plan:** prueba del límite (CA-76); medición de legibilidad y peso en la E2 (HI-08).
- Hasta entonces la ERS v1.13 dice que el punto de partida son los valores de RF-50.
- La medición no se hizo; no se probó ninguna foto real.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
