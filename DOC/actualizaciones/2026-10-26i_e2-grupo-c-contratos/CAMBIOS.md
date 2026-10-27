# Actualización 2026-10-26 (i) — E2, grupo C: propiedades y contratos

**Fecha:** 2026-10-26
**Documentos afectados:** código en [`src/alquileres/`](../../../src/alquileres/services.py), [`src/inquilinos/selectors.py`](../../../src/inquilinos/selectors.py), [`src/nucleo/auditoria.py`](../../../src/nucleo/auditoria.py), [`src/sga/privilegios.py`](../../../src/sga/privilegios.py), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS RF-06 a RF-10, RF-36, RF-42, RF-48; RN-02, RN-17, RN-30; CA-02, CA-10, CA-24, CA-29, CA-31, CA-32, CA-62, CA-63, CA-67 y CA-78; modelo de datos v0.7 (R2, R21, R26); instrucción del solicitante: «escribe el grupo C» (26-oct-2026)
**Estado:** implementado y probado; no aprobado

## 1. Decisión 2 de la E2 — renovación del contrato
**Pregunta:** RF-42 y CA-32 dicen que un contrato por decidir «se cierra o se renueva», pero la ERS no define la operación de renovar (OL-09, según el resumen de la ERS, habla de prórroga tácita; texto de la ley no leído por mí). ¿Cómo se registra la renovación?
**Opciones:** (a) cambiar la fecha de fin del mismo contrato, **recomendada**; (b) crear un contrato nuevo contiguo; (c) no implementarla en esta entrega.
**Respuesta del solicitante:** «Cambiar la fecha de fin del mismo contrato (Recomendado)».
**Decisión:** `renovar_contrato` cambia la fecha de fin a una posterior, o la quita (contrato abierto), con motivo obligatorio y auditoría. Es el mismo contrato y su serie de obligaciones continúa. Se rechaza si el contrato está anulado o cerrado, si ya es abierto, si la fecha no es posterior a la actual o si el cambio solapa con otro contrato.

## 2. Qué se escribió
| Pieza | Qué hace |
|---|---|
| `services.registrar_propiedad`, `actualizar_propiedad`, `marcar_inactiva`, `reactivar_propiedad` | RF-06, CA-63: alias único; inactivar se bloquea con un contrato futuro, vigente o por decidir; una propiedad inactiva no admite contratos nuevos |
| `services.crear_contrato` | RF-07, CA-02: con su condición inicial y auditoría. **Rechaza, informando todos los motivos a la vez:** datos incoherentes, inquilino sin consentimiento vigente (**CA-67**) o sin el frente de su documento (**R26, CA-78**), desactivado o desasociado, propiedad inactiva y solape (**R2, CA-24**). La vigencia menor de tres años solo advierte |
| `services.finalizar_contrato` | RF-09, RN-17, CA-31, CA-10: registra el fin y cierra; anula con auditoría las obligaciones posteriores sin movimientos; prorratea la del período que contiene el fin con un ajuste inmutable (`calculo.py`); conserva el historial; advierte si el fin está a menos de tres meses |
| `services.renovar_contrato` | Decisión 2 |
| `services.anular_contrato` | RF-48, CA-62: solo sin movimientos válidos y con motivo; anula sus obligaciones; deja de contar para el solape |
| `services.sustituir_inquilino` | RF-36, CA-24: cierra el contrato anterior y crea el nuevo **en una sola transacción**: si el nuevo no es válido, el anterior no se cierra |
| `selectors` | Estado del contrato (RN-30) y de la propiedad, y las consultas por estado que coinciden con él; importe vigente derivado |
| `movimientos.py` | Punto de extensión (proveedor reemplazable) para las preguntas sobre movimientos que la E3 contestará: «¿tiene movimientos?», «¿cuánto se ha abonado?» |
| `bloqueos.py` y `apps.ready` | **CA-29 real:** se registra en `inquilinos.bloqueos`; un inquilino con contrato futuro, vigente o por decidir no se desactiva y el mensaje dice en qué propiedad |
| Migración `0003_contrato_cerrado` | Columna `cerrado_en`, restricción «un contrato cerrado tiene su fecha de fin» y el disparador de «una sola vez» ampliado al cierre |

## 3. Propuestas del asistente (sin aprobar)
1. **`Contrato.cerrado_en`.** El modelo de datos deriva *finalizado* y *por decidir* de «hubo fin vencido sin cierre ni renovación» pero no guarda el cierre; sin una marca los dos estados no se distinguen. Es una columna nueva (**para el modelo de datos v0.8**). Consecuencia que también propongo: **un contrato cerrado no se renueva ni se reabre**; para otra relación se crea un contrato nuevo (RF-36).
2. **Solo se acorta el fin al finalizar.** Alargarlo es renovar.
3. **Se bloquea desactivar al inquilino con un contrato futuro**, igual que RF-06 bloquea inactivar la propiedad; RF-04 dice solo «vigente».
4. **Advertencia de la fecha de fin (RF-09):** «dista menos de tres meses de la fecha de registro» se midió hacia adelante (un fin ya pasado también avisa).
5. **Vigencia menor de tres años (RF-07):** se advierte si el fin es anterior al día previo al tercer aniversario del inicio; un contrato abierto no avisa. Se aplica a cualquier destino, como dice RF-07 (OL-08 habla de vivienda).
6. **Inquilino desactivado o desasociado no admite contratos nuevos** (la ERS solo pide consentimiento y frente).
7. **Alias sin distinguir mayúsculas; días de gracia hasta 365.**
8. **`descripcion` y `direccion` pasan a la lista de campos personales de la auditoría** (de la propiedad solo consta que cambiaron).
9. **El depósito de RF-07 («cuando corresponda»)** y el traslado o anulación del depósito son de la E3.

## 4. Verificación
- **575 pruebas pasan en Windows** (Python 3.12; 67 nuevas en total: 63 de servicios, 3 del cierre del modelo y 1 de cálculo) y **564 en WSL** (Python 3.14.4, Pillow 13.0.0); `makemigrations --check` sin cambios; `verificar.sh` sin fallos. Cobertura de `alquileres`: **99 %** (una línea del modelo sin ejecutar y una rama).
- **Mutaciones manuales, todas detectadas (13):** sin consentimiento, sin frente, sin la comprobación previa del solape (se detecta porque la prueba exige que el mensaje diga con qué contrato choca), finalizar anulando obligaciones con pagos, no prorratear, renovar con una fecha anterior, anular ignorando los movimientos, prorratear sin respetar lo abonado, estado que ignora el cierre, sin el bloqueo real de desactivar, inactivar ignorando los contratos futuros, no anular las obligaciones al anular el contrato y no advertir la vigencia corta.
- **Se probó además:** carreras (dos altas con el mismo alias, una renovación que choca a la vez); que ninguna operación deja nombre ni documento en la auditoría; los nueve casos de estado contra su consulta; el relevo de CA-24 en ambos bordes y con el anterior sin cerrarse si el nuevo falla.

## 5. Para la próxima versión de los documentos
Modelo de datos v0.8: `cerrado_en` en `CONTRATO`, R23 cumplida por construcción (decisión 1) y la regla de que un contrato cerrado no se reabre. ERS: la operación de renovar (decisión 2) y la advertencia de la fecha de fin. No se editó ninguna versión existente.

## 6. Qué no está hecho
Reajuste y corrección (D), obligaciones y proceso diario (E), fotografías (F), pantallas (G), medición y cierre (H). **La aceptación escrita del bloqueo por saldos pendientes (CA-29) llega con la E3.** 0 de 25 CA de la E2 marcados.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
