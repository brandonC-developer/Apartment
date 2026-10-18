# Evaluación de la metodología de seis fases

> **Nota de actualización (17-oct-2026, QA):** esta evaluación es de la fecha indicada y no se reescribe. Desde entonces, el DAS v0.6 incorporó la sección de restricciones, el árbol de calidad y el glosario (sección 5 y ajuste 1 quedan atendidos), y el modelo de datos de la fase 3 se inició con una prueba en PostgreSQL. Lo que dice sobre "DAS v0.4" se refiere a esa versión.

**Fecha:** 17 de octubre de 2026
**Pregunta:** ¿Es correcta, según buenas prácticas, la secuencia ERS → Arquitectura → Diseño técnico → Pruebas → Implementación → Despliegue y operación?

## 1. Veredicto

**La secuencia es correcta como mapa de productos de trabajo y de revisión, con cinco ajustes.** No lo es como proceso estrictamente secuencial en el que cada fase espera a que termine la anterior. Las fuentes consultadas coinciden en tres puntos:

1. Los procesos técnicos de los estándares de ciclo de vida incluyen requisitos, arquitectura, diseño, verificación, validación, operación y mantenimiento (fuentes F1, F3).
2. Un recorrido único y secuencial es riesgoso; hay que iterar (F5, F6).
3. La documentación debe mantenerse con el mismo control de versiones y revisión que el código, o se desactualiza (F8, F9).

## 2. Correspondencia entre las fases y los estándares

| Fase | Producto | Proceso técnico equivalente | Estándar o guía de referencia |
|---|---|---|---|
| 1 | ERS | Definición de requisitos de partes interesadas y de sistema/software | ISO/IEC/IEEE 29148:2018 (ya usada en la ERS) |
| 2 | Arquitectura | Definición de arquitectura | ISO/IEC/IEEE 42010:2022; arc42; SEI *Views and Beyond* |
| 3 | Diseño técnico | Definición de diseño | Sin estándar vigente equivalente verificado (ver nota 1) |
| 4 | Pruebas | Verificación y validación | ISO/IEC/IEEE 29119 (partes 2 y 3) |
| 5 | Implementación | Implementación e integración | ISO/IEC/IEEE 12207:2017 |
| 6 | Despliegue y operación | Transición, operación y mantenimiento | ISO/IEC/IEEE 12207:2017; SWEBOK v4 (área de operaciones) |

**Nota 1.** IEEE 1016-2009, sobre descripciones de diseño de software, figura como "Inactive-Reserved" desde el 5 de marzo de 2020 (F4). Se puede usar como referencia de contenido, no como norma vigente.

## 3. Ajustes recomendados

| # | Ajuste | Fundamento | Estado de la evidencia |
|---|---|---|---|
| 1 | **Tratar las fases como líneas base con revisión, no como cascada.** Aprobar cada documento por versión e iterar. Adelantar decisiones de alto riesgo (proveedor de WhatsApp, respaldo, retención legal) sin esperar al cierre de la fase anterior. | Royce, según el ensayo de Wheeler, calificó el esquema secuencial simple de "arriesgado" que "invita al fracaso" y pedía iterar (F5). Boehm describe el modelo en espiral como guiado por riesgo y no solo por documentos (F6). ISO/IEC/IEEE 12207 se presenta como adaptable a enfoques en cascada, iterativos y ágiles (F1). | Royce: fuente secundaria (el artículo original no se pudo descargar). Boehm: texto del artículo leído parcialmente por resumen. F1: página divulgativa de arc42, no la norma. |
| 2 | **Empezar la estrategia de pruebas en cuanto la ERS tenga línea base**, sin esperar al diseño técnico. Los criterios de aceptación ya existen en la ERS. | ISO/IEC/IEEE 29119-3 organiza la documentación de prueba por procesos de 29119-2 e incluye en el plan los niveles, criterios de entrada y salida y, en los casos de prueba, un apartado de trazabilidad (F7). | Fuente secundaria (catálogos). La recomendación de adelantar es **inferencia nuestra**, no un texto de la norma. |
| 3 | **Añadir gestión de configuración y control de cambios** como práctica transversal: baselines, versiones inmutables, registro de cambios por actualización. | ISO/IEC/IEEE 12207 incluye entre sus procesos de gestión técnica configuración, decisión, riesgo e información (F1). IEEE 828-2012, sobre gestión de configuración, está "Inactive-Reserved" desde 2023 y hay una revisión en proceso (F10). | F1 y F10 son secundarias o de catálogo; no se leyó el texto de las normas. |
| 4 | **Mantener la trazabilidad desde el origen de cada requisito** (pregunta, respuesta, decisión), no solo del requisito hacia las pruebas. | Gotel y Finkelstein (Imperial College, 1994), con estudios empíricos a más de 100 profesionales, concluyen que la mayoría de los problemas atribuidos a mala trazabilidad provienen de trazabilidad previa a la especificación insuficiente (F11). | Resumen del repositorio de UCL Discovery; PDF no leído completo. |
| 5 | **Gestionar la documentación como código:** control de versiones, revisión de cambios, un único lugar por documento y cambios registrados. | Write the Docs describe documentación en texto plano bajo Git con revisión como código (F8). Aghajani et al. (ICSE 2019) clasifican problemas de documentación mined de 878 artefactos; un trabajo posterior cita que la desactualización es un problema frecuente, con una cifra que **no pudimos confirmar** en el original (F9). | F8 leída por resumen; F9 solo en resumen y por cita de terceros. |

