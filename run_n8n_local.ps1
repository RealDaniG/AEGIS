<#
Arranque y gestión de n8n local en Windows (Docker Desktop requerido).

Uso:
  - Ejecuta en PowerShell: ./run_n8n_local.ps1 start
  - Para ver estado:        ./run_n8n_local.ps1 status
  - Para parar:             ./run_n8n_local.ps1 stop
  - Para reiniciar:         ./run_n8n_local.ps1 restart

Variables:
  - Usuario y contraseña de Basic Auth ajustables abajo.
  - Persistencia en carpeta ./n8n_data

Requisitos:
  - Tener Docker Desktop instalado y corriendo.
  - Puerto 5678 libre (UI y webhooks de n8n).
#>

param(
  [Parameter(Mandatory=$true)][ValidateSet('start','stop','status','restart')]
  [string]$action
)

$ErrorActionPreference = 'Stop'

$containerName = 'n8n-local'
$basicAuthUser = 'admin'
$basicAuthPass = 'ChangeMe123!'   # Cambia esta clave para producción

function Ensure-DataDir {
  if (-not (Test-Path -Path "n8n_data")) {
    New-Item -ItemType Directory -Force -Path "n8n_data" | Out-Null
  }
}

function Start-N8N {
  Ensure-DataDir
  Write-Host "Descargando imagen n8nio/n8n:latest…"
  docker pull n8nio/n8n:latest

  if ((docker ps -a --format ".Names" | Select-String -Pattern "^$containerName$")) {
    Write-Host "El contenedor ya existe; eliminando previo…"
    docker stop $containerName | Out-Null
    docker rm $containerName | Out-Null
  }

  Write-Host "Lanzando $containerName en http://127.0.0.1:5678 (Basic Auth)…"
  $env:N8N_BASIC_AUTH_USER = $basicAuthUser
  $env:N8N_BASIC_AUTH_PASSWORD = $basicAuthPass

  docker run -d --name $containerName --restart unless-stopped `
    -p 5678:5678 `
    -e N8N_BASIC_AUTH_ACTIVE=true `
    -e N8N_BASIC_AUTH_USER=$env:N8N_BASIC_AUTH_USER `
    -e N8N_BASIC_AUTH_PASSWORD=$env:N8N_BASIC_AUTH_PASSWORD `
    -e N8N_HOST=127.0.0.1 `
    -e N8N_PORT=5678 `
    -e N8N_PROTOCOL=http `
    -e WEBHOOK_URL=http://127.0.0.1:5678 `
    -v "${pwd}\n8n_data:/home/node/.n8n" `
    n8nio/n8n:latest | Out-Null

  Write-Host "n8n arrancado. Accede a: http://127.0.0.1:5678 (usuario: $basicAuthUser)" -ForegroundColor Green
}

function Stop-N8N {
  if ((docker ps -a --format ".Names" | Select-String -Pattern "^$containerName$")) {
    docker stop $containerName | Out-Null
    Write-Host "Contenedor detenido." -ForegroundColor Yellow
  } else {
    Write-Host "Contenedor no existe." -ForegroundColor Red
  }
}

function Status-N8N {
  docker ps --filter name=$containerName --format "table .Names`t.Status`t.Ports"
}

switch ($action) {
  'start'   { Start-N8N }
  'stop'    { Stop-N8N }
  'status'  { Status-N8N }
  'restart' { Stop-N8N; Start-N8N }
}