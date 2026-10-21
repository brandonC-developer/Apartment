# Documentación — Sistema de Gestión de Alquileres (SGA)

**Estado general:** ningún documento está aprobado. Todos son borradores.

## Mapa de fases

| Fase | Carpeta | Documento vigente | Estado |
|---|---|---|---|
| 1. Especificación de requisitos (ERS) | `fase-1-ers/` | `ERS_SGA_001_v1.9_borrador.md` | Borrador; pendiente de validación legal y aprobación |
| 2. Arquitectura de software | `fase-2-arquitectura/` | `DAS_SGA_001_v0.11_borrador.md` | Borrador; depende de la ERS |
| 3. Diseño técnico | `fase-3-diseno-tecnico/` | `MODELO_DATOS_SGA_001_v0.4_borrador.md`; `DISENO_TECNICO_SGA_001_v0.7_borrador.md` | Iniciada; modelo de datos y diseño técnico, en borrador sin revisar |
| 4. Estrategia y plan de pruebas | `fase-4-pruebas/` | `ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md` | Iniciada; estrategia en borrador sin revisar |
| 5. Plan de implementación | `fase-5-implementacion/` | — | No iniciada |
| 6. Despliegue y operación | `fase-6-despliegue-operacion/` | — | No iniciada |

Carpetas transversales:
- `legal/` — resumen para el abogado y, cuando lleguen, los dictámenes.
- `metodologia/` — evaluación de la metodología de seis fases y la plantilla de registro de cambios.
- `actualizaciones/` — un registro por cada actualización, con el motivo, los cambios, las decisiones y la evidencia.
- `.claude/skills/recomendacion-buenas-practicas/` (en la raíz del proyecto, fuera de `DOC/`) — skill con el modo de trabajo para recomendaciones.
- `herramientas/` — `verificar_coherencia.ps1`: comprueba identificadores, enlaces, vigencia, versión de la base de cada documento, cobertura de la matriz de la ERS y de los CA en la estrategia de pruebas, y que los README listen sus archivos. Ejecutar con `powershell -File DOC\herramientas\verificar_coherencia.ps1`.

## Convenciones

1. **Un solo lugar por documento.** Cada versión vive en la carpeta de su fase con el nombre `PREFIJO_VERSION_estado.md`. Una versión aprobada o reemplazada **no se edita**; los cambios van en una versión nueva.
2. **Cada actualización tiene su carpeta** en `actualizaciones/AAAA-MM-DD_<documentos y versiones>/` con un `CAMBIOS.md` basado en `metodologia/plantilla_CAMBIOS.md`. Esa carpeta enlaza los documentos de las carpetas de fase; no los copia.
3. **La trazabilidad empieza en el origen:** cada cambio de requisito indica la pregunta, la respuesta y la decisión que lo originó.
4. **Las decisiones pendientes** usan identificadores únicos (DP-nn) comunes a la ERS y al DAS.
5. **Ninguna fase se da por cerrada** hasta tener responsable, fecha y aceptación formal en su registro de aprobación.

## Historial de actualizaciones

