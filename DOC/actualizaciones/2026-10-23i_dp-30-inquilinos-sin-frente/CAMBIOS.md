# Actualización 2026-10-23 (i) — DP-30: inquilinos guardados sin frente

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorpora en la ERS v1.13 (pendiente de redactar, junto con la del tope de 5 MiB ya incorporada en la v1.12 y lo que se decida después). [DOC/README.md](../../README.md)
**Origen:** DP-30 de la [ERS v1.12](../../fase-1-ers/ERS_SGA_001_v1.12_borrador.md), abierta en la [actualización 2026-10-23 (e)](../2026-10-23e_ERS-v1.12/CAMBIOS.md)
**Estado:** decisión registrada; documentos sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Qué se hace con los inquilinos guardados sin frente que nunca se completan? | "Aplicar RF-41 tal como está" (recomendada por el asistente) | No hay plazo ni regla nueva: un inquilino sin contrato se trata con RF-41 y CA-66 (1 año por defecto, configurable; aviso previo al administrador; eliminación de fotografías y desasociación de datos) |
| 2 | ¿Cómo se hace visible un inquilino sin frente? | "Indicación en la ficha + filtro en la lista" (recomendada) | La ficha muestra «Falta el frente» (ya propuesto en RF-03) y la lista de inquilinos tiene un filtro «Sin frente». **Sin alertas ni correos** |

DP-30 queda **resuelta** con estas dos decisiones.

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Ley 8968, art. 6, según OL-14 de la [ERS v1.12](../../fase-1-ers/ERS_SGA_001_v1.12_borrador.md) | Ley | **No se reabrió el texto hoy**; se tomó de cómo lo registra la ERS | Los datos deben ser adecuados a su fin y se eliminan cuando dejan de ser pertinentes | Que un año sea un plazo razonable para este caso es interpretación pendiente de abogado (DP-17) |
| Nielsen Norman Group, 10 heurísticas de usabilidad: https://www.nngroup.com/articles/ten-usability-heuristics/ | Referencia de usabilidad reconocida | Leída completa (WebFetch, 23-oct-2026) | Heurística 1: mantener informado al usuario; heurística 6: hacer visibles los elementos para no cargar la memoria | Heurísticas generales, no un estudio de este caso; la elección del filtro y de no enviar alertas es criterio del asistente |

## 3. Lo que propone el asistente y el solicitante no decidió
- Que el filtro «Sin frente» se base en el valor derivado "inquilino con frente cargado" del modelo v0.6 (sección 5); no requiere atributo nuevo.
- Que no haya alertas ni correos para este caso (criterio del asistente, aceptado).
- Los textos «Falta el frente» y «Sin frente».

## 4. Qué falta hacer (no se hizo)
- **ERS v1.13:** pasar DP-30 a resuelta en la sección 12; en RF-03 añadir el filtro «Sin frente» en la lista de inquilinos; en CA-78 añadir que la lista permite filtrar los inquilinos sin frente. RF-41 y CA-66 no cambian.
- Estrategia de pruebas (CA-78) y plan (E1 o E2, según dónde viva la lista de inquilinos): añadir el filtro como parte de CA-78.
- Hasta entonces la ERS v1.12 sigue listando DP-30 como abierta.
- Sin cambios en el modelo v0.6: el filtro usa un derivado que ya existe.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
