#!/usr/bin/env bash
# Corre las pruebas de Django en el entorno de la etapa A (Python 3.14, PostgreSQL 18 por socket con
# peer, age y pg_dump 18 reales), con el código ya desplegado en /opt/sga. Como root dentro de WSL:
#   wsl -d Ubuntu -u root -- bash /mnt/e/Proyectos/Portafolio/Apartment/src/despliegue/probar.sh
# Las pruebas crean y borran su propia base (`test_sga`), así que corren como el usuario `postgres`
# (el único con CREATE DATABASE y CREATE ROLE en esta configuración). No tocan la base `sga`.
set -euo pipefail
[ "$(id -u)" -eq 0 ] || { echo "ejecútelo como root" >&2; exit 2; }
PY=/opt/sga/venv/bin/python
cd /opt/sga/src
echo "Python: $($PY --version) | PostgreSQL: $(runuser -u postgres -- psql -X -tA -c 'SHOW server_version') | age: $(age --version) | pg_dump: $(pg_dump --version)"
echo "Dependencias instaladas:"; $PY -m pip list --format=freeze 2>/dev/null | grep -iE '^(django|psycopg|psycopg-binary|argon2-cffi|pyotp|cryptography|gunicorn)=='
ENTORNO=(env SGA_DEBUG=1 SGA_BD_USUARIO=postgres SGA_BD_HOST=/var/run/postgresql PYTHONDONTWRITEBYTECODE=1)
echo; echo "== makemigrations --check"
runuser -u postgres -- "${ENTORNO[@]}" $PY manage.py makemigrations --check --dry-run
echo; echo "== check --deploy"
runuser -u sga_app -- env $(grep -v '^#' /etc/sga/entorno | xargs) SGA_SECRET_KEY="$(cat /etc/sga/secret_key)" PYTHONDONTWRITEBYTECODE=1 $PY manage.py check --deploy || true
echo; echo "== pruebas"
runuser -u postgres -- "${ENTORNO[@]}" $PY manage.py test --verbosity 1
