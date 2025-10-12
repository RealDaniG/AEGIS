param(
  [string]$Workspace = "$PSScriptRoot"
)

try {
  $ws = Resolve-Path $Workspace
  Set-Location $ws
  $logDir = Join-Path $ws "ai_runs"
  if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
  $logPath = Join-Path $logDir ("scheduled_compute_" + (Get-Date -Format 'yyyyMMdd_HHmmss') + ".log")
  Write-Host "[scheduled] Iniciando compute_contribution.ps1 en $ws (log: $logPath)"
  & pwsh -NoProfile -ExecutionPolicy Bypass -File "$ws/scripts/compute_contribution.ps1" *>&1 | Tee-Object -FilePath $logPath
  Write-Host "[scheduled] Finalizado. Log en $logPath"
} catch {
  Write-Error "[scheduled] Error: $($_.Exception.Message)"
  exit 1
}