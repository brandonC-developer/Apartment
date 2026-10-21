# Estrategia y plan de pruebas

**Identificador:** EPP-SGA-001
**Versión:** 0.1
**Estado:** Borrador para revisión; no aprobado
**Fecha:** 20 de octubre de 2026
**ERS de referencia:** ERS-SGA-001 v1.8 (borrador no aprobado)
**DAS de referencia:** DAS-SGA-001 v0.9 (borrador no aprobado)

Este documento propone cómo demostrar que cada requisito del SGA funciona. **No hay código ni se ha autorizado implementarlo**: todo lo que sigue es un diseño de pruebas, no resultados. Lo que proviene de una fuente se indica con ella; lo demás es **propuesta** del asistente y espera decisión del solicitante (sección 11). No es asesoría legal: los criterios de aceptación que dependen de las leyes 7527 y 8968 son provisionales hasta que un abogado valide las obligaciones (DP-17).

## 1. Alcance

| Incluido | Fuera de alcance de este documento |
|---|---|
| Pruebas de los 57 criterios de aceptación (CA-01 a CA-57) | Casos de prueba detallados (se escriben con la implementación) |
| Verificación de los RNF sin criterio de aceptación (RNF-05, 07, 08, 09, 10, 11) | Pruebas de penetración por un tercero |
| Pruebas de operación: restauración, temporizador, HTTPS y respaldos | Pruebas del proyecto de WhatsApp (DP-04, diferido): solo se prueba la interfaz de canal |
| Datos de prueba y entornos | Cualquier dato personal real |

## 2. Fundamento metodológico y fuentes

