"""
Unified API Server for Metatron-ConscienceAI and Open-A.G.I Integration
"""

import asyncio
import json
import logging
import threading
import uvicorn
import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
api_client = None
active_connections = []
server_thread = None
server_should_stop = False

# Import these only when needed to avoid circular dependencies
UnifiedAPIClient = None
UnifiedAPISettings = None

# Create FastAPI app without lifespan events that might conflict with threading
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


# Serve static files from the Metatron-ConscienceAI webui directory
webui_dir = os.path.join(os.path.dirname(__file__), "..", "Metatron-ConscienceAI", "webui")
if os.path.exists(webui_dir):
    app.mount("/static", StaticFiles(directory=webui_dir), name="static")
    # Also mount assets specifically
    assets_dir = os.path.join(webui_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# Mount favicon directory
favicon_dir = os.path.join(os.path.dirname(__file__), "..", "favicon")
if os.path.exists(favicon_dir):
    app.mount("/favicon", StaticFiles(directory=favicon_dir), name="favicon")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - serve the main web UI"""
    # Try to serve the main index.html file
    index_path = os.path.join(webui_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    # Fallback to index_stream.html
    index_stream_path = os.path.join(webui_dir, "index_stream.html")
    if os.path.exists(index_stream_path):
        return FileResponse(index_stream_path)
    
    # Fallback to JSON response
    return {
        "message": "Unified Metatron-A.G.I API",
        "version": "1.0.0",
        "status": "running",
        "port": 8005,
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


async def initialize_client():
    """Initialize the unified API client"""
    global api_client, UnifiedAPIClient, UnifiedAPISettings
    
    # Import here to avoid circular dependencies
    if UnifiedAPIClient is None or UnifiedAPISettings is None:
        try:
            from unified_api.client import UnifiedAPIClient
            from unified_api.models import UnifiedAPISettings
        except ImportError as e:
            logger.error(f"Failed to import unified API modules: {e}")
            return
    
    try:
        if api_client is None:
            settings = UnifiedAPISettings()
            api_client = UnifiedAPIClient(settings)
            await api_client.initialize()
            logger.info("Unified API Client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Unified API Client: {e}")


async def cleanup_client():
    """Clean up the unified API client"""
    global api_client
    try:
        if api_client:
            await api_client.close()
            logger.info("Unified API Client closed")
    except Exception as e:
        logger.error(f"Error closing Unified API Client: {e}")
    finally:
        api_client = None


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Initialize client if not already done
    if api_client is None:
        await initialize_client()
        
    try:
        # Simple health check
        return {
            "status": "healthy",
            "timestamp": asyncio.get_event_loop().time(),
            "api_client_initialized": api_client is not None
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


@app.get("/state")
async def get_unified_state():
    """Get the unified state of both systems"""
    # Initialize client if not already done
    if api_client is None:
        await initialize_client()
        
    if not api_client:
        # Return a basic state if client is not available
        return {
            "timestamp": asyncio.get_event_loop().time(),
            "system_status": "running",
            "consciousness": None,
            "agi": None,
            "integration_metrics": {
                "systems_operational": (False, False),
                "consciousness_level": 0.0,
                "consensus_status": "unknown",
                "timestamp": asyncio.get_event_loop().time()
            }
        }
    
    try:
        state = await api_client.get_unified_state()
        if state:
            # Convert to dict for JSON serialization
            state_dict = {
                "timestamp": state.timestamp,
                "system_status": state.system_status.value if hasattr(state.system_status, 'value') else str(state.system_status),
                "consciousness": None,
                "agi": None,
                "integration_metrics": state.integration_metrics
            }
            
            # Add consciousness state if available
            if state.consciousness:
                state_dict["consciousness"] = {
                    "node_id": state.consciousness.node_id,
                    "timestamp": state.consciousness.timestamp,
                    "consciousness_level": state.consciousness.consciousness_level,
                    "phi": state.consciousness.phi,
                    "coherence": state.consciousness.coherence,
                    "recursive_depth": state.consciousness.recursive_depth,
                    "gamma_power": state.consciousness.gamma_power,
                    "fractal_dimension": state.consciousness.fractal_dimension,
                    "spiritual_awareness": state.consciousness.spiritual_awareness,
                    "state_classification": state.consciousness.state_classification,
                    "is_conscious": state.consciousness.is_conscious,
                    "dimensions": state.consciousness.dimensions
                }
            
            # Add AGI state if available
            if state.agi:
                state_dict["agi"] = {
                    "node_id": state.agi.node_id,
                    "timestamp": state.agi.timestamp,
                    "consensus_status": state.agi.consensus_status,
                    "network_health": state.agi.network_health,
                    "performance_metrics": state.agi.performance_metrics,
                    "active_connections": state.agi.active_connections,
                    "byzantine_threshold": state.agi.byzantine_threshold,
                    "quorum_size": state.agi.quorum_size
                }
            
            return state_dict
        else:
            # Return a basic state if unable to get unified state
            return {
                "timestamp": asyncio.get_event_loop().time(),
                "system_status": "running",
                "consciousness": None,
                "agi": None,
                "integration_metrics": {
                    "systems_operational": (False, False),
                    "consciousness_level": 0.0,
                    "consensus_status": "unknown",
                    "timestamp": asyncio.get_event_loop().time()
                }
            }
    except Exception as e:
        logger.error(f"Error retrieving state: {e}")
        # Return a basic state if there's an error
        return {
            "timestamp": asyncio.get_event_loop().time(),
            "system_status": "running",
            "consciousness": None,
            "agi": None,
            "integration_metrics": {
                "systems_operational": (False, False),
                "consciousness_level": 0.0,
                "consensus_status": "unknown",
                "timestamp": asyncio.get_event_loop().time()
            },
            "error": str(e)
        }


@app.get("/consciousness")
async def get_consciousness_state():
    """Get consciousness state only"""
    # Initialize client if not already done
    if api_client is None:
        await initialize_client()
        
    if not api_client:
        raise HTTPException(status_code=503, detail="API client not initialized")
    
    try:
        state = await api_client.get_consciousness_state()
        if state:
            # Convert to dict for JSON serialization
            return {
                "node_id": state.node_id,
                "timestamp": state.timestamp,
                "consciousness_level": state.consciousness_level,
                "phi": state.phi,
                "coherence": state.coherence,
                "recursive_depth": state.recursive_depth,
                "gamma_power": state.gamma_power,
                "fractal_dimension": state.fractal_dimension,
                "spiritual_awareness": state.spiritual_awareness,
                "state_classification": state.state_classification,
                "is_conscious": state.is_conscious,
                "dimensions": state.dimensions
            }
        else:
            return None
    except Exception as e:
        logger.error(f"Error retrieving consciousness state: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving consciousness state: {str(e)}")


@app.get("/agi")
async def get_agi_state():
    """Get AGI state only"""
    # Initialize client if not already done
    if api_client is None:
        await initialize_client()
        
    if not api_client:
        raise HTTPException(status_code=503, detail="API client not initialized")
    
    try:
        state = await api_client.get_agi_state()
        if state:
            # Convert to dict for JSON serialization
            return {
                "node_id": state.node_id,
                "timestamp": state.timestamp,
                "consensus_status": state.consensus_status,
                "network_health": state.network_health,
                "performance_metrics": state.performance_metrics,
                "active_connections": state.active_connections,
                "byzantine_threshold": state.byzantine_threshold,
                "quorum_size": state.quorum_size
            }
        else:
            return None
    except Exception as e:
        logger.error(f"Error retrieving AGI state: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving AGI state: {str(e)}")


@app.post("/input")
async def send_consciousness_input(input_data: Dict[str, float]):
    """Send sensory input to the consciousness system"""
    # Initialize client if not already done
    if api_client is None:
        await initialize_client()
        
    if not api_client:
        raise HTTPException(status_code=503, detail="API client not initialized")
    
    try:
        success = await api_client.send_consciousness_input(input_data)
        return {"success": success, "message": "Input processed" if success else "Input failed"}
    except Exception as e:
        logger.error(f"Error sending input: {e}")
        raise HTTPException(status_code=500, detail=f"Error sending input: {str(e)}")


@app.post("/chat")
async def send_chat_message(message_data: Dict[str, Any]):
    """Send a chat message to the AGI system"""
    # Initialize client if not already done
    if api_client is None:
        await initialize_client()
        
    if not api_client:
        raise HTTPException(status_code=503, detail="API client not initialized")
    
    try:
        message = message_data.get("message", "")
        session_id = message_data.get("session_id", "default")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # For now, we'll just return a mock response since we don't have the actual AGI system
        return {"response": f"Echo: {message}", "session_id": session_id}
    except Exception as e:
        logger.error(f"Error sending chat message: {e}")
        raise HTTPException(status_code=500, detail=f"Error sending chat message: {str(e)}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time state streaming"""
    # Initialize client if not already done
    if api_client is None:
        await initialize_client()
        
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Send initial state
        try:
            state = await get_unified_state()
            if state:
                await websocket.send_text(json.dumps(state, default=str))
        except Exception as e:
            logger.error(f"Error sending initial state: {e}")
        
        # Stream updates at regular intervals
        while True:
            try:
                state = await get_unified_state()
                if state:
                    await websocket.send_text(json.dumps(state, default=str))
            except Exception as e:
                logger.error(f"Error getting/sending state: {e}")
            
            # Wait before next update
            await asyncio.sleep(1.0)
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)
        await websocket.close()


def _run_server_in_thread(host: str, port: int):
    """Run the server in a separate thread to avoid event loop conflicts"""
    global server_should_stop
    loop = None
    try:
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Initialize the client in this loop
        loop.run_until_complete(initialize_client())
        
        # Run the server
        config = uvicorn.Config(app, host=host, port=port, log_level="info")
        server = uvicorn.Server(config)
        logger.info(f"Starting Unified API Server on {host}:{port}")
        loop.run_until_complete(server.serve())
    except Exception as e:
        logger.error(f"Error in API server thread: {e}")
    finally:
        # Clean up
        if loop:
            try:
                loop.run_until_complete(cleanup_client())
            except:
                pass


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
    
    # Keep the main thread alive
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
        stop_server()