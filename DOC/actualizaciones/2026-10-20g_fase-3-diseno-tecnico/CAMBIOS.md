# Actualización 2026-10-20 (g) — Fase 3: diseño técnico v0.1

**Fecha:** 20 de octubre de 2026
**Documentos afectados:** [Diseño técnico v0.1](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.1_borrador.md) (nuevo), [README de la fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md).
**Versión anterior:** ninguna; los productos "contratos de API", "permisos por operación" y "flujos de negocio detallados" figuraban como no iniciados.
**Estado:** borrador; no aprobado.

## 1. Motivo
El solicitante pidió seguir con la fase 3 y comprobar si la API ya estaba cubierta ("seguimos con la fase 3 y si ya está cubierto la API"). Respuesta: no hay API pública en la versión 1 (ADR-022); las interfaces que sí existen estaban definidas solo en concepto o sin definir.

## 2. Cambios
| ID | Tipo | Descripción | Origen |
|---|---|---|---|
| D1 | añadido | Diseño técnico DTE-SGA-001 v0.1: respuesta sobre la API, interfaces (web, comando diario, canal de WhatsApp, comprobante, exportación del titular), catálogo de permisos por operación y flujos F-01 a F-09 | Pregunta del solicitante |
| D2 | modificado | README de la fase 3: los tres productos pendientes pasan a un solo documento | Regla 3 de `CLAUDE.md` |
| D3 | modificado | `DOC/README.md`: mapa de fases e historial | Regla 3 de `CLAUDE.md` |

## 3. Impacto
Ningún requisito, regla ni identificador compartido cambia. Se propone ajustar en la próxima versión de la ERS el texto de la sección 15 (HT-04). Se organizó el catálogo de operaciones a partir de los RF leídos; no se revisó cada RF restante uno por uno.

## 4. Decisiones
- **Resueltas:** ninguna en esta actualización.
- **Pendientes del solicitante:** canal independiente para la notificación de recuperación de acceso (HT-05), si se define ya el punto de recepción de estados de WhatsApp (HT-01), formato y alcance de la exportación del titular (HT-03), formato del comprobante (HT-02, DP-20) y si se audita la reimpresión.
- **Hallazgos:** HT-01 a HT-07 (ver el documento).

## 5. Evidencia y fuentes
ERS v1.8 (secciones 5 y 8) y DAS v0.9 (sección 10 y ADR citados): leídos. Django, lista de despliegue, y OWASP, File Upload Cheat Sheet: leídas por resumen. Sin estudios universitarios: el contenido deriva requisitos ya definidos.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`. El script no revisa el documento nuevo. Se comprobó a mano que los CA, ADR, DP, RN y RE citados existen. Revisión de pares: no realizada.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | brandonC-developer | Pendiente | Pendiente |