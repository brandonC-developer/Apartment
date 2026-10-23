# Actualización 2026-10-23 (l) — ERS v1.14

**Fecha:** 2026-10-23
**Documentos afectados:** [ERS v1.14](../../fase-1-ers/ERS_SGA_001_v1.14_borrador.md) (nueva; reemplaza a la [v1.13](../../fase-1-ers/ERS_SGA_001_v1.13_borrador.md), que no se edita). Editados en su sitio, porque ninguno está reemplazado ni aprobado, para declarar la v1.14 como base y recoger el máximo de 10 fotografías: [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md), [Modelo de datos v0.6](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.6_borrador.md) (solo base y una nota), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) y [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md); además los README de las fases 1, 2, 4 y 5 y [DOC/README.md](../../README.md)
**Origen:** [2026-10-23 (k)](../2026-10-23k_dp-29-fotos-contrato/CAMBIOS.md); el solicitante pidió redactar la v1.14 (23-oct-2026)
**Estado:** borrador; no aprobado

## 1. Cambios en la ERS
| Elemento | Cambio | Origen |
|---|---|---|
| RF-52 | Máximo de **10 fotografías por contrato** (la número 11 se rechaza); la reducción parte de **3508 px y calidad 0,85** (ya no de los valores de RF-50); peso objetivo, pasos de calidad y valores definitivos se fijan al medir en la **E2** (antes decía E1 en DP-29) | Decisión del solicitante, (k) |
| CA-76 | Añade que la fotografía número 11 se rechaza con un mensaje que indica el máximo y se conservan las 10 anteriores | (k) |
| **DP-29** | **Dividida:** máximo resuelto; cifras definitivas abiertas hasta medir en la E2. Sigue en la lista de pendientes y en la de verificación del cierre | (k) |
| Sección 12.1g, nota de control v1.14, historial | Registro de las dos decisiones | — |

Totales: **52 RF, 30 RN, 18 RNF, 78 CA, 21 OL, 30 DP, 31 ADR, 11 RE.** Sin RF, CA ni DP nuevos.

## 2. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido (23-oct-2026):** máximo de 10 fotografías; 3508 px y calidad 0,85 como punto de partida.
- **Propuesta del asistente, sin decidir:** que el máximo se aplique también con un `CHECK` en la base (modelo v0.7); el peso objetivo (a medir); que 300 ppp sea la referencia de legibilidad.
- **Sin fuente:** el 10 (no se encontró un modelo oficial de contrato). Los 3508 px se apoyan en guías de OCR de escáneres (Illinois, Hyland), leídas por resumen y que no prueban nada para fotos con teléfono.

## 3. Alineación de los demás documentos
Solo base y lo mínimo: diseño técnico (F-10: 3508 px y máximo de 10), estrategia de pruebas (CA-76: la número 11), DAS (nota sobre el máximo y las cifras en la E2) y una **nota** en el modelo v0.6: `DOCUMENTO_CONTRATO` todavía no expresa el máximo. No se releyeron enteros.

## 4. Qué no se hizo
- **Modelo de datos v0.7** con el límite de 10 en `DOCUMENTO_CONTRATO` y su prueba en PostgreSQL: pendiente. Hasta entonces el modelo no lo expresa.
- No se midió ninguna foto real; las cifras definitivas siguen abiertas (DP-29).
- No se resolvieron DP-27 ni DP-28.
- El script comprueba identificadores, enlaces, bases y cobertura, no el contenido.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
