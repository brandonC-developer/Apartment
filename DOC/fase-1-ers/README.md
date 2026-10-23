# Fase 1 — Especificación de requisitos (ERS)

**Qué define:** qué debe hacer el sistema, reglas de negocio, restricciones y criterios de aceptación.

| Versión | Archivo | Estado |
|---|---|---|
| 1.4 | `ERS_SGA_001_v1.4_borrador_actualizado.md` | Reemplazada |
| 1.5 | `ERS_SGA_001_v1.5_borrador.md` | Reemplazada por la 1.6 |
| 1.6 | `ERS_SGA_001_v1.6_borrador.md` | Reemplazada por la 1.7 |
| 1.7 | `ERS_SGA_001_v1.7_borrador.md` | Reemplazada por la 1.8 |
| 1.8 | `ERS_SGA_001_v1.8_borrador.md` | Reemplazada por la 1.9 |
| 1.9 | `ERS_SGA_001_v1.9_borrador.md` | Reemplazada por la 1.10 |
| 1.10 | `ERS_SGA_001_v1.10_borrador.md` | Reemplazada por la 1.11 |
| 1.11 | `ERS_SGA_001_v1.11_borrador.md` | Reemplazada por la 1.12 |
| 1.12 | `ERS_SGA_001_v1.12_borrador.md` | Reemplazada por la 1.13 |
| 1.13 | `ERS_SGA_001_v1.13_borrador.md` | Reemplazada por la 1.14 |
| 1.14 | `ERS_SGA_001_v1.14_borrador.md` | Reemplazada por la 1.15 |
| 1.15 | `ERS_SGA_001_v1.15_borrador.md` | Reemplazada por la 1.16 |
| **1.16** | `ERS_SGA_001_v1.16_borrador.md` | **Vigente** (borrador, no aprobada) |

**Incorporado en la v1.16 (23-oct-2026):** DP-27 resuelta (el servidor elimina los metadatos de la imagen; CA-82), sin antivirus y con decodificación completa de la imagen (nota en RF-02; CA-83) y nueva DP-31 (transferencia de datos a Resend y DigitalOcean, para el abogado). Totales: 53 RF, 30 RN, 20 RNF, 83 CA, 31 DP. Actualizaciones [(zo)](../actualizaciones/2026-10-23zo_br-05-metadatos-imagenes/CAMBIOS.md), [(zp)](../actualizaciones/2026-10-23zp_br-06-antivirus/CAMBIOS.md), [(zs)](../actualizaciones/2026-10-23zs_br-10-transferencia-a-proveedores/CAMBIOS.md) y [(zt)](../actualizaciones/2026-10-23zt_alineacion-ERS-v1.16/CAMBIOS.md).

**Incorporado en la v1.15 (23-oct-2026):** RF-53 y CA-79 (vigilar el respaldo diario), RNF-19 y CA-80 (protección de las cuentas de servicios externos, por inspección) y RNF-20 y CA-81 (autenticación del correo saliente, en la etapa B); totales 53 RF, 20 RNF y 81 CA. Corrige el número de versión de la tabla de control, que decía 1.12 en las v1.13 y v1.14. Ver `../actualizaciones/2026-10-23zm_alineacion-ERS-v1.15/CAMBIOS.md`.

**Incorporado en la v1.14 (23-oct-2026):** máximo de 10 fotografías por contrato y punto de partida de 3508 px y calidad 0,85 para reducir la fotografía del contrato (RF-52, CA-76); DP-29 dividida: máximo resuelto, cifras definitivas por medir en la E2. Ver `../actualizaciones/2026-10-23l_ERS-v1.14/CAMBIOS.md`.

**Incorporado en la v1.13 (23-oct-2026):** DP-30 resuelta: los inquilinos sin frente se tratan con la retención sin contrato de RF-41 y CA-66 (sin plazo nuevo) y se hacen visibles con una indicación en la ficha y un filtro «Sin frente» en la lista (RF-03, CA-78). Sin RF ni CA nuevos. Ver `../actualizaciones/2026-10-23j_ERS-v1.13/CAMBIOS.md`.

**Incorporado en la v1.12 (23-oct-2026):** tope de subida de 5 MiB = 5 242 880 bytes; sin zona temporal de archivos (el inquilino se guarda primero y las fotografías se suben después a su ficha; el frente se exige antes de asignar un contrato: RF-01, RF-03, RF-07, CA-01, CA-78, DP-30); perfil de la propiedad con acciones desactivadas sin contrato vigente y «Reemplazar» (RF-51, RF-52, CA-75). Ver `../actualizaciones/2026-10-23e_ERS-v1.12/CAMBIOS.md`. Los demás documentos se alinearon con la v1.12 el 23-oct-2026 (actualización 2026-10-23f).

**Incorporado en la v1.11 (22-oct-2026):** la cédula se agrega desde el perfil de la propiedad y se guarda en el inquilino (RF-51, CA-75); la fotografía del contrato es un documento nuevo, asociado al contrato y distinto de la de la cédula (RF-52, CA-76, CA-77, entidad Documento del contrato); término "perfil de la propiedad"; DP-28 (conservación de la fotografía del contrato) y DP-29 (número de fotografías y cifras de reducción, por medir). Ver `../actualizaciones/2026-10-22j_ERS-v1.11/CAMBIOS.md`.

**Incorporado en la v1.10 (22-oct-2026):** reducción de la fotografía del documento en el navegador antes de enviarla (RF-50, CA-73, CA-74, supuesto S-03, DP-27) y envío del frente y el reverso en peticiones separadas (nota en RF-02). Las cifras (2048 px, calidad 0,85, objetivo de 2 MB, tope de 5 MB) son valores de diseño sin medir. Ver `../actualizaciones/2026-10-22f_ERS-v1.10/CAMBIOS.md`.

**Incorporado en la v1.9:** decisiones del solicitante del 20 y 21-oct-2026 sobre notificaciones (web y correo en la v1; WhatsApp futuro), cuenta (avisos de seguridad, cambio y restablecimiento de contraseña), exportación del titular y recibo de papel antes del comprobante del sistema (RF-37 dividido, RF-47 nuevo); criterios CA-58 a CA-72 y los requisitos RF-48 y RF-49 (revisión por módulos del 21-oct-2026). Difiere requisitos de prioridad Alta y varias decisiones van contra la recomendación; ver `../actualizaciones/2026-10-21e_ERS-v1.9/CAMBIOS.md`.

**Documentos alineados con la v1.11:** el 22-oct-2026 se alinearon, sin versión nueva, el DAS v0.11, el diseño técnico v0.7, la estrategia de pruebas v0.3, el plan de implementación v0.1, la lista de verificación v0.1 y el registro de avance (ver `../actualizaciones/2026-10-22k_alineacion-ERS-v1.11/CAMBIOS.md`). El modelo de datos v0.4 solo lo anota: le falta la entidad Documento del contrato, que requiere una versión nueva.

**Siguiente acción:** modelo de amenazas v0.3 con los requisitos nuevos; decidir DP-28 y DP-27 y medir DP-29, validación legal de la sección 3 (DP-17 a DP-21), resolver las decisiones pendientes de la sección 12 y obtener la aprobación del responsable del negocio.

**Actualizaciones:** ver `../actualizaciones/`.
