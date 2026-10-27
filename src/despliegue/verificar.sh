#!/usr/bin/env bash
# Verificación del despliegue de la etapa A (ADR-023, ADR-027, ADR-032 decisiones 4, 12, 13 y 17).
# Como root dentro de WSL, después de desplegar.sh. Crea una cuenta de prueba y la BORRA al terminar.
#   wsl -d Ubuntu -u root -- bash /mnt/e/Proyectos/Portafolio/Apartment/src/despliegue/verificar.sh
set -uo pipefail
[ "$(id -u)" -eq 0 ] || { echo "ejecútelo como root" >&2; exit 2; }
fallos=0
ok() { echo "OK     $*"; }
mal() { echo "FALLA  $*"; fallos=$((fallos + 1)); }
prueba() { if eval "$2" >/dev/null 2>&1; then ok "$1"; else mal "$1"; fi; }
psql_como() { local u="$1"; shift; runuser -u "$u" -- psql -X -tA -d sga "$@"; }

echo "== PostgreSQL"
prueba "no escucha en ningún puerto TCP" '! ss -ltn | grep -q ":5432 "'
prueba "el socket es 0770 con el grupo sga_bd" '[ "$(stat -c "%a %G" /var/run/postgresql/.s.PGSQL.5432)" = "770 sga_bd" ]'
prueba "pg_hba.conf sin errores y solo con registros local+peer" \
  '[ "$(runuser -u postgres -- psql -X -tA -c "SELECT count(*) FROM pg_hba_file_rules WHERE error IS NOT NULL OR type <> '"'"'local'"'"' OR auth_method <> '"'"'peer'"'"'")" = "0" ]'
prueba "sga_app entra como sga_app (peer)" 'psql_como sga_app -c "SELECT 1"'
prueba "sga_respaldos entra como sga_respaldos (peer)" 'psql_como sga_respaldos -c "SELECT 1"'
prueba "sga_app NO puede entrar como otro rol (sga_dueno)" '! psql_como sga_app -U sga_dueno -c "SELECT 1"'
prueba "un usuario del sistema ajeno NO entra a la base" '! runuser -u nobody -- psql -X -tA -d sga -c "SELECT 1"'
prueba "sga_app no puede modificar ni borrar la auditoría" '! psql_como sga_app -c "UPDATE nucleo_auditoria SET accion = accion" && ! psql_como sga_app -c "DELETE FROM nucleo_auditoria"'
prueba "sga_app no puede crear tablas" '! psql_como sga_app -c "CREATE TABLE intruso (id int)"'
prueba "sga_respaldos puede leer pero no escribir" 'psql_como sga_respaldos -c "SELECT count(*) FROM nucleo_organizacion" && ! psql_como sga_respaldos -c "UPDATE nucleo_organizacion SET zona_horaria = zona_horaria"'

echo; echo "== Servicios"
prueba "sga-gunicorn.socket activo" 'systemctl is-active --quiet sga-gunicorn.socket'
prueba "nginx activo" 'systemctl is-active --quiet nginx'
prueba "el socket de Gunicorn es del usuario de la aplicación y el grupo de Nginx, 0660" '[ "$(stat -c "%U %G %a" /run/sga/gunicorn.sock)" = "sga_app www-data 660" ]'
prueba "los secretos son 0640 y de root:sga_app" '[ "$(stat -c "%U:%G %a" /etc/sga/secret_key /etc/sga/clave_cifrado | sort -u)" = "root:sga_app 640" ]'
prueba "otro usuario no lee los secretos" '! runuser -u nobody -- cat /etc/sga/secret_key'
prueba "sga_respaldos no lee la clave de cifrado de la aplicación" '! runuser -u sga_respaldos -- cat /etc/sga/clave_cifrado'

echo; echo "== HTTP (recorrido real, con el límite de solicitudes en modo de solo registro)"
cambiar_limite() { sed -i "s/^limit_req_dry_run .*/limit_req_dry_run $1;/" /etc/nginx/sga-limites.conf && nginx -t >/dev/null 2>&1 && systemctl reload nginx; }
cambiar_limite on
trap 'cambiar_limite off' EXIT
if runuser -u sga_app -- env $(grep -v "^#" /etc/sga/entorno | xargs) /opt/sga/venv/bin/python /opt/sga/src/manage.py shell \
     -c "exec(open('/opt/sga/src/despliegue/verificar_http.py').read())"; then
  ok "recorrido por HTTPS completo"
else
  mal "el recorrido por HTTPS tuvo fallos (ver arriba)"
