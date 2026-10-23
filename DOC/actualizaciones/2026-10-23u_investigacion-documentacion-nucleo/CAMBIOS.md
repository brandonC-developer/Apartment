# Actualización 2026-10-23 (u) — Investigación: documentación núcleo del proyecto según buenas prácticas

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; solo [DOC/README.md](../../README.md) (fila nueva)
**Pregunta del solicitante:** "revisa si ya es necesario documentación para el proyecto como núcleo en buenas prácticas según estudios o expertos. INVESTIGA". Se interpreta como: ¿qué documentación núcleo falta o sobra hoy, según estudios y expertos?
**Estado:** investigación; las recomendaciones son **propuestas del asistente**, ninguna está decidida

## 1. Qué hay hoy (revisado en el repositorio, 23-oct-2026)
| Tipo de documento | Qué existe |
|---|---|
| Requisitos | ERS v1.14 (52 RF, 78 CA, matriz de trazabilidad) |
| Arquitectura | DAS v0.11 (restricciones, contexto, bloques, 31 ADR, árbol de calidad, glosario, riesgos) |
| Datos y diseño | Modelo de datos v0.7 (probado en PostgreSQL); diseño técnico v0.7 (permisos, flujos, hallazgos) |
| Pruebas y plan | Estrategia de pruebas v0.3; plan de implementación, lista de verificación y registro de avance |
| Legal y método | Resumen para el abogado, evaluación de la metodología, 14+ actualizaciones de hoy con su `CAMBIOS.md`, script de coherencia |
| Operación (fase 6) | **Solo un README**; "no iniciada" |
| No existe | Modelo de amenazas; diseños de pantalla (wireframes); README en la raíz del repositorio (hay `CLAUDE.md` y `DOC/`); procedimientos operativos |

Dato de volumen: unas 21 000 líneas en las carpetas de fase; 14 versiones de la ERS; sin código.

## 2. Fuentes
| # | Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|---|
| 1 | Manifiesto Ágil: https://agilemanifesto.org/ | Texto fundacional | Leído (WebFetch, 23-oct-2026) | "Working software over comprehensive documentation… while there is value in the items on the right, we value the items on the left more" | No dice cuánta documentación es suficiente; es una declaración de valores |
| 2 | Pasuksmit et al., *Towards Just-Enough Documentation for Agile Effort Estimation*: https://arxiv.org/abs/2107.02420 | Estudio empírico (encuesta) | Solo el resumen de arXiv, leído (23-oct-2026) | 121 profesionales ágiles de 25 países: lo más útil es requisitos funcionales, historias de usuario, definición de terminado, **wireframes de interfaz**, criterios de aceptación y dependencias entre tareas; 98 % considera la documentación de importancia moderada a extrema para estimar; esas informaciones suelen cambiar o faltar | Trata de **estimación de esfuerzo**, no del conjunto de documentos de un proyecto; no se leyó el artículo completo ni sus recomendaciones |
| 3 | Aghajani et al., *Software Documentation Issues Unveiled* (ICSE 2019): https://neverworkintheory.org/2021/10/06/software-documentation-issues-unveiled.html | Estudio revisado por pares (reseña) | Reseña leída; **el artículo y la taxonomía no se leyeron** (la taxonomía es una figura; el PDF de la versión de 2020 devolvió 403) | Analizó 878 artefactos de listas de correo, Stack Overflow, incidencias y pull requests y propuso una taxonomía de problemas de documentación | **No puedo citar qué categorías de problemas encontró** (desactualizada, incorrecta, etc.) |
| 4 | arc42, resumen: https://arc42.org/overview | Plantilla reconocida | Leída (23-oct-2026) | Lista las 12 secciones: objetivos, restricciones, contexto, estrategia, bloques, tiempo de ejecución, despliegue, conceptos transversales, decisiones, calidad, riesgos y deuda técnica, glosario | La página **no dice** si se pueden omitir secciones ni el tamaño proporcional; no lo afirmo |
| 5 | Diátaxis: https://diataxis.fr/ | Marco reconocido (usado por Canonical) | Leída (23-oct-2026) | Cuatro necesidades: tutoriales, guías prácticas, referencia y explicación | No leí el principio de no mezclarlos (la página no lo detalla) |
| 6 | OWASP, Threat Modeling Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html | Guía de experto reconocido | Leída (23-oct-2026) | Se hace idealmente al inicio, en el diseño; cuatro preguntas (qué construimos, qué puede salir mal, qué haremos, ¿lo hicimos bien?); se documentan el modelo del sistema, las amenazas, la respuesta a cada una y los requisitos de seguridad derivados | No fija el formato ni el tamaño |
| 7 | NIST SP 800-218 (SSDF): https://csrc.nist.gov/pubs/sp/800/218/final | Estándar | Solo la página de catálogo; **el PDF no se leyó** | Conjunto de prácticas de desarrollo seguro (febrero de 2022) | **No pude confirmar** que pida modelado de amenazas o requisitos de seguridad; no lo afirmo |
| 8 | Google SRE, respuesta a emergencias: https://sre.google/sre-book/emergency-response/ | Libro de expertos | Capítulo leído por resumen | Un incidente real se agravó porque los procedimientos de reversión no se habían probado; luego se exigió probarlos | **No habla de runbooks ni de playbooks** ni lo cuantifica; respalda solo "probar los procedimientos de recuperación" |
| 9 | Write the Docs, *Docs as Code*: https://www.writethedocs.org/guide/docs-as-code/ | Comunidad reconocida | Leída (23-oct-2026) | Escribir la documentación con las herramientas del software: Git, texto plano, revisiones y pruebas automáticas | No desarrolla beneficios medidos |
| 10 | Búsquedas sobre documentación ágil mínima | Resultados de búsqueda | Solo resultados | Existen estudios (Mielonen, 2023; Fraunhofer, 2016), pero **ninguno nombra un conjunto mínimo de documentos para un equipo pequeño** | No se abrieron |

