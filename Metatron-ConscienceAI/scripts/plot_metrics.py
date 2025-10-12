import argparse
import csv
import json
import os
import sys


def load_metrics(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        metrics = data.get("metrics", [])
    else:
        # Assume CSV
        metrics = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                m = {}
                for k, v in row.items():
                    if k == "cycle":
                        try:
                            m[k] = int(v)
                        except Exception:
                            m[k] = v
                    elif k in {"decision", "logic_truth"}:
                        try:
                            m[k] = int(v)
                        except Exception:
                            m[k] = v
                    else:
                        try:
                            m[k] = float(v)
                        except Exception:
                            m[k] = v
                metrics.append(m)
    return metrics


def ensure_outdir(out_dir: str):
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)


def plot_with_matplotlib(metrics, out_dir: str, show: bool, selected):
    try:
        import matplotlib.pyplot as plt
    except Exception as e:
        print("[WARN] matplotlib no disponible:", e)
        print("       Instala con: pip install matplotlib")
        return False

    ensure_outdir(out_dir)

    # Build series
    cycles = [m.get("cycle", i + 1) for i, m in enumerate(metrics)]
    all_keys = [k for k in metrics[0].keys() if k != "cycle"] if metrics else []
    keys = selected if selected else all_keys

    # Grid figure
    n = len(keys)
    cols = 2
    rows = (n + cols - 1) // cols
    fig, axs = plt.subplots(rows, cols, figsize=(6 * cols, 3.0 * rows), squeeze=False)
    axs_flat = axs.ravel()

    for i, key in enumerate(keys):
        ax = axs_flat[i]
        series = [m.get(key, 0) for m in metrics]
        if key in ("decision", "logic_truth"):
            ax.step(cycles, series, where='mid', label=key)
            ax.set_ylim(-0.1, 1.1)
        else:
            ax.plot(cycles, series, marker='o', label=key)
        ax.set_title(key)
        ax.set_xlabel("cycle")
        ax.grid(True, alpha=0.3)
    # Hide any extra axes
    for j in range(i + 1, len(axs_flat)):
        axs_flat[j].axis('off')

    fig.tight_layout()
    grid_path = os.path.join(out_dir, "metrics_grid.png") if out_dir else "metrics_grid.png"
    fig.savefig(grid_path, dpi=120)
    print(f"[OK] Guardado: {grid_path}")

    # Individual figures
    for key in keys:
        series = [m.get(key, 0) for m in metrics]
        plt.figure(figsize=(8, 3))
        if key in ("decision", "logic_truth"):
            plt.step(cycles, series, where='mid')
            plt.ylim(-0.1, 1.1)
        else:
            plt.plot(cycles, series, marker='o')
        plt.title(key)
        plt.xlabel("cycle")
        plt.grid(True, alpha=0.3)
        out_path = os.path.join(out_dir, f"metric_{key}.png") if out_dir else f"metric_{key}.png"
        plt.tight_layout()
        plt.savefig(out_path, dpi=120)
        plt.close()
        print(f"[OK] Guardado: {out_path}")

    if show:
        plt.show()

    return True


def ascii_plot(metrics, selected):
    print("[INFO] Usando modo ASCII (sin matplotlib)")
    cycles = [m.get("cycle", i + 1) for i, m in enumerate(metrics)]
    keys = selected if selected else [k for k in metrics[0].keys() if k != "cycle"]

    for key in keys:
        series = [m.get(key, 0) for m in metrics]
        # Normalize to 0..50
        try:
            vals = [float(v) for v in series]
            vmin = min(vals)
            vmax = max(vals)
            span = (vmax - vmin) or 1.0
            bars = [int(50 * (v - vmin) / span) for v in vals]
            print(f"\n{key}")
            for c, b, v in zip(cycles, bars, vals):
                print(f"{c:02d} | " + ("#" * b) + f" ({v:.6f})")
        except Exception:
            print(f"\n{key}")
            for c, v in zip(cycles, series):
                print(f"{c:02d} | {v}")


def main():
    parser = argparse.ArgumentParser(description="Plot metrics over cycles (CSV/JSON)")
    parser.add_argument("--in", dest="in_path", required=True, help="Input metrics file (CSV or JSON)")
    parser.add_argument("--out-dir", dest="out_dir", default="plots", help="Output directory for images")
    parser.add_argument("--show", action="store_true", help="Show plots interactively")
    parser.add_argument("--metrics", type=str, default="", help="Comma-separated list of metrics to plot (default: all)")
    args = parser.parse_args()

    metrics = load_metrics(args.in_path)
    if not metrics:
        print("[ERROR] No se pudieron cargar métricas del archivo.")
        sys.exit(1)

    selected = [m.strip() for m in args.metrics.split(",") if m.strip()] if args.metrics else []

    ok = plot_with_matplotlib(metrics, args.out_dir, args.show, selected)
    if not ok:
        ascii_plot(metrics, selected)


if __name__ == "__main__":
    main()