# Código del SGA — entrega E0 (esqueleto)

**Estado:** esqueleto del proyecto Django; **sin modelos, migraciones ni pantallas**. La E0 está *en curso* ([registro de avance](../DOC/fase-5-implementacion/AVANCE_IMPLEMENTACION.md)). Nada de lo que hay aquí está aprobado ni probado en el entorno de destino.

## Qué hay
| Ruta | Contenido |
|---|---|
| `sga/settings.py` | Configuración: secretos fuera del repositorio, PostgreSQL por socket, Argon2id, contraseñas de 15 caracteres, sesión de 24 h, cookies seguras si no hay `SGA_DEBUG` |
| `nucleo/`, `cuentas/` | Aplicaciones de la E0 (ADR-030), vacías salvo las pruebas de `nucleo` |
| `requirements.txt` | Versiones fijadas |
| `.env.ejemplo` | Variables de entorno de ejemplo |

## Entorno de desarrollo actual y su límite
Se creó con **Python 3.12 en Windows** (`py -3.12 -m venv .venv`) porque la distribución `Ubuntu-26.04` de WSL **aún no está instalada** y el plan pide Python 3.14 en ella (DOC/fase-5, secciones 5.1 y 5.2). Es una desviación del plan: todo debe volver a probarse en WSL, y las versiones de `requirements.txt` deben volver a fijarse allí.

## Pruebas
```
cd src
$env:SGA_DEBUG = "1"
.venv\Scripts\python manage.py test nucleo
```
Las pruebas de `nucleo` no usan la base de datos y las de `cuentas` sí (necesitan PostgreSQL; ver más abajo): comprueban Argon2id, el mínimo de 15 caracteres, la zona horaria, la ausencia del administrador de Django y que el proyecto no arranque sin `SECRET_KEY`. `manage.py check --deploy` solo avisa de HSTS, que se activa por etapas en la etapa B (ADR-032, decisión 5).

## Qué falta de la E0
Aviso por correo, auditoría, organización y configuración regional, roles de PostgreSQL y archivo de privilegios (ADR-027, 031), despliegue en WSL, HTTPS autofirmado, respaldo cifrado y su restauración, e integración continua.

## `cuentas.Administrador` (actualización zzc)
Modelo, cifrado del secreto del segundo factor (Fernet), TOTP con pyotp y límite de intentos, con 26 pruebas que necesitan PostgreSQL. Para correrlas hace falta un servidor PostgreSQL accesible y las variables `SGA_BD_HOST`, `SGA_BD_PUERTO` y `SGA_BD_USUARIO`; el usuario debe poder crear bases (el ejecutor crea `test_sga`). No existe todavía la vista de inicio de sesión, y **una vista que llame a `login()` tras `authenticate()` sin pedir el TOTP saltaría el segundo factor**.

## Códigos de recuperación (actualización zzd)
`CodigoRecuperacion`, `emitir_codigos_recuperacion` y `verificar_codigo_recuperacion` en `cuentas/autenticacion.py`; 38 pruebas en total. Aún sin vista que los use.

## Inicio de sesión (actualización 2026-10-24)
Rutas `/entrar/`, `/entrar/codigo/`, `/salir/` y `/` (página provisional protegida), con el middleware `LimiteDeSesion` (24 h / 1 h). 51 pruebas en total. La cuenta se crea con `crear_administrador`.

## Comandos de gestión (actualización 2026-10-24a)
`python manage.py crear_administrador --usuario X` y `python manage.py rescatar_segundo_factor`. 56 pruebas en total. Una cuenta recién creada registra su segundo factor en el primer ingreso (actualización 2026-10-24b, 64 pruebas), sin código QR.

## Token de registro del segundo factor (actualización 2026-10-24d)
`crear_administrador` y `rescatar_segundo_factor` imprimen un token de un solo uso (24 h) que la pantalla de registro pide antes de mostrar la clave. 78 pruebas en total.

## Auditoría base (actualización 2026-10-24e)
`nucleo.Auditoria` (solo inserción), `nucleo.auditoria.registrar` y la pantalla `/auditoria/`; los eventos de autenticación y de la cuenta se registran con la IP de origen. Detrás de Nginx hace falta `proxy_set_header X-Forwarded-For $remote_addr;`, que sustituye la del cliente (la configuración lee `X-Forwarded-For` cuando no es depuración; así lo corrigió la actualización 2026-10-24j). 100 pruebas en total.

## Organización y configuración regional (actualización 2026-10-24f)
`nucleo.Organizacion` (fila única), `nucleo/formato.py` (formato propio; en plantillas, `{% load formato %}`) y el middleware de la zona horaria. 121 pruebas en total.

