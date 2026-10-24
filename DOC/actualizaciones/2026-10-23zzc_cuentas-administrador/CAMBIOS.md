# Actualización 2026-10-23 (zzc) — Implementación de `cuentas.Administrador`

**Fecha:** 2026-10-23
**Documentos afectados:** código en [`src/cuentas/`](../../../src/cuentas/models.py), [`src/sga/settings.py`](../../../src/sga/settings.py), [`src/requirements.txt`](../../../src/requirements.txt), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** las decisiones [(zz)](../2026-10-23zz_modelo-de-usuario/CAMBIOS.md), [(zza)](../2026-10-23zza_biblioteca-segundo-factor/CAMBIOS.md) y [(zzb)](../2026-10-23zzb_cifrado-secreto-segundo-factor/CAMBIOS.md); instrucción del solicitante: «sí, escribe cuentas.Administrador ahora» (23-oct-2026)
**Estado:** implementado en parte y probado en un PostgreSQL desechable; no aprobado

## 1. Qué se escribió
| Archivo | Contenido | Requisitos |
|---|---|---|
| `cuentas/models.py` | `Administrador` sobre `AbstractBaseUser`, sin permisos de Django, con los campos del MDD v0.7; restricción de tabla `id = 1` (una sola cuenta); gestor con `crear_administrador` (`create_user` y `create_superuser` lanzan error) | RF-26, RF-27, RN-25 |
| `cuentas/cifrado.py` | Fernet/MultiFernet: cifrar, descifrar y recifrar (rotación) | Decisión (zzb) |
| `cuentas/autenticacion.py` | Primer paso (contraseña) y segundo paso (TOTP con pyotp) con el contador de intentos compartido, espera de 1 minuto duplicada hasta 1 hora, aviso al quinto fallo, ventana de ±1 intervalo y rechazo de repetición | RF-27, CA-68, CA-69 |
| `cuentas/backends.py` | Backend que verifica solo contraseña y contador | RF-27 |
| `cuentas/migrations/0001_initial.py` | Tabla con la restricción | MDD |
| `sga/settings.py` | `AUTH_USER_MODEL`, `AUTHENTICATION_BACKENDS` y `CLAVES_CIFRADO` | — |
| `cuentas/tests.py` | 26 pruebas con base de datos; en total 32 con las de `nucleo` | — |

## 2. Verificación
- **32 pruebas pasan** contra PostgreSQL 18 (clúster desechable en el puerto 54329, ya borrado), con `-W error::SyntaxWarning`.
- **Primera corrida: 1 fallo, error mío en la prueba** (el ayudante multiplicaba el desfase por 30, así que no probaba lo que decía); se corrigió el ayudante y se repitió.
- **Prueba de mutación manual:** cambiar `aceptado <= ultimo` por `<` hizo fallar la prueba de repetición; se restauró el código.
- No se probó la concurrencia real (dos intentos simultáneos); el bloqueo de fila existe pero no tiene prueba propia.
- Entorno: Python 3.12 en Windows, no el Python 3.14 del plan.

## 3. Qué se decidió al escribirlo (propuesta del asistente, sin aprobar)
- La restricción `id = 1` para imponer RN-25, y que la cuenta se cree con `id = 1`.
- Un intento hecho **durante la espera** se rechaza y **no suma** otro fallo; no estaba en CA-68.
- Una contraseña correcta **no reinicia** el contador; solo lo reinicia un TOTP correcto, porque el contador es compartido y de lo contrario quien conozca la contraseña podría probar códigos sin límite.
- Un usuario inexistente no cuenta fallos y hace un hash de relleno para parecerse en tiempo.
- Seis dígitos de TOTP y un `usuario` de hasta 150 caracteres.

## 4. Qué no está hecho (de RF-27 y de la E0)
- **Códigos de recuperación** (entidad CODIGO_RECUPERACION), su aviso y su límite compartido.
- **Vista de inicio de sesión de dos pasos y sesión de 24 h/1 h de inactividad (CA-48):** hoy el backend verifica solo la contraseña; **una vista que llame a `login()` sin pedir el TOTP lo saltaría**. El aviso está en el código.
- **Comando de creación y de rescate en el servidor** (RF-27) y activación del segundo factor (`segundo_factor_activo` no se pone en verdadero en ningún sitio).
- **Aviso de seguridad por correo** al quinto fallo (la función solo lo indica) y notificaciones.
- **Auditoría** de eventos de autenticación, restablecimiento de contraseña y cambio de correo.
- **Respaldo de la clave de cifrado** y su generación; el valor de `CLAVES_CIFRADO` vacío impide cifrar.
- Roles de PostgreSQL y archivo de privilegios, despliegue en WSL, respaldo y restauración, integración continua.
- 0 de 8 CA de la E0 cumplidos.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
