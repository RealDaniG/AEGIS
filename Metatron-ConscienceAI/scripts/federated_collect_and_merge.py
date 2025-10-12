#!/usr/bin/env python
"""
Colector federado: escanea un directorio de "inbox" con paquetes ZIP de adapters LoRA,
extrae los adapters, comprueba compatibilidad básica y ejecuta una agregación por promedio.

Uso:
  python scripts/federated_collect_and_merge.py \
    --inbox-dir federated/inbox \
    --work-dir federated/work \
    --out models/qwen2_5_0_5b_pdf_es_lora_global \
    [--min-adapters 2]
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from datetime import datetime
import csv
import zipfile

def find_zip_files(inbox: Path):
    return sorted([p for p in inbox.glob("*.zip")])

def extract_zip(zip_path: Path, work_dir: Path) -> Path:
    target = work_dir / zip_path.stem
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(target)
    return target

def read_base_model(adapter_dir: Path) -> str | None:
    cfg = adapter_dir / "adapter_config.json"
    if cfg.exists():
        try:
            data = json.loads(cfg.read_text(encoding="utf-8"))
            # intentos comunes
            for key in ("base_model_name_or_path", "base_model", "model_name"):
                if key in data:
                    return data[key]
        except Exception:
            return None
    return None

def has_adapter_files(adapter_dir: Path) -> bool:
    return (adapter_dir / "adapter_model.safetensors").exists()

def read_accuracy(adapter_dir: Path) -> float | None:
    # Primero intentar metrics.csv
    f = adapter_dir / "metrics.csv"
    if f.exists():
        try:
            with f.open("r", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                last = None
                for row in reader:
                    last = row
                if last:
                    for k in ("accuracy", "acc"):
                        if k in last and last[k] not in (None, ""):
                            try:
                                return float(last[k])
                            except Exception:
                                pass
        except Exception:
            pass
    # Si no hay CSV o no contiene accuracy, intentar manifest.json
    mf = adapter_dir / "manifest.json"
    if mf.exists():
        try:
            data = json.loads(mf.read_text(encoding="utf-8"))
            metrics = data.get("metrics") or {}
            acc = metrics.get("accuracy")
            if acc is not None:
                return float(acc)
        except Exception:
            pass
    return None

def compute_weights(adapters_dirs, metric_name: str | None):
    if not metric_name:
        return [1.0] * len(adapters_dirs)
    vals = []
    for d in adapters_dirs:
        if metric_name == "accuracy":
            v = read_accuracy(d)
        else:
            v = None
        vals.append(v)
    if all(v is None for v in vals):
        return [1.0] * len(adapters_dirs)
    available = [v for v in vals if v is not None]
    mean_v = sum(available) / len(available)
    vals = [v if v is not None else mean_v for v in vals]
    import math
    alpha = 5.0
    exps = [math.exp(alpha * (v - mean_v)) for v in vals]
    s = sum(exps)
    return [e / s for e in exps]

def main():
    parser = argparse.ArgumentParser(description="Colector y agregador federado de LoRA")
    parser.add_argument("--inbox-dir", type=str, required=True, help="Directorio con paquetes ZIP entrantes")
    parser.add_argument("--work-dir", type=str, required=True, help="Directorio de trabajo para extraer paquetes")
    parser.add_argument("--out", type=str, required=True, help="Directorio de salida del adapter global")
    parser.add_argument("--min-adapters", type=int, default=2, help="Mínimo de adapters para fusionar")
    parser.add_argument("--weighted-metric", type=str, default=None, help="Métrica para ponderar (ej: accuracy)")
    args = parser.parse_args()

    inbox = Path(args.inbox_dir)
    work = Path(args.work_dir)
    out_dir = Path(args.out)
    work.mkdir(parents=True, exist_ok=True)

    zips = find_zip_files(inbox)
    if not zips:
        print("[Colector] No hay paquetes en inbox.")
        return
    print(f"[Colector] Encontrados {len(zips)} paquetes ZIP.")

    extracted_dirs = []
    for zp in zips:
        d = extract_zip(zp, work)
        extracted_dirs.append(d)
        print(f"[Colector] Extraído: {zp.name} -> {d}")

    # Filtrar los que contienen adapter
    adapters_dirs = [d for d in extracted_dirs if has_adapter_files(d)]
    if len(adapters_dirs) < args.min_adapters:
        print(f"[Colector] Solo {len(adapters_dirs)} adapters válidos, mínimo requerido: {args.min_adapters}. Abortando.")
        return

    # Compatibilidad por base model (si está disponible)
    base_models = [(d, read_base_model(d)) for d in adapters_dirs]
    # Elegir el base_model más común
    counts = {}
    for _, bm in base_models:
        counts[bm] = counts.get(bm, 0) + 1
    common_bm = max(counts, key=counts.get)
    compatible = [d for d, bm in base_models if bm == common_bm]
    print(f"[Colector] Base model elegido: {common_bm} (adapters compatibles: {len(compatible)})")
    if len(compatible) < args.min_adapters:
        print("[Colector] No hay suficientes adapters compatibles para fusionar.")
        return

    # Calcular pesos si se solicita
    weights = compute_weights(compatible, args.weighted_metric)
    # Versionado de salida
    ts = datetime.now().strftime("v%Y%m%d_%H%M")
    versioned_out = out_dir / ts
    cmd = [
        "python", str(Path("scripts") / "aggregate_lora_adapters.py"),
        "--adapters", *[str(d) for d in compatible],
        "--weights", *[str(w) for w in weights],
        "--out", str(versioned_out),
    ]
    print("[Colector] Ejecutando agregación:", " ".join(cmd))
    import subprocess
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print("[Colector] Error en agregación:")
        print(r.stderr)
        return

    print(f"[Colector] Adapter global generado en {versioned_out}")
    # Changelog
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        changelog = out_dir / "CHANGELOG.md"
        weights_str = ", ".join(f"{w:.4f}" for w in weights)
        adapters_list = ", ".join(d.name for d in compatible)
        log = (
            f"\n## {ts}\n"
            f"Adapters: {adapters_list}\n"
            f"Weights: [{weights_str}]\n"
            f"Out: {versioned_out}\n"
        )
        with changelog.open("a", encoding="utf-8") as fh:
            fh.write(log)
    except Exception:
        pass

    # Limpieza opcional del workdir
    try:
        shutil.rmtree(work)
    except Exception:
        pass

if __name__ == "__main__":
    main()