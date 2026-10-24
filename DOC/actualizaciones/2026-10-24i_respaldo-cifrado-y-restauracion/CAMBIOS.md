# Actualización 2026-10-24 (i) — Respaldo cifrado y su restauración

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/respaldo/`](../../../src/respaldo/README.md), [`src/nucleo/tests_respaldo.py`](../../../src/nucleo/tests_respaldo.py), [`.github/workflows/integracion-continua.yml`](../../../.github/workflows/integracion-continua.yml), nuevo [`.gitattributes`](../../../.gitattributes), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** DAS v0.15, ADR-024 (respaldo diario cifrado), ADR-032 decisiones 9 y 15 (`age` a clave pública, un archivo por día, clave privada fuera del servidor, 05:00 y marca del último respaldo correcto), ADR-027 (rol de respaldos); ERS RNF-09 y RF-53; plan, sección 5.1 (etapa A: respaldos cifrados a una carpeta local) y criterio de salida de la E0 («una restauración completa probada desde el respaldo local»); instrucción del solicitante: «sí, escribe el respaldo cifrado y su restauración» (24-oct-2026)
**Estado:** implementado y probado con una base de pruebas; no aprobado

## 1. Qué se escribió
| Archivo | Contenido |
|---|---|
| `respaldo/respaldar.sh` | Genera por día `_base.dump.age`, `_globales.sql.age`, `_documentos.tar.age` y `.sha256`, cifrados con `age` a clave pública por tubería directa; se niega si falta la clave, si el archivo contiene una clave **privada** o si falta la carpeta de documentos; retención de 35 días; marca `ultimo_respaldo_correcto` al final |
| `respaldo/restaurar.sh` | Comprueba sumas, descifra las tres partes, restaura en una base **nueva** y en una carpeta **vacía** (no pisa nada; si falla, borra la base), consultas de cordura, `--solo-verificar` |
| `respaldo/systemd/` | Servicio y temporizador de las 05:00 hora de Costa Rica con `Persistent=true` y el endurecimiento de ADR-032 d4 — **borradores sin probar** |
| `respaldo/README.md` | Procedimiento de claves, de restauración y lo que falta |
| `nucleo/tests_respaldo.py` | 13 pruebas que ejecutan los scripts de verdad |
| `.gitattributes` | `*.sh` y `*.sql` con fin de línea LF (un script con CRLF no corre en Linux; el repositorio se trabaja en Windows con conversión automática) |
| Flujo de integración continua | Trabajo nuevo `respaldo` que instala el cliente 18 y `age` y exige que las pruebas no se omitan |

## 2. Propuestas del asistente (sin aprobar)
- **Retención con `find` en la etapa A** (35 días, DP-07): el ADR la asigna a la regla de ciclo de vida de Spaces; aquí se aplica local para no acumular.
- **Restauración sin propietarios ni privilegios** (`--no-owner --no-acl`) y luego `aplicar_privilegios`, coherente con ADR-031 decisión 3.
- **Consultas de cordura mínimas** (migraciones aplicadas y una fila de organización); se ampliarán con las entidades de cada entrega.
- **Repetir el respaldo el mismo día** sustituye el del día (un archivo por día).
- **Rutas** `/var/lib/sga/...` y `/opt/sga` de las unidades de systemd: el esquema de directorios del servidor no está decidido.
- **Clave Fernet fuera del respaldo** (ver el README de `respaldo/`): decisión tuya pendiente.

## 3. Verificación
- **153 pruebas pasan** (13 nuevas) contra PostgreSQL 18 desechable (ya borrado), Python 3.12 en Windows, `age` 1.3.2 y Git Bash. Se prueba: tres archivos con cabecera de `age`, sumas y marca; **nada en claro** (ni el contenido de un documento, ni un usuario de la base, ni la cabecera de `pg_dump`, ni `CREATE ROLE`); restauración de la base y de los documentos byte a byte; clave equivocada sin dejar base; archivo alterado detectado por su suma; no pisa una base ni una carpeta con contenido; `--solo-verificar`; fallo del respaldo sin tocar la marca ni dejar restos; negativa ante clave pública ausente o **privada** y carpeta ausente; retención solo de archivos de respaldo viejos; dos respaldos el mismo día; restauración que falla a medias borra la base; fallo en la última parte no deja marca ni archivos.
- **Mutaciones manuales:** no cifrar, no comprobar las sumas, no borrar la base fallida y escribir la marca antes de terminar hicieron fallar sus pruebas. Dos no fallaban al principio (la base fallida y la marca anticipada); se agregaron esas dos pruebas y entonces sí; se restauró el código.
- **Errores míos corregidos en el camino:** en Windows `bash` a secas desde Python se resuelve al lanzador de WSL (las pruebas usan la ruta completa y se omiten si es ese); `tar` toma `C:/x` como «equipo:ruta» (las pruebas convierten con `cygpath`; en Linux no ocurre); un `TransactionTestCase` vaciaba la fila de organización de las migraciones (`serialized_rollback`).
- **`pg_dump` y `pg_dumpall --globals-only --no-role-passwords` con el rol de respaldos** ya funcionaron sin ser superusuario (actualización 2026-10-24g).

## 4. Qué no se pudo comprobar
- El trabajo `respaldo` del flujo (el repositorio de PostgreSQL y el paquete `age` de Ubuntu en el ejecutor) **no se ha corrido**.
- Las unidades de systemd, la hora con zona dentro de `OnCalendar`, la autenticación `peer` del rol de respaldos y el tiempo de restauración con datos reales.
- La integridad del binario de `age` descargado para las pruebas: se tomó de las publicaciones oficiales y no se verificó su prueba de transparencia.

## 5. Qué no está hecho
Subida a Spaces antes de la marca, llave limitada, versionado y copia mensual (E6); vigilancia del respaldo, RF-53 (E4); comprobación mensual automática y registro trimestral (fase 6); WSL. 0 de 8 CA de la E0 cumplidos.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
