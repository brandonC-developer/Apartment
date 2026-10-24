# Actualización 2026-10-24 (e) — Auditoría base

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/nucleo/`](../../../src/nucleo/models.py) y [`src/cuentas/`](../../../src/cuentas/views.py), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS v1.16, RF-28 y RNF-06 (auditoría y su consulta), CA-53, CA-71, CA-68, CA-70; modelo de datos v0.7 (entidad AUDITORIA, R12, R14, R19); ADR-027; plan, HI-01 y HI-05; instrucción del solicitante: «sí, escribe la auditoría base» (24-oct-2026)
**Estado:** implementado y probado en un PostgreSQL desechable; no aprobado

## 1. Qué se escribió
| Archivo | Contenido |
|---|---|
| `nucleo/models.py` | `Auditoria` con los campos del MDD; solo inserción (`save` de una fila existente, `delete`, y `update()`/`delete()` masivos lanzan `RegistroInmutable`); restricción R19 en la base |
| `nucleo/auditoria.py` | `registrar` (de los campos personales y secretos solo conserva el nombre), `ip_de_origen` y los eventos de seguridad para la alerta |
| `nucleo/views.py`, `urls.py`, plantilla | `/auditoria/`: solo lectura, con filtros por fecha, tipo de evento, entidad y actor, y paginación; exige sesión |
| `cuentas/views.py` | Auditoría de `inicio_sesion`, `inicio_sesion_fallido`, `cierre_sesion`, `codigo_recuperacion_usado`, `codigos_emitidos`, `segundo_factor_registrado` y `cinco_fallos_seguidos`; la pantalla de inicio muestra los avisos de seguridad desde el inicio de sesión anterior |
| Comandos | `cuenta_creada` y `segundo_factor_rescatado` (constancia de CA-70) |
| `sga/settings.py` | `IP_ORIGEN_CABECERA` |
| Migración `nucleo/0001_initial.py` | Tabla y restricción |

## 2. Propuestas del asistente (sin aprobar)
- **Qué se registra de un fallo:** un solo tipo, `inicio_sesion_fallido`, para cualquier paso (contraseña, TOTP, código de recuperación, token o código de registro); no se distingue el paso, para no dar pistas. **No se guarda lo escrito en el campo de usuario** (puede ser una contraseña): el actor es `anonimo` en el primer paso y el usuario de la cuenta en los pasos siguientes.
- **Un intento hecho durante la espera no se registra**, para no inflar una tabla que no se borra; la defensa contra ese abuso es el límite de Nginx (ADR-032, decisión 11).
- **Actor de los comandos:** `servidor` (el solicitante ejecuta el comando; el MDD solo prevé administrador o proceso).
- **Lista de campos personales** (`nombre_completo`, `numero_documento`, `tipo_documento`, `telefono`, `correo`, `correo_electronico`, `imagen_cedula`, `fotografia`, `archivo`) y de secretos: sale de RF-28, pero la lista concreta es mía y se revisa con cada módulo nuevo.
- **Alerta web:** los eventos de seguridad posteriores al inicio de sesión anterior; no requiere guardar «leído».
- **Sin clave foránea** a la organización (el MDD no la incluye en los campos) ni a la ejecución del proceso (llega en la E2).
- **IP:** se confía en `X-Real-IP` solo cuando la configuración lo declara; Nginx debe sobrescribirla (`proxy_set_header X-Real-IP $remote_addr;`), cosa **no verificada** porque Nginx aún no está desplegado.
- La escritura de la auditoría no va en la misma transacción que el contador de intentos: hay una ventana mínima en la que un fallo podría contarse sin quedar registrado.
- Se quitó el aviso provisional en el registro del servidor de la actualización 2026-10-24d; lo reemplaza la auditoría.

## 3. Verificación
- **100 pruebas pasan** (22 nuevas de auditoría y 1 reemplazada) en PostgreSQL 18 desechable (ya borrado), Python 3.12 en Windows.
- Se prueba: CA-53 (teléfono sin valor, importe con valores), inmutabilidad, R19, IP de origen con y sin cabecera de confianza, CA-71 (fallo y acierto con fecha, hora e IP; sin contraseñas, códigos, tokens ni lo escrito en el usuario), consulta de solo lectura que no genera registros, filtros, paginación, cierre de sesión, código de recuperación, cinco fallos (un solo evento) y alerta de inicio, registro del segundo factor y comandos.
- **Mutaciones manuales:** guardar valores de campos personales, permitir editar, confiar siempre en la cabecera del cliente y guardar lo escrito en el usuario hicieron fallar sus pruebas; se restauró el código.
- Error mío en la escritura de las pruebas, corregido antes de la primera corrida: varios inicios en el mismo intervalo de 30 s fallaban por el rechazo de reutilización (correcto); la prueba reinicia el último intervalo.

## 4. Qué no está hecho
- **El rol de PostgreSQL de la aplicación solo con `SELECT` e `INSERT` sobre la auditoría** (ADR-027) y su prueba: dependen de los roles y del archivo de privilegios (sección E de la lista de tareas).
- Eventos de cambio y restablecimiento de contraseña y de cambio de correo (E4), emisión de códigos nuevos desde la sesión (pantalla pendiente), aviso por correo (E4) y alerta persistente por aviso fallido.
- Auditoría de los cambios de otras entidades: llega con cada entrega.
- Configuración regional, roles, WSL, respaldo y CI. 0 de 8 CA de la E0 cumplidos (CA-71 y CA-53 tienen su prueba, pero no la integración continua).

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
