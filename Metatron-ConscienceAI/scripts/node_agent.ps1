<#
 Intelente Node Agent
 - Lee node_config.json
 - Empaqueta delta con manifest y métricas
 - Sube el paquete al servidor federado

 Ejecutar manualmente:
   powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\node_agent.ps1
#>
param()
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-ProjectRoot {
  if ($PSScriptRoot) { return (Split-Path -Parent $PSScriptRoot) }
  return (Get-Location)
}

$root = Get-ProjectRoot
$cfgPath = Join-Path $root 'node_config.json'
if (-not (Test-Path $cfgPath)) {
  Write-Host "[ERROR] No se encontró node_config.json en $root" -ForegroundColor Red
  Write-Host "Crea o copia node_config.example.json a node_config.json y ajusta los valores."
  exit 1
}

$cfg = Get-Content $cfgPath -Raw | ConvertFrom-Json
function Get-Field($obj, $name, $default=$null) { if ($obj.PSObject.Properties.Name -contains $name) { return $obj.$name } else { return $default } }

$serverUrl = Get-Field $cfg 'server_url' 'http://127.0.0.1:8000'
$token     = Get-Field $cfg 'token' 'change-me'
$nodeId    = Get-Field $cfg 'node_id' 'node_01'
$modelDir  = Get-Field $cfg 'model_dir' (Join-Path $root 'models\finetune_es_pdf_lm')
$evalDir   = Get-Field $cfg 'eval_dir' (Join-Path $root 'ai_runs')
 $proxySocks5 = Get-Field $cfg 'proxy_socks5' $null

Write-Host "[INFO] Configuración:" -ForegroundColor Cyan
Write-Host " server_url: $serverUrl"
Write-Host " token: (oculto)"
Write-Host " node_id: $nodeId"
Write-Host " model_dir: $modelDir"
Write-Host " eval_dir: $evalDir"
Write-Host " proxy_socks5: $proxySocks5"

if (-not (Test-Path $modelDir)) { Write-Host "[ERROR] model_dir no existe: $modelDir" -ForegroundColor Red; exit 2 }
if (-not (Test-Path (Join-Path $modelDir 'adapter_model.safetensors'))) { Write-Host "[ERROR] Falta adapter_model.safetensors en $modelDir" -ForegroundColor Red; exit 3 }

$zipPath = Join-Path $root ('tmp_node_delta_' + (Get-Date -Format 'yyyyMMdd_HHmm') + '.zip')

Write-Host "[STEP] Empaquetando delta: $zipPath" -ForegroundColor Cyan
& python (Join-Path $root 'scripts\package_lora_delta.py') --model-dir $modelDir --eval-dir $evalDir --out $zipPath --node-id $nodeId
if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] Falló el empaquetado" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host "[STEP] Subiendo delta al servidor: $serverUrl" -ForegroundColor Cyan
if ($proxySocks5) {
  & python (Join-Path $root 'scripts\upload_delta_client.py') --zip $zipPath --url $serverUrl --token $token --node-id $nodeId --socks5 $proxySocks5
} else {
  & python (Join-Path $root 'scripts\upload_delta_client.py') --zip $zipPath --url $serverUrl --token $token --node-id $nodeId
}
if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] Falló la subida" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host "[OK] Nodo Intelente: delta empaquetado y subido correctamente." -ForegroundColor Green