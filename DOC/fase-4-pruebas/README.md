# Fase 4 — Estrategia y plan de pruebas

**Estado:** iniciada (estrategia v0.2 en borrador, sin revisar).

**Qué define:** cómo demostrar que cada requisito funciona, los escenarios y las condiciones de aceptación.

| Producto | Archivo | Estado |
|---|---|---|
| Estrategia y plan de pruebas | `ESTRATEGIA_PRUEBAS_SGA_001_v0.2_borrador.md` (vigente); la v0.1 se conserva | Borrador v0.2; no aprobado |
| Casos de prueba detallados | — | No iniciado; se escriben con la implementación |

**Entradas:** los criterios de aceptación CA-01 a CA-61 de la ERS v1.9 y su matriz de trazabilidad (sección 10); la estrategia v0.2 cubre CA-01 a CA-57 y falta incorporar CA-58 a CA-61, el canal de correo (CA-05, CA-08, CA-09, CA-43) y mover CA-37 y CA-54 a la fase posterior del comprobante, y las decisiones del DAS v0.9 (PostgreSQL 18, DigitalOcean, respaldos e integración continua).

**Observación de la evaluación metodológica:** esta fase podía empezar en cuanto la ERS tuviera línea base, sin esperar al diseño técnico. Es una inferencia nuestra a partir de la estructura de ISO/IEC/IEEE 29119-3, no un texto de la norma, que no se pudo abrir (ver `../metodologia/EVALUACION_METODOLOGIA_v1.md`, ajuste 2).

**Qué contiene la v0.2:** niveles de prueba, entornos y datos, cobertura de los 57 CA, verificación de los RNF sin criterio de aceptación (RNF-05, 07, 08, 09, 10 y 11), pruebas de operación (restauración, temporizador, HTTPS), casos límite, criterios de entrada y salida, hallazgos HP-01 a HP-04 y las siete decisiones del solicitante del 20-oct-2026 (ejecutor de Django, Selenium, Locust, cobertura sin umbral, restauración, RN-15 y prioridades diferibles).

**Cobertura que la fase debe resolver:** la segunda mitad de RN-15 (rechazar movimientos sobre períodos futuros, salvo el inmediato siguiente) no tenía CA (HP-01); la ERS v1.9 la cubre con CA-58. Ver `../actualizaciones/2026-10-20b_ERS-v1.8-matriz/CAMBIOS.md`.

**Casos que requieren atención especial:** fechas de fin de mes, años bisiestos, redondeo del prorrateo, gracia de 7 días, reajuste con fecha efectiva normalizada, numeración consecutiva de comprobantes, idempotencia del proceso diario, retención y eliminación de datos personales.

**Pendiente:** los puntos pendientes de la sección 11 de la estrategia, la revisión por otra persona y la validación legal de los CA marcados (L).
