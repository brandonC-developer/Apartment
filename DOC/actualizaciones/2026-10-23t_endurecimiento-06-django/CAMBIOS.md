# Actualización 2026-10-23 (t) — Endurecimiento, medida 7: Django (propuesta 8)

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en una versión nueva del DAS y en el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** propuesta 8 de la [actualización 2026-10-22](../2026-10-22_investigacion-endurecimiento-servidor/CAMBIOS.md); sigue a la [medida 6 (HTTPS y cabeceras)](../2026-10-23s_endurecimiento-05-https-cabeceras/CAMBIOS.md)
**Estado:** decisión registrada; documentos sin cambiar; no aprobado

## 1. Qué de la propuesta 8 ya estaba decidido
| Parte | Estado | Dónde |
|---|---|---|
| `manage.py check --deploy` en la integración continua | Decidido (20-oct-2026) | DAS, ADR-025 |
| Archivos subidos fuera de la raíz pública, con nombre aleatorio y nunca ejecutables | Decidido (20-oct-2026) | DAS, ADR-003 |
| Límite de intentos de acceso | Ya especificado en la aplicación | ERS RF-27, CA-68; modelo `ADMINISTRADOR` (`fallos_consecutivos`, `espera_hasta`) |
| `SECRET_KEY` fuera del repositorio | Pendiente: se decide en esta actualización | — |

## 2. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Dónde se guardan los secretos de la aplicación? | "Archivo en /etc/sga, 0640 root y grupo de la app" (recomendada por el asistente) | Archivo de secretos en `/etc/sga/` (ruta propuesta), fuera del repositorio y de la raíz web, con permisos `0640`, dueño `root` y grupo del usuario de la aplicación; Django lo lee al arrancar. Un secreto por clave distinta (`SECRET_KEY`, clave de Resend de la aplicación, clave propia del servidor para el correo de errores). La clave con que se cifran los respaldos **no** vive solo en el servidor |
| 2 | ¿Cuándo se rotan los secretos? | "Al sospechar exposición y una vez al año" (recomendada) | Rotación inmediata si hay sospecha de exposición, y una vez al año para la `SECRET_KEY` y las claves de API. La `SECRET_KEY` usa `SECRET_KEY_FALLBACKS` durante la transición y se quita la clave vieja en cuanto sea posible. Procedimiento escrito en la fase 6 |
| 3 | ¿Se añade `django-axes` o `django-ratelimit`? | "No: RF-27 en la app + limit_req en Nginx" (recomendada) | No se añade ninguna biblioteca. Se implementa el límite de RF-27/CA-68 y el límite por IP se resuelve en Nginx (medida 14, aún sin decidir) |

## 3. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Django, lista de despliegue 5.2: https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/ | Documentación oficial | Leída por resumen (WebFetch, 23-oct-2026) | `SECRET_KEY` aleatoria, fuera del código y del control de versiones, desde variable de entorno o archivo; `SECRET_KEY_FALLBACKS` para rotar y quitar las viejas pronto; proteger igual las credenciales de base de datos | No detalla qué se invalida al cambiar la clave (lo de sesiones y datos firmados viene de la documentación general de Django, no verificado en esa página); las claves de API no se mencionan expresamente |
| OWASP, Secrets Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html | Guía de experto reconocido | Leída por resumen (23-oct-2026) | Rotar con regularidad; revocar de inmediato lo expuesto; las credenciales de usuario se rotan solo ante sospecha; variables de entorno no recomendadas salvo que no haya otra opción; no guardar las claves junto a los secretos que cifran | Está escrita pensando en entornos de nube y orquestadores; no fija un plazo de rotación |
| OWASP, Django Security Cheat Sheet | Guía de experto reconocido | Leída en la investigación del 22-oct-2026 | Limitar intentos de acceso con `django-axes` o `django-ratelimit` | No dice que una biblioteca sea obligatoria |
| Nginx, ngx_http_limit_req_module | Documentación oficial | Leída en la investigación del 22-oct-2026 | `limit_req_zone` y `limit_req` limitan por clave (por ejemplo, la IP) | — |
| systemd.exec (`EnvironmentFile=`, `LoadCredential=`) | Documentación oficial | **No se pudo leer** esa parte (la página se corta a los 100 000 caracteres, en dos fuentes distintas) | — | Por eso no se propone `EnvironmentFile` ni credenciales de systemd |

## 4. Lo que propone el asistente y el solicitante no decidió
- La ruta `/etc/sga/` y los permisos exactos; el calendario anual; que un año sea el plazo.
- **Hallazgo del asistente, sin decidir:** el contador de RF-27 es **de la cuenta**, y hay una sola cuenta; quien falle cinco veces deja la cuenta en espera de hasta una hora aunque no sea el administrador. Se mitiga con el tope de una hora y el restablecimiento por correo, y con el límite por IP de Nginx. Cambiar a un contador por IP y cuenta sería cambiar una regla de negocio (RF-27) y no se hizo.
- **Pendiente explícito:** cómo se cifran los respaldos y dónde vive su clave (RNF-09). No se diseñó.

## 5. Qué no se hizo
- No se aplicó nada: no hay servidor.
- No se verificó qué invalida un cambio de `SECRET_KEY` ni cómo se comporta `SECRET_KEY_FALLBACKS`.
- No se leyó la documentación de systemd sobre `EnvironmentFile` y credenciales.
- No se diseñó el procedimiento de rotación ni el calendario en la fase 6.

## 6. Estado de las medidas de endurecimiento (actualizado)
| N.º | Medida | Estado |
|---|---|---|
| 1 y 2 | Marco y verificación (CIS) | Sustituidas por la decisión de la actualización (c) |
| 3 | Acceso remoto por SSH | Decidida ([actualización (o)](../2026-10-23o_endurecimiento-01-acceso-ssh/CAMBIOS.md)) |
| 4 | Firewall | Decidida ([actualización (p)](../2026-10-23p_endurecimiento-02-firewall/CAMBIOS.md)) |
| 5 | Actualizaciones automáticas y reinicio | Decidida ([actualización (q)](../2026-10-23q_endurecimiento-03-actualizaciones/CAMBIOS.md)), con la corrección de puertos |
| 6 y 12 | Servicios bajo usuarios sin privilegios y `systemd` | Decididas ([actualización (r)](../2026-10-23r_endurecimiento-04-servicios-systemd/CAMBIOS.md)) |
| 7 | HTTPS y cabeceras | Decidida ([actualización (s)](../2026-10-23s_endurecimiento-05-https-cabeceras/CAMBIOS.md)), salvo cifrados, CAA y CSP |
| **8** | **Django** | **Decidida (esta actualización)**; `check --deploy` y los archivos subidos ya estaban decididos |
| 9 | Revisión crítica con otra persona antes de datos reales | Pendiente |
| 11 | Gunicorn por socket Unix | Pendiente |
| 13 y 14 | Nginx (`server_tokens`, hosts desconocidos, límite de intentos) | Pendiente (el tope de subida y el rechazo de hosts desconocidos ya están decididos) |
| 15 a 18 | PostgreSQL (red, acceso, registro, contraseñas) | Pendiente |

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
