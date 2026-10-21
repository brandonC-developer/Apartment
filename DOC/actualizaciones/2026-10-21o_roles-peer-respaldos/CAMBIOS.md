# Actualización 2026-10-21 (o) — Punto 3: roles de base de datos, `peer` y respaldos

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado):** [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md) (ADR-027, ADR-024, sección 9, anexo A, referencia 30) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Decisión
| # | Pregunta | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | ¿Cómo se definen los roles de base de datos y dónde viven sus credenciales? | Tres roles (dueño, aplicación, respaldos de solo lectura) con autenticación `peer` por el socket Unix local, sin contraseñas de base de datos | Igual |

**Fuentes (por resumen, 21-oct-2026):** PostgreSQL, roles predefinidos (`pg_read_all_data`); PostgreSQL, autenticación `peer`; PostgreSQL, `pg_dumpall`.

## 2. Cambios
- ADR-027: tercer rol, `peer` y fuentes; el secreto del rol dueño deja de ser un pendiente (no hay secreto).
- ADR-024: el respaldo usa el rol de solo lectura y `pg_dumpall --globals-only --no-role-passwords`.
- Sección 9, anexo A y referencia 30.

## 3. Límites y puntos sin verificar
- Que `pg_dumpall --globals-only --no-role-passwords` funcione sin superusuario: la página no lo confirma; se prueba antes de producción, con el usuario `postgres` del sistema por `peer` como alternativa.
- La versión en que apareció `pg_read_all_data` (de memoria, la 14) y el uso de `sudo -u` para las migraciones no están verificados.
- La decisión solo vale mientras la base esté en el mismo Droplet; si se separa, se revisa.
- Los nombres de roles y usuarios del sistema son propuesta del asistente.

## 4. Efecto sobre los otros puntos
Adelanta parte del punto 4 (conexión: socket local por `peer`, sin cifrado de red porque no hay red). Quedan por revisar el punto 1 (esquema físico y migraciones), el 4 (gestión de conexiones) y el 6 (módulos como aplicaciones de Django).

## 5. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.