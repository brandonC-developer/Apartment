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
if (-not $ers -or -not $das) { Write-Output 'ERROR: no se encontro la ERS o el DAS.'; exit 1 }
Write-Output "ERS: $($ers.Name)"
Write-Output "DAS: $($das.Name)"

$archivos = @($ers, $das)
$texto = @{}
foreach ($a in $archivos) { $texto[$a.Name] = Get-Content -Path $a.FullName -Encoding UTF8 }

# Definiciones: el identificador abre una linea, una fila de tabla o un titulo.
$prefijos = 'RNF', 'RF', 'RN', 'CA', 'OL', 'DP', 'ADR'
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
    $sinDefinir = @($refs | Where-Object { -not $defs.Contains($_) } | Sort-Object)
    if ($sinDefinir.Count -gt 0) {
        $problemas += $sinDefinir.Count
        Write-Output "[$p] citados sin definir: $($sinDefinir -join ', ')"
    } else {
        Write-Output "[$p] ok ($($defs.Count) definidos)"
    }
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
