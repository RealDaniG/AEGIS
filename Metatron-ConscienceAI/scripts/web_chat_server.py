#!/usr/bin/env python
"""
Dedicated Web Chat Server for ConscienceAI
=========================================

Separate FastAPI server for chat functionality with RAG integration,
running on port 5180 to match KaseMaster's implementation.

Features:
- HTTP POST chat endpoint (primary)
- Optional WebSocket streaming (with fallback)
- RAG document integration
- Session management
- Tor Browser compatibility (fallback to HTTP)
"""

import os
import sys
import json
import time
import uuid
import asyncio
from pathlib import Path
from typing import List, Dict, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

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

# Import RAG functionality
try:
    from consciousness_engine.scripts.simple_rag import RagRetriever
    RAG_AVAILABLE = True
except ImportError:
    print("Warning: RAG functionality not available.")
    RAG_AVAILABLE = False
    RagRetriever = None

# Create FastAPI app
app = FastAPI(title="ConscienceAI Web Chat Server")

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
CHAT_LOG_DIR = REPO_ROOT / "ai_runs" / "chat_logs"
WEBUI_DIR = REPO_ROOT / "webui"
try:
    CHAT_LOG_DIR.mkdir(parents=True, exist_ok=True)
except (PermissionError, OSError):
    # Fallback to user's temp directory if Program Files is read-only
    import tempfile
    CHAT_LOG_DIR = Path(tempfile.gettempdir()) / "ConscienceAI" / "chat_logs"
    try:
        CHAT_LOG_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

# Mount static files if webui directory exists
if WEBUI_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEBUI_DIR)), name="static")

# Global chat system instance
chat_model = None
chat_tokenizer = None
chat_device = None
chat_sessions = {}

# Active WebSocket connections
active_chat_connections = []
chat_connection_metadata = {}

# Performance monitoring
chat_performance_metrics = {
    'total_messages': 0,
    'start_time': time.time(),
    'errors': 0
}

# RAG system
rag_retriever = None


def build_prompt(context: str, user_text: str) -> str:
    """Build prompt with context and user message."""
    parts = []
    if context:
        parts.append("[Contexto recuperado]\n" + context.strip() + "\n")
    parts.append("[Usuario]\n" + user_text.strip() + "\n\n[Asistente]")
    return "\n".join(parts)


@app.on_event("startup")
async def startup_event():
    """Initialize chat system with comprehensive setup."""
    global chat_model, chat_tokenizer, chat_device, rag_retriever
    
    print("\n" + "="*60)
    print("INITIALIZING CONSCIENCEAI WEB CHAT SERVER")
    print("="*60)
    print("Dedicated Chat Server: Port 5180")
    print("HTTP POST Endpoint: /api/chat")
    print("WebSocket Endpoint: /ws/chat (with fallback)")
    print("RAG Integration: Available" if RAG_AVAILABLE else "RAG Integration: Not Available")
    print("Static Files: " + str(WEBUI_DIR) if WEBUI_DIR.exists() else "Static Files: Not Available")
    print("="*60)
    
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
    
    # Initialize RAG if available
    if RAG_AVAILABLE:
        try:
            rag_corpus_path = REPO_ROOT / "datasets" / "rss_research.jsonl"
            if rag_corpus_path.exists():
                print(f"   * Loading RAG Corpus: {rag_corpus_path}")
                rag_retriever = RagRetriever(str(rag_corpus_path))
                print(f"   * RAG Documents: {len(rag_retriever.docs)}")
            else:
                print("   * RAG Corpus not found, RAG disabled")
                rag_retriever = None
        except Exception as e:
            print(f"   * RAG Initialization Failed: {e}")
            rag_retriever = None
    
    print("="*60)
    print("CONSCIENCEAI WEB CHAT SERVER READY")
    print("All features integrated on PORT 5180")
    print("="*60 + "\n")


