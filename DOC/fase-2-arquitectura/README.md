# Fase 2 — Arquitectura de software

**Qué define:** cómo se organiza la solución: componentes, responsabilidades, comunicación, seguridad y decisiones arquitectónicas.

| Versión | Archivo | Estado |
|---|---|---|
| 0.3 | `DAS_SGA_001_v0.3_borrador_actualizado.md` | Reemplazada |
| 0.4 | `DAS_SGA_001_v0.4_borrador.md` | Reemplazada |
| 0.5 | `DAS_SGA_001_v0.5_borrador.md` | Reemplazada por la 0.6 |
| 0.6 | `DAS_SGA_001_v0.6_borrador.md` | Reemplazada por la 0.7 |
| 0.7 | `DAS_SGA_001_v0.7_borrador.md` | Reemplazada por la 0.8 |
| 0.8 | `DAS_SGA_001_v0.8_borrador.md` | Reemplazada por la 0.9 |
| 0.9 | `DAS_SGA_001_v0.9_borrador.md` | Reemplazada por la 0.10 |
| 0.10 | `DAS_SGA_001_v0.10_borrador.md` | Reemplazada por la 0.11 |
| 0.11 | `DAS_SGA_001_v0.11_borrador.md` | Reemplazada por la 0.12 |
| 0.12 | `DAS_SGA_001_v0.12_borrador.md` | Reemplazada por la 0.13 |
| 0.13 | `DAS_SGA_001_v0.13_borrador.md` | Reemplazada por la 0.14 |
| 0.14 | `DAS_SGA_001_v0.14_borrador.md` | Reemplazada por la 0.15 |
| **0.15** | `DAS_SGA_001_v0.15_borrador.md` | **Vigente** (borrador, no aprobado) |

**Incorporado en la v0.15 (23-oct-2026):** ADR-003 (decodificación completa de la imagen, eliminación de metadatos en el servidor, sin antivirus), ADR-032 con 18 decisiones (17: registros de Nginx y Gunicorn; 18: dispositivo del administrador y llave SSH), DP-27 resuelta, DP-31 nueva (transferencia de datos a Resend y DigitalOcean, para el abogado) y referencia al modelo de amenazas v0.3 y a la ERS v1.16. Actualizaciones [(zo)](../actualizaciones/2026-10-23zo_br-05-metadatos-imagenes/CAMBIOS.md), [(zp)](../actualizaciones/2026-10-23zp_br-06-antivirus/CAMBIOS.md), [(zq)](../actualizaciones/2026-10-23zq_br-07-registros-nginx-gunicorn/CAMBIOS.md), [(zr)](../actualizaciones/2026-10-23zr_br-09-dispositivo-y-llave-ssh/CAMBIOS.md), [(zs)](../actualizaciones/2026-10-23zs_br-10-transferencia-a-proveedores/CAMBIOS.md) y [(zu)](../actualizaciones/2026-10-23zu_DAS-v0.15/CAMBIOS.md).

**Depende de:** `../fase-1-ers/ERS_SGA_001_v1.16_borrador.md`. La v0.12 (23-oct-2026) consolida la v0.11: integra los ajustes que se habían apilado sin versión nueva (ERS v1.10 a v1.14), añade el ADR-032 (endurecimiento del servidor), la entidad Documento del contrato y el flujo 10.7, y quita los ajustes apilados del historial; ver `../actualizaciones/2026-10-23v_DAS-v0.12/CAMBIOS.md`.
**Incorporado en la v0.14 (23-oct-2026):** el ADR-032 pasa a 16 decisiones: PostgreSQL solo por socket y sin contraseñas, Gunicorn por socket de systemd con 0660 y Nginx con cabeceras sustituidas, salida de los firewalls denegada por defecto, respaldo a las 05:00 con aviso si falla (requisito nuevo por redactar), cifrados TLS, CAA, CSP y reinicio con sesiones abiertas; se cierran los pendientes de los ADR-013, 024 y 029. Ver `../actualizaciones/2026-10-23zk_DAS-v0.14/CAMBIOS.md`.

**Incorporado en la v0.13 (23-oct-2026):** el ADR-032 pasa a cubrir las cuentas de proveedores y de correo (BR-01 y BR-12), el correo del dominio (BR-02), los respaldos (BR-03), las dependencias de Python (BR-04) y el límite de solicitudes (BR-08), con AM-04 aceptado; se cierran los pendientes de los ADR-022, 024, 025 y 026 que dependían de ellas. Ver `../actualizaciones/2026-10-23zf_DAS-v0.13/CAMBIOS.md`.
**Decisiones abiertas nuevas que afectan a esta fase:** del endurecimiento (ADR-032): Gunicorn por socket, Nginx, PostgreSQL, cifrados TLS, CAA, CSP, regla de salida de los firewalls y hora del respaldo; además DP-27, DP-28 y DP-29.

**Incorporado en la v0.6:** sección de restricciones (1.1), árbol de requisitos de calidad (4.1) y glosario (anexo B), según la evaluación metodológica.

**Decisiones abiertas que afectan a esta fase:** DP-04 (proveedor de WhatsApp, diferida) y las legales DP-17 a DP-21. DP-26 quedó resuelta en la v0.7. **Incorporado en la v0.11** (decisiones del solicitante del 20 y 21-oct-2026, ya en la ERS v1.9): notificaciones por correo y WhatsApp como canal futuro (ADR-008, ADR-026, RE-05), enlace de restablecimiento de contraseña (ADR-026), reintentador también para notificaciones (ADR-013), comprobante del sistema como fase posterior con número de recibo físico en la v1 (ADR-010, ADR-018) y exportación del titular en informe web imprimible. Sin cambios de stack. Siguen pendientes dominio, las dos direcciones, intervalo del reintentador y verificación del servicio de correo. **Incorporado en la v0.10:** avisos de seguridad de la cuenta por correo a dos direcciones, con Resend por API y un reintentador de intervalo corto (ADR-026; ajusta ADR-013 y ADR-023), decisión del solicitante del 20-oct-2026; requiere cambios en la ERS pendientes para su próxima versión. **Incorporado en la v0.9:** PostgreSQL 18, disco privado servido por Django, temporizador de systemd, DigitalOcean con Ubuntu 26.04, Nginx, Certbot y Gunicorn, respaldos cifrados a Spaces e integración continua (ADR-002, 003, 013 y 023 a 025), decisiones del solicitante del 20-oct-2026; tamaño del Droplet, región y dominio siguen pendientes. **Incorporado en la v0.8:** Python y Django con interfaz renderizada por el servidor (ADR-022, RE-04), decisión del solicitante del 20-oct-2026; el motor de base de datos y las demás piezas siguen pendientes.
