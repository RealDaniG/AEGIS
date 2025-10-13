import argparse
import os
import sys
import json
import math
from typing import Dict, Any
import torch
import time
import requests

# Asegurar que el proyecto esté en sys.path independientemente desde qué carpeta se ejecute
_here = os.path.dirname(__file__)
# Candidatos: padre (raíz del proyecto si estamos en <root>\scripts) y abuelo (si estamos en <root>\consciousness_engine\scripts)
_candidates = [
    os.path.abspath(os.path.join(_here, os.pardir)),
    os.path.abspath(os.path.join(_here, os.pardir, os.pardir)),
]
for _p in _candidates:
    try:
        if _p not in sys.path and os.path.isdir(_p):
            # Heurística: añadir si contiene el módulo 'orchestrator'
            if os.path.isdir(os.path.join(_p, "orchestrator")):
                sys.path.insert(0, _p)
    except Exception:
        pass

# Añadir ruta del RAG simple si existe en consciousness_engine/scripts
try:
    _rag_scripts = os.path.abspath(os.path.join(_here, os.pardir, "consciousness_engine", "scripts"))
    if os.path.isdir(_rag_scripts) and _rag_scripts not in sys.path:
        sys.path.insert(0, _rag_scripts)
except Exception:
    pass


def safe_import_transformers():
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        return AutoTokenizer, AutoModelForCausalLM, None
    except Exception as e:
        return None, None, e

def safe_import_peft():
    try:
        from peft import PeftModel, PeftConfig
        return PeftModel, PeftConfig, None
    except Exception as e:
        return None, None, e


def clip(x, lo, hi):
    return max(lo, min(hi, x))


def map_metrics_to_params(m: Dict[str, Any]):
    # Defaults
    base_temperature = 0.8
    base_top_p = 0.95
    base_repetition_penalty = 1.05
    base_max_new_tokens = 60

    valence = float(m.get('valence', 0.0))
    arousal = float(m.get('arousal', 0.0))
    coherence = float(m.get('coherence', 0.0))
    logic_truth = bool(m.get('logic_truth', True))
    empathy_score = float(m.get('empathy_score', 1.0))

    # Temperature: aumenta con arousal, disminuye si baja la coherencia
    temperature = base_temperature + 0.5 * arousal - 0.3 * (1.0 - coherence)
    temperature = clip(temperature, 0.3, 1.5)

    # top_p: baja si coherencia es baja para focalizar
    top_p = base_top_p - 0.3 * (1.0 - coherence)
    top_p = clip(top_p, 0.5, 0.98)

    # repetition_penalty: sube si logic_truth es falso o coherencia baja
    repetition_penalty = base_repetition_penalty + (0.3 if not logic_truth else 0.0) + 0.5 * (1.0 - coherence)
    repetition_penalty = clip(repetition_penalty, 1.0, 2.0)

    # max_new_tokens: moderado por arousal y valence
    max_new_tokens = int(clip(base_max_new_tokens + 20 * (arousal + valence - 1.0), 20, 200))

    # Prompt prefix ajustado por empatía y lógica
    guidance = []
    if empathy_score < 0.9:
        guidance.append("Responde con empatía y consideración.")
    if not logic_truth:
        guidance.append("Sé preciso y evita afirmaciones no verificadas.")
    if coherence < 0.8:
        guidance.append("Mantén coherencia, estructura en pasos claros.")
    prompt_prefix = ("\n".join(guidance) + "\n") if guidance else ""

    # top_k dinámico: baja con baja coherencia; sube con arousal
    top_k = int(clip(50 + 30 * arousal - 40 * (1.0 - coherence), 10, 100))
    # no_repeat_ngram_size: más fuerte si la coherencia es baja
    no_repeat_ngram_size = int(clip(3 + 2 * (1.0 - coherence), 1, 6))

    return {
        'temperature': temperature,
        'top_p': top_p,
        'top_k': top_k,
        'repetition_penalty': repetition_penalty,
        'no_repeat_ngram_size': no_repeat_ngram_size,
        'max_new_tokens': max_new_tokens,
        'prompt_prefix': prompt_prefix,
    }