**Conclusión sobre la evidencia:** no encontré un estudio que diga qué conjunto exacto de documentos necesita un proyecto como este. Lo que hay son principios (suficiente, no exhaustivo; guiado por lo que usa el lector) y plantillas. Las recomendaciones de abajo son criterio del asistente apoyado en esos principios.

## 3. Hallazgos
1. **El núcleo de requisitos, arquitectura, datos, diseño, pruebas y plan ya cubre lo que piden las fuentes** (las 12 secciones de arc42 están representadas en el DAS y el diseño técnico; los criterios de aceptación y la definición de terminado existen). No hace falta documentación núcleo nueva para empezar la etapa A.
2. **Faltan tres cosas con respaldo:** (a) un **modelo de amenazas** (fuente 6), porque el sistema guarda fotos de documentos de identidad y no hay ninguno; (b) **diseños de pantalla** (fuente 2: los wireframes figuran entre lo más útil), porque el sistema tiene interfaz renderizada por servidor y el perfil de la propiedad (HT-11) solo está descrito en texto; (c) **procedimientos operativos probados** (fuente 8), que la fase 6 documentará con la etapa B.
3. **Deuda de consistencia (hallazgo propio, sin estudio que lo cuantifique):** las decisiones de hoy (endurecimiento, tope de subida, zona temporal, perfil de la propiedad) están en `CAMBIOS.md` y en "ajustes" apilados en el DAS v0.11, pero el DAS no tiene una versión que las consolide. Un lector nuevo tendría que juntar 15 actualizaciones.
4. **Riesgo de exceso (fuente 1, con cautela):** 21 000 líneas y 14 versiones de la ERS antes de escribir código son un indicio de documentar más de lo que se verifica. El manifiesto no impone un límite.

## 4. Recomendaciones (propuestas del asistente; ninguna decidida)
| N.º | Propuesta | Fundamento | Cuándo |
|---|---|---|---|
| 1 | **Consolidar** en una versión nueva del DAS las decisiones tomadas (endurecimiento, subida de archivos, HTTPS, firewall…) y quitar los ajustes apilados | Hallazgo 3; Docs as Code (fuente 9) | Ahora |
| 2 | **Modelo de amenazas liviano**: un diagrama de flujo de datos y una tabla (amenaza, respuesta, requisito) para el administrador, las cédulas y el respaldo | Fuente 6 | Antes de cargar datos reales; mejor antes de la E1 |
| 3 | **Diseños de pantalla** solo de las entregas que se van a construir (E1: ficha de inquilino y subida de fotos; E2: perfil de la propiedad) | Fuente 2 | Al empezar cada entrega |
| 4 | **Procedimientos operativos** (restauración, rotación de secretos, actualización) y **probarlos** | Fuente 8; fase 6 | En la etapa B |
| 5 | **No añadir** manual de usuario, más versiones de la ERS por decisiones pequeñas (agruparlas) ni documentos nuevos antes de tener código | Fuente 1 | Siempre |
| 6 | Un **README en la raíz** que explique en una página qué es el proyecto y por dónde leer (tipo explicación, Diátaxis) | Fuente 5 | Cuando se quiera |

## 5. Qué no se hizo
- No se redactó ni se editó ningún documento.
- No se leyeron los textos completos de Aghajani et al., Pasuksmit et al., NIST SP 800-218 ni la documentación completa de arc42.
- No se verificó si arc42 permite omitir secciones.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
