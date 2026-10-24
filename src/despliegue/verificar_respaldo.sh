#!/usr/bin/env bash
# Verificación del respaldo cifrado en el servidor de la etapa A (ADR-024, ADR-032 d9 y d15, RNF-09).
# Como root dentro de WSL, con el sistema ya desplegado. Genera un par de claves SOLO PARA LA PRUEBA
# (en producción la privada se crea fuera del servidor y nunca está en él) y lo borra al terminar.
#   wsl -d Ubuntu -u root -- bash /mnt/e/Proyectos/Portafolio/Apartment/src/despliegue/verificar_respaldo.sh
set -uo pipefail
[ "$(id -u)" -eq 0 ] || { echo "ejecútelo como root" >&2; exit 2; }
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fallos=0
ok() { echo "OK     $*"; }
mal() { echo "FALLA  $*"; fallos=$((fallos + 1)); }
prueba() { if eval "$2" >/dev/null 2>&1; then ok "$1"; else mal "$1"; fi; }

CLAVES="$(mktemp -d /root/prueba_respaldo.XXXXXX)"
COPIA="$(mktemp -d /tmp/prueba_restauracion.XXXXXX)"
limpiar() {
  rm -rf "$CLAVES" "$COPIA"
  rm -f /var/lib/sga/documentos/prueba_respaldo.txt
  runuser -u postgres -- dropdb --if-exists sga_prueba_restauracion >/dev/null 2>&1
  rm -f /etc/sga/respaldo_clave_publica.txt
  systemctl disable --now sga-respaldo.timer >/dev/null 2>&1
  rm -f /var/lib/sga/respaldos/*
}
trap limpiar EXIT

age-keygen -o "$CLAVES/privada.txt" >/dev/null 2>&1
age-keygen -y "$CLAVES/privada.txt" > "$CLAVES/publica.txt"
echo "contenido de prueba de un documento" > /var/lib/sga/documentos/prueba_respaldo.txt
chown sga_app:sga_respaldos /var/lib/sga/documentos/prueba_respaldo.txt

echo "== Activación del respaldo"
bash "$AQUI/desplegar.sh" --clave-publica-respaldo "$CLAVES/publica.txt" >/dev/null 2>&1 && ok "desplegar.sh con la clave pública" || mal "desplegar.sh falló"
prueba "el temporizador está activo" 'systemctl is-active --quiet sga-respaldo.timer'
prueba "la clave del servidor es la pública (no contiene la privada)" '! grep -q AGE-SECRET-KEY /etc/sga/respaldo_clave_publica.txt'
echo "próxima ejecución: $(systemctl list-timers sga-respaldo.timer --no-pager 2>/dev/null | sed -n 2p | cut -c1-60)"
echo "hora normalizada: $(systemd-analyze calendar '*-*-* 05:00:00 America/Costa_Rica' --no-pager 2>&1 | grep -E 'Normalized|Next elapse|UTC' | tr '\n' ' ')"

echo; echo "== Ejecución del servicio"
if systemctl start sga-respaldo.service; then ok "sga-respaldo.service terminó bien"; else mal "sga-respaldo.service falló"; journalctl -u sga-respaldo.service --no-pager | tail -8; fi
D=/var/lib/sga/respaldos
fecha="$(TZ=America/Costa_Rica date +%Y-%m-%d)"
for parte in base.dump.age globales.sql.age documentos.tar.age; do
  prueba "existe ${fecha}_${parte} y es de sga_respaldos" "[ \"\$(stat -c %U $D/${fecha}_${parte})\" = sga_respaldos ]"
done
prueba "existen las sumas y la marca del último respaldo correcto" "[ -f $D/$fecha.sha256 ] && [ -f $D/ultimo_respaldo_correcto ]"
prueba "los archivos no son legibles por otros usuarios" '[ "$(stat -c %a '"$D/${fecha}_base.dump.age"')" = "600" ]'
prueba "nada en claro: ni el texto del documento ni la cabecera de pg_dump" \
  "! grep -rqa -e 'contenido de prueba de un documento' -e PGDMP $D"
journalctl -u sga-respaldo.service --no-pager 2>/dev/null | tail -3 | sed 's/^/journal: /'

echo; echo "== Restauración completa con la clave privada (como postgres, que puede crear bases)"
cp "$D"/* "$COPIA"/; cp "$CLAVES/privada.txt" "$COPIA/privada.txt"; chown -R postgres:postgres "$COPIA"
prueba "restaurar.sh restaura la base y los documentos" \
  "runuser -u postgres -- env PGDATABASE=postgres bash $AQUI/../respaldo/restaurar.sh --fecha $fecha --clave-privada $COPIA/privada.txt --origen $COPIA --base-destino sga_prueba_restauracion --documentos-destino $COPIA/documentos_recuperados"
prueba "el documento se recuperó igual" "[ \"\$(cat $COPIA/documentos_recuperados/prueba_respaldo.txt)\" = 'contenido de prueba de un documento' ]"
prueba "la base restaurada tiene las tablas del sistema" \
  "[ \"\$(runuser -u postgres -- psql -X -tA -d sga_prueba_restauracion -c 'SELECT count(*) FROM nucleo_organizacion')\" = 1 ]"

echo; echo "== Un fallo no deja una marca falsa"
marca_antes="$(cat $D/ultimo_respaldo_correcto)"
sleep 1
rm -f /etc/sga/respaldo_clave_publica.txt
if systemctl start sga-respaldo.service 2>/dev/null; then mal "el servicio debió fallar sin clave pública"; else ok "el servicio falla si falta la clave pública"; fi
prueba "la marca no cambió" "[ \"\$(cat $D/ultimo_respaldo_correcto)\" = '$marca_antes' ]"

echo; echo "== systemd-analyze security (informativo)"
systemd-analyze security sga-respaldo.service --no-pager 2>/dev/null | tail -1

echo; [ "$fallos" -eq 0 ] && echo "VERIFICACIÓN DEL RESPALDO: sin fallos" || echo "VERIFICACIÓN DEL RESPALDO: $fallos fallo(s)"
exit "$fallos"
