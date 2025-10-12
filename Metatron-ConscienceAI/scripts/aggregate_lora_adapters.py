#!/usr/bin/env python
"""
Agrega (fusiona) adapters LoRA compatibles mediante promedio ponderado de pesos.

Uso:
  python scripts/aggregate_lora_adapters.py \
    --adapters models/qwen2_5_0_5b_pdf_es_lora models/qwen2_5_0_5b_pdf_es_lora_full3e models/qwen2_5_0_5b_math_es_lora \
    --weights 0.4 0.4 0.2 \
    --out models/qwen2_5_0_5b_pdf_es_lora_merged

Requisitos: safetensors
Notas:
- Los adapters deben compartir la misma arquitectura/base.
- Si una clave no existe en algún adapter, se ignora esa clave para el promedio.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

from safetensors.torch import load_file, save_file
import torch


def load_adapter(path: Path) -> Dict[str, torch.Tensor]:
    file = path / "adapter_model.safetensors"
    if not file.exists():
        raise FileNotFoundError(f"No se encontró {file}. Asegúrate de que el adapter esté exportado.")
    return load_file(str(file))


def average_weights(adapters: List[Dict[str, torch.Tensor]], weights: List[float]) -> Dict[str, torch.Tensor]:
    # Normalizar pesos
    total = sum(weights)
    weights = [w / total for w in weights]
    keys_common = set(adapters[0].keys())
    for ad in adapters[1:]:
        keys_common &= set(ad.keys())
    merged: Dict[str, torch.Tensor] = {}
    for k in keys_common:
        accum = None
        for w, ad in zip(weights, adapters):
            t = ad[k]
            val = t * w
            accum = val if accum is None else accum + val
        merged[k] = accum
    return merged


def copy_config(src_dir: Path, out_dir: Path):
    cfg = src_dir / "adapter_config.json"
    if cfg.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "adapter_config.json").write_text(cfg.read_text(encoding="utf-8"), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Agregación de adapters LoRA por promedio")
    parser.add_argument("--adapters", nargs="+", type=str, required=True, help="Directorios de adapters")
    parser.add_argument("--weights", nargs="+", type=float, required=False, help="Pesos (mismo número que adapters)")
    parser.add_argument("--out", type=str, required=True, help="Directorio de salida del adapter fusionado")
    args = parser.parse_args()

    adapter_dirs = [Path(p) for p in args.adapters]
    out_dir = Path(args.out)

    if args.weights:
        if len(args.weights) != len(adapter_dirs):
            raise ValueError("El número de pesos debe coincidir con el número de adapters")
        weights = args.weights
    else:
        weights = [1.0] * len(adapter_dirs)

    print("Cargando adapters...")
    valid_dirs = []
    adapters = []
    for d in adapter_dirs:
        try:
            ad = load_adapter(d)
            adapters.append(ad)
            valid_dirs.append(d)
        except FileNotFoundError as e:
            print(f"[Aviso] {e}")

    if len(adapters) < 2:
        if len(adapters) == 1:
            print("[Aviso] Solo 1 adapter válido: se copiará como salida.")
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / "adapter_model.safetensors"
            save_file(adapters[0], str(out_file))
            copy_config(valid_dirs[0], out_dir)
            print("Listo.")
            return
        print("[Error] No hay adapters válidos.")
        return

    # Ajustar pesos a los adapters válidos
    if len(weights) != len(adapter_dirs):
        # Ya validado arriba, pero por seguridad
        weights = [1.0] * len(adapter_dirs)
    weights = [w for w, d in zip(weights, adapter_dirs) if d in valid_dirs]

    print("Promediando pesos...")
    merged = average_weights(adapters, weights)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "adapter_model.safetensors"
    print(f"Guardando adapter fusionado en {out_file}...")
    save_file(merged, str(out_file))

    copy_config(valid_dirs[0], out_dir)
    print("Listo.")


if __name__ == "__main__":
    main()