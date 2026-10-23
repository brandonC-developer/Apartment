# Ejecuta la prueba desechable del modelo v0.7 en un servidor PostgreSQL aparte (puerto 54329).
# Crea un directorio de datos temporal, lo arranca, corre prueba_modelo_v0.7_postgres.sql,
# hace las pruebas de concurrencia con dos sesiones reales y lo borra todo al terminar.
# No toca el servicio de PostgreSQL instalado. Uso:
#   powershell -File ejecutar_prueba_v0.7.ps1 -Salida resultado_prueba_v0.7.txt
param(
  [string]$Salida = 'resultado_prueba_v0.7.txt',
  [int]$Puerto = 54329
)
$ErrorActionPreference = 'Stop'
$bin = 'C:\Program Files\PostgreSQL\18\bin'
$aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
$raiz = Join-Path ([System.IO.Path]::GetTempPath()) ("sga_pg_v07_" + [guid]::NewGuid().ToString('N').Substring(0, 8))
$datos = Join-Path $raiz 'datos'
New-Item -ItemType Directory -Path $raiz | Out-Null
$out = New-Object System.Collections.Generic.List[string]

function Psql([string]$Base, [string[]]$Argumentos) {
  $so = Join-Path $raiz ([guid]::NewGuid().ToString('N') + '.out')
  $se = Join-Path $raiz ([guid]::NewGuid().ToString('N') + '.err')
  $lista = @('-p', $Puerto, '-U', 'test', '-d', $Base, '-X', '-v', 'ON_ERROR_STOP=1') + $Argumentos
  $p = Start-Process -FilePath "$bin\psql.exe" -ArgumentList $lista -NoNewWindow -Wait -PassThru -RedirectStandardOutput $so -RedirectStandardError $se
  $null = $p.Handle
  [pscustomobject]@{ Codigo = $p.ExitCode; Salida = (Get-Content $so -Raw -Encoding UTF8); Error = (Get-Content $se -Raw -Encoding UTF8) }
}
function Sql([string]$Base, [string]$Texto, [switch]$Valor) {
  # Escribe la sentencia en un archivo para no depender del entrecomillado de la linea de comandos
  $f = Join-Path $raiz ([guid]::NewGuid().ToString('N') + '.sql')
  Set-Content -Path $f -Encoding UTF8 -Value $Texto
  $extra = @(); if ($Valor) { $extra = @('-t', '-A') }
  Psql $Base ($extra + @('-f', $f))
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
function Par([string]$Base, [string]$SqlA, [string]$SqlB) {
  # Sesion A: abre transaccion, ejecuta, espera 3 s y confirma. Sesion B arranca 1 s despues, sin esperas propias.
  $a = Join-Path $raiz ([guid]::NewGuid().ToString('N') + '.sql'); $b = Join-Path $raiz ([guid]::NewGuid().ToString('N') + '.sql')
  Set-Content -Path $a -Encoding UTF8 -Value "BEGIN;`n$SqlA`nSELECT pg_sleep(3);`nCOMMIT;"
  Set-Content -Path $b -Encoding UTF8 -Value "BEGIN;`n$SqlB`nCOMMIT;"
  $sa = PsqlAsync $Base $a; Start-Sleep -Milliseconds 1000; $sb = PsqlAsync $Base $b
  # B se cierra primero: su cronometro debe pararse cuando B termina, no despues de esperar a A
  $rb = Termina $sb; $ra = Termina $sa
  [pscustomobject]@{ A = $ra; B = $rb }
}
$conc = New-Object System.Collections.Generic.List[object]
function Concluye([string]$prueba, [bool]$ok, [string]$detalle) { $conc.Add([pscustomobject]@{ Prueba = $prueba; Ok = $ok; Detalle = $detalle }) }
function Primera([string]$t) { if ($t) { ($t -split "`n")[0].Trim() } else { '' } }

try {
  if (Get-NetTCPConnection -LocalPort $Puerto -State Listen -ErrorAction SilentlyContinue) { throw "El puerto $Puerto ya esta en uso; no se toca." }
  $out.Add("Prueba del modelo MDD-SGA-001 v0.7 - " + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
  $out.Add((& "$bin\psql.exe" --version))
  & "$bin\initdb.exe" -D $datos -U test -A trust -E UTF8 --locale=C | Out-Null
  # El servidor hereda la salida de pg_ctl: se redirige a archivos y se espera solo a pg_ctl (no a sus hijos)
  $arr = Start-Process -FilePath "$bin\pg_ctl.exe" -ArgumentList @('start', '-D', $datos, '-o', "`"-p $Puerto`"", '-w', '-l', (Join-Path $raiz 'servidor.log')) `
    -NoNewWindow -PassThru -RedirectStandardOutput (Join-Path $raiz 'ctl.out') -RedirectStandardError (Join-Path $raiz 'ctl.err')
  if (-not $arr.WaitForExit(60000)) { throw 'pg_ctl start no termino en 60 s' }
  if ((Get-Content (Join-Path $raiz 'ctl.out') -Raw) -notmatch 'server started') { throw 'pg_ctl start fallo: ' + (Get-Content (Join-Path $raiz 'ctl.err') -Raw) }
  $out.Add("Servidor desechable en el puerto $Puerto (directorio temporal, se borra al terminar)")

  # 1. Comprobaciones de una sola sesion
  $r = Psql 'postgres' @('-f', (Join-Path $aqui 'prueba_modelo_v0.7_postgres.sql'))
  if ($r.Codigo -ne 0) { throw ("Fallo el script SQL: " + $r.Error) }
  $out.Add($r.Salida)
  $db = 'sga_prueba_v07'

  # 2. H18: orden de las fotografias del contrato 3 (Carla ya tiene la 1), sin y con bloqueo del contrato
  $p = Par $db "SELECT agregar_fotografia_contrato_sin_bloqueo(3, repeat('1',32), 'image/jpeg', 1000);" "SELECT agregar_fotografia_contrato_sin_bloqueo(3, repeat('2',32), 'image/jpeg', 1000);"
  Concluye 'H18 concurrencia SIN bloqueo del contrato: la segunda sesion calcula el mismo orden y R22 la rechaza' (($p.A.Codigo -eq 0) -and ($p.B.Codigo -ne 0) -and ($p.B.Error -match 'r22_orden_unico')) "primera=$($p.A.Codigo) segunda=$($p.B.Codigo) mensaje=$(Primera $p.B.Error)"
  $p = Par $db "SELECT agregar_fotografia_contrato(3, repeat('3',32), 'image/jpeg', 1000);" "SELECT agregar_fotografia_contrato(3, repeat('4',32), 'image/jpeg', 1000);"
  $o = Sql $db "SELECT string_agg(orden::text, ',' ORDER BY orden) FROM documento_contrato WHERE contrato_id=3;" -Valor
  Concluye 'H18 concurrencia CON bloqueo del contrato: las dos se registran con ordenes distintos (1 y 2 de antes, 3 de la sesion sin bloqueo, 4 y 5 ahora)' (($p.A.Codigo -eq 0) -and ($p.B.Codigo -eq 0) -and ($p.B.Segundos -ge 2) -and ($o.Salida.Trim() -eq '1,2,3,4,5')) "primera=$($p.A.Codigo) segunda=$($p.B.Codigo) espera=$($p.B.Segundos) s ordenes=$($o.Salida.Trim())"

  # 3. R25 bajo concurrencia: dos reemplazos simultaneos del frente de Ana
  $p = Par $db "SELECT agregar_o_reemplazar_cedula(1, 'frente', repeat('5',32), 'image/jpeg', 1000);" "SELECT agregar_o_reemplazar_cedula(1, 'frente', repeat('6',32), 'image/jpeg', 1000);"
  $n = Sql $db "SELECT count(*) || ':' || max(referencia_archivo) FROM documento_identidad WHERE inquilino_id=1 AND cara='frente' AND eliminado_en IS NULL;" -Valor
  Concluye 'R25 concurrencia: dos reemplazos del mismo frente, la segunda espera y falla; queda un solo frente activo, el de la primera' (($p.A.Codigo -eq 0) -and ($p.B.Codigo -ne 0) -and ($p.B.Segundos -ge 2) -and ($p.B.Error -match 'r25_una_activa_por_cara') -and ($n.Salida.Trim() -eq ('1:' + ('5' * 32)))) "primera=$($p.A.Codigo) segunda=$($p.B.Codigo) espera=$($p.B.Segundos) s mensaje=$(Primera $p.B.Error) activos=$($n.Salida.Trim())"

  # 4. R26 frente a un reemplazo del frente: nunca hay un instante visible sin frente
  Sql $db "INSERT INTO propiedad(alias) VALUES ('Casa C');" | Out-Null
  $p = Par $db "SELECT agregar_o_reemplazar_cedula(2, 'frente', repeat('7',32), 'image/jpeg', 1000);" "SELECT crear_contrato(2, 3, current_date, NULL);"
  $n = Sql $db "SELECT (SELECT count(*) FROM contrato WHERE inquilino_id=2 AND propiedad_id=3) || ':' || (SELECT count(*) FROM documento_identidad WHERE inquilino_id=2 AND cara='frente' AND eliminado_en IS NULL);" -Valor
  Concluye 'R26 concurrencia: crear el contrato mientras otra sesion reemplaza el frente se acepta sin esperar (el frente anterior sigue activo hasta confirmar)' (($p.A.Codigo -eq 0) -and ($p.B.Codigo -eq 0) -and ($p.B.Segundos -lt 2) -and ($n.Salida.Trim() -eq '1:1')) "reemplazo=$($p.A.Codigo) contrato=$($p.B.Codigo) espera=$($p.B.Segundos) s contratos:frentes_activos=$($n.Salida.Trim())"

  # 4b. R28 bajo concurrencia: un contrato con 9 fotografias; dos sesiones agregan a la vez (la 10 y la 11)
  Sql $db "INSERT INTO propiedad(alias) VALUES ('Casa D'); SELECT crear_contrato(3, (SELECT id FROM propiedad WHERE alias='Casa D'), current_date, NULL); SELECT agregar_fotografia_contrato((SELECT max(id) FROM contrato), repeat(to_hex(n),32), 'image/jpeg', 1000) FROM generate_series(1,9) n;" | Out-Null
  $cid = (Sql $db "SELECT max(id) FROM contrato;" -Valor).Salida.Trim()
  $p = Par $db "SELECT agregar_fotografia_contrato($cid, repeat('a',32), 'image/jpeg', 1000);" "SELECT agregar_fotografia_contrato($cid, repeat('b',32), 'image/jpeg', 1000);"
  $n = Sql $db "SELECT count(*) || ':' || max(orden) FROM documento_contrato WHERE contrato_id=$cid;" -Valor
  Concluye 'R28 concurrencia: con 9 fotografias, dos sesiones agregan a la vez; la primera registra la 10 y la segunda espera y la rechaza el servicio con el mensaje de R28' (($p.A.Codigo -eq 0) -and ($p.B.Codigo -ne 0) -and ($p.B.Segundos -ge 2) -and ($p.B.Error -match 'R28: el contrato ya tiene el maximo') -and ($n.Salida.Trim() -eq '10:10')) "primera=$($p.A.Codigo) segunda=$($p.B.Codigo) espera=$($p.B.Segundos) s mensaje=$(Primera $p.B.Error) filas:max_orden=$($n.Salida.Trim())"

  # 5. Patron del archivo huerfano (H19b): el archivo se escribe antes de la transaccion y se borra en la misma peticion si falla.
  #    Es el patron en PowerShell; no prueba Django ni el disco de produccion.
  $priv = Join-Path $raiz 'privado'; New-Item -ItemType Directory -Path $priv | Out-Null
  $refMal = '0' * 32
  Set-Content -Path (Join-Path $priv $refMal) -Value 'imagen simulada'
  $f = Sql $db "SELECT agregar_o_reemplazar_cedula(4, 'frente', '$refMal', 'image/jpeg', 1000);"   # Dani no tiene consentimiento: la transaccion falla
  if ($f.Codigo -ne 0) { Remove-Item (Join-Path $priv $refMal) }
  $fila = Sql $db "SELECT count(*) FROM documento_identidad WHERE referencia_archivo='$refMal';" -Valor
  Concluye 'H19b falla la transaccion: el archivo escrito se borra en la misma peticion y no queda fila' (($f.Codigo -ne 0) -and (-not (Test-Path (Join-Path $priv $refMal))) -and ($fila.Salida.Trim() -eq '0')) "codigo=$($f.Codigo) archivo_existe=$(Test-Path (Join-Path $priv $refMal)) filas=$($fila.Salida.Trim()) mensaje=$(Primera $f.Error)"
  $refBien = 'f' * 32
  Set-Content -Path (Join-Path $priv $refBien) -Value 'imagen simulada'
  $f = Sql $db "SELECT agregar_o_reemplazar_cedula(3, 'reverso', '$refBien', 'image/jpeg', 1000);"
  if ($f.Codigo -ne 0) { Remove-Item (Join-Path $priv $refBien) }
  $fila = Sql $db "SELECT count(*) FROM documento_identidad WHERE referencia_archivo='$refBien';" -Valor
  Concluye 'H19b si la transaccion se confirma, el archivo se conserva y hay una fila' (($f.Codigo -eq 0) -and (Test-Path (Join-Path $priv $refBien)) -and ($fila.Salida.Trim() -eq '1')) "codigo=$($f.Codigo) archivo_existe=$(Test-Path (Join-Path $priv $refBien)) filas=$($fila.Salida.Trim())"

  $out.Add('')
  $out.Add('== Pruebas de concurrencia y del archivo huerfano (sesiones reales de psql) ==')
  foreach ($c in $conc) { $out.Add((($(if ($c.Ok) { ' OK    ' } else { ' FALLA ' })) + $c.Prueba + ' | ' + $c.Detalle)) }
  $out.Add(("Concurrencia y archivo huerfano: {0} correctas, {1} fallas" -f @($conc | Where-Object Ok).Count, @($conc | Where-Object { -not $_.Ok }).Count))
}
finally {
  & "$bin\pg_ctl.exe" stop -D $datos -m fast 2>$null | Out-Null
  Start-Sleep -Milliseconds 500
  Remove-Item -Recurse -Force $raiz -ErrorAction SilentlyContinue
  $out.Add('Servidor detenido y directorio temporal borrado.')
  $out | Out-File -FilePath (Join-Path $aqui $Salida) -Encoding utf8
}
