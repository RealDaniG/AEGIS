import argparse
import json
import os
import sys
import subprocess


def run_orchestrator(cycles: int, out_path: str, fmt: str) -> subprocess.CompletedProcess:
    cmd = [
        sys.executable,
        "-m",
        "consciousness_engine.orchestrator.harmonic_orchestrator",
        "--cycles",
        str(cycles),
        "--out",
        out_path,
        "--format",
        fmt,
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def validate_metrics(out_path: str, fmt: str, expected_cycles: int) -> bool:
    if not os.path.exists(out_path):
        print(f"[ERROR] Metrics file not found: {out_path}")
        return False
    try:
        if fmt == "json":
            with open(out_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            metrics = data.get("metrics", [])
            if not isinstance(metrics, list) or len(metrics) == 0:
                print("[ERROR] No metrics found in JSON output")
                return False
            # Basic field validation on first entry
            m = metrics[0]
            required = [
                "cycle","entropy","coherence","valence","arousal",
                "decision","logic_truth","empathy_score","insight_strength"
            ]
            for k in required:
                if k not in m:
                    print(f"[ERROR] Missing field '{k}' in metrics entry")
                    return False
            print(f"[OK] JSON metrics validated. Entries: {len(metrics)} (expected {expected_cycles})")
            return True
        else:
            with open(out_path, "r", encoding="utf-8") as f:
                lines = [ln.strip() for ln in f.readlines() if ln.strip()]
            if len(lines) < 2:
                print("[ERROR] CSV has no data rows")
                return False
            header = lines[0].split(",")
            required = [
                "cycle","entropy","coherence","valence","arousal",
                "decision","logic_truth","empathy_score","insight_strength"
            ]
            for k in required:
                if k not in header:
                    print(f"[ERROR] Missing column '{k}' in CSV header")
                    return False
            rows = lines[1:]
            print(f"[OK] CSV metrics validated. Rows: {len(rows)} (expected {expected_cycles})")
            return True
    except Exception as e:
        print(f"[ERROR] Failed to validate metrics: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Smoke test for Harmonic Orchestrator")
    parser.add_argument("--cycles", type=int, default=3, help="Number of cycles to run")
    parser.add_argument("--format", type=str, choices=["csv", "json"], default="csv", help="Output format")
    parser.add_argument("--out", type=str, default=os.path.join("test_output", "metrics.csv"), help="Output metrics file path")
    args = parser.parse_args()

    dirname = os.path.dirname(args.out)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)

    proc = run_orchestrator(args.cycles, args.out, args.format)
    print(proc.stdout)
    if proc.returncode != 0:
        print(proc.stderr)
        print(f"[ERROR] Orchestrator exited with code {proc.returncode}")
        sys.exit(proc.returncode)

    ok = validate_metrics(args.out, args.format, args.cycles)
    if not ok:
        sys.exit(1)
    print("[SUCCESS] Smoke test completed.")


if __name__ == "__main__":
    main()