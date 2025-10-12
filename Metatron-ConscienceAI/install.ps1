<#
 Instalador sencillo para el proyecto Consciousness Engine (Windows/PowerShell)
 - Crea un entorno virtual (.venv)
 - Actualiza pip e instala dependencias desde requirements.txt
 - Muestra instrucciones para ejecutar los scripts de uso
#>

param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-Root {
  # Use robust path detection for different execution contexts
  if ($PSScriptRoot) { return $PSScriptRoot }
  elseif ($PSCommandPath) { return (Split-Path -Parent $PSCommandPath) }
  elseif ($MyInvocation.MyCommand.Path) { return (Split-Path -Parent $MyInvocation.MyCommand.Path) }
  else { return (Get-Location).Path }
}

$root = Get-Root
Write-Host "[INFO] Carpeta del proyecto:" $root
Set-Location $root

# Verificar Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
  Write-Host "[ERROR] No se encontró 'python' en el PATH. Instala Python 3.10+ y vuelve a ejecutar." -ForegroundColor Red
  exit 1
}

# Crear venv si no existe
if (-not (Test-Path "$root\.venv")) {
  Write-Host "[INFO] Creando entorno virtual (.venv)" -ForegroundColor Cyan
  python -m venv .venv
} else {
  Write-Host "[INFO] Entorno virtual ya existe (.venv)"
}

$venvPy = Join-Path $root ".venv\Scripts\python.exe"
$venvPip = Join-Path $root ".venv\Scripts\pip.exe"

Write-Host "[INFO] Actualizando pip" -ForegroundColor Cyan
& $venvPy -m pip install --upgrade pip

if (-not (Test-Path (Join-Path $root "requirements.txt"))) {
  Write-Host "[WARN] requirements.txt no encontrado. Creando uno mínimo..." -ForegroundColor Yellow
  @(
    'torch','transformers','datasets','peft','safetensors','accelerate','tqdm'
  ) | Out-File -FilePath (Join-Path $root "requirements.txt") -Encoding utf8
}

Write-Host "[INFO] Instalando dependencias" -ForegroundColor Cyan
& $venvPip install -r (Join-Path $root "requirements.txt")

Write-Host "[OK] Instalación completa." -ForegroundColor Green
Write-Host "\nPara iniciar el chat con el modelo entrenado, ejecuta:" -ForegroundColor Green
Write-Host "  .\\run_chat_full.ps1" -ForegroundColor Green
Write-Host "Para generar respuestas QA automáticamente, ejecuta:" -ForegroundColor Green
Write-Host "  .\\run_qa_generation.ps1" -ForegroundColor Green