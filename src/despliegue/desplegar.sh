#!/usr/bin/env bash
# Despliegue del SGA en la etapa A: WSL 2 con Ubuntu 26.04, sin contenedores (plan, sección 5.1).
# Un solo comando, idempotente, como root dentro de la distribución:
#   wsl -d Ubuntu -u root -- bash /mnt/e/Proyectos/Portafolio/Apartment/src/despliegue/desplegar.sh
# Opciones:
#   --nombre-sitio NOMBRE         nombre del sitio (por defecto localhost)
#   --clave-publica-respaldo ARCH clave pública de age para los respaldos; sin ella no se activa el
#                                 temporizador del respaldo (la clave privada no debe estar aquí)
#
# Qué hace: paquetes, usuarios del sistema, PostgreSQL 18 solo por socket con `peer`, roles y
# privilegios, el código en /opt/sga, secretos en /etc/sga, Gunicorn con socket de systemd, Nginx con
# HTTPS autofirmado y, si hay clave pública, el respaldo diario. No toca nada fuera de la distribución.
# Lo que es del servidor real (SSH, firewalls, actualizaciones automáticas, Certbot) es de la etapa B.
set -euo pipefail

NOMBRE_SITIO="localhost"
CLAVE_PUBLICA_RESPALDO=""
while [ $# -gt 0 ]; do
  case "$1" in
    --nombre-sitio) NOMBRE_SITIO="${2:-}"; shift 2 ;;
    --clave-publica-respaldo) CLAVE_PUBLICA_RESPALDO="${2:-}"; shift 2 ;;
    *) echo "desplegar: argumento desconocido: $1" >&2; exit 2 ;;
  esac
done
[[ "$NOMBRE_SITIO" =~ ^[A-Za-z0-9.-]+$ ]] || { echo "desplegar: nombre de sitio no válido" >&2; exit 2; }
[ "$(id -u)" -eq 0 ] || { echo "desplegar: ejecútelo como root" >&2; exit 2; }

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORIGEN="$(cd "$AQUI/.." && pwd)"           # la carpeta src del repositorio
DESTINO=/opt/sga
BD=sga
paso() { echo; echo "== $*"; }

paso "1. Paquetes del sistema"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq postgresql-18 postgresql-client-18 nginx age python3-venv openssl rsync curl ca-certificates >/dev/null
python3 --version

paso "2. Usuarios y grupos del sistema (estáticos, sin contraseña ni intérprete de órdenes)"
getent group sga_bd >/dev/null || groupadd --system sga_bd
for usuario in sga_dueno sga_app sga_respaldos; do
  id "$usuario" >/dev/null 2>&1 || useradd --system --user-group --no-create-home --shell /usr/sbin/nologin "$usuario"
  usermod -aG sga_bd "$usuario"
done
# El usuario `postgres` es dueño del socket y solo puede asignarle un grupo del que sea miembro
# (si no, PostgreSQL no arranca: «could not set group of file ... Operation not permitted»).
usermod -aG sga_bd postgres

paso "3. Carpetas"
install -d -m 0755 -o root -g root /etc/sga "$DESTINO"
install -d -m 0750 -o sga_app -g sga_respaldos /var/lib/sga/documentos
install -d -m 0750 -o sga_respaldos -g sga_respaldos /var/lib/sga/respaldos
chmod 0755 /var/lib/sga

