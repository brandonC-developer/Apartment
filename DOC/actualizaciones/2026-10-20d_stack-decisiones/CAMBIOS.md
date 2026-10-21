# Actualización 2026-10-20 (d) — DAS v0.9: decisiones del stack

**Fecha:** 20 de octubre de 2026
**Documentos afectados:** [DAS v0.9](../../fase-2-arquitectura/DAS_SGA_001_v0.9_borrador.md) (nuevo) y los README de las fases 2, 3, 5 y 6 y de `DOC/`.
**Versión anterior:** [DAS v0.8](../../fase-2-arquitectura/DAS_SGA_001_v0.8_borrador.md), que se conserva sin cambios.
**Estado:** borrador; no aprobado.

## 1. Motivo
Ronda de siete preguntas sobre el stack tecnológico, planteadas una por una por el asistente con investigación previa y recomendación. Las preguntas 1 (lenguaje y framework) y 3 (interfaz y API) se registraron en la [actualización 2026-10-20 (c)](../2026-10-20c_DAS-v0.8-Django/CAMBIOS.md); esta incorpora las demás.

## 2. Cambios
| ID | Tipo | Descripción | Origen |
|---|---|---|---|
| T1 | modificado | ADR-002: PostgreSQL 18 | Pregunta 2 (tabla de la sección 4) |
| T2 | modificado | ADR-013: temporizador de systemd con comando de Django | Pregunta 4 |
| T3 | modificado | ADR-003: documentos privados en disco, fuera de la raíz web, servidos por Django | Pregunta 5 |
| T4 | añadido | ADR-023: alojamiento en DigitalOcean, Ubuntu 26.04 LTS, Nginx, Certbot y Gunicorn bajo systemd, sin contenedores | Preguntas 6a y 6b |
| T5 | añadido | ADR-024: respaldos diarios cifrados a Spaces más respaldo semanal del Droplet | Pregunta 7a |
| T6 | añadido | ADR-025: integración continua con GitHub Actions | Pregunta 7b |
| T7 | modificado | RE-03 (proveedor), RE-04 (motor), sección 11 (respaldos de DigitalOcean), sección 5, referencias 20 a 25 y anexo A | Consecuencia de las anteriores |
| T8 | modificado | README de las fases 2, 3, 5 y 6 y de `DOC/` apuntan al DAS v0.9 | Regla 3 de `CLAUDE.md` |

## 3. Impacto
- **Arquitectura:** el stack queda fijado salvo versiones, tamaño del Droplet, región y dominio.
- **ERS:** sin cambios.
- **Legal:** DigitalOcean no tiene centros de datos en Latinoamérica; aplica DP-19 (transferencia de datos personales), pendiente de abogado.
- **Pruebas (fase 4):** hay que probar la regla de ciclo de vida de Spaces, la restauración y la ejecución del temporizador con zona horaria.

