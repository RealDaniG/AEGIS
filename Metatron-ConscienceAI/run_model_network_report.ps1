<#
 Genera un reporte rápido de estadísticas del modelo y de la red.
 Usa la misma lógica de selección de modelo que run_chat_full.ps1 para informar el modelo que se usará en el chat.
#>
param()
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-Root {
  if ($PSScriptRoot) { return $PSScriptRoot }
  elseif ($PSCommandPath) { return (Split-Path -Parent $PSCommandPath) }
  else { return (Get-Location).Path }
}

$root = Get-Root
Set-Location $root

$venvPy = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPy)) {
  Write-Host "[INFO] No se encontró .venv, ejecutando install.ps1..." -ForegroundColor Yellow
  & (Join-Path $root "install.ps1")
}

$modelFull = Join-Path $root "models\finetune_es_pdf_lm_full"
$modelLM = Join-Path $root "models\finetune_es_pdf_lm"
if (Test-Path $modelFull) {
  $modelPath = $modelFull
} elseif (Test-Path $modelLM) {
  $modelPath = $modelLM
} else {
  Write-Host "[WARN] No se encontró un modelo local afinado. Se usará 'distilgpt2' (requiere Internet)." -ForegroundColor Yellow
  $modelPath = "distilgpt2"
}

# Cargar server_url de node_config.json si existe
$serverUrl = ""
$cfgPath = Join-Path $root 'node_config.json'
if (Test-Path $cfgPath) {
  try {
    $cfg = Get-Content $cfgPath -Raw | ConvertFrom-Json
    if ($cfg.PSObject.Properties.Name -contains 'server_url') {
      $serverUrl = $cfg.server_url
    }
  } catch {
    Write-Host "[WARN] No se pudo leer node_config.json: $($_.Exception.Message)" -ForegroundColor Yellow
  }
}

Write-Host "[INFO] Generando reporte con el modelo: $modelPath" -ForegroundColor Cyan
& $venvPy (Join-Path $root "scripts\model_network_report.py") --model $modelPath --server-url $serverUrl --out (Join-Path $root "ai_runs\model_network_report.json") --skip-param-count