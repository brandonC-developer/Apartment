# Actualización 2026-10-23 (j) — ERS v1.13

**Fecha:** 2026-10-23
**Documentos afectados:** [ERS v1.13](../../fase-1-ers/ERS_SGA_001_v1.13_borrador.md) (nueva; reemplaza a la [v1.12](../../fase-1-ers/ERS_SGA_001_v1.12_borrador.md), que no se edita). Editados en su sitio, porque ninguno está reemplazado ni aprobado, solo para declarar la v1.13 como base y recoger el filtro «Sin frente»: [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md), [Modelo de datos v0.6](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.6_borrador.md), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) y [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md); además los README de las fases 1, 2, 4 y 5 y [DOC/README.md](../../README.md)
**Origen:** [2026-10-23 (i)](../2026-10-23i_dp-30-inquilinos-sin-frente/CAMBIOS.md); el solicitante pidió redactar la v1.13 (23-oct-2026)
**Estado:** borrador; no aprobado

## 1. Cambios en la ERS
| Elemento | Cambio | Origen |
|---|---|---|
| **DP-30** | Pasa de pendiente a **resuelta** (sección 12.2 y nueva 12.1f); sale de la lista de pendientes y de la lista de verificación del cierre | Decisión del solicitante, (i) |
| RF-03 | La lista de inquilinos permite filtrar los «Sin frente»; sin alertas ni correos | (i), pregunta 2 |
| CA-78 | Añade el filtro «Sin frente» (incluye al que solo tiene reverso, sin alerta) y que el inquilino sin frente ni contrato por más de un año recibe la retención de CA-66 | (i), preguntas 1 y 2 |
| RF-01 (nota v1.12) | Remite a la resolución de DP-30 | — |
| RF-41, CA-66 | **Sin cambios**: se aplican tal como están | (i), pregunta 1 |
| Control del documento | Nota de control v1.13, fila 1.13 del historial | — |

Totales: **52 RF, 30 RN, 18 RNF, 78 CA, 21 OL, 30 DP (DP-30 ahora resuelta; sigue habiendo DP-27, DP-28 y DP-29 pendientes entre otras), 31 ADR, 11 RE.** Sin RF ni CA nuevos.

## 2. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido (23-oct-2026):** aplicar RF-41 sin plazo nuevo; indicación en la ficha y filtro «Sin frente» en la lista; sin alertas.
- **Propuesta del asistente, sin decidir:** los textos «Falta el frente» y «Sin frente»; que el filtro incluya a quien solo tiene el reverso.
- Que un año sea un plazo razonable para este caso lo valida el abogado (DP-17).

## 3. Alineación de los demás documentos
Solo se cambió la base declarada y lo mínimo: filtro «Sin frente» en F-01 y en la estrategia de pruebas (CA-78), remisión en el modelo v0.6 (derivado y H19) y en el diseño técnico (pendiente 7). **No se releyeron enteros.** El plan no cambia: CA-78 sigue en la E2.

## 4. Qué no se hizo
- No hay requisitos ni criterios nuevos; no se tocaron RF-41 ni CA-66.
- No se resolvieron DP-27, DP-28 ni DP-29.
- El script comprueba identificadores, enlaces, bases y cobertura, no el contenido; se revisó a mano el texto que citaba DP-30.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
