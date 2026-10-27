# Tareas de implementación

**Identificador:** TAR-SGA-001
**Estado:** lista de tareas viva; no es un documento versionado ni aprobado
**Creada:** 24 de octubre de 2026 (actualización [2026-10-24c](../actualizaciones/2026-10-24c_lista-de-tareas-implementacion/CAMBIOS.md))
**Plan:** [Plan de implementación v0.1](PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) · **Registro de avance:** [AVANCE_IMPLEMENTACION.md](AVANCE_IMPLEMENTACION.md)

## Cómo se usa
- **Cada tarea sale de un documento del proyecto** y cita su origen (RF, RNF, CA, ADR, sección del plan). Las listas de requisitos y de criterios de aceptación se generaron del texto de la ERS v1.16 y de la tabla de entregas del plan v0.1, no de memoria. **No se inventan tareas durante la implementación:** si hace falta una que no está aquí, se agrega marcada *Propuesta* en la sección «Tareas agregadas» de la entrega y se pregunta al solicitante antes de hacerla.
- **Marcas:** `[ ]` pendiente, `[~]` parcial (se explica qué falta), `[x]` hecha, con fecha y evidencia (commit o prueba). Una tarea de CA solo se marca `[x]` cuando su prueba pasa en la integración continua con PostgreSQL 18 (condición 1 de terminado), no cuando el código existe.
- **Una entrega a la vez** (plan, sección 3.2). Solo la E0 está autorizada para implementarse (CLAUDE.md); las demás requieren la autorización expresa del solicitante.
- Los **RN** (reglas de negocio) no se listan aparte: se cumplen dentro de los RF y CA que los citan.
- **(L)** marca los CA cuyo resultado esperado depende de una obligación legal sin validar por abogado (EPP, sección 5).
- Cuando se marque algo aquí, se agrega la línea correspondiente en el historial de [AVANCE_IMPLEMENTACION.md](AVANCE_IMPLEMENTACION.md) si cambia el estado de una entrega.

## Condiciones comunes de terminado (se repiten en cada entrega)
Plan, sección 3.1. Una entrega no se da por terminada si falta alguna.


1. Pruebas de los CA asignados en la integración continua con PostgreSQL 18; ninguna Alta sin escribir (EPP, sección 11)
2. Integración continua en verde: pruebas, `check --deploy` y migraciones desde cero (ADR-025)
3. `verificar_coherencia.ps1` sin problemas
4. Tablas y secuencias nuevas en el archivo de privilegios, con su prueba (ADR-027, ADR-031)
5. Código sin cubrir de los módulos críticos revisado, sin umbral numérico (EPP, sección 9)
6. Desplegada en la etapa A (WSL 2 con Ubuntu-26.04) con datos ficticios y criterio de salida propio cumplido
7. Ningún dato personal ni secreto en los registros ni en la auditoría (RF-28, RNF-06, R14)
8. `CAMBIOS.md` de la entrega y trazabilidad (RF, CA, ADR) al día
9. Ningún defecto conocido de prioridad Alta abierto

---

## E0 — Esqueleto
**Aplicaciones:** nucleo, cuentas · **Estado:** en curso desde 2026-10-23 · **Criterio de salida:** Despliegue repetible con un comando en el entorno local; inicio de sesión con segundo factor; una restauración completa probada desde el respaldo local; pruebas de las restricciones de R12. La restauración desde Spaces y el HTTPS real se prueban en la etapa B

### A. Proyecto Django y configuración (plan E0; ADR-022, ADR-030)
- [x] Proyecto Django 5.2 con las aplicaciones `nucleo` y `cuentas` en `src/` (2026-10-23, c849f0b)
- [x] Secretos fuera del repositorio, leídos de variable de entorno o de `/etc/sga/` (ADR-032 d6; RNF-14) (c849f0b)
- [x] Hash Argon2id únicamente y contraseña de mínimo 15 caracteres (ADR-019; RF-27) (c849f0b)
- [x] Cookies seguras, HTTPS forzado y `SECURE_PROXY_SSL_HEADER` cuando no es depuración; HSTS en 0 hasta la etapa B (ADR-032 d5, d13) (c849f0b)
- [x] Sin `django.contrib.admin` (decisión del asistente, sin aprobar) (c849f0b)
- [x] Versiones fijadas en `requirements.txt` y probadas con Python 3.14.4 en WSL: las cinco dependencias más Gunicorn funcionan sin cambiar ninguna (actualización 2026-10-24j)
- [x] `CONN_MAX_AGE = 0`, sin pool (ADR-029): ya estaba y ahora tiene su prueba (2026-10-24, actualización 2026-10-24g)
- [x] Identificadores `BigAutoField` en todos los modelos del proyecto, con una prueba que lo exige para `nucleo` y `cuentas` (ADR-028; actualización 2026-10-24l)
- [x] Carpeta de documentos privados `RAIZ_DOCUMENTOS` (`/var/lib/sga/documentos`) fuera del código y de cualquier raíz web, sin `MEDIA_ROOT` ni URL pública, no servida por Nginx, con permisos de la aplicación y del respaldo; pruebas que lo exigen (RNF-03, RNF-14). **La vista que sirve los archivos con sesión y su auditoría son de la E1**

### B. Cuenta única y autenticación (RF-26, RF-27, RN-25, RNF-01, RNF-02; CA-13, CA-48, CA-68, CA-69, CA-70)
- [x] Modelo `Administrador` sobre `AbstractBaseUser`, sin permisos de Django, con una sola cuenta por restricción de tabla (2026-10-23, 34fb5e9; actualizaciones zz y zzc)
- [x] Secreto del segundo factor cifrado con Fernet/MultiFernet, clave en `/etc/sga/clave_cifrado` (34fb5e9; zzb)
- [x] TOTP con pyotp: 6 dígitos, intervalo de 30 s, tolerancia de ±1 intervalo, sin reutilizar un código aceptado (34fb5e9; CA-69)
- [x] Límite de intentos fallidos compartido por contraseña, TOTP y códigos de recuperación: 5 fallos, espera de 1 min que se duplica hasta 1 h, sin bloqueo permanente, el TOTP correcto reinicia el contador (34fb5e9; CA-68)
- [x] 10 códigos de recuperación de un solo uso, **guardados con Argon2id y sal propia por código** (NIST SP 800-63B; decisión del solicitante del 24-oct-2026, actualización 2026-10-24o); emitir nuevos exige la contraseña y **borra** los anteriores (`DELETE` solo en esa tabla, excepción decidida al ADR-027) (34fb5e9 y 3d2c230, corregido en la actualización 2026-10-24o; CA-69)
- [x] Vista de inicio de sesión en dos pasos: la contraseña sola no inicia sesión (2026-10-24, 1ee8ab6; RF-26, RNF-01)
- [x] Sesión con cierre a las 24 h y por inactividad de 1 h (1ee8ab6; CA-48)
- [x] Comandos de servidor `crear_administrador` y `rescatar_segundo_factor` (2026-10-24, 26e7895; CA-70)
- [x] Registro del segundo factor en el primer ingreso y entrega única de los 10 códigos (2026-10-24, a097789; CA-70)
- [x] Token de registro del segundo factor (un solo uso, 24 h, solo su hash) que imprimen `crear_administrador` y `rescatar_segundo_factor`; sin él, la contraseña sola no permite registrar un segundo factor (2026-10-24, actualización 2026-10-24d; propuesta del asistente derivada de la revisión de código)
- [x] Pantalla `/cuenta/codigos/` para emitir 10 códigos de recuperación nuevos desde la sesión: exige la contraseña actual con el mismo contador de intentos, invalida los anteriores, no se guarda en caché, los muestra una sola vez y deja el aviso (`codigos_emitidos` en la auditoría y alerta en la pantalla de inicio) (CA-69; el correo llega en la E4)
- [x] Todas las vistas exigen sesión salvo las del inicio de sesión: una prueba recorre **todas** las rutas del proyecto y falla si una vista nueva responde sin sesión y no está en la lista pública (CA-13, RNF-02)
- [x] Aviso al quinto fallo seguido: evento `cinco_fallos_seguidos` en la auditoría y alerta en la pantalla de inicio con los avisos desde el inicio de sesión anterior (CA-68; HI-01, HI-05); el correo llega en la E4
- [x] Aviso del rescate por el servidor: constancia `segundo_factor_rescatado` en la auditoría, alerta en la web y aviso impreso por el comando (CA-70; HI-01); el correo a las dos direcciones llega en la E4
- [ ] Alerta persistente en cada inicio de sesión cuando un aviso de seguridad queda en *fallido* (RF-27, ADR-026) — verificable plenamente en la E4
- [x] Pruebas de concurrencia con conexiones reales en paralelo: 8 fallos simultáneos cuentan exactamente 5 con un solo aviso, y un código TOTP o de recuperación enviado a la vez se acepta una sola vez. **Límite: sin el bloqueo de fila fallan con frecuencia, no siempre (es una carrera)**

### C. Auditoría base (RF-28, RNF-06; CA-53, CA-71)
- [x] Modelo `nucleo.Auditoria` de solo inserción y servicio `registrar`: actor, fecha y hora, operación, entidad, campos modificados y valores de campos **no personales**; de los personales y los secretos solo el nombre (RF-28; CA-53) (2026-10-24, actualización 2026-10-24e; la lista de campos personales es propuesta del asistente a partir de RF-28)
- [~] Eventos de autenticación con IP y sin secretos: `inicio_sesion`, `inicio_sesion_fallido`, `cierre_sesion`, `cuenta_creada`, `codigo_recuperacion_usado`, `codigos_emitidos`, `segundo_factor_registrado`, `segundo_factor_rescatado` y `cinco_fallos_seguidos` (RF-28; CA-71). **Faltan** los de cambio y restablecimiento de contraseña y de cambio de una dirección de correo (E4) y el de emisión de códigos nuevos desde la sesión (pantalla pendiente)
- [x] Tipo de actor *proceso* con su restricción R19 (actor «sistema» y ejecución obligatoria; el administrador no lleva ejecución); `ejecucion_id` sin clave foránea hasta la E2 (RF-28, HT-06)
- [x] Pantalla `/auditoria/` de solo lectura con filtros por fecha, tipo de evento, entidad y actor, de 50 en 50; consultarla no genera registro (CA-71)
- [x] Guardas en el modelo (error claro al editar o borrar) y bloqueo de `update()` y `delete()` masivos; sin sitio de administración (ADR-027); la defensa real del rol de PostgreSQL está en la sección E (actualización 2026-10-24g)
- [x] La auditoría no se borra automáticamente: ningún código la borra (RF-28; plazo de conservación en DP-18)
- [x] Dirección IP de origen detrás de Nginx: se lee `X-Forwarded-For`, que Nginx **sustituye** por `$remote_addr` (ADR-032 d13); comprobado en WSL enviando una IP falsificada: la auditoría guarda la real (127.0.0.1)

