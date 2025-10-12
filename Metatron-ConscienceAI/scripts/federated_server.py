#!/usr/bin/env python
from __future__ import annotations

import os
import hashlib
from pathlib import Path
import json
import subprocess
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Header, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, Any

# Intentar importar orquestador para métricas opcionales
try:
    from consciousness_engine.orchestrator.harmonic_orchestrator import run_once as orchestrator_run_once
except Exception:
    try:
        from orchestrator.harmonic_orchestrator import run_once as orchestrator_run_once  # type: ignore
    except Exception:
        orchestrator_run_once = None

# Backend de generación configurable
LLM_BACKEND = os.environ.get("LLM_BACKEND", "hf")  # "hf" o "ollama"
LLM_MODEL = os.environ.get("LLM_MODEL", "distilgpt2")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
# Ruta opcional a un adaptador LoRA entrenado (directorio con adapter_config.json y adapter_model.safetensors)
LORA_ADAPTER_PATH = os.environ.get("LORA_ADAPTER_PATH")

BASE_DIR = Path(__file__).resolve().parents[1]
INBOX_DIR = BASE_DIR / "federated" / "inbox"
WORK_DIR = BASE_DIR / "federated" / "work"
OUT_DIR_DEFAULT = BASE_DIR / "models" / "qwen2_5_0_5b_pdf_es_lora_global"
SESSIONS_DIR = BASE_DIR / "sessions"

TOKEN = os.environ.get("FEDERATOR_TOKEN", "change-me")

app = FastAPI(title="Federated LoRA Server", version="0.2.0")

# CORS básico: sólo mismo origen (la .onion o 127.0.0.1). Por defecto, no se abre a otros orígenes.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # si quieres restringir, reemplaza por tu .onion
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# -----------------------------
# Gestión de sesiones en memoria
# -----------------------------
class Session:
    def __init__(self, session_id: str, token: str, ttl_seconds: int = 24 * 3600):
        self.session_id = session_id
        self.token = token
        self.created_at = int(time.time())
        self.last_activity = self.created_at
        self.ttl = ttl_seconds
        self.history: list[Dict[str, str]] = []  # [{role, content}]
        self.last_request_at = 0

    def is_expired(self) -> bool:
        return int(time.time()) - self.created_at > self.ttl


SESSIONS: Dict[str, Session] = {}

def create_session(ttl_seconds: int = 24 * 3600) -> Session:
    sid = secrets.token_urlsafe(18)
    tok = secrets.token_urlsafe(24)
    s = Session(sid, tok, ttl_seconds)
    SESSIONS[sid] = s
    try:
        save_session(s)
    except Exception:
        pass
    return s

def get_session(session_id: str) -> Session | None:
    s = SESSIONS.get(session_id)
    if not s:
        # Intentar cargar desde disco si está disponible
        s = load_session(session_id)
    if s and s.is_expired():
        try:
            del SESSIONS[session_id]
        except Exception:
            pass
        try:
            # Eliminar del disco
            p = SESSIONS_DIR / f"{session_id}.json"
            if p.exists():
                p.unlink(missing_ok=True)
        except Exception:
            pass
        return None
    return s

def cleanup_sessions():
    now = int(time.time())
    expired = [sid for sid, s in SESSIONS.items() if now - s.created_at > s.ttl]
    for sid in expired:
        try:
            del SESSIONS[sid]
        except Exception:
            pass
        try:
            p = SESSIONS_DIR / f"{sid}.json"
            if p.exists():
                p.unlink(missing_ok=True)
        except Exception:
            pass

