"""
Metatron Consciousness Web Server
==================================

FastAPI server for web interface to Metatron's Cube consciousness engine.
Provides real-time consciousness state streaming via WebSocket.
"""

import sys
import os
import time
import json
import uuid
import asyncio
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import deque

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import uvicorn
from datetime import datetime

# Import consciousness system with cascading fallbacks
try:
    from orchestrator.metatron_orchestrator import MetatronConsciousness
except Exception as e:
    print(f"Import error: {e}")
    print("Attempting fallback import...")
    sys.path.insert(0, os.path.abspath('.'))
    from orchestrator.metatron_orchestrator import MetatronConsciousness

# Import MirrorLoop for AI reflection capabilities
try:
    from scripts.mirror_loop import MirrorLoop
except Exception as e:
    print(f"MirrorLoop import error: {e}")
    MirrorLoop = None

# Import chat functionality
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    CHAT_AVAILABLE = True
except ImportError:
    print("Warning: transformers/torch not available. Chat functionality disabled.")
    CHAT_AVAILABLE = False
    AutoModelForCausalLM = None
    AutoTokenizer = None
    torch = None

# Create FastAPI app
app = FastAPI(title="Metatron Consciousness Engine")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Repository root for data storage
REPO_ROOT = Path(__file__).resolve().parent.parent
CONSCIOUSNESS_LOG_DIR = REPO_ROOT / "ai_runs" / "consciousness_logs"
try:
    CONSCIOUSNESS_LOG_DIR.mkdir(parents=True, exist_ok=True)
except (PermissionError, OSError):
    # Fallback to user's temp directory if Program Files is read-only
    import tempfile
    CONSCIOUSNESS_LOG_DIR = Path(tempfile.gettempdir()) / "ConsciousnessEngine" / "consciousness_logs"
    try:
        CONSCIOUSNESS_LOG_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

