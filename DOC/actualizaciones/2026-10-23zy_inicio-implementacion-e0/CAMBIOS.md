# Actualización 2026-10-23 (zy) — Inicio de la implementación: esqueleto de la E0

**Fecha:** 2026-10-23
**Documentos afectados:** [CLAUDE.md](../../../CLAUDE.md) (la implementación se autoriza solo para la E0), [registro de avance](../../fase-5-implementacion/AVANCE_IMPLEMENTACION.md) (E0 pasa a *en curso*), [DOC/README.md](../../README.md) y el código nuevo en [`src/`](../../../src/README.md)
**Origen:** instrucción del solicitante (23-oct-2026): «sí, prepara el esqueleto E0»; y su respuesta a la pregunta sobre dónde va el código: «carpeta `src/` en este repositorio» (opción recomendada por el asistente)
**Estado:** esqueleto creado; no aprobado

## 1. Pregunta, respuesta y decisión
| Pregunta | Respuesta del solicitante | Decisión |
|---|---|---|
| ¿Se inicia la implementación? | «Sí, prepara el esqueleto E0» | La E0 se inicia **sin ERS ni DAS aprobados**; queda anotado como desviación |
| ¿Dónde va el código y se actualiza CLAUDE.md? | Carpeta `src/` en este repositorio (recomendada) | `src/` junto a `DOC/`; CLAUDE.md autoriza solo la E0 |

## 2. Qué se hizo
- Proyecto Django 5.2.18 con `psycopg` 3.3.6 y `argon2-cffi` 25.1.0 (versiones fijadas en `src/requirements.txt`), aplicaciones `nucleo` y `cuentas` vacías, configuración con secretos fuera del repositorio, PostgreSQL por socket, Argon2id, contraseñas de 15 caracteres, sesión de 24 h, cookies seguras fuera de desarrollo, sin el administrador de Django (propuesta).
- 6 pruebas sin base de datos, que pasan con `-W error`. `manage.py check` sin avisos; `check --deploy` solo avisa de HSTS (decisión 5 del ADR-032: se activa en la etapa B).
- Se añadió `.gitignore` en la raíz (`.venv/`, `__pycache__/`, `*.pyc`, `.env`).

## 3. Desviaciones y límites (importantes)
- **Entorno distinto del plan:** se usó **Python 3.12 en Windows**; el plan pide Python 3.14 en `Ubuntu-26.04` dentro de WSL 2, que **no está instalada** (solo existe `docker-desktop`). Hay que instalarla (`wsl --install -d Ubuntu-26.04`, interactivo) y volver a probar todo allí y a fijar versiones.
- **Nada del criterio de salida de la E0 se cumple todavía:** no hay modelo de usuario, segundo factor, auditoría, roles ni archivo de privilegios de PostgreSQL, despliegue, HTTPS, respaldo ni integración continua. 0 de 8 CA.
- **No se ejecutó nada contra PostgreSQL:** las pruebas no usan la base de datos.
- **No se decidió** la biblioteca del segundo factor ni el modelo de usuario (`AUTH_USER_MODEL` debe fijarse antes de la primera migración).
- La interfaz sin el administrador de Django, el orden de lectura de secretos (entorno, luego `/etc/sga/`) y la ruta de los secretos son propuesta del asistente.
- Las reglas de `CLAUDE.md` siguen vigentes para el código: no inventar, trazabilidad al requisito, y verificar antes de dar algo por terminado.
- El script de coherencia no revisa `src/`.

## 4. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
