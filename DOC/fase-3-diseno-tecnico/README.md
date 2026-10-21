# Fase 3 — Diseño técnico

**Estado:** iniciada (modelo de datos v0.3 y diseño técnico v0.1, ambos en borrador sin revisar).

**Qué definirá:** modelo de datos (entidades y relaciones), contratos de API, permisos y flujos de negocio.

| Producto | Archivo | Estado |
|---|---|---|
| Modelo lógico de datos | `MODELO_DATOS_SGA_001_v0.3_borrador.md` (vigente); v0.1 y v0.2 se conservan | Borrador v0.3, sin revisar |
| Interfaces (no hay API pública en la v1, ADR-022), permisos por operación y flujos de negocio | `DISENO_TECNICO_SGA_001_v0.6_borrador.md` (las v0.1 a v0.5 se conservan) | Borrador v0.6; no aprobado |

**Entradas:**
- [ERS v1.9](../fase-1-ers/ERS_SGA_001_v1.9_borrador.md) (secciones 5, 6 y 7; el modelo de datos v0.3 falta ajustarlo con el número de recibo físico de RF-47) y [DAS v0.11](../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md) (secciones 7, 8 y 10; lenguaje y framework en ADR-022).
- Motor de base de datos: el motor es PostgreSQL 18 (ADR-002, decisión del solicitante del 20-oct-2026). Desde la v0.8 del DAS la interfaz se renderiza en el servidor con Django y no hay API pública en la versión 1 (ADR-022); los "contratos de API" se reducen a interfaces internas.

**Hallazgos del modelado que afectan a la ERS y al DAS:** ver la sección 9 del modelo (H1 a H13). El más importante: el saldo de apertura se define como movimiento en los glosarios y como obligación en el resto de la ERS.

**Bloqueos:** ninguno para continuar con el modelo; la integración con WhatsApp espera a DP-04.

**Incorporado en la ERS v1.8 y el DAS v0.7:** H1 a H3, H9 a H13 y H4 (provisional). **Siguen abiertos:** DP-20 (comprobantes) y la revisión por otra persona.

**Nota:** IEEE 1016-2009 (descripciones de diseño de software) figura como inactiva; se usa solo como referencia de contenido. Ver `../metodologia/EVALUACION_METODOLOGIA_v1.md`.

**Incorporado en el diseño técnico v0.6:** HT-02 resuelto como cambio de alcance (decisión del solicitante del 21-oct-2026): primero recibos de papel fuera del sistema, con un campo opcional de número de recibo físico, y el comprobante generado por el sistema después; difiere RF-37 y CA-37 (Alta) y la ERS aún no lo refleja. DP-20 sigue abierta (contenido legal y factura electrónica). **Incorporado en la v0.5:** HT-03 (la exportación del titular incluye todo su registro con la foto de la cédula y se entrega como informe web imprimible; decisiones del solicitante del 21-oct-2026, que rectificó su primera elección de formato, PDF generado por el sistema). Requiere validación del abogado. **Incorporado en la v0.4:** HT-01 resuelto como cambio de alcance (decisión del solicitante del 21-oct-2026): en la v1 las notificaciones al administrador salen por web y correo, y WhatsApp queda para el futuro; la ERS y el DAS aún no lo reflejan. **Incorporado en la v0.3:** HT-08 (cambio con la contraseña actual; restablecimiento con enlace por correo de 15 minutos; decisiones del solicitante del 21-oct-2026, las dos primeras contra la recomendación). **Incorporado en la v0.2:** HT-05 (aviso de recuperación de acceso por correo a dos direcciones; ADR-026). **Pendiente:** decisiones de su sección 7 (auditoría de consultas de lectura, dominio y direcciones) y hallazgos HT-04, HT-06, HT-07 y HT-09; el DAS debe describir el correo con enlace.
