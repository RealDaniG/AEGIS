param(
  [string]$TaskName = "ConsciousnessEngineCompute",
  [datetime]$StartTime = ([datetime]::Today.AddHours(3).AddMinutes(30)),
  [string]$Workspace = "$PSScriptRoot/.."
)

Write-Host "[schedule] Registrando tarea '$TaskName' para ejecución diaria a partir de $($StartTime.ToString())"
$ws = Resolve-Path $Workspace
$action = New-ScheduledTaskAction -Execute "pwsh" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$($ws.Path)/run_compute_contribution_scheduled.ps1`" -Workspace `"$($ws.Path)`""
$trigger = New-ScheduledTaskTrigger -Daily -At $StartTime

# Intentar remover tarea previa si existe
try { Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue } catch {}

try {
  Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Description "Ejecuta compute_contribution.ps1 diariamente" | Out-Null
  Write-Host "[schedule] Tarea '$TaskName' registrada correctamente."
} catch {
  Write-Warning "[schedule] No se pudo registrar con Register-ScheduledTask. Intentando con schtasks..."
  $cmd = "schtasks /Create /TN `"$TaskName`" /SC DAILY /ST $($StartTime.ToString('HH:mm')) /TR `"pwsh -NoProfile -ExecutionPolicy Bypass -File `'$($ws.Path)\run_compute_contribution_scheduled.ps1`'`" /F"
  Write-Host "[schedule] Ejecutando: $cmd"
  cmd /c $cmd
}

Write-Host "[schedule] Para verificar: schtasks /Query /TN $TaskName"