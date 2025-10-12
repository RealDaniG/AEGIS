import argparse
import csv
import os


def read_last_metrics(csv_path):
    if not os.path.exists(csv_path):
        return None
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            return None
        return rows[-1]


def to_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default


def to_int(x, default=0):
    try:
        return int(x)
    except Exception:
        return default


def score_metrics(m):
    entropy = to_float(m.get('entropy', 0))
    coherence = to_float(m.get('coherence', 0))
    logic_truth = to_int(m.get('logic_truth', 0))
    decision = to_int(m.get('decision', 0))
    empathy = to_float(m.get('empathy_score', 0))
    insight = to_float(m.get('insight_strength', 0))
    # Heurística: favorecer coherencia y lógica; penalizar entropía
    score = coherence - 0.01 * entropy + 0.5 * logic_truth + 0.2 * decision + 0.05 * empathy + 0.05 * insight
    return score, coherence, entropy, logic_truth, decision


def main():
    parser = argparse.ArgumentParser(description='Compute optimal number of cycles based on metrics.csv files')
    parser.add_argument('--base-dir', type=str, default='ai_eval_cycles_', help='Base directory prefix (e.g., ai_eval_cycles_)')
    parser.add_argument('--min', type=int, default=1, help='Minimum cycles')
    parser.add_argument('--max', type=int, default=5, help='Maximum cycles')
    args = parser.parse_args()

    results = []
    for n in range(args.min, args.max + 1):
        path = os.path.join(f"{args.base_dir}{n}", 'metrics.csv')
        m = read_last_metrics(path)
        if m is None:
            continue
        score, coh, ent, lt, dec = score_metrics(m)
        results.append((n, score, coh, ent, lt, dec))

    if not results:
        print('[ERROR] No hay métricas para calcular ciclos óptimos.')
        return 1

    results.sort(key=lambda t: t[0])
    print('Resultados por ciclos:')
    for n, score, coh, ent, lt, dec in results:
        print(f"Ciclos={n}: score={score:.4f}, coherence={coh:.4f}, entropy={ent:.2f}, logic_truth={lt}, decision={dec}")

    # Seleccionar el mejor; en caso de empate por score, preferir menor número de ciclos
    scores = [r[1] for r in results]
    max_score = max(scores)
    # Si todas las puntuaciones son prácticamente iguales, preferimos 1 ciclo
    if (max(scores) - min(scores)) < 1e-6:
        best = min(results, key=lambda t: t[0])
    else:
        candidates = [r for r in results if abs(r[1] - max_score) < 1e-6]
        best = min(candidates, key=lambda t: t[0])
    print(f"\nRecomendación: ciclos óptimos ~ {best[0]}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())