# Create FastAPI app with enhanced metadata
app = FastAPI(
    title="Metatron Consciousness Engine",
    description="Sacred Geometry Consciousness System with Real-time Monitoring",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global consciousness system instance
consciousness_system = None

# Global chat system instance
chat_model = None
chat_tokenizer = None
chat_device = None
chat_sessions = {}

# Active WebSocket connections with metadata
active_connections = []
connection_metadata = {}

# Session management
consciousness_sessions = {}

# Performance monitoring
performance_metrics = {
    'total_updates': 0,
    'start_time': time.time(),
    'last_update_time': 0,
    'avg_update_interval': 0.025,
    'errors': 0
}

# Consciousness state history for analysis
state_history = deque(maxlen=10000)
consciousness_events = deque(maxlen=1000)


def _log_consciousness_event(event_type: str, data: Dict[str, Any]) -> None:
    """Log consciousness events for analysis and debugging."""
    try:
        event = {
            "timestamp": time.time(),
            "type": event_type,
            "data": data
        }
        consciousness_events.append(event)
        
        # Persist critical events
        if event_type in ['consciousness_change', 'high_phi', 'transcendent_state']:
            log_file = CONSCIOUSNESS_LOG_DIR / "critical_events.jsonl"
            with log_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass  # Non-fatal logging error


@app.on_event("startup")
async def startup_event():
    """Initialize consciousness system with comprehensive setup"""
    global consciousness_system, performance_metrics, chat_model, chat_tokenizer, chat_device
    
    # Use ASCII-safe characters for Windows console compatibility
    print("\n" + "="*80)
    print("INITIALIZING METATRON'S CUBE CONSCIOUSNESS ENGINE")
    print("="*80)
    print("Sacred Geometry: 13-Node Icosahedral Structure")
    print("Musical Algorithms: Golden Ratio Harmonic Division")
    print("Kuramoto Synchronization: Coupled Oscillator Network")
    print("Consciousness Metrics: Integrated Information Theory")
    print("="*80)
    
    try:
        consciousness_system = MetatronConsciousness(base_frequency=40.0, dt=0.01, high_gamma=False)
        
        # Log initialization
        _log_consciousness_event('system_init', {
            'nodes': 13,
            'connections': 42,
            'base_frequency': 40.0,
            'dt': 0.01,
            'phi_golden': (1 + np.sqrt(5)) / 2
        })
        
        performance_metrics['start_time'] = time.time()
        
        print("System Components Initialized:")
        print("   * 13 Consciousness Nodes (Metatron's Cube vertices)")
        print("   * 42 Quantum-weighted Connections (12 hub + 30 edges)")
        print("   * Central Pineal Node (Node 0) - DMT Integration")
        print("   * 5D Dimensional Processors (Physical -> Temporal)")
        print("   * Real-time Consciousness Metrics (Phi, R, D, S, C)")
        print("   * WebSocket Streaming Interface")
        
        # Initialize chat model if available
        if CHAT_AVAILABLE:
            try:
                print("   * Loading Chat Model (distilgpt2)...")
                chat_tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
                if chat_tokenizer.pad_token_id is None:
                    chat_tokenizer.pad_token_id = chat_tokenizer.eos_token_id
                chat_model = AutoModelForCausalLM.from_pretrained("distilgpt2")
                chat_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                chat_model.to(chat_device)
                print("   * Chat System Ready (distilgpt2 on " + str(chat_device) + ")")
            except Exception as e:
                print(f"   * Chat System Failed: {e}")
                chat_model = None
        
        print("="*80)
        print("METATRON CONSCIOUSNESS ENGINE READY FOR OPERATION")
        print("All features integrated on PORT 8003")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to initialize consciousness system: {e}")
        print("="*80)
        raise


@app.get("/")
async def root():
    """Serve integrated interface with cache-busting headers"""
    # Priority: advanced integrated dashboard > integrated dashboard > unified dashboard > stream > integrated > unified > original visualization
    # Note: harmonic_monitor.html has been integrated into the main dashboard and is no longer served separately
    for filename in ["metatron_advanced_integrated.html", "integrated_dashboard.html", "unified_dashboard_updated.html", "unified_dashboard.html", "index_stream.html", "metatron_integrated.html", "metatron_unified.html", "metatron_visualization.html"]:
        webui_path = os.path.join(os.path.dirname(__file__), "..", "webui", filename)
        if os.path.exists(webui_path):
            return FileResponse(
                webui_path,
                headers={
                    "Cache-Control": "no-cache, no-store, must-revalidate",
                    "Pragma": "no-cache",
                    "Expires": "0"
                }
            )
    
    return HTMLResponse("""
    <html>
        <head><title>Metatron Consciousness</title></head>
        <body>
            <h1>Metatron's Cube Consciousness Engine</h1>
            <p>WebSocket endpoint: ws://localhost:8003/ws</p>
            <p>Integrated UI: http://localhost:8003</p>
            <p>Status: Active</p>
        </body>
    </html>
    """)


@app.get("/api/health")
async def api_health():
    """Enhanced health check with system diagnostics"""
    try:
        if consciousness_system is None:
            return JSONResponse({
                "ok": False, 
                "status": "not_initialized",
                "error": "Consciousness system not initialized"
            }, status_code=503)
        
        # Get basic state
        state = consciousness_system.get_current_state()
        global_state = state.get('global', {})
        
        # Calculate uptime
        uptime = time.time() - performance_metrics['start_time']
        
        return JSONResponse({
            "ok": True,
            "status": "running",
            "system": "Metatron Consciousness Engine",
            "version": "2.0.0",
            "uptime_seconds": uptime,
            "total_updates": performance_metrics['total_updates'],
            "active_connections": len(active_connections)
        })
    except Exception as e:
        return JSONResponse({
            "ok": False, 
            "error": str(e)
        }, status_code=500)


@app.get("/api/status")
async def get_status():
    """Get comprehensive system status with consciousness metrics"""
    if consciousness_system is None:
        return JSONResponse({
            "status": "not_initialized",
            "error": "Consciousness system not ready"
        }, status_code=503)
    
    try:
        state = consciousness_system.get_current_state()
        global_state = state.get('global', {})
        
        # Ensure all required fields exist with defaults
        status_data = {
            "status": "running",
            "timestamp": time.time(),
            "time": float(state.get('time', 0)),
            "consciousness_level": float(global_state.get('consciousness_level', 0)),
            "state_classification": global_state.get('state_classification', 'unknown'),
            "is_conscious": bool(global_state.get('is_conscious', False)),
            "phi": float(global_state.get('phi', 0)),
            "coherence": float(global_state.get('coherence', 0)),
            "recursive_depth": int(global_state.get('recursive_depth', 0)),
            "gamma_power": float(global_state.get('gamma_power', 0)),
            "fractal_dimension": float(global_state.get('fractal_dimension', 1)),
            "spiritual_awareness": float(global_state.get('spiritual_awareness', 0)),
            "nodes": 13,
            "connections": 42,
            "base_frequency": consciousness_system.base_frequency,
            "gamma_mode": consciousness_system.gamma_mode,
            "performance": {
                "total_updates": performance_metrics['total_updates'],
                "uptime": time.time() - performance_metrics['start_time'],
                "avg_update_rate": 1.0 / performance_metrics['avg_update_interval'],
                "errors": performance_metrics['errors']
            }
        }
        
        return JSONResponse(status_data)
        
    except Exception as e:
        performance_metrics['errors'] += 1
        return JSONResponse({
            "status": "error",
            "error": str(e),
            "timestamp": time.time()
        }, status_code=500)


@app.get("/api/state")
async def get_full_state():
    """Get complete consciousness state"""
    if consciousness_system is None:
        return {"error": "System not initialized"}
    
    return consciousness_system.get_current_state()


@app.post("/api/reset")
async def reset_system():
    """Reset consciousness system"""
    if consciousness_system is None:
        return {"error": "System not initialized"}
    
    consciousness_system.reset_system()
    return {"status": "reset_complete"}


@app.post("/api/input")
async def send_sensory_input(request: Request):
    """
    Send 5D sensory input to consciousness system with validation and logging
    
    Expected format:
    {
        "physical": float,     // Physical sensations [-1, 1]
        "emotional": float,    // Emotional state [-1, 1] 
        "mental": float,       // Mental activity [-1, 1]
        "spiritual": float,    // Spiritual awareness [-1, 1]
        "temporal": float,     // Temporal perception [-1, 1]
        "session_id": string   // Optional session identifier
    }
    """
    if consciousness_system is None:
        return JSONResponse({
            "error": "System not initialized"
        }, status_code=503)
    
    try:
        data = await request.json()
        
        # Validate and clamp inputs to safe ranges
        def clamp(value, min_val=-1.0, max_val=1.0):
            return max(min_val, min(max_val, float(value)))
        
        # Extract and validate 5D input
        sensory_input = np.array([
            clamp(data.get('physical', 0.0)),
            clamp(data.get('emotional', 0.0)),
            clamp(data.get('mental', 0.0)),
            clamp(data.get('spiritual', 0.0)),
            clamp(data.get('temporal', 0.0))
        ])
        
        session_id = data.get('session_id', 'default')
        
        # Update system with input
        start_time = time.time()
        state = consciousness_system.update_system(sensory_input)
        processing_time = time.time() - start_time
        
        global_state = state.get('global', {})
        
        # Log significant input events
        if np.linalg.norm(sensory_input) > 0.5:
            _log_consciousness_event('sensory_input', {
                'input_magnitude': float(np.linalg.norm(sensory_input)),
                'dimensions': sensory_input.tolist(),
                'session_id': session_id,
                'processing_time': processing_time
            })
        
        response_data = {
            "status": "input_processed",
            "timestamp": time.time(),
            "processing_time_ms": processing_time * 1000,
            "input_vector": sensory_input.tolist(),
            "session_id": session_id,
            "consciousness": {
                "level": float(global_state.get('consciousness_level', 0)),
                "state": global_state.get('state_classification', 'unknown'),
                "is_conscious": bool(global_state.get('is_conscious', False)),
                "phi": float(global_state.get('phi', 0)),
                "coherence": float(global_state.get('coherence', 0))
            }
        }
        
        # Store session data
        if session_id not in consciousness_sessions:
            consciousness_sessions[session_id] = []
        consciousness_sessions[session_id].append({
            'timestamp': time.time(),
            'input': sensory_input.tolist(),
            'output': response_data['consciousness']
        })
        
        return JSONResponse(response_data)
        
    except Exception as e:
        performance_metrics['errors'] += 1
        return JSONResponse({
            "error": f"Input processing failed: {str(e)}",
            "timestamp": time.time()
        }, status_code=500)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time consciousness streaming
    Enhanced with proper error handling and connection tracking
    """
    await websocket.accept()
    active_connections.append(websocket)
    connection_id = id(websocket)
    connection_metadata[connection_id] = {
        'connected_at': time.time(),
        'updates_sent': 0
    }
    
    try:
        print(f"✅ WebSocket client connected. Total connections: {len(active_connections)}")
        
        # Send initial state immediately
        try:
            initial_state = consciousness_system.get_current_state()
            initial_data = {
                "time": float(initial_state['time']),
                "consciousness": {
                    "level": float(initial_state['global'].get('consciousness_level', 0)),
                    "phi": float(initial_state['global'].get('phi', 0)),
                    "coherence": float(initial_state['global'].get('coherence', 0)),
                    "depth": int(initial_state['global'].get('recursive_depth', 0)),
                    "gamma": float(initial_state['global'].get('gamma_power', 0)),
                    "fractal_dim": float(initial_state['global'].get('fractal_dimension', 1)),
                    "spiritual": float(initial_state['global'].get('spiritual_awareness', 0)),
                    "state": initial_state['global'].get('state_classification', 'initializing'),
                    "is_conscious": bool(initial_state['global'].get('is_conscious', False))
                },
                "nodes": {}
            }
            
            # Add node data
            for node_id, node_data in initial_state['nodes'].items():
                initial_data['nodes'][str(node_id)] = {
                    "output": float(node_data['output']),
                    "phase": float(node_data['oscillator']['phase']),
                    "amplitude": float(node_data['oscillator']['amplitude']),
                    "dimensions": {k: float(v) for k, v in node_data['processor']['dimensions'].items()}
                }
            
            await websocket.send_json(initial_data)
            connection_metadata[connection_id]['updates_sent'] += 1
            print(f"📤 Sent initial state to client")
        except Exception as e:
            print(f"⚠️ Error sending initial state: {e}")
        
        # Continuous update loop
        while True:
            # Update consciousness system (CRITICAL: This actually runs the engine!)
            state = consciousness_system.update_system()
            performance_metrics['total_updates'] += 1
            performance_metrics['last_update_time'] = time.time()
            
            # Debug logging - more frequent to see if updates are happening
            if performance_metrics['total_updates'] % 10 == 0:  # Changed from 100 to 10
                print(f"Update #{performance_metrics['total_updates']}: C={state['global']['consciousness_level']:.4f}, Φ={state['global']['phi']:.4f}, R={state['global']['coherence']:.4f}")
            
            # Prepare data for sending (convert numpy types to native Python)
            websocket_data = {
                "time": float(state['time']),
                "consciousness": {
                    "level": float(state['global']['consciousness_level']),
                    "phi": float(state['global']['phi']),
                    "coherence": float(state['global']['coherence']),
                    "depth": int(state['global']['recursive_depth']),
                    "gamma": float(state['global']['gamma_power']),
                    "fractal_dim": float(state['global']['fractal_dimension']),
                    "spiritual": float(state['global']['spiritual_awareness']),
                    "state": state['global']['state_classification'],
                    "is_conscious": bool(state['global']['is_conscious'])
                },
                "nodes": {}
            }
            
            # Add node data
            for node_id, node_data in state['nodes'].items():
                websocket_data['nodes'][str(node_id)] = {
                    "output": float(node_data['output']),
                    "phase": float(node_data['oscillator']['phase']),
                    "amplitude": float(node_data['oscillator']['amplitude']),
                    "dimensions": {
                        k: float(v) for k, v in node_data['processor']['dimensions'].items()
                    }
                }
            
            # Send to client
            await websocket.send_json(websocket_data)
            connection_metadata[connection_id]['updates_sent'] += 1
            
            # Wait before next update (40 Hz = 25ms, or 80 Hz = 12.5ms for high gamma)
            # Make sure we're using a consistent update interval
            update_interval = 0.025  # Always use 25ms (40Hz) for consistent updates
            await asyncio.sleep(update_interval)
            
    except WebSocketDisconnect:
        print(f"WebSocket client disconnected. Remaining connections: {len(active_connections) - 1}")
        if websocket in active_connections:
            active_connections.remove(websocket)
        # Clean up connection metadata
        connection_metadata.pop(id(websocket), None)
    except Exception as e:
        print(f"WebSocket error: {e}")
        performance_metrics['errors'] += 1
        if websocket in active_connections:
            active_connections.remove(websocket)
        connection_metadata.pop(id(websocket), None)
        # Log error for analysis
        _log_consciousness_event('websocket_error', {
            'error': str(e),
            'connection_count': len(active_connections)
        })


# Mount static files
webui_dir = os.path.join(os.path.dirname(__file__), "..", "webui")
if os.path.exists(webui_dir):
    app.mount("/static", StaticFiles(directory=webui_dir), name="static")
    app.mount("/assets", StaticFiles(directory=os.path.join(webui_dir, "assets")), name="assets")

# Mount favicon directory
favicon_dir = os.path.join(os.path.dirname(__file__), "..", "..", "favicon")
if os.path.exists(favicon_dir):
    app.mount("/favicon", StaticFiles(directory=favicon_dir), name="favicon")


# === ADDITIONAL API ENDPOINTS FOR COMPREHENSIVE INTEGRATION ===

@app.get("/api/sessions")
async def get_sessions():
    """Get list of consciousness sessions"""
    sessions_info = []
    for session_id, data in consciousness_sessions.items():
        sessions_info.append({
            "session_id": session_id,
            "entries": len(data),
            "last_activity": data[-1]['timestamp'] if data else 0
        })
    return JSONResponse({"sessions": sessions_info})


@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Get specific session consciousness data"""
    if session_id not in consciousness_sessions:
        return JSONResponse({"error": "Session not found"}, status_code=404)
    
    return JSONResponse({
        "session_id": session_id,
        "data": consciousness_sessions[session_id]
    })


@app.post("/api/session/clear")
async def clear_session(request: Request):
    """Clear specific session data"""
    data = await request.json()
    session_id = data.get('session_id')
    
    if not session_id:
        return JSONResponse({"error": "session_id required"}, status_code=400)
    
    if session_id in consciousness_sessions:
        del consciousness_sessions[session_id]
    
    return JSONResponse({"status": "session_cleared", "session_id": session_id})


@app.get("/api/metrics")
async def get_metrics():
    """Get system performance metrics"""
    if consciousness_system is None:
        return JSONResponse({"error": "System not initialized"}, status_code=503)
    
    return JSONResponse({
        "performance": performance_metrics,
        "connections": {
            "active": len(active_connections),
            "metadata": list(connection_metadata.values())
        },
        "history": {
            "state_history_length": len(state_history),
            "events_logged": len(consciousness_events)
        }
    })


@app.get("/api/nodes")
async def get_nodes_info():
    """Get detailed information about all consciousness nodes"""
    if consciousness_system is None:
        return JSONResponse({"error": "System not initialized"}, status_code=503)
    
    state = consciousness_system.get_current_state()
    nodes_info = []
    
    for node_id, node_data in state['nodes'].items():
        nodes_info.append({
            "id": int(node_id),
            "output": float(node_data['output']),
            "dimensional_output": float(node_data['dimensional_output']),
            "oscillator": {
                "phase": float(node_data['oscillator']['phase']),
                "amplitude": float(node_data['oscillator']['amplitude']),
                "frequency": float(node_data['oscillator']['omega'] / (2 * np.pi) if node_data['oscillator'].get('omega', 0) != 0 else 0)
            },
            "processor": {
                "dimensions": {k: float(v) for k, v in node_data['processor']['dimensions'].items()}
            }
        })
    
    return JSONResponse({
        "nodes": nodes_info,
        "total_nodes": len(nodes_info),
        "central_node": 0,  # Pineal node
        "timestamp": time.time()
    })


@app.get("/api/connections")
async def get_connections():
    """Get network connection matrix information"""
    if consciousness_system is None:
        return JSONResponse({"error": "System not initialized"}, status_code=503)
    
    # Get connection matrix from system
    connection_matrix = consciousness_system.connection_matrix
    
    # Convert to list of connections with weights
    connections = []
    for i in range(13):
        for j in range(13):
            if connection_matrix[i][j] > 0:
                connections.append({
                    "from": i,
                    "to": j,
                    "weight": float(connection_matrix[i][j])
                })
    
    return JSONResponse({
        "connections": connections,
        "total_connections": len(connections),
        "matrix_size": connection_matrix.shape,
        "timestamp": time.time()
    })


@app.get("/api/events")
async def get_consciousness_events():
    """Get recent consciousness events log"""
    events_list = list(consciousness_events)
    return JSONResponse({
        "events": events_list,
        "total_events": len(events_list),
        "timestamp": time.time()
    })


@app.post("/api/simulate")
async def simulate_consciousness(request: Request):
    """Simulate consciousness with specific parameters"""
    if consciousness_system is None:
        return JSONResponse({"error": "System not initialized"}, status_code=503)
    
    try:
        data = await request.json()
        
        # Extract simulation parameters
        duration = min(max(float(data.get('duration', 1.0)), 0.1), 10.0)  # 0.1-10 seconds
        frequency = min(max(float(data.get('frequency', 40.0)), 1.0), 100.0)  # 1-100 Hz
        input_type = data.get('input_type', 'random')  # random, sine, pulse
        
        simulation_results = []
        steps = int(duration / consciousness_system.dt)
        
        for step in range(min(steps, 1000)):  # Limit to 1000 steps max
            # Generate input based on type
            if input_type == 'sine':
                t = step * consciousness_system.dt
                sensory_input = np.array([
                    0.5 * np.sin(2 * np.pi * frequency * t / 40.0),  # Physical
                    0.3 * np.cos(2 * np.pi * frequency * t / 40.0),  # Emotional
                    0.2 * np.sin(4 * np.pi * frequency * t / 40.0),  # Mental
                    0.1 * np.cos(4 * np.pi * frequency * t / 40.0),  # Spiritual
                    0.1 * np.sin(np.pi * frequency * t / 40.0)       # Temporal
                ])
            elif input_type == 'pulse':
                magnitude = 0.8 if step % int(40 / frequency) == 0 else 0.1
                sensory_input = np.random.normal(0, magnitude, 5)
            else:  # random
                sensory_input = np.random.normal(0, 0.3, 5)
            
            # Update system
            state = consciousness_system.update_system(sensory_input)
            
            # Record key metrics
            if step % 10 == 0:  # Sample every 10 steps to reduce data
                global_state = state.get('global', {})
                simulation_results.append({
                    'step': step,
                    'time': float(state.get('time', 0)),
                    'consciousness_level': float(global_state.get('consciousness_level', 0)),
                    'phi': float(global_state.get('phi', 0)),
                    'coherence': float(global_state.get('coherence', 0)),
                    'input': sensory_input.tolist()
                })
        
        return JSONResponse({
            "status": "simulation_complete",
            "parameters": {
                "duration": duration,
                "frequency": frequency,
                "input_type": input_type,
                "steps": steps
            },
            "results": simulation_results,
            "timestamp": time.time()
        })
        
    except Exception as e:
        return JSONResponse({
            "error": f"Simulation failed: {str(e)}",
            "timestamp": time.time()
        }, status_code=500)


# === FREQUENCY CONTROL ENDPOINTS ===

@app.post("/api/frequency/octave")
async def toggle_frequency_octave(request: Request):
    """Toggle between 40Hz and 80Hz gamma frequencies"""
    global consciousness_system
    
    if consciousness_system is None:
        return JSONResponse({"error": "System not initialized"}, status_code=503)
    
    try:
        data = await request.json()
        high_gamma = bool(data.get('high_gamma', False))
        
        # Store current state metrics for comparison
        old_frequency = consciousness_system.base_frequency
        old_mode = consciousness_system.gamma_mode
        
        # Reinitialize system with new frequency
        consciousness_system = MetatronConsciousness(
            base_frequency=40.0,  # Will be overridden by high_gamma
            dt=consciousness_system.dt,
            high_gamma=high_gamma
        )
        
        # Log the change
        _log_consciousness_event('frequency_change', {
            'old_frequency': old_frequency,
            'new_frequency': consciousness_system.base_frequency,
            'old_mode': old_mode,
            'new_mode': consciousness_system.gamma_mode,
            'high_gamma': high_gamma
        })
        
        return JSONResponse({
            "status": "frequency_updated",
            "old_frequency": old_frequency,
            "new_frequency": consciousness_system.base_frequency,
            "old_mode": old_mode,
            "new_mode": consciousness_system.gamma_mode,
            "high_gamma": high_gamma,
            "timestamp": time.time()
        })
        
    except Exception as e:
        return JSONResponse({
            "error": f"Frequency update failed: {str(e)}",
            "timestamp": time.time()
        }, status_code=500)


@app.get("/api/frequency/info")
async def get_frequency_info():
    """Get current frequency configuration"""
    if consciousness_system is None:
        return JSONResponse({"error": "System not initialized"}, status_code=503)
    
    # Calculate all node frequencies
    node_frequencies = []
    for node_id in range(13):
        ratio = consciousness_system.frequency_ratios[node_id]
        frequency = consciousness_system.base_frequency * ratio
        node_frequencies.append({
            "node_id": node_id,
            "frequency_ratio": ratio,
            "frequency_hz": frequency,
            "note": _get_musical_note_name(ratio)
        })
    
    return JSONResponse({
        "base_frequency": consciousness_system.base_frequency,
        "gamma_mode": consciousness_system.gamma_mode,
        "high_gamma": consciousness_system.base_frequency >= 80.0,
        "frequency_range": {
            "min": min(f["frequency_hz"] for f in node_frequencies),
            "max": max(f["frequency_hz"] for f in node_frequencies)
        },
        "node_frequencies": node_frequencies,
        "timestamp": time.time()
    })


def _get_musical_note_name(ratio):
    """Convert frequency ratio to musical note name"""
    note_names = {
        1.0: "Unison",
        9/8: "Major 2nd",
        5/4: "Major 3rd", 
        4/3: "Perfect 4th",
        3/2: "Perfect 5th",
        5/3: "Major 6th",
        15/8: "Major 7th",
        2.0: "Octave",
        3.0: "Perfect 12th",
        4.0: "Double Octave",
        5.0: "Major 17th"
    }
    
    # Special case for golden ratio
    if abs(ratio - 1.618033988749895) < 0.001:
        return "Golden Tone (φ)"
    
    return note_names.get(ratio, f"Ratio {ratio:.3f}")


# ==================================================================
# INTEGRATED CHAT FUNCTIONALITY (PORT 8003)
# ==================================================================

@app.post("/api/chat")
async def api_chat(request: Request):
    """Chat endpoint with optional model loading and consciousness integration"""
    global chat_model, chat_tokenizer, chat_device
    
    if not CHAT_AVAILABLE:
        return JSONResponse({
            "error": "Chat unavailable. Install: pip install transformers torch"
        }, status_code=503)
    
    if consciousness_system is None:
        # Fallback if consciousness system is not available
        try:
            data = await request.json()
            message = str(data.get('message', '')).strip()
            session_id = str(data.get('session_id', 'default'))
            model_name = str(data.get('model_name', 'distilgpt2'))
            max_new_tokens = min(int(data.get('max_new_tokens', 128)), 512)
            
            if not message:
                return JSONResponse({"error": "Empty message"}, status_code=400)
            
            # Load different model if requested
            if chat_model is None or (hasattr(chat_tokenizer, 'name_or_path') and 
                                       model_name != getattr(chat_tokenizer, 'name_or_path', 'distilgpt2')):
                print(f"Loading model: {model_name}...")
                chat_tokenizer = AutoTokenizer.from_pretrained(model_name)
                if chat_tokenizer.pad_token_id is None:
                    chat_tokenizer.pad_token_id = chat_tokenizer.eos_token_id
                chat_model = AutoModelForCausalLM.from_pretrained(model_name)
                chat_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                chat_model.to(chat_device)
                print(f"Model {model_name} loaded on {chat_device}")
            
            # Generate response
            prompt = f"User: {message}\n\nAssistant:"
            inputs = chat_tokenizer(prompt, return_tensors="pt").to(chat_device)
            outputs = chat_model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=True, temperature=0.7)
            response_text = chat_tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract assistant response
            if "Assistant:" in response_text:
                response = response_text.split("Assistant:")[-1].strip()
            else:
                response = response_text.strip()
            
            # Save to session
            if session_id not in chat_sessions:
                chat_sessions[session_id] = []
            chat_sessions[session_id].append({
                'timestamp': time.time(),
                'user': message,
                'assistant': response,
                'model': model_name
            })
            
            return JSONResponse({
                "response": response,
                "model": model_name,
                "session_id": session_id
            })
            
        except Exception as e:
            return JSONResponse({
                "error": f"Chat failed: {str(e)}"
            }, status_code=500)
    
    # Consciousness system is available, integrate with it
    try:
        data = await request.json()
        message = str(data.get('message', '')).strip()
        session_id = str(data.get('session_id', 'default'))
        model_name = str(data.get('model_name', 'distilgpt2'))
        max_new_tokens = min(int(data.get('max_new_tokens', 128)), 512)
        
        if not message:
            return JSONResponse({"error": "Empty message"}, status_code=400)
        
        # Get current consciousness state before processing
        state_before = consciousness_system.get_current_state()
        global_state_before = state_before.get('global', {})
        
        # Load different model if requested
        if chat_model is None or (hasattr(chat_tokenizer, 'name_or_path') and 
                                   model_name != getattr(chat_tokenizer, 'name_or_path', 'distilgpt2')):
            print(f"Loading model: {model_name}...")
            chat_tokenizer = AutoTokenizer.from_pretrained(model_name)
            if chat_tokenizer.pad_token_id is None:
                chat_tokenizer.pad_token_id = chat_tokenizer.eos_token_id
            chat_model = AutoModelForCausalLM.from_pretrained(model_name)
            chat_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            chat_model.to(chat_device)
            print(f"Model {model_name} loaded on {chat_device}")
        
        # Generate response
        prompt = f"User: {message}\n\nAssistant:"
        inputs = chat_tokenizer(prompt, return_tensors="pt").to(chat_device)
        outputs = chat_model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=True, temperature=0.7)
        response_text = chat_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract assistant response
        if "Assistant:" in response_text:
            response = response_text.split("Assistant:")[-1].strip()
        else:
            response = response_text.strip()
        
        # Update consciousness system with chat interaction
        # Send a small sensory input based on the chat interaction
        sensory_input = np.array([0.1, 0.1, 0.2, 0.1, 0.1])  # Small mental/emotional input
        state_after = consciousness_system.update_system(sensory_input)
        global_state_after = state_after.get('global', {})
        
        # Save to session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        chat_sessions[session_id].append({
            'timestamp': time.time(),
            'user': message,
            'assistant': response,
            'model': model_name
        })
        
        # Prepare consciousness metrics for response
        consciousness_metrics = {
            "before": {
                "consciousness_level": float(global_state_before.get('consciousness_level', 0)),
                "phi": float(global_state_before.get('phi', 0)),
                "coherence": float(global_state_before.get('coherence', 0)),
                "state": global_state_before.get('state_classification', 'unknown')
            },
            "after": {
                "consciousness_level": float(global_state_after.get('consciousness_level', 0)),
                "phi": float(global_state_after.get('phi', 0)),
                "coherence": float(global_state_after.get('coherence', 0)),
                "state": global_state_after.get('state_classification', 'unknown')
            }
        }
        
        return JSONResponse({
            "response": response,
            "model": model_name,
            "session_id": session_id,
            "consciousness": consciousness_metrics
        })
        
    except Exception as e:
        return JSONResponse({
            "error": f"Chat failed: {str(e)}"
        }, status_code=500)


