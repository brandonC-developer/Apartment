# Actualización 2026-10-21 (p) — ADR-029: gestión de las conexiones a la base de datos

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado):** [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md) (ADR-029 nuevo, anexo A, referencia 31), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md) (pendientes) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Decisión
| # | Pregunta | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | ¿Cómo gestiona Django las conexiones a PostgreSQL? | Valor por defecto: una conexión por petición (`CONN_MAX_AGE = 0`), sin pool | Igual |

**Fuente (por resumen, 21-oct-2026):** Django, bases de datos (`CONN_MAX_AGE`, `CONN_HEALTH_CHECKS`, pool de PostgreSQL).

## 2. Cambios
- DAS v0.11: ADR-029, anexo A y referencia 31.
- Estrategia de pruebas v0.3: la medición con Locust incluye el efecto de abrir una conexión por petición.

## 3. Límites
- No se pudo abrir la página de diseño de Gunicorn (redirigió y dio 404): el número de procesos queda para la fase 6, sin fuente.
- Que abrir una conexión local sea barato y que el límite de 100 conexiones de PostgreSQL sobre son afirmaciones del asistente, sin medir ni verificar hoy.
- La versión de Django desde la que existe la opción `pool` no se confirmó.

## 4. Quedan por revisar (puntos 1 y 6)
Esquema físico y migraciones; módulos del DAS como aplicaciones de Django. El punto 3 (roles) y el 5 (identificadores) están resueltos.

## 5. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.