### D. Organización y configuración regional (RF-33, RNF-12, RNF-17; CA-18)
- [x] Entidad `nucleo.Organizacion` de una sola fila (restricción de la tabla y migración de datos) con moneda CRC y zona `America/Costa_Rica` como predeterminadas, zona validada contra IANA, hora del proceso diario 07:00 y la identidad del responsable (RF-33). **Se edita con el comando `configurar_organizacion` (decisión del solicitante, 24-oct-2026), con auditoría; las pantallas web llegan solo con el RF que las pida** (RF-21 en la E4). Solo los atributos que usa la E0
- [x] Formato propio (`nucleo/formato.py` y filtros de plantilla): fechas dd/mm/aaaa, números con punto de miles y coma decimal, símbolo delante, porcentajes con coma; lectura estricta; todo con `Decimal` (RNF-12). **Colones sin decimales si el importe es entero y con dos si tiene céntimos; dólares siempre con dos** (decisión del solicitante, 24-oct-2026)
- [x] Marcas temporales en UTC y aritmética decimal exacta (`float` rechazado en el formato) (RNF-17); `USE_TZ = True`; la zona de la organización se activa en cada petición (`ZonaHorariaDeLaOrganizacion`)
- [~] Los registros históricos no cambian al modificar la configuración regional: probado con la auditoría (instante intacto, solo cambia la presentación) (CA-18); la parte de contratos en USD se completa en la E2

### E. Base de datos: roles, privilegios y esquema (ADR-027, ADR-029, ADR-031; condición 4)
- [x] Tres roles de PostgreSQL con `LOGIN`, sin contraseña, sin superusuario: dueño, aplicación y respaldos (`db/roles.sql`), con autenticación `peer` real en WSL: cada rol entra solo desde el usuario del sistema del mismo nombre (ADR-027, ADR-032 d12; actualización 2026-10-24j)
- [x] Archivo de privilegios idempotente `sga/privilegios.py` + `manage.py aplicar_privilegios`, que el rol dueño ejecuta tras cada `migrate`; parte de cero (`REVOKE ALL`) y concede solo lo que consta (ADR-031 d3; el formato es propuesta del asistente)
- [x] Prueba que compara las tablas reales con el archivo y exige una entrada por tabla (ADR-031 d3)
- [x] Prueba de que el rol de la aplicación es rechazado en `UPDATE`, `DELETE` y `TRUNCATE` sobre la auditoría, incluso con SQL directo (ADR-027); queda por repetir en las tablas de movimientos, ajustes y accesos cuando existan (E1 y E3)
- [x] Extensión `btree_gist` creada por una migración de `nucleo` (ADR-031 d1; la usa la E2); la crea el rol dueño sin ser superusuario, comprobado en WSL
- [x] `CONNECT` y `TEMPORARY` revocados a `PUBLIC` y concedidos a los tres roles; `listen_addresses = ''` (sin puerto TCP), socket 0770 con el grupo `sga_bd` y `pg_hba.conf` con solo registros `local`+`peer`, comprobados en WSL

### F. Despliegue en la etapa A: WSL 2 con Ubuntu-26.04, sin contenedores (plan, sección 5.1; ADR-023)
- [x] Distribución instalada: **se llama `Ubuntu`** (no `Ubuntu-26.04`), es Ubuntu 26.04.1 LTS con systemd activo, Python 3.14.4, PostgreSQL 18.6 y Nginx 1.28.3 (2026-10-24)
- [x] Python 3.14.4 del sistema y entorno virtual en `/opt/sga/venv`; **las cinco dependencias fijadas más Gunicorn 26.2.0 se instalan y funcionan con 3.14** (157 pruebas pasan)
- [x] PostgreSQL 18.6 con los roles y `peer` dentro de WSL, solo por el socket Unix
- [x] Gunicorn con `gunicorn.socket` de systemd, 3 workers `sync`, `timeout` 30 s, `max_requests` 1 000 con jitter 100; **`forwarded_allow_ips` por defecto basta**: Django detecta HTTPS detrás de Nginx (ADR-032 d13, pendiente declarado)
- [x] Nginx como proxy inverso con HTTPS autofirmado (EC P-256, 825 días), TLS 1.3 y 1.2, redirección 80→443, `Host` desconocido sin respuesta (444), cabeceras `X-Forwarded-*` sustituidas, `server_tokens off` por servidor (ADR-032 d5, d13)
- [x] Usuarios de sistema estáticos (`sga_dueno`, `sga_app`, `sga_respaldos`) y unidades endurecidas; `systemd-analyze security`: Gunicorn **1.5 OK**, respaldo **3.0 OK** (antes 5.5 y 7.7) (ADR-032 d4)
- [x] Registros de Nginx con formato propio sin cadena de consulta, Gunicorn sin registro de acceso (errores a journald) y rotación diaria de 14 días (la trae el `logrotate` de Ubuntu, verificado) (ADR-032 d17)
- [x] Despliegue repetible con un solo comando, idempotente: `desplegar.sh` (se ejecutó más de seis veces seguidas); `verificar.sh`, `verificar_http.py`, `verificar_respaldo.sh` y `probar.sh` lo comprueban (criterio de salida)
- [x] Límite de solicitudes en Nginx: zona de autenticación (6 por minuto, ráfaga de 6) y zona general (10 por segundo, ráfaga de 30), respuesta 429 (ADR-032 d11); probado con una ráfaga real. `limit_req_dry_run` queda disponible para las pruebas de la etapa B
- [x] Política de contenido (CSP) fija y estricta en modo informe, `nosniff`, `X-Frame-Options` y `Referrer-Policy` (ADR-032 d5 y d16); sin scripts ni estilos en línea, con una prueba que lo exige
- [ ] Pasar la CSP de informe a obligatoria cuando no haya violaciones, y activar HSTS por etapas (ADR-032 d5, d16): etapa B
- [ ] Cifrados de TLS 1.2 fijados con el generador vigente y escáner externo (ADR-032 d16): etapa B
- [x] `manage.py check --deploy` sin avisos distintos de HSTS, también en WSL con Python 3.14 (ADR-025)

### G. Respaldo cifrado y restauración (ADR-024, ADR-032 d9; RNF-09)
- [x] Herramienta de cifrado: `age` a clave pública, como fija el ADR-032 d9; se usó la versión 1.3.2 (2026-08-29) en las pruebas locales, descargada de las publicaciones oficiales de FiloSottile/age sin verificar su prueba de transparencia (`.proof`)
- [x] Respaldo diario `respaldo/respaldar.sh`: `pg_dump` en formato personalizado, `pg_dumpall --globals-only --no-role-passwords` y la carpeta de documentos, cada uno cifrado por tubería (nada en claro en el disco) a una carpeta local, con sumas y retención de 35 días (ADR-024, ADR-032 d9; actualización 2026-10-24i)
- [x] Restauración `respaldo/restaurar.sh` probada en WSL con `peer` y con las unidades de systemd: respaldo por el servicio real y restauración completa de la base y de los documentos con la clave privada (criterio de salida; RNF-09). **Pendiente: medir el tiempo frente al RTO de 24 h con datos reales (E6)**
- [x] Se restaura con la clave correcta y falla con otra, sin dejar una base a medias (EPP, sección 7)
- [x] Guía de las claves en `respaldo/README.md`: la `age` se genera fuera del servidor y se guarda en dos lugares fuera de línea. **Clave Fernet: sin copia; si se pierde, los códigos de recuperación siguen sirviendo y `rescatar_segundo_factor` registra el autenticador de nuevo** (decisión del solicitante, 24-oct-2026); un secreto ilegible ya es un fallo con aviso y no un error 500
- [x] Marca `ultimo_respaldo_correcto` escrita solo al terminar todo, de forma atómica; un fallo en cualquier parte no la toca (ADR-032 d15; la subida a Spaces antes de la marca y la vigilancia, RF-53, llegan en la E6 y la E4)

### H. Integración continua (ADR-025, ADR-032 d10)
- [x] Flujo de GitHub Actions `.github/workflows/integracion-continua.yml` (PostgreSQL 18, Python 3.14): migraciones al día, pruebas desde cero, `check --deploy` y despliegue de la base con roles y privilegios (ADR-025). **Todas las corridas en verde, informado por el solicitante el 2026-10-24**
- [x] `pip-audit` en un trabajo propio del flujo, con ejecución semanal además de cada cambio (ADR-032 d10): en verde, informado por el solicitante el 2026-10-24
- [x] Todo repetido en Python 3.14.4 en WSL y en la integración continua: 196 pruebas pasan, 0 omitidas en WSL; corridas de GitHub en verde (informado por el solicitante)

### I. Pruebas de seguridad de la aplicación de la E0 (EPP, sección 7)
- [x] Contraseña de mínimo 15 caracteres sin reglas de composición y Argon2id (`nucleo/tests.py`, `cuentas/tests.py`)
- [x] CSRF activo en todos los formularios (los cinco rechazan un envío sin token, con y sin sesión), acceso sin sesión bloqueado y primer paso sin distinguir usuario inexistente de contraseña mala (`cuentas/tests_cuenta.py`)
- [x] Ningún secreto en los registros del programa: una prueba captura todos los registros durante el recorrido completo (inicio, token, registro del segundo factor, códigos nuevos, auditoría) y no aparece ninguna contraseña, código, token, secreto ni lo escrito en el campo de usuario; la auditoría tiene su propia prueba (CA-71) y el registro de Nginx se verificó sin cadena de consulta. **La condición 7 de terminado se cierra con la entrega, porque las entregas siguientes agregan datos personales**