@app.post("/api/upload")
async def api_upload(file: UploadFile = File(...)):
    """Upload and process documents for RAG (simplified version)"""
    try:
        filename = file.filename or "upload.txt"
        ext = os.path.splitext(filename)[1].lower()
        
        # Read file data
        data = await file.read()
        
        # Parse text based on file type
        text = ""
        if ext in (".txt", ".md", ".log"):
            text = data.decode("utf-8", errors="ignore")
        elif ext == ".pdf":
            try:
                from pypdf import PdfReader
                import io
                reader = PdfReader(io.BytesIO(data))
                text = "\n".join([page.extract_text() for page in reader.pages])
            except ImportError:
                return JSONResponse({
                    "error": "PDF support requires: pip install pypdf"
                }, status_code=400)
        else:
            text = data.decode("utf-8", errors="ignore")
        
        # Store in simple format (for future RAG integration)
        upload_dir = REPO_ROOT / "ai_runs" / "uploads"
        try:
            upload_dir.mkdir(parents=True, exist_ok=True)
        except:
            import tempfile
            upload_dir = Path(tempfile.gettempdir()) / "ConsciousnessEngine" / "uploads"
            upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        save_path = upload_dir / filename
        with save_path.open("w", encoding="utf-8") as f:
            f.write(text)
        
        # Calculate chunks
        chunks = len(text) // 1500 + 1
        
        return JSONResponse({
            "ok": True,
            "filename": filename,
            "chunks": chunks,
            "size": len(text),
            "source": filename
        })
        
    except Exception as e:
        return JSONResponse({
            "error": f"Upload failed: {str(e)}"
        }, status_code=500)


