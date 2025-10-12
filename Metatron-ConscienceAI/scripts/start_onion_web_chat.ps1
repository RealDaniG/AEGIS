<#
 Orquesta el arranque de la Web UI de chat y la publicación del servicio .onion.

 Pasos:
 1) Inicia la Web UI (FastAPI + Uvicorn) en 127.0.0.1:5180
 2) Configura y levanta el servicio oculto Tor que publica la Web UI en .onion

 Uso:
   pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\start_onion_web_chat.ps1

 Requisitos:
   - Tor instalado y 'tor.exe' disponible en PATH (o Tor Browser)
   - Dependencias Python instaladas (fastapi, uvicorn, transformers, torch)
#>
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Robust path detection for different execution contexts
if ($PSScriptRoot) {
    $scriptsDir = $PSScriptRoot
} elseif ($PSCommandPath) {
    $scriptsDir = Split-Path -Parent $PSCommandPath
} else {
    $scriptsDir = Join-Path (Get-Location | Select-Object -ExpandProperty Path) "scripts"
}
$repoRoot = Split-Path -Parent $scriptsDir

Write-Host "[STEP] Comprobando si el servidor WebUI ya está activo en 127.0.0.1:5180 ..." -ForegroundColor Cyan
$tncWeb = Test-NetConnection -ComputerName 127.0.0.1 -Port 5180 -WarningAction SilentlyContinue
if (-not $tncWeb.TcpTestSucceeded) {
  Write-Host "[STEP] Iniciando Web Chat (run_web_chat.ps1) en 127.0.0.1:5180 ..." -ForegroundColor Cyan
  $runWebChatScript = Join-Path $repoRoot 'run_web_chat.ps1'
  if (Test-Path $runWebChatScript) {
    Start-Process pwsh -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$runWebChatScript`"" -WindowStyle Minimized | Out-Null
    Start-Sleep -Seconds 3
  } else {
    Write-Host "[ERROR] No se encontró run_web_chat.ps1 en $repoRoot" -ForegroundColor Red
    exit 1
  }
} else {
  Write-Host "[INFO] WebUI ya está escuchando en 127.0.0.1:5180, se omite arranque." -ForegroundColor Yellow
}

$setupScript = Join-Path $scriptsDir 'setup_onion_service.ps1'
if (Test-Path $setupScript) {
  $socksPort = 9060
  Write-Host "[STEP] Comprobando SOCKS de Tor en 127.0.0.1:$socksPort ..." -ForegroundColor Cyan
  $tncSocks = Test-NetConnection -ComputerName 127.0.0.1 -Port $socksPort -WarningAction SilentlyContinue
  if (-not $tncSocks.TcpTestSucceeded) {
    Write-Host "[STEP] Configurando servicio .onion para el puerto local 5180 (SocksPort $socksPort) ..." -ForegroundColor Cyan
    & pwsh -NoProfile -ExecutionPolicy Bypass -File $setupScript -LocalPort 5180 -SocksPort $socksPort
  } else {
    Write-Host "[INFO] Tor SOCKS ya activo en 127.0.0.1:$socksPort, se omite reconfiguración." -ForegroundColor Yellow
  }

  $hsHostname = Join-Path $env:LOCALAPPDATA 'TorHiddenService\service\hostname'
  if (Test-Path $hsHostname) {
    $onion = Get-Content $hsHostname -Raw
    Write-Host "[OK] Servicio .onion accesible: http://$onion/" -ForegroundColor Green
  } else {
    Write-Host "[WARN] No se encontró hostname .onion; verifica logs de Tor." -ForegroundColor Yellow
  }

  Write-Host "[TIP] Abre la WebUI en: http://<tu_onion>/ desde Tor Browser" -ForegroundColor Green
  Write-Host "[TIP] Si WebSocket falla en Tor Browser, desactiva 'Streaming' y usa el modo normal (HTTP)." -ForegroundColor Yellow
} else {
  Write-Host "[ERROR] No se encontró $setupScript" -ForegroundColor Red
  exit 1
}

Write-Host "[DONE] Web Chat levantado localmente y publicado en .onion (si Tor está instalado)." -ForegroundColor Green