# Actualización 2026-10-22 — Investigación del endurecimiento del servidor (RE-09)

**Fecha:** 2026-10-22
**Documentos afectados:** [README de la fase 6](../../fase-6-despliegue-operacion/README.md) y [DOC/README.md](../../README.md). No se edita ningún documento versionado: el DAS v0.11 sigue diciendo "sin investigar" y lo recogerá una versión nueva cuando el solicitante decida.
**Estado:** investigación; las recomendaciones son **propuestas del asistente**, ninguna está decidida ni aprobada.

## 1. Motivo
El DAS v0.11 (RE-09, secciones 5 y 11) y el README de la fase 6 dejaban el endurecimiento del servidor como "guías reconocidas aún sin investigar". El solicitante pidió investigarlo (22-oct-2026).

## 2. Registro de fuentes
Todas se consultaron el 22-oct-2026 con WebFetch (la página se convierte a texto y una herramienta responde a una pregunta concreta; no es lectura íntegra por el asistente) o con WebSearch (solo resultados de búsqueda).

| # | Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|---|
| F1 | CIS, [Ubuntu Linux benchmarks](https://www.cisecurity.org/benchmark/ubuntu_linux/) | Estándar de la industria | Página abierta; **no** se abrió el PDF del benchmark | Existe "Ubuntu Linux 26.04 LTS (1.0.0)" como benchmark y en CIS-CAT Pro; no figura en Build Kits ni Hardened Images. El PDF es gratis para uso no comercial; el uso comercial y CIS-CAT requieren membresía (la página no lo detalla del todo) | No se leyeron los controles. La licencia del PDF para uso comercial no está verificada |
| F2 | Canonical, [CIS compliance with Ubuntu LTS (USG)](https://ubuntu.com/security/certifications/docs/usg/cis) | Documentación del proveedor | Página abierta | Las herramientas de Canonical automatizan CIS solo para 24.04, 22.04, 20.04, 18.04 y 16.04 (perfil 1.0.0 en 24.04). **26.04 no está listada** "al momento de escribir" | Puede estar desactualizada; no se probó `usg` en una 26.04 |
| F3 | Canonical, [Install Ubuntu Security Guide](https://documentation.ubuntu.com/security/compliance/usg/install-usg/) | Documentación del proveedor | Página abierta | USG requiere Ubuntu Pro (existe la suscripción personal gratuita); comandos `pro attach`, `pro enable usg`, `apt install usg` | La página solo menciona 20.04. Límites y condiciones de la suscripción gratuita (5 máquinas, uso personal o comercial pequeño) vienen de un anuncio de 2022 visto solo en resultados de búsqueda; **sin verificar hoy** |
| F4 | Canonical, [Ubuntu 26.04 LTS release notes](https://documentation.ubuntu.com/release-notes/26.04/) y [ciclo de vida](https://ubuntu.com/about/release-cycle) | Documentación del proveedor | Solo resultados de búsqueda | 26.04 publicada el 23-abr-2026; mantenimiento estándar hasta mayo de 2031 (las notas dicen abril de 2031) | Dos fuentes oficiales difieren en el mes; no se abrieron las páginas |
| F5 | NIST, [SP 800-123 Guide to General Server Security](https://csrc.nist.gov/pubs/sp/800/123/final) | Estándar (NIST) | Página de catálogo abierta; **el PDF no se leyó** | Es el documento de referencia para asegurar servidores de red; publicación final de julio de 2008, sin revisión anunciada | Antigua (2008); no se leyó su contenido. Se cita como marco, no para controles concretos |
| F6 | DigitalOcean, [Cloud Firewalls](https://docs.digitalocean.com/products/networking/firewalls/details/features/) | Documentación del proveedor | Página abierta | Firewall de red con estado, sin costo adicional, deniega por defecto, se aplica por etiquetas, la regla de denegar gana. La página **no explica** la interacción con UFW ni IPv6. Una página de la comunidad (resultados de búsqueda) dice que son independientes y que hay que evitar conflictos | Interacción con UFW e IPv6 sin verificar en documentación oficial |
| F7 | DigitalOcean, [Add SSH keys](https://docs.digitalocean.com/products/droplets/how-to/add-ssh-keys/) | Documentación del proveedor | Página abierta | Recomienda llaves SSH sobre contraseñas; no habla de desactivar la contraseña | — |
| F8 | Canonical, [OpenSSH server](https://ubuntu.com/server/docs/how-to/security/openssh-server/) | Documentación del proveedor | Página abierta | Recomienda ed25519; `sshd -t` antes de reiniciar; 2FA U2F/TOTP además de llave. **No** trae sección de endurecimiento (PasswordAuthentication, PermitRootLogin no aparecen) | Los valores de `sshd_config` quedan sin fuente aquí; ver recomendación 3 |
| F9 | Canonical, [Automatic updates](https://ubuntu.com/server/docs/how-to/software/automatic-updates/) | Documentación del proveedor | Página abierta | `unattended-upgrades` viene instalado y corre a diario; por defecto solo aplica seguridad; reinicio automático desactivado; correo vacío; registros en `/var/log/unattended-upgrades/` | — |
| F10 | Canonical, [Firewall (UFW)](https://ubuntu.com/server/docs/how-to/security/firewalls/) | Documentación del proveedor | Página abierta | UFW está desactivado por defecto; comandos `ufw allow`, `ufw enable`, `ufw status verbose`, `ufw logging on`. **No** documenta políticas por defecto ni `ufw limit` | — |
| F11 | Django, [Deployment checklist 5.2](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/) | Documentación oficial | Página abierta | `check --deploy`; `SECRET_KEY` fuera del código; `DEBUG=False`; `ALLOWED_HOSTS` y rechazo de hosts desconocidos en el servidor web; HTTPS con redirección en el servidor web; cookies seguras; los subidos son no confiables y no se ejecutan; no usar `runserver` | No menciona HSTS |
| F12 | OWASP, [Django Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html) | Guía de experto reconocido | Página abierta | HSTS, nosniff, X-Frame-Options, `SECURE_SSL_REDIRECT`, `SECURE_PROXY_SSL_HEADER` solo tras un proxy confiable, limitación de intentos de acceso (django-axes o django-ratelimit), validadores de contraseña, cambiar la URL del admin (solo oscuridad) | No cubre cargas de archivos. CSP integrada solo desde Django 6.0 (el proyecto usa 5.2) |
| F13 | OWASP, [TLS Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html) | Guía de experto reconocido | Página abierta | TLS 1.3 por defecto y 1.2 por compatibilidad; desactivar TLS 1.0 y 1.1; sin compresión; registros CAA | No cubre OCSP stapling; la curva de Nginx citada incluye X25519MLKEM768 y exige un OpenSSL reciente (sin verificar) |
| F14 | Mozilla, [Server Side TLS](https://wiki.mozilla.org/Security/Server%20Side%20TLS) y generador | Guía reconocida | Solo resultados de búsqueda | Perfil "Intermediate" recomendado para uso general; el generador se archivó el 28-may-2026 (solo lectura) | No se abrió; la configuración de Nginx debe tomarse del generador vigente y verificarse |
| F15 | systemd, [systemd.exec](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html) | Documentación oficial | Leída en parte (100 000 de 244 377 caracteres) | `NoNewPrivileges`, `ProtectSystem=strict`, `ProtectHome`, `PrivateTmp`, `ReadWritePaths`, `CapabilityBoundingSet` | `RestrictAddressFamilies` y `systemd-analyze security` no se leyeron |

**No se pudo verificar:** el contenido de los controles del benchmark CIS 26.04 (PDF no abierto); el comportamiento de `usg` en 26.04; la interacción del Cloud Firewall con UFW e IPv6; guías de Nginx del proveedor (no se consultaron); guías de Gunicorn y de PostgreSQL (no se consultaron).

## 3. Hallazgos
- **E1.** Existe el benchmark CIS para Ubuntu 26.04 (1.0.0, F1), pero la herramienta de automatización de Canonical (USG) no lo lista (F2). Aplicarlo sería manual, con el PDF, o esperar a que USG lo soporte.
- **E2.** Ni la documentación de Ubuntu ni la de DigitalOcean que se leyeron dan los valores de `sshd_config` (F7, F8); esa parte de la recomendación se apoya en CIS (no leído) y es criterio del asistente.
- **E3.** Se conservan los dos firewalls del DAS (ADR-023) pero sin fuente que describa cómo interactúan (F6, F10).

## 4. Recomendaciones (propuestas del asistente; ninguna decidida)
Los valores concretos son de diseño y deben contrastarse con el PDF del benchmark CIS 26.04 antes de adoptarlos.

| N.º | Propuesta | Fundamento |
|---|---|---|
| 1 | **Marco:** usar el benchmark CIS Ubuntu 26.04 nivel 1 (servidor) como lista de controles, con NIST SP 800-123 como marco general y OWASP para la capa de aplicación | F1, F5, F12 |
| 2 | **Verificación:** descargar el PDF de CIS (gratis para uso no comercial) y revisar su licencia; probar `usg` en la WSL de la etapa A solo si Canonical añade 26.04; si no, aplicar los controles a mano y registrarlos | F1, F2, F3 |
| 3 | **Acceso remoto:** solo llave ed25519, sin contraseña y sin acceso directo de root, con un usuario administrador distinto del usuario de la aplicación; validar con `sshd -t` antes de reiniciar; segundo factor (TOTP o FIDO) como mejora | F7, F8; la parte "sin contraseña ni root" es criterio del asistente sin fuente leída |
| 4 | **Firewall:** Cloud Firewall por etiqueta con deny por defecto (entrada: 80, 443 y 22 solo desde la IP del solicitante) y UFW en el servidor como segunda capa, con las mismas reglas | F6, F10; DAS ADR-023. Pendiente de verificar la interacción e IPv6 |
| 5 | **Actualizaciones:** dejar `unattended-upgrades` activo (solo seguridad), configurar el correo del solicitante y decidir si se permite el reinicio automático en una hora fija (**decisión de negocio**: ventana de mantenimiento) | F9 |
| 6 | **Servicios:** Gunicorn y el proceso diario bajo usuarios sin privilegios con `NoNewPrivileges`, `ProtectSystem=strict`, `ProtectHome`, `PrivateTmp` y `ReadWritePaths` solo para documentos y registros | F15; ADR-024 y ADR-027 |
| 7 | **HTTPS y cabeceras:** redirección a HTTPS en Nginx, HSTS, `nosniff`, `X-Frame-Options`, cookies seguras, `SECURE_PROXY_SSL_HEADER` solo con Nginx por delante, TLS 1.2 y 1.3 con el perfil Intermediate del generador de Mozilla verificado al momento, registro CAA y Nginx que rechace hosts desconocidos | F11, F12, F13, F14 |
| 8 | **Django:** `check --deploy` en la integración continua, `SECRET_KEY` fuera del repositorio, limitación de intentos de acceso (django-axes o django-ratelimit; elegir una es decisión de diseño) y los archivos subidos fuera de la raíz pública y nunca ejecutables | F11, F12 |
| 9 | **Antes de datos reales:** pasar la lista de revisión crítica con otra persona (DP-23) y registrar el resultado | Plan de implementación, sección 3.3 |

## 5. Decisiones y preguntas
| Pregunta | Respuesta | Decisión |
|---|---|---|
| ¿Qué guías se usan para endurecer el servidor? | Pendiente | Ninguna: solo propuesta (N.º 1) |
| ¿Se permite reinicio automático y a qué hora? | Pendiente | Ninguna |

## 6. Pendientes
- Descargar y leer el benchmark CIS 26.04 y registrar qué controles se adoptan.
- Investigar Nginx, Gunicorn y PostgreSQL (guías de endurecimiento propias) y la interacción Cloud Firewall con UFW e IPv6.
- Verificar hoy las condiciones de Ubuntu Pro gratuito.
- Incorporar lo que se decida al DAS (versión nueva) y a un procedimiento de la fase 6.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