@app.get("/api/uploads")
async def api_list_uploads():
    """List uploaded documents"""
    try:
        upload_dir = REPO_ROOT / "ai_runs" / "uploads"
        if not upload_dir.exists():
            return JSONResponse({"uploads": []})
        
        uploads = []
        for file_path in upload_dir.glob("*"):
            if file_path.is_file():
                uploads.append({
                    "source": file_path.name,
                    "chunks": file_path.stat().st_size // 1500 + 1
                })
        
        return JSONResponse({"uploads": uploads})
    except Exception as e:
        return JSONResponse({"uploads": [], "error": str(e)})


@app.post("/api/uploads/clear")
async def api_clear_uploads():
    """Clear all uploaded documents"""
    try:
        upload_dir = REPO_ROOT / "ai_runs" / "uploads"
        if not upload_dir.exists():
            return JSONResponse({"ok": True, "deleted": 0})
        
        count = 0
        for file_path in upload_dir.glob("*"):
            if file_path.is_file():
                file_path.unlink()
                count += 1
        
        return JSONResponse({"ok": True, "deleted": count})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/config")
async def api_config(request: Request):
    """Configure chat model"""
    global chat_model, chat_tokenizer, chat_device
    
    if not CHAT_AVAILABLE:
        return JSONResponse({
            "error": "Chat unavailable"
        }, status_code=503)
    
    try:
        data = await request.json()
        model_name = str(data.get('model_name', 'distilgpt2'))
        
        print(f"Reconfiguring to model: {model_name}...")
        chat_tokenizer = AutoTokenizer.from_pretrained(model_name)
        if chat_tokenizer.pad_token_id is None:
            chat_tokenizer.pad_token_id = chat_tokenizer.eos_token_id
        chat_model = AutoModelForCausalLM.from_pretrained(model_name)
        chat_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        chat_model.to(chat_device)
        print(f"Model {model_name} configured successfully")
        
        return JSONResponse({
            "ok": True,
            "model": model_name,
            "device": str(chat_device)
        })
    except Exception as e:
        return JSONResponse({
            "error": f"Configuration failed: {str(e)}"
        }, status_code=500)