### J. Criterios de aceptación de la E0

- [x] **CA-13** — Una sola cuenta con segundo factor · prioridad Alta — cumplido: `cuentas/tests_cuenta.py` (todas las vistas exigen sesión), `cuentas/tests.py` (una sola cuenta por la tabla) (corridas de la integración continua en verde, informadas por el solicitante el 2026-10-24)
- [~] **CA-18** — Configuración regional · prioridad Media — cumplido en lo que le toca a la E0 (zona de la organización, formato, UTC, el histórico no cambia al cambiar la zona); **su parte de contratos en USD se verifica en la E2, por aceptación del solicitante del 2026-10-24** (actualización 2026-10-24n)
- [x] **CA-48** — Sesión · prioridad Alta — cumplido: `cuentas/tests.py` (cierre a las 24 h y a la hora de inactividad) (corridas de la integración continua en verde, informadas por el solicitante el 2026-10-24)
- [x] **CA-53** — Auditoría sin valores personales · prioridad Alta — cumplido: `nucleo/tests_auditoria.py` (el teléfono consta como cambiado sin su valor; un importe, con anterior y nuevo) (corridas de la integración continua en verde, informadas por el solicitante el 2026-10-24)
- [x] **CA-68** — Límite de intentos fallidos (RF-27) · prioridad Alta — cumplido en el alcance de la E0 (HI-05): espera creciente y reinicio probados; el aviso queda en la auditoría y en la alerta web; **el correo a las dos direcciones se verifica en la E4** (corridas de la integración continua en verde, informadas por el solicitante el 2026-10-24)
- [x] **CA-69** — Segundo factor y códigos de recuperación (RF-27) · prioridad Alta — cumplido en el alcance de la E0 (HI-05): 10 códigos de un solo uso, TOTP sin repetición y con tolerancia, códigos nuevos con la contraseña; aviso en la auditoría y la alerta web; el correo en la E4 (corridas de la integración continua en verde, informadas por el solicitante el 2026-10-24)
- [x] **CA-70** — Creación de la cuenta y rescate por el servidor (RF-27) · prioridad Alta — cumplido en el alcance de la E0 (HI-01): creación y rescate por comandos, registro en el primer ingreso, constancia en la auditoría; el aviso por correo a las dos direcciones en la E4 (corridas de la integración continua en verde, informadas por el solicitante el 2026-10-24)
- [x] **CA-71** — Auditoría de autenticación y su consulta (RF-28) · prioridad Alta — cumplido: `cuentas/tests_auditoria.py` y `nucleo/tests_auditoria.py` (fallo y acierto con fecha, hora e IP; sin secretos; consulta de solo lectura que no genera registros) (corridas de la integración continua en verde, informadas por el solicitante el 2026-10-24)


*Estado a 2026-10-24: 7 de 8 cumplidos con su prueba en verde en la integración continua; CA-18 cumplido en lo que le toca a la E0 y su parte de contratos diferida a la E2 por aceptación del solicitante.*

### K. Requisitos de la E0

- [ ] **RF-26** — Autenticar administrador
- [ ] **RF-27** — Administrar la cuenta
- [ ] **RF-28** — Auditar operaciones críticas
- [ ] **RF-33** — Configurar moneda y zona horaria

- [ ] **RNF-01** — Autenticación
- [ ] **RNF-02** — Autorización
- [ ] **RNF-06** — Trazabilidad
- [ ] **RNF-09** — Recuperación
- [ ] **RNF-12** — Configuración regional
- [ ] **RNF-14** — Seguridad de los datos
- [ ] **RNF-17** — Zona horaria y moneda

### L. Cierre de la E0

- [x] 1. Pruebas de los CA asignados en la integración continua con PostgreSQL 18; ninguna Alta sin escribir (EPP, sección 11): corridas en verde informadas por el solicitante el 2026-10-24; los 7 CA completos y la parte de CA-18 que le toca a la E0
- [x] 2. Integración continua en verde: pruebas, `check --deploy` y migraciones desde cero (ADR-025): informado por el solicitante el 2026-10-24 (todas las corridas, incluidos `respaldo` y `pip-audit`); el asistente no puede ver las Actions
- [x] 3. `verificar_coherencia.ps1` sin problemas (2026-10-24)
- [x] 4. Tablas y secuencias nuevas en el archivo de privilegios, con su prueba (ADR-027, ADR-031): una prueba exige una entrada por tabla
- [x] 5. Código sin cubrir de los módulos críticos revisado, sin umbral numérico (EPP, sección 9): **autorrevisión** del autor con la herramienta de cobertura el 2026-10-24 (94 % a 99 %; 39 a 8 líneas sin ejecutar, las 8 restantes son ajustes que se prueban en procesos aparte); detalle en la actualización 2026-10-24m. **No sustituye la revisión por otra persona que el plan exige para lo crítico antes de cargar datos reales (sección 3.3), todavía sin persona designada**
- [x] 6. Desplegada en la etapa A (WSL 2 con Ubuntu 26.04.1) con datos ficticios y criterio de salida propio cumplido: despliegue de un comando, inicio de sesión con segundo factor, restauración completa desde el respaldo local y pruebas de R12 (actualización 2026-10-24j)
- [x] 7. Ningún dato personal ni secreto en los registros ni en la auditoría (RF-28, RNF-06, R14): pruebas de los registros del programa, de la auditoría y del registro de Nginx; **en la E0 no hay datos personales de terceros todavía; se repite en cada entrega**
- [x] 8. `CAMBIOS.md` de la entrega y trazabilidad (RF, CA, ADR) al día: actualizaciones 2026-10-23zy a 2026-10-24n
- [x] 9. Ningún defecto conocido de prioridad Alta abierto, hasta donde el asistente sabe al 2026-10-24 (las decisiones abiertas no son defectos; las lista el CAMBIOS 2026-10-24n)
- [x] Actualizar `AVANCE_IMPLEMENTACION.md` (estado, fecha de fin, condiciones y CA aprobados): E0 terminada el 2026-10-24, 9 de 9 condiciones, 7 de 8 CA con CA-18 diferido en su parte de contratos
- [ ] Tareas agregadas durante la entrega (*Propuesta*; preguntar antes): —


---

## E1 Inquilinos
**Aplicaciones:** inquilinos · **Estado:** terminada el 2026-10-26 (9 de 9 condiciones, 8 de 8 CA; CA-29 solo en su mecanismo) · iniciada el 2026-10-24 (autorizada por el solicitante)
**Contenido (plan):** Inquilino, cédulas privadas, consentimiento con el texto de cada versión, accesos a documentos y su auditoría, reducción de la fotografía en el navegador y subida de cada archivo por separado
**Criterio de salida:** Cédula servida solo por la vista con autorización y registrada; acceso denegado sin sesión; peso de fotos reales de un iPhone y dos Android medido y registrado

### Tareas específicas (del criterio de salida, los hallazgos y el plan)

- [x] Cédula servida solo por la vista con autorización y registrada; acceso denegado sin sesión (criterio de salida; CA-11, CA-26): pruebas y recorrido real por HTTPS en WSL (302 sin sesión; un acceso registrado por consulta)
- [x] Medir y registrar el peso de fotos reales de un iPhone y de dos Android tras la reducción (criterio de salida; CA-73): **con la desviación aceptada por el solicitante el 2026-10-26** (muestras públicas de 2 iPhone 14 Pro, un Galaxy S23 y un Pixel 8, más una foto de su propio Motorola moto g72): de 0,34 a 1,28 MiB, todas bajo 2 MB (actualizaciones 2026-10-26b y 2026-10-26d)
- [x] Probar que un fallo al guardar no deja un archivo huérfano (HI-07; borrado en la misma petición, propuesta): pruebas del servicio y del almacenamiento (fallo de `fsync`)
- [x] Comprobar el navegador que no puede reducir la imagen (CA-74): **no se hizo a mano**; lo cubre una prueba automática con un navegador real al que se le quita el lienzo (propuesta del asistente: el solicitante puede exigir la comprobación manual)
- [x] CA-67: en la E1 solo el texto de cada versión y el aviso en la ficha; el rechazo de contratos nuevos con un inquilino que revocó va en la E2 (HI-04): hecho el texto, la revocación sin cambiar datos y el aviso

### Plan de trabajo de la E1 (propuesta del asistente derivada de los RF, CA, el modelo de datos v0.7 y el diseño técnico; sin aprobar)
**A. Modelos y esquema** (MDD v0.7; ADR-027, ADR-028, ADR-031)
- [x] Aplicación `inquilinos` y sus modelos: `Inquilino`, `TextoConsentimiento`, `Consentimiento`, `DocumentoIdentidad` y `AccesoDocumento`, con las restricciones de la base (R14, R25, R27, medio, cara, acción, revocación posterior al consentimiento) (RF-01, RF-39, RF-45; actualización 2026-10-24r). `AccesoDocumento` solo cubre la cédula: el acceso a la fotografía del contrato queda para la E2 (ver el CAMBIOS)
- [x] Privilegios y guardas: `AccesoDocumento` y `TextoConsentimiento` solo `SELECT` e `INSERT`; `Consentimiento` solo actualiza `revocado_en`; `DocumentoIdentidad` solo actualiza `eliminado_en`; `Inquilino` sin `DELETE`; entradas en `sga/privilegios.py`; guardas comunes en `nucleo.models.RegistroProtegido` (ADR-027)
- [x] Pruebas con SQL directo de que el rol de la aplicación es rechazado en `UPDATE`, `DELETE` y `TRUNCATE` sobre los accesos a documentos y de que solo puede tocar las columnas permitidas de los consentimientos y las fotografías (ADR-027); 5 pruebas nuevas en `nucleo/tests_privilegios.py`

