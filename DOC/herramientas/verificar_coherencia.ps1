# Verifica la coherencia de la documentacion del SGA.
#
# Comprueba, sobre la ultima version de cada documento:
#   1. Que todo identificador citado (RF, RN, RNF, CA, OL, DP, ADR, RE) en la ERS, el DAS, el modelo de datos,
#      el diseno tecnico y la estrategia de pruebas este definido en la ERS o el DAS.
#   2. Que los enlaces relativos entre archivos .md existan.
#   3. Vigencia: README de cada fase y DOC/README.md marcan la ultima version, y el encabezado coincide con el nombre.
#   4. Base: los documentos que citan otra version (ERS, DAS, modelo de datos) citan la ultima.
#   5. Cobertura: cada RF, RN, RNF y CA definido en la ERS aparece en su matriz de trazabilidad (seccion 10).
#   6. Cobertura de pruebas: cada CA definido esta asignado en la tabla de cobertura de la estrategia de pruebas.
#   7. Que cada archivo .md de una carpeta de fase (menos el README) conste por nombre en el README de esa fase.
#
# No comprueba el contenido ni la logica: tras cambios de reglas, relee los documentos.
# Los identificadores locales HT-nn (diseno tecnico) y HP-nn (estrategia de pruebas) no se comprueban.
#
# Uso (desde cualquier carpeta):
#   powershell -File DOC\herramientas\verificar_coherencia.ps1
# Termina con codigo 1 si encuentra problemas.

$ErrorActionPreference = 'Stop'
$doc = Split-Path -Parent $PSScriptRoot
$problemas = 0
$guion = [string][char]0x2013   # raya usada en los rangos de la matriz (por ejemplo RF-21 a RF-25)

function Get-UltimaVersion([string]$carpeta, [string]$prefijo) {
    $clave = {
        $m = [regex]::Match($_.Name, '_v(\d+)\.(\d+)')
        [int]$m.Groups[1].Value * 1000 + [int]$m.Groups[2].Value
    }
    Get-ChildItem -Path (Join-Path $doc $carpeta) -Filter "${prefijo}_*.md" |
        Where-Object { [regex]::IsMatch($_.Name, '_v\d+\.\d+') } |
        Sort-Object $clave |
        Select-Object -Last 1
}

function Get-Version($archivo) { [regex]::Match($archivo.Name, '_v(\d+\.\d+)').Groups[1].Value }

$ers = Get-UltimaVersion 'fase-1-ers' 'ERS_SGA_001'
$das = Get-UltimaVersion 'fase-2-arquitectura' 'DAS_SGA_001'
$mdd = Get-UltimaVersion 'fase-3-diseno-tecnico' 'MODELO_DATOS_SGA_001'
$dte = Get-UltimaVersion 'fase-3-diseno-tecnico' 'DISENO_TECNICO_SGA_001'
$epp = Get-UltimaVersion 'fase-4-pruebas' 'ESTRATEGIA_PRUEBAS_SGA_001'
$pim = Get-UltimaVersion 'fase-5-implementacion' 'PLAN_IMPLEMENTACION_SGA_001'
$lrc = Get-UltimaVersion 'fase-5-implementacion' 'LISTA_REVISION_CRITICA_SGA_001'
if (-not $ers -or -not $das) { Write-Output 'ERROR: no se encontro la ERS o el DAS.'; exit 1 }
Write-Output "ERS: $($ers.Name)"
Write-Output "DAS: $($das.Name)"
if ($mdd) { Write-Output "MDD: $($mdd.Name) (se comprueban sus citas y su base)" }
if ($dte) { Write-Output "DTE: $($dte.Name) (se comprueban sus citas y su base)" }
if ($epp) { Write-Output "EPP: $($epp.Name) (se comprueban sus citas, su base y la cobertura de CA)" }
if ($lrc) { Write-Output "LRC: $($lrc.Name) (se comprueban sus citas, su base y su vigencia)" }
if ($pim) { Write-Output "PIM: $($pim.Name) (se comprueban sus citas, su base y que cada RF y CA conste una vez en sus entregas)" }

