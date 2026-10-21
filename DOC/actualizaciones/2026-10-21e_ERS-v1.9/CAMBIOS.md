# Actualización 2026-10-21 (e) — ERS v1.9

**Fecha:** 2026-10-21
**Documentos afectados:** [ERS v1.9](../../fase-1-ers/ERS_SGA_001_v1.9_borrador.md); README de la [fase 1](../../fase-1-ers/README.md), de las fases 2, 3, 4 y 5, y [DOC/README.md](../../README.md)
**Versión anterior:** [ERS v1.8](../../fase-1-ers/ERS_SGA_001_v1.8_borrador.md) (se conserva sin cambios)
**Estado:** borrador; no aprobado ni validado por abogado

## 1. Motivo
Reunir en la ERS las decisiones del solicitante tomadas el 20 y 21-oct-2026 al resolver los hallazgos del diseño técnico (HT-01, HT-02, HT-03, HT-05 y HT-08), más el criterio de aceptación de la segunda mitad de RN-15 (HP-01) y el ajuste del texto de API (HT-04). Antes de esta versión las decisiones solo constaban en el DAS v0.10 y el diseño técnico v0.6, que contradecían la ERS v1.8.

## 2. Cambios
| ID | Tipo | Descripción | Origen (hallazgo → decisión) |
|---|---|---|---|
| Sección 2.3 y 2.4 | modificado | Notificaciones web y correo en la v1; WhatsApp y SMS fuera; el correo ya no está excluido; comprobante del sistema y factura electrónica fuera de la v1 | HT-01, HT-02, HT-05 |
| Sección 2.5, 4, glosario | modificado | Servicio de correo como actor; supuestos; términos nuevos | HT-01, HT-05 |
| RF-23, RF-24, RF-44 | modificado | Correo en lugar de WhatsApp; sin estados posteriores; límites de contenido extendidos al correo (propuesta) | HT-01 |
| RF-27 | modificado | Avisos de seguridad a dos direcciones (cuatro eventos); cambio de contraseña y de segundo factor con la contraseña actual; restablecimiento por enlace de correo de 15 minutos | HT-05, HT-08 |
| RF-37 | modificado | Marcado como fase posterior | HT-02 |
| RF-47 | **nuevo** | Anotar el número del recibo físico | HT-02 |
| RF-40 | modificado | Exportación de todo el registro del titular, con la foto, en informe web imprimible | HT-03 |
| Sección 7 (datos) | modificado | Movimiento con número de recibo físico; Organización con correos; Comprobante como fase posterior | HT-01, HT-02, HT-05 |
| RNF-05 | modificado | Fallo del correo en lugar de WhatsApp | HT-01 |
| CA-04, CA-34, CA-37, CA-54 | modificado | Comprobante pasa a la fase posterior | HT-02 |
| CA-05, CA-08, CA-09, CA-43 | modificado | Canal de correo | HT-01 |
| CA-27, CA-47 | modificado | Alcance de la exportación; aviso de seguridad a dos direcciones | HT-03, HT-05 |
| CA-58 | **nuevo** | Movimientos sobre períodos futuros (RN-15, segunda mitad) | HP-01 |
| CA-59 | **nuevo** | Cambio y restablecimiento de contraseña y de segundo factor | HT-08 |
| CA-60 | **nuevo** | Fallo del aviso de seguridad | HT-05 |
| CA-61 | **nuevo** | Número de recibo físico | HT-02 |
| Sección 10 | modificado | Matriz: RN-15 completo con CA-58; recibos con RF-47 y CA-61; acceso con CA-59 y CA-60 | — |
| Sección 11 | modificado | Riesgos de correo, dominio, cuenta de correo y recibos de papel | — |
| DP-04, DP-19, DP-20 | modificado | WhatsApp futuro; segunda dirección y alcance de la exportación; recibo de papel y factura electrónica | — |
| Sección 12.1b | añadido | Tabla de decisiones del solicitante con hallazgo, requisitos y si fueron contra la recomendación | — |
| Sección 14, 15, 16, Q-17 | modificado | Lista de revisión; texto de API (HT-04); referencias 8b y 8c; Q-17 | HT-04 |

No se añadió ningún DP, RN, OL ni RNF nuevo. No se cambió el significado de ningún ID existente: RF-37, CA-37 y CA-54 conservan su enunciado y solo se marcan como fase posterior.

## 3. Impacto
- **Alcance:** cambia respecto de la v1.8: correo en lugar de WhatsApp y recibo de papel en lugar de comprobante del sistema.
- **Prioridad Alta diferida:** RF-37 y CA-37 (Alta en la estrategia de pruebas). Consta como aceptación del solicitante en la actualización 2026-10-21d. La lista de revisión de la ERS (sección 14) pide aceptarlo por escrito antes de aprobar.
- **DAS v0.10:** falta ajustar ADR-008 (canal), ADR-026 (correo de notificaciones y de restablecimiento) y ADR-013 (el temporizador de reintentos también cubriría las notificaciones). No se hizo.
- **Modelo de datos v0.3:** falta el campo opcional y único "número de recibo físico" y el cambio de Comprobante a fase posterior.
- **Estrategia de pruebas v0.2:** falta incorporar CA-58 a CA-61, el canal de correo y mover CA-37 y CA-54.
- **Diseño técnico v0.6:** sigue su base en la ERS v1.8; su contenido ya coincide con la v1.9, pero cita "ERS v1.8" como base.
- **Resumen para el abogado v2:** no se actualizó; hay que sumar la factura electrónica, la foto de la cédula en la exportación, la segunda dirección y los límites de RF-44 para el correo.

## 4. Decisiones
No se tomaron decisiones nuevas aquí; se trasladan las ya registradas (ver sección 12.1b de la ERS):
[2026-10-20h](../2026-10-20h_ht-05-recuperacion-acceso/CAMBIOS.md), [2026-10-21](../2026-10-21_ht-08-contrasena-segundo-factor/CAMBIOS.md), [2026-10-21b](../2026-10-21b_ht-01-canal-correo/CAMBIOS.md), [2026-10-21c](../2026-10-21c_ht-03-exportacion-titular/CAMBIOS.md) y [2026-10-21d](../2026-10-21d_ht-02-comprobante-fisico/CAMBIOS.md).

**Redacciones mías, propuestas, que el solicitante no revisó una por una:** CA-58 a CA-61 (los ejemplos numéricos y de nombres), la frase de RF-27 sobre alerta persistente y auditoría, y la extensión de RF-44 al correo. Revisarlas.

**Pendientes:** validación legal (DP-17, DP-19, DP-20); ajustes del DAS, modelo de datos, estrategia de pruebas y resumen para el abogado; dominio y dos direcciones de correo; intervalo del reintentador; protecciones del enlace de restablecimiento (respuesta idéntica, invalidar sesiones, límite de solicitudes) sin decidir.

## 5. Evidencia y fuentes
Las de las actualizaciones citadas arriba. Los textos legales de RF-40 provienen de la Ley 8968, art. 7, y el Reglamento 37554-JP, arts. 21 y 22 (copias .docx del Archivo Nacional, leídas en esos artículos). No hay fuentes nuevas.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1` (resultado abajo). Además se buscaron a mano las menciones de WhatsApp y comprobante en la ERS v1.9.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
