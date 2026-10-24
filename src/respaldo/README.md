# Respaldo cifrado y restauración

Implementa el ADR-024 y las decisiones 9 y 15 del ADR-032 en la etapa A (destino local, sin Spaces).
Todo lo que sigue es lo que hace el código; lo marcado **Propuesta** no está decidido.

## Qué hace `respaldar.sh`
Cada día genera, en `SGA_RESPALDO_DESTINO` (por defecto `/var/lib/sga/respaldos`), cuatro archivos:

| Archivo | Contenido |
|---|---|
| `AAAA-MM-DD_base.dump.age` | `pg_dump` en formato personalizado |
| `AAAA-MM-DD_globales.sql.age` | `pg_dumpall --globals-only --no-role-passwords` |
| `AAAA-MM-DD_documentos.tar.age` | La carpeta de documentos privados (`SGA_DOCUMENTOS`) |
| `AAAA-MM-DD.sha256` | Sumas de los tres archivos |

Cada parte pasa por una tubería directamente a `age -R <clave pública>`: nada se escribe en claro en el disco. La marca `ultimo_respaldo_correcto` (instante UTC) se escribe **al final** y solo si todo salió bien; la vigilancia de RF-53 (E4) comparará su antigüedad con 26 horas. Retención: en la etapa A, 35 días con `find` (DP-07); en la etapa B la aplica la regla de ciclo de vida de Spaces.

## Claves (procedimiento propuesto)
1. **En tu equipo, nunca en el servidor:** `age-keygen -o respaldo_privada.txt` (imprime la clave pública).
2. Copia **solo la clave pública** (`age1...`) a `/etc/sga/respaldo_clave_publica.txt` del servidor (`age-keygen -y respaldo_privada.txt`). El script se niega a respaldar si ese archivo contiene la privada.
3. Guarda `respaldo_privada.txt` en **dos lugares independientes y fuera de línea** (ADR-032 d9). Nadie más sabe dónde están (DP-23): es un riesgo asumido mientras el solicitante ocupa los tres roles.
4. Prueba la restauración con esa copia cada trimestre.

**Propuesta, sobre la clave Fernet** de `/etc/sga/clave_cifrado` (el secreto del segundo factor): no va en el respaldo ni necesita copia. Si se pierde, el secreto TOTP guardado no se puede descifrar y se resuelve con `rescatar_segundo_factor`, que obliga a registrar el segundo factor de nuevo. Cuesta una molestia, no datos del negocio. Decide si prefieres guardarla también fuera de línea.

## Restaurar
```
restaurar.sh --fecha AAAA-MM-DD --clave-privada respaldo_privada.txt --base-destino sga_restaurada \
             --documentos-destino /ruta/vacia
restaurar.sh --fecha AAAA-MM-DD --clave-privada respaldo_privada.txt --solo-verificar
```
Comprueba las sumas, descifra las tres partes, restaura en una base **nueva** (se niega si existe y, si falla, la borra) y en una carpeta **vacía**, y hace consultas de cordura (migraciones aplicadas y una sola fila de organización). Restaura sin propietarios ni privilegios: después, como rol dueño, `manage.py aplicar_privilegios`. `--solo-verificar` no crea nada y sirve para la comprobación mensual automática (E6).

## Pruebas
`nucleo/tests_respaldo.py` ejecuta los dos scripts de verdad. Necesita `bash`, `age`, `age-keygen`, `pg_dump`/`pg_restore` de **la misma versión mayor que el servidor**, `tar` y un usuario que pueda crear bases; si falta algo, se omiten con el motivo. En Windows hace falta Git Bash (no el lanzador de WSL) y `SGA_AGE` apuntando a `age.exe`.

## Lo que falta
- Subida a Spaces antes de escribir la marca, llave limitada a un bucket, versionado y copia mensual (E6, etapa B).
- Probar las unidades de `systemd/` en WSL (borradores) y la autenticación `peer` del rol de respaldos.
- La comprobación mensual automática y el registro trimestral en la fase 6.
- Medir el tiempo de restauración frente al RTO de 24 h con datos reales.