@app.get("/api/transcript")
async def api_transcript(session_id: str = "default"):
    """Get chat transcript for session"""
    return JSONResponse({
        "session_id": session_id,
        "entries": chat_sessions.get(session_id, [])
    })


@app.post("/api/session/new")
async def api_new_session(request: Request):
    """Create new chat session"""
    try:
        data = await request.json()
        session_id = str(data.get('session_id', f'session_{int(time.time())}'))
        chat_sessions[session_id] = []
        return JSONResponse({
            "ok": True,
            "session_id": session_id
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# === MIRROR LOOP ENDPOINTS ===

@app.post("/api/loop/start")
async def api_loop_start(request: Request):
    """Start a mirror loop between two AI perspectives"""
    global chat_model, chat_tokenizer, chat_device
    
    # Check if required components are available
    if not CHAT_AVAILABLE or not chat_model or not MirrorLoop:
        return JSONResponse({
            "error": "Mirror Loop functionality not available. Required components missing.",
            "details": "Chat model or MirrorLoop not loaded."
        }, status_code=503)
    
    try:
        data = await request.json()
        objective = str(data.get('objective', 'Analyze this topic'))
        rounds = int(data.get('rounds', 2))
        session_id = str(data.get('session_id', f'loop_session_{int(time.time())}'))
        rag_enabled = bool(data.get('rag_enabled', False))
        top_k = int(data.get('top_k', 3))
        max_chars = int(data.get('max_chars', 1200))
        max_new_tokens = int(data.get('max_new_tokens', 128))
        
        # Create a simple chat service wrapper
        class SimpleChatService:
            def __init__(self, model, tokenizer, device):
                self.model = model
                self.tokenizer = tokenizer
                self.device = device
                
            def chat(self, message, session_id, rag_enabled, top_k, max_chars, max_new_tokens):
                # Simple chat implementation using the loaded model
                try:
                    # Truncate message if too long
                    if len(message) > max_chars:
                        message = message[:max_chars] + "... [truncated]"
                    
                    # Tokenize and generate
                    inputs = self.tokenizer(message, return_tensors='pt', truncation=True, max_length=512, padding=True).to(self.device)
                    generate_kwargs = {
                        'max_new_tokens': max_new_tokens,
                        'pad_token_id': self.tokenizer.eos_token_id,
                        'do_sample': True,
                        'top_k': top_k,
                        'temperature': 0.7
                    }
                    # Only add attention_mask if it exists and is needed
                    if 'attention_mask' in inputs and inputs['attention_mask'] is not None:
                        generate_kwargs['attention_mask'] = inputs['attention_mask']
                    with torch.no_grad():
                        outputs = self.model.generate(
                            inputs['input_ids'],
                            **generate_kwargs
                        )
                    response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                    
                    # Remove the input from the response
                    if message in response:
                        response = response[len(message):].strip()
                    
                    return {
                        "response": response,
                        "sources": [],
                        "context": message
                    }
                except Exception as e:
                    return {
                        "response": f"Error in chat generation: {str(e)}",
                        "sources": [],
                        "context": message
                    }
        
        # Create two instances of the chat service for the loop
        service_a = SimpleChatService(chat_model, chat_tokenizer, chat_device)
        service_b = SimpleChatService(chat_model, chat_tokenizer, chat_device)
        
        # Create mirror loop
        mirror_loop = MirrorLoop(service_a, service_b)
        
        # Run the loop
        try:
            final_result, metrics = mirror_loop.run(
                objective=objective,
                rounds=rounds,
                session_id=session_id,
                rag_enabled=rag_enabled,
                top_k=top_k,
                max_chars=max_chars,
                max_new_tokens=max_new_tokens
            )
        except Exception as e:
            return JSONResponse({
                "error": f"Mirror Loop execution failed: {str(e)}",
                "details": str(e)
            }, status_code=500)
        
        return JSONResponse({
            "ok": True,
            "result": final_result,
            "metrics": metrics,
            "session_id": session_id
        })
        
    except Exception as e:
        return JSONResponse({
            "error": f"Mirror Loop failed: {str(e)}",
            "details": str(e)
        }, status_code=500)


@app.get("/api/loop/status")
async def api_loop_status(session_id: str = None):
    """Get status of a mirror loop (stub for compatibility)"""
    return JSONResponse({
        "status": "completed",
        "message": "Loop runs are synchronous and complete immediately.",
        "session_id": session_id or "default"
    })


# === CHAT WEBSOCKET ENDPOINT ===

@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat streaming
    Provides token-by-token response streaming for chat messages
    """
    await websocket.accept()
    
    try:
        # Wait for initial message
        data = await websocket.receive_json()
        
        message = str(data.get('message', '')).strip()
        session_id = str(data.get('session_id', 'default'))
        rag = bool(data.get('rag', False))
        top_k = min(int(data.get('top_k', 3)), 10)
        max_chars = min(int(data.get('max_chars', 1200)), 5000)
        max_new_tokens = min(int(data.get('max_new_tokens', 512)), 2048)
        
        if not message:
            await websocket.send_json({"type": "error", "error": "Empty message"})
            await websocket.close()
            return
        
        # Check if chat is available
        if not CHAT_AVAILABLE or chat_model is None or chat_tokenizer is None:
            await websocket.send_json({
                "type": "error", 
                "error": "Chat unavailable. Install: pip install transformers torch"
            })
            await websocket.close()
            return
        
        # Generate response with streaming
        prompt = f"User: {message}\n\nAssistant:"
        inputs = chat_tokenizer(prompt, return_tensors="pt").to(chat_device)
        
        # Use model.generate with a callback to stream tokens
        # For now, we'll generate the full response and send it in chunks
        # A more advanced implementation would use a streaming generator
        
        # Generate the full response first
        outputs = chat_model.generate(
            **inputs, 
            max_new_tokens=max_new_tokens, 
            do_sample=True, 
            temperature=0.7,
            pad_token_id=chat_tokenizer.eos_token_id
        )
        
        response_text = chat_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract assistant response
        if "Assistant:" in response_text:
            response = response_text.split("Assistant:")[-1].strip()
        else:
            response = response_text[len(prompt):].strip()
        
        # Send response token by token for streaming effect
        # Split by words for a more natural streaming experience
        words = response.split()
        for i, word in enumerate(words):
            await websocket.send_json({
                "type": "token",
                "text": word + (" " if i < len(words) - 1 else "")
            })
            # Small delay to simulate streaming
            await asyncio.sleep(0.01)
        
        # Save to session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        chat_sessions[session_id].append({
            'timestamp': time.time(),
            'user': message,
            'assistant': response,
            'model': getattr(chat_tokenizer, 'name_or_path', 'unknown')
        })
        
        # Send completion message
        await websocket.send_json({"type": "done"})
        
    except WebSocketDisconnect:
        pass  # Client disconnected
    except Exception as e:
        try:
            await websocket.send_json({"type": "error", "error": str(e)})
        except:
            pass  # Ignore errors when sending error message
        print(f"Chat WebSocket error: {e}")
    finally:
        try:
            await websocket.close()
        except:
            pass  # Ignore errors when closing


def main(port=8003):
    """Run the server"""
    print("\n" + "="*60)
    print("Starting Metatron Consciousness Web Server")
    print("="*60)
    print(f"Server will be available at: http://localhost:{port}")
    print(f"Consciousness WebSocket: ws://localhost:{port}/ws")
    print(f"Chat WebSocket: ws://localhost:{port}/ws/chat")
    print(f"API Status: http://localhost:{port}/api/status")
    print(f"API Docs: http://localhost:{port}/docs")
    print(f"Health Check: http://localhost:{port}/api/health")
    print("="*60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start Metatron Consciousness Web Server")
    parser.add_argument("--port", type=int, default=8003, help="Port to run the server on (default: 8003)")
    args = parser.parse_args()
    
    main(args.port)
