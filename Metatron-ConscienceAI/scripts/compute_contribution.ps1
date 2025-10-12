<#
 Contribución de cómputo del nodo (mínima y segura)
 - Registra recursos del nodo
 - Ejecuta ingesta RSS
 - (Opcional) Entrena un pequeño adapter LoRA en QA (subset)
 - Empaqueta y sube el delta al servidor federado

 Uso manual:
   powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\compute_contribution.ps1

 Para programar (Programador de tareas de Windows):
   Acción: Iniciar un programa
   Programa/script: powershell.exe
   Argumentos: -NoProfile -ExecutionPolicy Bypass -File "C:\ruta\al\repo\scripts\compute_contribution.ps1"
#>
param()
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-ProjectRoot {
  if ($PSScriptRoot) { return (Split-Path -Parent $PSScriptRoot) }
  return (Get-Location)
}

function Resolve-PythonExe {
  param([string]$rootPath)
  $venvPy = Join-Path $rootPath ".venv\Scripts\python.exe"
  if (Test-Path $venvPy) { return $venvPy }
  return "python"
}

function Get-Field($obj, $name, $default=$null) {
  if ($null -eq $obj) { return $default }
  if ($obj.PSObject.Properties.Name -contains $name) { return $obj.$name } else { return $default }
}

