import argparse
import json
import os
import platform
import sys
import time


def safe_imports():
    mods = {}
    for name in ("requests", "transformers", "torch"):
        try:
            mods[name] = __import__(name)
        except Exception:
            mods[name] = None
    return mods


def external_ip(requests_mod):
    if requests_mod is None:
        return {"error": "requests no disponible"}
    try:
        r = requests_mod.get("https://api.ipify.org?format=json", timeout=5)
        return {"ip": r.json().get("ip")}
    except Exception as e:
        return {"error": str(e)}


def server_latency(requests_mod, url: str | None):
    if requests_mod is None or not url:
        return {}
    base = url.rstrip("/")
    candidates = ["/status", "/", "/list"]
    for path in candidates:
        full = base + path
        try:
            t0 = time.time()
            r = requests_mod.get(full, timeout=5)
            dt = (time.time() - t0) * 1000.0
            return {
                "url": full,
                "status_code": r.status_code,
                "latency_ms": round(dt, 2),
            }
        except Exception as e:
            last_err = str(e)
            continue
    return {"error": last_err if "last_err" in locals() else "no reachable path"}


def gpu_info(torch_mod):
    info = {
        "available": False,
        "count": 0,
        "name": None,
        "compute_capability": None,
        "architecture": None,
    }
    if torch_mod is None:
        return info
    try:
        avail = torch_mod.cuda.is_available()
        info["available"] = bool(avail)
        if avail:
            count = torch_mod.cuda.device_count()
            info["count"] = int(count)
            try:
                info["name"] = torch_mod.cuda.get_device_name(0)
            except Exception:
                pass
            try:
                major, minor = torch_mod.cuda.get_device_capability(0)
                info["compute_capability"] = f"{major}.{minor}"
                info["architecture"] = "ampere_or_newer" if major >= 8 else "pre_ampere"
            except Exception:
                pass
    except Exception:
        pass
    return info


def model_config(transformers_mod, model_ref: str):
    cfg = {}
    if transformers_mod is None:
        return {"error": "transformers no disponible"}
    try:
        AutoConfig = getattr(transformers_mod, "AutoConfig")
        c = AutoConfig.from_pretrained(model_ref)
        # Campos comunes
        keys = [
            "model_type",
            "vocab_size",
            "hidden_size",
            "num_hidden_layers",
            "num_attention_heads",
            "max_position_embeddings",
            "intermediate_size",
            "n_embd",
            "n_layer",
            "n_head",
        ]
        for k in keys:
            cfg[k] = getattr(c, k, None)
        return cfg
    except Exception as e:
        return {"error": str(e)}


def param_count(transformers_mod, model_ref: str):
    if transformers_mod is None:
        return {"error": "transformers no disponible"}
    try:
        AutoModelForCausalLM = getattr(transformers_mod, "AutoModelForCausalLM")
        m = AutoModelForCausalLM.from_pretrained(model_ref, low_cpu_mem_usage=True, torch_dtype="auto")
        total = int(sum(p.numel() for p in m.parameters()))
        return {"total_parameters": total}
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Reporte rápido de modelo y red")
    parser.add_argument("--model", required=True, help="Modelo (ruta local o hub id)")
    parser.add_argument("--server-url", default="", help="URL del servidor federado para medir latencia")
    parser.add_argument("--out", default="ai_runs/model_network_report.json", help="Ruta de salida JSON")
    parser.add_argument("--skip-param-count", action="store_true", help="Saltar el conteo de parámetros para evitar cargas pesadas")
    args = parser.parse_args()

    mods = safe_imports()

    # Sistema
    sys_info = {
        "python": sys.version.split()[0],
        "os": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
    }

    versions = {
        "transformers": getattr(mods.get("transformers"), "__version__", None),
        "torch": getattr(mods.get("torch"), "__version__", None),
    }

    # Modelo
    m_cfg = model_config(mods.get("transformers"), args.model)
    m_params = {"skipped": True} if args.skip_param_count else param_count(mods.get("transformers"), args.model)

    # GPU
    gpu = gpu_info(mods.get("torch"))

    # Red
    ext_ip = external_ip(mods.get("requests"))
    latency = server_latency(mods.get("requests"), args.server_url)

    data = {
        "collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "system": sys_info,
        "versions": versions,
        "model": {
            "ref": args.model,
            "config": m_cfg,
            "parameters": m_params,
        },
        "gpu": gpu,
        "network": {
            "external_ip": ext_ip,
            "server_latency": latency,
        },
    }

    out_path = args.out
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Resumen humano
    print("[Reporte] Modelo y Red")
    print(f"  Modelo: {args.model}")
    cfg = data["model"]["config"]
    if "error" not in cfg:
        print(f"  - tipo: {cfg.get('model_type')} | vocab: {cfg.get('vocab_size')} | hidden: {cfg.get('hidden_size')} | capas: {cfg.get('num_hidden_layers')}")
        print(f"  - heads: {cfg.get('num_attention_heads')} | max_pos: {cfg.get('max_position_embeddings')} | intermed: {cfg.get('intermediate_size')}")
    else:
        print(f"  - config error: {cfg['error']}")
    pinfo = data["model"]["parameters"]
    if "total_parameters" in pinfo:
        print(f"  - parámetros: {pinfo['total_parameters']:,}")
    elif pinfo.get("skipped"):
        print("  - parámetros: omitido (skip-param-count)")
    else:
        print(f"  - parámetros error: {pinfo.get('error')}")

    print(f"  GPU: disponible={data['gpu'].get('available')} | nombre={data['gpu'].get('name')} | count={data['gpu'].get('count')} | cc={data['gpu'].get('compute_capability')}")
    print(f"  Red: IP externa={data['network']['external_ip'].get('ip', 'N/A')} | latencia servidor={data['network']['server_latency'].get('latency_ms', 'N/A')} ms")
    print(f"  Versiones: transformers={versions['transformers']} | torch={versions['torch']} | python={sys_info['python']}")
    print(f"[OK] Guardado en {out_path}")


if __name__ == "__main__":
    main()