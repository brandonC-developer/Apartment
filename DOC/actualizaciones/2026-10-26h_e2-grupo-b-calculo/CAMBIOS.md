# Actualización 2026-10-26 (h) — E2, grupo B: cálculo de períodos, vencimientos y prorrateo

**Fecha:** 2026-10-26
**Documentos afectados:** código en [`src/alquileres/calculo.py`](../../../src/alquileres/calculo.py) y [`tests_calculo.py`](../../../src/alquileres/tests_calculo.py), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS RN-03, RN-05, RN-06, RN-12, RN-13, RF-09, RF-11 y RF-14; modelo de datos v0.7 (sección 3.3, condición aplicable a un período; sección 12, ejemplo 300 000 × 11 / 31 = 106 452 y empates de H5); instrucción del solicitante: «sí, escribe el grupo B» (26-oct-2026)
**Estado:** implementado y probado; no aprobado

## 1. Qué se escribió
Un módulo de **funciones puras** (sin base de datos, reloj ni zona horaria): las fechas son `date` y los importes `Decimal`; un `float` se rechaza.

| Función | Regla |
|---|---|
| `periodo(fecha_inicio, n)` | RN-03: el día ancla es el de `fecha_inicio`; cada período empieza ese día o el último del mes si no existe, y termina el día anterior al inicio del siguiente. **El ancla sale siempre de `fecha_inicio`**: un contrato del 31 vuelve al 31 en los meses que lo tienen |
| `periodo_que_contiene`, `periodos` | Período de una fecha (nulo si es anterior al inicio) y recorrido sucesivo |
| `vencimiento(periodo, dia)` | RN-05: el día en el mes de inicio, o el último del mes; si es anterior al inicio, el mes siguiente; si excede el último día del período, ese último día |
| `fecha_limite` | RN-06: vencimiento más días de gracia |
| `condicion_aplicable` | La condición de mayor `vigente_desde` que no supere el inicio del período (MDD 3.3) |
| `redondear` | RN-12: colones a la unidad y dólares a dos decimales, **`ROUND_HALF_UP` explícito** |
| `prorratear_ultimo_periodo` | RN-12: `monto × días cobrables / días del período`, ambos extremos inclusivos, en aritmética exacta (`Fraction`) y **un solo redondeo al final**; no prorratea si la fecha de fin es el último día del período; devuelve el importe, el delta y los datos de RN-13 |

## 2. Propuestas del asistente (sin aprobar)
- **Empate de `vigente_desde`** en `condicion_aplicable`: gana la condición registrada después (mayor `id`). Una corrección con la misma fecha efectiva que la anterior es el caso real; el modelo de datos no dice qué pasa.
- **`importe_previo`** de `datos_calculo` como texto con 6 decimales (solo descriptivo; el cálculo usa la fracción exacta).
- **El delta del prorrateo puede ser cero** (por ejemplo 29/30 de 1 colón redondea a 1): `AjusteObligacion` no admite un delta cero, así que el servicio del grupo C **no debe registrar un ajuste** en ese caso. Lo dejé documentado en la clase.
- Ningún valor numérico nuevo: todo sale de la ERS.

## 3. Verificación
- **41 pruebas nuevas; 508 pasan en Windows** (Python 3.12) y **497 en WSL** (Python 3.14.4, Pillow 13.0.0); `verificar.sh` sin fallos. Cobertura del módulo: **100 %** de líneas y ramas.
- **Casos:** el ejemplo de RN-03 (inicio el 10 de enero); inicio el 29, 30 y 31; febrero común y bisiesto; el 29 de febrero de 2028 y su año siguiente; cambio de año; los períodos **contiguos y de 28 a 31 días para los 31 días de ancla, los doce meses y cuatro años (2026, 2027, 2028 y 2100, que no es bisiesto)**; `periodo_que_contiene` contra el recorrido día a día; el vencimiento dentro del período para todo día y todo ancla; el ejemplo del modelo 300 000 × 11 / 31 = 106 452; empates en colones (0,5 → 1) y en dólares (1,005 → 1,01), donde el redondeo al par daría otro valor; un único redondeo (100 × 7 / 30 = 23,33 y no 23,31); y que no se acepta `float`.
- **Mutaciones manuales, todas detectadas (9):** limitar el ancla a 30, fin del período exclusivo, vencimiento sin salto al mes siguiente, vencimiento sin tope del período, redondeo al par, días cobrables sin el día inclusivo, prorratear el período completo, el empate de condiciones por el id menor y redondear el importe diario antes de multiplicar.

## 4. Hallazgos
1. **El ejemplo de RN-12 sale bien** y las pruebas de H5 se confirman con `Fraction`: el modo por omisión de `Decimal` (al par) habría dado 1,00 en lugar de 1,01.
2. **La fecha límite no se acota al período:** RN-06 solo suma los días de gracia; con vencimiento el 29 de un período corto y 7 días de gracia la fecha límite cae en el período siguiente. Es lo que dice la ERS; lo anoto por si el solicitante lo quiere distinto.

## 5. Qué no está hecho
Servicios de propiedades y contratos (C), reajuste y corrección (D), obligaciones y proceso diario (E), fotografías (F), pantallas (G) y medición y cierre (H). 0 de 25 CA de la E2.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
