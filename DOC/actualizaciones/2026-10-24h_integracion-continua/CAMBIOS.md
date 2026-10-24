# Actualización 2026-10-24 (h) — Integración continua

**Fecha:** 2026-10-24
**Documentos afectados:** nuevo [`.github/workflows/integracion-continua.yml`](../../../.github/workflows/integracion-continua.yml), [`src/sga/settings.py`](../../../src/sga/settings.py), [`src/.env.ejemplo`](../../../src/.env.ejemplo), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** DAS v0.15, ADR-025 (GitHub Actions: pruebas, `check --deploy` y migraciones contra PostgreSQL 18) y ADR-032 decisiones 10 y 12 (`pip-audit` en la integración continua; credenciales efímeras); plan, condiciones 1 y 2 de terminado; instrucción del solicitante: «integración continua primero: es lo que permite marcar los CA como cumplidos» (24-oct-2026)
**Estado:** escrito y simulado en local; **no ha corrido en GitHub**; no aprobado

## 1. Qué se escribió
El flujo tiene dos trabajos y se dispara en cada `push` a `main`, en cada solicitud de integración, a mano y cada lunes:

| Trabajo | Pasos |
|---|---|
| **Pruebas, `check --deploy` y migraciones** (Ubuntu, Python 3.14, servicio `postgres:18`) | 1) instalar dependencias; 2) `makemigrations --check --dry-run` (ningún cambio de modelo sin migración); 3) todas las pruebas, cuyo ejecutor aplica las migraciones desde cero; 4) `check --deploy` sin `SGA_DEBUG`, que **solo admite el aviso de HSTS** (`security.W004`, que se activa en la etapa B; ADR-032 d5) y falla con cualquier otro; 5) despliegue de la base como en el servidor: `db/roles.sql`, `migrate` como rol dueño, `aplicar_privilegios` y una lectura como rol de la aplicación |
| **Vulnerabilidades de las dependencias** | `pip-audit` sobre `src/requirements.txt`, en un trabajo aparte para que su fallo no tape el de las pruebas |

Además, en `settings.py` se agregó `ALLOWED_HOSTS` desde la variable `SGA_HOSTS_PERMITIDOS`: `check --deploy` lo exigía (aviso `security.W020`) y el README anterior decía, sin haberlo comprobado, que solo avisaba de HSTS.

## 2. Propuestas del asistente (sin aprobar)
- **Acciones fijadas por SHA completo** (guía de endurecimiento de GitHub Actions; `actions/checkout` v7.0.1 y `actions/setup-python` v7.0.0, de más de dos semanas: la última de `setup-python`, v7.1.0, tiene dos días). Hay que actualizar los SHA a mano; Dependabot podría hacerlo y no se decidió.
- **Servicio de PostgreSQL sin contraseña** (`trust`): la base existe solo durante la corrida y no es alcanzable desde fuera (ADR-032 d12: credenciales efímeras).
- **Una sola versión de Python (3.14)**, la del plan; no hay una matriz con 3.12.
- **Ejecución semanal** del flujo (lunes), porque las vulnerabilidades aparecen sin que cambie el código; el ADR dice «alerta», no la frecuencia.
- **`pip-audit` fijado en 2.10.1**, la versión que se probó en local.
- `ALLOWED_HOSTS` por variable de entorno; en las pruebas y con `SGA_DEBUG=1` Django admite `localhost`.

## 3. Verificación (y sus límites)
- El archivo YAML se leyó con un analizador y tiene los dos trabajos y los pasos esperados.
- **Cada paso se ejecutó por separado en local** contra un PostgreSQL 18 desechable (ya borrado) con el mismo texto de los comandos: `makemigrations --check` sin cambios; el script de `check --deploy` pasa con solo W004 y **falla** cuando aparece otro aviso (se probó con `ALLOWED_HOSTS` vacío); el despliegue de la base (roles, migraciones, privilegios y lectura como `sga_app`) funcionó; las 140 pruebas pasan.
- `pip-audit` 2.10.1 sobre `requirements.txt`: **sin vulnerabilidades conocidas** (consulta del 2026-10-24).
- **Lo que no se pudo comprobar:** que el flujo corra en GitHub (no hay `gh` ni acceso a las Actions desde aquí; el repositorio es privado y puede haber límites de minutos), que `psql` exista en la imagen del ejecutor (se supone, sin verificar), que la imagen `postgres:18` exista con ese nombre, y que las cinco dependencias funcionen con **Python 3.14**: todo se probó con 3.12. La primera corrida lo dirá.

## 4. Qué cambia para marcar los CA
- Un CA solo se marca como cumplido cuando su prueba pasa **en esa corrida verde con Python 3.14** (condición 1 de terminado), y la E0 se da por terminada solo con las nueve condiciones. La integración continua es necesaria, no suficiente: sigue faltando WSL con el despliegue real, el respaldo cifrado y su restauración, y varias pruebas de CA de la E0 que dependen de eso.
- **0 de 8 CA de la E0 cumplidos** hasta que exista esa primera corrida verde.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
