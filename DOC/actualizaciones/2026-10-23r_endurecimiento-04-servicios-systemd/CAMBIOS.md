# Actualización 2026-10-23 (r) — Endurecimiento, medidas 4 y 5: servicios bajo usuarios sin privilegios y `systemd` (propuestas 6 y 12)

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en una versión nueva del DAS (ADR-024, ADR-027) y en el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** propuestas 6 y 12 de las actualizaciones [2026-10-22](../2026-10-22_investigacion-endurecimiento-servidor/CAMBIOS.md) y [2026-10-22 (b)](../2026-10-22b_endurecimiento-nginx-gunicorn-postgresql/CAMBIOS.md); la 12 repite la 6 para Gunicorn, por eso se tratan juntas. Sigue a la [medida 3 (actualizaciones)](../2026-10-23q_endurecimiento-03-actualizaciones/CAMBIOS.md)
**Estado:** decisión registrada; documentos sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Qué usuario del sistema ejecuta Gunicorn y el proceso diario? | "Usuario estático sin privilegios, igual al rol de BD" (recomendada por el asistente) | Un usuario de sistema **estático**, sin shell ni directorio personal, con el mismo nombre que el rol de la aplicación en PostgreSQL (para la autenticación `peer` de ADR-027). Ejecuta Gunicorn y el proceso diario. El usuario administrador del SSH (medida 1) es distinto; las migraciones las lanza ese administrador con `sudo -u` (ADR-027). **No se usa `DynamicUser=true`** |
| 2 | ¿Qué restricciones de `systemd` lleva cada unidad? | "El conjunto base leído, medido con `systemd-analyze`" (recomendada) | `NoNewPrivileges=true`, `ProtectSystem=strict`, `ReadWritePaths=` solo con el directorio de documentos privados y el de registros, `ProtectHome=true`, `PrivateTmp=true`, `PrivateDevices=true`, `CapabilityBoundingSet=` vacío y `RuntimeDirectory=` para el socket de Gunicorn. En la etapa A se mide cada unidad con `systemd-analyze security` y se añade lo que haga falta |
| 3 | ¿La unidad del respaldo lleva el mismo patrón? | "Sí: usuario estático del rol de respaldos y restricciones base" (recomendada) | Tercer usuario de sistema estático y sin privilegios, con el nombre del rol de respaldos (`peer`, ADR-027); las mismas restricciones base; escritura solo en su directorio de trabajo y lectura de los documentos privados |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| systemd.exec: https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html | Documentación oficial | **Leída en parte**: los primeros 100 000 de 244 377 caracteres (WebFetch, 23-oct-2026); la herramienta no permite pedir el resto | `NoNewPrivileges`, `ProtectSystem` (`strict`, `full`), `ProtectHome`, `PrivateTmp`, `PrivateDevices`, `ReadWritePaths`/`ReadOnlyPaths`, `CapabilityBoundingSet`, `RuntimeDirectory`, `User=`, `DynamicUser=` (asigna usuario y grupo al iniciar y los libera al parar; implica `NoNewPrivileges`, `ProtectSystem=strict` y `ProtectHome=read-only`) | **No se leyeron** `RestrictAddressFamilies`, `SystemCallFilter`, `ProtectKernelTunables`, `RestrictNamespaces`, `MemoryDenyWriteExecute` ni `LockPersonality` |
| systemd-analyze: https://www.freedesktop.org/software/systemd/man/latest/systemd-analyze.html | Documentación oficial | Leída por resumen (23-oct-2026) | `security` da un puntaje de exposición de 0,0 a 10,0 por unidad (alto = poco sandboxing); admite una unidad concreta y `--offline` | Solo evalúa las funciones del propio systemd; un puntaje alto no implica vulnerabilidad; no cubre D-Bus |
| DAS ADR-027 y ADR-024 (PostgreSQL, autenticación `peer`, roles predefinidos) | Documento del proyecto, con fuentes leídas por resumen el 21-oct-2026 | Releído | Tres roles con `peer`; el rol de respaldos es de solo lectura | Que `pg_dumpall --globals-only` funcione sin superusuario no está confirmado |

## 3. Lo que propone el asistente y el solicitante no decidió
- Descartar `DynamicUser=true` por su relación con `peer` y la propiedad de los archivos privados: **no se verificó** que `peer` reconozca a un usuario dinámico; es criterio del asistente.
- Que el respaldo tenga su propio usuario: criterio del asistente, derivado de ADR-027.
- Dónde viven exactamente el directorio de documentos y el de registros: sin decidir.
- Cómo se protegen las credenciales con las que el respaldo sube la copia cifrada: no se diseñó.

## 4. Qué no se hizo
- No se aplicó nada: no hay servidor.
- **No se verificó** que una conexión por socket Unix a PostgreSQL funcione desde una unidad con `ProtectSystem=strict`.
- No se leyeron las directivas de red y de llamadas al sistema; **no se adoptan** hasta medir en la etapa A (la aplicación necesita red saliente para Resend).
- No se definió un puntaje objetivo de `systemd-analyze security` (no hay fuente para fijarlo).
- Nombres concretos de los usuarios y de las unidades: sin decidir.

## 5. Estado de las medidas de endurecimiento (actualizado)
| N.º | Medida | Estado |
|---|---|---|
| 1 y 2 | Marco y verificación (CIS) | Sustituidas por la decisión de la actualización (c) |
| 3 | Acceso remoto por SSH | Decidida ([actualización (o)](../2026-10-23o_endurecimiento-01-acceso-ssh/CAMBIOS.md)) |
| 4 | Firewall | Decidida ([actualización (p)](../2026-10-23p_endurecimiento-02-firewall/CAMBIOS.md)), salvo la salida y los rangos de Cloudflare |
| 5 | Actualizaciones automáticas y reinicio | Decidida ([actualización (q)](../2026-10-23q_endurecimiento-03-actualizaciones/CAMBIOS.md)), salvo `Automatic-Reboot-WithUsers` y la hora del respaldo |
| **6 y 12** | **Servicios bajo usuarios sin privilegios y `systemd`** | **Decididas (esta actualización)**, salvo rutas, nombres y directivas de red |
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
