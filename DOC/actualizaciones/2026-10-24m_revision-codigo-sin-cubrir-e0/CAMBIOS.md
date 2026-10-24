# Actualización 2026-10-24 (m) — Revisión del código sin cubrir de la E0

**Fecha:** 2026-10-24
**Documentos afectados:** pruebas nuevas en [`src/cuentas/tests_cobertura.py`](../../../src/cuentas/tests_cobertura.py), [`src/nucleo/tests_ajustes.py`](../../../src/nucleo/tests_ajustes.py), [`src/nucleo/tests_privilegios.py`](../../../src/nucleo/tests_privilegios.py) y [`src/nucleo/tests_regional.py`](../../../src/nucleo/tests_regional.py); [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia y no se modificó ningún código de la aplicación.
**Origen:** plan de implementación, sección 3.1, condición 5 de terminado («se revisó el código sin cubrir de los módulos críticos; sin umbral numérico de cobertura») y estrategia de pruebas, sección 9; instrucción del solicitante: «sí, haz la revisión del código sin cubrir» (24-oct-2026)
**Estado:** hecha; **es una autorrevisión del autor**, no la revisión por otra persona del plan (sección 3.3); no aprobada

## 1. Método
Se midió la cobertura de líneas y de ramas (`coverage` con `--branch`, instalada solo para la medición y retirada después, sin tocar `requirements.txt`) sobre los paquetes `cuentas`, `nucleo` y `sga`, sin migraciones, pruebas, `wsgi`, `asgi` ni `apps`. Se leyó cada línea y rama sin ejecutar, se decidió si era un riesgo, se escribió la prueba cuando lo era y se repitió la medición. No se fijó ningún umbral numérico (así lo dice la condición): el 99 % es un resultado, no una meta.

## 2. Resultado
| | Antes | Después |
|---|---|---|
| Líneas sin ejecutar | 39 de 823 | 8 de 823 |
| Ramas parciales | 12 de 168 | 4 de 168 |
| Cobertura total | 94 % | **99 %** |
| Pruebas | 181 | **196** (15 nuevas); pasan en Windows con Python 3.12 y en WSL con Python 3.14.4, esta sin ninguna omitida |

Todos los módulos críticos de la E0 (`cuentas.autenticacion`, `backends`, `cifrado`, `models`, `views`, `middleware`, los dos comandos de la cuenta, `nucleo.auditoria`, `organizacion`, `privilegios`, `formato`, `models`, `views`) quedaron en **100 %** de líneas y ramas.

## 3. Revisión de cada línea sin cubrir
| Dónde | Qué era | Riesgo | Decisión |
|---|---|---|---|
| `autenticacion.comprobar_token_registro`, cuenta con segundo factor ya activo | Devolver «incorrecto» sin tocar el contador | Bajo (la vista ya redirige), pero es una barrera contra una carrera | **Prueba nueva**: no cambia el contador |
| `views.registro_segundo_factor`, rama `TOKEN_INVALIDO` | El token se vence o se consume **entre** pedirlo y activar | **Medio**: es la segunda comprobación bajo bloqueo de la corrección de seguridad de la actualización 2026-10-24d | **Prueba nueva**: se vuelve a pedir, no se activa, no hay sesión. Con la comprobación quitada la prueba falla |
| `views` líneas 85, 105 y 154 | Con la sesión iniciada, los pasos del inicio redirigen al inicio | Bajo | **Prueba nueva**: ninguno cuenta fallos ni cambia nada |
| `views.cerrar_sesion` sin sesión | Rama sin autenticación | Bajo | **Prueba nueva**: redirige y no escribe auditoría |
| `backends.authenticate` sin usuario o sin contraseña | Devuelve `None` sin tocar la cuenta | Medio (entrada vacía) | **Prueba nueva** |
| `backends.get_user`, cuenta inexistente | Una sesión de una cuenta borrada | Medio (sesión huérfana) | **Prueba nueva**: la sesión se trata como anónima. La rama devuelve `None`; si la cambiara por un usuario falso, Django la frenaría por el hash de la sesión, así que esa mutación **no** la detecta la prueba (equivalente) |
| `cuentas.models`: usuario vacío y `__str__` | Validación del gestor y texto | Bajo | **Pruebas nuevas** |
| `nucleo.models`: dos `__str__` | Texto | Ninguno | **Prueba nueva** |
| `nucleo.management.commands.aplicar_privilegios` (0 %) | El **comando**, no la función que usa | **Medio**: es lo que ejecuta el rol dueño en cada despliegue | **Pruebas nuevas**: `--mostrar` imprime y no ejecuta (con la mutación que lo ejecuta, falla); aplicar concede y avisa de las tablas sin entrada |
| `sga/settings.py` 19, 35, 150-156 | Lectura de secretos y ajustes sin depuración | **Alto si fallan** (cookies seguras, HTTPS, clave secreta) | **Pruebas nuevas en un proceso aparte** (`nucleo/tests_ajustes.py`): clave desde el entorno y desde un archivo, cookies seguras, redirección a HTTPS, cabecera de `Nginx`, IP de origen y hosts. Con una cookie no segura, falla |

## 4. Lo que la cobertura no mide
- **Los 8 que siguen sin ejecutar** son las mismas líneas de `settings.py`: ahora se prueban en un proceso aparte y `coverage` no sigue procesos hijos; no son líneas sin probar.
- **Los scripts de shell** (`respaldo/`, `despliegue/`) no los mide una herramienta de Python. Se probaron ejecutándolos de verdad y con mutaciones (actualizaciones 2026-10-24i y 2026-10-24j); en Windows 13 de esas pruebas se omiten por falta de `age` en el PATH y corren en WSL y en el trabajo `respaldo` del flujo.
- **Las plantillas** no se miden.
- **Cobertura no es calidad de las pruebas:** una línea ejecutada no prueba que el resultado sea el correcto. Por eso se hicieron además mutaciones manuales en cada actualización.

## 5. Límites de esta revisión (importan)
- **Es el mismo autor quien escribió el código y quien lo revisó**, sin pausa de tiempo. El plan (sección 3.3) exige para lo crítico —seguridad, datos personales y modelo financiero— una **revisión por una persona distinta** antes de cargar datos reales, con la lista LRC-SGA-001; **sigue sin haber persona designada**. Esta actualización cumple la condición 5 de terminado de la E0 y no reemplaza esa revisión.
- La E0 **no contiene** los módulos que la condición menciona como críticos de negocio (períodos, prorrateo, reajuste, movimientos y plazos legales): llegan en las entregas E2 a E5, y esta revisión se repite en cada una.
- Un caso sin resolver que apareció: la mutación equivalente de `get_user` (ver arriba).

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