**B. Registro, ficha y estado del inquilino**
- [x] Registrar un inquilino (nombre, tipo y número de documento obligatorios; teléfono y correo opcionales) con el consentimiento, en una transacción con su auditoría; sin fotografía todavía (RF-01, CA-01): `services.registrar_inquilino` (servicio probado; la pantalla es del grupo F; el texto del consentimiento, del grupo C) (actualización 2026-10-24s)
- [x] Advertir de un documento duplicado entre inquilinos activos antes de guardar, sin bloquear (RF-01, CA-25): `DocumentoDuplicado` sin guardar hasta confirmar; también al cambiar la identificación y al reactivar
- [x] Buscar (nombre, documento, teléfono y correo, en una sola consulta), consultar y actualizar la ficha; solo se guarda y se audita lo que cambia, sin valores personales (RF-03, RF-05, RF-28, CA-53): `selectors.listar_inquilinos`, `selectors.obtener_ficha`, `services.actualizar_inquilino`. **RF-05 se completa con el contrato vigente y las obligaciones en la E2 y la E3**
- [x] La ficha indica cuándo falta el frente (`falta_frente`) y la lista filtra «Sin frente», que incluye a quien solo tiene el reverso; sin alertas ni correos (RF-03). Los textos de las pantallas, en el grupo F
- [x] Desactivar y reactivar (RF-04, CA-29) con un **punto de extensión** (`inquilinos.bloqueos`): la E1 lo prueba con comprobaciones falsas; el bloqueo real por contrato vigente se verifica en la E2 y el de saldos pendientes en la E3. Desactivar no borra nada del historial

**C. Consentimiento** (RF-39, OL-13; DP-21 abierta)
- [x] Texto informativo con los ocho puntos del art. 5 de la Ley 8968 como versión inmutable (`TextoConsentimiento`), **borrador del asistente que se marca «sin validar por abogado»** en el propio texto y con el campo `borrador` (decisión 1); se carga con `manage.py cargar_texto_consentimiento` desde la identidad del responsable (que debe estar definida); el consentimiento apunta a la versión mostrada, con medio y fecha, y la ficha muestra el texto exacto de esa versión (CA-67, primera parte; actualización 2026-10-24t). **El texto no es asesoría legal y espera al abogado (DP-21)**
- [x] Registrar la revocación sin efecto retroactivo (`services.revocar_consentimiento`) y mostrar el aviso en la ficha (`consentimiento_revocado`, `puede_crear_contratos`) (CA-67, segunda parte). Los ganchos `inquilinos.ganchos.al_revocar` permiten que la E5 abra de oficio la solicitud de supresión y la E2 consulta `tiene_consentimiento_vigente`; **el rechazo de contratos nuevos va en la E2 (HI-04) y la solicitud de supresión, en la E5 (RF-40)**

**D. Fotografías del documento: servidor** (RF-02, RF-45, ADR-003; CA-74, CA-83, CA-11, CA-26)
- [x] Almacenamiento privado fuera de la raíz web (`RAIZ_DOCUMENTOS/cedulas`), nombre aleatorio (UUID) creado con `O_EXCL`, permisos 0640 y carpeta con bit setgid para que el respaldo lea; una referencia con otra forma (`..`, barras, mayúsculas, extensiones) se rechaza (actualización 2026-10-24u)
- [x] Validación en el servidor con Pillow (12.3.0; **13.0.0 desde la actualización 2026-10-26c**), una petición por archivo: JPEG o PNG por su tipo real, hasta 5 242 880 bytes, decodificación completa que rechaza lo dañado, tope de 60 millones de píxeles comprobado antes de decodificar (RF-02, R27, CA-74, CA-83); exige el consentimiento vigente (RF-39)
- [x] Se vuelve a codificar la imagen sin metadatos (ubicación, cámara, comentario, XMP, bloques de texto de PNG, datos añadidos al final) y con la orientación aplicada; se conserva el perfil de color (RF-02, BR-05). **Con el JPEG sin girar se usan las mismas tablas de calidad, pero no es una transcodificación sin pérdida**; CA-82 se completa en la E2 con fotos reales
- [x] A lo sumo una fotografía activa por cara; reemplazar marca la anterior como eliminada en la misma transacción y borra su archivo del disco al confirmarla (R25); un fallo al guardar no deja un archivo huérfano (HI-07)
- [x] Vista que entrega el archivo solo con sesión, sin URL pública, con `no-store` y `nosniff`, y un `AccesoDocumento` por cada consulta o descarga sin la imagen; si el registro falla, no se entrega (RF-45, CA-11, CA-26). Subida de UN archivo por petición en `/inquilinos/<id>/fotografias/<cara>/`
- [x] Nginx: `client_max_body_size` de 6 MiB solo en la ruta de subida y 1 MiB en el resto, comprobado en WSL con cuerpos reales (201, 413 y 413) (ADR-003)

**E. Reducción en el navegador** (RF-50; CA-73, CA-74)
- [x] Script propio sin bibliotecas (`reducir_fotografia.js`): lado mayor de 2048 píxeles sin ampliar, JPEG a calidad 0,85 y menor (0,80, 0,75, 0,70) si pasa de 2 MB, reducción del lado si pasa de 5 MiB, orientación conservada, fondo blanco para PNG con transparencia; si el navegador no puede, envía el original solo si es JPEG o PNG de hasta 5 MiB y si no avisa antes de enviar; mensajes como texto, nunca como HTML (actualización 2026-10-24v)
- [x] El script es un archivo estático propio: `collectstatic` a `/opt/sga/static` (de root; la aplicación no puede escribir) y Nginx sirve `/static/` con `alias` emparejado; la CSP en modo informe no registra violaciones; verificado en WSL que no se sale de `/static/` (6 intentos) ni se sirven los documentos privados
- [x] 11 pruebas en un navegador real con Selenium y `StaticLiveServerTestCase` (Chrome y Edge sin ventana; se omiten donde no hay navegador): una foto de 4032x3024 y 6,44 MiB sale de 2048x1536 y 1,47 MiB (CA-73); sin lienzo se envía el original o se avisa (CA-74). La comprobación **manual** del navegador sin lienzo queda para el grupo G

**F. Pantallas** (decisión 6: funcionales y accesibles, sin estilos; los wireframes siguen pendientes)
- [x] Lista con búsqueda (nombre, documento, teléfono, correo), filtro de estado y «Sin frente»; registro con el texto informativo a la vista, medio y fecha del consentimiento y confirmación obligatoria; ficha con datos, fotografías (ver y descargar) y consentimientos; editar; desactivar y reactivar con confirmación (el motivo de bloqueo se muestra); revocar el consentimiento con confirmación y sin tocar datos. Todas con `login_required`, CSRF y `no-store`; 35 pruebas propias y un recorrido real por HTTPS en WSL (actualización 2026-10-24w)

**G. Medición, despliegue y cierre**
- [x] Medir y registrar el peso de fotos reales (CA-73): hecho con muestras públicas de teléfonos y una foto del solicitante, **desviación aceptada por él el 2026-10-26**; herramienta `src/despliegue/medir_reduccion.py`; de 0,34 a 1,28 MiB tras la reducción (actualizaciones 2026-10-26b y 2026-10-26d)
- [x] Desplegar en WSL, verificar, actualizar la CI y repetir las pruebas con Python 3.14 (hecho con cada grupo; en el último despliegue: 393 pruebas en WSL y `verificar.sh` sin fallos; **el resultado de GitHub Actions lo confirma el solicitante**)
- [x] Cierre con las nueve condiciones comunes y el registro de avance (actualización 2026-10-26d)

**Decisiones del solicitante de la E1 (24-oct-2026; actualización 2026-10-24q)**
1. **Texto informativo del consentimiento:** borrador redactado por el asistente, marcado «sin validar por abogado» (DP-21); versión inmutable que el abogado reemplazará con una versión nueva.
2. **Imágenes:** Pillow 12.3.0 (**sustituido por 13.0.0 el 2026-10-26 por 37 vulnerabilidades, actualización 2026-10-26c**); decodificación completa, tope de 60 millones de píxeles, orientación aplicada, archivo nuevo sin metadatos (volver a codificar); Pillow 13.0.0 se descarta por tener 8 días.
3. **Pruebas del navegador:** ya decididas en la estrategia de pruebas (Selenium con `StaticLiveServerTestCase`); no se pregunta. Se omiten donde no haya navegador (WSL).
4. **Archivos estáticos:** `collectstatic` a `/opt/sga/static` y Nginx sirve `/static/` con `alias` bien emparejado; prueba de que no se sirve nada fuera de `/static/` ni los documentos privados.
5. **Desactivar (CA-29):** punto de extensión de comprobaciones de bloqueo; la E1 lo prueba con una comprobación falsa y **el bloqueo real se verifica en la E2 (contrato vigente) y en la E3 (saldos pendientes)**, con aceptación escrita del solicitante (CA-29 es de prioridad Media).
6. **Pantallas:** funcionales y accesibles, sin estilos; el diseño llega con los wireframes.

### Requisitos funcionales

- [ ] **RF-01** — Registrar inquilino
- [ ] **RF-02** — Validar información
- [ ] **RF-03** — Consultar y actualizar al inquilino
- [ ] **RF-04** — Desactivar inquilino
- [ ] **RF-05** — Consultar ficha de inquilino
- [ ] **RF-39** — Informar y registrar consentimiento
- [ ] **RF-45** — Auditar acceso a cédulas y exportaciones del titular
- [ ] **RF-50** — Reducir la fotografía antes de enviarla

### Requisitos no funcionales

- [ ] **RNF-03** — Privacidad
- [ ] **RNF-15** — Confidencialidad

### Criterios de aceptación (con la prioridad de la estrategia de pruebas)

