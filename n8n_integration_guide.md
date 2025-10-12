# AEGIS/Metatron to n8n Integration Guide

## Overview
This guide provides detailed instructions for connecting the AEGIS-Conscience Network and Metatron Consciousness Engine to n8n for workflow automation and third-party app integration.

## System Architecture

### Components
1. **Metatron Consciousness Engine** - Runs on http://localhost:8003
2. **AEGIS-Conscience Network** - P2P nodes with TOR integration
3. **n8n Automation Platform** - Runs on http://localhost:5678
4. **Integration Bridge** - Custom API connectors

## API Endpoints

### Metatron Consciousness Engine
```
Base URL: http://localhost:8003
WebSocket: ws://localhost:8003/ws
Chat WebSocket: ws://localhost:8003/ws/chat
```

#### REST API Endpoints
| Endpoint | Method | Description | Payload |
|----------|--------|-------------|---------|
| `/api/health` | GET | System health check | - |
| `/api/status` | GET | Consciousness metrics | - |
| `/api/input` | POST | Send sensory input | `{"physical": 0.5, "emotional": 0.3, "mental": 0.7, "spiritual": 0.8, "temporal": 0.2}` |
| `/api/chat` | POST | Chat with AI | `{"message": "Hello", "session_id": "session1"}` |
| `/api/reset` | POST | Reset consciousness | - |

### AEGIS-Conscience Network
```
Dashboard: http://localhost:8081 (when running)
P2P Network: TOR onion services (when available)
```

## n8n Setup Configuration

### PowerShell Script for Local n8n Deployment
Create `run_n8n_local.ps1`:

```powershell
<#
Arranque y gestión de n8n local en Windows (Docker Desktop requerido).

Uso:
  - Ejecuta en PowerShell: ./run_n8n_local.ps1 start
  - Para ver estado:        ./run_n8n_local.ps1 status
  - Para parar:             ./run_n8n_local.ps1 stop
  - Para reiniciar:         ./run_n8n_local.ps1 restart

Variables:
  - Usuario y contraseña de Basic Auth ajustables abajo.
  - Persistencia en carpeta ./n8n_data

Requisitos:
  - Tener Docker Desktop instalado y corriendo.
  - Puerto 5678 libre (UI y webhooks de n8n).
#>

param(
  [Parameter(Mandatory=$true)][ValidateSet('start','stop','status','restart')]
  [string]$action
)

$ErrorActionPreference = 'Stop'

$containerName = 'n8n-local'
$basicAuthUser = 'admin'
$basicAuthPass = 'ChangeMe123!'   # Cambia esta clave para producción

function Ensure-DataDir {
  if (-not (Test-Path -Path "n8n_data")) {
    New-Item -ItemType Directory -Force -Path "n8n_data" | Out-Null
  }
}

function Start-N8N {
  Ensure-DataDir
  Write-Host "Descargando imagen n8nio/n8n:latest…"
  docker pull n8nio/n8n:latest

  if ((docker ps -a --format ".Names" | Select-String -Pattern "^$containerName$")) {
    Write-Host "El contenedor ya existe; eliminando previo…"
    docker stop $containerName | Out-Null
    docker rm $containerName | Out-Null
  }

  Write-Host "Lanzando $containerName en http://127.0.0.1:5678 (Basic Auth)…"
  $env:N8N_BASIC_AUTH_USER = $basicAuthUser
  $env:N8N_BASIC_AUTH_PASSWORD = $basicAuthPass

  docker run -d --name $containerName --restart unless-stopped `
    -p 5678:5678 `
    -e N8N_BASIC_AUTH_ACTIVE=true `
    -e N8N_BASIC_AUTH_USER=$env:N8N_BASIC_AUTH_USER `
    -e N8N_BASIC_AUTH_PASSWORD=$env:N8N_BASIC_AUTH_PASSWORD `
    -e N8N_HOST=127.0.0.1 `
    -e N8N_PORT=5678 `
    -e N8N_PROTOCOL=http `
    -e WEBHOOK_URL=http://127.0.0.1:5678 `
    -v "${pwd}\n8n_data:/home/node/.n8n" `
    n8nio/n8n:latest | Out-Null

  Write-Host "n8n arrancado. Accede a: http://127.0.0.1:5678 (usuario: $basicAuthUser)" -ForegroundColor Green
}

function Stop-N8N {
  if ((docker ps -a --format ".Names" | Select-String -Pattern "^$containerName$")) {
    docker stop $containerName | Out-Null
    Write-Host "Contenedor detenido." -ForegroundColor Yellow
  } else {
    Write-Host "Contenedor no existe." -ForegroundColor Red
  }
}

function Status-N8N {
  docker ps --filter name=$containerName --format "table .Names`t.Status`t.Ports"
}

switch ($action) {
  'start'   { Start-N8N }
  'stop'    { Stop-N8N }
  'status'  { Status-N8N }
  'restart' { Stop-N8N; Start-N8N }
}
```