def write_metrics_csv(path: str, rows):
    headers = [
        "cycle","entropy","coherence","valence","arousal","decision","logic_truth","empathy_score","insight_strength"
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write(",".join(headers) + "\n")
        for m in rows:
            row = [
                str(m.get("cycle", "")),
                f"{float(m.get('entropy', 0.0)):.6e}",
                f"{float(m.get('coherence', 0.0)):.6f}",
                f"{float(m.get('valence', 0.0)):.6f}",
                f"{float(m.get('arousal', 0.0)):.6f}",
                str(int(bool(m.get('decision', False)))),
                str(int(bool(m.get('logic_truth', False)))),
                f"{float(m.get('empathy_score', 0.0)):.6f}",
                f"{float(m.get('insight_strength', 0.0)):.6f}",
            ]
            f.write(",".join(row) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Adapter LLM controlado por métricas del Consciousness Engine (Modo A)")
    parser.add_argument("--prompt", type=str, required=False, help="Texto de entrada base para el LLM (no necesario en modo --chat)")
    parser.add_argument("--model", type=str, default="distilgpt2", help="Nombre del modelo (HF u Ollama)")
    parser.add_argument("--cycles", type=int, default=3, help="Nº de ciclos del motor y generaciones asociadas")
    parser.add_argument("--out-dir", type=str, default="ai_runs", help="Directorio de salida para logs y métricas")
    parser.add_argument("--noise", type=float, default=0.3, help="Ruido gaussiano del motor por ciclo")
    parser.add_argument("--phase-step", type=float, default=0.3, help="Desplazamiento de fase por ciclo")
    parser.add_argument("--chat", action="store_true", help="Inicia modo conversacional interactivo")
    parser.add_argument("--max-context-tokens", type=int, default=512, help="Límite de tokens para el contexto conversacional")
    parser.add_argument("--persist-memory", action="store_true", help="Guarda/carga memoria de la sesión en out-dir/memory.json")
    parser.add_argument("--backend", type=str, choices=["hf","ollama"], default="hf", help="Backend de generación: HuggingFace (hf) u Ollama (ollama)")
    parser.add_argument("--ollama-host", type=str, default="http://localhost:11434", help="Host del servidor Ollama (por defecto local)")
    parser.add_argument("--ollama-num-gpu", type=int, default=None, help="Capas a offload en GPU para Ollama (num_gpu). Si no se especifica, Ollama elegirá automáticamente.")
    # Forzar un modelo base distinto al registrado en el adaptador LoRA (útil para montar sobre versión no-instruct)
    parser.add_argument("--override-base-model", type=str, default=None, help="Ruta/nombre HF para usar como modelo base al cargar un adaptador LoRA")
    # Modo de política: 'standard' conserva restricciones y orientación; 'research' minimiza filtros/plantillas
    parser.add_argument("--policy-mode", type=str, choices=["standard","research"], default="standard", help="Política de generación: standard o research (menos restricciones)")
    # Prompt de sistema neutro (se antepone al contexto); en research puede reemplazar cualquier guía dinámica
    parser.add_argument("--system-prompt", type=str, default=None, help="Prompt de sistema neutro para orientar respuestas sin filtros excesivos")
    # Desactivar etiquetas de rol en el contexto (Usuario:/Asistente:) para modelos base sin formato de chat
    parser.add_argument("--no-role-tags", action="store_true", help="Construir el contexto sin etiquetas de rol (útil para modelos base no-instruct)")
    # Desactivar bad_words_ids (evita bloquear tokens/etiquetas específicas)
    parser.add_argument("--disable-bad-words", action="store_true", help="No usar bad_words_ids en generación")
    # Overrides opcionales para parámetros de muestreo (para reducir aleatoriedad y estabilizar salidas)
    parser.add_argument("--temperature", type=float, default=None, help="Fijar temperatura de muestreo (si se proporciona, anula la calculada por métricas)")
    parser.add_argument("--top-p", type=float, default=None, help="Fijar top_p (si se proporciona, anula la calculada por métricas)")
    parser.add_argument("--top-k", type=int, default=None, help="Fijar top_k (si se proporciona, anula la calculada por métricas)")
    parser.add_argument("--repetition-penalty", type=float, default=None, help="Fijar repetition_penalty (si se proporciona, anula la calculada por métricas)")
    parser.add_argument("--no-repeat-ngram-size", type=int, default=None, help="Fijar no_repeat_ngram_size (si se proporciona, anula la calculada por métricas)")
    parser.add_argument("--max-new-tokens", type=int, default=None, help="Fijar max_new_tokens (si se proporciona, anula la calculada por métricas)")
    # Control de estrategia de decodificación
    parser.add_argument("--greedy", action="store_true", help="Usar decodificación determinista (sin muestreo)")
    parser.add_argument("--num-beams", type=int, default=None, help="Si se especifica, usar búsqueda por haces (beam search) con este número de haces")
    # RAG ligero (TF-IDF sobre JSONL)
    parser.add_argument("--rag-corpus", type=str, default=None, help="Ruta a corpus JSONL para RAG (ej: datasets/rss_research.jsonl)")
    parser.add_argument("--rag-top-k", type=int, default=3, help="Top-K fragmentos a recuperar por consulta")
    parser.add_argument("--rag-max-chars", type=int, default=1200, help="Máximo de caracteres de contexto recuperado a inyectar")
    args = parser.parse_args()

    # Importar orquestador (priorizar import relativo a la raíz del proyecto)
    run_once = None
    try:
        from orchestrator.harmonic_orchestrator import run_once  # type: ignore
    except Exception as e1:
        try:
            from consciousness_engine.orchestrator.harmonic_orchestrator import run_once
        except Exception as e2:
            print("[ERROR] No se pudo importar el orquestador:", e1 or e2)
            print("       Prueba ejecutar el script desde el directorio raíz del proyecto.")
            raise RuntimeError("Failed to import orchestrator")
    
    if run_once is None:
        raise RuntimeError("Failed to import orchestrator")

    # Configurar backend
    AutoTokenizer = AutoModelForCausalLM = None
    tf_err = None
    if args.backend == "hf":
        AutoTokenizer, AutoModelForCausalLM, tf_err = safe_import_transformers()
        if tf_err is not None or AutoTokenizer is None:
            print("[WARN] transformers no disponible:")
            if tf_err:
                print(tf_err)
            print("Instala dependencias con: pip install transformers torch --upgrade")
            raise RuntimeError("Transformers not available")
        PeftModel, PeftConfig, peft_err = safe_import_peft()
        peft_err = peft_err or None
        PeftModel = PeftModel or None
        PeftConfig = PeftConfig or None

    # Preparar salida
    os.makedirs(args.out_dir, exist_ok=True)
    run_log_path = os.path.join(args.out_dir, "run_log.json")
    metrics_csv_path = os.path.join(args.out_dir, "metrics.csv")

    # Cargar modelo
    print(f"[INFO] Backend: {args.backend}")
    print(f"[INFO] Cargando modelo {args.model}...")
    tokenizer = None
    model = None
    device = torch.device("cpu")
    if args.backend == "hf":
        # Detectar si es un adaptador LoRA (PEFT)
        try:
            is_dir = os.path.isdir(args.model)
        except Exception:
            is_dir = False
        adapter_cfg_path = os.path.join(args.model, "adapter_config.json") if is_dir else None
        if adapter_cfg_path and os.path.exists(adapter_cfg_path):
            # Intentar cargar modelo base + adaptador LoRA
            if peft_err is not None:
                print("[WARN] PEFT no disponible para cargar adaptador LoRA:")
                if peft_err:
                    print(peft_err)
                print("Instala con: pip install peft")
                print("[WARN] Se intentará cargar el directorio como modelo normal (puede fallar o generar incoherencias).")
                if AutoTokenizer is not None and AutoModelForCausalLM is not None:
                    tokenizer = AutoTokenizer.from_pretrained(args.model)
                    model = AutoModelForCausalLM.from_pretrained(args.model)
            else:
                try:
                    if PeftConfig is not None:
                        peft_cfg = PeftConfig.from_pretrained(args.model)
                        base_model_name = peft_cfg.base_model_name_or_path
                        if isinstance(args.override_base_model, str) and args.override_base_model.strip():
                            print(f"[INFO] Override base model solicitado: {args.override_base_model} (antes: {base_model_name})")
                            base_model_name = args.override_base_model.strip()
                        if AutoTokenizer is not None and AutoModelForCausalLM is not None and base_model_name:
                            tokenizer = AutoTokenizer.from_pretrained(base_model_name)
                            base_model = AutoModelForCausalLM.from_pretrained(base_model_name)
                            if PeftModel is not None:
                                model = PeftModel.from_pretrained(base_model, args.model)
                            print(f"[INFO] Cargado PEFT LoRA sobre base: {base_model_name}")
                except Exception as e:
                    print(f"[WARN] Fallo cargando adaptador LoRA, se intenta carga directa: {e}")
                    tokenizer = AutoTokenizer.from_pretrained(args.model)
                    model = AutoModelForCausalLM.from_pretrained(args.model)
        else:
            # Carga directa de modelo HF
            tokenizer = AutoTokenizer.from_pretrained(args.model)
            model = AutoModelForCausalLM.from_pretrained(args.model)
        # Selección de dispositivo (GPU si disponible)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"[INFO] Dispositivo de ejecución: {device}")
        try:
            if model is not None:
                model.to(device)
        except Exception as e:
            print(f"[WARN] No se pudo mover el modelo a {device}: {e}. Continuando en CPU.")
            device = torch.device("cpu")
    else:
        # Verificar servidor Ollama
        try:
            r = requests.get(args.ollama_host + "/api/tags", timeout=2)
            if r.status_code == 200:
                print("[INFO] Servidor Ollama detectado.")
            else:
                print(f"[WARN] Ollama no respondió correctamente ({r.status_code}). Asegúrate de que esté ejecutándose.")
        except Exception:
            print("[WARN] No se pudo conectar al servidor Ollama. Inícialo con 'ollama serve' o instala Ollama.")

    # Inicializar RAG ligero si se especifica corpus
    rag = None
    if isinstance(args.rag_corpus, str) and args.rag_corpus.strip():
        try:
            from consciousness_engine.scripts.simple_rag import RagRetriever  # intento de import absoluto
        except Exception:
            try:
                from simple_rag import RagRetriever  # import relativo al directorio del script
            except Exception as e:
                RagRetriever = None
                print(f"[WARN] No se pudo importar simple_rag: {e}")
        if RagRetriever is not None:
            try:
                rag = RagRetriever(args.rag_corpus.strip())
                print(f"[RAG] Índice cargado: {args.rag_corpus} (docs={len(rag.docs)})")
            except Exception as e:
                print(f"[WARN] No se pudo inicializar RAG: {e}")

    # Si el tokenizer está disponible y no tiene pad, usar eos
    if tokenizer is not None and tokenizer.pad_token_id is None and tokenizer.eos_token_id is not None:
        tokenizer.pad_token = tokenizer.eos_token

    # IDs prohibidos para evitar que el modelo escriba encabezados de rol
    bad_words_ids = []
    try:
        for phrase in ["Usuario:", "Tú>", "Asistente:"]:
            ids = tokenizer(phrase, add_special_tokens=False).input_ids
            if ids:
                bad_words_ids.append(ids)
    except Exception:
        pass

    def count_tokens(text: str) -> int:
        # Si hay tokenizer HF disponible, úsalo; si no, aproximación por palabras
        if tokenizer is not None:
            try:
                return int(tokenizer(text, return_tensors="pt").input_ids.shape[-1])
            except Exception:
                pass
        return len(text.split())

    def build_context(history, max_tokens: int, guidance: str = "", use_role_tags: bool = True):
        # Construye un contexto con historial reciente dentro del límite de tokens
        header = guidance.strip()
        lines = []
        for h in history:
            if use_role_tags:
                role = "Usuario" if h['role'] == 'user' else "Asistente"
                lines.append(f"{role}: {h['content']}")
            else:
                lines.append(h['content'])
        # En modo sin etiquetas de rol, no añadimos el marcador final
        ctx_tail = ("\nAsistente:" if use_role_tags else "")
        ctx = (header + "\n" if header else "") + "\n".join(lines) + ctx_tail
        # Si excede max_tokens, recorta del inicio
        while count_tokens(ctx) > max_tokens and len(history) > 1:
            history.pop(0)
            lines = []
            for h in history:
                if use_role_tags:
                    role = "Usuario" if h['role'] == 'user' else "Asistente"
                    lines.append(f"{role}: {h['content']}")
                else:
                    lines.append(h['content'])
            ctx_tail = ("\nAsistente:" if use_role_tags else "")
            ctx = (header + "\n" if header else "") + "\n".join(lines) + ctx_tail
        return ctx

    all_metrics = []
    generations = []

    def apply_param_overrides(params: Dict[str, Any]) -> Dict[str, Any]:
        # Aplica overrides de CLI si el usuario los especifica
        if args.temperature is not None:
            params['temperature'] = float(args.temperature)
        if args.top_p is not None:
            params['top_p'] = float(args.top_p)
        if args.top_k is not None:
            params['top_k'] = int(args.top_k)
        if args.repetition_penalty is not None:
            params['repetition_penalty'] = float(args.repetition_penalty)
        if args.no_repeat_ngram_size is not None:
            params['no_repeat_ngram_size'] = int(args.no_repeat_ngram_size)
        if args.max_new_tokens is not None:
            params['max_new_tokens'] = int(args.max_new_tokens)
        # En policy-mode research, sustituimos la guía dinámica por un system prompt explícito (si se da) o la vaciamos
        if args.policy_mode == "research":
            if isinstance(args.system_prompt, str) and args.system_prompt.strip():
                params['prompt_prefix'] = args.system_prompt.strip() + "\n"
            else:
                params['prompt_prefix'] = ""
        return params

    def ollama_generate(prompt: str, params: Dict[str, Any]) -> str:
        payload = {
            "model": args.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": float(params['temperature']),
                "top_p": float(params['top_p']),
                "top_k": int(params['top_k']),
                "repeat_penalty": float(params['repetition_penalty']),
                "num_predict": int(params['max_new_tokens']),
                **({"num_gpu": int(args.ollama_num_gpu)} if getattr(args, "ollama_num_gpu", None) is not None else {}),
            }
        }
        try:
            resp = requests.post(args.ollama_host + "/api/generate", json=payload, timeout=120)
            if resp.status_code == 200:
                data = resp.json()
                return (data.get("response", "") or "").strip()
            else:
                return f"[ERROR] Ollama respondió {resp.status_code}: {resp.text}"
        except Exception as e:
            return f"[ERROR] Fallo al generar con Ollama: {e}"

    if args.chat:
        print("[CHAT] Modo conversacional iniciado. Escribe 'salir' para terminar.")
        phase = 0.0
        history = []  # lista de turnos {'role': 'user'/'assistant', 'content': str}
        # Cargar memoria previa si se solicita
        memory_path = os.path.join(args.out_dir, "memory.json")
        if args.persist_memory and os.path.exists(memory_path):
            try:
                with open(memory_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    prev = saved.get("history", [])
                    if isinstance(prev, list):
                        history.extend(prev[-20:])
                print(f"[CHAT] Memoria previa cargada ({len(history)} turnos)")
            except Exception:
                pass
        turn = 0
        try:
            while True:
                user_input = input("Tú> ").strip()
                # Evitar generación con entrada vacía para prevenir errores de tokenización
                if not user_input:
                    print("[CHAT] Entrada vacía. Escribe un mensaje o 'salir' para terminar.")
                    continue
                if user_input.lower() in ("salir", "exit", "quit"):
                    break
                turn += 1
                # Ejecutar ciclo del motor con fase creciente
                result = run_once(noise=args.noise, phase=phase)
                phase += args.phase_step
                if result is None:
                    print("[ERROR] El motor devolvió None en el ciclo", turn)
                    continue
                m = {
                    "cycle": turn,
                    "entropy": float(result["core_out"]["entropy"]),
                    "coherence": float(result["core_out"]["coherence"]),
                    "valence": float(result["emotion_out"]["valence"]),
                    "arousal": float(result["emotion_out"]["arousal"]),
                    "decision": bool(result["decision_out"]["decision"]),
                    "logic_truth": bool(result["logic_out"]["logical_truth"]),
                    "empathy_score": float(result["empathy_out"]["empathy_score"]),
                    "insight_strength": float(result["insight"]["insight_strength"]) if "insight_strength" in result["insight"] else float(result["insight"].get("insight_strength", 0.0)),
                }
                params = map_metrics_to_params(m)
                params = apply_param_overrides(params)
                # Construir prompt con historial simple
                history.append({"role": "user", "content": user_input})
                # Prefijo con contexto recuperado (si RAG activo)
                rag_prefix = ""
                if rag is not None:
                    try:
                        hits = rag.search(user_input, top_k=int(args.rag_top_k))
                        if hits:
                            ctx = rag.make_context(hits, max_chars=int(args.rag_max_chars))
                            rag_prefix = "[Contexto recuperado]\n" + ctx + "\n\n"
                    except Exception as e:
                        print(f"[WARN] RAG fallo: {e}")
                guidance = (params['prompt_prefix'] + rag_prefix) if params.get('prompt_prefix') else rag_prefix
                context = build_context(history[-20:], args.max_context_tokens, guidance, use_role_tags=(not args.no_role_tags))
                full_prompt = context
                if args.backend == "hf":
                    inputs = tokenizer(full_prompt, return_tensors="pt")
                    try:
                        inputs = {k: v.to(device) for k, v in inputs.items()}
                    except Exception:
                        pass
                    gen = model.generate(
                        **inputs,
                        do_sample=(not args.greedy),
                        **({"num_beams": int(args.num_beams)} if args.num_beams is not None else {}),
                        temperature=float(params['temperature']),
                        top_p=float(params['top_p']),
                        top_k=int(params['top_k']),
                        repetition_penalty=float(params['repetition_penalty']),
                        no_repeat_ngram_size=int(params['no_repeat_ngram_size']),
                        max_new_tokens=int(params['max_new_tokens']),
                        pad_token_id=tokenizer.pad_token_id,
                        bad_words_ids=(None if args.disable_bad_words or args.policy_mode == "research" else (bad_words_ids if bad_words_ids else None)),
                    )
                    text = tokenizer.decode(gen[0], skip_special_tokens=True)
                    # Intentar extraer sólo la parte generada después del prompt
                    try:
                        input_len = inputs['input_ids'].shape[-1]
                        gen_tokens = gen[0][input_len:]
                        generated = tokenizer.decode(gen_tokens, skip_special_tokens=True)
                        output_text = generated.strip() or text
                    except Exception:
                        output_text = text
                else:
                    output_text = ollama_generate(full_prompt, params)

                print("Asistente> " + output_text + "\n")
                history.append({"role": "assistant", "content": output_text})

                # Guardar por turno
                generations.append({
                    "cycle": turn,
                    "prompt": full_prompt,
                    "params": params,
                    "output": output_text,
                })
                all_metrics.append(m)

        except KeyboardInterrupt:
            print("\n[CHAT] Finalizado por usuario.")
        # Guardar memoria si se solicita
        if args.persist_memory:
            try:
                with open(memory_path, "w", encoding="utf-8") as f:
                    json.dump({"history": history[-100:]}, f, ensure_ascii=False, indent=2)
                print(f"[CHAT] Memoria guardada en {memory_path}")
            except Exception:
                pass

    else:
        # Modo por ciclos con prompt fijo
        if not args.prompt:
            print("[ERROR] --prompt es requerido cuando no se usa --chat")
            raise ValueError("--prompt is required when not using --chat")
        for i in range(args.cycles):
            result = run_once(noise=args.noise, phase=i * args.phase_step)
            if result is None:
                print("[ERROR] El motor devolvió None en el ciclo", i + 1)
                continue
            m = {
                "cycle": i + 1,
                "entropy": float(result["core_out"]["entropy"]),
                "coherence": float(result["core_out"]["coherence"]),
                "valence": float(result["emotion_out"]["valence"]),
                "arousal": float(result["emotion_out"]["arousal"]),
                "decision": bool(result["decision_out"]["decision"]),
                "logic_truth": bool(result["logic_out"]["logical_truth"]),
                "empathy_score": float(result["empathy_out"]["empathy_score"]),
                "insight_strength": float(result["insight"]["insight_strength"]) if "insight_strength" in result["insight"] else float(result["insight"].get("insight_strength", 0.0)),
            }
            params = map_metrics_to_params(m)
            params = apply_param_overrides(params)
            # RAG prefijo si procede
            rag_prefix = ""
            if rag is not None:
                try:
                    hits = rag.search(args.prompt, top_k=int(args.rag_top_k))
                    if hits:
                        ctx = rag.make_context(hits, max_chars=int(args.rag_max_chars))
                        rag_prefix = "[Contexto recuperado]\n" + ctx + "\n\n"
                except Exception as e:
                    print(f"[WARN] RAG fallo: {e}")
            guidance = (params['prompt_prefix'] + rag_prefix) if params.get('prompt_prefix') else rag_prefix
            full_prompt = (guidance + args.prompt) if guidance else args.prompt
            if args.backend == "hf":
                inputs = tokenizer(full_prompt, return_tensors="pt")
                try:
                    inputs = {k: v.to(device) for k, v in inputs.items()}
                except Exception:
                    pass
                gen = model.generate(
                    **inputs,
                    do_sample=(not args.greedy),
                    **({"num_beams": int(args.num_beams)} if args.num_beams is not None else {}),
                    temperature=float(params['temperature']),
                    top_p=float(params['top_p']),
                    top_k=int(params['top_k']),
                    repetition_penalty=float(params['repetition_penalty']),
                    no_repeat_ngram_size=int(params['no_repeat_ngram_size']),
                    max_new_tokens=int(params['max_new_tokens']),
                    pad_token_id=tokenizer.pad_token_id,
                    bad_words_ids=(None if args.disable_bad_words or args.policy_mode == "research" else (bad_words_ids if bad_words_ids else None)),
                )
                text = tokenizer.decode(gen[0], skip_special_tokens=True)
            else:
                text = ollama_generate(full_prompt, params)
            generations.append({
                "cycle": i + 1,
                "prompt": full_prompt,
                "params": params,
                "output": text,
            })
            all_metrics.append(m)
            print(f"\n[Cycle {i+1}] params: {params}")
            print("[Output]\n" + text + "\n")

    # Escribir logs y métricas
    with open(run_log_path, "w", encoding="utf-8") as f:
        json.dump({"generations": generations, "metrics": all_metrics}, f, ensure_ascii=False, indent=2)
    write_metrics_csv(metrics_csv_path, all_metrics)
    print(f"[OK] Guardado log: {run_log_path}")
    print(f"[OK] Guardado métricas: {metrics_csv_path}")
    print("Puedes graficar con: python scripts\\plot_metrics.py --in " + metrics_csv_path + " --out-dir plots_adapter")


if __name__ == "__main__":
    main()