- [x] **CA-01** — Registro de inquilino · prioridad Media — cumplido: `inquilinos/tests_pantallas.py` y `tests_servicios.py` (con campos obligatorios y consentimiento; sin consentimiento, error y nada guardado; sin teléfono ni correo se guarda)
- [x] **CA-11** — Protección de cédula · prioridad Alta — cumplido: `inquilinos/tests_fotografias.py` (sin sesión 302, sin URL pública) y recorrido real por HTTPS en WSL
- [x] **CA-25** — Documento duplicado · prioridad Media — cumplido: `tests_servicios.py` y `tests_pantallas.py` (advierte antes de guardar y solo guarda si se confirma)
- [x] **CA-26** — Auditoría de acceso a cédula · prioridad Alta — cumplido: `tests_fotografias.py` (un registro por consulta o descarga, sin la imagen; si el registro falla no se entrega) y WSL (2 accesos)
- [x] **CA-29** — Desactivar con contrato vigente · prioridad Media — cumplido **solo en el mecanismo** (punto de extensión probado con un motivo registrado); **el bloqueo real por contrato vigente va en la E2 y por saldos pendientes en la E3**, por aceptación del solicitante (actualización 2026-10-24 (q))
- [x] **CA-73** — Reducción de la fotografía en el navegador (RF-50) · prioridad Media — cumplido: `tests_navegador.py` (4032x3024 de 6,44 MiB a 2048x1536 de 1,47 MiB; 1200x800 no se amplía; orientación) y medición con fotos de teléfono, **con la desviación aceptada por el solicitante** (actualización 2026-10-26d)
- [x] **CA-74** — Envío sin reducción y un archivo por petición (RF-50, RF-02) · prioridad Alta — cumplido: `tests_navegador.py` (sin lienzo se envía el original o se avisa) y `tests_fotografias.py` (el servidor rechaza lo que pesa más de 5 MiB o no es JPEG/PNG; un rechazo no descarta el otro archivo)
- [x] **CA-83** — Imagen que no se puede decodificar (RF-02) · prioridad Media — cumplido: `tests_imagenes.py` (truncados y dañados, JPEG y MPO) y `tests_fotografias.py`

### Cierre

- [x] 1. Pruebas de los CA asignados en la integración continua con PostgreSQL 18; ninguna Alta sin escribir (EPP, sección 11): los 8 CA tienen pruebas; corridas de la integración continua en verde informadas por el solicitante el 2026-10-26 (tras el cambio a Pillow 13.0.0); 410 pruebas en Windows y 399 en WSL
- [x] 2. Integración continua en verde: pruebas, `check --deploy` y migraciones desde cero (ADR-025): informado por el solicitante el 2026-10-26 («Git pasó las pruebas»); **el asistente no ve las corridas**, y la del commit de cierre la confirma el solicitante
- [x] 3. `verificar_coherencia.ps1` sin problemas (2026-10-26)
- [x] 4. Tablas y secuencias nuevas en el archivo de privilegios, con su prueba (ADR-027, ADR-031): las cinco tablas de `inquilinos` están en `sga/privilegios.py` y la prueba exige una entrada por tabla
- [x] 5. Código sin cubrir de los módulos críticos revisado, sin umbral numérico (EPP, sección 9): **autorrevisión** del autor con la herramienta de cobertura el 2026-10-26 (de 706 líneas de `inquilinos`, 5 sin ejecutar: 4 defensas inalcanzables de `imagenes.py` y 1 rama) tras añadir 4 pruebas; **no es una revisión independiente**
- [x] 6. Desplegada en la etapa A (WSL 2 con Ubuntu-26.04) con datos ficticios y criterio de salida propio cumplido: despliegue de un comando, recorrido real por HTTPS (registro, ficha, subida de cédula con GPS sin metadatos guardados, entrega solo con sesión, accesos registrados, límites de Nginx, estáticos) y fotos de teléfono reducidas y aceptadas por el servidor
- [x] 7. Ningún dato personal ni secreto en los registros ni en la auditoría (RF-28, RNF-06, R14): pruebas de la auditoría (solo nombres de campos cambiados), registro de Nginx sin la cadena de consulta (la búsqueda va en ella) y Gunicorn sin registro de acceso, comprobados en WSL; el nombre del archivo de cédula es un UUID
- [x] 8. `CAMBIOS.md` de la entrega y trazabilidad (RF, CA, ADR) al día: actualizaciones 2026-10-24p a 2026-10-24w y 2026-10-26a a 2026-10-26d
- [x] 9. Ningún defecto conocido de prioridad Alta abierto, hasta donde el asistente sabe al 2026-10-26: el defecto del MPO se corrigió; las decisiones abiertas (ciclo ACCESO_DOCUMENTO / DOCUMENTO_CONTRATO para la E2, revisor independiente, abogado) no son defectos
- [x] Actualizar `AVANCE_IMPLEMENTACION.md` (estado, fecha de fin, condiciones y CA aprobados): E1 terminada el 2026-10-26, 9 de 9 condiciones, 8 de 8 CA (CA-29 solo en su mecanismo)
- [ ] Tareas agregadas durante la entrega (*Propuesta*; preguntar antes): —


---

## E2 Contratos y obligaciones
**Aplicaciones:** alquileres, nucleo · **Estado:** en curso desde 2026-10-26 (autorizada por el solicitante)
**Contenido (plan):** Propiedades, contratos y condiciones, solape (R2), finalizar, anular y sustituir inquilino, alias de la propiedad y su estado inactivo, reajuste y corrección, obligaciones por período, estados, saldo de apertura y proceso diario, perfil de la propiedad con la cédula del inquilino del contrato vigente y la fotografía del contrato
**Criterio de salida:** Proceso diario idempotente (dos ejecuciones sin duplicados); casos de fin de mes, bisiesto, prorrateo y gracia pasan

### Tareas específicas (del criterio de salida, los hallazgos y el plan)

- [x] Proceso diario idempotente: dos ejecuciones sin duplicados (criterio de salida; RNF-04, RNF-16): probado en Windows y en WSL como `sga_app` (actualización 2026-10-26k)
- [x] Casos de fin de mes, año bisiesto, prorrateo y días de gracia pasan (criterio de salida): probados en los grupos B y E
- [ ] Medir con fotos reales (un iPhone y dos Android) los metadatos que deja la reducción y registrar el resultado (CA-82, DP-29)
- [ ] Fijar las cifras de reducción de la fotografía del contrato (DP-29; hoy parten de 3508 px y calidad 0,85)
- [x] CA-67 completo: rechazo de contratos nuevos con un inquilino que revocó el consentimiento (HI-04): `crear_contrato` lo rechaza y lo prueba (actualización 2026-10-26i)
- [ ] CA-75 y CA-78 (cédula desde el perfil de la propiedad y contrato rechazado sin frente) (HI-08): **CA-78 ya se rechaza y se prueba en el servicio** (actualización 2026-10-26i); CA-75 es del grupo F

### Plan de trabajo de la E2 (propuesta del asistente derivada de los RF, RN, CA, el modelo de datos v0.7 y el diseño técnico; sin aprobar)
**A. Modelos y esquema** (MDD v0.7; ADR-027, ADR-028, ADR-030, ADR-031)
- [x] Aplicación `alquileres` y sus modelos: `Propiedad`, `Contrato`, `CondicionContrato`, `Obligacion`, `AjusteObligacion`, `DocumentoContrato` y `EjecucionProceso`, con las restricciones del modelo (R1, R2 con exclusión de PostgreSQL y `btree_gist`, R3, R20, R21, R22, R28) (RF-06, RF-07, RF-10, RF-11, RF-12, RF-52). Hecho el 2026-10-26 (actualización 2026-10-26g): ocho tablas con 32 restricciones de tabla, el solape con `btree_gist` probado en un día compartido, el relevo contiguo, el contrato abierto y el anulado; la anulación se completa una sola vez con un disparador
- [x] Acceso a la fotografía del contrato: tabla propia `AccesoDocumentoContrato` en `alquileres` con su clave foránea (decisión 1 de la E2), solo `SELECT` e `INSERT` (R12, R23)
- [x] Privilegios mínimos y guardas: `AjusteObligacion` solo `SELECT` e `INSERT`; `Obligacion` sin tocar `importe_inicial`; entradas en `sga/privilegios.py` con su prueba (R12, ADR-027): ocho entradas nuevas en `sga/privilegios.py` (el despliegue aplica 23 tablas); el contrato solo actualiza `fecha_fin`, `anulado_en` y `motivo_anulacion`, y la obligación solo `anulada_en` y `motivo_anulacion`; probado con SQL directo como el rol de la aplicación

**B. Cálculo de períodos e importes** (funciones puras, sin base de datos)
- [x] Período de alquiler (RN-03), vencimiento (RN-05), fecha límite con días de gracia (RN-06) y prorrateo del último período con redondeo explícito (RN-12): fin de mes, año bisiesto, 29, 30 y 31, CRC sin decimales y USD a dos. Hecho el 2026-10-26 (actualización 2026-10-26h): `alquileres/calculo.py`, 41 pruebas, 100 % de cobertura, 9 mutaciones detectadas; **el redondeo es `ROUND_HALF_UP` explícito y un solo redondeo al final**
- [x] Cálculo guardado en `datos_calculo` para reconstruir la regla (RN-13): `Prorrateo.datos_calculo()` devuelve la regla, los días cobrables y del período, el importe previo (cociente exacto con 6 decimales) y el final

**C. Propiedades y contratos** (RF-06 a RF-09, RF-36, RF-48; RN-02, RN-30)
- [x] Servicios de propiedad: alias único, inactiva con bloqueo si hay contrato vigente, futuro o por decidir, y sin contratos nuevos mientras esté inactiva (CA-63): alias sin distinguir mayúsculas (propuesta), dirección y descripción sin valor en la auditoría
- [x] Crear contrato: frente cargado (R26), solape (R2), advertencia por vigencia menor de tres años, condición inicial, auditoría (CA-02, CA-78, CA-32): todos los motivos de rechazo a la vez; la comprobación previa del solape dice con qué contrato choca y la restricción de la base es la última defensa; el depósito (RF-07, «cuando corresponda») es de la E3
- [x] Rechazar contratos nuevos con un inquilino que revocó el consentimiento (CA-67 completo, HI-04)
- [x] Estado derivado del contrato y de la propiedad (futuro, vigente, por decidir, finalizado, anulado): nueva marca `cerrado_en` (propuesta) para distinguir finalizado de por decidir; la consulta por estado y el estado de un contrato coinciden en los nueve casos probados
- [x] Finalizar contrato con prorrateo y anulación de obligaciones futuras sin movimientos; anular contrato sin movimientos; sustituir inquilino (CA-24, CA-31, CA-62), **y renovar cambiando la fecha de fin del mismo contrato (decisión 2 de la E2)**; los movimientos de la E3 se consultan por un proveedor reemplazable (`alquileres/movimientos.py`)
- [x] Registrar en `inquilinos.bloqueos` el motivo real «contrato vigente o futuro» (CA-29, parte de la E2): se registra al arrancar la aplicación; bloquea con contrato futuro, vigente o por decidir (los futuros, propuesta); **la aceptación escrita del solicitante para el bloqueo por saldos de la E3 sigue pendiente al cierre**

