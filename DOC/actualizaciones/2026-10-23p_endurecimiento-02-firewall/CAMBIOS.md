# Actualización 2026-10-23 (p) — Endurecimiento, medida 2: firewall (propuesta 4)

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en una versión nueva del DAS (ADR-023 la recoge en parte) y en el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** propuesta 4 de la [actualización 2026-10-22](../2026-10-22_investigacion-endurecimiento-servidor/CAMBIOS.md); sigue a la [medida 1 (SSH)](../2026-10-23o_endurecimiento-01-acceso-ssh/CAMBIOS.md)
**Estado:** decisión registrada; documentos sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Qué capas de firewall se usan? | "Cloud Firewall + UFW con las mismas reglas" (recomendada por el asistente) | Se mantienen las dos capas (ADR-023). Cloud Firewall con denegación por defecto; UFW dentro del servidor con las mismas reglas y ninguna más (excepto la del SSH, ver 2). Una tabla única en la fase 6; todo cambio se hace en las dos |
| 2 | ¿Desde dónde se acepta el SSH (puerto 22)? | "Tu IP en Cloud Firewall; UFW abierto con 'ufw limit'" (recomendada) | Cloud Firewall: 22 solo desde la IP del solicitante (se edita desde el panel sin entrar por SSH). UFW: 22 abierto con `ufw limit`. **Es la única regla distinta entre las dos capas** y se anota en la tabla de la fase 6 |
| 3 | ¿Qué se hace con IPv6 en el servidor? | "No activar IPv6" (recomendada) | IPv6 no se activa en el Droplet; solo reglas para IPv4. Se confirma con `ufw status verbose` y `ip6tables` que no queda nada abierto por IPv6 |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| DigitalOcean, características de Cloud Firewalls: https://docs.digitalocean.com/products/networking/firewalls/details/features/ | Documentación del proveedor | Leída por resumen (WebFetch, 23-oct-2026) | Firewall con estado en la red; bloquea lo no permitido; la regla de denegación gana; actúa antes de que el tráfico llegue al servidor | No trata IPv6, ICMP, reglas de salida por defecto ni límites |
| DigitalOcean, configurar reglas: https://docs.digitalocean.com/products/networking/firewalls/how-to/configure-rules/ | Documentación del proveedor | Leída por resumen (23-oct-2026) | Un puerto se limita a una IP o CIDR (también IPv6); las reglas nuevas vienen prellenadas con "All IPv4" y "All IPv6"; las reglas permiten por defecto | — |
| DigitalOcean, depurar un firewall: https://docs.digitalocean.com/support/how-do-i-debug-a-firewall-causing-connection-problems-with-my-droplet/index.html.md | Documentación del proveedor | Leída por resumen (23-oct-2026) | Con ambos firewalls "they may have conflicting rule sets"; recomienda alinear las reglas del local con las del Cloud Firewall; comandos de revisión (`ufw status verbose`, `ip6tables`) | No explica la interacción con IPv6 |
| DigitalOcean, IPv6: https://docs.digitalocean.com/products/networking/ipv6/ | Documentación del proveedor | Leída por resumen (23-oct-2026) | IPv6 es opcional; los Droplets reciben IPv4 por defecto; se desactiva en la configuración de la interfaz | No describe los pasos de activación |
| Manual de UFW, Ubuntu: https://manpages.ubuntu.com/manpages/noble/en/man8/ufw.8.html | Documentación oficial | Leída por resumen (23-oct-2026) | Desactivado tras instalar; entrada en denegar y salida en permitir; IPv6 permitido por defecto; `ufw limit` bloquea con 6 o más conexiones en 30 segundos | Manual de Ubuntu 24.04 ("noble"); el de 26.04 no se abrió |
| Búsqueda sobre la interacción entre Cloud Firewall y UFW | Resultados de búsqueda | Solo resultados | Capas distintas (red y host); reglas separadas | **Ninguna fuente confirma cómo se combinan con IPv6**; que un paquete deba pasar por las dos capas es inferencia del asistente |

## 3. Reglas resultantes (propuesta del asistente, sin probar)
| Capa | Entrada | Salida |
|---|---|---|
| Cloud Firewall | 22/tcp solo desde la IP del solicitante; 80/tcp y 443/tcp desde IPv4 | **Sin decidir** |
| UFW | Política de entrada en denegar; 80/tcp y 443/tcp permitidos; 22/tcp con `ufw limit` | Política por defecto (permitir); **sin decidir** si se restringe |

## 4. Lo que propone el asistente y el solicitante no decidió
- Que la segunda capa (UFW) sirva de respaldo si el servidor quedara fuera del Cloud Firewall: criterio del asistente, sin fuente.
- Qué hacer con la **salida** de tráfico en las dos capas (no se trató).
- Si 80 y 443 se limitan a los rangos de Cloudflare cuando se use como proxy: **no se investigó ni se decidió**.
- Cuál es la IP del solicitante y cómo se actualiza si cambia (se hace desde el panel de DigitalOcean).

## 5. Qué no se hizo
- No se aplicó nada: no hay servidor. Es una configuración de la fase 6.
- No se probó la combinación de ambos firewalls ni la ausencia de IPv6.
- No se verificó si DigitalOcean ofrece una consola de recuperación en caso de perder el acceso por SSH.
- Los valores por defecto del paquete de UFW de Ubuntu 26.04 no se verificaron.

## 6. Estado de las medidas de endurecimiento (actualizado)
| N.º | Medida | Estado |
|---|---|---|
| 1 y 2 | Marco y verificación (CIS) | Sustituidas por la decisión de la actualización (c) |
| 3 | Acceso remoto por SSH | Decidida ([actualización (o)](../2026-10-23o_endurecimiento-01-acceso-ssh/CAMBIOS.md)) |
| **4** | **Firewall** | **Decidida (esta actualización)**, salvo la salida y los rangos de Cloudflare |
| 5 | Actualizaciones automáticas y reinicio | Pendiente |
| 6 y 12 | Servicios bajo usuarios sin privilegios y `systemd` | Pendiente |
| 7 | HTTPS y cabeceras | Pendiente |
| 8 | Django (`check --deploy`, `SECRET_KEY`, límite de intentos, archivos subidos) | Pendiente |
| 9 | Revisión crítica con otra persona antes de datos reales | Pendiente |
| 11 | Gunicorn por socket Unix | Pendiente |
| 13 y 14 | Nginx (`server_tokens`, hosts desconocidos, límite de intentos) | Pendiente (el tope de subida ya está decidido) |
| 15 a 18 | PostgreSQL (red, acceso, registro, contraseñas) | Pendiente |

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
