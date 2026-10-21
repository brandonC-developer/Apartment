# Estrategia y plan de pruebas

**Identificador:** EPP-SGA-001
**Versión:** 0.3 — reemplaza a la [v0.2](ESTRATEGIA_PRUEBAS_SGA_001_v0.2_borrador.md), que se conserva sin cambios (la [v0.1](ESTRATEGIA_PRUEBAS_SGA_001_v0.1_borrador.md) también)
**Estado:** Borrador para revisión; no aprobado
**Fecha:** 21 de octubre de 2026
**ERS de referencia:** ERS-SGA-001 v1.9 (borrador no aprobado)
**DAS de referencia:** DAS-SGA-001 v0.11 (borrador no aprobado)

Este documento propone cómo demostrar que cada requisito del SGA funciona. **No hay código ni se ha autorizado implementarlo**: todo lo que sigue es un diseño de pruebas, no resultados. Lo que proviene de una fuente se indica con ella; lo demás es **propuesta** del asistente. La v0.3 alinea la estrategia con la ERS v1.9 y el DAS v0.11 (decisiones del solicitante del 20 y 21-oct-2026: pruebas del canal de correo, CA-58 a CA-61, recibo físico y comprobante como fase posterior; sección 5 y HP-01); la v0.2 incorporó las siete decisiones del solicitante del 20-oct-2026 (sección 11); lo que sigue como propuesta se indica. No es asesoría legal: los criterios de aceptación que dependen de las leyes 7527 y 8968 son provisionales hasta que un abogado valide las obligaciones (DP-17).

## 1. Alcance

| Incluido | Fuera de alcance de este documento |
|---|---|
| Pruebas de los 61 criterios de aceptación (CA-01 a CA-61; CA-37 y CA-54 pertenecen a la fase posterior del comprobante y no se ejecutan en la v1) | Casos de prueba detallados (se escriben con la implementación) |
| Verificación de los RNF sin criterio de aceptación (RNF-05, 07, 08, 09, 10, 11) | Pruebas de penetración por un tercero |
| Pruebas de operación: restauración, temporizador, HTTPS y respaldos | Pruebas del canal de WhatsApp (DP-04, futuro, fuera de la v1): solo se prueba la interfaz de canal de salida con el correo y un canal simulado |
| Datos de prueba y entornos | Cualquier dato personal real |

## 2. Fundamento metodológico y fuentes

