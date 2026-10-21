# Actualización 2026-10-21 (d) — Diseño técnico v0.6 (HT-02)

**Fecha:** 2026-10-21
**Documentos afectados:** [Diseño técnico v0.6](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.6_borrador.md); README de la [fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md)
**Versión anterior:** [Diseño técnico v0.5](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.5_borrador.md) (se conserva sin cambios)
**Estado:** borrador; no aprobado

## 1. Motivo
Hallazgo HT-02: formato y contenido del comprobante de pago y si los procedimientos pactados lo sustituyen (DP-20). La respuesta del solicitante cambió el alcance de RF-37.

## 2. Cambios
| ID | Tipo | Descripción | Origen |
|---|---|---|---|
| DTE 3.4.2 | añadido | Comprobante en dos fases: recibo de papel fuera del sistema (B) y comprobante del sistema (A) | P1 a P3 |
| DTE 1, 3.4, 4.2, 6 (HT-02), 7 | modificado | Estado del comprobante y de la reimpresión | — |
| DTE 2 | modificado | Fila nueva con las notas de prensa sobre factura electrónica | — |

## 3. Impacto
**Cambio de alcance no reflejado todavía en la ERS ni en las demás fases:**
- **ERS v1.9:** RF-37, CA-37, la parte de comprobante de CA-04 y CA-34, RN y el dato "comprobante" de la sección 6, y la numeración consecutiva; añadir el campo opcional "número de recibo físico".
- **Estrategia de pruebas:** CA-37 (Alta) y las pruebas de numeración consecutiva pasan a la fase A. La regla de diferimiento exige aceptación escrita para una prioridad Alta: se registra abajo.
- **Modelo de datos:** campo opcional y único "número de recibo físico" en el movimiento; no está hecho.
- **Legal:** OL-03 (art. 56: el arrendador conserva copia) se cumple con copia física; el art. 58 y la factura electrónica siguen con el abogado o contador.

## 4. Decisiones
| # | Pregunta | Respuesta del solicitante | Recomendación del asistente |
|---|---|---|---|
| P1 | ¿Qué naturaleza tiene el comprobante en la v1? | "Por el momento es físico los comprobantes" (necesitó aclaración) | Comprobante interno, no factura electrónica |
| P2 | ¿Qué significa "físico"? (A: el sistema lo genera y se imprime; B: el recibo se hace fuera del sistema) | "Se podría ambos; por el momento se trabaja con la B y poco a poco se integrará la A" | A |
| P3 | Mientras sea B, ¿qué registra el SGA y cómo se trata RF-37? | Dividir RF-37: ahora solo anotar el número del recibo de papel; el comprobante del sistema después | Igual |

**Aceptación de diferir un requisito Alta:** al elegir la opción recomendada de P3, que la describía, el solicitante aceptó diferir RF-37 y asumir sus riesgos: numeración a mano y posibles errores, papel sin marca de anulado, sin copia electrónica. Es una respuesta del solicitante, no aprobación del negocio.

**Pendientes:** DP-20 (contenido legal, si el recibo de papel basta, si Hacienda exige factura electrónica); fecha o versión de la fase A; si las consultas de lectura se auditan.

## 5. Evidencia y fuentes
- ERS v1.8: RF-37, OL-03, DP-20 y el resumen para el abogado v2 (A3), leídos.
- Búsqueda web del 21-oct-2026 sobre factura electrónica para arrendadores: solo resultados de búsqueda (El Financiero, La Nación), de 2018 a 2024, de terceros; las páginas no se abrieron. Mencionan la resolución DGT-R-012-2018. No hay fuente oficial vigente de Hacienda; no se afirma que la obligación exista.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`. No revisa el diseño técnico.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
