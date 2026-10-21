# Fase 3 — Diseño técnico

**Estado:** iniciada (modelo de datos v0.4 y diseño técnico v0.7, ambos en borrador sin revisar).

**Qué definirá:** modelo de datos (entidades y relaciones), contratos de API, permisos y flujos de negocio.

| Producto | Archivo | Estado |
|---|---|---|
| Modelo lógico de datos | `MODELO_DATOS_SGA_001_v0.4_borrador.md` (vigente); `MODELO_DATOS_SGA_001_v0.1_borrador.md`, `MODELO_DATOS_SGA_001_v0.2_borrador.md` y `MODELO_DATOS_SGA_001_v0.3_borrador.md` se conservan | Borrador v0.4, sin revisar |
| Interfaces (no hay API pública en la v1, ADR-022), permisos por operación y flujos de negocio | `DISENO_TECNICO_SGA_001_v0.7_borrador.md` (vigente; se conservan `DISENO_TECNICO_SGA_001_v0.1_borrador.md`, `DISENO_TECNICO_SGA_001_v0.2_borrador.md`, `DISENO_TECNICO_SGA_001_v0.3_borrador.md`, `DISENO_TECNICO_SGA_001_v0.4_borrador.md`, `DISENO_TECNICO_SGA_001_v0.5_borrador.md` y `DISENO_TECNICO_SGA_001_v0.6_borrador.md`) | Borrador v0.7; no aprobado |

**Entradas:**
- [ERS v1.9](../fase-1-ers/ERS_SGA_001_v1.9_borrador.md) (secciones 5, 6 y 7) y [DAS v0.11](../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md) (secciones 7, 8 y 10; lenguaje y framework en ADR-022).
- Motor de base de datos: el motor es PostgreSQL 18 (ADR-002, decisión del solicitante del 20-oct-2026). Desde la v0.8 del DAS la interfaz se renderiza en el servidor con Django y no hay API pública en la versión 1 (ADR-022); los "contratos de API" se reducen a interfaces internas.

**Hallazgos del modelado que afectan a la ERS y al DAS:** ver la sección 9 del modelo (H1 a H14; H14 es propuesta del asistente, no decidida por el solicitante). El más importante: el saldo de apertura se define como movimiento en los glosarios y como obligación en el resto de la ERS.

**Bloqueos:** ninguno para continuar con el modelo; la integración con WhatsApp espera a DP-04.

**Incorporado en la ERS v1.8 y el DAS v0.7:** H1 a H3, H9 a H13 y H4 (provisional). **Siguen abiertos:** DP-20 (comprobantes) y la revisión por otra persona.

**Nota:** IEEE 1016-2009 (descripciones de diseño de software) figura como inactiva; se usa solo como referencia de contenido. Ver `../metodologia/EVALUACION_METODOLOGIA_v1.md`.

**Incorporado en el modelo de datos v0.4 y el diseño técnico v0.7 (21-oct-2026):** alineación con la ERS v1.9 y el DAS v0.11, sin decisiones nuevas: número de recibo físico en MOVIMIENTO (RF-47), COMPROBANTE como fase posterior, correos en ORGANIZACION, NOTIFICACION con canal de correo y avisos de seguridad, entidad TOKEN_RESTABLECIMIENTO. **Incorporado en el diseño técnico v0.6:** HT-02 resuelto como cambio de alcance (decisión del solicitante del 21-oct-2026): primero recibos de papel fuera del sistema, con un campo opcional de número de recibo físico, y el comprobante generado por el sistema después; difiere RF-37 y CA-37 (Alta); la ERS v1.9 ya lo refleja. DP-20 sigue abierta (contenido legal y factura electrónica). **Incorporado en la v0.5:** HT-03 (la exportación del titular incluye todo su registro con la foto de la cédula y se entrega como informe web imprimible; decisiones del solicitante del 21-oct-2026, que rectificó su primera elección de formato, PDF generado por el sistema). Requiere validación del abogado. **Incorporado en la v0.4:** HT-01 resuelto como cambio de alcance (decisión del solicitante del 21-oct-2026): en la v1 las notificaciones al administrador salen por web y correo, y WhatsApp queda para el futuro; la ERS v1.9 y el DAS v0.11 ya lo reflejan. **Incorporado en la v0.3:** HT-08 (cambio con la contraseña actual; restablecimiento con enlace por correo de 15 minutos; decisiones del solicitante del 21-oct-2026, las dos primeras contra la recomendación). **Incorporado en la v0.2:** HT-05 (aviso de recuperación de acceso por correo a dos direcciones; ADR-026). **Pendiente:** decisiones de su sección 7 (auditoría de consultas de lectura, dominio y direcciones) y hallazgos HT-06 y HT-07. HT-04 y HT-09 quedaron resueltos en la ERS v1.9.
