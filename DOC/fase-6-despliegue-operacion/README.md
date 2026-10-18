# Fase 6 — Despliegue y operación

**Estado:** no iniciada.

**Qué documentará:** entornos, despliegues, copias de seguridad, recuperación, monitoreo, mantenimiento y procedimientos operativos.

**Entradas:** DAS v0.7 (secciones 10 y 11, RE-03, RE-09 y ADR-021) y las decisiones ya tomadas: DP-07 (RPO y RTO de 24 h, retención de 35 días) y DP-08 (VPS administrado por el solicitante, acceso por internet).

**Requisitos de la ERS que se verifican aquí:** RNF-09 (recuperación), RNF-14 (seguridad de los datos), RNF-18 (documentación de seguridad), RF-41 (retención y eliminación), RF-46 (incidentes), RNF-16 (idempotencia del proceso diario).

**Puntos críticos:**
- Prueba de restauración de base de datos y archivos antes de producción.
- Los respaldos deben respetar la eliminación y desasociación por retención (DP-18).
- Monitoreo del proceso diario de las 07:00 y de las notificaciones fallidas.
- Endurecimiento del servidor (VPS administrado por el solicitante): las guías reconocidas (por ejemplo, CIS Benchmarks, OWASP) **aún no se han investigado**.
- Condiciones recomendadas antes de cargar datos reales: servidor endurecido, prueba de restauración superada y revisión legal cerrada.
- Documento de seguridad y protocolo de actuación (OL-20, OL-21) y procedimiento de respuesta a incidentes con aviso en cinco días hábiles (OL-19), todo pendiente de abogado.
