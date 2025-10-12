# Ejecuta el ciclo de ingesta RSS y actualiza métricas y autogestión de feeds.
# Úsalo manualmente o prográmalo en el Programador de tareas de Windows.

$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot
try {
  Write-Host "[RSS] Iniciando ingesta..." -ForegroundColor Cyan
  $python = "python"

  $argsList = @(
    "--feeds", ".\datasets\rss_feeds.json",
    "--out", ".\datasets\rss_research.jsonl",
    "--stats", ".\ai_runs\rss_stats.json",
    "--languages", "es,en",
    "--topics", "ia;inteligencia artificial;machine learning;ml;física cuántica;neurociencia",
    "--max-items-per-feed", "50",
    "--auto-manage"
  )
  & $python .\scripts\rss_ingest.py @argsList

  Write-Host "[RSS] Ingesta finalizada." -ForegroundColor Green
} finally {
  Pop-Location
}

# Para programar:
# 1. Abrir Programador de tareas -> Crear tarea básica.
# 2. Acción: Iniciar un programa.
# 3. Programa/script: powershell.exe
# 4. Argumentos: -ExecutionPolicy Bypass -File "C:\ruta\a\run_ingest_cycle.ps1"
# 5. Programar Diario a la hora deseada.