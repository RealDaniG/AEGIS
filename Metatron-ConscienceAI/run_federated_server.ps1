# Arrancar servidor federado FastAPI (Uvicorn)

param(
  [string]$BindHost = "127.0.0.1",
  [int]$Port = 8000,
  [string]$Token = "change-me"
)

$ErrorActionPreference = "Stop"
Push-Location $PSScriptRoot
try {
  $env:FEDERATOR_TOKEN = $Token
  Write-Host "Iniciando servidor federado en http://$BindHost`:$Port" -ForegroundColor Cyan
  python -m uvicorn --app-dir scripts federated_server:app --host $BindHost --port $Port
} finally {
  Pop-Location
}