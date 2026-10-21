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
| **0.11** | `DAS_SGA_001_v0.11_borrador.md` | **Vigente** (borrador, no aprobado) |

**Depende de:** `../fase-1-ers/ERS_SGA_001_v1.9_borrador.md`. La v0.11 alinea el DAS con la ERS v1.9.

**Incorporado en la v0.6:** sección de restricciones (1.1), árbol de requisitos de calidad (4.1) y glosario (anexo B), según la evaluación metodológica.

**Decisiones abiertas que afectan a esta fase:** DP-04 (proveedor de WhatsApp, diferida) y las legales DP-17 a DP-21. DP-26 quedó resuelta en la v0.7. **Incorporado en la v0.11** (decisiones del solicitante del 20 y 21-oct-2026, ya en la ERS v1.9): notificaciones por correo y WhatsApp como canal futuro (ADR-008, ADR-026, RE-05), enlace de restablecimiento de contraseña (ADR-026), reintentador también para notificaciones (ADR-013), comprobante del sistema como fase posterior con número de recibo físico en la v1 (ADR-010, ADR-018) y exportación del titular en informe web imprimible. Sin cambios de stack. Siguen pendientes dominio, las dos direcciones, intervalo del reintentador y verificación del servicio de correo. **Incorporado en la v0.10:** avisos de seguridad de la cuenta por correo a dos direcciones, con Resend por API y un reintentador de intervalo corto (ADR-026; ajusta ADR-013 y ADR-023), decisión del solicitante del 20-oct-2026; requiere cambios en la ERS pendientes para su próxima versión. **Incorporado en la v0.9:** PostgreSQL 18, disco privado servido por Django, temporizador de systemd, DigitalOcean con Ubuntu 26.04, Nginx, Certbot y Gunicorn, respaldos cifrados a Spaces e integración continua (ADR-002, 003, 013 y 023 a 025), decisiones del solicitante del 20-oct-2026; tamaño del Droplet, región y dominio siguen pendientes. **Incorporado en la v0.8:** Python y Django con interfaz renderizada por el servidor (ADR-022, RE-04), decisión del solicitante del 20-oct-2026; el motor de base de datos y las demás piezas siguen pendientes.