$archivos = @($ers, $das)
$texto = @{}
foreach ($a in $archivos) { $texto[$a.Name] = Get-Content -Path $a.FullName -Encoding UTF8 }
$otros = @($mdd, $dte, $epp, $pim, $lrc) | Where-Object { $_ }
$textoOtros = @{}
foreach ($o in $otros) { $textoOtros[$o.Name] = Get-Content -Path $o.FullName -Encoding UTF8 }

# 1. Definiciones: el identificador abre una linea, una fila de tabla o un titulo.
$prefijos = 'RNF', 'RF', 'RN', 'CA', 'OL', 'DP', 'ADR', 'RE'
$definidos = @{}
foreach ($p in $prefijos) {
    $defs = New-Object 'System.Collections.Generic.HashSet[string]'
    $refs = New-Object 'System.Collections.Generic.HashSet[string]'
    foreach ($a in $archivos) {
        foreach ($linea in $texto[$a.Name]) {
            if ($linea -match "^(\*\*|\| |### )$p-(\d+)\b") {
                [void]$defs.Add("$p-$($Matches[2])")
            }
            foreach ($m in [regex]::Matches($linea, "(?<![A-Z])$p-(\d+)")) { [void]$refs.Add($m.Value) }
        }
    }
    foreach ($o in $otros) {
        foreach ($linea in $textoOtros[$o.Name]) {
            foreach ($m in [regex]::Matches($linea, "(?<![A-Z])$p-(\d+)")) { [void]$refs.Add($m.Value) }
        }
    }
    $definidos[$p] = $defs
    $sinDefinir = @($refs | Where-Object { -not $defs.Contains($_) } | Sort-Object)
    if ($sinDefinir.Count -gt 0) {
        $problemas += $sinDefinir.Count
        Write-Output "[$p] citados sin definir: $($sinDefinir -join ', ')"
    } else {
        Write-Output "[$p] ok ($($defs.Count) definidos)"
    }
}

# 3. Vigencia: la ultima version de cada documento debe constar como vigente en su README y en DOC/README.md,
# su encabezado debe llevar la misma version que el nombre del archivo, y las versiones anteriores de la misma
# familia no deben figurar como vigentes.
$vigentes = @(
    @{ Doc = $ers; Carpeta = 'fase-1-ers'; Prefijo = 'ERS_SGA_001' },
    @{ Doc = $das; Carpeta = 'fase-2-arquitectura'; Prefijo = 'DAS_SGA_001' },
    @{ Doc = $mdd; Carpeta = 'fase-3-diseno-tecnico'; Prefijo = 'MODELO_DATOS_SGA_001' },
    @{ Doc = $dte; Carpeta = 'fase-3-diseno-tecnico'; Prefijo = 'DISENO_TECNICO_SGA_001' },
    @{ Doc = $epp; Carpeta = 'fase-4-pruebas'; Prefijo = 'ESTRATEGIA_PRUEBAS_SGA_001' },
    @{ Doc = $pim; Carpeta = 'fase-5-implementacion'; Prefijo = 'PLAN_IMPLEMENTACION_SGA_001' },
    @{ Doc = $lrc; Carpeta = 'fase-5-implementacion'; Prefijo = 'LISTA_REVISION_CRITICA_SGA_001' }
)
$readmeRaiz = Get-Content -Path (Join-Path $doc 'README.md') -Raw -Encoding UTF8
foreach ($v in $vigentes) {
    if (-not $v.Doc) { continue }
    $nombre = $v.Doc.Name
    $version = Get-Version $v.Doc
    $readme = Get-Content -Path (Join-Path $doc "$($v.Carpeta)\README.md") -Encoding UTF8
    $marcada = @($readme | Where-Object { $_ -match [regex]::Escape($nombre) -and $_ -match 'vigente' })
    if ($marcada.Count -eq 0) { $problemas++; Write-Output "[vigencia] $($v.Carpeta)/README.md no marca $nombre como vigente." }
    $otras = @($readme | Where-Object { $_ -match 'vigente' -and $_ -match [regex]::Escape($v.Prefijo) -and $_ -notmatch [regex]::Escape($nombre) })
    if ($otras.Count -gt 0) { $problemas++; Write-Output "[vigencia] $($v.Carpeta)/README.md marca como vigente otra version: $($otras[0].Trim())" }
    if (-not $readmeRaiz.Contains($nombre)) { $problemas++; Write-Output "[vigencia] DOC/README.md no cita $nombre." }
    $enc = (Get-Content -Path $v.Doc.FullName -Encoding UTF8 -TotalCount 12) -join "`n"
    if ($enc -notmatch "Versi.n:\*\*\s*$([regex]::Escape($version))\b") { $problemas++; Write-Output "[vigencia] el encabezado de $nombre no declara la version $version." }
}

