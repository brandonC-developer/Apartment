# Fase 4 — Estrategia y plan de pruebas

**Estado:** no iniciada.

**Qué definirá:** cómo demostrar que cada requisito funciona, los escenarios y las condiciones de aceptación.

**Entradas:** los criterios de aceptación CA-01 a CA-57 de la ERS v1.8 y la matriz de trazabilidad (sección 10).

**Observación de la evaluación metodológica:** esta fase puede empezar en cuanto la ERS tenga línea base, sin esperar al diseño técnico. Es una inferencia nuestra a partir de la estructura de ISO/IEC/IEEE 29119-3, no un texto de la norma (ver `../metodologia/EVALUACION_METODOLOGIA_v1.md`, ajuste 2).

**Cobertura que la fase 4 debe resolver (matriz de la ERS, sección 10):** RNF-05, RNF-07, RNF-08, RNF-09, RNF-10 y RNF-11 no tienen criterio de aceptación y deben verificarse con pruebas no funcionales. La segunda mitad de RN-15 (rechazar movimientos sobre períodos futuros, salvo el inmediato siguiente) no tiene CA. Ver `../actualizaciones/2026-10-20b_ERS-v1.8-matriz/CAMBIOS.md`.

**Casos que requieren atención especial:** fechas de fin de mes, años bisiestos, redondeo del prorrateo, gracia de 7 días, reajuste con fecha efectiva normalizada, numeración consecutiva de comprobantes, idempotencia del proceso diario, retención y eliminación de datos personales.
