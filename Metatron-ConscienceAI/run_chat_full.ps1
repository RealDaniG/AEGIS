<#
 Ejecuta el chat interactivo con el modelo español afinado.
 Si no existe el entorno virtual, invoca install.ps1 automáticamente.
#>
param()
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-Root {
  # Usar variables modernas para obtener la ruta del script de forma robusta
  if ($PSScriptRoot) { return $PSScriptRoot }
  elseif ($PSCommandPath) { return (Split-Path -Parent $PSCommandPath) }
  else { return (Get-Location).Path }
}

$root = Get-Root
Set-Location $root

if (-not (Test-Path "$root\.venv")) {
  Write-Host "[INFO] No se encontró .venv, ejecutando install.ps1..." -ForegroundColor Yellow
  & (Join-Path $root "install.ps1")
}

$venvPy = Join-Path $root ".venv\Scripts\python.exe"

$modelFull = Join-Path $root "models\finetune_es_pdf_lm_full"
$modelLM = Join-Path $root "models\finetune_es_pdf_lm"
$outDir = "ai_chat_es_pdf_full"

if (Test-Path $modelFull) {
  $modelPath = $modelFull
} elseif (Test-Path $modelLM) {
  $modelPath = $modelLM
} else {
  Write-Host "[WARN] No se encontró un modelo local afinado. Se usará 'distilgpt2' (requiere Internet)." -ForegroundColor Yellow
  $modelPath = "distilgpt2"
}

Write-Host "[INFO] Iniciando chat con el modelo: $modelPath" -ForegroundColor Cyan
& $venvPy (Join-Path $root "scripts\ai_adapter_llm.py") --chat --model $modelPath --out-dir $outDir --noise 0.35 --phase-step 0.45 --max-context-tokens 1024 --persist-memory --rag-corpus "datasets/rss_research.jsonl" --rag-top-k 3 --rag-max-chars 1200