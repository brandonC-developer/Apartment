# Actualización 2026-10-21 (f) — DAS v0.11

**Fecha:** 2026-10-21
**Documentos afectados:** [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md); README de las fases 2, 3, 5 y 6 y [DOC/README.md](../../README.md)
**Versión anterior:** [DAS v0.10](../../fase-2-arquitectura/DAS_SGA_001_v0.10_borrador.md) (se conserva sin cambios)
**Estado:** borrador; no aprobado

## 1. Motivo
Alinear la arquitectura con la [ERS v1.9](../../fase-1-ers/ERS_SGA_001_v1.9_borrador.md), que incorporó las decisiones del solicitante del 20 y 21-oct-2026. El DAS v0.10 seguía describiendo WhatsApp como canal de la v1, el comprobante numerado por el sistema y ninguna salida para restablecer la contraseña.

## 2. Cambios
| ID | Tipo | Descripción | Origen |
|---|---|---|---|
| Encabezado, historial, sección 1 | modificado | Versión 0.11, ERS de referencia v1.9 | — |
| RE-05 | modificado | WhatsApp fuera de la v1 | HT-01 (21-oct-2026) |
| Secciones 3, 4, 4.1, 6 | modificado | Servicio de correo como actor; diagramas; escenarios de calidad (correo, restablecimiento de contraseña, recibo físico) | HT-01, HT-02, HT-08 |
| Sección 7.2, 7.7, 8 | modificado | Número de recibo físico; comprobante como fase posterior; exportación del titular en informe web imprimible; entidades Movimiento, Organización, Notificación, Comprobante | HT-02, HT-03, HT-01 |
| Sección 9 | modificado | Avisos a dos direcciones; cambio y restablecimiento de contraseña | HT-05, HT-08 |
| Sección 10.1, 10.2, 10.3, 10.6 | modificado | Resumen por correo; transacción sin número de comprobante en la v1; reintentos por correo; sin punto de entrada exterior | HT-01, HT-02 |
| Sección 12 | modificado | Riesgos de recibo de papel, restablecimiento por correo y cuenta única | HT-02, HT-08 |
| ADR-008 | modificado | Canal futuro (WhatsApp) y correo en la v1; sin recepción de estados | HT-01 |
| ADR-010, ADR-018 | modificado | Comprobante del sistema y serie global: fase posterior | HT-02 |
| ADR-013 | modificado | El reintentador cubre también notificaciones | HT-01 |
| ADR-026 | modificado | Notificaciones al administrador; enlace de restablecimiento; cambios de la ERS ya hechos | HT-01, HT-08 |
| Secciones 14 a 17, anexos A y B | modificado | DP-04, DP-19 y DP-20; trazabilidad con RF-47, CA-58 a CA-61; condiciones; referencia 27; filas de decisiones; glosario | — |

No se añadió ningún ADR, RE ni DP nuevo, y ningún ID cambió de significado. Sin cambios de stack (ADR-002, 003, 022 a 025 intactos).

## 3. Impacto
- **Modelo de datos v0.3:** sigue sin el campo "número de recibo físico" (opcional, único) ni el cambio de Comprobante a fase posterior; falta una versión nueva.
- **Estrategia de pruebas v0.2:** falta incorporar CA-58 a CA-61, el canal de correo y mover CA-37 y CA-54.
- **Diseño técnico v0.6:** coincide con el DAS; sus citas a "DAS v0.10" se corregirían en una versión próxima.
- **Resumen para el abogado v2:** falta actualizarlo.

## 4. Decisiones
No hay decisiones nuevas; se trasladan las del 20 y 21-oct-2026 ya registradas en [2026-10-20h](../2026-10-20h_ht-05-recuperacion-acceso/CAMBIOS.md), [2026-10-21](../2026-10-21_ht-08-contrasena-segundo-factor/CAMBIOS.md), [2026-10-21b](../2026-10-21b_ht-01-canal-correo/CAMBIOS.md), [2026-10-21c](../2026-10-21c_ht-03-exportacion-titular/CAMBIOS.md), [2026-10-21d](../2026-10-21d_ht-02-comprobante-fisico/CAMBIOS.md) y [2026-10-21e](../2026-10-21e_ERS-v1.9/CAMBIOS.md).

**Redacciones mías, no revisadas una por una por el solicitante:** el texto de los ADR-008 y ADR-026 ajustados (por ejemplo, que el mismo temporizador reintente notificaciones y avisos) y la explicación de que el correo con enlace es de otro tipo que los avisos del ADR-026.

**Pendientes:** dominio y costo; las dos direcciones; intervalo del reintentador; entregabilidad, términos de servicio y registros DNS de Resend; protecciones del enlace de restablecimiento sin decidir (respuesta idéntica, invalidar sesiones, límite de solicitudes); validación legal (DP-17, DP-19, DP-20).

## 5. Evidencia y fuentes
Las de las actualizaciones citadas. Fuentes nuevas respecto de la v0.10, todas por resumen o solo búsqueda: OWASP Authentication y Multifactor Authentication Cheat Sheets, Meta (webhooks de WhatsApp), Ley 8968 art. 7 y Reglamento 37554-JP arts. 21 y 22 (copias del Archivo Nacional), y notas de prensa sobre factura electrónica (no citadas como respaldo).

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1` y búsqueda manual de las menciones de WhatsApp y comprobante en el DAS v0.11.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