paso "4. PostgreSQL 18 solo por socket Unix con peer (ADR-027, ADR-032 d12)"
PG=/etc/postgresql/18/main
[ -d "$PG" ] || { echo "desplegar: no existe el clúster $PG" >&2; exit 1; }
install -d -m 0755 "$PG/conf.d"
install -m 0644 "$AQUI/postgresql/sga.conf" "$PG/conf.d/sga.conf"
[ -f "$PG/pg_hba.conf.original" ] || cp -p "$PG/pg_hba.conf" "$PG/pg_hba.conf.original"
install -m 0640 -o postgres -g postgres "$AQUI/postgresql/pg_hba.conf" "$PG/pg_hba.conf"
systemctl restart postgresql@18-main
for _ in $(seq 1 30); do runuser -u postgres -- psql -X -tA -c 'SELECT 1' >/dev/null 2>&1 && break; sleep 1; done
errores="$(runuser -u postgres -- psql -X -tA -c 'SELECT count(*) FROM pg_hba_file_rules WHERE error IS NOT NULL')"
if [ "$errores" != "0" ]; then
  echo "desplegar: pg_hba.conf tiene errores; se restaura el original" >&2
  cp -p "$PG/pg_hba.conf.original" "$PG/pg_hba.conf"; systemctl restart postgresql@18-main; exit 1
fi
runuser -u postgres -- psql -X -tA -c 'SELECT pg_reload_conf()' >/dev/null

paso "5. Roles y base (src/db/roles.sql)"
runuser -u postgres -- psql -X -v ON_ERROR_STOP=1 -q \
  -v rol_dueno=sga_dueno -v rol_app=sga_app -v rol_respaldos=sga_respaldos -v base="$BD" -f "$ORIGEN/db/roles.sql" >/dev/null

paso "6. Código y entorno virtual en $DESTINO"
rsync -a --delete --exclude '.venv' --exclude '__pycache__' --exclude '*.pyc' --exclude '.env' \
  --exclude 'despliegue/__pycache__' "$ORIGEN/" "$DESTINO/src/"