@app.get("/")
async def root():
    """Serve chat interface."""
    return HTMLResponse("""
    <html>
        <head>
            <title>ConscienceAI Web Chat</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .container { max-width: 800px; margin: 0 auto; }
                .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
                .user { background-color: #e3f2fd; }
                .assistant { background-color: #f5f5f5; }
                .system { background-color: #fff3e0; }
                #chat { height: 400px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; margin: 10px 0; }
                #input { width: 70%; padding: 10px; }
                button { padding: 10px 15px; margin: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>ConscienceAI Web Chat</h1>
                <div id="chat"></div>
                <input type="text" id="input" placeholder="Type your message...">
                <button onclick="sendMessage()">Send</button>
                <button onclick="clearChat()">Clear</button>
                <br><br>
                <label><input type="checkbox" id="ragToggle" checked> Enable RAG</label>
                <label><input type="checkbox" id="streamToggle"> Enable Streaming</label>
            </div>
            <script>
                const chat = document.getElementById('chat');
                const input = document.getElementById('input');
                
                function addMessage(role, text) {
                    const div = document.createElement('div');
                    div.className = `message ${role}`;
                    div.innerHTML = `<strong>${role}:</strong> ${text}`;
                    chat.appendChild(div);
                    chat.scrollTop = chat.scrollHeight;
                }
                
                async function sendMessage() {
                    const message = input.value.trim();
                    if (!message) return;
                    
                    addMessage('user', message);
                    input.value = '';
                    
                    try {
                        const ragEnabled = document.getElementById('ragToggle').checked;
                        const streaming = document.getElementById('streamToggle').checked;
                        
                        if (streaming) {
                            // WebSocket streaming
                            const ws = new WebSocket(`ws://${location.host}/ws/chat`);
                            let response = '';
                            
                            ws.onopen = () => {
                                ws.send(JSON.stringify({
                                    message: message,
                                    rag_enabled: ragEnabled
                                }));
                            };
                            
                            ws.onmessage = (event) => {
                                const data = JSON.parse(event.data);
                                if (data.type === 'token') {
                                    response += data.text;
                                    const lastMsg = chat.lastChild;
                                    if (lastMsg && lastMsg.className.includes('assistant')) {
                                        lastMsg.innerHTML = `<strong>assistant:</strong> ${response}`;
                                    } else {
                                        addMessage('assistant', response);
                                    }
                                    chat.scrollTop = chat.scrollHeight;
                                } else if (data.type === 'done') {
                                    ws.close();
                                } else if (data.type === 'error') {
                                    addMessage('system', `Error: ${data.error}`);
                                    ws.close();
                                }
                            };
                            
                            ws.onerror = (error) => {
                                console.error('WebSocket error:', error);
                                // Fallback to HTTP POST
                                fallbackToHttpPost(message, ragEnabled);
                            };
                        } else {
                            // HTTP POST
                            const response = await fetch('/api/chat', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    message: message,
                                    rag_enabled: ragEnabled
                                })
                            });
                            
                            const data = await response.json();
                            addMessage('assistant', data.response || 'No response');
                        }
                    } catch (error) {
                        console.error('Chat error:', error);
                        addMessage('system', `Error: ${error.message}`);
                    }
                }
                
                async function fallbackToHttpPost(message, ragEnabled) {
                    try {
                        addMessage('system', '[WebSocket failed, falling back to HTTP...]');
                        
                        const response = await fetch('/api/chat', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                message: message,
                                rag_enabled: ragEnabled
                            })
                        });
                        
                        const data = await response.json();
                        addMessage('assistant', data.response || 'No response');
                    } catch (error) {
                        addMessage('system', `Fallback error: ${error.message}`);
                    }
                }
                
                function clearChat() {
                    chat.innerHTML = '';
                }
                
                input.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
            </script>
        </body>
    </html>
    """)


@app.get("/api/health")
async def api_health():
    """Health check endpoint."""
    return JSONResponse({
        "ok": True,
        "status": "running",
        "system": "ConscienceAI Web Chat Server",
        "version": "1.0.0",
        "chat_available": CHAT_AVAILABLE,
        "rag_available": RAG_AVAILABLE and rag_retriever is not None,
        "uptime_seconds": time.time() - chat_performance_metrics['start_time'],
        "total_messages": chat_performance_metrics['total_messages']
    })


@app.post("/api/chat")
async def api_chat(request: Request):
    """Chat endpoint with RAG integration."""
    global chat_model, chat_tokenizer, chat_device, rag_retriever
    
    if not CHAT_AVAILABLE or chat_model is None:
        return JSONResponse({
            "error": "Chat unavailable. Install: pip install transformers torch"
        }, status_code=503)
    
    try:
        data = await request.json()
        message = str(data.get('message', '')).strip()
        session_id = str(data.get('session_id', 'default'))
        rag_enabled = bool(data.get('rag_enabled', True))
        max_new_tokens = min(int(data.get('max_new_tokens', 128)), 512)
        
        if not message:
            return JSONResponse({"error": "Empty message"}, status_code=400)
        
        # Retrieve context with RAG if enabled
        context = ""
        if rag_enabled and RAG_AVAILABLE and rag_retriever is not None:
            try:
                hits = rag_retriever.search(message, top_k=3)
                context = rag_retriever.make_context(hits, max_chars=1200) if hits else ""
            except Exception as e:
                print(f"RAG retrieval error: {e}")
        
        # Build prompt
        prompt = build_prompt(context, message)
        
        # Generate response
        inputs = chat_tokenizer(prompt, return_tensors="pt").to(chat_device)
        outputs = chat_model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=True, temperature=0.7)
        response_text = chat_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract assistant response
        if "[Asistente]" in response_text:
            response = response_text.split("[Asistente]")[-1].strip()
        else:
            response = response_text.strip()
        
        # Save to session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        chat_sessions[session_id].append({
            'timestamp': time.time(),
            'user': message,
            'assistant': response,
            'context': context
        })
        
        chat_performance_metrics['total_messages'] += 1
        
        return JSONResponse({
            "response": response,
            "context": context,
            "sources": []  # For compatibility with frontend
        })
        
    except Exception as e:
        chat_performance_metrics['errors'] += 1
        return JSONResponse({
            "error": f"Chat failed: {str(e)}"
        }, status_code=500)


