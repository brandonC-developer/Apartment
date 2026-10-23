# Ejecuta la prueba desechable del modelo v0.5 en un servidor PostgreSQL aparte (puerto 54329).
# Crea un directorio de datos temporal, lo arranca, corre prueba_modelo_v0.5_postgres.sql,
# hace las pruebas de concurrencia con dos sesiones reales y lo borra todo al terminar.
# No toca el servicio de PostgreSQL instalado. Uso:
#   powershell -File ejecutar_prueba_v0.5.ps1 -Salida resultado_prueba_v0.5.txt
param(
  [string]$Salida = 'resultado_prueba_v0.5.txt',
  [int]$Puerto = 54329
)
$ErrorActionPreference = 'Stop'
$bin = 'C:\Program Files\PostgreSQL\18\bin'
$aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
$raiz = Join-Path ([System.IO.Path]::GetTempPath()) ("sga_pg_v05_" + [guid]::NewGuid().ToString('N').Substring(0, 8))
$datos = Join-Path $raiz 'datos'
New-Item -ItemType Directory -Path $raiz | Out-Null
$out = New-Object System.Collections.Generic.List[string]

function Psql([string]$Base, [string[]]$Argumentos, [string]$Etiqueta) {
  $so = Join-Path $raiz ([guid]::NewGuid().ToString('N') + '.out')
  $se = Join-Path $raiz ([guid]::NewGuid().ToString('N') + '.err')
  $lista = @('-p', $Puerto, '-U', 'test', '-d', $Base, '-X', '-v', 'ON_ERROR_STOP=1') + $Argumentos
  $p = Start-Process -FilePath "$bin\psql.exe" -ArgumentList $lista -NoNewWindow -Wait -PassThru -RedirectStandardOutput $so -RedirectStandardError $se
  [pscustomobject]@{ Codigo = $p.ExitCode; Salida = (Get-Content $so -Raw -Encoding UTF8); Error = (Get-Content $se -Raw -Encoding UTF8) }
}
function Sql([string]$Base, [string]$Texto, [switch]$Valor) {
  # Escribe la sentencia en un archivo para no depender del entrecomillado de la linea de comandos
  $f = Join-Path $raiz ([guid]::NewGuid().ToString('N') + '.sql')
  Set-Content -Path $f -Encoding UTF8 -Value $Texto
  $extra = @(); if ($Valor) { $extra = @('-t', '-A') }
  Psql $Base ($extra + @('-f', $f)) 'sql'
}
function PsqlAsync([string]$Base, [string]$Archivo) {
  $so = Join-Path $raiz ([guid]::NewGuid().ToString('N') + '.out')
  $se = Join-Path $raiz ([guid]::NewGuid().ToString('N') + '.err')
  $lista = @('-p', $Puerto, '-U', 'test', '-d', $Base, '-X', '-v', 'ON_ERROR_STOP=1', '-f', $Archivo)
  $p = Start-Process -FilePath "$bin\psql.exe" -ArgumentList $lista -NoNewWindow -PassThru -RedirectStandardOutput $so -RedirectStandardError $se
  $null = $p.Handle   # sin esto, .NET no puede leer el codigo de salida cuando el proceso termina
  [pscustomobject]@{ Proceso = $p; So = $so; Se = $se; Reloj = [System.Diagnostics.Stopwatch]::StartNew() }
}
function Termina($s) {
  $s.Proceso.WaitForExit(); $s.Reloj.Stop()
  [pscustomobject]@{ Codigo = $s.Proceso.ExitCode; Segundos = [math]::Round($s.Reloj.Elapsed.TotalSeconds, 1); Error = (Get-Content $s.Se -Raw -Encoding UTF8); Salida = (Get-Content $s.So -Raw -Encoding UTF8) }
}
$conc = New-Object System.Collections.Generic.List[object]
function Concluye([string]$prueba, [bool]$ok, [string]$detalle) { $conc.Add([pscustomobject]@{ Prueba = $prueba; Ok = $ok; Detalle = $detalle }) }

