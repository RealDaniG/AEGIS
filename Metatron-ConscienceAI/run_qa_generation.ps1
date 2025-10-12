<#
 Genera respuestas automáticas para el dataset QA usando el modelo entrenado completo.
 Si no existe el entorno virtual, invoca install.ps1 automáticamente.
#>
param()
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-Root {
  $scriptPath = $MyInvocation.MyCommand.Path
  return Split-Path -Parent $scriptPath
}

$root = Get-Root
Set-Location $root

if (-not (Test-Path "$root\.venv")) {
  Write-Host "[INFO] No se encontró .venv, ejecutando install.ps1..." -ForegroundColor Yellow
  & (Join-Path $root "install.ps1")
}

$venvPy = Join-Path $root ".venv\Scripts\python.exe"

$modelFull = Join-Path $root "consciousness_engine\models\finetune_es_pdf_lm_full"
$inputQA  = Join-Path $root "consciousness_engine\datasets\pdf_es_qa.jsonl"
$outputQA = Join-Path $root "consciousness_engine\datasets\pdf_es_qa_filled.jsonl"

if (-not (Test-Path $modelFull)) {
  Write-Host "[ERROR] No se encontró el modelo completo: $modelFull" -ForegroundColor Red
  Write-Host "Ejecuta primero el entrenamiento completo o coloca el modelo en esa ruta."
  exit 1
}

if (-not (Test-Path $inputQA)) {
  Write-Host "[ERROR] No se encontró el dataset QA: $inputQA" -ForegroundColor Red
  exit 1
}

Write-Host "[INFO] Generando respuestas QA..." -ForegroundColor Cyan
& $venvPy (Join-Path $root "consciousness_engine\scripts\generate_qa_responses.py") --model $modelFull --input $inputQA --output $outputQA --max-input-tokens 768 --max-new-tokens 160 --temperature 0.7 --top-p 0.9
Write-Host "[OK] Proceso de generación finalizado. Salida: $outputQA" -ForegroundColor Green