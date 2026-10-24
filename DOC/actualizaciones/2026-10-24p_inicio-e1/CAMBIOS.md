# Actualización 2026-10-24 (p) — Inicio de la entrega E1 (Inquilinos)

**Fecha:** 2026-10-24
**Documentos afectados:** [`CLAUDE.md`](../../../CLAUDE.md), [`AVANCE_IMPLEMENTACION.md`](../../fase-5-implementacion/AVANCE_IMPLEMENTACION.md), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [README de la fase 5](../../fase-5-implementacion/README.md) y [DOC/README.md](../../README.md). No cambia ningún código ni el plan v0.1.
**Origen:** pregunta del asistente al cerrar la actualización 2026-10-24 (o): «¿Autorizas la E1?»; respuesta del solicitante: **«sí, autorizo la E1»** (24-oct-2026). El plan (sección 3.2) exige una entrega a la vez y CLAUDE.md pedía su autorización expresa
**Estado:** E1 *en curso*; no aprobado (la ERS y el DAS siguen sin aprobar)

## 1. Qué se registró
- **CLAUDE.md** ahora dice que la implementación está autorizada para la E0 (terminada) y la E1; las demás entregas siguen requiriendo autorización expresa.
- **Registro de avance:** E1 *en curso* desde el 24-oct-2026, 0 de 8 CA.
- **Plan de trabajo de la E1** en la lista de tareas, en siete grupos (modelos, registro y ficha, consentimiento, fotografías en el servidor, reducción en el navegador, pantallas, medición y cierre) y las cinco decisiones que la entrega necesita. Es propuesta del asistente derivada de los RF, los CA, el modelo de datos v0.7 y el ADR-003.

## 2. Alcance de la E1 (del plan)
RF-01, 02, 03, 04, 05, 39, 45 y 50; RNF-03 y RNF-15; CA-01, 11, 25, 26, 29, 73, 74 y 83. Criterio de salida: cédula servida solo por la vista con autorización y registrada, acceso denegado sin sesión, y peso de fotos reales de un iPhone y dos teléfonos Android medido y registrado.

## 3. Lo que la E1 no puede cerrar sola (para que no sorprenda)
- **CA-29 (desactivar con contrato vigente):** los contratos llegan en la E2. Se propone un punto de extensión y verificar el bloqueo real en la E2, como se hizo con CA-18; eso requeriría tu aceptación escrita (prioridad Media).
- **CA-67 y la revocación:** en la E1 el texto de cada versión y el aviso en la ficha; el rechazo de contratos nuevos va en la E2 (HI-04) y la solicitud de supresión de oficio, en la E5 (RF-40).
- **Fotos reales:** la medición del peso (CA-73) necesita fotografías de un iPhone y de dos teléfonos Android que tienes que aportar.
- **El texto informativo del consentimiento** es contenido legal pendiente del abogado (DP-21): lo que se escriba es un borrador sin validar.

## 4. Corrección de un error mío en la lista de tareas
Al cerrar la E0 (actualización 2026-10-24 (n)) mi script marcó como hechas las casillas de cierre de **todas** las entregas (E1 a E6) con el texto de la E0, no solo las de la E0. Quedó así publicado en el commit `6fa7d08` y los siguientes. Se restauraron a pendientes las 60 líneas afectadas de E1 a E6 y se comprobó que ninguna casilla de cierre quede marcada fuera de la E0. El registro de avance y el CAMBIOS del cierre no tenían el error.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