fi
cambiar_limite off
prueba "con el límite aplicado, una ráfaga de 15 peticiones a /entrar/ produce 429"   'n=0; for _ in $(seq 1 15); do c=$(curl -ks -o /dev/null -w "%{http_code}" https://localhost/entrar/); [ "$c" = "429" ] && n=$((n+1)); done; [ "$n" -gt 0 ]'
prueba "un Host desconocido no recibe respuesta (444)" '[ "$(curl -ks -o /dev/null -w "%{http_code}" --max-time 10 -H "Host: otro.ejemplo" https://127.0.0.1/entrar/)" = "000" ]'
prueba "HTTP redirige a HTTPS (301)" '[ "$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 http://localhost/)" = "301" ]'
prueba "el registro de Nginx no guarda la cadena de consulta" '! grep -q "BUSQUEDA-SECRETA-123" /var/log/nginx/sga_acceso.log && grep -q "/auditoria/" /var/log/nginx/sga_acceso.log'
prueba "el registro de Nginx tiene los campos del formato propio" 'grep -Eq "^[0-9.]+ \[[^]]+\] (GET|POST) /[^ ]* [0-9]{3} [0-9]+ [0-9.]+$" /var/log/nginx/sga_acceso.log'
prueba "Gunicorn no tiene registro de acceso (el journal no trae peticiones)" '! journalctl -u sga-gunicorn.service --no-pager 2>/dev/null | grep -q "GET /entrar/"'
prueba "la rotación de los registros de Nginx es diaria y de 14 días" 'grep -Eq "^\s*daily" /etc/logrotate.d/nginx && grep -Eq "^\s*rotate 14" /etc/logrotate.d/nginx'

echo; echo "== Archivos estáticos"
estatico="https://localhost/static/inquilinos/reducir_fotografia.js"
prueba "el script de reducción se sirve por Nginx con tipo JavaScript, nosniff y caché"   'cab="$(curl -ks -D - -o /tmp/sga_js.txt "$estatico")"; echo "$cab" | head -1 | grep -q " 200" && echo "$cab" | grep -qi "^content-type: .*javascript" && echo "$cab" | grep -qi "^x-content-type-options: nosniff" && echo "$cab" | grep -qi "^cache-control: max-age=3600" && grep -q "LADO_MAXIMO" /tmp/sga_js.txt'
prueba "la carpeta de estáticos es de root y la aplicación no puede escribir en ella"   '[ "$(stat -c %U /opt/sga/static)" = root ] && ! runuser -u sga_app -- touch /opt/sga/static/intruso'
prueba "no hay lista de archivos de /static/" '[ "$(curl -ks -o /dev/null -w "%{http_code}" https://localhost/static/)" != "200" ]'
for ataque in "/static../etc/passwd" "/static/../etc/passwd" "/static/%2e%2e/%2e%2e/etc/passwd" "/static/..%2f..%2fetc/passwd" "/static/inquilinos/../../../etc/passwd" "/static/%2e%2e%2f%2e%2e%2fvar/lib/sga/documentos"; do
  prueba "intento de salir de /static/: $ataque" '! curl -ks --path-as-is "https://localhost$ataque" | grep -q "root:"; [ "$(curl -ks --path-as-is -o /dev/null -w "%{http_code}" "https://localhost$ataque")" != "200" ]'
done
prueba "los documentos privados no se sirven por /static/" '[ "$(curl -ks -o /dev/null -w "%{http_code}" https://localhost/static/cedulas/x.jpg)" = "404" ]'
prueba "las fotografías de contratos tampoco se sirven por /static/" '[ "$(curl -ks -o /dev/null -w "%{http_code}" https://localhost/static/contratos/x.jpg)" = "404" ]'

echo; echo "== Proceso diario (RF-11, RNF-16)"
prueba "el temporizador del proceso diario está activo" 'systemctl is-active --quiet sga-proceso-diario.timer'
prueba "el proceso diario corre como sga_app y dos ejecuciones terminan bien" 'for i in 1 2; do runuser -u sga_app -- env $(grep -v "^#" /etc/sga/entorno | xargs) /opt/sga/venv/bin/python /opt/sga/src/manage.py ejecutar_proceso_diario || exit 1; done'

echo; echo "== Limpieza de la cuenta de prueba"
runuser -u postgres -- psql -X -q -d sga -c "TRUNCATE cuentas_administrador, nucleo_auditoria, alquileres_ejecucionproceso, inquilinos_accesodocumento, inquilinos_documentoidentidad, inquilinos_consentimiento, inquilinos_textoconsentimiento, inquilinos_inquilino CASCADE; DELETE FROM django_session" >/dev/null && rm -rf /var/lib/sga/documentos/cedulas /var/lib/sga/documentos/contratos && ok "datos de prueba y archivos borrados" || mal "no se borraron los datos de prueba"

echo; echo "== systemd-analyze security (informativo, ADR-032 d4)"
for unidad in sga-gunicorn.service sga-respaldo.service sga-proceso-diario.service; do
  [ -f "/etc/systemd/system/$unidad" ] && systemd-analyze security "$unidad" --no-pager 2>/dev/null | tail -1 | sed "s/^/$unidad: /"
done

echo; [ "$fallos" -eq 0 ] && echo "VERIFICACIÓN: sin fallos" || echo "VERIFICACIÓN: $fallos fallo(s)"
exit "$fallos"