| Fuente | Qué respalda | Cómo se validó | Limitaciones |
|---|---|---|---|
| [Vocke, *The Practical Test Pyramid* (martinfowler.com, 26-feb-2018)](https://martinfowler.com/articles/practical-test-pyramid.html) | Muchas pruebas unitarias rápidas, menos de integración y muy pocas de extremo a extremo; evitar la pirámide invertida | Leída por resumen | Artículo de un autor sobre su experiencia, no un estudio empírico |
| [Django, visión general de pruebas](https://docs.djangoproject.com/en/stable/topics/testing/overview/) | `TestCase` envuelve cada prueba en una transacción; `TransactionTestCase` confirma de verdad; pruebas con base de datos de prueba; ejecución en paralelo; `DEBUG = False` en pruebas; `--shuffle` para detectar dependencias de orden | Leída por resumen | No trata PostgreSQL en una sección propia |
| [Django, herramientas de pruebas](https://docs.djangoproject.com/en/stable/topics/testing/tools/) | Cliente de pruebas con `enforce_csrf_checks`; `override_settings`; buzón de correo en memoria; `assertNumQueries` | Leída por resumen, hasta el carácter 100.000 de 113.245 | El resumen no cubrió cómo probar código dependiente del tiempo |
| [OWASP, Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) | Existe una guía de pruebas de seguridad web, versión estable 4.2 (5.0 en desarrollo) | Solo la página de presentación | **No se leyeron sus categorías ni sus casos**; aquí solo se usa como referencia futura |
| ISO/IEC/IEEE 29119-3 (documentación de pruebas) | La evaluación metodológica del proyecto la propone como base de esta fase | **No se pudo abrir** ([página de ISO](https://www.iso.org/standard/79429.html), error 403) | No se afirma nada sobre su contenido; la estructura de este documento es propia |
| [pytest-django](https://pytest-django.readthedocs.io/en/latest/changelog.html) | Versión 4.14.0 (10-ago-2026); soporte oficial de Django 5.2 y 6.0; Django 6.1 no consta y 6.2 LTS no está confirmado; ejecuta pruebas `unittest` sin cambios | Leída por resumen | Respalda la decisión de no usarlo ahora y poder migrar después |
| [Django, LiveServerTestCase](https://docs.djangoproject.com/en/stable/topics/testing/tools/#liveservertestcase), [Playwright](https://playwright.dev/python/docs/browsers), [Selenium y Safari](https://www.selenium.dev/documentation/webdriver/browsers/safari/) | Selenium con `StaticLiveServerTestCase` está documentado por Django; WebKit de Playwright no es idéntico a Safari; `safaridriver` es de macOS | Leídas por resumen | Ninguna herramienta prueba el Safari real en Windows; Playwright con el servidor en vivo de Django no se verificó |
| [Locust](https://docs.locust.io/en/stable/what-is-locust.html), [k6](https://grafana.com/docs/k6/latest/), [hey](https://github.com/rakyll/hey) | Locust: Python, licencia MIT, interfaz web y modo sin interfaz | Leídas por resumen | **Ninguna confirmó el reporte del percentil 95** |
| [Inozemtseva y Holmes, Univ. de Waterloo, ICSE 2014](https://cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf); [Fowler, *TestCoverage*, 2012](https://martinfowler.com/bliki/TestCoverage.html); [Coverage.py](https://coverage.readthedocs.io/en/latest/) | La cobertura tiene una correlación de baja a moderada con la detección de fallos y no debe ser una meta; sirve para encontrar código sin probar; Coverage.py mide ramas | Waterloo: solo resultados de búsqueda. Fowler y Coverage.py: por resumen | Estudio sobre sistemas Java. No se confirmó la opción de Coverage.py para fallar bajo un umbral ni su uso con Django. La guía de Google no se pudo leer |
| [Google, *Site Reliability Engineering*, integridad de datos](https://sre.google/sre-book/data-integrity/); [PostgreSQL, pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html) | Probar la recuperación de forma continua, automatizar y alertar si falla; restaurar en una base nueva | Leídas por resumen | Escala distinta a la del SGA; NIST SP 800-34 no se usa porque su página no trata las pruebas |
| [ISTQB, programa del nivel básico](https://study.astqb.org/?p=5); [mapeo de pruebas basadas en riesgo, Univ. del Valle, 2021](https://revistaingenieria.univalle.edu.co/index.php/ingenieria_y_competitividad/article/view/9503); [taxonomía de Fraunhofer](https://arxiv.org/abs/1912.11519) | Priorizar pruebas por probabilidad e impacto del riesgo | Solo el índice del programa y resultados de búsqueda | No fijan qué porcentaje puede quedar sin probar; esa regla es criterio del solicitante y del asistente |

La proporción de la pirámide es una orientación del autor, no una regla medida. No encontré estudios universitarios sobre estrategias de pruebas para sistemas de saldos y comprobantes.

## 3. Niveles de prueba (propuesta)

| Nivel | Qué prueba | Herramienta (propuesta) | Base de datos |
|---|---|---|---|
| Unitarias | Reglas puras: períodos por aniversario, prorrateo, reajuste, saldos, estados derivados, plazos de cinco días hábiles | Ejecutor de Django (`unittest`), decisión del solicitante | Ninguna |
| Integración | Restricciones de PostgreSQL (contratos solapados, unicidad contrato-período, comprobantes sin huecos, clave de solicitud), transacciones y el comando diario | `TestCase` de Django | **PostgreSQL 18**, no SQLite: `ExclusionConstraint` es de PostgreSQL |
| Concurrencia | Contador de comprobantes y envío repetido de un abono | `TransactionTestCase` (confirma de verdad) | PostgreSQL 18 |
| Vistas y permisos | Acceso denegado, CSRF, sesión, descarga de documentos privados | Cliente de pruebas con `enforce_csrf_checks=True` | PostgreSQL 18 |
| Extremo a extremo | Pocos recorridos críticos en navegador (registrar pago y emitir comprobante; alta de contrato) | Selenium con `StaticLiveServerTestCase` de Django, decisión del solicitante | PostgreSQL 18 |
| No funcionales y de operación | Rendimiento, compatibilidad, restauración, temporizador, HTTPS | Locust para el rendimiento (decisión del solicitante); ver secciones 6 y 7 | Entorno de prueba |

Notas de diseño:
- Las pruebas usan **la misma versión de PostgreSQL que producción** (18), porque ADR-002 depende de funciones propias de PostgreSQL.
- Django ejecuta las pruebas con `DEBUG = False`. Para acelerarlas permite un hasher de contraseñas rápido; por eso debe existir además **una prueba con Argon2id y los parámetros del ADR-019**, que no use ese atajo.
- El tiempo se controla fijando la hora actual en las pruebas. La técnica concreta (parchear `timezone.now` o una biblioteca) **no está respaldada por la documentación de Django que leí**; es práctica común y queda por decidir.
- Para detectar dependencias ocultas entre pruebas, Django ofrece `--shuffle` (fuente: visión general).
- La cobertura de código se mide con Coverage.py, con ramas, de forma informativa (sección 9).
- Una prueba para la segunda mitad de RN-15 se escribe aunque no tenga CA (HP-01).

## 4. Entornos y datos de prueba (propuesta)

| Entorno | Uso | Datos |
|---|---|---|
| Local del desarrollador | Unitarias, integración, vistas | Sintéticos |
| Integración continua (GitHub Actions, ADR-025) | Todo lo automatizable en cada cambio: pruebas, `check --deploy`, migraciones, contra PostgreSQL 18 | Sintéticos |
| Droplet de prueba temporal (DigitalOcean, ADR-023) | Restauración, temporizador con zona horaria, HTTPS con `certbot renew --dry-run`, prueba de borrado a los 35 días de Spaces | Sintéticos |

Reglas: **nunca datos personales reales en pruebas** (Ley 8968, sin validar por abogado); fotografías de cédula de prueba generadas, no reales; las claves de Spaces y de cifrado de prueba son distintas de las de producción. El volumen de prueba de rendimiento es el de diseño: 50 propiedades (RE-08).

## 5. Cobertura de criterios de aceptación

Prioridad (propuesta): **Alta** = dinero, plazos legales, datos personales o seguridad; **Media** = reglas de negocio sin riesgo legal inmediato; **Baja** = presentación o comodidad. Un CA con **(L)** depende de una obligación legal sin validar por abogado (DP-17 a DP-21): su prueba se puede escribir, pero el resultado esperado es provisional.

| Área (ERS sección 9) | CA | Nivel principal | Prioridad |
|---|---|---|---|
| Inquilinos y datos personales | CA-01, 25, 29 | Integración | Media |
| | CA-11, 26 | Vistas y permisos; integración (auditoría) | Alta |
| | CA-27, 28 (L) | Unitarias (plazo de cinco días hábiles); integración (retención) | Alta |
| Contratos y obligaciones | CA-02, 24, 32 | Integración (solape de contratos) | Media |
| | CA-03, 30, 14, 31 | Unitarias (fechas, mes corto, prorrateo); integración (unicidad) | Alta |
| Movimientos y estados | CA-04, 19, 20, 21, 33, 34, 35 | Unitarias; integración | Alta |
| | CA-50, 51, 36 | Unitarias (vencimiento, tope, gracia) | Alta |
| | CA-37 (L), 38 | CA-37: fase posterior del comprobante (no se ejecuta en la v1). CA-38: integración | Alta |
| | CA-58 (L) | Unitarias (regla de período futuro) e integración de la operación de registro | Alta |
| | CA-61 | Integración (número de recibo físico único; movimiento sin número) | Media |
| Cambios de condiciones | CA-12, 39, 22, 40 | Unitarias (fecha efectiva, tope, bloqueo por abonos); integración | Alta |
| Calendario | CA-06, 07 | Vistas | Baja |
| Notificaciones | CA-08, 41, 05, 42, 43, 44 | Integración (buzón de correo en memoria de Django, comando diario) | Media |
| | CA-09 | Integración (canal de correo simulado que falla) | Media |
| Depósito | CA-15, 16, 17, 23, 45, 46 | Unitarias; integración | Media |
| Seguridad y configuración | CA-13, 47, 48 | Vistas y permisos | Alta |
| | CA-59 | Vistas y permisos; integración (enlace de un solo uso y 15 minutos; no inicia sesión; buzón en memoria) | Alta |
| | CA-60 (L) | Integración (correo simulado que falla en el aviso de seguridad; reintentos; alerta persistente) | Alta |
| | CA-18 | Unitarias; operación (zona horaria del temporizador) | Media |
| | CA-10 | Integración | Alta |
| | CA-56, 57 (L) | Unitarias (plazo); integración | Alta |
| | CA-52, 54 | CA-52: concurrencia. CA-54: fase posterior del comprobante (no se ejecuta en la v1) | Alta |
| | CA-53 | Integración (auditoría) | Alta |
| | CA-55, 49 | Unitarias; integración | Alta |

Recuento: 61 de 61 CA asignados (los 57 de la v0.2 más CA-58 a CA-61); CA-37 y CA-54 quedan asignados pero se ejecutan solo en la fase posterior del comprobante. No se recalculó el desglose por área de la v0.2, porque los CA nuevos no siguen las áreas de la sección 9 de la ERS.

## 6. Requisitos sin criterio de aceptación

Origen: matriz de trazabilidad de la ERS v1.8 (sección 10; ver la [actualización 2026-10-20 (b)](../actualizaciones/2026-10-20b_ERS-v1.8-matriz/CAMBIOS.md)); la ERS v1.9 no cambió los seis RNF sin criterio.

| Requisito | Cómo se verificaría (propuesta) | Cuándo |
|---|---|---|
| RNF-05 Un fallo del servicio de correo (o, en el futuro, de WhatsApp) no bloquea nada | Prueba de integración con un canal simulado que falla: la notificación web se conserva y el registro de movimientos sigue funcionando (CA-09 cubre parte) | Automatizada |
| RNF-07 Validación y mensajes comprensibles | Pruebas de formularios con entradas inválidas; revisión manual de los mensajes | Automatizada y manual |
| RNF-08 Consultas en menos de 2 s en el percentil 95 | Medición con Locust (decisión del solicitante) y datos sintéticos de 50 propiedades, en un Droplet equivalente al de producción; si Locust no reporta el percentil 95, se calcula en Python. La ERS lo llama "objetivo a validar" | Antes de producción |
| RNF-09 Respaldo y recuperación | Restauración en un Droplet temporal desde la copia cifrada de Spaces: medir el tiempo (RTO de 24 h), comprobar contenido de contratos, movimientos, comprobantes y fotografías; comprobar que se borra a los 35 días. Lo ejecuta el solicitante a mano, con una comprobación automática mensual entre pruebas y registro en la carpeta de la fase 6 (sin datos personales) | Antes de producción y cada 3 meses |
| RNF-10 Navegadores | Recorridos críticos en las dos últimas versiones mayores de Chrome, Edge, Firefox y Safari, en escritorio y móvil; manual o con Selenium; Safari y móvil siempre a mano, porque ninguna herramienta prueba el Safari real en Windows | Antes de producción |
| RNF-11 Separación de responsabilidades | Revisión de diseño (dependencias entre módulos); no es una prueba automática | En la revisión de código |

## 7. Pruebas no funcionales y de operación (propuesta)

| Tema | Prueba | Fuente / estado |
|---|---|---|
| HTTPS | `certbot renew --dry-run` en el servidor de prueba | [Certbot](https://eff-certbot.readthedocs.io/en/stable/using.html#automated-renewals), leída por resumen |
| Configuración de producción | `manage.py check --deploy` en la integración continua | [Django, lista de despliegue](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/), leída por resumen |
| Temporizador diario | Ejecutarlo en el Droplet de prueba: con el servidor apagado a la hora, debe recuperarse (`Persistent=yes`); comprobar la hora local en `America/Costa_Rica` y que una segunda ejecución no duplique (RNF-16) | [systemd](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html), por resumen; versión mínima de systemd **no verificada** |
| Respaldo y borrado a 35 días | Regla de ciclo de vida de Spaces con una retención corta primero, para ver si borra | Solo resultados de búsqueda; hay reportes antiguos de que no siempre borraba |
| Comprobación automática mensual de restauración | Un script restaura el último respaldo en una base temporal con `pg_restore`, ejecuta consultas de cordura y avisa si falla o no da señal de éxito. **Propuesta del asistente, aceptada por el solicitante; hay que probarla** | Principio de Google (por resumen); el script no existe |
| Cifrado de respaldos | Restaurar con la clave correcta y comprobar que falla con una incorrecta | Herramienta de cifrado aún sin elegir (ADR-024) |
| Seguridad de la aplicación | Contraseña de 15 caracteres mínimo, Argon2id (ADR-019), bloqueo de acceso sin sesión, descarga de cédula solo autenticado, CSRF, subida de archivos (formato real, 5 MB, nombre aleatorio) | OWASP WSTG como referencia futura; **sus casos no se leyeron** |
| Endurecimiento del servidor | Revisión contra una guía reconocida (CIS, OWASP) | **Sin investigar** (DAS, sección 16) |

## 8. Casos que requieren atención especial

Entradas que cada prueba debe cubrir. Los resultados esperados salen de los CA de la ERS; aquí no se recalculan.

| Tema | Entradas límite | CA relacionados |
|---|---|---|
| Fin de mes y meses cortos | Contratos que inician el 29, 30 y 31 | CA-03, CA-30 |
| Años bisiestos | Contrato o período que incluye el 29 de febrero (2028 es bisiesto) | CA-03, CA-14 |
| Prorrateo del último período | Meses de 28, 29, 30 y 31 días; redondeo (DP-01 sin validar) | CA-14 |
| Gracia de 7 días | Pago el día 7, el día 8; vencimiento dentro del período | CA-36, CA-50 |
| Reajuste | Fecha efectiva normalizada, tope digitado, moneda extranjera, importe por debajo de lo abonado | CA-12, CA-39, CA-40, CA-51 |
| Importes | Aritmética decimal exacta, CRC y USD, tipo de cambio manual (RNF-17) | CA-38, CA-55 |
| Comprobantes | Numeración consecutiva sin huecos, aun si una transacción falla; serie global provisional (DP-20) | CA-37, CA-54 |
| Idempotencia | Mismo envío con la misma clave; proceso diario ejecutado dos veces | CA-52, RNF-16 |
| Zona horaria | Hora local más zona (DP-26); temporizador del servidor | CA-18, RNF-12 |
| Retención y eliminación | Cinco años de la fotografía; solicitud del titular en cinco días hábiles; respaldos de 35 días (DP-18) | CA-27, CA-28 |

## 9. Criterios de entrada y salida (propuesta, valores por decidir)

- **Entrada:** ERS aprobada; DAS aprobado; entorno de integración continua operativo.
- **Salida de la versión 1:** todos los CA de prioridad alta pasan; ningún defecto abierto que afecte dinero, plazos legales, datos personales o seguridad; restauración superada; RNF-08 medido; revisión legal cerrada (DP-17 a DP-21) o riesgo asumido por escrito.
- **Pruebas que pueden quedar sin ejecutar antes de producción (decisión del solicitante, 20-oct-2026):** ninguna de prioridad **alta**; las de prioridad **media** solo con una aceptación escrita por caso (qué falta, riesgo y plazo) en el registro de cambios; las de prioridad **baja** se pueden diferir, con la lista de lo pendiente. Las categorías y reglas son criterio del solicitante y del asistente; ninguna fuente fija porcentajes.
- **Umbral de cobertura de código (decisión del solicitante, 20-oct-2026):** **ninguno**. Coverage.py con ramas, informativa, en la integración continua; en cada entrega se revisa el código sin cubrir de los módulos críticos (períodos, prorrateo, reajuste, movimientos, comprobantes y plazos legales).

## 10. Hallazgos de esta estrategia

| ID | Hallazgo | Propuesta |
|---|---|---|
| HP-01 | **Resuelto en la ERS v1.9 con CA-58 (21-oct-2026).** La segunda mitad de RN-15 no tenía criterio de aceptación. La redacción de CA-58 es propuesta del asistente, no revisada por el solicitante, y su resultado esperado queda provisional (L) hasta el dictamen sobre OL-11. Propuesta registrada en la v0.2 (abajo): | **Decidido (20-oct-2026):** caso de prueba ahora, marcado "sin CA" y de prioridad alta (L); el CA se añade en la próxima versión de la ERS junto con el dictamen del abogado sobre OL-11. Inferencia del asistente, no verificada con datos: por RF-11 y por el rechazo de saldo negativo, la regla es difícil de violar en uso normal |
| HP-02 | Los CA no citan los requisitos que verifican; la trazabilidad solo está en la matriz de la ERS | Al escribir los casos de prueba, cada uno cita su CA y sus RF, RN y RNF |
| HP-03 | El script de coherencia no revisa este documento ni que cada requisito esté en la matriz. La auditoría del 21-oct-2026 mostró que esto dejó pasar tres documentos desalineados con la ERS v1.9 | Ampliar el script: la decisión sobre ampliarlo sigue pendiente del solicitante |
| HP-04 | Los CA marcados (L) tienen resultado esperado provisional | Revisar con el dictamen del abogado |

HP-nn es un identificador local de este documento, no de la lista compartida del proyecto.

## 11. Decisiones del solicitante y pendientes

Decididas el 20-oct-2026, tras una investigación y una recomendación del asistente por cada una (detalle y fuentes en la [actualización 2026-10-20 (f)](../actualizaciones/2026-10-20f_fase-4-decisiones/CAMBIOS.md)). En todos los casos se eligió la opción recomendada.

| # | Pregunta | Decisión |
|---|---|---|
| 1 | Ejecutor de pruebas | El de Django (`unittest`) |
| 2 | Pruebas de extremo a extremo | Selenium con `StaticLiveServerTestCase`; Safari y móvil a mano |
| 3 | Medición de rendimiento (RNF-08) | Locust, en Python |
| 4 | Umbral de cobertura | Ninguno; Coverage.py informativa y revisión de módulos críticos |
| 5 | Restauración | El solicitante, trimestral a mano más comprobación automática mensual; registro en el repositorio |
| 6 | Segunda mitad de RN-15 | Prueba ahora sin CA; CA en la próxima ERS |
| 7 | Qué puede quedar sin probar | Nada de prioridad alta; media con aceptación escrita; baja diferible |

**Pendientes:**
- Probar que Locust reporta el percentil 95 o calcularlo en Python.
- Escribir y probar el script de comprobación mensual de restauración.
- Elegir la herramienta de cifrado de los respaldos (ADR-024).
- Compatibilidad de Selenium con los navegadores y la versión de Python elegidos.
- Quién revisa estas pruebas: hoy el solicitante ocupa los tres roles (DP-23).
## 12. Condiciones para aprobar esta estrategia

- Aprobar la ERS v1.9 y el DAS v0.11.
- Resolver los pendientes de la sección 11.
- Revisión por otra persona distinta del autor (hoy el solicitante ocupa los tres roles, DP-23).
- Incorporar el dictamen del abogado en los CA marcados (L).

## Registro de aprobación

| Rol | Nombre | Resultado | Fecha |
|---|---|---|---|
| Responsable del negocio | Pendiente | Pendiente | Pendiente |
| Responsable técnico | Pendiente | Pendiente | Pendiente |
| Responsable de pruebas | Pendiente | Pendiente | Pendiente |

**Fin del documento — EPP-SGA-001, versión 0.2 (borrador no aprobado).**