$root = Get-ProjectRoot
$py = Resolve-PythonExe -rootPath $root
Push-Location $root
try {
  # Leer configuración
  $cfgPath = Join-Path $root 'node_config.json'
  if (-not (Test-Path $cfgPath)) {
    Write-Host "[ERROR] No se encontró node_config.json en $root" -ForegroundColor Red
    Write-Host "Crea o copia node_config.example.json a node_config.json y ajusta los valores."
    exit 1
  }
  $cfg = Get-Content $cfgPath -Raw | ConvertFrom-Json

  $serverUrl   = Get-Field $cfg 'server_url' 'http://127.0.0.1:8000'
  $token       = Get-Field $cfg 'token' 'change-me'
  $nodeId      = Get-Field $cfg 'node_id' 'node_01'
  $evalDir     = Get-Field $cfg 'eval_dir' (Join-Path $root 'ai_runs')
  $proxySocks5 = Get-Field $cfg 'proxy_socks5' $null

  $computeCfg  = Get-Field $cfg 'compute_contribution' $null
  $enabled     = Get-Field $computeCfg 'enabled' $true
  $baseModel   = Get-Field $computeCfg 'model' 'Qwen/Qwen2.5-0.5B-Instruct'
  $qaSubset    = [int](Get-Field $computeCfg 'qa_subset_size' 200)
  $epochs      = [int](Get-Field $computeCfg 'epochs' 1)
  $batchSize   = [int](Get-Field $computeCfg 'batch_size' 1)
  $maxSeqLen   = [int](Get-Field $computeCfg 'max_seq_len' 512)

  Write-Host "[INFO] Configuración de contribución de cómputo:" -ForegroundColor Cyan
  Write-Host " server_url: $serverUrl"
  Write-Host " node_id: $nodeId"
  Write-Host " proxy_socks5: $proxySocks5"
  Write-Host " enabled: $enabled"
  Write-Host " base_model: $baseModel"
  Write-Host " qa_subset_size: $qaSubset; epochs: $epochs; batch_size: $batchSize; max_seq_len: $maxSeqLen"

  if (-not $enabled) {
    Write-Host "[INFO] compute_contribution.enabled=false. Nada que hacer." -ForegroundColor Yellow
    exit 0
  }

  # Pre-chequeo de conectividad .onion vía Tor (si aplica)
  if ($proxySocks5 -and ($serverUrl -match "\.onion")) {
    Write-Host "[STEP] Verificando conectividad .onion (/list)" -ForegroundColor Cyan
    try {
      & pwsh -NoProfile -ExecutionPolicy Bypass -File (Join-Path $root 'scripts\test_onion_connectivity.ps1')
      if ($LASTEXITCODE -ne 0) { Write-Host "[WARN] Conectividad .onion fallida, se continuará igualmente y se intentará subir con reintentos." -ForegroundColor Yellow }
    } catch {
      Write-Host "[WARN] No se pudo ejecutar test_onion_connectivity.ps1: $($_.Exception.Message)" -ForegroundColor Yellow
    }
  }

  # Paso 1: Recursos del nodo
  Write-Host "[STEP] Registrando recursos del nodo" -ForegroundColor Cyan
  & $py (Join-Path $root 'scripts\node_resources.py')
  if ($LASTEXITCODE -ne 0) { Write-Host "[WARN] node_resources.py devolvió código $LASTEXITCODE" -ForegroundColor Yellow }

  # Paso 2: Ingesta RSS
  Write-Host "[STEP] Ejecutando ingesta RSS" -ForegroundColor Cyan
  & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $root 'run_ingest_cycle.ps1')
  if ($LASTEXITCODE -ne 0) { Write-Host "[WARN] run_ingest_cycle.ps1 devolvió código $LASTEXITCODE" -ForegroundColor Yellow }

  # Paso 3: Entrenamiento ligero (QA subset) -> LoRA adapter
  $qaSrc = Join-Path $root 'datasets\pdf_es_qa.jsonl'
  $qaSmall = Join-Path $root 'datasets\pdf_es_qa.small.jsonl'
  $outDir = Join-Path $root ("models\contrib_qa_lora_" + (Get-Date -Format 'yyyyMMdd_HHmm'))

  if (Test-Path $qaSrc) {
    Write-Host "[STEP] Preparando subset QA ($qaSubset)" -ForegroundColor Cyan
    & $py (Join-Path $root 'scripts\make_subset_jsonl.py') --input $qaSrc --output $qaSmall --limit $qaSubset
    if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] Falló la creación del subset QA" -ForegroundColor Red; exit $LASTEXITCODE }

    Write-Host "[STEP] Entrenando adapter LoRA (ligero)" -ForegroundColor Cyan
    $trainArgs = @('--model', $baseModel, '--train-file', $qaSmall, '--out-dir', $outDir, '--epochs', $epochs, '--batch-size', $batchSize, '--lr', '2e-5', '--max-seq-len', $maxSeqLen, '--lora')
    & $py (Join-Path $root 'scripts\train_llm_qa.py') @trainArgs
    if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] Falló el entrenamiento ligero" -ForegroundColor Red; exit $LASTEXITCODE }
  } else {
    Write-Host "[INFO] No existe datasets\\pdf_es_qa.jsonl. Omitiendo entrenamiento QA." -ForegroundColor Yellow
    # Aún podemos contribuir empaquetando/adaptando si existieran otros adapters.
    $outDir = (Join-Path $root 'models\finetune_es_pdf_lm')
  }

  # Paso 4: Empaquetar y subir delta
  $zipPath = Join-Path $root ('tmp_node_delta_' + (Get-Date -Format 'yyyyMMdd_HHmm') + '.zip')
  Write-Host "[STEP] Empaquetando delta: $zipPath" -ForegroundColor Cyan
  & $py (Join-Path $root 'scripts\package_lora_delta.py') --model-dir $outDir --eval-dir $evalDir --out $zipPath --node-id $nodeId
  if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] Falló el empaquetado de delta" -ForegroundColor Red; exit $LASTEXITCODE }

  Write-Host "[STEP] Subiendo delta al servidor federado: $serverUrl" -ForegroundColor Cyan
  if ($proxySocks5) {
    & $py (Join-Path $root 'scripts\upload_delta_client.py') --zip $zipPath --url $serverUrl --token $token --node-id $nodeId --socks5 $proxySocks5
  } else {
    & $py (Join-Path $root 'scripts\upload_delta_client.py') --zip $zipPath --url $serverUrl --token $token --node-id $nodeId
  }
  if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] Falló la subida del delta" -ForegroundColor Red; exit $LASTEXITCODE }

  Write-Host "[OK] Contribución de cómputo completada y subida." -ForegroundColor Green

  # Paso 5: Reporte simple de métricas (gráficas)
  try {
    $metricsCsv = Join-Path $evalDir 'metrics.csv'
    $manifestJson = Join-Path $evalDir 'manifest.json'
    $plotsOut = Join-Path $evalDir 'plots'
    if (Test-Path $metricsCsv) {
      Write-Host "[STEP] Generando gráficas de métricas desde metrics.csv" -ForegroundColor Cyan
      & $py (Join-Path $root 'scripts\plot_metrics.py') --in $metricsCsv --out-dir $plotsOut
      if ($LASTEXITCODE -ne 0) { Write-Host "[WARN] plot_metrics.py devolvió código $LASTEXITCODE" -ForegroundColor Yellow }
    } elseif (Test-Path $manifestJson) {
      Write-Host "[STEP] Generando gráficas de métricas desde manifest.json" -ForegroundColor Cyan
      & $py (Join-Path $root 'scripts\plot_metrics.py') --in $manifestJson --out-dir $plotsOut
      if ($LASTEXITCODE -ne 0) { Write-Host "[WARN] plot_metrics.py devolvió código $LASTEXITCODE" -ForegroundColor Yellow }
    } else {
      Write-Host "[INFO] No se encontraron métricas en '$evalDir'. Omitiendo reporte de gráficas." -ForegroundColor Yellow
    }
  } catch {
    Write-Host "[WARN] No se pudo generar el reporte de métricas: $($_.Exception.Message)" -ForegroundColor Yellow
  }
} finally {
  Pop-Location
}