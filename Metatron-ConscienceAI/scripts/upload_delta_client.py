#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path
import requests
import time


def build_proxies(socks5: str | None):
    """Construye diccionario de proxies para requests si se especifica SOCKS5.
    Usa esquema socks5h para que la resolución de DNS la haga el proxy (Tor).
    """
    if not socks5:
        return None
    return {
        "http": f"socks5h://{socks5}",
        "https": f"socks5h://{socks5}",
    }


def main():
    parser = argparse.ArgumentParser(description="Cliente para subir paquetes LoRA al servidor federado")
    parser.add_argument("--url", type=str, required=True, help="URL base del servidor (ej: http://127.0.0.1:8000)")
    parser.add_argument("--token", type=str, required=True, help="Token de autenticación")
    parser.add_argument("--zip", type=str, required=True, help="Ruta del paquete ZIP a subir")
    parser.add_argument("--node-id", type=str, required=False, default="local-node", help="Identificador del nodo")
    parser.add_argument("--socks5", type=str, required=False, default=None, help="Proxy SOCKS5 (ej: 127.0.0.1:9050) para Tor/.onion")
    args = parser.parse_args()

    zip_path = Path(args.zip)
    if not zip_path.exists():
        raise FileNotFoundError(f"No existe {zip_path}")

    files = {"file": (zip_path.name, zip_path.read_bytes(), "application/zip")}
    headers = {"X-Auth-Token": args.token, "X-Node-Id": args.node_id}
    proxies = build_proxies(args.socks5)
    url = f"{args.url}/upload"
    last_exc = None
    for attempt in range(1, 6):
        try:
            resp = requests.post(url, files=files, headers=headers, timeout=120, proxies=proxies)
            resp.raise_for_status()
            try:
                print(resp.json())
            except ValueError:
                print({"status": resp.status_code, "text": resp.text[:500]})
            return
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            last_exc = e
            wait = min(5 * attempt, 20)
            print(f"[WARN] Conexión fallida (intento {attempt}/5): {e}. Reintentando en {wait}s...")
            time.sleep(wait)
        except requests.exceptions.HTTPError as e:
            # Reintenta en 5xx; en 4xx no tiene sentido reintentar
            if 500 <= e.response.status_code < 600:
                last_exc = e
                wait = min(5 * attempt, 20)
                print(f"[WARN] HTTP {e.response.status_code} (intento {attempt}/5): {e}. Reintentando en {wait}s...")
                time.sleep(wait)
            else:
                raise
    # Si llegó aquí, agotó los reintentos
    raise SystemExit(f"Fallo al subir tras múltiples intentos: {last_exc}")


if __name__ == "__main__":
    main()