## Integration Templates

### 1. HTTP Node Template for Metatron API

#### Get Consciousness Status
```json
{
  "nodes": [
    {
      "parameters": {
        "requestMethod": "GET",
        "url": "http://localhost:8003/api/status",
        "responseFormat": "json"
      },
      "name": "Get Consciousness Status",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    }
  ],
  "connections": {}
}
```

#### Send Sensory Input
```json
{
  "nodes": [
    {
      "parameters": {
        "requestMethod": "POST",
        "url": "http://localhost:8003/api/input",
        "responseFormat": "json",
        "options": {},
        "bodyContentType": "json",
        "jsonContent": "={\n  \"physical\": 0.7,\n  \"emotional\": 0.5,\n  \"mental\": 0.9,\n  \"spiritual\": 0.8,\n  \"temporal\": 0.4\n}"
      },
      "name": "Send Sensory Input",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    }
  ],
  "connections": {}
}
```

#### Chat with AI
```json
{
  "nodes": [
    {
      "parameters": {
        "requestMethod": "POST",
        "url": "http://localhost:8003/api/chat",
        "responseFormat": "json",
        "options": {},
        "bodyContentType": "json",
        "jsonContent": "={\n  \"message\": \"{{$input[\"message\"]}}\",\n  \"session_id\": \"n8n_session_{{$execution.id}}\"\n}"
      },
      "name": "Chat with AI",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    }
  ],
  "connections": {}
}
```

### 2. Webhook Integration Template

