# Actualización 2026-10-23 (v) — DAS v0.12: consolidación

**Fecha:** 2026-10-23
**Documentos afectados:** [DAS v0.12](../../fase-2-arquitectura/DAS_SGA_001_v0.12_borrador.md) (nuevo; reemplaza a la [v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md), que no se edita). Editados en su sitio, solo para declarar la v0.12 como base: [Modelo de datos v0.7](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.7_borrador.md), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) y [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md); además los README de las fases 2, 5 y 6 y [DOC/README.md](../../README.md)
**Origen:** recomendación 1 de la [investigación de la documentación núcleo](../2026-10-23u_investigacion-documentacion-nucleo/CAMBIOS.md); el solicitante pidió consolidar el DAS v0.12 (23-oct-2026)
**Estado:** borrador; no aprobado

## 1. Qué es "consolidar"
El DAS v0.11 había acumulado "ajustes sin versión nueva" de los días 21 a 23-oct-2026 en el historial, en los ADR y en el anexo. La v0.12 los integra en el cuerpo y deja una sola lectura. **No cambia ninguna decisión ya tomada.** El detalle, las fuentes y la trazabilidad de cada una siguen en su `CAMBIOS.md`.

## 2. Cambios
| Parte | Cambio |
|---|---|
| Encabezado e historial | Párrafo inicial reescrito; el historial pasa de unas 20 líneas apiladas a una lista breve por versión; los ajustes "sin versión nueva" ya no figuran como tales |
| ADR-003, 008, 013, 023, 024, 026, 027 | Las viñetas "Ajuste v0.10 / v0.11 / punto 3 / fase 5 / etapas" pasan a llevar un título descriptivo (por ejemplo, "Vigilancia del proceso diario", "Etapas de despliegue", "Rol de respaldos", "Tres roles y autenticación `peer`"); el ADR-027 ya no dice "dos roles" y luego "tres" |
| ADR-023 | El firewall del servidor pasa de "se recomienda" a "se mantienen los dos con las mismas reglas"; "endurecimiento sin investigar" se sustituye por la remisión al ADR-032 |
| **ADR-032 (nuevo)** | Endurecimiento del servidor: las seis medidas decididas el 23-oct-2026 (SSH, firewall, actualizaciones, servicios y systemd, HTTPS y cabeceras, Django y secretos), con fundamento, lo propuesto, lo no verificado y lo pendiente |
| Sección 7.7 | Inquilinos sin frente (DP-30, ERS v1.13) |
| Sección 8 | Nueva entidad "Documento del contrato"; el documento de identidad se sube directo a la ficha; el registro de acceso cubre ambos tipos de documento |
| **Sección 10.7 (nueva)** | Registro del inquilino y subida de fotografías, sin zona temporal |
| Secciones 9, 11, 12, 14, 16 | Endurecimiento decidido en parte (ADR-032); condiciones antes de datos reales; DP-27, DP-28 y DP-29 en la lista de pendientes |
| Sección 17 | Referencias 36 (fuentes del endurecimiento) y 37 (documentación núcleo) |
| Anexo A | La fila de endurecimiento pasa de "sin investigar" a "decidido en parte"; filas nuevas de las decisiones del 23-oct-2026 (sin zona temporal, 10 fotografías, perfil de la propiedad, ADR-032); la fila de reducción de fotografías anota que la zona temporal se descartó |
| Anexo B | Dos términos: perfil de la propiedad y fotografía del contrato |
| Bases | ERS v1.14 (ya declarada); los documentos de las fases 3 a 5 declaran la v0.12 |

## 3. Qué no se hizo
- **No se reescribieron todos los ADR**: las viñetas de decisión, fundamento y "no verificado" de cada ADR se conservan tal como estaban; solo cambiaron los rótulos de los ajustes y los puntos que contradecían decisiones posteriores. Sigue habiendo texto histórico dentro de los ADR (por ejemplo, el ADR-022 con la preferencia por Django 6.2 LTS que luego se sustituyó por la 5.2).
- No se releyeron las secciones 7.1 a 7.6, 10.1 a 10.6 ni la 15, que no cambiaron.
- No se pasó el DAS por la plantilla completa de arc42 ni se añadieron diagramas.
- No se añadió el modelo de amenazas (recomendación 2 de la investigación).
- El script comprueba identificadores, enlaces y bases, no el contenido.

## 4. Lo que propone el asistente y el solicitante no decidió
- Los títulos descriptivos de los antiguos ajustes y el orden de la sección 10.7.
- El texto del ADR-032 recoge las decisiones tal como se registraron; lo marcado "propuesta" allí sigue sin decidir.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