**D. Reajuste y corrección** (RF-10; RN-14)
- [x] Reajuste con fecha efectiva al inicio del período siguiente, tope digitado con su fuente, advertencia sin bloqueo y rechazo en moneda extranjera (CA-12, CA-39, CA-51): `condiciones.reajustar_contrato`; el porcentaje se calcula con fracciones exactas y 4 decimales; en vivienda el tope y la fuente son obligatorios y superarlo solo advierte; las obligaciones pagadas no se tocan (actualización 2026-10-26j)
- [x] Corrección retroactiva con motivo y ajustes inmutables; bloqueo si el importe queda bajo lo abonado (CA-22, CA-40, CA-55): `condiciones.corregir_contrato` (monto, día de vencimiento y días de gracia) y `ajustar_manualmente` (RF-09); **por la decisión 3 de la E2 las fechas de vencimiento y límite de las no pagadas se actualizan con auditoría del valor anterior y el nuevo**; el historial de importes se reconstruye con `selectors.historial_de_importes`; un error en el período (la fecha de inicio) **no** se corrige aquí

**E. Obligaciones y proceso diario** (RF-11, RF-12, RF-14, RF-42, RF-43; RNF-04, RNF-16)
- [x] Generación 30 días antes del período para contratos futuros, vigentes y por decidir, idempotente y segura en paralelo (CA-03, CA-30, CA-14, CA-36, CA-50): `obligaciones.generar_obligaciones`; el último período nace prorrateado y el contrato por decidir sigue generando (actualización 2026-10-26k)
- [x] Saldo de apertura con su fecha de vencimiento digitada (CA-49): `registrar_saldo_de_apertura`; la fecha de apertura va en `datos_calculo` (propuesta)
- [x] Estado de la obligación derivado (pendiente, vencida, pagada, anulada) con la fecha local de la organización: `selectors.estado_de_la_obligacion`
- [x] Comando del proceso diario con `EjecucionProceso` y su unidad `systemd` con temporizador (propuesta); dos ejecuciones sin duplicados (criterio de salida): `ejecutar_proceso_diario`, `sga-proceso-diario.timer` a las 07:00

**F. Fotografías del contrato y cédula desde el perfil** (RF-51, RF-52; CA-75, CA-76, CA-77, CA-82)
- [ ] Fotografía del contrato: hasta 10, bloqueo de la fila del contrato, reducción en el navegador con lado de 3508 px de partida y entrega solo con sesión, auditada (H18)
- [ ] Cédula desde el perfil de la propiedad, con «Reemplazar» y acción desactivada sin contrato vigente

**G. Pantallas** (como en la E1: funcionales y accesibles, sin estilos)
- [ ] Propiedades y su perfil, contratos y sus condiciones, obligaciones por contrato, saldo de apertura, reajuste y corrección

**H. Medición, despliegue y cierre**
- [ ] Medir con fotos de teléfono el peso de la fotografía del contrato y los metadatos que deja la reducción; fijar las cifras (DP-29, CA-82)
- [ ] Desplegar en WSL, verificar y repetir las pruebas con Python 3.14; comprobar la versión de Pillow dentro de WSL
- [ ] Cierre con las nueve condiciones comunes y el registro de avance

**Decisiones del solicitante de la E2 (26-oct-2026; actualización 2026-10-26f)**
1. **Acceso a la fotografía del contrato:** tabla propia `AccesoDocumentoContrato` en `alquileres`, con clave foránea al `DocumentoContrato` y solo inserción; la cédula sigue en `inquilinos.AccesoDocumento`. R23 se cumple por construcción (cada tabla tiene una sola clave foránea). Descartadas: aplicación neutra con referencia genérica y referencia sin clave foránea.
2. **Renovación del contrato (actualización 2026-10-26i):** renovar es cambiar la fecha de fin del mismo contrato a una posterior o quitarla, con motivo y auditoría; se rechaza si el contrato está anulado o cerrado, si ya es abierto o si el cambio solapa con otro. Descartadas: contrato nuevo contiguo y no implementar la renovación.
3. **Fechas de las obligaciones en una corrección (actualización 2026-10-26j):** se actualizan `fecha_vencimiento` y `fecha_limite` de las obligaciones no pagadas, no anuladas y de períodos desde la fecha efectiva, con auditoría del valor anterior y el nuevo; el importe inicial sigue inmutable. Descartadas: que solo rija para las obligaciones nuevas y anular y regenerar.

### Requisitos funcionales

- [ ] **RF-06** — Registrar propiedad
- [ ] **RF-07** — Crear contrato
- [ ] **RF-08** — Validar solapamiento contractual
- [ ] **RF-09** — Finalizar contrato
- [ ] **RF-10** — Modificar condiciones contractuales
- [ ] **RF-11** — Generar obligaciones por período
- [ ] **RF-12** — Evitar duplicados
- [ ] **RF-14** — Determinar estado de obligación
- [ ] **RF-36** — Sustituir inquilino mediante nuevo contrato
- [ ] **RF-42** — Avisar vencimiento de contrato
- [ ] **RF-43** — Registrar saldo de apertura
- [ ] **RF-48** — Anular contrato
- [ ] **RF-51** — Agregar la cédula desde el perfil de la propiedad
- [ ] **RF-52** — Registrar la fotografía del contrato

### Requisitos no funcionales

- [ ] **RNF-04** — Integridad
- [ ] **RNF-16** — Idempotencia de procesos

### Criterios de aceptación (con la prioridad de la estrategia de pruebas)

- [ ] **CA-02** — Creación de contrato · prioridad Media
- [ ] **CA-03** — Generación mensual y mes corto · prioridad Alta
- [ ] **CA-10** — Conservación del historial · prioridad Alta
- [ ] **CA-12** — Reajuste · prioridad Alta
- [ ] **CA-14** — Último período prorrateado · prioridad Alta
- [ ] **CA-22** — Corrección con obligaciones no pagadas · prioridad Alta
- [ ] **CA-24** — Sustitución de inquilino · prioridad Media
- [ ] **CA-30** — Generación anticipada · prioridad Alta
- [ ] **CA-31** — Fin de contrato con obligaciones futuras · prioridad Alta
- [ ] **CA-32** — Contrato por decidir · prioridad Media
- [ ] **CA-36** — Vencimiento y gracia · prioridad Alta
- [ ] **CA-39** — Reajuste sobre el tope o en moneda extranjera · prioridad Alta
- [ ] **CA-40** — Cambio por debajo de lo abonado · prioridad Alta
- [ ] **CA-49** — Saldo de apertura · prioridad Alta
- [ ] **CA-50** — Vencimiento dentro del período · prioridad Alta
- [ ] **CA-51** — Tope de reajuste digitado · prioridad Alta
- [ ] **CA-55** — Ajuste que conserva el importe inicial · prioridad Alta
- [ ] **CA-62** — Anular un contrato (RF-48) · prioridad Media
- [ ] **CA-63** — Propiedad inactiva (RF-06) · prioridad Media
- [ ] **CA-67** — Consentimiento y revocación (RF-39) · prioridad Alta
- [ ] **CA-75** — Cédula desde el perfil de la propiedad (RF-51) · prioridad Media
- [ ] **CA-76** — Fotografía del contrato (RF-52) · prioridad Alta
- [ ] **CA-77** — Protección y auditoría de la fotografía del contrato (RF-52) · prioridad Alta
- [ ] **CA-78** — Registro en dos pasos y contrato sin frente (RF-01, RF-03, RF-07) · prioridad Alta
- [ ] **CA-82** — Metadatos de la imagen (RF-02, RF-50) · prioridad Media

### Cierre

- [ ] 1. Pruebas de los CA asignados en la integración continua con PostgreSQL 18; ninguna Alta sin escribir (EPP, sección 11)
- [ ] 2. Integración continua en verde: pruebas, `check --deploy` y migraciones desde cero (ADR-025)
- [ ] 3. `verificar_coherencia.ps1` sin problemas
- [ ] 4. Tablas y secuencias nuevas en el archivo de privilegios, con su prueba (ADR-027, ADR-031)
- [ ] 5. Código sin cubrir de los módulos críticos revisado, sin umbral numérico (EPP, sección 9)
- [ ] 6. Desplegada en la etapa A (WSL 2 con Ubuntu-26.04) con datos ficticios y criterio de salida propio cumplido
- [ ] 7. Ningún dato personal ni secreto en los registros ni en la auditoría (RF-28, RNF-06, R14)
- [ ] 8. `CAMBIOS.md` de la entrega y trazabilidad (RF, CA, ADR) al día
- [ ] 9. Ningún defecto conocido de prioridad Alta abierto
- [ ] Actualizar `AVANCE_IMPLEMENTACION.md`
- [ ] Tareas agregadas durante la entrega (*Propuesta*; preguntar antes): —


---

## E3 Movimientos y depósitos
**Aplicaciones:** alquileres · **Estado:** no iniciada (requiere autorización expresa del solicitante)
**Contenido (plan):** Abonos y pagos completos, moneda distinta, anulación, saldo derivado, historial, depósito de garantía, número de recibo físico, rechazo de períodos futuros (RN-15)
**Criterio de salida:** Saldo nunca negativo ni con dos abonos simultáneos (bloqueo de fila, HT-07); envío repetido no duplica; historial inmutable

### Tareas específicas (del criterio de salida, los hallazgos y el plan)

- [ ] Saldo nunca negativo ni con dos abonos simultáneos: bloqueo de fila (HT-07) (criterio de salida)
- [ ] Envío repetido de un abono no duplica el movimiento (CA-52) (criterio de salida)
- [ ] Historial inmutable: el rol de la aplicación es rechazado en `UPDATE` y `DELETE` sobre movimientos (criterio de salida; ADR-027)

### Requisitos funcionales

