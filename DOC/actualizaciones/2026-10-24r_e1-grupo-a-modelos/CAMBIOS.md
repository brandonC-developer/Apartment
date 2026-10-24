# Actualización 2026-10-24 (r) — E1, grupo A: modelos y privilegios de `inquilinos`

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/inquilinos/`](../../../src/inquilinos/models.py), [`src/nucleo/models.py`](../../../src/nucleo/models.py), [`src/sga/privilegios.py`](../../../src/sga/privilegios.py), [`src/sga/settings.py`](../../../src/sga/settings.py), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** modelo de datos v0.7 (INQUILINO, TEXTO_CONSENTIMIENTO, CONSENTIMIENTO, DOCUMENTO_IDENTIDAD, ACCESO_DOCUMENTO; R12, R14, R23, R25, R27), ERS RF-01, RF-02, RF-39 y RF-45, ADR-027, ADR-028 y ADR-030; plan de trabajo de la E1 (grupo A); instrucción del solicitante: «sí, escribe el grupo A» (24-oct-2026)
**Estado:** implementado y probado; no aprobado

## 1. Qué se escribió
| Pieza | Contenido |
|---|---|
| `inquilinos.Inquilino` | Nombre y número de documento obligatorios salvo en un desasociado, que no conserva ningún dato personal (RF-41); tipo de documento restringido a cédula, DIMEX, pasaporte u otro; teléfono y correo opcionales; `activo`; **índice por tipo y número de documento, no único**: el duplicado es una advertencia del servicio, no un bloqueo (RF-01, CA-25) |
| `inquilinos.TextoConsentimiento` | Versión única e inmutable del texto; con `borrador` verdadero hasta que un abogado lo valide (decisión del solicitante del 24-oct-2026) |
| `inquilinos.Consentimiento` | Apunta a la versión mostrada; medio físico o electrónico; solo se puede registrar la revocación, que no puede ser anterior al consentimiento |
| `inquilinos.DocumentoIdentidad` | Una fotografía activa por cara (R25, restricción parcial única); peso entre 1 byte y 5 242 880 y tipo JPEG o PNG (R27, segunda defensa); nombre de archivo único; solo se puede marcar como eliminada |
| `inquilinos.AccesoDocumento` | Quién, cuándo y qué acción (consulta o descarga) sobre una cédula, sin la imagen; solo inserción (R12) |
| `nucleo.models.RegistroProtegido` | Base reutilizable de las tablas protegidas: `CAMPOS_ACTUALIZABLES` lista las únicas columnas que cambian; bloquea `delete()` y el `update()` de otras columnas, y `save()` sin `update_fields`. **`Auditoria` pasó a usarla** (mismo comportamiento) |
| `sga/privilegios.py` | Las cinco tablas con sus privilegios mínimos (ver la sección 3) |
| Migración | `inquilinos/0001_initial.py` |

## 2. Propuestas del asistente (sin aprobar)
- **Campos y restricciones del modelo que el MDD no detalla:** `nombre_completo` y `numero_documento` admiten nulo solo para el desasociado; `borrador` en el texto; `referencia_archivo` única; `CHECK` de cara, medio y acción; revocación no anterior al consentimiento.
- **Textos y longitudes:** nombre de 200 caracteres, número de documento de 60, teléfono de 40, correo de 254 (el correo se guarda como texto y se validará en el servicio).
- **`on_delete=PROTECT`** entre todas las claves foráneas: ni la base ni Django dejan borrar un inquilino con fotografías o consentimientos, ni una versión del texto con consentimientos.
- `RegistroProtegido` como mecanismo común en lugar de repetir las guardas en cada modelo.

## 3. Privilegios del rol de la aplicación
| Tabla | Privilegios |
|---|---|
| `inquilinos_inquilino` | `SELECT`, `INSERT`, `UPDATE` (sin `DELETE`: se desactiva y la retención desasocia con `UPDATE`) |
| `inquilinos_textoconsentimiento` | `SELECT`, `INSERT` |
| `inquilinos_consentimiento` | `SELECT`, `INSERT`; `UPDATE` solo de `revocado_en` |
| `inquilinos_documentoidentidad` | `SELECT`, `INSERT`; `UPDATE` solo de `eliminado_en` |
| `inquilinos_accesodocumento` | `SELECT`, `INSERT` (R12) |

## 4. Hallazgo para la E2 (no decidido)
El modelo de datos hace que **`ACCESO_DOCUMENTO` apunte a dos tablas**: la cédula (`DOCUMENTO_IDENTIDAD`, de `inquilinos`) o la fotografía de un contrato (`DOCUMENTO_CONTRATO`, de `alquileres`; R23, RF-52). Pero el ADR-030 pone `alquileres` por encima de `inquilinos`: una clave foránea de `inquilinos.AccesoDocumento` hacia `alquileres` crearía un ciclo de migraciones. Por eso **la E1 solo modela el acceso a la cédula**. Opciones para la E2, a decidir con el solicitante cuando llegue: (a) una tabla `AccesoDocumentoContrato` propia en `alquileres`; (b) mover el acceso a una aplicación sin dependencias hacia arriba; (c) una referencia sin clave foránea con la integridad en el servicio. Mi inclinación es (a), pero no se decide ahora. Además R23 («exactamente uno de los dos») dejaría de ser una restricción de una tabla.

## 5. Verificación
- **237 pruebas pasan** (26 nuevas) en Windows con Python 3.12 y **en WSL con Python 3.14.4, sin ninguna omitida**; `makemigrations --check` sin cambios; el despliegue aplicó la migración con el rol dueño; `verificar.sh` sin fallos.
- Se prueba: campos obligatorios y desasociado sin datos personales; tipo de documento; duplicado permitido en la base; unicidad y reemplazo de la fotografía activa por cara; peso (1, 5 242 880, 0 y 5 242 881) y tipo real; versiones únicas, con contenido e inmutables; consentimiento con medio válido y revocación no anterior; no se puede borrar un inquilino ni una versión con dependientes ni siquiera con SQL directo; los accesos solo se insertan; y, **con SQL directo como el rol de la aplicación**, las cinco tablas rechazan lo que no está permitido.
- **Mutaciones manuales, todas detectadas:** dar `UPDATE` sobre los accesos, dar `UPDATE` de toda la fotografía, permitir en la guarda de Django cambiar el tamaño, quitar la unicidad de la fotografía activa por cara y quitar el tope de 5 MiB (en la migración).
- Errores míos corregidos en el camino: una prueba suponía que la clave foránea se comprueba al instante (Django las deja diferidas hasta confirmar) y un ayudante sobrante.

## 6. Qué no está hecho
Servicios de registro y ficha (grupo B), el texto y el registro del consentimiento (C), las fotografías en el servidor con Pillow (D), el script del navegador (E), las pantallas (F) y la medición con fotos reales (G). 0 de 8 CA de la E1.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
