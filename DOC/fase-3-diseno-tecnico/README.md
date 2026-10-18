# Fase 3 — Diseño técnico

**Estado:** iniciada (modelo de datos v0.3 en borrador, con prueba en PostgreSQL).

**Qué definirá:** modelo de datos (entidades y relaciones), contratos de API, permisos y flujos de negocio.

| Producto | Archivo | Estado |
|---|---|---|
| Modelo lógico de datos | `MODELO_DATOS_SGA_001_v0.3_borrador.md` (vigente); v0.1 y v0.2 se conservan | Borrador v0.3, sin revisar |
| Contratos de API | — | No iniciado |
| Permisos por operación | — | No iniciado |
| Flujos de negocio detallados | — | No iniciado |

**Entradas:**
- ERS v1.6 (secciones 5, 6 y 7) y DAS v0.5 (secciones 7, 8 y 10).
- Decisión de motor de base de datos y de estilo de API (ADR-002), todavía abierta.

**Hallazgos del modelado que afectan a la ERS y al DAS:** ver la sección 9 del modelo (H1 a H13). El más importante: el saldo de apertura se define como movimiento en los glosarios y como obligación en el resto de la ERS.

**Bloqueos:** ninguno para continuar con el modelo; la integración con WhatsApp espera a DP-04.

**Incorporado en la ERS v1.8 y el DAS v0.7:** H1 a H3, H9 a H13 y H4 (provisional). **Siguen abiertos:** DP-20 (comprobantes) y la revisión por otra persona.

**Nota:** IEEE 1016-2009 (descripciones de diseño de software) figura como inactiva; se usa solo como referencia de contenido. Ver `../metodologia/EVALUACION_METODOLOGIA_v1.md`.
