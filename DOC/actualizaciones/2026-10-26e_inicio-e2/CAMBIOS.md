# Actualización 2026-10-26 (e) — Inicio de la entrega E2 (Contratos y obligaciones)

**Fecha:** 2026-10-26
**Documentos afectados:** [`CLAUDE.md`](../../../CLAUDE.md), [`AVANCE_IMPLEMENTACION.md`](../../fase-5-implementacion/AVANCE_IMPLEMENTACION.md), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [README de la fase 5](../../fase-5-implementacion/README.md) y [DOC/README.md](../../README.md). No cambia ningún código ni el plan v0.1.
**Origen:** pregunta del asistente al cerrar la E1 (actualización [2026-10-26 (d)](../2026-10-26d_cierre-e1/CAMBIOS.md)): «¿Autorizas la E2?»; respuesta del solicitante: **«autorizo la E2»** (26-oct-2026). El plan (sección 3.2) exige una entrega a la vez y CLAUDE.md pedía su autorización expresa
**Estado:** E2 *en curso*; no aprobado (la ERS y el DAS siguen sin aprobar)

## 1. Qué se registró
- **CLAUDE.md** ahora dice que la implementación está autorizada para la E0 y la E1 (terminadas) y la E2; las demás entregas siguen requiriendo autorización expresa.
- **Registro de avance:** E2 *en curso* desde el 26-oct-2026, 0 de 25 CA.
- **Plan de trabajo de la E2** en la lista de tareas, en ocho grupos (modelos, cálculo de períodos e importes, propiedades y contratos, reajuste y corrección, obligaciones y proceso diario, fotografías, pantallas, medición y cierre). Es propuesta del asistente derivada de los RF, los RN, los CA, el modelo de datos v0.7 y el plan; no está aprobada.

## 2. Alcance de la E2 (del plan)
RF-06 a RF-12, RF-14, RF-36, RF-42, RF-43, RF-48, RF-51 y RF-52; RNF-04 y RNF-16; 25 CA (CA-02, 03, 10, 12, 14, 22, 24, 30, 31, 32, 36, 39, 40, 49, 50, 51, 55, 62, 63, 67, 75, 76, 77, 78 y 82). Criterio de salida: proceso diario idempotente (dos ejecuciones sin duplicados) y casos de fin de mes, bisiesto, prorrateo y gracia que pasan.

## 3. Lo que la E2 trae de la E1 (para que no sorprenda)
- **CA-29 real:** el bloqueo de desactivar a un inquilino por contrato vigente se registra en `inquilinos.bloqueos` (decisión 5 de la E1); el de saldos pendientes es de la E3. Hace falta **tu aceptación escrita** al cerrar la E2 para esa parte.
- **CA-67 completo:** rechazo de contratos nuevos con un inquilino que revocó el consentimiento.
- **CA-18, parte de contratos en USD:** diferida desde la E0 por tu aceptación.
- **CA-82:** la medición de la reducción en el navegador ya tiene un primer dato (cinco fotos, sin GPS ni EXIF) de la actualización 2026-10-26 (d); la E2 la repite con la fotografía del contrato, cuyo lado de partida es 3508 px (DP-29).
- **Hallazgo de la E1 sin decidir:** el acceso a la fotografía del contrato crearía un ciclo de migraciones (actualización [2026-10-24 (r)](../2026-10-24r_e1-grupo-a-modelos/CAMBIOS.md), sección 4). Es la **decisión 1** de la E2, que se pregunta aparte.
- **Dependencias abiertas que no son defectos:** DP-28 (conservación de la fotografía del contrato; mientras no se decida, no se borra), la retención de DP-18 y la validación del abogado.

## 4. Qué no se hizo
No se escribió código. Las decisiones de la E2 se preguntan una por una y se registrarán en la actualización 2026-10-26 (f).

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
