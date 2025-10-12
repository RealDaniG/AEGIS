<#
 Rotación segura de token para el nodo federado

 Uso:
   pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\rotate_token.ps1 -NewToken "NUEVO_TOKEN" [-TaskName "ConsciousnessEngineCompute"] [-ConfigPath "ruta\node_config.json"] [-TestConnectivity] [-DryRun]

 Qué hace:
   1) (Opcional) Deshabilita la tarea programada diaria.
   2) Actualiza el campo "token" en node_config.json, creando copia de seguridad.
   3) (Opcional) Ejecuta test de conectividad .onion vía Tor.
   4) (Opcional) Rehabilita la tarea programada.

 Requisitos:
   - PowerShell 7+
   - Permisos para administrar tareas programadas (si se usan Disable/Enable-ScheduledTask)
#>
param(
  [Parameter(Mandatory=$true)][string]$NewToken,
  [string]$TaskName = "ConsciousnessEngineCompute",
  [string]$ConfigPath,
  [switch]$TestConnectivity,
  [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-ProjectRoot {
  if ($PSScriptRoot) { return (Split-Path -Parent $PSScriptRoot) }
  return (Get-Location)
}

function Write-Info([string]$msg) { Write-Host $msg -ForegroundColor Cyan }
function Write-Ok([string]$msg)   { Write-Host $msg -ForegroundColor Green }
function Write-Warn([string]$msg) { Write-Host $msg -ForegroundColor Yellow }
function Write-Err([string]$msg)  { Write-Host $msg -ForegroundColor Red }

$root = Get-ProjectRoot
if (-not $ConfigPath) { $ConfigPath = Join-Path $root 'node_config.json' }

Write-Info "[STEP] Iniciando rotación de token"
Write-Host " ConfigPath: $ConfigPath"
Write-Host " TaskName:   $TaskName"
Write-Host " DryRun:     $($DryRun.IsPresent)"

if (-not (Test-Path $ConfigPath)) {
  Write-Err "[ERROR] No se encontró $ConfigPath"
  exit 1
}

# 1) Deshabilitar tarea programada (si existe)
try {
  $task = $null
  try { $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction Stop } catch {}
  if ($null -ne $task) {
    Write-Info "[STEP] Deshabilitando tarea programada '$TaskName'"
    if (-not $DryRun) {
      try {
        Disable-ScheduledTask -TaskName $TaskName -ErrorAction Stop | Out-Null
      } catch {
        Write-Warn "[WARN] Disable-ScheduledTask falló, probando schtasks.exe"
        & schtasks.exe /Change /TN $TaskName /DISABLE | Out-Null
      }
    } else {
      Write-Warn "[DRYRUN] Saltando deshabilitar tarea"
    }
  } else {
    Write-Warn "[INFO] Tarea '$TaskName' no encontrada; se continúa sin deshabilitar."
  }
} catch {
  Write-Warn "[WARN] No se pudo deshabilitar la tarea: $($_.Exception.Message)"
}

# 2) Actualizar node_config.json
Write-Info "[STEP] Actualizando token en node_config.json"
$cfgJson = Get-Content $ConfigPath -Raw
try { $cfg = $cfgJson | ConvertFrom-Json } catch { Write-Err "[ERROR] node_config.json no es JSON válido: $($_.Exception.Message)"; exit 1 }

$oldToken = $cfg.token
Write-Host " Token actual:    $([string]::IsNullOrEmpty($oldToken) ? '<vacío>' : '<oculto>')"
Write-Host " Token nuevo:     <oculto>"

# Backup
$backupPath = "$ConfigPath.bak." + (Get-Date -Format 'yyyyMMdd_HHmm')
if (-not $DryRun) {
  Copy-Item -LiteralPath $ConfigPath -Destination $backupPath -Force
  Write-Host " Copia de seguridad: $backupPath"
} else {
  Write-Warn "[DRYRUN] Saltando copia de seguridad"
}

$cfg.token = $NewToken
if (-not $DryRun) {
  ($cfg | ConvertTo-Json -Depth 6) | Set-Content -LiteralPath $ConfigPath -Encoding UTF8
  Write-Ok "[OK] Token actualizado en $ConfigPath"
} else {
  Write-Warn "[DRYRUN] No se escribe el archivo. Mostraría nuevo contenido si no fuera secreto."
}

# 3) Test de conectividad .onion vía Tor (opcional)
if ($TestConnectivity) {
  Write-Info "[STEP] Probando conectividad .onion (/list)"
  try {
    if (-not $DryRun) {
      & pwsh -NoProfile -ExecutionPolicy Bypass -File (Join-Path $root 'scripts\test_onion_connectivity.ps1')
      if ($LASTEXITCODE -ne 0) { Write-Warn "[WARN] Conectividad .onion fallida (exit $LASTEXITCODE)." }
    } else {
      Write-Warn "[DRYRUN] Saltando test de conectividad"
    }
  } catch {
    Write-Warn "[WARN] Error al ejecutar test_onion_connectivity.ps1: $($_.Exception.Message)"
  }
}

# 4) Rehabilitar tarea programada (si existía)
try {
  $task = $null
  try { $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction Stop } catch {}
  if ($null -ne $task) {
    Write-Info "[STEP] Habilitando tarea programada '$TaskName'"
    if (-not $DryRun) {
      try {
        Enable-ScheduledTask -TaskName $TaskName -ErrorAction Stop | Out-Null
      } catch {
        Write-Warn "[WARN] Enable-ScheduledTask falló, probando schtasks.exe"
        & schtasks.exe /Change /TN $TaskName /ENABLE | Out-Null
      }
    } else {
      Write-Warn "[DRYRUN] Saltando habilitar tarea"
    }
  }
} catch {
  Write-Warn "[WARN] No se pudo habilitar la tarea: $($_.Exception.Message)"
}

Write-Ok "[DONE] Rotación de token completada."