## Roles y privilegios (actualización 2026-10-24g)
1. Una vez, como `postgres`: `psql -v ON_ERROR_STOP=1 -v rol_dueno=sga_dueno -v rol_app=sga_app -v rol_respaldos=sga_respaldos -v base=sga -f db/roles.sql`.
2. Tras cada despliegue, como rol dueño: `SGA_BD_USUARIO=sga_dueno python manage.py migrate` y `SGA_BD_USUARIO=sga_dueno python manage.py aplicar_privilegios`.
3. Gunicorn y los comandos diarios usan el rol `sga_app`. Toda tabla nueva necesita su entrada en `sga/privilegios.py`; una prueba lo exige. 140 pruebas en total (las de roles necesitan un usuario de conexión que pueda crear roles).

## Integración continua (actualización 2026-10-24h)
`.github/workflows/integracion-continua.yml` (en la raíz del repositorio). Pasos que puede repetir en local: `python manage.py makemigrations --check --dry-run`, `python manage.py test` y, sin `SGA_DEBUG`, `python manage.py check --deploy` con `SGA_SECRET_KEY` y `SGA_HOSTS_PERMITIDOS` definidos (solo debe quedar el aviso de HSTS). Nota: el aviso `security.W020` (ALLOWED_HOSTS vacío) también aparece sin `SGA_HOSTS_PERMITIDOS`; la afirmación anterior de este archivo de que solo avisaba de HSTS no incluía ese caso.

## Respaldo cifrado y restauración (actualización 2026-10-24i)
`respaldo/respaldar.sh`, `respaldo/restaurar.sh` y su guía en `respaldo/README.md`. 153 pruebas en total; las del respaldo exigen `age` y un `pg_dump` de la misma versión mayor que el servidor, y se omiten si falta algo.

## Despliegue en la etapa A: WSL (actualización 2026-10-24j)
La distribución se llama `Ubuntu` (Ubuntu 26.04.1). Todo se hace con archivos de `despliegue/`, como root dentro de WSL:
```
wsl -d Ubuntu -u root -- bash /mnt/e/Proyectos/Portafolio/Apartment/src/despliegue/desplegar.sh
wsl -d Ubuntu -u root -- bash /mnt/e/Proyectos/Portafolio/Apartment/src/despliegue/verificar.sh
wsl -d Ubuntu -u root -- bash /mnt/e/Proyectos/Portafolio/Apartment/src/despliegue/verificar_respaldo.sh
wsl -d Ubuntu -u root -- bash /mnt/e/Proyectos/Portafolio/Apartment/src/despliegue/probar.sh
```
`desplegar.sh` es idempotente y acepta `--clave-publica-respaldo ARCHIVO` y `--nombre-sitio NOMBRE`. El sitio queda en `https://localhost/` (certificado autofirmado: el navegador avisará). Para crear la cuenta: `runuser -u sga_app -- env $(grep -v "^#" /etc/sga/entorno | xargs) /opt/sga/venv/bin/python /opt/sga/src/manage.py crear_administrador --usuario NOMBRE`. Los scripts `verificar*.sh` borran los datos de prueba que crean; **no los ejecute sobre datos que quiera conservar**. 157 pruebas en total.

## Pendientes pequeños de la E0 (actualización 2026-10-24l)
Pantalla `/cuenta/codigos/` (códigos de recuperación nuevos), ajuste `RAIZ_DOCUMENTOS` para los documentos privados y migración de `btree_gist`. 181 pruebas en total. Toda vista nueva debe usar `login_required` o declararse pública en `cuentas/tests_cuenta.py`.

## Revisión del código sin cubrir (actualización 2026-10-24m)
Para medir la cobertura: instalar `coverage` en el entorno virtual (no está en `requirements.txt`) y `coverage run --branch --source=cuentas,nucleo,sga manage.py test`. 196 pruebas; los ajustes de `settings.py` se prueban en un proceso aparte, que `coverage` no mide.

## Decisiones del 24-oct-2026 (actualización 2026-10-24o)
- `python manage.py configurar_organizacion` muestra o cambia el responsable, la zona y la hora del proceso diario (sin pantalla web).
- Los códigos de recuperación se guardan con Argon2id y sal (`CODIGOS_ARGON2`); tras la migración `cuentas/0004` hay que emitir códigos nuevos desde `/cuenta/codigos/`.
- Colones: sin decimales si el importe es entero y con dos si tiene céntimos; dólares con dos.
- 211 pruebas en total.

## E1, grupo A: modelos de `inquilinos` (actualización 2026-10-24r)
Aplicación `inquilinos` (inquilino, texto y consentimiento, fotografía del documento y acceso a documentos). `nucleo.models.RegistroProtegido` es la base de las tablas que no se editan; toda tabla nueva necesita su entrada en `sga/privilegios.py`. 237 pruebas en total.

