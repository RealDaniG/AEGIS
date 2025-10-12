#!/usr/bin/env python
"""
Registra los recursos del nodo (CPU/GPU/RAM/Disco) y política de contribución.

Salida por defecto: ai_runs/node_resources.json
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import platform
from datetime import datetime, timezone

try:
    import psutil  # type: ignore
except Exception:
    psutil = None

try:
    import torch  # type: ignore
except Exception:
    torch = None


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def get_gpu_info():
    info = {
        "available": False,
        "name": None,
        "count": 0,
        "compute_capability": None,
        "architecture": None,
    }
    if torch is None:
        return info
    avail = torch.cuda.is_available()
    info["available"] = bool(avail)
    if avail:
        count = torch.cuda.device_count()
        info["count"] = int(count)
        try:
            name = torch.cuda.get_device_name(0)
        except Exception:
            name = None
        info["name"] = name
        # compute capability
        try:
            major, minor = torch.cuda.get_device_capability(0)
            info["compute_capability"] = f"{major}.{minor}"
            arch = "ampere_or_newer" if major >= 8 else "pre_ampere"
            info["architecture"] = arch
        except Exception:
            pass
    return info


def main():
    out_path = Path("ai_runs/node_resources.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cpu_count = os.cpu_count() or 1
    system = platform.system()
    release = platform.release()
    version = platform.version()

    mem_total = None
    mem_available = None
    disk_total = None
    disk_free = None
    if psutil:
        vm = psutil.virtual_memory()
        mem_total = vm.total
        mem_available = vm.available
        disk = psutil.disk_usage(".")
        disk_total = disk.total
        disk_free = disk.free

    gpu = get_gpu_info()

    # Política de contribución (ejemplo): porcentaje de CPU/tiempo y horario preferente
    contribution = {
        "cpu_share": 0.5,  # 50% de núcleos disponibles
        "schedule": {
            "preferred_hours_local": ["22:00-06:00"],
            "max_daily_minutes": 240
        },
        "tasks": ["ingest", "qa_generation", "evaluation", "lora_finetune"],
    }

    data = {
        "collected_at": utc_now(),
        "node": {
            "system": system,
            "release": release,
            "version": version,
        },
        "cpu": {
            "cores": cpu_count,
        },
        "memory": {
            "total_bytes": mem_total,
            "available_bytes": mem_available,
        },
        "disk": {
            "total_bytes": disk_total,
            "free_bytes": disk_free,
        },
        "gpu": gpu,
        "contribution_policy": contribution,
    }

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Recursos del nodo guardados en {out_path}")


if __name__ == "__main__":
    main()