"""
Unified API Server for Metatron-ConscienceAI and Open-A.G.I Integration
"""

import asyncio
import json
import logging
import threading
import uvicorn
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .client import UnifiedAPIClient
from .models import UnifiedSystemState, UnifiedAPISettings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Unified Metatron-A.G.I API",
    description="Unified API for Metatron Consciousness Engine and Open A.G.I System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global client instance
api_client: Optional[UnifiedAPIClient] = None
settings = UnifiedAPISettings()

# Active WebSocket connections
active_connections = []

# Server thread reference
server_thread = None
server_should_stop = False


@app.on_event("startup")
async def startup_event():
    """Initialize the unified API client on startup"""
    global api_client
    try:
        api_client = UnifiedAPIClient(settings)
        await api_client.initialize()
        logger.info("Unified API Server initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Unified API Server: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    global api_client
    if api_client:
        await api_client.close()
        logger.info("Unified API Client closed")


@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "Unified Metatron-A.G.I API",
        "version": "1.0.0",
        "endpoints": {
            "GET /health": "System health check",
            "GET /state": "Get unified system state",
            "GET /consciousness": "Get consciousness state only",
            "GET /agi": "Get AGI state only",
            "POST /input": "Send consciousness input",
            "POST /chat": "Send chat message",
            "WebSocket /ws": "Real-time state streaming"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if not api_client:
        raise HTTPException(status_code=503, detail="API client not initialized")
    
    try:
        # Simple health check
        return {
            "status": "healthy",
            "timestamp": asyncio.get_event_loop().time(),
            "api_client_initialized": True
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


@app.get("/state")
async def get_unified_state():
    """Get the unified state of both systems"""
    if not api_client:
        raise HTTPException(status_code=503, detail="API client not initialized")
    
    try:
        state = await api_client.get_unified_state()
        if state:
            return state
        else:
            raise HTTPException(status_code=503, detail="Failed to retrieve system state")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving state: {str(e)}")


@app.get("/consciousness")
async def get_consciousness_state():
    """Get consciousness state only"""
    if not api_client:
        raise HTTPException(status_code=503, detail="API client not initialized")
    
    try:
        state = await api_client.get_consciousness_state()
        if state:
            return state
        else:
            raise HTTPException(status_code=503, detail="Failed to retrieve consciousness state")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving consciousness state: {str(e)}")


@app.get("/agi")
async def get_agi_state():
    """Get AGI state only"""
    if not api_client:
        raise HTTPException(status_code=503, detail="API client not initialized")
    
    try:
        state = await api_client.get_agi_state()
        if state:
            return state
        else:
            raise HTTPException(status_code=503, detail="Failed to retrieve AGI state")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving AGI state: {str(e)}")


@app.post("/input")
async def send_consciousness_input(input_data: Dict[str, float]):
    """Send sensory input to the consciousness system"""
    if not api_client:
        raise HTTPException(status_code=503, detail="API client not initialized")
    
    try:
        success = await api_client.send_consciousness_input(input_data)
        return {"success": success, "message": "Input processed" if success else "Input failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending input: {str(e)}")


@app.post("/chat")
async def send_chat_message(message_data: Dict[str, Any]):
    """Send a chat message to the AGI system"""
    if not api_client:
        raise HTTPException(status_code=503, detail="API client not initialized")
    
    try:
        message = message_data.get("message", "")
        session_id = message_data.get("session_id", "default")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        response = await api_client.send_chat_message(message, session_id)
        if response:
            return {"response": response, "session_id": session_id}
        else:
            raise HTTPException(status_code=503, detail="Failed to get chat response")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending chat message: {str(e)}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time state streaming"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Send initial state
        if api_client:
            state = await api_client.get_unified_state()
            if state:
                await websocket.send_text(json.dumps(state.__dict__, default=str))
        
        # Stream updates at regular intervals
        while True:
            if api_client:
                state = await api_client.get_unified_state()
                if state:
                    await websocket.send_text(json.dumps(state.__dict__, default=str))
            
            # Wait before next update
            await asyncio.sleep(settings.update_interval)
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)
        await websocket.close()


def _run_server_in_thread(host: str, port: int):
    """Run the server in a separate thread to avoid event loop conflicts"""
    global server_should_stop
    try:
        config = uvicorn.Config("unified_api.server:app", host=host, port=port, log_level="info")
        server = uvicorn.Server(config)
        logger.info(f"Starting Unified API Server on {host}:{port}")
        server.run()
    except Exception as e:
        logger.error(f"Error in API server thread: {e}")


def start_server(host: str = "0.0.0.0", port: int = 8005):
    """Start the unified API server in a separate thread to avoid event loop conflicts"""
    global server_thread, server_should_stop
    server_should_stop = False
    server_thread = threading.Thread(target=_run_server_in_thread, args=(host, port), daemon=True)
    server_thread.start()
    logger.info(f"Unified API Server thread started on {host}:{port}")


def stop_server():
    """Stop the unified API server"""
    global server_thread, server_should_stop
    server_should_stop = True
    if server_thread and server_thread.is_alive():
        logger.info("Stopping Unified API Server thread")
        # Note: Proper shutdown of uvicorn in a thread is complex, 
        # in practice you might want to use a more sophisticated approach
        # For now, we'll just mark it as stopped and let it terminate naturally
    logger.info("Unified API Server thread stop requested")


# Example usage
if __name__ == "__main__":
    start_server()