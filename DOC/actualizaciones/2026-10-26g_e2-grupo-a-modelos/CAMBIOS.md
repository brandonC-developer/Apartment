# Actualización 2026-10-26 (g) — E2, grupo A: modelos y privilegios de `alquileres`

**Fecha:** 2026-10-26
**Documentos afectados:** código en [`src/alquileres/`](../../../src/alquileres/models.py), [`src/sga/privilegios.py`](../../../src/sga/privilegios.py), [`src/sga/settings.py`](../../../src/sga/settings.py), [`src/nucleo/tests_privilegios.py`](../../../src/nucleo/tests_privilegios.py), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** modelo de datos v0.7 (PROPIEDAD, CONTRATO, CONDICION_CONTRATO, OBLIGACION, AJUSTE_OBLIGACION, DOCUMENTO_CONTRATO, EJECUCION_PROCESO; R1, R2, R3, R12, R13, R20 a R23, R27, R28), ADR-014, ADR-016, ADR-027, ADR-030 y ADR-031; decisión 1 de la E2 ([2026-10-26 (f)](../2026-10-26f_decisiones-e2/CAMBIOS.md)); instrucción del solicitante: «hazlo y actualiza toda la documentación y las tareas» (26-oct-2026)
**Estado:** implementado y probado; no aprobado

## 1. Qué se escribió
| Tabla (modelo) | Contenido y restricciones |
|---|---|
| `Propiedad` | Alias obligatorio y único (R20) **sin distinguir mayúsculas** (propuesta); descripción y dirección; `inactiva`. Sin `DELETE` |
| `Contrato` | Inquilino y propiedad (no se borran); destino, fechas, moneda; fin no anterior al inicio; **R2: restricción de exclusión de PostgreSQL** sobre propiedad y rango de fechas inclusivo, abierto si no hay fin, que ignora los contratos anulados (ADR-031); R21: la anulación lleva su motivo. Solo cambian la fecha de fin y la anulación |
| `CondicionContrato` | Historial de monto, vencimiento y gracia; R3 en lo que cabe en una tabla; una sola condición inicial; los datos del reajuste (notificación y porcentaje) solo en reajustes; el tope digitado va con su fuente; la corrección exige motivo. Solo inserción |
| `Obligacion` | R1 (una regular por contrato y período, una apertura por contrato); la apertura sin período y la regular con período ordenado; fecha límite no anterior al vencimiento; importe positivo; anulación con motivo. Solo cambian `anulada_en` y `motivo_anulacion` |
| `AjusteObligacion` | Delta distinto de cero; la corrección y el ajuste manual llevan motivo (R13). Solo inserción (ADR-016) |
| `DocumentoContrato` | R22 y R28: numeradas de 1 a 10 sin repetir; R27: 1 a 5 242 880 bytes y JPEG o PNG; referencia única. Solo inserción, **sin `eliminado_en`** (DP-28 abierta) |
| `AccesoDocumentoContrato` | Decisión 1: tabla propia con una sola clave foránea (R23 por construcción). Solo inserción (R12) |
| `EjecucionProceso` | Fecha local, inicio, fin, resultado (en curso, correcta o fallida) y detalle; al terminar solo se completa el cierre; una terminada lleva su instante |
| Migraciones | `0001_initial` (depende de `inquilinos` y de `nucleo.0004_btree_gist`) y `0002_anulacion_una_sola_vez` |
| `sga/privilegios.py` | Ocho entradas con privilegios mínimos (ver la sección 3); el despliegue aplica ahora **23 tablas** |

## 2. Propuestas del asistente (sin aprobar)
- **Alias sin distinguir mayúsculas** (`Casa 1` y `casa 1` son el mismo alias).
- **Disparadores de PostgreSQL** que impiden cambiar la anulación de un contrato o de una obligación una vez completada: R12 pide «se completa una sola vez» y los privilegios por columna no distinguen la primera vez de la segunda. Lo cubren también con SQL directo.
- **`Contrato` con `RegistroProtegido`:** solo cambian `fecha_fin`, `anulado_en` y `motivo_anulacion`; el resto (inicio, moneda, destino, inquilino, propiedad) no se edita. *Riesgo:* si el solicitante quiere corregir el inicio de un contrato (RF-10, «corrección de período»), habrá que abrir ese campo y decidir cómo se recalculan las obligaciones; lo planteo al llegar al grupo D.
- **`registrada_en`, `registrado_en`, `iniciada_en`** sin valor automático: los pasa el servicio, para poder probar con fechas fijas.
- Longitudes: alias de 60 caracteres, fuente del tope de 200; porcentajes con 4 decimales (`numeric(8,4)`).
- Que `EjecucionProceso` permita varias ejecuciones el mismo día (reintentos).

## 3. Privilegios del rol de la aplicación
| Tabla | Privilegios |
|---|---|
| `alquileres_propiedad` | `SELECT`, `INSERT`, `UPDATE` (sin `DELETE`: se marca inactiva) |
| `alquileres_contrato` | `SELECT`, `INSERT`; `UPDATE` solo de `fecha_fin`, `anulado_en` y `motivo_anulacion` |
| `alquileres_condicioncontrato`, `alquileres_ajusteobligacion`, `alquileres_documentocontrato`, `alquileres_accesodocumentocontrato` | `SELECT`, `INSERT` (R12) |
| `alquileres_obligacion` | `SELECT`, `INSERT`; `UPDATE` solo de `anulada_en` y `motivo_anulacion` (el importe inicial nunca) |
| `alquileres_ejecucionproceso` | `SELECT`, `INSERT`; `UPDATE` solo de `terminada_en`, `resultado` y `detalle` |

## 4. Verificación
- **467 pruebas pasan en Windows** (Python 3.12; 57 nuevas) y **456 en WSL** (Python 3.14.4, Pillow 13.0.0); `makemigrations --check` sin cambios; el despliegue aplicó las migraciones con el rol dueño y los privilegios a 23 tablas; `verificar.sh` sin fallos.
- Se prueba: alias; moneda, destino, fechas y anulación del contrato; **el solape** (día compartido en cualquier borde, contrato abierto, relevo contiguo, propiedades distintas, anulados que no cuentan y alargar un fin hasta solapar); la protección de las filas con Django y **con SQL directo como el rol de la aplicación**; las condiciones, las obligaciones, los ajustes, las fotografías (de 1 a 10, peso y tipo), los accesos y la ejecución del proceso.
- **Mutaciones manuales, todas detectadas (5):** rango semiabierto en el solape (el último día dejaba de contar), que los contratos anulados cuenten, quitar el disparador de la anulación, dar `UPDATE` completo del contrato y subir el máximo de fotografías de 10 a 11 en la migración.

## 5. Hallazgos
1. **Las pruebas de modelos corren contra las migraciones, no contra el modelo:** para mutar una restricción hay que cambiar la migración (lo hice así). La primera mutación del máximo de fotografías no se aplicó porque el formato de la migración era distinto; se repitió bien.
2. **R23 deja de ser una restricción:** con la decisión 1 queda cumplida por construcción. El modelo de datos v0.8 (pendiente) debe decirlo.
3. **`btree_gist` ya estaba creada** por una migración de `nucleo` (E0); `alquileres` depende de ella.

## 6. Qué no está hecho
Cálculo de períodos (B), servicios de propiedades y contratos (C), reajuste y corrección (D), obligaciones y proceso diario (E), fotografías (F), pantallas (G) y medición y cierre (H). 0 de 25 CA de la E2.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
