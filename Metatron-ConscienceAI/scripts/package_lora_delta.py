#!/usr/bin/env python
"""
Empaqueta un adapter LoRA y sus métricas asociadas en un zip para envío federado.

Uso:
  python scripts/package_lora_delta.py --model-dir models/qwen2_5_0_5b_pdf_es_lora_full3e --eval-dir ai_eval_qwen25_lora_over_base_research --out federated/out/qwen25_pdf_full3e.zip
"""
from __future__ import annotations

import argparse
from pathlib import Path
import json
import csv
from datetime import datetime
import zipfile


def add_if_exists(z: zipfile.ZipFile, base: Path, rel: str):
    p = base / rel
    if p.exists():
        z.write(p, arcname=rel)


def read_base_model(model_dir: Path) -> str | None:
    cfg = model_dir / "adapter_config.json"
    if cfg.exists():
        try:
            data = json.loads(cfg.read_text(encoding="utf-8"))
            for key in ("base_model_name_or_path", "base_model", "model_name"):
                if key in data:
                    return data[key]
        except Exception:
            return None
    return None


def read_accuracy_from_metrics(eval_dir: Path) -> float | None:
    f = eval_dir / "metrics.csv"
    if not f.exists():
        return None
    try:
        with f.open("r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            last = None
            for row in reader:
                last = row
            if not last:
                return None
            for k in ("accuracy", "acc"):
                if k in last and last[k] not in (None, ""):
                    try:
                        return float(last[k])
                    except Exception:
                        pass
    except Exception:
        return None
    return None


def main():
    parser = argparse.ArgumentParser(description="Empaquetado de adapter LoRA + métricas")
    parser.add_argument("--model-dir", type=str, required=True, help="Directorio del adapter LoRA")
    parser.add_argument("--eval-dir", type=str, required=False, help="Directorio con run_log.json/metrics.csv")
    parser.add_argument("--out", type=str, required=True, help="Ruta del zip de salida")
    parser.add_argument("--node-id", type=str, required=False, help="Identificador del nodo que genera el delta")
    args = parser.parse_args()

    model_dir = Path(args.model_dir)
    eval_dir = Path(args.eval_dir) if args.eval_dir else None
    out_zip = Path(args.out)
    out_zip.parent.mkdir(parents=True, exist_ok=True)

    to_zip = [
        "adapter_model.safetensors",
        "adapter_config.json",
        "added_tokens.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "merges.txt",
        "special_tokens_map.json",
        "training_args.bin",
        "chat_template.jinja",
    ]

    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for rel in to_zip:
            add_if_exists(z, model_dir, rel)
        # Incluir checkpoints si existen
        for child in model_dir.glob("checkpoint-*"):
            for f in child.rglob("*"):
                rel = f.relative_to(model_dir).as_posix()
                z.write(f, arcname=rel)
        # Métricas de evaluación
        if eval_dir and eval_dir.exists():
            for rel in ["run_log.json", "metrics.csv"]:
                add_if_exists(z, eval_dir, rel)
        # Manifest
        manifest = {
            "created_at": datetime.utcnow().isoformat() + "Z",
            "node_id": args.node_id or None,
            "base_model": read_base_model(model_dir),
            "metrics": {
                "accuracy": read_accuracy_from_metrics(eval_dir) if eval_dir else None
            },
            "files": [rel for rel in to_zip if (model_dir / rel).exists()],
        }
        manifest_bytes = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")
        z.writestr("manifest.json", manifest_bytes)

    print(f"Paquete generado: {out_zip}")


if __name__ == "__main__":
    main()