- [ ] **RF-13** — Registrar pago completo
- [ ] **RF-15** — Consultar historial
- [ ] **RF-16** — Anular movimiento
- [ ] **RF-29** — Definir depósito de garantía
- [ ] **RF-30** — Registrar abonos al depósito
- [ ] **RF-31** — Calcular saldo del depósito
- [ ] **RF-32** — Consultar historial del depósito
- [ ] **RF-34** — Registrar abono de alquiler
- [ ] **RF-35** — Calcular saldo de alquiler
- [ ] **RF-38** — Registrar pago en moneda distinta
- [ ] **RF-47** — Anotar el número del recibo físico

### Criterios de aceptación (con la prioridad de la estrategia de pruebas)

- [ ] **CA-04** — Registro de pago completo · prioridad Alta
- [ ] **CA-15** — Abonos al depósito · prioridad Media
- [ ] **CA-16** — Completar depósito · prioridad Media
- [ ] **CA-17** — Separación entre alquiler y depósito · prioridad Media
- [ ] **CA-19** — Abono parcial · prioridad Alta
- [ ] **CA-20** — Completar con abonos · prioridad Alta
- [ ] **CA-21** — Fecha retroactiva · prioridad Alta
- [ ] **CA-23** — Excepción de abonos · prioridad Media
- [ ] **CA-33** — Fecha no válida · prioridad Alta
- [ ] **CA-34** — Anulación de movimiento · prioridad Alta
- [ ] **CA-35** — Anulación de obligación · prioridad Alta
- [ ] **CA-38** — Pago en moneda distinta de la del contrato · prioridad Alta
- [ ] **CA-45** — Depósito mayor a una mensualidad · prioridad Media
- [ ] **CA-46** — Depósito de contrato cerrado · prioridad Media
- [ ] **CA-52** — Envío repetido de un abono · prioridad Alta
- [ ] **CA-58** — Movimientos sobre períodos futuros (RN-15, segunda mitad) · prioridad Alta · (L) legal sin validar
- [ ] **CA-61** — Número de recibo físico (RF-47) · prioridad Media

### Cierre

- [ ] 1. Pruebas de los CA asignados en la integración continua con PostgreSQL 18; ninguna Alta sin escribir (EPP, sección 11)
- [ ] 2. Integración continua en verde: pruebas, `check --deploy` y migraciones desde cero (ADR-025)
- [ ] 3. `verificar_coherencia.ps1` sin problemas
- [ ] 4. Tablas y secuencias nuevas en el archivo de privilegios, con su prueba (ADR-027, ADR-031)
- [ ] 5. Código sin cubrir de los módulos críticos revisado, sin umbral numérico (EPP, sección 9)
- [ ] 6. Desplegada en la etapa A (WSL 2 con Ubuntu-26.04) con datos ficticios y criterio de salida propio cumplido
- [ ] 7. Ningún dato personal ni secreto en los registros ni en la auditoría (RF-28, RNF-06, R14)
- [ ] 8. `CAMBIOS.md` de la entrega y trazabilidad (RF, CA, ADR) al día
- [ ] 9. Ningún defecto conocido de prioridad Alta abierto
- [ ] Actualizar `AVANCE_IMPLEMENTACION.md`
- [ ] Tareas agregadas durante la entrega (*Propuesta*; preguntar antes): —


---

## E4 Notificaciones y cuenta
**Aplicaciones:** notificaciones, cuentas · **Estado:** no iniciada (requiere autorización expresa del solicitante)
**Contenido (plan):** Notificación web y por correo, recordatorios, resumen diario de atraso, reintentos cada minuto, avisos de seguridad, cambio y restablecimiento de contraseña, cambio de una dirección de correo, vigilancia del proceso diario y del respaldo diario
**Criterio de salida:** Correo simulado que falla no bloquea nada; avisos a dos direcciones; enlace de un solo uso y 15 minutos con sus protecciones

### Tareas específicas (del criterio de salida, los hallazgos y el plan)

- [ ] Correo simulado que falla no bloquea nada (criterio de salida; RNF-05, CA-09)
- [ ] Avisos de seguridad a las dos direcciones, con el contenido de ADR-026 y sin códigos ni enlaces de acceso (criterio de salida)
- [ ] Envío por correo de los avisos que la E0 solo registra y muestra como alerta (CA-68, CA-69; HI-01, HI-05)
- [ ] CA-47 completo, con su aviso (HI-02)
- [ ] Enlace de restablecimiento de un solo uso y 15 minutos, con sus protecciones (criterio de salida; CA-59)
- [ ] Vigilancia del proceso diario y del respaldo (HI-06; CA-72, CA-79)

### Requisitos funcionales

- [ ] **RF-21** — Configurar recordatorios anticipados
- [ ] **RF-22** — Generar alertas diarias de atraso
- [ ] **RF-23** — Notificar por canales aprobados
- [ ] **RF-24** — Registrar intentos de notificación
- [ ] **RF-25** — Cancelar notificaciones futuras
- [ ] **RF-44** — Minimizar datos en mensajes externos
- [ ] **RF-49** — Vigilar el proceso diario
- [ ] **RF-53** — Vigilar el respaldo diario

### Requisitos no funcionales

- [ ] **RNF-05** — Confiabilidad

### Criterios de aceptación (con la prioridad de la estrategia de pruebas)

- [ ] **CA-05** — Alerta diaria y resumen · prioridad Media
- [ ] **CA-08** — Recordatorio configurable · prioridad Media
- [ ] **CA-09** — Fallo del envío de correo · prioridad Media
- [ ] **CA-41** — Cambio de anticipación · prioridad Media
- [ ] **CA-42** — Proceso omitido · prioridad Media
- [ ] **CA-43** — Contenido mínimo · prioridad Media
- [ ] **CA-44** — Abono sin notificación individual · prioridad Media
- [ ] **CA-47** — Recuperación de acceso · prioridad Alta
- [ ] **CA-59** — Restablecer la contraseña olvidada (RF-27) · prioridad Alta
- [ ] **CA-60** — Fallo del aviso de seguridad (RF-27) · prioridad Alta · (L) legal sin validar
- [ ] **CA-64** — Cambiar una dirección de correo (RF-27) · prioridad Alta
- [ ] **CA-72** — Alerta de proceso diario omitido o fallido (RF-49) · prioridad Media
- [ ] **CA-79** — Alerta de respaldo omitido o fallido (RF-53) · prioridad Media

### Cierre

- [ ] 1. Pruebas de los CA asignados en la integración continua con PostgreSQL 18; ninguna Alta sin escribir (EPP, sección 11)
- [ ] 2. Integración continua en verde: pruebas, `check --deploy` y migraciones desde cero (ADR-025)
- [ ] 3. `verificar_coherencia.ps1` sin problemas
- [ ] 4. Tablas y secuencias nuevas en el archivo de privilegios, con su prueba (ADR-027, ADR-031)
- [ ] 5. Código sin cubrir de los módulos críticos revisado, sin umbral numérico (EPP, sección 9)
- [ ] 6. Desplegada en la etapa A (WSL 2 con Ubuntu-26.04) con datos ficticios y criterio de salida propio cumplido
- [ ] 7. Ningún dato personal ni secreto en los registros ni en la auditoría (RF-28, RNF-06, R14)
- [ ] 8. `CAMBIOS.md` de la entrega y trazabilidad (RF, CA, ADR) al día
- [ ] 9. Ningún defecto conocido de prioridad Alta abierto
- [ ] Actualizar `AVANCE_IMPLEMENTACION.md`
- [ ] Tareas agregadas durante la entrega (*Propuesta*; preguntar antes): —


---

## E5 Calendario y privacidad
**Aplicaciones:** alquileres, privacidad · **Estado:** no iniciada (requiere autorización expresa del solicitante)
**Contenido (plan):** Calendario mensual y filtros, solicitudes del titular y su exportación, desasociación a petición, revocación de consentimiento, retención (también de quien no tiene contrato), incidentes de seguridad y su constancia, preparación de la carga inicial por digitación con conciliación (sección 5)
**Criterio de salida:** Exportación con todo el registro y su auditoría; retención con aviso previo; plazo de cinco días hábiles

### Tareas específicas (del criterio de salida, los hallazgos y el plan)

- [ ] Exportación con todo el registro y su auditoría (criterio de salida; CA-27)
- [ ] Retención con aviso previo (criterio de salida; CA-28, CA-66)
- [ ] Plazo de cinco días hábiles (criterio de salida; CA-27, CA-56)
- [ ] Preparar la carga inicial por digitación con conciliación (plan, sección 5)

### Requisitos funcionales

- [ ] **RF-17** — Mostrar calendario mensual
- [ ] **RF-18** — Filtrar por inquilino o por propiedad
- [ ] **RF-19** — Filtrar por estado
- [ ] **RF-20** — Consultar detalle de evento
- [ ] **RF-40** — Atender solicitudes del titular
- [ ] **RF-41** — Retener y eliminar datos personales
- [ ] **RF-46** — Gestionar incidentes de seguridad

### Requisitos no funcionales

- [ ] **RNF-13** — Protección de datos

### Criterios de aceptación (con la prioridad de la estrategia de pruebas)

- [ ] **CA-06** — Calendario general · prioridad Baja
- [ ] **CA-07** — Filtro por inquilino · prioridad Baja
- [ ] **CA-27** — Solicitud del titular · prioridad Alta · (L) legal sin validar
- [ ] **CA-28** — Retención · prioridad Alta · (L) legal sin validar
- [ ] **CA-56** — Plazo de aviso de un incidente · prioridad Alta · (L) legal sin validar
- [ ] **CA-57** — Constancia de avisos de un incidente · prioridad Alta · (L) legal sin validar
- [ ] **CA-65** — Desasociar a petición del titular (RF-40) · prioridad Alta · (L) legal sin validar
- [ ] **CA-66** — Retención sin contrato (RF-41) · prioridad Alta · (L) legal sin validar

### Cierre