def save_session(s: Session):
    try:
        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "session_id": s.session_id,
            "token": s.token,
            "created_at": s.created_at,
            "last_activity": s.last_activity,
            "ttl": s.ttl,
            "history": s.history,
            "last_request_at": s.last_request_at,
        }
        (SESSIONS_DIR / f"{s.session_id}.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

def load_session(session_id: str) -> Session | None:
    try:
        p = SESSIONS_DIR / f"{session_id}.json"
        if not p.exists():
            return None
        data = json.loads(p.read_text(encoding="utf-8"))
        token = data.get("token")
        ttl = int(data.get("ttl", 24 * 3600))
        s = Session(session_id, token, ttl)
        s.created_at = int(data.get("created_at", int(time.time())))
        s.last_activity = int(data.get("last_activity", s.created_at))
        s.last_request_at = int(data.get("last_request_at", 0))
        hist = data.get("history") or []
        if isinstance(hist, list):
            s.history = [
                {"role": str(m.get("role", "user")), "content": str(m.get("content", ""))}
                for m in hist
                if isinstance(m, dict)
            ]
        SESSIONS[session_id] = s
        return s
    except Exception:
        return None


# -----------------------------
# Servicio de generación (modelo)
# -----------------------------
class ChatModelService:
    def __init__(self):
        self.backend = LLM_BACKEND
        self.model_name = LLM_MODEL
        self.ollama_host = OLLAMA_HOST
        self.lora_adapter_path = LORA_ADAPTER_PATH
        self.tokenizer = None
        self.model = None
        self.device = "cpu"

    def startup(self):
        if self.backend == "hf":
            try:
                from transformers import AutoTokenizer, AutoModelForCausalLM
                import torch  # type: ignore
                # Si se especificó un adaptador LoRA entrenado, usar el modelo base indicado en su adapter_config
                if self.lora_adapter_path and Path(self.lora_adapter_path).exists():
                    try:
                        import json
                        from peft import PeftModel  # type: ignore
                        cfg_path = Path(self.lora_adapter_path) / "adapter_config.json"
                        base_model_name = None
                        if cfg_path.exists():
                            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
                            base_model_name = cfg.get("base_model_name_or_path")
                        base_model_name = base_model_name or self.model_name
                        self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)
                        base_model = AutoModelForCausalLM.from_pretrained(base_model_name)
                        self.model = PeftModel.from_pretrained(base_model, self.lora_adapter_path)
                        self.device = "cuda" if hasattr(torch, "cuda") and torch.cuda.is_available() else "cpu"
                        try:
                            self.model.to(self.device)
                        except Exception:
                            self.device = "cpu"
                        if getattr(self.tokenizer, "pad_token_id", None) is None and getattr(self.tokenizer, "eos_token_id", None) is not None:
                            self.tokenizer.pad_token = self.tokenizer.eos_token
                        print(f"[INFO] Cargado modelo base '{base_model_name}' con adaptador LoRA en '{self.lora_adapter_path}'.")
                    except Exception as e:
                        print(f"[WARN] Falló carga de LoRA ({e}). Se intentará cargar modelo '{self.model_name}' sin LoRA.")
                        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
                        self.device = "cuda" if hasattr(torch, "cuda") and torch.cuda.is_available() else "cpu"
                        try:
                            self.model.to(self.device)
                        except Exception:
                            self.device = "cpu"
                        if getattr(self.tokenizer, "pad_token_id", None) is None and getattr(self.tokenizer, "eos_token_id", None) is not None:
                            self.tokenizer.pad_token = self.tokenizer.eos_token
                else:
                    # Carga estándar sin LoRA
                    self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                    self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
                    self.device = "cuda" if hasattr(torch, "cuda") and torch.cuda.is_available() else "cpu"
                    try:
                        self.model.to(self.device)
                    except Exception:
                        self.device = "cpu"
                    if getattr(self.tokenizer, "pad_token_id", None) is None and getattr(self.tokenizer, "eos_token_id", None) is not None:
                        self.tokenizer.pad_token = self.tokenizer.eos_token
            except Exception as e:
                # Fallback simple: marcar backend como no disponible
                self.backend = "none"
                print(f"[WARN] No se pudo cargar HF ({e}). Cambiando backend a 'none'.")
        elif self.backend == "ollama":
            # Verificar que Ollama responda
            try:
                import requests  # type: ignore
                r = requests.get(self.ollama_host + "/api/tags", timeout=3)
                if r.status_code != 200:
                    print(f"[WARN] Ollama no respondió ({r.status_code}). Backend deshabilitado.")
                    self.backend = "none"
            except Exception as e:
                print(f"[WARN] Ollama no disponible: {e}")
                self.backend = "none"

    def generate(self, prompt: str, max_new_tokens: int = 128) -> str:
        cleanup_sessions()  # limpieza oportuna
        if self.backend == "hf" and self.tokenizer and self.model:
            import torch  # type: ignore
            inputs = self.tokenizer(prompt, return_tensors="pt")
            try:
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            except Exception:
                pass
            gen = self.model.generate(
                **inputs,
                do_sample=True,
                temperature=0.8,
                top_p=0.9,
                top_k=50,
                repetition_penalty=1.1,
                no_repeat_ngram_size=2,
                max_new_tokens=max_new_tokens,
                pad_token_id=self.tokenizer.pad_token_id,
            )
            try:
                input_len = inputs['input_ids'].shape[-1]
                gen_tokens = gen[0][input_len:]
                return self.tokenizer.decode(gen_tokens, skip_special_tokens=True).strip()
            except Exception:
                return self.tokenizer.decode(gen[0], skip_special_tokens=True).strip()
        elif self.backend == "ollama":
            try:
                import requests  # type: ignore
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 50,
                        "repeat_penalty": 1.1,
                        "num_predict": max_new_tokens,
                    }
                }
                resp = requests.post(self.ollama_host + "/api/generate", json=payload, timeout=120)
                if resp.status_code == 200:
                    data = resp.json()
                    return (data.get("response", "") or "").strip()
                else:
                    return f"[ERROR] Ollama respondió {resp.status_code}: {resp.text}"
            except Exception as e:
                return f"[ERROR] Fallo Ollama: {e}"
        else:
            return "[ERROR] Backend de generación no disponible."


