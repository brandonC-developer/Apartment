# Actualización 2026-10-23 (o) — Endurecimiento, medida 1: acceso remoto por SSH (propuesta 3)

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en una versión nueva del DAS y en el procedimiento de la fase 6 cuando se hayan decidido las medidas que se quieran adoptar. [DOC/README.md](../../README.md)
**Origen:** propuesta 3 de la [actualización 2026-10-22](../2026-10-22_investigacion-endurecimiento-servidor/CAMBIOS.md); base y orden decididos en la [actualización 2026-10-22 (c)](../2026-10-22c_decision-base-endurecimiento-lynis/CAMBIOS.md)
**Estado:** decisión registrada; documentos sin cambiar; no aprobado

## 1. Pregunta, respuesta y decisión
| Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|
| ¿Cómo se entra al servidor por SSH? | "Solo llave ed25519, sin contraseña ni root" (recomendada por el asistente) | Acceso solo con llave ed25519 protegida con passphrase; sin contraseña de cuenta; sin acceso directo de `root`; un usuario administrador distinto del usuario que ejecuta la aplicación; `sshd -t` antes de reiniciar el servicio. El segundo factor (TOTP o FIDO) queda como mejora futura, no decidida |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| OpenBSD, `sshd_config`: https://man.openbsd.org/sshd_config | Documentación oficial | Leída por resumen (WebFetch, 23-oct-2026) | Por defecto `PasswordAuthentication yes`, `PermitRootLogin prohibit-password`, `PubkeyAuthentication yes`, `MaxAuthTries 6`; `AuthenticationMethods` y `AllowUsers` | Es el manual de OpenSSH de OpenBSD; el paquete de Ubuntu 26.04 puede traer otros valores por defecto, sin verificar |
| Mozilla, guía de OpenSSH: https://infosec.mozilla.org/guidelines/openssh | Guía reconocida | Leída por resumen (WebFetch, 23-oct-2026) | Configuración "Modern" con solo llave pública; `PermitRootLogin No` por trazabilidad (usuario normal y `sudo`); ed25519 preferida; passphrase fuerte en llaves de usuario; revisar PAM porque `PasswordAuthentication no` no basta | Pie "©2017", sin versión ni fecha de revisión: puede estar desactualizada. No menciona `AllowUsers` ni `AllowGroups` |
| Canonical, servidor OpenSSH: https://ubuntu.com/server/docs/how-to/security/openssh-server/ | Documentación del proveedor | Leída en la investigación del 22-oct-2026 | Recomienda ed25519 y `sshd -t` antes de reiniciar | No trae sección de endurecimiento |

## 3. Lo que propone el asistente y el solicitante no decidió
- La separación entre usuario administrador y usuario de la aplicación: criterio del asistente, sin fuente leída.
- Revisar `/etc/pam.d/sshd` para que PAM no acepte contraseñas (por la guía de Mozilla).
- Guardar una copia de la llave y conocer la vía de recuperación del proveedor: **no se verificó** si DigitalOcean ofrece una consola de recuperación.
- Probar una segunda sesión antes de cerrar la primera al cambiar `sshd_config`.
- El segundo factor como mejora futura.

## 4. Qué no se hizo
- No se aplicó nada: no hay servidor. Es una configuración de la fase 6.
- No se verificaron los valores por defecto del paquete de OpenSSH de Ubuntu 26.04 ni la interacción con el firewall (propuesta 4, aún sin decidir).
- La restricción del acceso SSH a la IP del solicitante pertenece a la propuesta 4 y no está decidida.

## 5. Estado de las medidas de endurecimiento
| N.º | Medida | Estado |
|---|---|---|
| 1 y 2 | Marco y verificación (CIS) | Sustituidas por la decisión de la actualización (c): no se afirma conformidad con CIS; se usa documentación oficial, OWASP y NIST, y Lynis para auditar |
| **3** | **Acceso remoto por SSH** | **Decidida (esta actualización)** |
| 4 | Firewall (Cloud Firewall y UFW) | Pendiente |
| 5 | Actualizaciones automáticas y reinicio | Pendiente |
| 6 y 12 | Servicios bajo usuarios sin privilegios y `systemd` | Pendiente |
| 7 | HTTPS y cabeceras | Pendiente |
| 8 | Django (`check --deploy`, `SECRET_KEY`, límite de intentos, archivos subidos) | Pendiente |
| 9 | Revisión crítica con otra persona antes de datos reales | Pendiente |
| 11 | Gunicorn por socket Unix | Pendiente |
| 13 y 14 | Nginx (`server_tokens`, hosts desconocidos, límite de intentos) | Pendiente (el tope de subida ya está decidido) |
| 15 a 18 | PostgreSQL (red, acceso, registro, contraseñas) | Pendiente |

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
