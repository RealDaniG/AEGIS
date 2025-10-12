<#
 Configura y levanta un servicio oculto Tor (.onion) que expone el puerto local del chat.

 Uso manual:
   pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup_onion_service.ps1 -LocalPort 8000

 Requisitos:
   - Tor instalado y 'tor.exe' disponible en PATH (o en el sistema)
#>
param(
  [int]$LocalPort = 8000,
  [int]$SocksPort = 9060
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-OnionRoot {
  $base = Join-Path $env:LOCALAPPDATA 'TorHiddenService'
  New-Item -ItemType Directory -Force -Path $base | Out-Null
  return $base
}

$torRoot = Get-OnionRoot
$torrcPath = Join-Path $torRoot 'torrc'
$dataDir = Join-Path $torRoot 'data'
$hsDir = Join-Path $torRoot 'service'
$logPath = Join-Path $torRoot 'tor.log'

New-Item -ItemType Directory -Force -Path $dataDir | Out-Null
New-Item -ItemType Directory -Force -Path $hsDir | Out-Null

$torrc = @(
  "DataDirectory $dataDir",
  "HiddenServiceDir $hsDir",
  "HiddenServiceVersion 3",
  "HiddenServicePort 80 127.0.0.1:$LocalPort",
  "SocksPort 127.0.0.1:$SocksPort",
  "Log notice file $logPath"
) -join "`n"

# Escribir torrc en UTF-8 sin BOM para evitar errores de parseo en Tor
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText($torrcPath, $torrc, $utf8NoBom)
Write-Host "[INFO] torrc escrito en: $torrcPath (UTF-8 sin BOM)" -ForegroundColor Cyan

$torCmd = Get-Command tor.exe -ErrorAction SilentlyContinue
if (-not $torCmd) {
  Write-Host "[ERROR] No se encontró 'tor.exe'. Instala Tor (Tor Expert Bundle o Tor Browser) y agrega 'tor.exe' al PATH." -ForegroundColor Red
  Write-Host "Descarga: https://www.torproject.org/" -ForegroundColor Yellow
  exit 1
}

Write-Host "[STEP] Iniciando Tor con torrc..." -ForegroundColor Cyan
try {
  Start-Process -FilePath $torCmd.Source -ArgumentList "-f `"$torrcPath`"" -WindowStyle Hidden | Out-Null
} catch {
  Write-Host "[ERROR] No se pudo iniciar Tor: $($_.Exception.Message)" -ForegroundColor Red
  exit 1
}

# Esperar a que se genere el hostname
$hostnamePath = Join-Path $hsDir 'hostname'
Write-Host "[INFO] Esperando generación de .onion..." -ForegroundColor Cyan
for ($i=0; $i -lt 30; $i++) {
  if (Test-Path $hostnamePath) { break }
  Start-Sleep -Seconds 1
}

if (Test-Path $hostnamePath) {
  $onion = Get-Content $hostnamePath -Raw
  Write-Host "[OK] Servicio .onion listo: http://$onion/" -ForegroundColor Green
  Write-Host "[TIP] Accede desde Tor Browser o usa curl con --socks5-hostname 127.0.0.1:$SocksPort" -ForegroundColor Green
  Write-Host "[INFO] Esperando bootstrap de Tor (hasta 30s)..." -ForegroundColor Cyan
  for ($j=0; $j -lt 30; $j++) {
    if (Test-Path $logPath) {
      $tail = Get-Content $logPath -ErrorAction SilentlyContinue | Select-Object -Last 50
      if ($tail -match 'Bootstrapped 100%') { break }
    }
    Start-Sleep -Seconds 1
  }
  if (Test-Path $logPath) {
    $statusLine = (Get-Content $logPath | Select-Object -Last 1)
    Write-Host "[LOG] Última línea: $statusLine" -ForegroundColor DarkGray
  }
} else {
  Write-Host "[WARN] No se generó hostname. Verifica logs de Tor y que el puerto $LocalPort esté escuchando en 127.0.0.1" -ForegroundColor Yellow
}