CHAT = ChatModelService()

@app.on_event("startup")
def _startup_event():
    CHAT.startup()


def ensure_dirs():
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
def health():
    ensure_dirs()
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index():
    ensure_dirs()
    return """
    <!doctype html>
    <html lang=\"es\">
      <head>
        <meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <title>Chat .onion · Servidor Federado LoRA</title>
        <style>
          :root{color-scheme: light dark}
          body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif; margin: 1.5rem; line-height: 1.5; }
          header { margin-bottom: 1rem; }
          code { background: #ececec; padding: 2px 4px; border-radius: 4px; }
          .links a { display: inline-block; margin-right: 1rem; }
          .note { color: #555; font-size: 0.95rem; }
          .chat { max-width: 840px; border: 1px solid #ddd; border-radius: 8px; padding: 12px; }
          .msg { margin: 8px 0; }
          .user { font-weight: 600; }
          .assistant { }
          textarea { width: 100%; min-height: 80px; }
          button { padding: 6px 10px; }
          .small { font-size: 0.9rem; }
        </style>
      </head>
      <body>
        <header>
          <h1>Chat sobre Tor (.onion)</h1>
          <p class=\"note\">Usa el chat para interactuar con el modelo. La sesión se crea automáticamente y se conserva en este navegador durante 24h (cookie HttpOnly).</p>
          <p class=\"small\">Docs: <a href=\"/docs\">/docs</a> · Salud: <a href=\"/health\">/health</a></p>
        </header>
        <section class=\"chat\">
          <div id=\"log\"></div>
          <textarea id=\"input\" placeholder=\"Escribe tu mensaje...\"></textarea>
          <div style=\"margin-top:8px\">
            <button id=\"send\">Enviar</button>
            <span id=\"status\" class=\"small\"></span>
          </div>
        </section>
        <script>
        const statusEl = document.getElementById('status');
        const logEl = document.getElementById('log');
        const inputEl = document.getElementById('input');
        let sessionToken = null;

        function append(role, text){
          const div = document.createElement('div');
          div.className = 'msg ' + (role === 'user' ? 'user' : 'assistant');
          div.textContent = (role === 'user' ? 'Tú> ' : 'Asistente> ') + text;
          logEl.appendChild(div);
        }

        async function ensureSession(){
          if (sessionToken) return;
          statusEl.textContent = 'Creando sesión...';
          const resp = await fetch('/session/new', { method: 'POST' });
          if (!resp.ok){ statusEl.textContent = 'Error creando sesión'; return; }
          const data = await resp.json();
          sessionToken = data.token;
          statusEl.textContent = 'Sesión lista';
        }

        document.getElementById('send').addEventListener('click', async () => {
          const msg = inputEl.value.trim();
          if (!msg) return;
          await ensureSession();
          append('user', msg);
          inputEl.value = '';
          statusEl.textContent = 'Generando...';
          const resp = await fetch('/chat', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-Session-Token': sessionToken,
            },
            body: JSON.stringify({ message: msg })
          });
          if (!resp.ok){
            statusEl.textContent = 'Error ' + resp.status;
            const txt = await resp.text();
            append('assistant', 'Error: ' + txt);
            return;
          }
          const data = await resp.json();
          append('assistant', data.response);
          statusEl.textContent = '';
        });
        </script>
      </body>
    </html>
    """


