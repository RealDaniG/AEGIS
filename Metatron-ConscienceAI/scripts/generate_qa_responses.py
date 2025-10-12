import argparse
import json
import os
from typing import Dict, Iterator

import torch
from tqdm import tqdm
from transformers import AutoTokenizer, GPT2LMHeadModel


def read_jsonl(path: str) -> Iterator[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception:
                continue


def main():
    parser = argparse.ArgumentParser(description="Generar respuestas automáticas para dataset QA JSONL")
    parser.add_argument("--model", required=True, help="Ruta/nombre del modelo para generación")
    parser.add_argument("--input", required=True, help="Ruta al JSONL con campos instruction/input/response")
    parser.add_argument("--output", required=True, help="Ruta de salida JSONL con responses completadas")
    parser.add_argument("--max-new-tokens", type=int, default=180)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--limit", type=int, default=0, help="Limitar número de ejemplos (0 = sin límite)")
    parser.add_argument("--max-input-tokens", type=int, default=800, help="Máximo de tokens de entrada antes de generar")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print(f"[INFO] Cargando tokenizer y modelo: {args.model}")
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = GPT2LMHeadModel.from_pretrained(args.model)
    model.config.pad_token_id = tokenizer.pad_token_id
    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    print(f"[INFO] Dispositivo: {device}")

    count = 0
    written = 0
    with open(args.output, "w", encoding="utf-8") as out_f:
        for ex in tqdm(read_jsonl(args.input), desc="Generando", unit="ej"):
            if args.limit and count >= args.limit:
                break
            count += 1

            instr = ex.get("instruction") or ex.get("question") or "Resume el fragmento y extrae conceptos clave."
            inp = ex.get("input") or ex.get("context") or ex.get("text") or ""

            prompt = (
                f"Instrucción: {instr}\n"
                f"Entrada:\n{inp}\n"
                f"Respuesta:"
            )

            # Limitar tamaño de entrada para evitar overflow de posiciones
            max_pos = getattr(model.config, "n_positions", None) or getattr(model.config, "max_position_embeddings", 1024)
            budget = max_pos - args.max_new_tokens - 8
            max_inp = min(args.max_input_tokens, budget)
            inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_inp)
            input_ids = inputs["input_ids"].to(device)

            with torch.no_grad():
                gen_ids = model.generate(
                    input_ids=input_ids,
                    max_new_tokens=args.max_new_tokens,
                    do_sample=True,
                    temperature=args.temperature,
                    top_p=args.top_p,
                    eos_token_id=tokenizer.eos_token_id,
                    pad_token_id=tokenizer.pad_token_id,
                )

            # Solo la parte generada nueva
            gen_new = gen_ids[0][input_ids.shape[1]:]
            response = tokenizer.decode(gen_new, skip_special_tokens=True).strip()

            ex_out = dict(ex)
            ex_out["response"] = response
            out_f.write(json.dumps(ex_out, ensure_ascii=False) + "\n")
            written += 1

    print(f"[OK] Generación completada. Ejemplos escritos: {written}")


if __name__ == "__main__":
    main()