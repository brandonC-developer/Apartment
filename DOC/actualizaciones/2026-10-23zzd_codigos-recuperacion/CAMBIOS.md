# Actualización 2026-10-23 (zzd) — Códigos de recuperación

**Fecha:** 2026-10-23
**Documentos afectados:** código en [`src/cuentas/`](../../../src/cuentas/autenticacion.py), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS v1.16, RF-27 y CA-69 (10 códigos de un solo uso, con hash, mostrados una vez; emitir nuevos exige la contraseña actual e invalida los anteriores; límite de intentos compartido); instrucción del solicitante: «continue» (24-oct-2026) tras ofrecer este paso
**Estado:** implementado y probado en un PostgreSQL desechable; no aprobado

## 1. Qué se escribió
| Archivo | Contenido |
|---|---|
| `cuentas/models.py` | `CodigoRecuperacion` (`administrador`, `hash_codigo` único, `usado_en`, `creado_en`), según el MDD v0.7 |
| `cuentas/migrations/0002_codigorecuperacion.py` | Tabla |
| `cuentas/autenticacion.py` | `emitir_codigos_recuperacion` (exige la contraseña, borra los anteriores, devuelve 10 en claro una sola vez) y `verificar_codigo_recuperacion` (comparte el contador y la espera; uno correcto se marca usado y reinicia el contador) |
| `cuentas/tests.py` | 6 pruebas nuevas; en total 38 con las anteriores |

## 2. Qué decidió el asistente (propuesta, sin aprobar)
La ERS fija la cantidad y las reglas, no el formato. Propuesto: 10 caracteres de un alfabeto de 31 sin caracteres confusos (sin 0, O, 1, I, L), unos 49 bits, mostrados como `XXXXX-XXXXX`; se aceptan minúsculas, espacios y sin guion; hash SHA-256 del código normalizado (no Argon2, porque el código es aleatorio y de alta entropía, y el límite de intentos acota las pruebas). Emitir de nuevo **borra** los anteriores en lugar de marcarlos.

## 3. Verificación
- **38 pruebas pasan** contra PostgreSQL 18 (clúster desechable en el puerto 54329, ya borrado), Python 3.12 en Windows.
- Se prueba: 10 códigos distintos y solo hashes guardados, contraseña exigida, un solo uso, normalización, invalidación al emitir de nuevo, contador y espera compartidos.
- Sin prueba de concurrencia real.

## 4. Qué no está hecho
Vista de inicio de sesión de dos pasos y sesión (CA-48), comando de creación y rescate, activación del segundo factor, aviso de seguridad por correo (la función solo lo indica), auditoría, roles de PostgreSQL, despliegue en WSL, respaldo y CI. 0 de 8 CA de la E0 cumplidos.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