def check_token(x_auth_token: Optional[str]):
    if not x_auth_token or x_auth_token != TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# -----------------------------
# Endpoints de sesión y chat
# -----------------------------

@app.post("/session/new")
def new_session(ttl_seconds: int = 24 * 3600):
    s = create_session(ttl_seconds)
    # Cookie HttpOnly con el session_id; el token se devuelve en el cuerpo y debe enviarse por header
    resp = JSONResponse({
        "session_id": s.session_id,
        "token": s.token,
        "expires_in": ttl_seconds,
    })
    # Nota: en .onion no hay HTTPS, pero Tor cifra fin-a-fin; mantenemos SameSite=Strict
    resp.set_cookie(
        key="SESSION_ID",
        value=s.session_id,
        httponly=True,
        samesite="strict",
        secure=False,
        max_age=ttl_seconds,
    )
    try:
        save_session(s)
    except Exception:
        pass
    return resp


def _get_session_from_request(request: Request, x_session_token: Optional[str]) -> Session:
    sid = request.cookies.get("SESSION_ID")
    if not sid:
        raise HTTPException(status_code=401, detail="Sesión no encontrada (cookie)")
    s = get_session(sid)
    if not s:
        raise HTTPException(status_code=401, detail="Sesión expirada o inválida")
    if not x_session_token or x_session_token != s.token:
        raise HTTPException(status_code=401, detail="Token de sesión inválido")
    # Rate limit básico: mínimo 2s entre peticiones por sesión
    now = int(time.time())
    if now - s.last_request_at < 2:
        raise HTTPException(status_code=429, detail="Demasiadas peticiones (espera 2s)")
    s.last_request_at = now
    s.last_activity = now
    try:
        save_session(s)
    except Exception:
        pass
    return s


@app.get("/session/me")
def session_me(request: Request, x_session_token: Optional[str] = Header(None)):
    s = _get_session_from_request(request, x_session_token)
    resp = {
        "session_id": s.session_id,
        "created_at": s.created_at,
        "last_activity": s.last_activity,
        "history_len": len(s.history),
        "ttl": s.ttl,
    }
    try:
        save_session(s)
    except Exception:
        pass
    return resp


@app.post("/chat")
def chat(request: Request, payload: Dict[str, Any], x_session_token: Optional[str] = Header(None)):
    s = _get_session_from_request(request, x_session_token)
    user_msg = (payload or {}).get("message")
    if not isinstance(user_msg, str) or not user_msg.strip():
        raise HTTPException(status_code=400, detail="Mensaje vacío")
    s.history.append({"role": "user", "content": user_msg})

    # Métricas opcionales del orquestador para ajustar parámetros (simple demo)
    prefix = ""
    if orchestrator_run_once is not None:
        try:
            result = orchestrator_run_once(noise=0.3, phase=float(len(s.history)) * 0.2)
            if result is not None:
                # Añadir una guía liviana basada en coherencia/valencia
                coh = float(result.get("core_out", {}).get("coherence", 0.0))
                val = float(result.get("emotion_out", {}).get("valence", 0.0))
                prefix = f"(Contexto estable: {coh:.2f}; tono positivo: {val:.2f})\n"
        except Exception:
            pass

    # Construir contexto simple
    ctx_msgs = s.history[-20:]
    context = "\n".join([("Usuario: " + m["content"]) if m["role"]=="user" else ("Asistente: " + m["content"]) for m in ctx_msgs])
    prompt = (prefix + context + "\nAsistente: ")
    output = CHAT.generate(prompt, max_new_tokens=192)
    s.history.append({"role": "assistant", "content": output})
    try:
        save_session(s)
    except Exception:
        pass
    return {"response": output}


