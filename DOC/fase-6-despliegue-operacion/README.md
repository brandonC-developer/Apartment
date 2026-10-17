# Fase 6 — Despliegue y operación

**Estado:** no iniciada.

**Qué documentará:** entornos, despliegues, copias de seguridad, recuperación, monitoreo, mantenimiento y procedimientos operativos.

**Entradas:** DAS v0.4 (secciones 10 y 11) y las decisiones DP-07 (RPO, RTO, retención de respaldos) y DP-08 (exposición pública).

**Requisitos de la ERS que se verifican aquí:** RNF-09 (recuperación), RNF-14 (seguridad de los datos), RF-41 (retención y eliminación), RNF-16 (idempotencia del proceso diario).

**Puntos críticos:**
- Prueba de restauración de base de datos y archivos antes de producción.
- Los respaldos deben respetar la eliminación y desasociación por retención (DP-18).
- Monitoreo del proceso diario de las 07:00 y de las notificaciones fallidas.
