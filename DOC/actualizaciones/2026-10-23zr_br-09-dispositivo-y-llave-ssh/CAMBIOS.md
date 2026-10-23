# Actualización 2026-10-23 (zr) — BR-09: dispositivo del administrador y llave SSH

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el modelo de amenazas (versión nueva: BR-09, AM-02, AM-15), el DAS (ADR-032, decisión 1) y el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** brecha BR-09 y amenazas AM-02 y AM-15 del [modelo de amenazas v0.3](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.3_borrador.md)
**Estado:** decisión registrada; documentos sin cambiar; no aprobado

## 1. Pregunta, respuesta y decisión
| Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|
| ¿Cómo se protege el dispositivo del administrador y su llave SSH? | "Prácticas mínimas en la fase 6; llave física como mejora futura" (recomendada por el asistente) | La fase 6 incluirá un procedimiento del dispositivo con prácticas mínimas: sistema y navegador actualizados, cifrado de disco, bloqueo de pantalla, llave ed25519 con passphrase (ya decidido en el ADR-032), copia de la llave fuera del dispositivo y cuándo revocarla si se pierde. La llave de seguridad física (FIDO2) queda como **mejora futura**, no como requisito |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Notas de versión de OpenSSH 8.2: https://www.openssh.com/txt/release-8.2 | Documentación del proveedor | **Solo resultados de búsqueda** | Existen las llaves `ecdsa-sk` y `ed25519-sk` respaldadas por hardware; el token debe estar conectado al usarlas; no todos los tokens admiten `ed25519-sk` ni claves residentes | No se abrió la página; no se verificó la versión de OpenSSH de Ubuntu 26.04 |
| NIST SP 800-46 Rev. 2: https://csrc.nist.gov/pubs/sp/800/46/r2/final | Estándar | **Solo resultados de búsqueda** (ficha de la publicación) | Solo que existe y trata el acceso remoto y el teletrabajo | **No se leyó su contenido**; no respalda ninguna de las prácticas concretas; es de 2016 y tiene un borrador de la Rev. 3 |

## 3. Lo que propone el asistente y el solicitante no decidió
- La **lista concreta de prácticas** (cifrado de disco, bloqueo de pantalla, copia de la llave, revocación): criterio del asistente, sin fuente leída; hay que contrastarla con una guía antes de la fase 6.
- Que la llave física sea mejora y no requisito: se apoya en el costo y en el riesgo de quedarse sin acceso con un solo administrador; **el costo de la llave física no se verificó**.
- No se evaluó el segundo factor de SSH por otra vía (por ejemplo, TOTP con PAM).
- AM-02 sigue **alto** y sin aceptar: el procedimiento reduce su probabilidad, pero el sistema no puede impedirlo.

## 4. Qué no se hizo
- No se escribió el procedimiento de la fase 6 ni se actualizó el modelo de amenazas.
- No se revisó el estado real del dispositivo del solicitante.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
