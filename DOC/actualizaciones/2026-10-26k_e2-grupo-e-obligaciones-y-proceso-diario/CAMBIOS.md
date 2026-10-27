# Actualización 2026-10-26 (k) — E2, grupo E: obligaciones y proceso diario

**Fecha:** 2026-10-27
**Documentos afectados:** código en [`src/alquileres/obligaciones.py`](../../../src/alquileres/obligaciones.py), [`proceso.py`](../../../src/alquileres/proceso.py), el comando `ejecutar_proceso_diario`, selectores, servicios y las unidades de `systemd`; [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS RF-11, RF-12, RF-14, RF-42, RF-43, RNF-04, RNF-16; CA-03, CA-14, CA-30, CA-36, CA-49, CA-50; modelo de datos v0.7 (R1, ADR-015); instrucción del solicitante: «escribe el grupo E»
**Estado:** implementado y probado; no aprobado

## 1. Qué se escribió
| Pieza | Qué hace |
|---|---|
| `obligaciones.generar_obligaciones` | Crea las obligaciones que faltan de un contrato futuro, vigente o por decidir, las que inician hasta 30 días después de hoy (CA-30: el 11 de marzo genera la del 10 de abril, el 10 no). Usa la condición que rige cada período, el vencimiento dentro del período (CA-03, CA-50) y la gracia. Bloquea la fila del contrato y, si otra ejecución ganó la carrera, la restricción única (R1) se trata como «ya existe», sin error (RF-12) |
| Último período | Si el contrato ya tiene fecha de fin dentro de un período, esa obligación nace prorrateada con el mismo ajuste inmutable que al finalizar (CA-14: ₡92.903) |
| `registrar_saldo_de_apertura` | RF-43, CA-49: obligación sin período, vencimiento digitado (por omisión, apertura + gracia) y fecha límite igual; los períodos que inician hasta la fecha de apertura no se generan |
| `selectors.estado_de_la_obligacion`, `saldo_de_la_obligacion` | RF-14, CA-36: anulada, pagada (saldo cero), vencida (hoy > fecha límite) o pendiente; el saldo resta los movimientos por el proveedor de la E3 |
| `proceso.ejecutar` y `manage.py ejecutar_proceso_diario` | Registra la ejecución en `EjecucionProceso` (correcta o fallida), audita como actor «sistema» con su ejecución (R19); un contrato que falla no detiene a los demás y deja la ejecución fallida con código de salida distinto de cero |
| `sga-proceso-diario.service` y `.timer` | 07:00 de Costa Rica, `Persistent=true`, como `sga_app` con el endurecimiento de las demás unidades; `desplegar.sh` los instala y `verificar.sh` comprueba el temporizador y dos ejecuciones seguidas |
| `services._prorratear` | Ahora parte del importe sin los prorrateos anteriores, así puede repetirse; `renovar_contrato` ajusta el prorrateo del último período al nuevo fin (se retira si el contrato continúa) |

## 2. Propuestas del asistente (sin aprobar)
1. **La fecha de apertura se guarda en `datos_calculo`** de la obligación de apertura (`{"regla": "saldo_de_apertura", "fecha_apertura": ...}`): el modelo v0.7 no tiene otra columna y no se cambió el esquema. MDD v0.8 podría darle columna propia.
2. **Reglas del saldo de apertura:** la fecha no es anterior al inicio ni futura; el vencimiento no es anterior a la fecha de apertura; un solo saldo por contrato; se rechaza si ya hay obligaciones regulares vigentes de períodos incluidos en el saldo.
3. **Un contrato por decidir genera períodos nuevos con el importe completo** y no prorratea (RF-42); el contrato con fin futuro no genera períodos que inicien después del fin.
4. **Sin saldo de apertura, un contrato que empezó en el pasado genera todos sus períodos pasados de una vez** (RF-11 al pie de la letra) y quedan vencidos. Para evitarlo está el saldo de apertura; si prefieres que el sistema lo exija o genere solo desde el mes de carga, dímelo.
5. **Un período anulado no se vuelve a generar** (la restricción única cuenta también las anuladas).
6. **Horario de las 07:00** según ADR-032 d15; `systemd` en WSL aceptó la zona dentro de `OnCalendar` al activar el temporizador.

## 3. Lo que no se hizo
- Avisos de RF-42 (120 días antes, notificación persistente, resumen por correo): son de la entrega de notificaciones.
- Prueba de concurrencia real con dos procesos: se probó la carrera simulada (la otra ejecución gana entre la lectura y la inserción) y la restricción de la base con SQL directo.

## 4. Verificación
- **676 pruebas encontradas: en Windows (Python 3.12) pasan, con 14 omitidas; en WSL (Python 3.14.4) corren 665 sin fallos.** 54 son nuevas. `verificar.sh` sin fallos, con el temporizador activo y el proceso corriendo dos veces como `sga_app`; cobertura de `alquileres` 99 % y 100 % en los módulos nuevos.
- **Mutaciones, 21 de 21 detectadas** (una sobrevivió y se cubrió con una prueba del borde «apertura el día de inicio»): anticipación de 29 y 31 días, apertura inclusiva, carrera sin tolerancia, sin tope de fin, prorrateo de períodos posteriores, fecha futura, vencimiento por omisión, fecha límite distinta, condición equivocada, actor sistema, vencida el último día de gracia, saldo cero, saldo sin abonos, prorrateo sobre lo prorrateado, renovación sin ajuste, ejecución fallida sin marcar, fallo sin registrar y comando sin código de error.

## 5. Qué no está hecho
Fotografías (F), pantallas (G) y medición y cierre (H). 0 de 25 CA de la E2 marcados.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