try {
  if (Get-NetTCPConnection -LocalPort $Puerto -State Listen -ErrorAction SilentlyContinue) { throw "El puerto $Puerto ya esta en uso; no se toca." }
  $out.Add("Prueba del modelo MDD-SGA-001 v0.5 - " + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
  $out.Add((& "$bin\psql.exe" --version))
  & "$bin\initdb.exe" -D $datos -U test -A trust -E UTF8 --locale=C | Out-Null
  # El servidor hereda la salida de pg_ctl: se redirige a archivos y se espera solo a pg_ctl (no a sus hijos)
  $arr = Start-Process -FilePath "$bin\pg_ctl.exe" -ArgumentList @('start', '-D', $datos, '-o', "`"-p $Puerto`"", '-w', '-l', (Join-Path $raiz 'servidor.log')) `
    -NoNewWindow -PassThru -RedirectStandardOutput (Join-Path $raiz 'ctl.out') -RedirectStandardError (Join-Path $raiz 'ctl.err')
  if (-not $arr.WaitForExit(60000)) { throw 'pg_ctl start no termino en 60 s' }
  # El codigo de salida no siempre esta disponible con la salida redirigida: se confirma con el mensaje de pg_ctl
  if ((Get-Content (Join-Path $raiz 'ctl.out') -Raw) -notmatch 'server started') { throw 'pg_ctl start fallo: ' + (Get-Content (Join-Path $raiz 'ctl.err') -Raw) }
  $out.Add("Servidor desechable en el puerto $Puerto (directorio temporal, se borra al terminar)")

  # 1. Comprobaciones de una sola sesion
  $r = Psql 'postgres' @('-f', (Join-Path $aqui 'prueba_modelo_v0.5_postgres.sql')) 'una sesion'
  if ($r.Codigo -ne 0) { throw ("Fallo el script SQL: " + $r.Error) }
  $out.Add($r.Salida)

  # 2. Concurrencia de R24: dos sesiones intentan usar el mismo identificador
  $a = Join-Path $raiz 'a.sql'; $b = Join-Path $raiz 'b.sql'
  Set-Content -Path $a -Encoding UTF8 -Value "BEGIN;`nSELECT asociar_cedula('h-concurrente', 3, repeat('9',32));`nSELECT pg_sleep(3);`nCOMMIT;"
  Set-Content -Path $b -Encoding UTF8 -Value "BEGIN;`nSELECT asociar_cedula('h-concurrente', 3, repeat('8',32));`nCOMMIT;"
  $sa = PsqlAsync 'sga_prueba_v05' $a; Start-Sleep -Milliseconds 1000; $sb = PsqlAsync 'sga_prueba_v05' $b
  $ra = Termina $sa; $rb = Termina $sb
  Concluye 'R24 concurrencia: la primera sesion usa el identificador' ($ra.Codigo -eq 0) "codigo=$($ra.Codigo)"
  Concluye 'R24 concurrencia: la segunda espera el bloqueo (>= 2 s) y falla' (($rb.Codigo -ne 0) -and ($rb.Segundos -ge 2) -and ($rb.Error -match 'no valido')) "codigo=$($rb.Codigo) espera=$($rb.Segundos) s mensaje=$(($rb.Error -split "`n")[0].Trim())"
  $n = Sql 'sga_prueba_v05' "SELECT count(*) || ':' || max(referencia_archivo) FROM documento_identidad WHERE inquilino_id=3 AND cara='reverso';" -Valor
  Concluye 'R24 concurrencia: queda una sola fotografia, la de la primera sesion' ($n.Salida.Trim() -eq ('1:' + ('9' * 32))) ("obtenido=" + $n.Salida.Trim())

  # 3. Concurrencia del orden de fotografias del contrato (R22), con y sin bloqueo del contrato
  Sql 'sga_prueba_v05' @"
INSERT INTO archivo_temporal(identificador_hash,destino,referencia_archivo,tipo_real_archivo,tamano_bytes,creado_en,expira_en)
SELECT h,'documento_contrato',repeat(c,32),'image/jpeg',1000,now(),now()+interval '24 hours'
FROM (VALUES ('h-c3','1'),('h-c4','2'),('h-c5','3'),('h-c6','4')) v(h,c);
CREATE FUNCTION asociar_fotografia_contrato_bloqueando(h text, con bigint, ref_definitiva text) RETURNS bigint LANGUAGE plpgsql AS `$`$
BEGIN
  PERFORM 1 FROM contrato WHERE id = con FOR UPDATE;   -- serializa a quienes agregan fotografias al mismo contrato
  RETURN asociar_fotografia_contrato(h, con, ref_definitiva);
END `$`$;
"@ | Out-Null
  Set-Content -Path $a -Encoding UTF8 -Value "BEGIN;`nSELECT asociar_fotografia_contrato('h-c3', 3, repeat('1',32));`nSELECT pg_sleep(3);`nCOMMIT;"
  Set-Content -Path $b -Encoding UTF8 -Value "BEGIN;`nSELECT asociar_fotografia_contrato('h-c4', 3, repeat('2',32));`nCOMMIT;"
  $sa = PsqlAsync 'sga_prueba_v05' $a; Start-Sleep -Milliseconds 1000; $sb = PsqlAsync 'sga_prueba_v05' $b
  $ra = Termina $sa; $rb = Termina $sb
  Concluye 'R22 concurrencia SIN bloqueo del contrato: la segunda sesion calcula el mismo orden y R22 la rechaza' (($ra.Codigo -eq 0) -and ($rb.Codigo -ne 0) -and ($rb.Error -match 'r22_orden_unico')) "primera=$($ra.Codigo) segunda=$($rb.Codigo) mensaje=$(($rb.Error -split "`n")[0].Trim())"
  Set-Content -Path $a -Encoding UTF8 -Value "BEGIN;`nSELECT asociar_fotografia_contrato_bloqueando('h-c5', 3, repeat('3',32));`nSELECT pg_sleep(3);`nCOMMIT;"
  Set-Content -Path $b -Encoding UTF8 -Value "BEGIN;`nSELECT asociar_fotografia_contrato_bloqueando('h-c6', 3, repeat('4',32));`nCOMMIT;"
  $sa = PsqlAsync 'sga_prueba_v05' $a; Start-Sleep -Milliseconds 1000; $sb = PsqlAsync 'sga_prueba_v05' $b
  $ra = Termina $sa; $rb = Termina $sb
  $o = Sql 'sga_prueba_v05' "SELECT string_agg(orden::text, ',' ORDER BY orden) FROM documento_contrato WHERE contrato_id=3;" -Valor
  Concluye 'R22 concurrencia CON bloqueo del contrato: las dos se registran con ordenes distintos (1 y 2 de antes, 3 y 4 ahora)' (($ra.Codigo -eq 0) -and ($rb.Codigo -eq 0) -and ($o.Salida.Trim() -eq '1,2,3,4')) "primera=$($ra.Codigo) segunda=$($rb.Codigo) espera=$($rb.Segundos) s ordenes=$($o.Salida.Trim())"

  $out.Add('')
  $out.Add('== Pruebas de concurrencia (dos sesiones reales) ==')
  foreach ($c in $conc) { $out.Add((($(if ($c.Ok) { ' OK    ' } else { ' FALLA ' })) + $c.Prueba + ' | ' + $c.Detalle)) }
  $out.Add(("Concurrencia: {0} correctas, {1} fallas" -f @($conc | Where-Object Ok).Count, @($conc | Where-Object { -not $_.Ok }).Count))
}
finally {
  & "$bin\pg_ctl.exe" stop -D $datos -m fast 2>$null | Out-Null
  Start-Sleep -Milliseconds 500
  Remove-Item -Recurse -Force $raiz -ErrorAction SilentlyContinue
  $out.Add('Servidor detenido y directorio temporal borrado.')
  $out | Out-File -FilePath (Join-Path $aqui $Salida) -Encoding utf8
}
