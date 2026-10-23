# Actualización 2026-10-22 (g) — Alineación de los documentos con la ERS v1.10

**Fecha:** 2026-10-22
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado; mismo criterio que la [actualización 2026-10-21 (ac)](../2026-10-21ac_repaso-final-y-limpieza/CAMBIOS.md)):** [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md), [Modelo de datos v0.4](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.4_borrador.md), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md), [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md), el [registro de avance](../../fase-5-implementacion/AVANCE_IMPLEMENTACION.md), los README de las fases 1 a 5 y [DOC/README.md](../../README.md)
**Origen:** [2026-10-22 (f)](../2026-10-22f_ERS-v1.10/CAMBIOS.md)
**Estado:** borrador; no aprobado

## 1. Motivo
Tras publicar la ERS v1.10, el script de coherencia señalaba 11 problemas: seis documentos declaraban la v1.9 como base y faltaban RF-50, CA-73 y CA-74 en la estrategia de pruebas y en el plan. El solicitante pidió alinearlos (22-oct-2026).

## 2. Cambios
| Documento | Cambio |
|---|---|
| DAS v0.11 | Base ERS v1.10; viñeta de seguridad de archivos con la reducción en el navegador (no es un control de seguridad) y un JavaScript mínimo sobre las plantillas de Django (sin aplicación de una sola página, ADR-022); el límite de Nginx de 6m queda decidido en lugar de pendiente; fila nueva en la tabla de trazabilidad; nota en el historial. **No se añade ni cambia ningún ADR** |
| Modelo de datos v0.4 | Base ERS v1.10; nota: RF-50 no añade campos ni entidades |
| Diseño técnico v0.7 | Base ERS v1.10; RF-50 en la operación "Registrar inquilino"; nota en el flujo F-01; **nuevo hallazgo HT-10** (la subida por separado deja sin cumplir el paso "una transacción, sin archivos huérfanos") y pendiente 7 |
| Estrategia de pruebas v0.3 | Base ERS v1.10; CA-73 (extremo a extremo, prioridad Media) y CA-74 (integración, Alta) asignados; recuento 74 de 74 |
| Plan de implementación v0.1 | Base ERS v1.10; RF-50, CA-73 y CA-74 en la E1; nuevo riesgo HI-07 (HT-10 se decide antes de la E1) |
| Lista de verificación v0.1 | Base ERS v1.10; RV-14 precisa el límite de 6m y que la reducción del navegador no cuenta como control |
| Registro de avance | E1 pasa de 0/5 a 0/7 CA; línea nueva en el historial (la entrega sigue *no iniciada*) |

## 3. Lo que propone el asistente y el solicitante no decidió
- Los **niveles y prioridades** de CA-73 (Media) y CA-74 (Alta) en la estrategia de pruebas.
- **HT-10**: la zona temporal con identificador de un solo uso, la alternativa del inquilino provisional y el plazo de limpieza. La decisión de subir por separado es del solicitante; cómo se resuelve el huérfano no.
- Asignar RF-50 a la **E1** (por pertenecer a la aplicación `inquilinos`, ADR-030).

## 4. Qué no se hizo
- No se creó ninguna versión nueva de los documentos de las fases 2 a 5 ni se escribieron ADR nuevos.
- No se resolvió HT-10 ni DP-27.
- No se verificó que los textos de los documentos coincidan con la lógica; el script comprueba identificadores, enlaces, bases y cobertura. Se revisaron a mano los cambios (diferencias de Git).

## 5. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`: sin problemas (50 RF y 74 CA con matriz, pruebas y plan completos; 7 entregas registradas, ninguna en curso).

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