@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat streaming
    Provides token-by-token response streaming for chat messages
    With fallback mechanism for network compatibility
    """
    await websocket.accept()
    active_chat_connections.append(websocket)
    connection_id = id(websocket)
    chat_connection_metadata[connection_id] = {
        'connected_at': time.time(),
        'messages_sent': 0
    }
    
    try:
        print(f"✅ Chat WebSocket client connected. Total connections: {len(active_chat_connections)}")
        
        # Wait for initial message
        data = await websocket.receive_json()
        
        message = str(data.get('message', '')).strip()
        rag_enabled = bool(data.get('rag_enabled', True))
        max_new_tokens = min(int(data.get('max_new_tokens', 128)), 512)
        
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
        
        # Retrieve context with RAG if enabled
        context = ""
        if rag_enabled and RAG_AVAILABLE and rag_retriever is not None:
            try:
                hits = rag_retriever.search(message, top_k=3)
                context = rag_retriever.make_context(hits, max_chars=1200) if hits else ""
            except Exception as e:
                print(f"RAG retrieval error: {e}")
        
        # Build prompt
        prompt = build_prompt(context, message)
        
        # Generate response with streaming
        inputs = chat_tokenizer(prompt, return_tensors="pt").to(chat_device)
        
        # Generate the full response first (simplified streaming)
        outputs = chat_model.generate(
            **inputs, 
            max_new_tokens=max_new_tokens, 
            do_sample=True, 
            temperature=0.7,
            pad_token_id=chat_tokenizer.eos_token_id
        )
        
        response_text = chat_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract assistant response
        if "[Asistente]" in response_text:
            response = response_text.split("[Asistente]")[-1].strip()
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
        session_id = data.get('session_id', 'websocket_session')
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        chat_sessions[session_id].append({
            'timestamp': time.time(),
            'user': message,
            'assistant': response,
            'context': context
        })
        
        chat_performance_metrics['total_messages'] += 1
        chat_connection_metadata[connection_id]['messages_sent'] += 1
        
        # Send completion message
        await websocket.send_json({"type": "done"})
        
    except WebSocketDisconnect:
        print(f"Chat WebSocket client disconnected. Remaining connections: {len(active_chat_connections) - 1}")
        if websocket in active_chat_connections:
            active_chat_connections.remove(websocket)
        # Clean up connection metadata
        chat_connection_metadata.pop(id(websocket), None)
    except Exception as e:
        print(f"Chat WebSocket error: {e}")
        chat_performance_metrics['errors'] += 1
        if websocket in active_chat_connections:
            active_chat_connections.remove(websocket)
        chat_connection_metadata.pop(id(websocket), None)
        # Log error for analysis
        try:
            await websocket.send_json({"type": "error", "error": str(e)})
        except:
            pass  # Ignore errors when sending error message
    finally:
        try:
            await websocket.close()
        except:
            pass  # Ignore errors when closing


@app.post("/api/upload")
async def api_upload(file: UploadFile = File(...)):
    """Upload and process documents for RAG."""
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
            upload_dir = Path(tempfile.gettempdir()) / "ConscienceAI" / "uploads"
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
    """List uploaded documents."""
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
    """Clear all uploaded documents."""
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


@app.get("/api/transcript")
async def api_transcript(session_id: str = "default"):
    """Get chat transcript for session."""
    return JSONResponse({
        "session_id": session_id,
        "entries": chat_sessions.get(session_id, [])
    })


def main():
    """Run the chat server."""
    print("\n" + "="*60)
    print("Starting ConscienceAI Web Chat Server")
    print("="*60)
    print(f"Server will be available at: http://localhost:5180")
    print(f"WebSocket endpoint: ws://localhost:5180/ws/chat")
    print(f"API Chat: http://localhost:5180/api/chat")
    print(f"API Health: http://localhost:5180/api/health")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=5180,
        log_level="info"
    )


if __name__ == "__main__":
    main()