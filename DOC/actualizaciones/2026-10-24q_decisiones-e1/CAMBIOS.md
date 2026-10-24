# Actualización 2026-10-24 (q) — Decisiones de la entrega E1

**Fecha:** 2026-10-24
**Documentos afectados:** [`AVANCE_IMPLEMENTACION.md`](../../fase-5-implementacion/AVANCE_IMPLEMENTACION.md), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md) y [DOC/README.md](../../README.md). No cambia ningún código ni el plan v0.1.
**Origen:** el plan de trabajo de la E1 (actualización [2026-10-24 (p)](../2026-10-24p_inicio-e1/CAMBIOS.md)) listaba cinco decisiones; se contestaron una por una el 24-oct-2026
**Estado:** decisiones registradas; no aprobado

## 1. Trazabilidad: pregunta, respuesta y decisión
| # | Pregunta | Recomendación del asistente | Respuesta del solicitante | Decisión |
|---|---|---|---|---|
| 1 | ¿Quién redacta el texto informativo del consentimiento mientras el abogado no lo valida? | Borrador del asistente, marcado «sin validar» | «Borrador del asistente marcado «sin validar» (Recomendado)» | El asistente redacta el texto con los ocho puntos del art. 5 y lo que el sistema hace; el sistema lo muestra como borrador sin validar; el abogado lo reemplazará con una versión nueva (DP-21) |
| 2 | ¿Cómo valida y limpia el servidor las imágenes? | Pillow 12.3.0: decodificar, quitar metadatos y volver a codificar | «Pillow 12.3.0: decodificar, quitar metadatos y volver a codificar (Recomendado)» | Tipo real, 5 MiB, decodificación completa, tope de 60 millones de píxeles, orientación aplicada, archivo nuevo sin metadatos |
| 3 | (No se preguntó) ¿Cómo se prueba la reducción en el navegador? | — | — | Ya decidido en la estrategia de pruebas: Selenium con `StaticLiveServerTestCase`; se omite donde no haya navegador |
| 4 | ¿Cómo se publica el script propio de reducción? | `collectstatic` y Nginx sirve `/static/` | «collectstatic y Nginx sirve /static/ (Recomendado)» | Carpeta `/opt/sga/static` de solo lectura servida por Nginx; prueba de que no se sirve nada fuera de ella |
| 5 | ¿Cómo se resuelve el bloqueo de desactivar (CA-29) si los contratos no existen hasta la E2? | Punto de extensión; bloqueo real en la E2 y la E3 | «Punto de extensión; el bloqueo real se verifica en la E2 y E3 (Recomendado)» | La E1 entrega el mecanismo y lo prueba con una comprobación falsa; **el solicitante acepta diferir el bloqueo real a la E2 (contrato vigente) y la E3 (saldos pendientes)**; CA-29 es de prioridad Media |
| 6 | ¿Cómo son las pantallas mientras no existan wireframes? | Funcionales y accesibles, sin estilos | «Funcionales y accesibles, sin estilos; diseño después (Recomendado)» | HTML semántico sin CSS; un pase de diseño con los wireframes |

## 2. Fuentes y su validación
| Fuente | Qué respalda | Cómo se validó | Límites |
|---|---|---|---|
| [OWASP, File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) | Decodificar y volver a codificar; quitar metadatos; guardar fuera de la raíz web con nombre aleatorio. **También dice que reescribir no garantiza eliminar todo contenido malicioso y que el procesador de imágenes maneja entrada no confiable** | Leída con un resumen automático | No menciona límites de dimensiones; el tope de 60 millones de píxeles es criterio del asistente |
| [Django, despliegue de archivos estáticos](https://docs.djangoproject.com/en/5.2/howto/static-files/deployment/) | `collectstatic` y que el servidor web sirva `STATIC_ROOT` bajo `STATIC_URL` | Leída con un resumen automático | No menciona el almacenamiento con huella ni la caché |
| Pillow en PyPI | 12.3.0 (2026-07-01) tiene ruedas para Python 3.14; 13.0.0 salió el 2026-10-16 | Consulta a la API de PyPI el 24-oct-2026 | No se ha instalado ni probado todavía con las fotos |
| Art. 5 de la Ley 8968 | Los ocho puntos del texto informativo | Copia municipal de 2021, leída antes (no es la oficial) | **No es asesoría legal; el borrador no está validado** (DP-17, DP-21) |
| Estrategia de pruebas, ADR-003, ADR-030, ERS (RF-01 a RF-05, RF-39, RF-45, RF-50, CA-01 a CA-83) | Decisiones 3, 5 y 6 | Leídos por el asistente | Criterio de diseño del asistente |

## 3. Qué cambió en el registro de avance
- E1 conserva *en curso*, 0 de 8 CA. Nota de desviación: **CA-29** se cumple en la E1 solo en el mecanismo; el bloqueo real pasa a la E2 y la E3 por aceptación escrita del solicitante. Las filas de la E2 y la E3 reciben ese trabajo.
- El plan v0.1 no se versiona por esto (igual que con CA-18 y CA-47); si prefieres una versión nueva del plan que lo recoja, se hace.

## 4. Lo que sigue
Orden de trabajo propuesto (grupos A a G de la lista de tareas): modelos y privilegios, luego servicios de registro y ficha, el consentimiento, las fotografías en el servidor, el script del navegador, las pantallas y, al final, la medición con fotos reales (necesita las tuyas) y el cierre. Cada paso se hace con tu orden, como en la E0.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