# 4. Base: lo que cada documento declara como base en su encabezado debe ser la ultima version.
$bases = @(
    @{ Doc = $das; Cita = @('ERS') },
    @{ Doc = $mdd; Cita = @('ERS', 'DAS') },
    @{ Doc = $dte; Cita = @('ERS', 'DAS', 'MDD') },
    @{ Doc = $epp; Cita = @('ERS', 'DAS') },
    @{ Doc = $pim; Cita = @('ERS', 'DAS', 'MDD') },
    @{ Doc = $lrc; Cita = @('ERS', 'DAS', 'MDD') }
)
$ultimas = @{ ERS = Get-Version $ers; DAS = Get-Version $das }
if ($mdd) { $ultimas['MDD'] = Get-Version $mdd }
foreach ($b in $bases) {
    if (-not $b.Doc) { continue }
    $lineas = @(Get-Content -Path $b.Doc.FullName -Encoding UTF8 -TotalCount 14 | Where-Object { $_ -match '(Base:|de referencia:)' })
    foreach ($sigla in $b.Cita) {
        $citadas = @()
        foreach ($l in $lineas) {
            foreach ($m in [regex]::Matches($l, "(?<![A-Z])$sigla(?:-SGA-001)?\]?[^v\n]{0,40}?v(\d+\.\d+)")) { $citadas += $m.Groups[1].Value }
        }
        if ($citadas.Count -eq 0) { continue }
        foreach ($c in ($citadas | Sort-Object -Unique)) {
            if ($c -ne $ultimas[$sigla]) {
                $problemas++
                Write-Output "[base] $($b.Doc.Name) cita $sigla v$c como base y la ultima es v$($ultimas[$sigla])."
            }
        }
    }
}

# 5. Cobertura de la matriz de trazabilidad de la ERS (seccion 10): cada RF, RN, RNF y CA definido debe aparecer.
$lineasErs = $texto[$ers.Name]
$ini = -1; $fin = $lineasErs.Count
for ($i = 0; $i -lt $lineasErs.Count; $i++) {
    if ($lineasErs[$i] -match '^# 10\. Matriz') { $ini = $i }
    elseif ($ini -ge 0 -and $lineasErs[$i] -match '^# 11\.') { $fin = $i; break }
}
if ($ini -lt 0) {
    $problemas++; Write-Output '[matriz] no se encontro la seccion 10 (Matriz de trazabilidad) en la ERS.'
} else {
    $matriz = ($lineasErs[$ini..($fin - 1)]) -join "`n"
    foreach ($p in 'RF', 'RN', 'RNF', 'CA') {
        $cubiertos = New-Object 'System.Collections.Generic.HashSet[int]'
        $patron = "(?<![A-Z])$p-(\d+)(?:\s*[$guion-]\s*(?:$p-)?(\d+))?"
        foreach ($m in [regex]::Matches($matriz, $patron)) {
            $a = [int]$m.Groups[1].Value
            $z = if ($m.Groups[2].Success) { [int]$m.Groups[2].Value } else { $a }
            if ($z -ge $a -and ($z - $a) -lt 100) { foreach ($n in $a..$z) { [void]$cubiertos.Add($n) } }
        }
        $sinMatriz = @($definidos[$p] | Where-Object { -not $cubiertos.Contains([int]($_ -replace '^[A-Z]+-', '')) } | Sort-Object)
        if ($sinMatriz.Count -gt 0) {
            $problemas += $sinMatriz.Count
            Write-Output "[matriz] $p sin aparecer en la matriz: $($sinMatriz -join ', ')"
        } else {
            Write-Output "[matriz] $p ok ($($definidos[$p].Count) en la matriz)"
        }
    }
}

