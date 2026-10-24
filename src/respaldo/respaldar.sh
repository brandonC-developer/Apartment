#!/usr/bin/env bash
# Respaldo diario cifrado del SGA (ADR-024; ADR-032, decisiones 9 y 15; RNF-09; RF-53).
#
# Un archivo cifrado por parte y por día, en el destino local de la etapa A:
#   AAAA-MM-DD_base.dump.age       pg_dump en formato personalizado
#   AAAA-MM-DD_globales.sql.age    pg_dumpall --globals-only --no-role-passwords
#   AAAA-MM-DD_documentos.tar.age  la carpeta de documentos privados
#   AAAA-MM-DD.sha256              sumas de comprobación de los tres
# El cifrado es `age` a clave pública: el servidor solo tiene la clave pública. Nada se escribe en
# claro en el disco: cada parte pasa por una tubería directamente al cifrado.
# La marca `ultimo_respaldo_correcto` se escribe solo al terminar todo; si algo falla, no se toca y
# el error sale con código distinto de cero (RF-53 vigila su antigüedad).
#
# Variables (todas con valor por defecto):
#   SGA_BD_NOMBRE, SGA_RESPALDO_DESTINO, SGA_RESPALDO_CLAVE_PUBLICA, SGA_DOCUMENTOS,
#   SGA_RESPALDO_RETENCION_DIAS (35, DP-07) y SGA_AGE (ruta del programa `age`).
# La conexión a PostgreSQL usa las variables PG* del entorno (en el servidor, el rol de respaldos
# por el socket Unix con autenticación peer, ADR-027).
set -euo pipefail
umask 077

BD="${SGA_BD_NOMBRE:-sga}"
DESTINO="${SGA_RESPALDO_DESTINO:-/var/lib/sga/respaldos}"
CLAVE_PUBLICA="${SGA_RESPALDO_CLAVE_PUBLICA:-/etc/sga/respaldo_clave_publica.txt}"
DOCUMENTOS="${SGA_DOCUMENTOS:-/var/lib/sga/documentos}"
RETENCION_DIAS="${SGA_RESPALDO_RETENCION_DIAS:-35}"
AGE="${SGA_AGE:-age}"

fallar() { echo "respaldo: $*" >&2; exit 1; }

command -v "$AGE" >/dev/null 2>&1 || fallar "no se encuentra el programa age ($AGE)"
[ -r "$CLAVE_PUBLICA" ] || fallar "no se puede leer la clave pública: $CLAVE_PUBLICA"
if grep -q 'AGE-SECRET-KEY' "$CLAVE_PUBLICA"; then
  fallar "el archivo contiene una clave PRIVADA: el servidor solo debe tener la pública"
fi
grep -q '^age1' "$CLAVE_PUBLICA" || fallar "el archivo de clave pública no contiene una clave age1..."
[ -d "$DOCUMENTOS" ] || fallar "no existe la carpeta de documentos: $DOCUMENTOS"
case "$RETENCION_DIAS" in ''|*[!0-9]*) fallar "SGA_RESPALDO_RETENCION_DIAS debe ser un entero" ;; esac

mkdir -p "$DESTINO"
FECHA="$(TZ=America/Costa_Rica date +%Y-%m-%d)"
TRABAJO="$(mktemp -d "$DESTINO/.en_curso.XXXXXX")"
trap 'rm -rf "$TRABAJO"' EXIT

cifrar() { "$AGE" -R "$CLAVE_PUBLICA" -o "$1"; }

pg_dump --format=custom --dbname="$BD" | cifrar "$TRABAJO/base.dump.age"
# --database: pg_dumpall conecta a esa base y no a template1, donde el rol de respaldos no tiene entrada en pg_hba.conf.
pg_dumpall --globals-only --no-role-passwords --database="$BD" | cifrar "$TRABAJO/globales.sql.age"
tar -C "$DOCUMENTOS" -cf - . | cifrar "$TRABAJO/documentos.tar.age"

# Cada parte debe existir, no estar vacía y empezar con la cabecera de age.
for parte in base.dump.age globales.sql.age documentos.tar.age; do
  [ -s "$TRABAJO/$parte" ] || fallar "la parte $parte quedó vacía"
  [ "$(head -c 21 "$TRABAJO/$parte")" = "age-encryption.org/v1" ] || fallar "la parte $parte no es un archivo age"
done

# Se publican los archivos con su nombre final y, al final, las sumas y la marca.
mv -f "$TRABAJO/base.dump.age" "$DESTINO/${FECHA}_base.dump.age"
mv -f "$TRABAJO/globales.sql.age" "$DESTINO/${FECHA}_globales.sql.age"
mv -f "$TRABAJO/documentos.tar.age" "$DESTINO/${FECHA}_documentos.tar.age"
( cd "$DESTINO" && sha256sum "${FECHA}_base.dump.age" "${FECHA}_globales.sql.age" "${FECHA}_documentos.tar.age" > "$TRABAJO/sumas" )
mv -f "$TRABAJO/sumas" "$DESTINO/${FECHA}.sha256"

# Retención (RNF-09, DP-07): en la etapa A se aplica aquí; en la etapa B la aplica la regla de ciclo de vida de Spaces.
find "$DESTINO" -maxdepth 1 -type f \( -name '????-??-??_*.age' -o -name '????-??-??.sha256' \) -mtime +"$RETENCION_DIAS" -delete

# La marca se escribe al final y de forma atómica (RF-53, CA-79).
date -u +%Y-%m-%dT%H:%M:%SZ > "$TRABAJO/marca"
mv -f "$TRABAJO/marca" "$DESTINO/ultimo_respaldo_correcto"

echo "respaldo: $FECHA correcto"
