# Actualización 2026-10-24 (t) — E1, grupo C: consentimiento

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/inquilinos/`](../../../src/inquilinos/textos.py), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS RF-39, OL-13, RF-40, RF-41, RF-44, CA-67; Ley 8968, art. 5; decisión 1 de la E1 (actualización [2026-10-24 (q)](../2026-10-24q_decisiones-e1/CAMBIOS.md)); instrucción del solicitante: «sí, escribe el grupo C» (24-oct-2026)
**Estado:** implementado y probado; **el texto es un borrador sin validar por abogado**; no aprobado

## 1. Fuente del artículo 5, y qué se leyó
Se leyó el **texto completo del art. 5 de la Ley 8968** en la copia del MICITT ([PDF](https://www.micitt.go.cr/sites/default/files/marco_juridico_legal/08.%20Ley%20n.%C2%B0%208968%20Ley%20de%20Protecci%C3%B3n%20de%20la%20Persona%20frente%20al%20tratamiento%20de%20sus%20datos%20personales..pdf), generada el 7-ene-2026 desde la página oficial), extraído con `pdftotext`; el sitio oficial (SCIJ/Sinalevi) no entrega el texto a una consulta automática. **Lo leído:** el punto 1.- «Obligación de informar» con los incisos a) a h) (existencia de la base, fines, destinatarios y quiénes la consultan, carácter obligatorio o facultativo, tratamiento, consecuencias de la negativa, derechos, identidad y dirección del responsable), el punto 2.- «Otorgamiento del consentimiento» (expreso, por escrito físico o electrónico, revocable de la misma forma sin efecto retroactivo) y la prohibición de acopiar datos sin consentimiento informado. **No se verificó** que esa copia coincida con la redacción vigente publicada en La Gaceta. **No es asesoría legal.**

## 2. Qué se escribió
| Pieza | Qué hace |
|---|---|
| `inquilinos/textos.py` | El **borrador** del texto, con los ocho puntos en el orden del artículo y el consentimiento al final; empieza con «BORRADOR SIN VALIDAR POR UN ABOGADO»; el punto 8 lleva el nombre y la dirección del responsable; no se puede generar sin ellos |
| `services.crear_version_texto` | Guarda el texto como la versión siguiente (nace como borrador), no crea otra si el contenido es idéntico y deja el evento `texto_consentimiento_cargado`. Las versiones anteriores no se tocan |
| `manage.py cargar_texto_consentimiento` | Genera el borrador desde la identidad del responsable de la organización; con `--archivo` carga el texto del abogado y con `--validado` lo marca como validado |
| `services.revocar_consentimiento` | Marca el consentimiento vigente como revocado **sin cambiar ni borrar ningún dato ni fotografía** (sin efecto retroactivo), deja el evento `consentimiento_revocado` sin datos personales y ejecuta los ganchos en la misma transacción |
| `inquilinos/ganchos.py` | `al_revocar`: funciones de otras aplicaciones que se ejecutan al revocar (la E5 registrará la que abre de oficio la solicitud de supresión); si una falla, la revocación se deshace |
| `selectors` | `consentimiento_vigente`, `tiene_consentimiento_vigente` y, en la ficha, `consentimiento_vigente`, `consentimiento_revocado` (aviso) y `puede_crear_contratos` |

## 3. El texto: qué dice y qué marqué para el abogado
El borrador informa de: la base «Sistema de Gestión de Alquileres»; los fines (identificar y verificar al inquilino, administrar contrato, obligaciones y pagos, contacto manual por el administrador, obligaciones legales; sin publicidad ni venta); los destinatarios (solo el administrador con segundo factor; el proveedor de alojamiento y las copias cifradas en Estados Unidos; el servicio de correo que envía avisos al administrador sin documento ni imágenes); lo obligatorio (nombre, tipo y número de documento y, antes de un contrato, el frente) y lo facultativo (teléfono, correo, reverso); el tratamiento y los plazos de conservación de la ERS (cinco años tras el fin del contrato, un año sin contrato); las consecuencias de negarse; los derechos y el plazo de cinco días hábiles; y el responsable. Cada punto se apoya en la ERS v1.16, no en el artículo, que solo fija **qué** informar.
**Marcado dentro del texto «[A VALIDAR POR EL ABOGADO: …]»:** si el alojamiento y el correo en el extranjero son una transferencia y qué debe decir el punto 3 (DP-31); los plazos de conservación frente a obligaciones contables o tributarias (DP-18); el alcance de la supresión y la información sobre la Agencia (DP-18). El abogado puede cambiar cualquier otra cosa: **todo el texto es una propuesta mía.**

## 4. Propuestas del asistente (sin aprobar)
- La estructura y la redacción del texto, incluidas la frase final del consentimiento y mencionar a la Agencia de Protección de Datos de los Habitantes (nombre tomado de las notas del proyecto, no verificado en el artículo).
- Que el texto lleve el nombre y la dirección del responsable **dentro del contenido**: así el consentimiento apunta al texto exacto que se mostró; si el responsable cambia, hay que cargar una versión nueva.
- Los ganchos como mecanismo de la revocación (en vez de que `inquilinos` importe a `privacidad`, lo que rompería el ADR-030).
- Que el comando `cargar_texto_consentimiento` sea la única vía de cargar versiones, sin pantalla (igual que `configurar_organizacion`).

## 5. Verificación
- **297 pruebas pasan** (24 nuevas) en Windows con Python 3.12 y **en WSL con Python 3.14.4, sin ninguna omitida**; `makemigrations --check` sin cambios.
- Se prueba: los ocho puntos presentes y en orden, el responsable en el punto 8, la marca de borrador y los avisos al abogado, obligatorio frente a facultativo, que el texto **no afirme que cumpla la ley**, que sin identidad no se genere; versiones (la 1 como borrador, sin duplicar, una validada es una versión nueva); el comando; la revocación sin efecto retroactivo (los datos del inquilino y sus fotografías quedan idénticos), su auditoría sin datos personales, el aviso de la ficha, no revocar dos veces, ganchos en la misma transacción que se deshacen si uno falla; y CA-67 primera parte (la ficha muestra el texto exacto de la versión consentida aunque haya una nueva).
- **Mutaciones manuales, todas detectadas:** no ejecutar los ganchos, revocar sin exigir un consentimiento vigente, quitar un punto del texto, que la ficha no avise, quitar la marca de borrador y hacer que el texto afirme que cumple la ley.

## 6. Qué no está hecho
Mostrar el texto y registrar el consentimiento en una pantalla (grupo F), las fotografías en el servidor (D), el script del navegador (E) y la medición (G). El rechazo de contratos nuevos tras una revocación es de la E2 y la solicitud de supresión de oficio, de la E5. **Falta que tú definas el nombre y la dirección del responsable** (`configurar_organizacion`) y cargues el borrador (`cargar_texto_consentimiento`). 0 de 8 CA de la E1.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