@app.post("/upload")
async def upload_delta(
    file: UploadFile = File(...),
    x_auth_token: Optional[str] = Header(None),
    x_node_id: Optional[str] = Header(None),
):
    check_token(x_auth_token)
    ensure_dirs()
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos .zip")
    tmp_path = INBOX_DIR / file.filename
    contents = await file.read()
    tmp_path.write_bytes(contents)
    digest = sha256_file(tmp_path)
    final_name = f"{Path(file.filename).stem}_{digest[:8]}.zip"
    final_path = INBOX_DIR / final_name
    # Si el archivo destino ya existe (duplicado), genera un nombre único incremental
    if final_path.exists():
        base_stem = Path(file.filename).stem
        idx = 1
        while True:
            alt_name = f"{base_stem}_{digest[:8]}_{idx}.zip"
            alt_path = INBOX_DIR / alt_name
            if not alt_path.exists():
                final_name = alt_name
                final_path = alt_path
                break
            idx += 1
    # Mover/renombrar al nombre final
    try:
        tmp_path.rename(final_path)
    except FileExistsError:
        # Como salvaguarda adicional ante condiciones de carrera, elegir un nombre único y reintentar
        base_stem = Path(file.filename).stem
        idx = 1
        while True:
            alt_name = f"{base_stem}_{digest[:8]}_{idx}.zip"
            alt_path = INBOX_DIR / alt_name
            if not alt_path.exists():
                final_name = alt_name
                final_path = alt_path
                break
            idx += 1
        tmp_path.rename(final_path)
    manifest = {
        "filename": final_name,
        "sha256": digest,
        "size": final_path.stat().st_size,
        "node_id": x_node_id or "unknown",
    }
    (INBOX_DIR / f"{final_name}.json").write_text(JSONResponse(content=manifest).body.decode(), encoding="utf-8")
    return manifest


@app.get("/list")
def list_inbox(x_auth_token: Optional[str] = Header(None)):
    check_token(x_auth_token)
    ensure_dirs()
    items = []
    for p in INBOX_DIR.glob("*.zip"):
        items.append({
            "filename": p.name,
            "size": p.stat().st_size,
            "mtime": p.stat().st_mtime,
        })
    return {"count": len(items), "items": items}


@app.post("/aggregate")
def aggregate(x_auth_token: Optional[str] = Header(None), min_adapters: int = 2, out_dir: Optional[str] = None):
    check_token(x_auth_token)
    ensure_dirs()
    out = Path(out_dir) if out_dir else OUT_DIR_DEFAULT
    cmd = [
        "python", str(BASE_DIR / "scripts" / "federated_collect_and_merge.py"),
        "--inbox-dir", str(INBOX_DIR),
        "--work-dir", str(WORK_DIR),
        "--out", str(out),
        "--min-adapters", str(min_adapters),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "returncode": r.returncode,
        "stdout": r.stdout,
        "stderr": r.stderr,
        "out": str(out),
    }


@app.post("/aggregate/weighted")
def aggregate_weighted(
    x_auth_token: Optional[str] = Header(None),
    metric_name: str = "accuracy",
    min_adapters: int = 2,
    out_dir: Optional[str] = None,
):
    check_token(x_auth_token)
    ensure_dirs()
    out = Path(out_dir) if out_dir else OUT_DIR_DEFAULT
    cmd = [
        "python", str(BASE_DIR / "scripts" / "federated_collect_and_merge.py"),
        "--inbox-dir", str(INBOX_DIR),
        "--work-dir", str(WORK_DIR),
        "--out", str(out),
        "--min-adapters", str(min_adapters),
        "--weighted-metric", str(metric_name),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "returncode": r.returncode,
        "stdout": r.stdout,
        "stderr": r.stderr,
        "out": str(out),
        "metric": metric_name,
    }


def _find_latest_global_dir(base: Path) -> Optional[Path]:
    if not base.exists():
        return None
    candidates = [p for p in base.iterdir() if p.is_dir() and p.name.startswith("v")]
    if not candidates:
        return base if (base / "adapter_model.safetensors").exists() else None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]


@app.get("/download/global")
def download_global(x_auth_token: Optional[str] = Header(None), out_dir: Optional[str] = None, file_name: str = "adapter_model.safetensors"):
    check_token(x_auth_token)
    ensure_dirs()
    base = Path(out_dir) if out_dir else OUT_DIR_DEFAULT
    latest = _find_latest_global_dir(base)
    if not latest:
        raise HTTPException(status_code=404, detail="No hay adapter global disponible")
    target = latest / file_name
    if not target.exists():
        raise HTTPException(status_code=404, detail=f"Archivo {file_name} no encontrado en {latest}")
    return FileResponse(str(target), filename=target.name)