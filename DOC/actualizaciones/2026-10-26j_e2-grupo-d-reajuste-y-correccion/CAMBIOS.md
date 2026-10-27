# Actualización 2026-10-26 (j) — E2, grupo D: reajuste, corrección y ajuste manual

**Fecha:** 2026-10-26
**Documentos afectados:** código en [`src/alquileres/condiciones.py`](../../../src/alquileres/condiciones.py) y sus modelos, selectores y privilegios, [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS RF-09, RF-10, RN-12, RN-14; OL-06 y OL-07 (según el resumen de la ERS, **sin validar por un abogado**); CA-12, CA-22, CA-39, CA-40, CA-51 y CA-55; modelo de datos v0.7 (H9, R13, ADR-014, ADR-016); instrucción del solicitante: «escribe el grupo D» (26-oct-2026)
**Estado:** implementado y probado; no aprobado

## 1. Decisión 3 de la E2 — las fechas de pago en una corrección
**Pregunta:** una corrección retroactiva puede cambiar el monto, el día de vencimiento o los días de gracia (RF-10, CA-22). Para el monto basta un ajuste inmutable, pero las obligaciones ya generadas guardan su fecha de vencimiento y su fecha límite sin poder cambiarlas (R12, el modelo y los privilegios). ¿Qué se hace con las fechas de las obligaciones no pagadas ya generadas?
**Opciones:** (a) actualizar las fechas de las no pagadas con auditoría, **recomendada**; (b) que la corrección solo rija para las obligaciones que se generen después; (c) anular y volver a generar las no pagadas.
**Fundamento:** RF-10 dice que la corrección «puede actualizar obligaciones no pagadas, incluidas las vencidas» y CA-22 que «el historial permite reconstruir los valores anteriores y nuevos». La opción (a) cumple eso al pie de la letra; su costo es que dos columnas dejan de ser inmutables y la historia de fechas vive en la auditoría (criterio propio: el principio de entradas inmutables de la fuente del modelo, Fowler, no distingue entre importes y fechas; es una excepción consciente).
**Respuesta del solicitante:** «Actualizar las fechas de las no pagadas, con auditoría (Recomendado)».
**Decisión:** `fecha_vencimiento` y `fecha_limite` pasan a poder actualizarse (solo esas dos columnas, también en el rol de la aplicación) y cada cambio deja en la auditoría su valor anterior y el nuevo. `importe_inicial` sigue sin poder cambiar.

## 2. Qué se escribió
| Operación | Qué hace |
|---|---|
| `reajustar_contrato` | **CA-12:** la fecha efectiva se normaliza al inicio del período siguiente al que contiene la notificación (10 mar–9 abr, notificado el 20 de marzo: rige desde el 10 de abril); las obligaciones anteriores mantienen su monto y las posteriores aplican el nuevo. **CA-51:** en vivienda se exigen el tope vigente y su fuente, que se conservan junto al reajuste. **CA-39:** si el porcentaje supera el tope solo advierte; una vivienda con precio en dólares se rechaza (OL-07) |
| `corregir_contrato` | **CA-22:** condición nueva desde una fecha efectiva, con motivo obligatorio; las pagadas no cambian y las no pagadas, incluidas las vencidas, se actualizan: el importe con ajustes inmutables y, por la decisión 3, las fechas de pago. **CA-40:** un cambio que deje una obligación por debajo de lo abonado se bloquea mostrando el exceso (por ejemplo ₡20.000) y **no cambia nada** |
| `ajustar_manualmente` | RF-09: ajuste manual del importe del último período de un contrato finalizado, con motivo, como ajuste inmutable |
| `selectors.historial_de_importes` | **CA-55:** el importe paso a paso (inicial y cada ajuste con su anterior y su nuevo): el inicial nunca se sobrescribe |
| `selectors.condicion_vigente_en` | La condición que rige en una fecha |

## 3. Propuestas del asistente (sin aprobar)
1. **Notificación:** no puede ser anterior al inicio del contrato ni futura; «el período siguiente» es el primero que inicia **después** de la notificación (si se notifica el mismo día que inicia un período, rige desde el siguiente).
2. **Un reajuste con la misma fecha efectiva que otro se rechaza** («use una corrección»); un reajuste igual al monto actual también.
3. **Se permite un reajuste a la baja** (porcentaje negativo): la ERS solo limita los aumentos.
4. **Tope digitado entre 0 y 100 %** con hasta cuatro decimales; porcentaje de cambio de hasta 9 999,9999 %.
5. **Motivo opcional en el reajuste** (el modelo de datos solo lo exige en las correcciones, aunque RF-10 lo menciona para ambos).
6. **Las obligaciones con un ajuste manual no se tocan** en una corrección o un reajuste posterior, y se avisa cuántas fueron: es una decisión explícita del administrador.
7. **Las obligaciones pagadas** (abonado ≥ importe vigente) no se modifican; las parcialmente pagadas sí, mientras no queden por debajo de lo abonado.
8. **Una corrección con fecha efectiva a mitad de período** aplica desde el primer período que inicia en o después de esa fecha.
9. **Una corrección con la misma fecha efectiva que otra condición** gana la registrada después (así se puede corregir la condición inicial; ver `calculo.condicion_aplicable`).
10. **El ajuste manual** solo para la obligación del último período de un contrato finalizado (RF-09), no para cualquier obligación.

## 4. Lo que no se implementó (y por qué)
- **Error en el período (la fecha de inicio):** RF-10 dice que la corrección corrige «monto, vencimiento o período». Cambiar la fecha de inicio mueve todos los períodos y las obligaciones ya generadas; no está soportado. Alternativa: anular el contrato si no tiene movimientos y crear uno nuevo, o finalizarlo y crear otro. **Pregunta abierta para ti** si lo necesitas.
- **Frecuencia anual del reajuste (OL-06):** la ley, según la ERS, habla de actualizar el precio al final de cada año del contrato; el sistema no lo impone ni lo advierte porque la ERS solo pide advertir el tope. Pendiente de validación por el abogado (DP-17).
- **Obligaciones aún no generadas:** las generará el proceso diario (grupo E) con la condición que rige cada período (`condicion_aplicable`).

## 5. Verificación
- **622 pruebas pasan en Windows** (Python 3.12; 47 nuevas) y **611 en WSL** (Python 3.14.4, Pillow 13.0.0); `makemigrations --check` sin cambios; `verificar.sh` sin fallos. Cobertura de `alquileres`: **99 %** (una línea del modelo sin ejecutar).
- **Casos:** el ejemplo de CA-12 y sus bordes (notificación el primer y el último día del período), el porcentaje a cuatro decimales, tope y fuente (conservados, exigidos, fuera de rango, dentro y exactamente en el tope), dólares con vivienda y con otro destino, dos reajustes seguidos, correcciones con pagadas, vencidas, parcialmente pagadas, ajuste manual previo y último período prorrateado, el bloqueo de **₡100.000 abonados vs. ₡80.000** con el exceso de ₡20.000, el vencimiento corregido siempre dentro del período, la auditoría de los valores anteriores y nuevos, y el historial de importes.
- **Mutaciones manuales, todas detectadas (13):** fecha efectiva igual al período de la notificación, sin exigir el tope, vivienda en dólares aceptada, sin advertencia, tocar las pagadas, sin bloqueo por debajo de lo abonado, corrección sin motivo, sin actualizar las fechas de pago, sobrescribir el ajuste manual, porcentaje sin decimales, sin prorrateo del último período, notificación futura y ajustes a períodos anteriores a la fecha efectiva.
- **Privilegios:** la prueba con SQL directo como el rol de la aplicación ahora permite actualizar las dos fechas y sigue rechazando `importe_inicial`, el período, la moneda, el tipo y `datos_calculo`.

## 6. Qué no está hecho
Obligaciones y proceso diario (E), fotografías (F), pantallas (G) y medición y cierre (H). 0 de 25 CA de la E2 marcados.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