## 4. Decisiones del solicitante (pregunta → respuesta)
En todos los casos la opción elegida fue la que recomendó el asistente; las preguntas, opciones y fuentes están en la tabla.
## Tabla de decisiones (sección 4)
| # | Pregunta | Respuesta | Fecha | Fuentes y validación |
|---|---|---|---|---|
| 2 | Motor de base de datos | "confirma PostgreSQL 18" (PostgreSQL 18; recomendación del asistente) | 20-oct-2026 | Política de versiones de PostgreSQL, leída por resumen: la 18 recibe soporte hasta el 14-nov-2030; la 14 termina el 12-nov-2026. Prueba desechable del 17-oct-2026 en 18.4 (ver ADR-002). Resuelve el "motor pendiente" de ADR-002; migraciones y respaldos siguen pendientes. |
| 4 | Tareas programadas (proceso diario de las 07:00) | Temporizador de systemd + comando de Django (opción recomendada) | 20-oct-2026 | Documentación de systemd (`Persistent=` y zona IANA en OnCalendar) y de Django (comandos de gestión ejecutables desde cron o un programador), leídas por resumen; Celery exige un intermediario de mensajes (Redis o RabbitMQ), por resumen. Django USE_TZ y zoneinfo, por resumen. La versión mínima de systemd con zona en la hora no se verificó. |
| 5 | Archivos privados (cédulas y documentos) | Disco del servidor, fuera de la raíz web, servido por Django tras comprobar permisos (opción recomendada) | 20-oct-2026 | OWASP File Upload Cheat Sheet (almacenar fuera de la raíz web, nombre aleatorio, mínimos permisos, autorización en la descarga, no confiar en el Content-Type) y documentación de Django (FileResponse; contenido subido por usuarios, límite de tamaño en el servidor web y lista blanca de extensiones), leídas por resumen. Django recomienda servir los archivos subidos desde un dominio distinto, pero eso aplica a archivos públicos; aquí se entregan solo por una vista con autorización. Cifrado en reposo y análisis antivirus no se decidieron. |
| 6a | Proveedor de alojamiento | "usaremos esa plataforma" (DigitalOcean) | 20-oct-2026 | Documentación de DigitalOcean (Droplets, regiones, precios, Cloud Firewalls, imágenes), leída por resumen; ver la investigación de la sesión en la sección siguiente. Tamaño del Droplet y región **no decididos**. Los centros de datos están en Estados Unidos, Canadá, Europa y Asia-Pacífico, no en Latinoamérica: aplica DP-19 (transferencia de datos), pendiente de abogado. |
| 6b | Servidor: sistema, proxy con HTTPS y servidor de aplicaciones | Ubuntu 26.04 LTS + Nginx + Certbot + Gunicorn bajo systemd, sin contenedores, en DigitalOcean (opción recomendada) | 20-oct-2026 | Lista de imágenes de DigitalOcean (26.04 LTS disponible; nota de lanzamiento solo por resultados de búsqueda), Cloud Firewalls (sin costo adicional), guía de despliegue de Gunicorn (proxy que amortigüe clientes lentos; sugiere Nginx), Certbot (renovación automática, `--dry-run`) y Caddy (no amortigua peticiones por defecto), todo por resumen. No verificado: versión de Python de Ubuntu 26.04 y compatibilidad con Django, si el Cloud Firewall reemplaza a `ufw`, y los comandos de las guías de DigitalOcean para la 26.04. Tamaño del Droplet y región no decididos. |
| 7a | Respaldos | `pg_dump` diario cifrado a Spaces + respaldo semanal del Droplet (opción recomendada) | 20-oct-2026 | Documentación de PostgreSQL sobre `pg_dump` (copias consistentes; roles con `pg_dumpall`; advierte que fuera de casos simples no es lo indicado para respaldos regulares de producción), por resumen; reglas de ciclo de vida de Spaces, solo resultados de búsqueda (con reportes antiguos de usuarios sobre borrado que no siempre funcionaba: hay que probarlo); respaldos del Droplet de DigitalOcean, resultados de búsqueda. **No verificado:** cifrado en reposo de Spaces (la página dio 404); herramienta de cifrado por elegir. |
| 7b | Integración continua | GitHub Actions con pruebas, `check --deploy` y migraciones (opción recomendada) | 20-oct-2026 | Facturación de GitHub Actions (2.000 minutos al mes en repositorios privados del plan gratis), solo resultados de búsqueda; no se verificó la visibilidad del repositorio. |

## 5. Pendientes
- Tamaño del Droplet, región, nombre de dominio y endurecimiento del servidor.
- Versión de Django y de Python, y su compatibilidad con Ubuntu 26.04.
- Herramienta y custodia de las claves de cifrado de los respaldos, y prueba de que la regla de ciclo de vida borra a los 35 días.
- Cifrado en reposo y análisis antivirus de los documentos privados.
- Visibilidad del repositorio de GitHub.
- DP-19 y DP-17 a DP-21: abogado.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`. La investigación se leyó por resumen (la herramienta devuelve un resumen del texto, no el texto completo); en cada fila se indica qué se leyó y qué quedó solo como resultado de búsqueda o no se pudo abrir. Revisión de pares: no realizada. Los precios de DigitalOcean no traen fecha de publicación: se consultaron el 20-oct-2026 y hay que volver a verificarlos al contratar.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | brandonC-developer | Pendiente | Pendiente |