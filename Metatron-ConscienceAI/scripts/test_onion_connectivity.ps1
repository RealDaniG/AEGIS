param(
  [string]$ConfigPath = "$PSScriptRoot/../node_config.json"
)

Write-Host "[test_onion_connectivity] Leyendo configuración desde: $ConfigPath"
if (-not (Test-Path $ConfigPath)) {
  Write-Error "No se encontró el archivo de configuración en $ConfigPath"
  exit 1
}

$config = Get-Content -Raw -Path $ConfigPath | ConvertFrom-Json
$serverUrl = $config.server_url
$token = $config.token
$socks = $config.proxy_socks5

if (-not $serverUrl -or -not $token -or -not $socks) {
  Write-Error "Faltan campos en node_config.json: server_url, token o proxy_socks5"
  exit 1
}

Write-Host "[test_onion_connectivity] Probando puerto Tor ($socks) ..."
$socksHost,$socksPort = $socks.Split(":")
$portInt = [int]$socksPort
$tnc = Test-NetConnection -ComputerName $socksHost -Port $portInt -WarningAction SilentlyContinue
if (-not $tnc.TcpTestSucceeded) {
  Write-Error "Tor SOCKS5 no accesible en $socks"
  exit 1
}
Write-Host "[test_onion_connectivity] Tor accesible en $socks"

$pythonPath = Join-Path (Resolve-Path "$PSScriptRoot/..") ".venv/Scripts/python.exe"
if (-not (Test-Path $pythonPath)) {
  Write-Warning "Python de .venv no encontrado en $pythonPath. Intentando 'python' del sistema."
  $pythonPath = "python"
}

$pyCode = @"
import sys, json
import requests

server_url = sys.argv[1]
token = sys.argv[2]
proxy = sys.argv[3]

socks = {
    'http': f'socks5h://{proxy}',
    'https': f'socks5h://{proxy}',
}
headers = {'X-Auth-Token': token}

r = requests.get(server_url.rstrip('/') + '/list', headers=headers, proxies=socks, timeout=60)
print('STATUS', r.status_code)
print('BODY', r.text[:500])
"@

Write-Host "[test_onion_connectivity] Haciendo GET $serverUrl/list vía Tor ..."
$res = & $pythonPath -c $pyCode $serverUrl $token $socks
if ($LASTEXITCODE -ne 0) {
  Write-Error "Fallo al consultar /list vía Tor"
  exit $LASTEXITCODE
}
Write-Host $res
Write-Host "[test_onion_connectivity] Completado"