chown -R root:root "$DESTINO/src"; find "$DESTINO/src" -type d -exec chmod 0755 {} +; find "$DESTINO/src" -type f -exec chmod 0644 {} +
chmod 0755 "$DESTINO"/src/respaldo/*.sh "$DESTINO"/src/despliegue/*.sh
[ -x "$DESTINO/venv/bin/python" ] || python3 -m venv "$DESTINO/venv"
"$DESTINO/venv/bin/python" -m pip install -q --disable-pip-version-check -r "$DESTINO/src/requirements.txt"
"$DESTINO/venv/bin/python" --version

paso "7. Secretos en /etc/sga (ADR-032 d6)"
if [ ! -f /etc/sga/secret_key ]; then
  "$DESTINO/venv/bin/python" -c 'import secrets; print(secrets.token_urlsafe(64), end="")' > /etc/sga/secret_key
fi
if [ ! -f /etc/sga/clave_cifrado ]; then
  "$DESTINO/venv/bin/python" -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode(), end="")' > /etc/sga/clave_cifrado
fi
chown root:sga_app /etc/sga/secret_key /etc/sga/clave_cifrado; chmod 0640 /etc/sga/secret_key /etc/sga/clave_cifrado
cat > /etc/sga/entorno <<EOF
# Variables de Gunicorn y de los comandos de la aplicación. Sin secretos: estos están en archivos.
SGA_BD_NOMBRE=$BD
SGA_BD_USUARIO=sga_app
SGA_BD_HOST=/var/run/postgresql
SGA_HOSTS_PERMITIDOS=$NOMBRE_SITIO
EOF
chmod 0644 /etc/sga/entorno

paso "8. Migraciones y privilegios con el rol dueño"
como_dueno() {
  runuser -u sga_dueno -- env SGA_BD_NOMBRE="$BD" SGA_BD_USUARIO=sga_dueno SGA_BD_HOST=/var/run/postgresql \
    SGA_SECRET_KEY=migracion-no-usa-esta-clave PYTHONDONTWRITEBYTECODE=1 \
    "$DESTINO/venv/bin/python" "$DESTINO/src/manage.py" "$@"
}
como_dueno migrate --no-input -v 0
como_dueno aplicar_privilegios

paso "9. Certificado autofirmado (etapa A)"
install -d -m 0755 /etc/ssl/sga
if [ ! -f /etc/ssl/sga/certificado.pem ]; then
  openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes -days 825 \
    -subj "/CN=$NOMBRE_SITIO" -addext "subjectAltName=DNS:$NOMBRE_SITIO,DNS:localhost,IP:127.0.0.1" \
    -keyout /etc/ssl/sga/clave.pem -out /etc/ssl/sga/certificado.pem 2>/dev/null
  chmod 0600 /etc/ssl/sga/clave.pem
fi

paso "10. Gunicorn con socket de systemd"
install -m 0644 "$AQUI/systemd/sga-gunicorn.socket" "$AQUI/systemd/sga-gunicorn.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable sga-gunicorn.socket >/dev/null 2>&1
systemctl restart sga-gunicorn.socket
systemctl try-restart sga-gunicorn.service || true

paso "11. Nginx"
install -m 0644 "$AQUI/nginx/sga-http.conf" /etc/nginx/conf.d/sga.conf
install -m 0644 "$AQUI/nginx/sga-proxy.conf" /etc/nginx/sga-proxy.conf
install -m 0644 "$AQUI/nginx/sga-limites.conf" /etc/nginx/sga-limites.conf
sed "s/@NOMBRE_SITIO@/$NOMBRE_SITIO/g" "$AQUI/nginx/sga-sitio.conf" > /etc/nginx/sites-available/sga
ln -sf /etc/nginx/sites-available/sga /etc/nginx/sites-enabled/sga
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl enable nginx >/dev/null 2>&1
systemctl reload nginx 2>/dev/null || systemctl restart nginx

paso "12. Respaldo diario (ADR-024, ADR-032 d15)"
if [ -n "$CLAVE_PUBLICA_RESPALDO" ]; then
  [ -r "$CLAVE_PUBLICA_RESPALDO" ] || { echo "desplegar: no se lee $CLAVE_PUBLICA_RESPALDO" >&2; exit 1; }
  ! grep -q 'AGE-SECRET-KEY' "$CLAVE_PUBLICA_RESPALDO" || { echo "desplegar: ese archivo contiene una clave PRIVADA" >&2; exit 1; }
  install -m 0644 "$CLAVE_PUBLICA_RESPALDO" /etc/sga/respaldo_clave_publica.txt
fi
if [ -f /etc/sga/respaldo_clave_publica.txt ]; then
  install -m 0644 "$AQUI/../respaldo/systemd/sga-respaldo.service" "$AQUI/../respaldo/systemd/sga-respaldo.timer" /etc/systemd/system/
  systemctl daemon-reload
  systemctl enable --now sga-respaldo.timer >/dev/null 2>&1
  echo "temporizador del respaldo activo"
else
  echo "SIN respaldo: falta la clave pública (--clave-publica-respaldo). El temporizador NO se activó."
fi

paso "13. Comprobación"
# Se pide «/» y no «/entrar/»: la zona de autenticación de Nginx limita las peticiones a /entrar/ (6 por minuto).
codigo() { curl -ks -o /dev/null -w '%{http_code}' --max-time 15 "$@" || true; }
https="$(codigo "https://$NOMBRE_SITIO/" --resolve "$NOMBRE_SITIO:443:127.0.0.1")"
http="$(codigo "http://$NOMBRE_SITIO/" --resolve "$NOMBRE_SITIO:80:127.0.0.1")"
echo "HTTPS /: $https (esperado 302 al inicio de sesión) | HTTP /: $http (esperado 301)"
[ "$https" = "302" ] && [ "$http" = "301" ] || { echo "desplegar: la comprobación falló" >&2; exit 1; }
echo
echo "Despliegue terminado. Cuenta administradora: runuser -u sga_app -- env \$(grep -v '^#' /etc/sga/entorno | xargs) $DESTINO/venv/bin/python $DESTINO/src/manage.py crear_administrador --usuario NOMBRE"
