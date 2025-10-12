#!/usr/bin/env python
"""
Crea un subconjunto de un JSONL (toma las primeras N líneas; opcionalmente baraja).

Uso:
  python scripts/make_subset_jsonl.py --input datasets/pdf_es_qa.jsonl --output datasets/pdf_es_qa.small.jsonl --limit 200
  python scripts/make_subset_jsonl.py --input X.jsonl --output Y.jsonl --limit 500 --shuffle
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Ruta al JSONL de entrada")
    p.add_argument("--output", required=True, help="Ruta al JSONL de salida")
    p.add_argument("--limit", type=int, required=True, help="Número máximo de líneas a copiar")
    p.add_argument("--shuffle", action="store_true", help="Barajar antes de tomar el subset")
    args = p.parse_args()

    src = Path(args.input)
    dst = Path(args.output)
    if not src.exists():
        raise FileNotFoundError(f"No existe {src}")

    items = []
    with src.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                items.append(obj)
            except Exception:
                # Omitir líneas mal formadas
                continue

    if not items:
        raise RuntimeError("El archivo de entrada no contiene objetos válidos")

    if args.shuffle:
        random.shuffle(items)

    subset = items[: max(0, args.limit)]
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8") as f:
        for obj in subset:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    print(f"[OK] Subconjunto creado: {dst} (líneas: {len(subset)})")


if __name__ == "__main__":
    main()