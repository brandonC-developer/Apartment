# Actualización 2026-10-23 (e) — ERS v1.12

**Fecha:** 2026-10-23
**Documentos afectados:** [ERS v1.12](../../fase-1-ers/ERS_SGA_001_v1.12_borrador.md) (nueva; reemplaza a la [v1.11](../../fase-1-ers/ERS_SGA_001_v1.11_borrador.md), que no se edita); [README de la fase 1](../../fase-1-ers/README.md) y [DOC/README.md](../../README.md). **Los demás documentos no se tocaron** y siguen declarando la v1.11 como base (ver la sección 5)
**Origen:** [2026-10-23 (HT-11)](../2026-10-23_ht-11-perfil-propiedad/CAMBIOS.md), [(c) tope de 5 MiB](../2026-10-23c_unidad-tope-5mb/CAMBIOS.md) y [(d) sin zona temporal](../2026-10-23d_quitar-zona-temporal/CAMBIOS.md); el solicitante pidió redactar la v1.12 (23-oct-2026)
**Estado:** borrador; no aprobado

## 1. Cambios
| Requisito | Cambio | Origen |
|---|---|---|
| RF-02, RF-50, RF-52, CA-73, CA-74, CA-76, sec. 12.1c | "5 MB" pasa a **5 MiB (5 242 880 bytes)**; la cifra en bytes se escribe en RF-02. Las notas de control e historial anteriores no se tocaron: se aclara en la nota v1.12 que allí se lee 5 MiB | (c) |
| RF-01 | El frente es obligatorio **antes de asignar un contrato**, no para guardar al inquilino; se guardan con datos y consentimiento. Registro en dos pasos | (d) |
| RF-03 | La ficha permite agregar o reemplazar el frente y el reverso; la reemplazada se marca eliminada; la ficha indica cuándo falta el frente (indicación propuesta) | (d) |
| RF-07, CA-02 | Se rechaza un contrato con un inquilino sin frente cargado | (d), regla propuesta por el asistente |
| CA-01 | Se guarda el inquilino sin fotografía; ya no exige el frente | (d) |
| **CA-78 (nuevo)** | Registro en dos pasos: contrato rechazado sin frente, frente subido desde la ficha, archivo rechazado sin perder datos | (d) |
| RF-51, RF-52, CA-75, glosario "Perfil de la propiedad" | Contenido del perfil (datos de RF-06, inquilino y contrato vigente, sin historial de contratos); acciones **desactivadas** con el aviso «No hay contrato vigente»; «Reemplazar» si la cara ya existe (en RF-51) | HT-11 |
| **DP-30 (nueva)** | Inquilinos guardados sin frente: lista o aviso, plazo y destino de los no completados | (d) |
| Sec. 12.1e, matriz, lista de verificación | Registro de las decisiones del 23-oct-2026; CA-78 en la matriz; punto nuevo de DP-30 | — |

Totales: **52 RF, 30 RN, 18 RNF, 78 CA, 21 OL, 30 DP, 31 ADR, 11 RE** (ya no hay RF nuevos; CA +1, DP +1).

## 2. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido por el solicitante (23-oct-2026):** los tres puntos del perfil; el tope en 5 MiB; quitar la zona temporal y registrar en dos pasos; "sin contrato hasta tener el frente".
- **Propuesta del asistente, sin decidir:** que la regla del contrato sin frente se aplique en RF-07 y CA-02 tal como está redactada; la indicación "falta el frente" en la ficha; que las acciones desactivadas de RF-52 sigan la misma regla que RF-51; los textos de los avisos; CA-78 (redacción y alcance); DP-30.
- **Pregunta nueva que surge:** en RF-04 y RF-39 no cambia nada, pero un inquilino que quede sin frente y sin contrato puede acumularse (DP-30).

## 3. Qué no se hizo
- **No se alineó ningún otro documento.** El DAS v0.11, el modelo v0.5 (que sigue con `ARCHIVO_TEMPORAL`), el diseño técnico v0.7 (F-01, F-10), la estrategia de pruebas, el plan y el registro de avance siguen describiendo la v1.11. CA-78 no está en la estrategia ni en el plan.
- No se cambió el criterio del objetivo de 2 MB de RF-50 (tiene unidad ambigua; es un objetivo de diseño, no un tope).
- No se cita ninguna obligación legal nueva; DP-17 a DP-21 siguen sin dictamen.

## 4. Verificación
Se ejecutó el script de coherencia; los avisos esperables son los documentos que aún declaran la v1.11 y la falta de CA-78 en la estrategia y el plan (sección 5).

## 5. Lo que sigue (propuesta del asistente)
1. Alinear DAS, diseño técnico, estrategia de pruebas, plan, lista de verificación y avance con la v1.12.
2. Modelo de datos v0.6: sin `ARCHIVO_TEMPORAL`, R24 ni H16; regla del contrato sin frente; ajustar la prueba en PostgreSQL.
3. Resolver DP-30.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
