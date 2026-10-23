# Fase 6 — Despliegue y operación

**Estado:** no iniciada.

**Qué documentará:** entornos, despliegues, copias de seguridad, recuperación, monitoreo, mantenimiento y procedimientos operativos.

**Entradas:** DAS v0.14 (secciones 10 y 11, RE-03, RE-09, ADR-021 y ADR-023 a ADR-032) y las decisiones ya tomadas: DP-07 (RPO y RTO de 24 h, retención de 35 días) y DP-08 (VPS administrado por el solicitante, acceso por internet).

**Requisitos de la ERS que se verifican aquí:** RNF-09 (recuperación), RNF-14 (seguridad de los datos), RNF-18 (documentación de seguridad), RF-41 (retención y eliminación), RF-46 (incidentes), RNF-16 (idempotencia del proceso diario).

**Puntos críticos:**
- Prueba de restauración de base de datos y archivos antes de producción.
- Los respaldos deben respetar la eliminación y desasociación por retención (DP-18).
- Monitoreo del proceso diario de las 07:00 y de las notificaciones fallidas.
- Endurecimiento del servidor (VPS administrado por el solicitante): **investigado el 22-oct-2026**, con propuestas sin decidir y fuentes validadas en [actualizaciones/2026-10-22_investigacion-endurecimiento-servidor](../actualizaciones/2026-10-22_investigacion-endurecimiento-servidor/CAMBIOS.md); Nginx, Gunicorn y PostgreSQL investigados el mismo día en [la actualización (b)](../actualizaciones/2026-10-22b_endurecimiento-nginx-gunicorn-postgresql/CAMBIOS.md); el solicitante decidió el 22-oct-2026 no depender del PDF de CIS y auditar con Lynis ([actualización (c)](../actualizaciones/2026-10-22c_decision-base-endurecimiento-lynis/CAMBIOS.md)); falta probar Lynis y verificar los valores por defecto de Ubuntu 26.04 en una instalación real. Límite de subida de la foto de la cédula y compresión en el navegador: [propuesta en la actualización (d)](../actualizaciones/2026-10-22d_limite-subida-foto-cedula/CAMBIOS.md) y [decisión del solicitante en la (e)](../actualizaciones/2026-10-22e_decision-limite-subida/CAMBIOS.md): 5 MB por archivo, compresión de 2048 px y calidad 0,85, Nginx 6m, frente y reverso por separado; la compresión aún no está en la ERS.
- Condiciones recomendadas antes de cargar datos reales: servidor endurecido, prueba de restauración superada y revisión legal cerrada.
- Documento de seguridad y protocolo de actuación (OL-20, OL-21) y procedimiento de respuesta a incidentes con aviso en cinco días hábiles (OL-19), todo pendiente de abogado.

**Contexto que viene de la fase 5 (21-oct-2026):** la implementación va primero en local y gratis (etapa A, WSL 2 con Ubuntu-26.04, sin contenedores) y solo después se contratan los servicios (etapa B: DigitalOcean en NYC3, dominio `.com` en Cloudflare, Resend). Esta fase documenta la etapa B y la operación. Pendientes que le corresponden: endurecimiento del servidor, verificación de Resend (entregabilidad, términos y DNS), monitoreo externo del servidor, procedimiento ante un aviso de seguridad inesperado, rescate de la cuenta por el servidor (RF-27, CA-70), vigilancia del proceso diario (RF-49), documento de seguridad y revisión por otra persona de lo crítico (plan de implementación, sección 3.3).

**Decidido en la fase 4 (20-oct-2026):** la restauración trimestral la ejecuta el solicitante a mano, con una comprobación automática mensual, y los resultados se registran en esta carpeta, sin datos personales. El registro y el script no existen todavía.