| Fecha | Carpeta | Resumen |
|---|---|---|
| 2026-10-14 | `actualizaciones/2026-10-14_ERS-v1.4_DAS-v0.3/` | ERS v1.4 y DAS v0.3 |
| 2026-10-17 | `actualizaciones/2026-10-17_ERS-v1.5_DAS-v0.4/` | ERS v1.5 y DAS v0.4; obligaciones legales; revisión de coherencia |
| 2026-10-17 (b) | `actualizaciones/2026-10-17b_ERS-v1.6_DAS-v0.5/` | ERS v1.6 y DAS v0.5; cierre de DP-22, DP-24 y DP-25 |
| 2026-10-17 (c) | `actualizaciones/2026-10-17c_ERS-v1.7_DAS-v0.6/` | ERS v1.7 y DAS v0.6; cierre de DP-07 y DP-08, DP-04 diferida; modelo de datos v0.1 y v0.2 con prueba en PostgreSQL; hallazgos H1 a H13 |
| 2026-10-17 (d) | `actualizaciones/2026-10-17d_ERS-v1.8_DAS-v0.7/` | ERS v1.8 y DAS v0.7; cierre de DP-14, DP-23 y DP-26; H4 provisional; lectura del Reglamento 37554-JP (OL-19 a OL-21); resumen para el abogado v2 |
| 2026-10-17 (e) | `actualizaciones/2026-10-17e_QA-documentos/` | QA de vigencia de todos los documentos: 16 hallazgos corregidos, script ampliado |
| 2026-10-20 | `actualizaciones/2026-10-20_README-fase-3/` | Corrección del README de la fase 3 (entradas ERS v1.8 y DAS v0.7; ADR-002) |
| 2026-10-20 (b) | `actualizaciones/2026-10-20b_ERS-v1.8-matriz/` | Matriz de trazabilidad de la ERS v1.8: RN-10, RN-15, RN-25 y seis RNF sin criterio |
| 2026-10-20 (c) | `actualizaciones/2026-10-20c_DAS-v0.8-Django/` | DAS v0.8: Python y Django con interfaz renderizada por el servidor (ADR-022); RE-04 actualizada |
| 2026-10-20 (d) | `actualizaciones/2026-10-20d_stack-decisiones/` | DAS v0.9: PostgreSQL 18, systemd, documentos en disco, DigitalOcean con Ubuntu 26.04, Nginx y Gunicorn, respaldos a Spaces e integración continua (ADR-002, 003, 013, 023 a 025) |
| 2026-10-20 (e) | `actualizaciones/2026-10-20e_fase-4-estrategia-pruebas/` | Fase 4 iniciada: estrategia de pruebas v0.1 (niveles, cobertura de los 57 CA, RNF sin criterio, pruebas de operación; hallazgos HP-01 a HP-04) |
| 2026-10-20 (f) | `actualizaciones/2026-10-20f_fase-4-decisiones/` | Estrategia de pruebas v0.2: ejecutor de Django, Selenium, Locust, cobertura sin umbral, restauración trimestral y mensual, RN-15 y prioridades diferibles |
| 2026-10-20 (g) | `actualizaciones/2026-10-20g_fase-3-diseno-tecnico/` | Diseño técnico v0.1: la API no es pública en la v1; interfaces, permisos por operación y flujos F-01 a F-09; hallazgos HT-01 a HT-07 |
| 2026-10-20 (h) | `actualizaciones/2026-10-20h_ht-05-recuperacion-acceso/` | DAS v0.10 y diseño técnico v0.2: avisos de seguridad de la cuenta por correo (ADR-026); HT-05 resuelto; hallazgos HT-08 y HT-09 |
| 2026-10-21 | `actualizaciones/2026-10-21_ht-08-contrasena-segundo-factor/` | Diseño técnico v0.3: HT-08 resuelto (cambio con contraseña actual; restablecimiento con enlace por correo de 15 minutos); dos decisiones contra la recomendación |
| 2026-10-21 (b) | `actualizaciones/2026-10-21b_ht-01-canal-correo/` | Diseño técnico v0.4: HT-01 resuelto como cambio de alcance (v1 con notificación web y correo; WhatsApp futuro); corrección del destinatario de WhatsApp |
| 2026-10-21 (c) | `actualizaciones/2026-10-21c_ht-03-exportacion-titular/` | Diseño técnico v0.5: HT-03 resuelto (exportación del titular con todo su registro y la foto de la cédula, en informe web imprimible); lectura de Ley 8968 art. 7 y Reglamento arts. 21 y 22 |
| 2026-10-21 (d) | `actualizaciones/2026-10-21d_ht-02-comprobante-fisico/` | Diseño técnico v0.6: HT-02 resuelto como cambio de alcance (recibo de papel fuera del sistema primero; comprobante del sistema después); difiere RF-37 y CA-37 |
| 2026-10-21 (e) | `actualizaciones/2026-10-21e_ERS-v1.9/` | ERS v1.9: reúne las decisiones de HT-01, 02, 03, 05 y 08 (notificaciones por correo, avisos de seguridad, restablecimiento de contraseña, exportación del titular, recibo de papel antes del comprobante), nuevos RF-47 y CA-58 a CA-61; difiere RF-37 (Alta) |
| 2026-10-21 (f) | `actualizaciones/2026-10-21f_DAS-v0.11/` | DAS v0.11: alinea la arquitectura con la ERS v1.9 (ADR-008, 010, 013, 018 y 026; RE-05; correo en lugar de WhatsApp; recibo físico; restablecimiento de contraseña) |
| 2026-10-21 (g) | `actualizaciones/2026-10-21g_auditoria-coherencia/` | Auditoría de enlaces, vigencia y coherencia: 4 correcciones en ERS v1.9 y DAS v0.11; lista de documentos desalineados (modelo de datos, estrategia de pruebas, diseño técnico, resumen para el abogado y el script) |
| 2026-10-21 (h) | `actualizaciones/2026-10-21h_alineacion-MDD-EPP-DTE/` | Modelo de datos v0.4, diseño técnico v0.7 y estrategia de pruebas v0.3: alineados con la ERS v1.9 y el DAS v0.11 (recibo físico, correo, avisos de seguridad, restablecimiento de contraseña); sin decisiones nuevas |
| 2026-10-21 (i) | `actualizaciones/2026-10-21i_registro-validacion-legal/` | Registro de la declaración del solicitante de que el abogado verificó todo; sin dictamen, nombre ni fecha aportados |
| 2026-10-21 (j) | `actualizaciones/2026-10-21j_script-coherencia/` | Script de coherencia ampliado: citas en diseño técnico y pruebas, base declarada, cobertura de la matriz y de CA, README de fase |
| 2026-10-21 (k) | `actualizaciones/2026-10-21k_decisiones-tecnicas-abiertas/` | Cierre de cinco decisiones técnicas: dominio .com en Cloudflare, dos direcciones del solicitante, reintentador cada 1 minuto, protecciones del enlace de restablecimiento y auditoría de cédulas y exportaciones |
| 2026-10-21 (l) | `actualizaciones/2026-10-21l_ht-06-ht-07/` | HT-06 y HT-07 resueltos: actor sistema (tipo proceso) con su ejecución en la auditoría; bloqueo de fila con select_for_update sin nowait; ideas de dos cuentas y sistema tipo CMS registradas |
| 2026-10-21 (m) | `actualizaciones/2026-10-21m_adr-027-roles-base-de-datos/` | ADR-027: dos roles de base de datos (dueño solo para migraciones; aplicación sin UPDATE ni DELETE sobre el historial) más guardas en Django; aplica R12 |
| 2026-10-21 (n) | `actualizaciones/2026-10-21n_adr-028-identificadores/` | ADR-028: identificadores internos enteros de 64 bits autoincrementales (BigAutoField); H7 resuelto |
| 2026-10-21 (o) | `actualizaciones/2026-10-21o_roles-peer-respaldos/` | Punto 3: tres roles de base de datos (dueño, aplicación, respaldos de solo lectura) con autenticación peer por socket local, sin contraseñas; ajuste de ADR-027 y ADR-024 |
| 2026-10-21 (p) | `actualizaciones/2026-10-21p_adr-029-conexiones/` | ADR-029: una conexión por petición (CONN_MAX_AGE = 0), sin pool, por socket local; se revisa con la prueba de carga |
| 2026-10-21 (q) | `actualizaciones/2026-10-21q_adr-030-aplicaciones-django/` | ADR-030: seis aplicaciones de Django, servicios y selectores, claves foráneas solo hacia abajo; propuesta del asistente con la elección delegada |

## Control de versiones

El proyecto tiene un repositorio Git en la raíz creado por el solicitante; al 17-oct-2026 el árbol de trabajo estaba limpio y sincronizado con `origin/main`. La visibilidad del repositorio remoto no está verificada: confirmar que no sea público, pues contiene análisis legal y decisiones del negocio. Las fuentes consultadas (`metodologia/EVALUACION_METODOLOGIA_v1.md`, ajuste 5) recomiendan mantener la documentación bajo control de versiones con revisión de cambios. Hasta entonces, las versiones se distinguen por nombre de archivo.
