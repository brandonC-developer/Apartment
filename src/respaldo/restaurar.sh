#!/usr/bin/env bash
# Restauración de un respaldo cifrado del SGA (ADR-024, RNF-09). Sirve para la prueba trimestral y,
# con otro destino, para recuperar el servicio.
#
#   restaurar.sh --fecha AAAA-MM-DD --clave-privada ARCHIVO --base-destino NOMBRE \
#                [--documentos-destino CARPETA] [--origen CARPETA] [--solo-verificar]
#
# - Comprueba las sumas de los tres archivos y que se descifran con la clave privada.
# - Restaura en una base NUEVA: se niega si ya existe y, si algo falla, la borra. Nunca pisa una base.
# - Restaura los documentos en una carpeta VACÍA, si se indica.
# - `--solo-verificar` descifra y lista el contenido sin crear nada (comprobación automática mensual).
# - Se restaura sin propietarios ni privilegios (`--no-owner --no-acl`): después, como rol dueño,
#   `manage.py aplicar_privilegios` los vuelve a conceder (ADR-031, decisión 3).
# La clave privada la entrega quien restaura, desde su copia fuera de línea; no vive en el servidor.
set -euo pipefail
umask 077

ORIGEN="${SGA_RESPALDO_DESTINO:-/var/lib/sga/respaldos}"
AGE="${SGA_AGE:-age}"
FECHA="" CLAVE="" BASE="" DOCS="" SOLO_VERIFICAR=0

fallar() { echo "restauración: $*" >&2; exit 1; }

while [ $# -gt 0 ]; do
  case "$1" in
    --fecha) FECHA="${2:-}"; shift 2 ;;
    --clave-privada) CLAVE="${2:-}"; shift 2 ;;
    --base-destino) BASE="${2:-}"; shift 2 ;;
    --documentos-destino) DOCS="${2:-}"; shift 2 ;;
    --origen) ORIGEN="${2:-}"; shift 2 ;;
    --solo-verificar) SOLO_VERIFICAR=1; shift ;;
    *) fallar "argumento desconocido: $1" ;;
  esac
done

[[ "$FECHA" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || fallar "indique --fecha AAAA-MM-DD"
[ -r "$CLAVE" ] || fallar "indique --clave-privada con un archivo legible"
grep -q 'AGE-SECRET-KEY' "$CLAVE" || fallar "el archivo no contiene una clave privada de age"
command -v "$AGE" >/dev/null 2>&1 || fallar "no se encuentra el programa age ($AGE)"
if [ "$SOLO_VERIFICAR" -eq 0 ]; then
  [ -n "$BASE" ] || fallar "indique --base-destino (o --solo-verificar)"
  [[ "$BASE" =~ ^[A-Za-z0-9_]+$ ]] || fallar "el nombre de la base solo admite letras, números y _"
fi

PARTES=("${FECHA}_base.dump.age" "${FECHA}_globales.sql.age" "${FECHA}_documentos.tar.age")
for parte in "${PARTES[@]}" "${FECHA}.sha256"; do
  [ -r "$ORIGEN/$parte" ] || fallar "falta $ORIGEN/$parte"
done

# 1) Integridad: las sumas deben coincidir.
( cd "$ORIGEN" && sha256sum --check --quiet "${FECHA}.sha256" ) || fallar "las sumas de comprobación no coinciden: archivo alterado o dañado"
echo "restauración: sumas correctas"

descifrar() { "$AGE" --decrypt -i "$CLAVE" "$ORIGEN/$1"; }

# 2) Se descifra todo y se comprueba que tiene la forma esperada, sin crear nada.
descifrar "${FECHA}_base.dump.age" | pg_restore --list > /dev/null || fallar "la base no se descifra o no es un volcado válido (¿clave equivocada?)"
descifrar "${FECHA}_globales.sql.age" > /dev/null || fallar "los roles no se descifran"
descifrar "${FECHA}_documentos.tar.age" | tar -tf - > /dev/null || fallar "los documentos no se descifran o no son un tar válido"
echo "restauración: las tres partes se descifran y son válidas"
if [ "$SOLO_VERIFICAR" -eq 1 ]; then exit 0; fi

# 3) Base nueva. Si algo falla desde aquí, se borra para no dejar una restauración a medias.
existe="$(psql -X -tA -d postgres -c "SELECT 1 FROM pg_database WHERE datname = '$BASE'")"
[ -z "$existe" ] || fallar "la base $BASE ya existe: no se pisa. Use otro nombre o bórrela a mano"
if [ -n "$DOCS" ]; then
  mkdir -p "$DOCS"
  [ -z "$(ls -A "$DOCS")" ] || fallar "la carpeta de documentos $DOCS no está vacía"
fi

createdb "$BASE"
TERMINADA=0
limpiar() {
  if [ "$TERMINADA" -ne 1 ]; then
    echo "restauración: falló, se borra la base $BASE" >&2
    dropdb --if-exists "$BASE" || true
  fi
}
trap limpiar EXIT
descifrar "${FECHA}_base.dump.age" | pg_restore --no-owner --no-acl --exit-on-error --dbname="$BASE"
if [ -n "$DOCS" ]; then
  descifrar "${FECHA}_documentos.tar.age" | tar -x -C "$DOCS"
fi

# 4) Consultas de cordura: la restauración debe traer lo mínimo de una instalación.
migraciones="$(psql -X -tA -d "$BASE" -c 'SELECT count(*) FROM django_migrations')"
[ "$migraciones" -gt 0 ] || fallar "la base restaurada no tiene migraciones aplicadas"
organizacion="$(psql -X -tA -d "$BASE" -c 'SELECT count(*) FROM nucleo_organizacion')"
[ "$organizacion" -eq 1 ] || fallar "la base restaurada debería tener una sola fila de organización"
TERMINADA=1
echo "restauración: base $BASE restaurada (migraciones: $migraciones, organización: $organizacion)"
echo "restauración: ahora, como rol dueño: manage.py aplicar_privilegios"