# 6. Cobertura de CA en la estrategia de pruebas: filas de la tabla con la forma "| area | CA-01, 25 (L), 29 | nivel | prioridad |".
if ($epp) {
    $asignados = New-Object 'System.Collections.Generic.HashSet[int]'
    foreach ($l in $textoOtros[$epp.Name]) {
        if ($l -match '^\|[^|]*\|\s*(CA-[^|]+)\|') {
            $celda = $Matches[1] -replace '\(L\)', ''
            foreach ($m in [regex]::Matches($celda, '\d+')) { [void]$asignados.Add([int]$m.Value) }
        }
    }
    $sinAsignar = @($definidos['CA'] | Where-Object { -not $asignados.Contains([int]($_ -replace '^CA-', '')) } | Sort-Object)
    if ($sinAsignar.Count -gt 0) {
        $problemas += $sinAsignar.Count
        Write-Output "[pruebas] CA sin asignar en $($epp.Name): $($sinAsignar -join ', ')"
    } else {
        Write-Output "[pruebas] CA ok ($($definidos['CA'].Count) asignados)"
    }
}

# 8. Plan de implementacion: cada RF y cada CA definido consta exactamente una vez en la tabla de entregas
# (filas "| E0 ... |" y "| Posterior ... |", con las columnas de RF en la quinta celda y de CA en la septima).
if ($pim) {
    $rfPlan = @{}; $caPlan = @{}
    foreach ($l in $textoOtros[$pim.Name]) {
        if ($l -match '^\| (E\d|Posterior) ') {
            $celdas = $l.Split('|')
            if ($celdas.Count -lt 8) { continue }
            foreach ($m in [regex]::Matches($celdas[4], '\d+')) { $k = [int]$m.Value; $rfPlan[$k] = 1 + [int]$rfPlan[$k] }
            foreach ($m in [regex]::Matches($celdas[6], '\d+')) { $k = [int]$m.Value; $caPlan[$k] = 1 + [int]$caPlan[$k] }
        }
    }
    foreach ($par in @(@('RF', $rfPlan), @('CA', $caPlan))) {
        $p = $par[0]; $mapa = $par[1]
        $faltan = @($definidos[$p] | Where-Object { -not $mapa.ContainsKey([int]($_ -replace '^[A-Z]+-', '')) } | Sort-Object)
        $repetidos = @($mapa.Keys | Where-Object { $mapa[$_] -gt 1 } | Sort-Object | ForEach-Object { "$p-$_" })
        if ($faltan.Count -gt 0) { $problemas += $faltan.Count; Write-Output "[plan] $p sin entrega en $($pim.Name): $($faltan -join ', ')" }
        if ($repetidos.Count -gt 0) { $problemas += $repetidos.Count; Write-Output "[plan] $p en mas de una entrega: $($repetidos -join ', ')" }
        if ($faltan.Count -eq 0 -and $repetidos.Count -eq 0) { Write-Output "[plan] $p ok ($($definidos[$p].Count) con una entrega)" }
    }
}

