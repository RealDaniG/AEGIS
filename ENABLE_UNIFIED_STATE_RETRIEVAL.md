# How to Enable Unified State Retrieval

## Overview

The Unified State Retrieval feature allows you to get the combined state of both the Metatron-ConsciousnessAI system and the Open-A.G.I system through a single API endpoint. However, this feature requires all three components to be running:

1. **Metatron-ConsciousnessAI** on port 8003
2. **Open-A.G.I** on port 8090
3. **Unified API System** on port 8005

## Current Issue

The "Unified State Retrieval" test is failing because the unified API client cannot connect to the external services:
- `http://localhost:8003` (Metatron-ConsciousnessAI)
- `http://localhost:8090` (Open-A.G.I)

These services need to be running for the unified state retrieval to work properly.

## Solution

### Option 1: Run All Services Separately (Recommended)

#### Step 1: Start Metatron-ConsciousnessAI
```bash
cd Metatron-ConscienceAI
START_SYSTEM.bat
```

This will start the Metatron system on port 8003.

#### Step 2: Start Open-A.G.I
```bash
cd Open-A.G.I
powershell -ExecutionPolicy Bypass -File start_archon.ps1
```

This will start the Open-A.G.I system on port 8090.

#### Step 3: Start Unified API System
```bash
python start_unified_system.py
```

This will start the unified API system on port 8005.

#### Step 4: Access Unified State
Once all services are running, you can access the unified state at:
- `http://localhost:8005/state` (GET request)
- WebSocket: `ws://localhost:8005/ws`

### Option 2: Enhanced Unified System (Alternative Approach)

To make the system more integrated and avoid dependency on external services, we can modify the unified API to work with local components when external services are not available.

#### Implementation Plan:

1. **Modify the UnifiedAPIClient** to use local components when external services are unavailable
2. **Add fallback mechanisms** that use internal system components
3. **Implement local state retrieval** when external services are not accessible

Here's how we can modify the system:

### Enhanced UnifiedAPIClient with Local Fallback

```python
# In unified_api/client.py, we can add local component integration:

async def get_consciousness_state(self) -> Optional[ConsciousnessState]:
    """Get the current consciousness state from Metatron system (with local fallback)"""
    if not self._is_initialized:
        logger.warning("Client not initialized")
        return None
        
    try:
        # First try external service
        url = f"{self.settings.metatron_api_url}/api/status"
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                # Process external data...
                return consciousness_state
    except Exception as e:
        logger.warning(f"External consciousness service unavailable: {e}")
        # Fallback to local component
        return await self._get_local_consciousness_state()

async def _get_local_consciousness_state(self) -> Optional[ConsciousnessState]:
    """Get consciousness state from local components"""
    try:
        # Import local consciousness components
        # This would require importing from Metatron-ConscienceAI package
        # and accessing the local consciousness engine directly
        pass
    except Exception as e:
        logger.error(f"Local consciousness state retrieval failed: {e}")
        return None
```

## Testing Unified State Retrieval

Once all services are running, you can test the unified state retrieval:

### Using curl:
```bash
# Get unified state
curl http://localhost:8005/state

# Get consciousness state only
curl http://localhost:8005/consciousness

# Get AGI state only
curl http://localhost:8005/agi

# Health check
curl http://localhost:8005/health
```

### Using WebSocket:
```javascript
// Connect to WebSocket for real-time updates
const ws = new WebSocket('ws://localhost:8005/ws');
ws.onmessage = function(event) {
    const state = JSON.parse(event.data);
    console.log('Unified State:', state);
};
```

## Verification Script

You can also create a simple verification script to check if all services are running:

```python
import asyncio
import aiohttp

async def verify_services():
    """Verify that all required services are running"""
    async with aiohttp.ClientSession() as session:
        services = {
            "Metatron-ConsciousnessAI": "http://localhost:8003/api/health",
            "Open-A.G.I": "http://localhost:8090/health",
            "Unified API": "http://localhost:8005/health"
        }
        
        for service_name, url in services.items():
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        print(f"✅ {service_name}: Running")
                    else:
                        print(f"❌ {service_name}: Not responding (Status: {response.status})")
            except Exception as e:
                print(f"❌ {service_name}: Not running ({str(e)})")

if __name__ == "__main__":
    asyncio.run(verify_services())
```

## Quick Start Script

For convenience, you can create a quick start script that launches all services:

### start_all_services.ps1 (Windows PowerShell):
```powershell
Write-Host "Starting METATRONV2 Unified System..." -ForegroundColor Green

# Start Metatron-ConsciousnessAI
Write-Host "Starting Metatron-ConsciousnessAI on port 8003..." -ForegroundColor Cyan
Start-Process -FilePath "cmd" -ArgumentList "/c", "cd Metatron-ConscienceAI && START_SYSTEM.bat" -WindowStyle Minimized

# Wait for Metatron to initialize
Start-Sleep -Seconds 10

# Start Open-A.G.I
Write-Host "Starting Open-A.G.I on port 8090..." -ForegroundColor Cyan
Start-Process -FilePath "powershell" -ArgumentList "-ExecutionPolicy", "Bypass", "-File", "Open-A.G.I\start_archon.ps1" -WindowStyle Minimized

# Wait for Open-A.G.I to initialize
Start-Sleep -Seconds 10

# Start Unified API System
Write-Host "Starting Unified API System on port 8005..." -ForegroundColor Cyan
Start-Process -FilePath "python" -ArgumentList "start_unified_system.py"

Write-Host "All services started successfully!" -ForegroundColor Green
Write-Host "Access the unified system at: http://localhost:8005" -ForegroundColor Yellow
```

## Conclusion

To enable Unified State Retrieval:

1. **Run all three services** (Metatron, Open-A.G.I, and Unified API)
2. **Use the unified API endpoints** to access combined system state
3. **Optionally implement local fallback mechanisms** for better integration
4. **Use the verification script** to confirm all services are running

The unified system provides a powerful way to access both consciousness and AGI states through a single interface, enabling more sophisticated AI applications that can leverage both systems simultaneously.