| Fuente | Qué respalda | Cómo se validó | Limitaciones |
|---|---|---|---|
| [Vocke, *The Practical Test Pyramid* (martinfowler.com, 26-feb-2018)](https://martinfowler.com/articles/practical-test-pyramid.html) | Muchas pruebas unitarias rápidas, menos de integración y muy pocas de extremo a extremo; evitar la pirámide invertida | Leída por resumen | Artículo de un autor sobre su experiencia, no un estudio empírico |
| [Django, visión general de pruebas](https://docs.djangoproject.com/en/stable/topics/testing/overview/) | `TestCase` envuelve cada prueba en una transacción; `TransactionTestCase` confirma de verdad; pruebas con base de datos de prueba; ejecución en paralelo; `DEBUG = False` en pruebas; `--shuffle` para detectar dependencias de orden | Leída por resumen | No trata PostgreSQL en una sección propia |
| [Django, herramientas de pruebas](https://docs.djangoproject.com/en/stable/topics/testing/tools/) | Cliente de pruebas con `enforce_csrf_checks`; `override_settings`; buzón de correo en memoria; `assertNumQueries` | Leída por resumen, hasta el carácter 100.000 de 113.245 | El resumen no cubrió cómo probar código dependiente del tiempo |
| [OWASP, Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) | Existe una guía de pruebas de seguridad web, versión estable 4.2 (5.0 en desarrollo) | Solo la página de presentación | **No se leyeron sus categorías ni sus casos**; aquí solo se usa como referencia futura |
| ISO/IEC/IEEE 29119-3 (documentación de pruebas) | La evaluación metodológica del proyecto la propone como base de esta fase | **No se pudo abrir** ([página de ISO](https://www.iso.org/standard/79429.html), error 403) | No se afirma nada sobre su contenido; la estructura de este documento es propia |

La proporción de la pirámide es una orientación del autor, no una regla medida. No encontré estudios universitarios sobre estrategias de pruebas para sistemas de saldos y comprobantes.

## 3. Niveles de prueba (propuesta)

| Nivel | Qué prueba | Herramienta (propuesta) | Base de datos |
|---|---|---|---|
| Unitarias | Reglas puras: períodos por aniversario, prorrateo, reajuste, saldos, estados derivados, plazos de cinco días hábiles | Ejecutor de pruebas de Django | Ninguna |
| Integración | Restricciones de PostgreSQL (contratos solapados, unicidad contrato-período, comprobantes sin huecos, clave de solicitud), transacciones y el comando diario | `TestCase` de Django | **PostgreSQL 18**, no SQLite: `ExclusionConstraint` es de PostgreSQL |
| Concurrencia | Contador de comprobantes y envío repetido de un abono | `TransactionTestCase` (confirma de verdad) | PostgreSQL 18 |
| Vistas y permisos | Acceso denegado, CSRF, sesión, descarga de documentos privados | Cliente de pruebas con `enforce_csrf_checks=True` | PostgreSQL 18 |
| Extremo a extremo | Pocos recorridos críticos en navegador (registrar pago y emitir comprobante; alta de contrato) | Por elegir (no investigada) | PostgreSQL 18 |
| No funcionales y de operación | Rendimiento, compatibilidad, restauración, temporizador, HTTPS | Ver sección 7 | Entorno de prueba |

Notas de diseño:
- Las pruebas usan **la misma versión de PostgreSQL que producción** (18), porque ADR-002 depende de funciones propias de PostgreSQL.
- Django ejecuta las pruebas con `DEBUG = False`. Para acelerarlas permite un hasher de contraseñas rápido; por eso debe existir además **una prueba con Argon2id y los parámetros del ADR-019**, que no use ese atajo.
- El tiempo se controla fijando la hora actual en las pruebas. La técnica concreta (parchear `timezone.now` o una biblioteca) **no está respaldada por la documentación de Django que leí**; es práctica común y queda por decidir.
- Para detectar dependencias ocultas entre pruebas, Django ofrece `--shuffle` (fuente: visión general).

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
| | CA-37 (L), 38 | Integración; concurrencia (comprobantes consecutivos) | Alta |
| Cambios de condiciones | CA-12, 39, 22, 40 | Unitarias (fecha efectiva, tope, bloqueo por abonos); integración | Alta |
| Calendario | CA-06, 07 | Vistas | Baja |
| Notificaciones | CA-08, 41, 05, 42, 43, 44 | Integración (buzón en memoria, comando diario) | Media |
| | CA-09 | Integración (canal simulado que falla) | Media |
| Depósito | CA-15, 16, 17, 23, 45, 46 | Unitarias; integración | Media |
| Seguridad y configuración | CA-13, 47, 48 | Vistas y permisos | Alta |
| | CA-18 | Unitarias; operación (zona horaria del temporizador) | Media |
| | CA-10 | Integración | Alta |
| | CA-56, 57 (L) | Unitarias (plazo); integración | Alta |
| | CA-52, 54 | Concurrencia | Alta |
| | CA-53 | Integración (auditoría) | Alta |
| | CA-55, 49 | Unitarias; integración | Alta |

Recuento: 57 de 57 CA asignados (7 + 7 + 12 + 4 + 2 + 7 + 6 + 12 por área de la sección 9 de la ERS).

## 6. Requisitos sin criterio de aceptación

Origen: matriz de trazabilidad de la ERS v1.8 (sección 10; ver la [actualización 2026-10-20 (b)](../actualizaciones/2026-10-20b_ERS-v1.8-matriz/CAMBIOS.md)).

| Requisito | Cómo se verificaría (propuesta) | Cuándo |
|---|---|---|
| RNF-05 Un fallo de WhatsApp no bloquea nada | Prueba de integración con un canal simulado que falla: la notificación web se conserva y el registro de movimientos sigue funcionando (CA-09 cubre parte) | Automatizada |
| RNF-07 Validación y mensajes comprensibles | Pruebas de formularios con entradas inválidas; revisión manual de los mensajes | Automatizada y manual |
| RNF-08 Consultas en menos de 2 s en el percentil 95 | Medición con datos sintéticos de 50 propiedades; herramienta de carga por elegir. La ERS lo llama "objetivo a validar" | Antes de producción |
| RNF-09 Respaldo y recuperación | Restauración en un Droplet temporal desde la copia cifrada de Spaces: medir el tiempo (RTO de 24 h), comprobar contenido de contratos, movimientos, comprobantes y fotografías; comprobar que se borra a los 35 días | Antes de producción y cada 3 meses |
| RNF-10 Navegadores | Recorridos críticos en las dos últimas versiones mayores de Chrome, Edge, Firefox y Safari, en escritorio y móvil; manual o con la herramienta de extremo a extremo | Antes de producción |
| RNF-11 Separación de responsabilidades | Revisión de diseño (dependencias entre módulos); no es una prueba automática | En la revisión de código |

## 7. Pruebas no funcionales y de operación (propuesta)

| Tema | Prueba | Fuente / estado |
|---|---|---|
| HTTPS | `certbot renew --dry-run` en el servidor de prueba | [Certbot](https://eff-certbot.readthedocs.io/en/stable/using.html#automated-renewals), leída por resumen |
| Configuración de producción | `manage.py check --deploy` en la integración continua | [Django, lista de despliegue](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/), leída por resumen |
| Temporizador diario | Ejecutarlo en el Droplet de prueba: con el servidor apagado a la hora, debe recuperarse (`Persistent=yes`); comprobar la hora local en `America/Costa_Rica` y que una segunda ejecución no duplique (RNF-16) | [systemd](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html), por resumen; versión mínima de systemd **no verificada** |
| Respaldo y borrado a 35 días | Regla de ciclo de vida de Spaces con una retención corta primero, para ver si borra | Solo resultados de búsqueda; hay reportes antiguos de que no siempre borraba |
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
- **Umbral de cobertura de código:** **sin definir** (sección 11). No se propone un porcentaje: no encontré fuente que respalde uno para este tipo de sistema.

## 10. Hallazgos de esta estrategia

| ID | Hallazgo | Propuesta |
|---|---|---|
| HP-01 | La segunda mitad de RN-15 (rechazar movimientos sobre períodos que aún no inician, salvo el inmediato siguiente) no tiene criterio de aceptación | Decidir si se añade un CA en la próxima versión de la ERS; hasta entonces, un caso de prueba marcado como "sin CA" |
| HP-02 | Los CA no citan los requisitos que verifican; la trazabilidad solo está en la matriz de la ERS | Al escribir los casos de prueba, cada uno cita su CA y sus RF, RN y RNF |
| HP-03 | El script de coherencia no revisa este documento ni que cada requisito esté en la matriz | Ampliar el script cuando se apruebe el documento |
| HP-04 | Los CA marcados (L) tienen resultado esperado provisional | Revisar con el dictamen del abogado |

HP-nn es un identificador local de este documento, no de la lista compartida del proyecto.

## 11. Decisiones pendientes del solicitante

1. Ejecutor de pruebas: el de Django (`unittest`, el predeterminado) o `pytest` (no investigado).
2. Herramienta de pruebas de extremo a extremo y de carga (no investigadas).
3. Umbral de cobertura de código, si se desea alguno.
4. Quién ejecuta la restauración trimestral y dónde se registra su resultado.
5. Si se añade un CA para la segunda mitad de RN-15 (HP-01).
6. Qué prioridad se acepta que quede sin probar antes de producción, si el tiempo lo exige.

## 12. Condiciones para aprobar esta estrategia

- Aprobar la ERS v1.8 y el DAS v0.9.
- Resolver la sección 11.
- Revisión por otra persona distinta del autor (hoy el solicitante ocupa los tres roles, DP-23).
- Incorporar el dictamen del abogado en los CA marcados (L).

## Registro de aprobación

| Rol | Nombre | Resultado | Fecha |
|---|---|---|---|
| Responsable del negocio | Pendiente | Pendiente | Pendiente |
| Responsable técnico | Pendiente | Pendiente | Pendiente |
| Responsable de pruebas | Pendiente | Pendiente | Pendiente |

**Fin del documento — EPP-SGA-001, versión 0.1 (borrador no aprobado).**
