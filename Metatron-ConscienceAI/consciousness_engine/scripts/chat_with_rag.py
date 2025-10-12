import argparse
import os
import sys
import json
from typing import List

# Asegurar import local de simple_rag
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from simple_rag import RagRetriever  # type: ignore


def build_prompt(context: str, user_text: str) -> str:
    parts: List[str] = []
    if context:
        parts.append("[Contexto recuperado]\n" + context.strip() + "\n")
    parts.append("[Usuario]\n" + user_text.strip() + "\n\n[Asistente]")
    return "\n".join(parts)


def ensure_transformers():
    try:
        import transformers  # noqa: F401
        import torch  # noqa: F401
    except Exception:
        raise RuntimeError("Se requieren 'transformers' y 'torch'. Instala con: pip install transformers torch")


def main():
    parser = argparse.ArgumentParser(description="Chat simple con RAG TF-IDF ligero")
    parser.add_argument("--rag-corpus", type=str, required=True, help="Ruta a corpus JSONL para RAG")
    parser.add_argument("--model", type=str, default="distilgpt2", help="Modelo HF para generación")
    parser.add_argument("--top-k", type=int, default=3, help="Top-K documentos recuperados")
    parser.add_argument("--max-chars", type=int, default=1200, help="Máximo de caracteres del contexto inyectado")
    parser.add_argument("--max-new-tokens", type=int, default=128, help="Tokens nuevos a generar")
    parser.add_argument("--out-dir", type=str, default="runs", help="Carpeta para guardar transcripciones")
    args = parser.parse_args()

    ensure_transformers()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    print(f"[RAG] Cargando corpus: {args.rag_corpus}")
    rag = RagRetriever(args.rag_corpus)
    print(f"[RAG] Documentos: {len(rag.docs)}")

    print(f"[HF] Cargando modelo: {args.model}")
    tok = AutoTokenizer.from_pretrained(args.model)
    if tok.pad_token_id is None:
        tok.pad_token_id = tok.eos_token_id
    model = AutoModelForCausalLM.from_pretrained(args.model)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    os.makedirs(args.out_dir, exist_ok=True)
    chat_log_path = os.path.join(args.out_dir, "chat_rag_log.jsonl")
    print("[INFO] Escribe tu consulta. Ctrl+C para salir.")

    with open(chat_log_path, "a", encoding="utf-8") as logf:
        while True:
            try:
                user_q = input("Tú> ").strip()
                if not user_q:
                    continue
                hits = rag.search(user_q, top_k=int(args.top_k))
                context = rag.make_context(hits, max_chars=int(args.max_chars)) if hits else ""
                prompt = build_prompt(context, user_q)
                inputs = tok(prompt, return_tensors="pt").to(device)
                out = model.generate(**inputs, max_new_tokens=int(args.max_new_tokens), do_sample=True)
                text = tok.decode(out[0], skip_special_tokens=True)
                # Tomar solo la parte de la respuesta después de [Asistente]
                resp = text.split("[Asistente]")[-1].strip()
                print(f"Asistente> {resp}")
                logf.write(json.dumps({"user": user_q, "context": context, "response": resp}, ensure_ascii=False) + "\n")
                logf.flush()
            except KeyboardInterrupt:
                print("\n[FIN] Sesión terminada.")
                break
            except Exception as e:
                print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()