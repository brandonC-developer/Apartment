# Actualización 2026-10-24 (a) — Comandos de creación y rescate de la cuenta

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/cuentas/management/commands/`](../../../src/cuentas/management/commands/crear_administrador.py), [`src/cuentas/tests.py`](../../../src/cuentas/tests.py), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS v1.16, RF-27 («creación y rescate por el servidor»); instrucción del solicitante: «sí, escribe el comando de creación y rescate» (24-oct-2026)
**Estado:** implementado y probado en un PostgreSQL desechable; no aprobado

## 1. Qué se escribió
| Comando | Qué hace |
|---|---|
| `crear_administrador --usuario X` | Pide la contraseña dos veces por teclado (nunca como argumento), la valida con los validadores (mínimo 15 caracteres) y crea la única cuenta con el segundo factor sin registrar. Falla si ya existe una cuenta (RN-25) |
| `rescatar_segundo_factor [--confirmar]` | Pide escribir `RESCATAR`; desactiva el segundo factor, borra el secreto y los códigos de recuperación, reinicia el contador de intentos y **cierra todas las sesiones**. No cambia la contraseña |

Pruebas: 5 nuevas; en total **56 pasan** en un PostgreSQL 18 desechable (ya borrado), Python 3.12 en Windows. Mutación manual: quitar el cierre de sesiones hizo fallar su prueba; se restauró.

## 2. Propuestas del asistente (sin aprobar)
- Reiniciar el contador de intentos y cerrar **todas** las sesiones al rescatar (la ERS no lo dice).
- Confirmación escrita `RESCATAR`, con `--confirmar` para scripts.
- El rescate no cambia la contraseña; si también se perdió, falta el restablecimiento por correo.

## 3. Qué no está hecho
- **Registro del segundo factor en el primer ingreso** (RF-27: «el segundo factor se activa en el primer ingreso»): sin esa pantalla, **la cuenta creada no puede iniciar sesión**, porque la vista exige el segundo factor activo. Es lo siguiente.
- **Constancia en la auditoría y aviso a las dos direcciones** del rescate (RF-27): no hay modelo de auditoría ni envío de correo; el comando lo advierte y pide registrarlo a mano.
- Cambio y restablecimiento de contraseña, otros avisos de seguridad, roles de PostgreSQL, despliegue en WSL, respaldo y CI. 0 de 8 CA de la E0 cumplidos.

## 4. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
