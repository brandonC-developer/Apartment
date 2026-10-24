# Actualización 2026-10-24 — Vista de inicio de sesión de dos pasos y límites de sesión

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/cuentas/`](../../../src/cuentas/views.py), [`src/sga/`](../../../src/sga/settings.py), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS v1.16, RF-26, RF-27, RNF-01, CA-48, CA-68, CA-69; instrucción del solicitante: «sí, escribe la vista de inicio de sesión» (24-oct-2026)
**Estado:** implementado y probado en un PostgreSQL desechable; no aprobado

## 1. Qué se escribió
| Archivo | Contenido | Requisitos |
|---|---|---|
| `cuentas/views.py` | Paso 1 (usuario y contraseña) que **no** inicia sesión: anota en la sesión el primer paso, 5 minutos. Paso 2 (TOTP de 6 dígitos o código de recuperación) que es el único que llama a `login()`. Cierre de sesión por POST y página protegida provisional | RF-26, RNF-01 |
| `cuentas/middleware.py` | `LimiteDeSesion`: cierra la sesión a las 24 h de abierta o tras 1 h sin actividad; una sesión autenticada sin marcas de tiempo se cierra | RF-27, CA-48 |
| `cuentas/urls.py`, `sga/urls.py`, plantillas | Rutas `/`, `/entrar/`, `/entrar/codigo/`, `/salir/` y HTML mínimo sin estilos | — |
| `sga/settings.py` | Middleware y `LOGIN_URL` | — |
| `cuentas/tests.py` | 13 pruebas de la vista y la sesión; en total 51 | — |

## 2. Propuestas del asistente (sin aprobar)
- Vigencia del primer paso: **5 minutos**.
- Un **mismo mensaje** en el primer paso para usuario inexistente, contraseña incorrecta, cuenta en espera y segundo factor sin activar, para no revelar cuál ocurrió; en el segundo paso sí se informa la espera.
- Con el segundo factor **sin activar no hay acceso** (RNF-01); la activación llegará con el comando de creación.
- Un código de 6 dígitos se trata como TOTP y cualquier otro como código de recuperación.
- El cierre a las 24 h es absoluto desde el inicio; la actividad solo renueva la inactividad.
- Sin estilos ni diseño: las pantallas reales dependen de los wireframes (pendientes).

## 3. Verificación
- **51 pruebas pasan** contra PostgreSQL 18 desechable (puerto 54329, ya borrado); Python 3.12 en Windows.
- **Pruebas de mutación manuales:** quitar la exigencia de segundo factor activo hizo fallar su prueba; anular el límite de inactividad hizo fallar la suya; ambos cambios se restauraron.
- **Primera corrida: 1 fallo, error mío en la prueba** (comparaba el HTML completo, cuyo token CSRF cambia); se corrigió comparando el mensaje.
- No se probó en un navegador ni con HTTPS; `SESSION_COOKIE_AGE` de 24 h sigue vigente como respaldo.

## 4. Qué no está hecho
Aviso de seguridad por correo (al quinto fallo, al iniciar sesión, etc.), auditoría de los eventos, comando de creación y rescate con activación del segundo factor (hoy la cuenta solo puede crearse desde código), cambio y restablecimiento de contraseña, límite por dirección IP, estilos, roles de PostgreSQL, despliegue en WSL, respaldo y CI. 0 de 8 CA de la E0 cumplidos.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