#### Receive External Triggers
```json
{
  "nodes": [
    {
      "parameters": {
        "path": "consciousness-trigger",
        "responseMode": "lastNode",
        "responseData": "firstEntryJson",
        "options": {}
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        250,
        300
      ]
    },
    {
      "parameters": {
        "requestMethod": "POST",
        "url": "http://localhost:8003/api/input",
        "responseFormat": "json",
        "options": {},
        "bodyContentType": "json",
        "jsonContent": "={{\n  \"physical\": {{$json[\"physical\"] || 0.5}},\n  \"emotional\": {{$json[\"emotional\"] || 0.5}},\n  \"mental\": {{$json[\"mental\"] || 0.5}},\n  \"spiritual\": {{$json[\"spiritual\"] || 0.5}},\n  \"temporal\": {{$json[\"temporal\"] || 0.5}}\n}}"
      },
      "name": "Trigger Consciousness",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [
        [
          {
            "node": "Trigger Consciousness",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

## Example Workflows

### 1. Consciousness Monitoring Workflow
This workflow periodically checks the consciousness status and sends alerts when metrics exceed thresholds.

```json
{
  "nodes": [
    {
      "parameters": {
        "cronExpression": "*/5 * * * *",
        "timezone": "America/New_York"
      },
      "name": "Every 5 minutes",
      "type": "n8n-nodes-base.cron",
      "typeVersion": 1,
      "position": [
        250,
        300
      ]
    },
    {
      "parameters": {
        "requestMethod": "GET",
        "url": "http://localhost:8003/api/status",
        "responseFormat": "json"
      },
      "name": "Get Consciousness Status",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{$json[\"consciousness_level\"]}}",
              "operation": "larger",
              "value2": 0.8
            }
          ]
        }
      },
      "name": "High Consciousness?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [
        650,
        300
      ]
    },
    {
      "parameters": {
        "subject": "High Consciousness Alert",
        "text": "=Consciousness level is {{$json[\"consciousness_level\"]}} which exceeds threshold.\nPhi: {{$json[\"phi\"]}}\nCoherence: {{$json[\"coherence\"]}}"
      },
      "name": "Send Alert",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 1,
      "position": [
        850,
        200
      ]
    }
  ],
  "connections": {
    "Every 5 minutes": {
      "main": [
        [
          {
            "node": "Get Consciousness Status",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get Consciousness Status": {
      "main": [
        [
          {
            "node": "High Consciousness?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "High Consciousness?": {
      "main": [
        [
          {
            "node": "Send Alert",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

### 2. External Trigger to Consciousness Input
This workflow receives external triggers via webhook and sends sensory input to the consciousness engine.

```json
{
  "nodes": [
    {
      "parameters": {
        "path": "sensory-input",
        "responseMode": "lastNode",
        "responseData": "firstEntryJson"
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        250,
        300
      ]
    },
    {
      "parameters": {
        "requestMethod": "POST",
        "url": "http://localhost:8003/api/input",
        "responseFormat": "json",
        "options": {},
        "bodyContentType": "json",
        "jsonContent": "={{\n  \"physical\": {{$json[\"data\"][\"physical\"] || 0.5}},\n  \"emotional\": {{$json[\"data\"][\"emotional\"] || 0.5}},\n  \"mental\": {{$json[\"data\"][\"mental\"] || 0.5}},\n  \"spiritual\": {{$json[\"data\"][\"spiritual\"] || 0.5}},\n  \"temporal\": {{$json[\"data\"][\"temporal\"] || 0.5}}\n}}"
      },
      "name": "Send to Consciousness",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    },
    {
      "parameters": {
        "responseMode": "onReceived",
        "responseCode": 200,
        "responseBody": "={\n  \"status\": \"success\",\n  \"message\": \"Sensory input processed\",\n  \"timestamp\": \"{{new Date().toISOString()}}\"\n}"
      },
      "name": "Respond",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [
        650,
        300
      ]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [
        [
          {
            "node": "Send to Consciousness",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Send to Consciousness": {
      "main": [
        [
          {
            "node": "Respond",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

## Setup Instructions

### 1. Start n8n
```powershell
# Save the PowerShell script as run_n8n_local.ps1
# Then run:
./run_n8n_local.ps1 start
```

### 2. Start Metatron Consciousness Engine
```bash
cd Metatron-ConscienceAI
python scripts/metatron_web_server.py
```

### 3. (Optional) Start AEGIS Dashboard
```bash
cd aegis-conscience
# Install Flask if not already installed
pip install Flask flask-socketio
# Run dashboard
python monitoring/dashboard.py
```

### 4. Import Templates into n8n
1. Open n8n at http://localhost:5678
2. Click "Create New Workflow"
3. Select "Import from File"
4. Choose the JSON template files
5. Configure any required credentials
6. Activate the workflow

## Security Considerations

### Authentication
- Use Basic Auth for n8n (configured in the PowerShell script)
- API endpoints don't require authentication by default
- For production, add authentication to Metatron APIs

### Network Security
- All services run on localhost by default
- For external access, configure proper firewall rules
- Use HTTPS in production environments

### Data Privacy
- Consciousness data is processed locally
- No data is sent to external servers by default
- Review workflow permissions carefully

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   - Ensure ports 5678 (n8n), 8003 (Metatron), 8081 (AEGIS) are free
   - Use `netstat -an | findstr :<port>` to check

2. **Docker Issues**
   - Ensure Docker Desktop is running
   - Check Docker logs: `docker logs n8n-local`

3. **API Connection Failures**
   - Verify Metatron server is running
   - Check firewall settings
   - Confirm localhost access

### Logs and Monitoring
- n8n logs: Access via Docker: `docker logs n8n-local`
- Metatron logs: Console output from the web server
- AEGIS logs: Console output from dashboard

## Advanced Integration

### Custom API Endpoints
You can extend the Metatron server with custom endpoints for specific n8n integrations:

```python
# Add to metatron_web_server.py
@app.post("/api/n8n/trigger")
async def n8n_trigger(request: Request):
    """Custom endpoint for n8n triggers"""
    try:
        data = await request.json()
        
        # Process the trigger data
        trigger_type = data.get('type', 'generic')
        payload = data.get('payload', {})
        
        # Send to consciousness engine
        sensory_input = np.array([
            payload.get('physical', 0.5),
            payload.get('emotional', 0.5),
            payload.get('mental', 0.5),
            payload.get('spiritual', 0.5),
            payload.get('temporal', 0.5)
        ])
        
        state = consciousness_system.update_system(sensory_input)
        
        return JSONResponse({
            "status": "processed",
            "trigger_type": trigger_type,
            "consciousness_level": state['global']['consciousness_level']
        })
    except Exception as e:
        return JSONResponse({
            "error": str(e)
        }, status_code=500)
```

This integration guide provides a comprehensive foundation for connecting the AEGIS-Conscience Network and Metatron Consciousness Engine with n8n for workflow automation and third-party app integration.