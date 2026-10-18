# Verifica la coherencia de la documentacion del SGA.
#
# Comprueba, sobre la ultima version de la ERS y del DAS:
#   1. Que todo identificador citado (RF, RN, RNF, CA, OL, DP, ADR) este definido.
#   2. Que los enlaces relativos entre archivos .md existan.
#
# Uso (desde cualquier carpeta):
#   powershell -File DOC\herramientas\verificar_coherencia.ps1
# Termina con codigo 1 si encuentra problemas.

$ErrorActionPreference = 'Stop'
$doc = Split-Path -Parent $PSScriptRoot
$problemas = 0

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

$ers = Get-UltimaVersion 'fase-1-ers' 'ERS_SGA_001'
$das = Get-UltimaVersion 'fase-2-arquitectura' 'DAS_SGA_001'
$mdd = Get-UltimaVersion 'fase-3-diseno-tecnico' 'MODELO_DATOS_SGA_001'
if (-not $ers -or -not $das) { Write-Output 'ERROR: no se encontro la ERS o el DAS.'; exit 1 }
Write-Output "ERS: $($ers.Name)"
Write-Output "DAS: $($das.Name)"
if ($mdd) { Write-Output "MDD: $($mdd.Name) (solo se comprueban sus citas)" }

$archivos = @($ers, $das)
$texto = @{}
foreach ($a in $archivos) { $texto[$a.Name] = Get-Content -Path $a.FullName -Encoding UTF8 }

# Definiciones: el identificador abre una linea, una fila de tabla o un titulo.
$prefijos = 'RNF', 'RF', 'RN', 'CA', 'OL', 'DP', 'ADR', 'RE'
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
    if ($mdd) {
        foreach ($linea in (Get-Content -Path $mdd.FullName -Encoding UTF8)) {
            foreach ($m in [regex]::Matches($linea, "(?<![A-Z])$p-(\d+)")) { [void]$refs.Add($m.Value) }
        }
    }
    $sinDefinir = @($refs | Where-Object { -not $defs.Contains($_) } | Sort-Object)
    if ($sinDefinir.Count -gt 0) {
        $problemas += $sinDefinir.Count
        Write-Output "[$p] citados sin definir: $($sinDefinir -join ', ')"
    } else {
        Write-Output "[$p] ok ($($defs.Count) definidos)"
    }
}

# Vigencia: la ultima version de cada documento debe constar como vigente en su README y en DOC/README.md,
# su encabezado debe llevar la misma version que el nombre del archivo, y las versiones anteriores no deben figurar como vigentes.
$vigentes = @(
    @{ Doc = $ers; Carpeta = 'fase-1-ers' },
    @{ Doc = $das; Carpeta = 'fase-2-arquitectura' },
    @{ Doc = $mdd; Carpeta = 'fase-3-diseno-tecnico' }
)
$readmeRaiz = Get-Content -Path (Join-Path $doc 'README.md') -Raw -Encoding UTF8
foreach ($v in $vigentes) {
    if (-not $v.Doc) { continue }
    $nombre = $v.Doc.Name
    $version = [regex]::Match($nombre, '_v(\d+\.\d+)').Groups[1].Value
    $readme = Get-Content -Path (Join-Path $doc "$($v.Carpeta)\README.md") -Encoding UTF8
    $marcada = @($readme | Where-Object { $_ -match [regex]::Escape($nombre) -and $_ -match 'Vigente' })
    if ($marcada.Count -eq 0) { $problemas++; Write-Output "[vigencia] $($v.Carpeta)/README.md no marca $nombre como vigente." }
    $otras = @($readme | Where-Object { $_ -match 'Vigente' -and $_ -notmatch [regex]::Escape($nombre) })
    if ($otras.Count -gt 0) { $problemas++; Write-Output "[vigencia] $($v.Carpeta)/README.md marca como vigente otra version: $($otras[0].Trim())" }
    if (-not $readmeRaiz.Contains($nombre)) { $problemas++; Write-Output "[vigencia] DOC/README.md no cita $nombre." }
    $enc = (Get-Content -Path $v.Doc.FullName -Encoding UTF8 -TotalCount 12) -join "`n"
    if ($enc -notmatch "Versi.n:\*\*\s*$([regex]::Escape($version))\b") { $problemas++; Write-Output "[vigencia] el encabezado de $nombre no declara la version $version." }
}

# Cada actualizacion lleva CAMBIOS.md; una carpeta EN-CURSO se avisa (no es error mientras haya trabajo abierto).
Get-ChildItem -Path (Join-Path $doc 'actualizaciones') -Directory | ForEach-Object {
    if (-not (Test-Path -LiteralPath (Join-Path $_.FullName 'CAMBIOS.md'))) { $problemas++; Write-Output "[actualizacion] $($_.Name) no tiene CAMBIOS.md." }
    if ($_.Name -match 'EN-CURSO') { Write-Output "[aviso] la actualizacion $($_.Name) sigue en curso." }
}

# Enlaces relativos entre archivos .md.
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