## 4. Lo que las seis fases no cubren y conviene añadir

| Tema | Por qué importa en este proyecto |
|---|---|
| **Validación legal como puerta de aprobación** | Las obligaciones de la Ley 7527 y la Ley 8968 afectan requisitos. Está pendiente (DP-17). |
| **Seguridad y privacidad transversales** | SWEBOK v4 incorpora seguridad como área propia, junto con arquitectura y operaciones (F2). En el proyecto hay datos de cédulas y posible dato sensible. |
| **Migración y carga inicial de datos** | El saldo de apertura (RF-43) exige un plan de carga que no corresponde claramente a ninguna de las seis fases. |
| **Decisiones y riesgos como registro continuo** | La ERS ya tiene decisiones pendientes y el DAS tiene ADR. ISO/IEC/IEEE 42010:2022 incluye una cláusula de decisiones y justificación (F12, referencia divulgativa). |

## 5. Estructura del DAS frente a arc42

arc42 tiene 12 secciones (F13): introducción y objetivos, restricciones, contexto y alcance, estrategia de solución, vista de bloques, vista de ejecución, vista de despliegue, conceptos transversales, decisiones de arquitectura, requisitos de calidad, riesgos y deuda técnica, glosario. El DAS v0.4 cubre la mayoría. **Faltan** una sección de restricciones, un árbol de requisitos de calidad y un glosario propio, y la vista de despliegue depende de decisiones aún abiertas (DP-04, DP-08).

## 6. Límites de esta evaluación

- Los estándares ISO e IEEE son de pago. No se leyó ninguno; las descripciones provienen de catálogos y páginas divulgativas, que se señalan como tales.
- El ensayo de Royce de 1970 no se pudo descargar; se citó mediante el ensayo de David A. Wheeler.
- Dos fuentes divulgativas listan los procesos técnicos de ISO/IEC/IEEE 12207 de forma distinta (10 frente a 14). Solo se afirma lo que aparece en ambas: requisitos, arquitectura, implementación, integración, verificación, validación, operación y mantenimiento. "Definición de diseño" aparece solo en una; por eso el ajuste de la fase 3 queda como inferencia.
- No se encontraron estudios que comparen empíricamente esta secuencia de seis fases con otras para proyectos de este tamaño.

## 7. Fuentes

| ID | Fuente | Tipo | Cómo se validó |
|---|---|---|---|
| F1 | arc42 Quality, resumen de ISO/IEC/IEEE 12207. https://quality.arc42.org/standards/iso12207 | Divulgativa | Leída por resumen |
| F2 | SWEBOK Guide v4, IEEE Computer Society. https://www.computer.org/education/bodies-of-knowledge/software-engineering | Guía profesional | Solo resultados de búsqueda; áreas nuevas: arquitectura, operaciones, seguridad |
| F3 | Wikipedia y arc42 sobre ISO/IEC/IEEE 12207:2017 (procesos técnicos) | Divulgativa | Comparadas entre sí |
| F4 | IEEE SA, IEEE 1016-2009. https://standards.ieee.org/ieee/1016/4502/ | Catálogo oficial | Leída por resumen |
| F5 | D. A. Wheeler, "The Waterfall Model". https://dwheeler.com/essays/waterfall.html (cita a Royce, 1970) | Ensayo | Leída por resumen |
| F6 | B. W. Boehm, "A Spiral Model of Software Development and Enhancement", *Computer* 21(5), 1988. https://faculty.washington.edu/hazeline/misc/reserve/boehm_spiralmodel.pdf | Artículo, copia universitaria | Solo resultados de búsqueda |
| F7 | ISO/IEC/IEEE 29119-3:2021, catálogos. https://standards.ieee.org/ieee/360/7499/ y otros | Catálogos | Resultados de búsqueda |
| F8 | Write the Docs, "Docs as Code". https://www.writethedocs.org/guide/docs-as-code/ | Comunidad profesional | Leída por resumen |
| F9 | Aghajani et al., "Software Documentation Issues Unveiled", ICSE 2019. https://2019.icse-conferences.org/details/icse-2019-Technical-Papers/49/Software-Documentation-Issues-Unveiled | Artículo universitario | Solo resumen |
| F10 | IEEE SA, IEEE 828-2012. https://standards.ieee.org/standard/828-2012.html | Catálogo oficial | Resultados de búsqueda |
| F11 | Gotel y Finkelstein, "An Analysis of the Requirements Traceability Problem", IEEE ICRE 1994. https://discovery.ucl.ac.uk/749/ | Artículo universitario | Resultados de búsqueda |
| F12 | arc42 Quality, resumen de ISO/IEC/IEEE 42010:2022. https://quality.arc42.org/standards/iso-42010 | Divulgativa | Resultados de búsqueda |
| F13 | arc42, plantilla. https://docs.arc42.org/home/ | Plantilla de referencia | Leída por resumen |