# 9. Registro de avance: cada entrega del plan consta con un estado valido y, como maximo, una esta en curso o bloqueada.
$avance = Join-Path (Join-Path $doc 'fase-5-implementacion') 'AVANCE_IMPLEMENTACION.md'
if ($pim -and (Test-Path -LiteralPath $avance)) {
    $estadosValidos = 'no iniciada', 'en curso', 'terminada', 'bloqueada'
    $entregasPlan = @()
    foreach ($l in $textoOtros[$pim.Name]) { if ($l -match '^\| (E\d) ') { $entregasPlan += $Matches[1] } }
    $entregasAvance = @{}
    foreach ($l in (Get-Content -Path $avance -Encoding UTF8)) {
        if ($l -match '^\| (E\d) ') {
            $clave = $Matches[1]
            $estado = ($l.Split('|')[2]).Trim()
            $entregasAvance[$clave] = $estado
        }
    }
    foreach ($e in $entregasPlan) {
        if (-not $entregasAvance.ContainsKey($e)) { $problemas++; Write-Output "[avance] $e no consta en AVANCE_IMPLEMENTACION.md." }
        elseif ($estadosValidos -notcontains $entregasAvance[$e]) { $problemas++; Write-Output "[avance] $e tiene un estado no valido: '$($entregasAvance[$e])'." }
    }
    $activas = @($entregasAvance.Keys | Where-Object { $entregasAvance[$_] -eq 'en curso' -or $entregasAvance[$_] -eq 'bloqueada' })
    if ($activas.Count -gt 1) { $problemas++; Write-Output "[avance] mas de una entrega en curso o bloqueada: $($activas -join ', ')." }
    if (($entregasAvance.Count -gt 0) -and ($problemas -eq 0 -or $true)) { Write-Output "[avance] $($entregasAvance.Count) entregas registradas, $($activas.Count) en curso o bloqueada" }
}

# 7. Cada archivo .md de una carpeta de fase consta por nombre en el README de la carpeta.
foreach ($carpeta in 'fase-1-ers', 'fase-2-arquitectura', 'fase-3-diseno-tecnico', 'fase-4-pruebas', 'fase-5-implementacion') {
    $ruta = Join-Path $doc $carpeta
    $textoReadme = Get-Content -Path (Join-Path $ruta 'README.md') -Raw -Encoding UTF8
    foreach ($f in (Get-ChildItem -Path $ruta -Filter '*.md' | Where-Object { $_.Name -ne 'README.md' })) {
        if (-not $textoReadme.Contains($f.Name)) {
            $problemas++
            Write-Output "[readme] $carpeta/README.md no lista $($f.Name)."
        }
    }
}

# Cada actualizacion lleva CAMBIOS.md; una carpeta EN-CURSO se avisa (no es error mientras haya trabajo abierto).
Get-ChildItem -Path (Join-Path $doc 'actualizaciones') -Directory | ForEach-Object {
    if (-not (Test-Path -LiteralPath (Join-Path $_.FullName 'CAMBIOS.md'))) { $problemas++; Write-Output "[actualizacion] $($_.Name) no tiene CAMBIOS.md." }
    if ($_.Name -match 'EN-CURSO') { Write-Output "[aviso] la actualizacion $($_.Name) sigue en curso." }
}

# 2. Enlaces relativos entre archivos .md.
$mds = Get-ChildItem -Path $doc -Recurse -Filter '*.md'
foreach ($f in $mds) {
    $dir = Split-Path -Parent $f.FullName
    $contenido = Get-Content -Path $f.FullName -Raw -Encoding UTF8
    foreach ($m in [regex]::Matches($contenido, '\]\(([^)#\s]+\.md)\)')) {
        $destino = $m.Groups[1].Value
        if ($destino -match '^https?:') { continue }
        if (-not (Test-Path -LiteralPath (Join-Path $dir $destino))) {
            $problemas++
            Write-Output "[enlace roto] $($f.FullName.Substring($doc.Length + 1)) -> $destino"
        }
    }
}

if ($problemas -eq 0) { Write-Output 'RESULTADO: sin problemas.'; exit 0 }
Write-Output "RESULTADO: $problemas problema(s)."
exit 1
