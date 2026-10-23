# Actualización 2026-10-23 (zb) — BR-04: actualización de las dependencias de Python

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el DAS (ADR-022 y ADR-025), el modelo de amenazas (versión nueva), el plan de implementación y el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** brecha BR-04 y amenaza AM-16 del [modelo de amenazas v0.1](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.1_borrador.md); pendiente del ADR-022 ("forma de instalar Django"). Sigue a la [BR-03](../2026-10-23za_br-03-respaldos-clave-spaces/CAMBIOS.md)
**Estado:** decisiones registradas; documentos sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Cómo se instalan Django y las demás dependencias de Python? | "pip en un entorno virtual con versiones fijadas" (recomendada por el asistente) | `pip` en un entorno virtual, con versiones exactas fijadas en un archivo de dependencias del repositorio; las mismas versiones en la etapa A (WSL) y en el Droplet. No se usan los paquetes de Ubuntu para Django. Cierra el pendiente del ADR-022 |
| 2 | ¿En cuánto tiempo se aplican las correcciones de seguridad? | "Alta: 3 días; moderada o baja: 14 días; resto: revisión mensual" (recomendada) | Seguridad alta (según la clasificación de Django): en cuanto salga y dentro de 3 días; moderada o baja: dentro de 14 días; las demás dependencias: revisión mensual. Antes de desplegar, pruebas y `check --deploy` (ADR-025). Un parche de seguridad es una versión de parche de la serie vigente, sin saltar de serie |
| 3 | ¿Cómo te enteras de una vulnerabilidad? | "django-announce + pip-audit en la integración continua + alertas de Dependabot" (recomendada) | Suscripción a django-announce con la dirección dedicada de proveedores (BR-01); `pip-audit` en la integración continua contra las dependencias fijadas (falla si hay vulnerabilidades conocidas); alertas de Dependabot de GitHub con correo a esa dirección |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Django, política de seguridad: https://docs.djangoproject.com/en/5.2/internals/security/ | Documentación oficial | Leída por resumen (WebFetch, 23-oct-2026) | Las dos series más recientes y las LTS reciben correcciones; parches publicados en PyPI y en el sitio el día de la divulgación; aviso previo de una semana en django-announce (fecha y gravedad, sin detalles); clasificación de severidad (alta: RCE e inyección SQL; moderada: XSS, CSRF, DoS, autenticación rota; baja: exposición de datos sensibles, sesiones); objetivo de resolución del proyecto de 90 días | El resultado de la herramienta traía **instrucciones dirigidas a un asistente de IA** (cerrar con un párrafo sobre el sentido de la vida); no se siguieron ni afectan a lo citado. Los plazos de 3 y 14 días son del asistente y no vienen de la página |
| pip-audit: https://github.com/pypa/pip-audit | Herramienta de la PyPA | Leída por resumen (23-oct-2026) | Busca vulnerabilidades conocidas en entornos y archivos de requisitos; usa la Python Packaging Advisory Database vía la API de PyPI; GitHub Action oficial; código de salida distinto de 0 si hay vulnerabilidades | No es un análisis de código ni protege contra paquetes maliciosos; no cubre bibliotecas nativas; puede mostrar avisos que no aplican |
| GitHub, alertas de Dependabot: https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts | Documentación del proveedor | Leída por resumen (23-oct-2026) | Alertas desde la GitHub Advisory Database; notificación por correo a quien tiene permisos y sigue el repositorio con notificaciones de seguridad; solo las advisories revisadas por GitHub generan alertas | **No dice si están disponibles sin costo para repositorios privados** |
| Ubuntu, mantenimiento de seguridad (ESM): https://ubuntu.com/security/esm | Documentación del proveedor | **Solo resultados de búsqueda** (23-oct-2026) | `universe`: cinco años de correcciones de la comunidad, "best-effort"; Pro (`esm-apps`): diez años de correcciones de Canonical para críticas y altas; gratis para uso personal en hasta 5 máquinas | **No se confirmó** si el paquete de Django de Ubuntu 26.04 está en `main` o en `universe`, ni su versión ni su retraso |
| DAS v0.12, ADR-022 y ADR-025 | Documento del proyecto | Releído | Django 5.2 LTS con Python 3.14 del sistema; Django con `pip` en un entorno virtual como propuesta sin decidir; integración continua con `check --deploy` | — |

## 3. Lo que propone el asistente y el solicitante no decidió
- Los plazos de 3 y 14 días y la revisión mensual: criterio del asistente, sin fuente.
- Que la ausencia del solicitante (DP-23) no tiene remedio: nadie más puede aplicar el parche.
- Que los avisos lleguen a la dirección dedicada de proveedores: coherencia con BR-01, no una fuente.

## 4. Qué no se hizo
- No se creó el archivo de dependencias, el entorno virtual, la integración continua ni las suscripciones; es etapa A y B.
- No se confirmó que Dependabot sea gratuito para el repositorio privado ni que el repositorio sea privado.
- No se midió cuánto tarda Ubuntu en publicar una corrección de Django, ni qué versión trae 26.04.
- `pip-audit` y Dependabot no detectan paquetes maliciosos ni la cadena de construcción, que sigue **fuera del modelo de amenazas v0.1**.
- No se definió el archivo de bloqueo con hashes (`--require-hashes`) ni quién actualiza las demás dependencias entre revisiones mensuales.

## 5. Qué falta hacer
1. DAS: cerrar el pendiente del ADR-022 y añadir a ADR-025 el uso de `pip-audit` (versión nueva o ajuste consolidado).
2. Modelo de amenazas v0.2: BR-04 cerrada; AM-16 con su nueva respuesta y riesgo residual.
3. Plan de implementación: tarea para crear el archivo de dependencias fijadas y el trabajo de `pip-audit`.
4. Fase 6: procedimiento de actualización con los plazos.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
