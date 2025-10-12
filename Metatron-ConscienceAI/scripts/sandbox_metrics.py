"""
Simple sandbox metrics runner for /api/chat to measure latency and source counts.

Usage:
  python scripts/sandbox_metrics.py [--server_url http://127.0.0.1:5179] [--runs 5]
"""
from __future__ import annotations

import argparse
import math
import statistics as stats
import time
import os
from typing import Any, Dict, List

import requests


def measure_chat(server_url: str, runs: int = 5) -> Dict[str, Any]:
    url = server_url.rstrip("/") + "/api/chat"
    payload: Dict[str, Any] = {
        "message": "Resumen breve de Bitcoin",
        "session_id": "sandbox_metrics",
        "rag": True,
        "top_k": 8,
        "max_chars": 1000,
        "max_new_tokens": 32,
    }

    times_ms: List[float] = []
    counts: List[int] = []
    samples: List[Dict[str, Any]] = []
    for i in range(max(1, int(runs))):
        t0 = time.time()
        r = requests.post(url, json=payload, timeout=60)
        dt = (time.time() - t0) * 1000.0
        try:
            data = r.json()
        except Exception:
            data = {}
        times_ms.append(dt)
        sources = data.get("sources") or []
        counts.append(len(sources))
        if i == 0 and isinstance(sources, list):
            samples = sources[:3]
        print(f"run {i+1}: {dt:.1f} ms, sources={counts[-1]}")

    sorted_times = sorted(times_ms)
    p50 = stats.median(times_ms)
    idx95 = max(0, min(len(sorted_times) - 1, math.ceil(0.95 * len(sorted_times)) - 1))
    p95 = sorted_times[idx95]
    avg_sources = (sum(counts) / len(counts)) if counts else 0.0

    print(f"p50: {p50:.1f} ms")
    print(f"p95: {p95:.1f} ms")
    print(f"avg_sources: {avg_sources:.2f}")

    # Show dedup fields sample
    if samples:
        print("sample dedup fields (first 3 sources):")
        for i, s in enumerate(samples, 1):
            m = (s.get("meta") or {})
            print(f"  {i}. norm={m.get('normalized_url')} dedup={m.get('dedup_sources')}")

    return {
        "p50_ms": p50,
        "p95_ms": p95,
        "avg_sources": avg_sources,
        "runs": len(times_ms),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--server_url", default=os.getenv("SERVER_URL", "http://127.0.0.1:5179"))
    ap.add_argument("--runs", type=int, default=5)
    args = ap.parse_args()
    measure_chat(args.server_url, runs=args.runs)


if __name__ == "__main__":
    main()