# Actualización 2026-10-20 (f) — Estrategia de pruebas v0.2: decisiones

**Fecha:** 20 de octubre de 2026
**Documentos afectados:** [Estrategia de pruebas v0.2](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.2_borrador.md) (nueva) y los README de las fases 4 y 6 y de `DOC/`.
**Versión anterior:** [Estrategia v0.1](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.1_borrador.md), que se conserva sin cambios.
**Estado:** borrador; no aprobado.

## 1. Motivo
Ronda de siete preguntas sobre las decisiones que dejó abiertas la estrategia v0.1 (sección 11), planteadas una por una con investigación y recomendación. Las preguntas 2 y 3 salieron de dividir "herramienta de extremo a extremo y de carga".

## 2. Cambios
| ID | Tipo | Descripción | Origen |
|---|---|---|---|
| E1 | modificado | Niveles de prueba (sección 3): ejecutor de Django, Selenium y Locust | Preguntas 1 a 3 |
| E2 | modificado | Rendimiento, restauración y navegadores (sección 6) y comprobación mensual de restauración (sección 7) | Preguntas 3, 5 y 2 |
| E3 | modificado | Criterios de salida y cobertura (sección 9) | Preguntas 4 y 7 |
| E4 | modificado | HP-01 decidido (sección 10) | Pregunta 6 |
| E5 | modificado | Sección 11: decisiones tomadas y pendientes; fuentes añadidas a la sección 2 | Todas |
| E6 | modificado | README de las fases 4 y 6 y de `DOC/` | Regla 3 de `CLAUDE.md` |

## 3. Impacto
- **ERS:** sin cambios. El CA de la segunda mitad de RN-15 se añade en la próxima versión de la ERS, no en esta actualización.
- **DAS:** sin cambios; el temporizador, los respaldos y la integración continua ya están en el DAS v0.9.
- **Fase 6:** debe crear el registro de restauraciones y el script de comprobación mensual.
- **Legal:** los CA marcados (L) siguen con resultado esperado provisional (DP-17 a DP-21).

## 4. Decisiones del solicitante (pregunta → respuesta)
En todos los casos eligió la opción recomendada por el asistente. Las categorías de prioridad y la regla de la pregunta 7 son criterio del solicitante y del asistente, sin una fuente que fije porcentajes.
## Tabla de decisiones (sección 4)
| # | Pregunta | Respuesta | Fecha | Fuentes y validación |
|---|---|---|---|---|
| 1 | Ejecutor de pruebas | El de Django, `unittest` (opción recomendada) | 20-oct-2026 | Documentación de Django sobre pruebas y de pytest-django (versión 4.14.0 del 10-ago-2026; soporte oficial de Django 5.2 y 6.0; Django 6.1 no consta y 6.2 LTS no está confirmado), leídas por resumen. Comparaciones de terceros solo por resultados de búsqueda. `subTest` de `unittest` no verificado en una fuente. Migrar a pytest-django después es posible: ejecuta pruebas `unittest` sin cambios (documentación de pytest-django). |
| 2 | Pruebas de extremo a extremo | Selenium con `StaticLiveServerTestCase` de Django (opción recomendada) | 20-oct-2026 | Documentación de Django sobre `LiveServerTestCase` (ejemplo con Selenium y Firefox; leída hasta el carácter 100.000 de 113.245), de Playwright (Chromium, Firefox y WebKit; WebKit no es idéntico a Safari; su ejemplo con `unittest` no menciona Django) y de Selenium para Safari (solo macOS), todas por resumen. Safari y móvil se verifican a mano antes de producción (RNF-10): ninguna herramienta prueba el Safari real en Windows. |
| 3 | Medición de rendimiento (RNF-08) | Locust, en Python (opción recomendada) | 20-oct-2026 | Documentación de Locust (Python, licencia MIT, interfaz web y modo sin interfaz), de k6 (código abierto; licencia, umbrales y percentiles sin confirmar) y de hey (generador de carga sencillo), todas por resumen. **Ninguna página confirmó el reporte del percentil 95**: se verifica al instalarla y, si no lo reporta, se calcula en Python. Se mide en un Droplet equivalente al de producción con 50 propiedades sintéticas. |
| 4 | Umbral de cobertura de código | Sin umbral; cobertura informativa (Coverage.py con ramas en la integración continua) y revisión de los módulos críticos en cada entrega (opción recomendada) | 20-oct-2026 | Inozemtseva y Holmes, Univ. de Waterloo, ICSE 2014 (correlación baja a moderada entre cobertura y detección de fallos; solo resultados de búsqueda), Fowler, *TestCoverage*, 2012 (contra la cobertura como meta; por resumen) y documentación de Coverage.py (cobertura de ramas; por resumen). No confirmado: opción de Coverage.py para fallar bajo un umbral y su uso con el ejecutor de Django. No se pudo leer el cuerpo de la guía de Google, por lo que no se citan sus cifras. El estudio es sobre sistemas Java, no sobre sistemas de saldos. |
| 5 | Restauración trimestral | El solicitante ejecuta una restauración completa cada trimestre a mano, más una comprobación automática mensual, con registro de resultados en el repositorio y sin datos personales (opción recomendada) | 20-oct-2026 | Google, *Site Reliability Engineering*, capítulo de integridad de datos (probar la recuperación de forma continua, automatizar y alertar si falla; por resumen), y documentación de `pg_restore` (por resumen). NIST SP 800-34 no se usa como respaldo: su página no trata las pruebas. La comprobación automática mensual y el registro en la carpeta de la fase 6 son propuesta del asistente, aceptada por el solicitante; hay que probarla. Hoy no hay revisión por una segunda persona (DP-23). |
| 6 | Segunda mitad de RN-15 (rechazo de movimientos sobre períodos futuros salvo el inmediato) | Caso de prueba ahora, marcado "sin CA", y CA en la próxima versión de la ERS junto con el dictamen del abogado sobre OL-11 (opción recomendada) | 20-oct-2026 | ERS v1.8: RN-15, RF-11 (generación 30 días antes) y OL-11; DAS v0.9 sección 10 (el saldo no puede quedar negativo). Inferencia del asistente, no verificada con datos: por RF-11 y por el rechazo de saldo negativo, la regla es difícil de violar en uso normal. OL-11 pendiente de abogado (DP-17). No se crea ERS v1.9 por esta razón. |

## 5. Pendientes
- Confirmar que Locust reporta el percentil 95 o calcularlo en Python.
- Escribir y probar el script de comprobación mensual de restauración, y crear el registro de restauraciones en la fase 6.
- Elegir la herramienta de cifrado de los respaldos (ADR-024).
- Comprobar Selenium con los navegadores y la versión de Python elegidos.
- Revisión de estas pruebas por otra persona (DP-23).
- CA para la segunda mitad de RN-15 en la próxima versión de la ERS, con el dictamen del abogado sobre OL-11.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`. La investigación se leyó por resumen (la herramienta devuelve un resumen, no el texto completo); en cada fila se indica qué se leyó y qué quedó solo como resultado de búsqueda o no se pudo abrir. Revisión de pares: no realizada.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | brandonC-developer | Pendiente | Pendiente |