- [ ] 1. Pruebas de los CA asignados en la integración continua con PostgreSQL 18; ninguna Alta sin escribir (EPP, sección 11)
- [ ] 2. Integración continua en verde: pruebas, `check --deploy` y migraciones desde cero (ADR-025)
- [ ] 3. `verificar_coherencia.ps1` sin problemas
- [ ] 4. Tablas y secuencias nuevas en el archivo de privilegios, con su prueba (ADR-027, ADR-031)
- [ ] 5. Código sin cubrir de los módulos críticos revisado, sin umbral numérico (EPP, sección 9)
- [ ] 6. Desplegada en la etapa A (WSL 2 con Ubuntu-26.04) con datos ficticios y criterio de salida propio cumplido
- [ ] 7. Ningún dato personal ni secreto en los registros ni en la auditoría (RF-28, RNF-06, R14)
- [ ] 8. `CAMBIOS.md` de la entrega y trazabilidad (RF, CA, ADR) al día
- [ ] 9. Ningún defecto conocido de prioridad Alta abierto
- [ ] Actualizar `AVANCE_IMPLEMENTACION.md`
- [ ] Tareas agregadas durante la entrega (*Propuesta*; preguntar antes): —


---

## E6 Etapa B y salida
**Aplicaciones:** todas · **Estado:** no iniciada (requiere autorización expresa del solicitante)
**Contenido (plan):** Contratar los servicios (dominio, Droplet de pruebas, Spaces, Resend), endurecimiento del servidor real, HTTPS con Certbot, restauración desde Spaces, entregabilidad del correo, prueba de carga, restauración mensual y trimestral, registro de cuentas externas con segundo factor, autenticación del correo (DMARC), documento de seguridad, ensayo de salida y paso a producción
**Criterio de salida:** Percentil 95 menor de 2 s con 50 propiedades en el Droplet de pruebas; restauración desde Spaces medida frente al RTO; correo entregado en una cuenta real; revisión de código sin cubrir de los módulos críticos

### Tareas específicas (del criterio de salida, los hallazgos y el plan)

- [ ] Percentil 95 menor de 2 s con 50 propiedades en el Droplet de pruebas (criterio de salida; RNF-08); si no cumple, pasar al plan de 2 vCPU y 2 GiB
- [ ] Restauración desde Spaces medida frente al RTO de 24 h (criterio de salida; RNF-09)
- [ ] Correo entregado en una cuenta real (criterio de salida; RNF-20)
- [ ] Revisión del código sin cubrir de los módulos críticos (criterio de salida)
- [ ] Contratar los servicios: dominio, Droplet de pruebas, Spaces y Resend; reconfirmar precios al contratar (plan, sección 5.1)
- [ ] HTTPS con Certbot y `certbot renew --dry-run` (EPP, sección 7)
- [ ] Prueba de la restauración mensual automática y de la trimestral manual, con registro en la fase 6 (EPP; ADR-024)
- [ ] Registro de cuentas externas con segundo factor (RNF-19, CA-80) y autenticación del correo con DMARC (RNF-20, CA-81)
- [ ] Documento de seguridad (RNF-18), ensayo de salida y paso a producción
- [ ] Auditoría del servidor con Lynis (ADR-032, pendiente)

### Requisitos funcionales

- (ninguno)

### Requisitos no funcionales

- [ ] **RNF-07** — Usabilidad
- [ ] **RNF-08** — Rendimiento
- [ ] **RNF-10** — Compatibilidad
- [ ] **RNF-11** — Mantenibilidad
- [ ] **RNF-18** — Documentación de seguridad
- [ ] **RNF-19** — Protección de las cuentas de servicios externos
- [ ] **RNF-20** — Autenticación del correo saliente

### Criterios de aceptación (con la prioridad de la estrategia de pruebas)

- [ ] **CA-80** — Registro de cuentas externas (RNF-19) · prioridad Media
- [ ] **CA-81** — Correo autenticado (RNF-20) · prioridad Alta

### Endurecimiento del servidor real (ADR-032, 18 decisiones)

- [ ] 1. Acceso remoto por SSH: solo llave ed25519 con passphrase, sin contraseña ni `root` directo, usuario administrador distinto del de la aplicación, `sshd -t` antes de reiniciar
- [ ] 2. Firewall: Cloud Firewall y UFW; puerto 22 limitado a la IP del solicitante; 80 y 443 abiertos; sin IPv6
- [ ] 3. Actualizaciones: `unattended-upgrades`, reinicio a las 04:00 de Costa Rica, correo solo si hay error
- [ ] 4. Servicios y systemd: usuarios de sistema estáticos, `NoNewPrivileges`, `ProtectSystem=strict`, sin `DynamicUser`
- [ ] 5. HTTPS y cabeceras: DNS only, Certbot, TLS 1.3 y 1.2, HSTS por etapas
- [ ] 6. Secretos en `/etc/sga/` (0640, root y grupo de la aplicación), fuera del repositorio; rotación anual
- [ ] 7. Cuentas de proveedores y de correo: mejor segundo factor disponible, dos factores y códigos fuera del dispositivo
- [ ] 8. Autenticación del correo: subdominio dedicado, SPF, DKIM y DMARC (`p=none` y luego `p=reject`)
- [ ] 9. Respaldos: `age` a clave pública, un archivo por día, clave privada en dos copias fuera de línea, copia mensual
- [ ] 10. Dependencias de Python: versiones fijadas, `pip-audit` en la integración continua, plazos de 3 y 14 días
- [ ] 11. Límite de solicitudes en Nginx (`limit_req`) y riesgo aceptado
- [ ] 12. PostgreSQL solo por socket Unix, `pg_hba.conf` con `peer`, privilegios revocados a `PUBLIC`
- [ ] 13. Gunicorn y Nginx: `gunicorn.socket`, 3 workers `sync`, `timeout` de 30 s
- [ ] 14. Salida de los firewalls denegada por defecto y permitida por puerto
- [ ] 15. Respaldo diario a las 05:00 de Costa Rica, con marca de último respaldo correcto y aviso de fallo
- [ ] 16. Cifrados TLS, CAA y CSP
- [ ] 17. Registros de Nginx con formato propio sin cadena de consulta; Gunicorn sin registro de acceso; rotación de 14 días
- [ ] 18. Procedimiento del dispositivo del administrador y de la llave SSH (fase 6)

### Cierre

- [ ] 1. Pruebas de los CA asignados en la integración continua con PostgreSQL 18; ninguna Alta sin escribir (EPP, sección 11)
- [ ] 2. Integración continua en verde: pruebas, `check --deploy` y migraciones desde cero (ADR-025)
- [ ] 3. `verificar_coherencia.ps1` sin problemas
- [ ] 4. Tablas y secuencias nuevas en el archivo de privilegios, con su prueba (ADR-027, ADR-031)
- [ ] 5. Código sin cubrir de los módulos críticos revisado, sin umbral numérico (EPP, sección 9)
- [ ] 6. Desplegada en la etapa A (WSL 2 con Ubuntu-26.04) con datos ficticios y criterio de salida propio cumplido
- [ ] 7. Ningún dato personal ni secreto en los registros ni en la auditoría (RF-28, RNF-06, R14)
- [ ] 8. `CAMBIOS.md` de la entrega y trazabilidad (RF, CA, ADR) al día
- [ ] 9. Ningún defecto conocido de prioridad Alta abierto
- [ ] Actualizar `AVANCE_IMPLEMENTACION.md`
- [ ] Tareas agregadas durante la entrega (*Propuesta*; preguntar antes): —


---

## Posterior — fuera de la v1
Comprobante numerado generado por el sistema (fase posterior por decisión del 21-oct-2026)

- [ ] **RF-37** — Emitir comprobante de pago
- [ ] **CA-37** — Comprobantes consecutivos (fase posterior, RF-37; no aplica a la v1) · prioridad Alta · (L) legal sin validar
- [ ] **CA-54** — Comprobantes sin huecos (fase posterior, RF-37; no aplica a la v1) · prioridad Alta

---

## Antes de cargar datos reales (plan, sección 4)
- [ ] Servidor endurecido (ADR-032; guía y Lynis pendientes)
- [ ] Una prueba de restauración superada
- [ ] Revisión legal cerrada: DP-17 a DP-21 y DP-31 (consulta sobre Resend y DigitalOcean) abiertos; **sin dictamen escrito**
- [ ] Dominio comprado y servicio de correo verificado (entregabilidad, términos y DNS)
- [ ] Aprobación formal de la ERS y del DAS
- [ ] Revisión por una persona distinta de lo crítico, con la lista LRC-SGA-001 y sus hallazgos resueltos (plan 3.3); **persona sin designar**

## Carga inicial de datos (plan, sección 5; después de la E5 y de lo anterior)
- [ ] Origen: registros actuales preparados fuera del sistema y del repositorio (formato y ubicación pendientes)
- [ ] Al menos dos ensayos con datos ficticios en el entorno de pruebas, con una reversión
- [ ] Carga real digitada por las pantallas, con el consentimiento registrado y la cédula subida (RF-39)
- [ ] Conciliación de inquilinos, propiedades, contratos y saldos de apertura contra el origen; toda diferencia se investiga
- [ ] Respaldo completo inmediatamente antes de la carga
- [ ] Constancia de la carga en el repositorio, sin datos personales

## Fase 6 (despliegue y operación; DAS)
- [ ] Procedimiento del dispositivo del administrador y de la llave SSH (ADR-032 d18)
- [ ] Registro de cuentas externas (RNF-19, CA-80)
- [ ] Procedimiento ante un aviso de seguridad inesperado, y de respuesta a incidentes con aviso en cinco días hábiles (OL-19)
- [ ] Documento de seguridad y protocolo de actuación (OL-20, OL-21; RNF-18)
- [ ] Rotación y retención de los registros de journald, de auditoría y de PostgreSQL (ADR-032, pendiente)
- [ ] Monitoreo externo del servidor

## Puntos por decidir que surgieron al armar esta lista
1. **Reemplazo del segundo factor con la sesión iniciada** (RF-27, exige la contraseña actual): el plan no lo asigna a ninguna entrega. Propuesta del asistente: E4, junto al cambio de contraseña. La pantalla para emitir códigos nuevos (CA-69) sí está en la E0 porque CA-69 se asigna a ella.
2. **Orden dentro de la E0:** el plan no lo fija. Propuesta: terminar B (avisos y rescate), luego C (auditoría) porque B depende de ella, después D, E, y dejar F, G y H para cuando WSL esté instalado.
3. **Python 3.14 en WSL:** todo el código se probó con Python 3.12 en Windows; hasta repetirlo en WSL ninguna tarea de la E0 debería darse por terminada.