## E1, grupo B: servicios de inquilinos (actualización 2026-10-24s)
`inquilinos/services.py` (escribe), `selectors.py` (lee) y `bloqueos.py` (punto de extensión para el bloqueo de desactivar). Aún sin pantallas ni rutas. 273 pruebas en total.

## E1, grupo C: consentimiento (actualización 2026-10-24t)
Antes de usar el sistema con un inquilino: `python manage.py configurar_organizacion --nombre-responsable ... --direccion-responsable ...` y luego `python manage.py cargar_texto_consentimiento`. El texto es un **borrador sin validar por abogado**; el texto definitivo se carga con `--archivo ... --validado`. 297 pruebas en total.

## E1, grupo D: fotografías del documento (actualización 2026-10-24u)
Nueva dependencia: Pillow (13.0.0 desde la actualización 2026-10-26c; antes 12.3.0). Rutas: `POST /inquilinos/<id>/fotografias/<cara>/` (un archivo por petición), `GET /inquilinos/documentos/<id>/ver/` y `.../descargar/`. Los archivos van en `RAIZ_DOCUMENTOS/cedulas` y solo salen por esa vista. **Al editar scripts de shell desde Python en Windows, escribir con `newline='\n'`**: un CRLF no corre en Linux. 347 pruebas en total.

## E1, grupo E: reducción en el navegador (actualización 2026-10-24v)
El script `inquilinos/static/inquilinos/reducir_fotografia.js` se sirve con `collectstatic` (`SGA_ESTATICOS`, por defecto `/opt/sga/static`) y Nginx `/static/`. Pruebas del navegador: `pip install -r requirements-pruebas.txt` (Selenium); usan Chrome, Edge o Firefox y se omiten si no hay (`SGA_NAVEGADOR=chrome|edge|firefox` fuerza uno). 368 pruebas en Windows; 357 en WSL.

## E1, grupo F: pantallas (actualización 2026-10-24w)
Las pantallas están en `inquilinos/pantallas.py` y sus plantillas; sin estilos hasta los wireframes. Rutas: `/inquilinos/`, `/inquilinos/nuevo/`, `/inquilinos/<id>/` y, bajo ella, `editar/`, `desactivar/`, `reactivar/` y `consentimiento/revocar/`. Para registrar a alguien debe existir un texto de consentimiento cargado (`manage.py cargar_texto_consentimiento`). **Las pruebas que suben archivos deben usar una carpeta temporal en `RAIZ_DOCUMENTOS`** (como `Pantallas` y `Base`). 404 pruebas en Windows; 393 en WSL.

## E1, grupo G: medición de fotografías (actualización 2026-10-26a)
`cd src; .venv\Scripts\python despliegue\medir_reduccion.py CARPETA [--guardar SALIDA]` abre un navegador real, aplica el script de reducción a cada imagen de la carpeta e imprime peso, píxeles, calidad y metadatos (sin valores). Las fotos son datos personales: no las copie al repositorio; `img/` no está versionada.

## E2, grupo A: modelos de `alquileres` (actualización 2026-10-26g)
Aplicación `alquileres` (propiedades, contratos, condiciones, obligaciones, ajustes, fotografías del contrato, accesos y ejecuciones del proceso diario), sin servicios ni pantallas todavía. El solape de contratos (R2) es una restricción de exclusión de PostgreSQL y necesita la extensión `btree_gist` (migración de `nucleo`). Las pruebas de modelos corren contra las migraciones: para mutar una restricción hay que cambiar la migración. 467 pruebas en Windows; 456 en WSL.

## E2, grupo B: cálculo de períodos y prorrateo (actualización 2026-10-26h)
`alquileres/calculo.py` reúne las funciones puras de períodos, vencimientos, fecha límite, condición aplicable y prorrateo (RN-03, RN-05, RN-06, RN-12, RN-13). No usa la base ni el reloj: las fechas son `date` y los importes `Decimal` (un `float` se rechaza). El redondeo es siempre `ROUND_HALF_UP` y se hace una sola vez al final. 508 pruebas en Windows; 497 en WSL.

## E2, grupo C: propiedades y contratos (actualización 2026-10-26i)
`alquileres/services.py` (escritura), `selectors.py` (estados y consultas), `movimientos.py` (punto de extensión que la E3 reemplaza con `movimientos.usar(proveedor)`) y `bloqueos.py` (se registra en `inquilinos.bloqueos` al arrancar). Los errores de datos son `inquilinos.services.ErrorDeValidacion`. Las operaciones reciben `ahora` para poder probarlas con fechas fijas; el «hoy» sale de él en la zona horaria activa. 575 pruebas en Windows; 564 en WSL.
