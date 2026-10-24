# Código del SGA — entrega E0 (esqueleto)

**Estado:** esqueleto del proyecto Django; **sin modelos, migraciones ni pantallas**. La E0 está *en curso* ([registro de avance](../DOC/fase-5-implementacion/AVANCE_IMPLEMENTACION.md)). Nada de lo que hay aquí está aprobado ni probado en el entorno de destino.

## Qué hay
| Ruta | Contenido |
|---|---|
| `sga/settings.py` | Configuración: secretos fuera del repositorio, PostgreSQL por socket, Argon2id, contraseñas de 15 caracteres, sesión de 24 h, cookies seguras si no hay `SGA_DEBUG` |
| `nucleo/`, `cuentas/` | Aplicaciones de la E0 (ADR-030), vacías salvo las pruebas de `nucleo` |
| `requirements.txt` | Versiones fijadas |
| `.env.ejemplo` | Variables de entorno de ejemplo |

## Entorno de desarrollo actual y su límite
Se creó con **Python 3.12 en Windows** (`py -3.12 -m venv .venv`) porque la distribución `Ubuntu-26.04` de WSL **aún no está instalada** y el plan pide Python 3.14 en ella (DOC/fase-5, secciones 5.1 y 5.2). Es una desviación del plan: todo debe volver a probarse en WSL, y las versiones de `requirements.txt` deben volver a fijarse allí.

## Pruebas
```
cd src
$env:SGA_DEBUG = "1"
.venv\Scripts\python manage.py test nucleo
```
Las pruebas de `nucleo` no usan la base de datos y las de `cuentas` sí (necesitan PostgreSQL; ver más abajo): comprueban Argon2id, el mínimo de 15 caracteres, la zona horaria, la ausencia del administrador de Django y que el proyecto no arranque sin `SECRET_KEY`. `manage.py check --deploy` solo avisa de HSTS, que se activa por etapas en la etapa B (ADR-032, decisión 5).

## Qué falta de la E0
Comando de creación y rescate, aviso por correo, límite de intentos, auditoría, organización y configuración regional, roles de PostgreSQL y archivo de privilegios (ADR-027, 031), despliegue en WSL, HTTPS autofirmado, respaldo cifrado y su restauración, e integración continua.

## `cuentas.Administrador` (actualización zzc)
Modelo, cifrado del secreto del segundo factor (Fernet), TOTP con pyotp y límite de intentos, con 26 pruebas que necesitan PostgreSQL. Para correrlas hace falta un servidor PostgreSQL accesible y las variables `SGA_BD_HOST`, `SGA_BD_PUERTO` y `SGA_BD_USUARIO`; el usuario debe poder crear bases (el ejecutor crea `test_sga`). No existe todavía la vista de inicio de sesión, y **una vista que llame a `login()` tras `authenticate()` sin pedir el TOTP saltaría el segundo factor**.

## Códigos de recuperación (actualización zzd)
`CodigoRecuperacion`, `emitir_codigos_recuperacion` y `verificar_codigo_recuperacion` en `cuentas/autenticacion.py`; 38 pruebas en total. Aún sin vista que los use.

## Inicio de sesión (actualización 2026-10-24)
Rutas `/entrar/`, `/entrar/codigo/`, `/salir/` y `/` (página provisional protegida), con el middleware `LimiteDeSesion` (24 h / 1 h). 51 pruebas en total. La cuenta aún solo se crea desde código: no hay comando de creación ni activación del segundo factor.
