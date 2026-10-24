# Actualización 2026-10-24 (j) — Despliegue de la etapa A en WSL

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/despliegue/`](../../../src/despliegue/desplegar.sh), [`src/respaldo/`](../../../src/respaldo/README.md), [`src/sga/settings.py`](../../../src/sga/settings.py), [`src/nucleo/middleware.py`](../../../src/nucleo/middleware.py), [`src/requirements.txt`](../../../src/requirements.txt), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** plan, sección 5.1 (etapa A: WSL 2 con Ubuntu 26.04, sin contenedores, con Nginx, Gunicorn, PostgreSQL 18 con roles y `peer`, temporizadores de systemd y respaldos a una carpeta local) y criterio de salida de la E0; DAS v0.15, ADR-023, ADR-027 y ADR-032 (decisiones 4, 5, 6, 11, 12, 13, 16 y 17); instrucción del solicitante: «sí, ya instalé WSL, sigue con el despliegue», y autorización expresa de instalar paquetes del sistema dentro de la distribución (24-oct-2026)
**Estado:** desplegado y verificado en la máquina del solicitante; no aprobado

## 1. El entorno (comprobado)
Distribución `Ubuntu` (no `Ubuntu-26.04`: así quedó instalada), Ubuntu 26.04.1 LTS, WSL 2.6.2.0, systemd activo, 12 procesadores, 7,8 GiB de memoria; Python 3.14.4, PostgreSQL 18.6, Nginx 1.28.3 y `age` 1.2.1 de los paquetes de Ubuntu. Antes de la autorización solo existía `docker-desktop`.

## 2. Qué se escribió
| Archivo | Contenido |
|---|---|
| `despliegue/desplegar.sh` | **Un solo comando**, como root dentro de la distribución, idempotente: paquetes, usuarios del sistema, PostgreSQL por socket con `peer`, roles y base, código y entorno virtual en `/opt/sga`, secretos en `/etc/sga`, migraciones y privilegios con el rol dueño, certificado autofirmado, Gunicorn con socket de systemd, Nginx, y el respaldo diario si se le da la clave pública; termina con una comprobación HTTP/HTTPS |
| `despliegue/postgresql/` | `sga.conf` (sin TCP, socket 0770 con el grupo `sga_bd`, registro mínimo) y `pg_hba.conf` (solo `local` + `peer`) |
| `despliegue/systemd/` | Socket y servicio de Gunicorn endurecidos |
| `despliegue/nginx/` | Sitio con HTTPS autofirmado, redirección, 444 para un `Host` desconocido, zonas de límite de solicitudes, registro propio, cabeceras sustituidas |
| `despliegue/verificar.sh`, `verificar_http.py`, `verificar_respaldo.sh`, `probar.sh` | Verificaciones repetibles (ver sección 4) |
| `nucleo/middleware.py` | `PoliticaDeContenido`: CSP de la decisión 16 como `Content-Security-Policy-Report-Only` |
| `nucleo/tests_cabeceras.py` | 4 pruebas: la política en toda respuesta, su contenido, las cabeceras de Django y plantillas sin código en línea |
| `requirements.txt` | `gunicorn==26.2.0` (publicada el 2026-08-24) |
| `sga/settings.py` | La IP de origen sale de `X-Forwarded-For` (ver sección 5) |

## 3. Hallazgos al desplegar (errores míos o supuestos del DAS que no se cumplían)
1. **PostgreSQL no arranca si el grupo del socket no incluye a `postgres`.** El ADR-032 d12 dice que el grupo contiene «solo los usuarios del sistema que usan la base»; el servidor `postgres` también debe ser miembro («could not set group of file ... Operation not permitted»). Se agregó. Es una precisión a la decisión, no un cambio.
2. **`pg_dumpall --globals-only` conecta a `template1`** aunque se le pase `--dbname`, y el rol de respaldos no tiene entrada en `pg_hba.conf` para ella. Se usa `--database=sga`. Con la autenticación `trust` de las pruebas de Windows no se veía; solo apareció con `peer` real.
3. **Ubuntu 26.04 trae `server_tokens build;` en `nginx.conf`**: no se puede repetir la directiva en `conf.d`; `server_tokens off;` va en cada bloque `server` y se verificó que la cabecera sea `nginx` sin versión.
4. **El límite de Nginx para `/entrar/` (6 por minuto, ráfaga de 6) frena un recorrido de prueba completo** (registrar el segundo factor son más de seis peticiones seguidas). La verificación pone `limit_req_dry_run on` mientras recorre el sistema y lo restaura, y prueba aparte que una ráfaga de 15 recibe 429. El despliegue comprueba `/` y no `/entrar/` por la misma razón. Un uso normal (4 peticiones por inicio de sesión) cabe en la ráfaga.
5. **`forwarded_allow_ips` por defecto basta**: Django detecta HTTPS detrás de Nginx sin ponerlo en `'*'` (pendiente declarado en el ADR-032 d13).
6. **El `README` de la actualización 2026-10-24e decía `X-Real-IP`**; el DAS decide `X-Forwarded-For` sustituido (d13). Se cambió el código y esta actualización lo corrige; la 2026-10-24e no se edita.
7. Comandos con `env $(xargs < entorno)` fallaban por las líneas de comentario del archivo: se filtran.
8. Mi primer intento de ejecutar scripts por tubería desde PowerShell insertaba una marca de orden de bytes; se ejecutan desde archivo.

## 4. Verificación (hecha de verdad en WSL)
- **`verificar.sh`: sin fallos.** PostgreSQL sin puerto TCP, socket 0770 `sga_bd`, `pg_hba.conf` solo `local`+`peer`; cada rol entra solo como sí mismo y un usuario ajeno no entra; la aplicación no modifica la auditoría ni crea tablas; el respaldo lee y no escribe; secretos 0640 `root:sga_app` que otros usuarios no leen; socket de Gunicorn `sga_app:www-data` 0660.
- **Recorrido real por HTTPS (`verificar_http.py`): sin fallos.** Cuenta de prueba, token, registro del segundo factor con 10 códigos, sesión con cookies `Secure` y `HttpOnly`, pantalla de auditoría, cierre de sesión; **la IP falsificada por el cliente no llega a la auditoría** (guarda 127.0.0.1); Host desconocido sin respuesta; HTTP→HTTPS 301; el registro de Nginx **no contiene la cadena de consulta** de una búsqueda de prueba; ráfaga de 15 peticiones → 429. La cuenta de prueba se borra al terminar.
- **`verificar_respaldo.sh`: sin fallos.** Con un par de claves **solo de prueba** generado en la distribución: el servicio `sga-respaldo.service` real hace el respaldo con usuario `sga_respaldos`, archivos 0600 sin nada en claro, y la **restauración completa** con la clave privada devuelve la base y el documento; sin clave pública el servicio falla y no cambia la marca. `systemd-analyze calendar` confirma 05:00 de Costa Rica = 11:00 UTC.
- **`probar.sh`: 157 pruebas pasan en Python 3.14.4, PostgreSQL 18.6 y `age`/`pg_dump` reales, 0 omitidas.** `makemigrations --check` sin cambios y `check --deploy` con solo el aviso de HSTS. Esto responde la duda de compatibilidad con 3.14: las dependencias fijadas funcionan.
- `systemd-analyze security`: Gunicorn **1.5 OK** y respaldo **3.0 OK** tras agregar el endurecimiento adicional (antes 5.5 y 7.7); ambos siguen funcionando con él, incluido `MemoryDenyWriteExecute`.
- `verificar_coherencia.ps1` sin problemas.

## 5. Propuestas del asistente (sin aprobar)
- Nombres de usuario del sistema y de rol iguales (`sga_dueno`, `sga_app`, `sga_respaldos`), grupo `sga_bd`, rutas `/opt/sga`, `/etc/sga`, `/var/lib/sga`.
- Endurecimiento adicional de systemd (`ProtectKernel*`, `RestrictNamespaces`, `MemoryDenyWriteExecute`, `SystemCallFilter=@system-service`, `RestrictAddressFamilies`, entre otros): el ADR lista un conjunto menor. Gunicorn permite también `AF_INET`/`AF_INET6` porque la E4 enviará correo.
- `PrivateUsers` **no** se usa en las unidades: cambiaría el identificador de usuario que PostgreSQL lee para `peer` (supuesto no probado).
- El certificado autofirmado (EC P-256, 825 días) y el nombre `localhost` como sitio.
- Las pruebas del sistema corren como `postgres`, el único con `CREATE DATABASE` y `CREATE ROLE`.
- El despliegue y la verificación **borran los datos de prueba** con `TRUNCATE` como `postgres`, porque el rol de la aplicación no puede borrar la auditoría ni la cuenta (R12).

## 6. Qué no se probó
- La primera corrida en GitHub Actions (siguen pendientes las dos del flujo; no hay `gh` ni acceso a las Actions desde aquí).
- El tiempo de restauración con datos reales; el rendimiento (RNF-08) y todo lo que depende del Droplet, de Spaces, de Resend, del dominio y de Certbot (E6).
- La red de WSL con otro equipo y el reinicio de la máquina (que los servicios vuelvan a levantar solos; systemd los tiene habilitados, no se reinició para comprobarlo).
- El `DELETE` de los códigos de recuperación, los decimales en colones y la pantalla de la organización siguen sin decidir.

## 7. Efecto sobre la E0
Quedan resueltas las secciones E, F y G de la lista de tareas y la repetición con Python 3.14. **Siguen sin marcarse los 8 CA** porque la regla es una corrida verde en la integración continua; localmente las pruebas de todos pasan en 3.14. Quedan por hacer de la E0: la primera corrida verde en GitHub y las tareas pendientes de las secciones B, C e I (pantalla de códigos nuevos, prueba de concurrencia, alertas por aviso fallido, datos personales en registros).

## 8. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
