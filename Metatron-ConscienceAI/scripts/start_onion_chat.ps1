<#
 Orquesta el arranque del servidor de chat y la publicación del servicio .onion.

 Pasos:
 1) Inicia el servidor federado (chat) en 127.0.0.1:8000
 2) Configura y levanta el servicio oculto Tor que publica el chat en .onion

 Uso:
   pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\start_onion_chat.ps1
#>
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Robust path detection for different execution contexts
if ($PSScriptRoot) {
    $repoRoot = Split-Path -Parent $PSScriptRoot
} elseif ($PSCommandPath) {
    $repoRoot = Split-Path -Parent $PSCommandPath
} else {
    $repoRoot = Get-Location | Select-Object -ExpandProperty Path
}
if (Test-Path (Join-Path $repoRoot 'run_federated_server.ps1')) {
  Write-Host "[STEP] Iniciando servidor de chat (run_federated_server.ps1)..." -ForegroundColor Cyan
  Start-Process pwsh -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$(Join-Path $repoRoot 'run_federated_server.ps1')`"" -WindowStyle Minimized | Out-Null
} else {
  Write-Host "[ERROR] No se encontró run_federated_server.ps1 en $repoRoot" -ForegroundColor Red
  exit 1
}

Start-Sleep -Seconds 2

$setupScript = Join-Path $repoRoot 'scripts\setup_onion_service.ps1'
if (Test-Path $setupScript) {
  Write-Host "[STEP] Configurando servicio .onion..." -ForegroundColor Cyan
  & pwsh -NoProfile -ExecutionPolicy Bypass -File $setupScript -LocalPort 8000
} else {
  Write-Host "[ERROR] No se encontró $setupScript" -ForegroundColor Red
  exit 1
}

Write-Host "[DONE] Chat levantado localmente y publicado en .onion (si Tor está instalado)." -ForegroundColor Green