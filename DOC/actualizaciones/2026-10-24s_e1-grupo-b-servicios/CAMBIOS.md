# Actualización 2026-10-24 (s) — E1, grupo B: registro, ficha y estado del inquilino

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/inquilinos/`](../../../src/inquilinos/services.py), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS RF-01, RF-02, RF-03, RF-04, RF-05, RF-28, RF-39; CA-01, CA-25, CA-29 y CA-53; modelo de datos v0.7; ADR-030 (servicios y selectores); decisiones de la E1 del 24-oct-2026 (actualización [2026-10-24 (q)](../2026-10-24q_decisiones-e1/CAMBIOS.md)); instrucción del solicitante: «sí, escribe el grupo B» (24-oct-2026)
**Estado:** implementado y probado; sin pantallas; no aprobado

## 1. Qué se escribió
| Pieza | Qué hace |
|---|---|
| `services.registrar_inquilino` | Valida y guarda al inquilino con su consentimiento (versión del texto, medio y fecha) en **una transacción** con dos eventos de auditoría; sin fotografías. Obligatorios: nombre completo, tipo y número de documento y el consentimiento (RF-01, RF-39); teléfono y correo opcionales |
| Advertencia de duplicado | Si hay un **inquilino activo** con el mismo tipo y número de documento, lanza `DocumentoDuplicado` **sin guardar**; se guarda al repetir con `confirmar_duplicado` (CA-25: advierte antes de guardar y no bloquea). Mismo aviso al cambiar la identificación y al reactivar |
| `services.actualizar_inquilino` | Solo valida los campos enviados y solo guarda y audita los que cambian; no toca a un inquilino desasociado; bloquea la fila durante el cambio |
| `services.desactivar_inquilino` y `reactivar_inquilino` | Desactivar no borra nada (el historial queda); consulta el punto de extensión y se bloquea con cualquier motivo (CA-29, mecanismo) |
| `inquilinos.bloqueos` | Punto de extensión: cada aplicación registra una función que recibe al inquilino y devuelve los motivos de bloqueo. La E1 no registra ninguna real; la E2 aporta «contrato vigente» y la E3, «saldos pendientes» |
| `selectors.listar_inquilinos` | Activos, inactivos o todos; búsqueda por nombre, documento, teléfono y correo sin distinguir mayúsculas; filtro «sin frente» (incluye a quien solo tiene el reverso o ninguna fotografía); **una sola consulta**; no lista a los desasociados |
| `selectors.obtener_ficha` y `texto_vigente` | Datos, último consentimiento con su texto, fotografías activas por cara y `falta_frente`. El contrato vigente, las obligaciones y el historial (RF-05) llegan con la E2 y la E3 |

## 2. Auditoría (RF-28, CA-53)
Eventos nuevos: `inquilino_registrado`, `consentimiento_otorgado`, `inquilino_actualizado`, `inquilino_desactivado` e `inquilino_reactivado`, con el actor, la IP, la fecha y hora. **De los campos personales solo consta que cambiaron**: se comprobó que ni el nombre, el documento, el teléfono ni el correo aparecen en ningún registro, y que `activo`, la versión del texto y el medio sí constan con su valor. Las lecturas (lista y ficha) no se auditan (RF-45).

## 3. Propuestas del asistente (sin aprobar)
- **Formato del teléfono** (RF-02 pide validar el formato de contacto sin definirlo): al menos 6 dígitos y solo dígitos, espacios, `+`, `-`, `(`, `)` o punto, hasta 40 caracteres.
- **Formato del correo:** el validador de direcciones de Django, hasta 254 caracteres. El número de documento solo se exige no vacío (hasta 60 caracteres): no se inventó un formato por tipo.
- **El servicio no recibe la petición:** recibe el actor y la IP; las vistas del grupo F se los pasan.
- **Excepciones** `ErrorDeValidacion`, `DocumentoDuplicado` y `NoSePuedeDesactivar` para que la pantalla muestre mensajes y la advertencia.
- **La búsqueda incluye teléfono y correo**, no solo nombre y documento.
- Reactivar también avisa del duplicado.

## 4. Verificación
- **273 pruebas pasan** (36 nuevas) en Windows con Python 3.12 y **en WSL con Python 3.14.4, sin ninguna omitida**.
- Se prueba, entre otras cosas: CA-01 (guarda sin fotografía, teléfono ni correo), cada campo obligatorio vacío y que no queda nada guardado, sin consentimiento o con un medio o fecha inválidos, formatos, CA-25, solo cuentan los activos del mismo tipo y número, CA-53 (qué cambió, quién y cuándo, sin valores), atomicidad (si la auditoría falla no queda nada), CA-29 en su mecanismo con una o varias comprobaciones, historial intacto al desactivar, y la lista (búsqueda, estados, desasociados, «sin frente», una sola consulta, intento de inyección SQL sin efecto).
- **Mutaciones manuales, todas detectadas:** contar inactivos como duplicados, no exigir el consentimiento, guardar el teléfono en la auditoría, ignorar los bloqueos, que «sin frente» cuente el reverso y auditar aunque nada cambie.

## 5. Qué no está hecho
El texto del consentimiento y su revocación (grupo C), las fotografías en el servidor (D), el script del navegador (E), las pantallas, con los mensajes y la advertencia de duplicado a la vista (F) y la medición con fotos reales (G). **0 de 8 CA de la E1**: CA-01, CA-25 y CA-53 tienen su servicio probado pero se dan por cumplidos cuando exista la pantalla o el flujo completo y la integración continua esté en verde.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
