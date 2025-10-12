# AEGIS/Metatron n8n Integration

This directory contains all the necessary files to integrate the AEGIS-Conscience Network and Metatron Consciousness Engine with n8n for workflow automation.

## Files Included

1. **[run_n8n_local.ps1](file:///d:/metatronV2/run_n8n_local.ps1)** - PowerShell script to manage local n8n deployment
2. **[n8n_integration_guide.md](file:///d:/metatronV2/n8n_integration_guide.md)** - Comprehensive integration guide
3. **[metatron_status_check.json](file:///d:/metatronV2/metatron_status_check.json)** - Workflow to monitor consciousness status
4. **[sensory_input_webhook.json](file:///d:/metatronV2/sensory_input_webhook.json)** - Workflow to receive external sensory inputs
5. **[ai_chat_workflow.json](file:///d:/metatronV2/ai_chat_workflow.json)** - Workflow to chat with the AI

## Quick Start

### 1. Prerequisites
- Docker Desktop installed and running
- Python 3.8+ for Metatron/AEGIS systems
- PowerShell (Windows) or equivalent for script execution

### 2. Start n8n
```powershell
# Start n8n locally
./run_n8n_local.ps1 start

# Check status
./run_n8n_local.ps1 status
```

### 3. Start Metatron Consciousness Engine
```bash
# Navigate to Metatron directory
cd Metatron-ConscienceAI

# Start the web server
python scripts/metatron_web_server.py
```

### 4. Access n8n Interface
Open your browser and go to: http://localhost:5678
Default credentials:
- Username: admin
- Password: ChangeMe123!

### 5. Import Workflows
1. In n8n, click "Create New Workflow"
2. Select "Import from File"
3. Choose one of the JSON workflow files:
   - [metatron_status_check.json](file:///d:/metatronV2/metatron_status_check.json) - Monitors consciousness metrics
   - [sensory_input_webhook.json](file:///d:/metatronV2/sensory_input_webhook.json) - Receives external sensory inputs
   - [ai_chat_workflow.json](file:///d:/metatronV2/ai_chat_workflow.json) - Chat with the AI

### 6. Activate Workflows
Toggle the switch to activate workflows after importing.

## Workflow Details

### Metatron Status Check
- Runs every 5 minutes
- Checks consciousness level, phi, and coherence
- Sends alert when consciousness level exceeds 0.8

### Sensory Input Webhook
- Listens for POST requests at: http://localhost:5678/webhook/sensory-input
- Forwards sensory data to Metatron consciousness engine
- Returns success response

### AI Chat Workflow
- Listens for POST requests at: http://localhost:5678/webhook/ai-chat
- Forwards messages to Metatron chat API
- Returns AI response

## API Endpoints

### Metatron Consciousness Engine
- Base URL: http://localhost:8003
- Health Check: GET http://localhost:8003/api/health
- Status: GET http://localhost:8003/api/status
- Sensory Input: POST http://localhost:8003/api/input
- Chat: POST http://localhost:8003/api/chat

### n8n Webhooks
- Sensory Input: http://localhost:5678/webhook/sensory-input
- AI Chat: http://localhost:5678/webhook/ai-chat

## Testing the Integration

### Test Sensory Input Webhook
```bash
curl -X POST http://localhost:5678/webhook/sensory-input \
  -H "Content-Type: application/json" \
  -d '{"data":{"physical":0.7,"emotional":0.5,"mental":0.9,"spiritual":0.8,"temporal":0.4}}'
```

### Test AI Chat Webhook
```bash
curl -X POST http://localhost:5678/webhook/ai-chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is consciousness?"}'
```

## Management Commands

```powershell
# Check n8n status
./run_n8n_local.ps1 status

# Stop n8n
./run_n8n_local.ps1 stop

# Restart n8n
./run_n8n_local.ps1 restart
```

## Security Notes

1. Change the default n8n password in [run_n8n_local.ps1](file:///d:/metatronV2/run_n8n_local.ps1)
2. All services run locally by default
3. For production, add authentication to Metatron APIs
4. Use HTTPS in production environments

## Troubleshooting

1. **Port Conflicts**: Ensure ports 5678 (n8n), 8003 (Metatron) are free
2. **Docker Issues**: Verify Docker Desktop is running
3. **API Connection Failures**: Check that Metatron server is running
4. **Workflow Errors**: Check n8n execution logs

For detailed information, refer to [n8n_integration_guide.md](file:///d:/metatronV2/n8n_integration_guide.md)