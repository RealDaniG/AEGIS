#!/usr/bin/env python
"""
Ingesta de feeds RSS/Atom para investigación con autogestión de fuentes.

Características:
- Lee un archivo JSON con la lista de feeds y metadatos (activo, prioridad, tópicos, idioma).
- Descarga entradas nuevas y las guarda en JSONL con trazabilidad (feed, título, resumen, link, fecha).
- Filtra por idiomas y palabras clave (tópicos) para priorizar relevancia.
- Evita duplicados usando (feed_url + entry_id/link) como clave.
- Actualiza métricas por feed (procesados, coincidencias, tasa de coincidencia).
- Autogestión opcional: desactiva feeds de baja relevancia según umbral.

Uso:
  python scripts/rss_ingest.py \
    --feeds datasets/rss_feeds.json \
    --out datasets/rss_research.jsonl \
    --stats ai_runs/rss_stats.json \
    --languages es,en \
    --topics "ia;inteligencia artificial;machine learning;ml;física cuántica;neurociencia" \
    --max-items-per-feed 50 \
    --auto-manage

Requiere: feedparser
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from datetime import datetime
import re
import sys

try:
    import feedparser  # type: ignore
except Exception:
    print("ERROR: Falta la dependencia 'feedparser'. Instala con: python -m pip install feedparser", file=sys.stderr)
    sys.exit(1)


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_existing_ids(out_path: Path) -> set[str]:
    ids: set[str] = set()
    if not out_path.exists():
        return ids
    try:
        with out_path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    if isinstance(obj, dict) and "_id" in obj:
                        ids.add(str(obj["_id"]))
                except Exception:
                    continue
    except Exception:
        pass
    return ids


def normalize_text(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def entry_language(entry) -> str:
    # Intento heurístico de idioma: RSS/Atom no siempre lo incluye.
    lang = (
        getattr(entry, "language", None)
        or getattr(entry, "dc_language", None)
        or getattr(entry, "lang", None)
    )
    if isinstance(lang, str):
        return lang.lower()[:2]
    return ""


def matches_topics(text: str, topics_regex) -> bool:
    if not text:
        return False
    return bool(topics_regex.search(text.lower()))


def ingest_feed(feed: dict, args, existing_ids: set[str]):
    url = feed.get("url")
    name = feed.get("name", url)
    priority = feed.get("priority", "medium")
    topics = feed.get("topics", [])
    feed_lang = (feed.get("language") or "").lower()

    if not url:
        return [], {"processed": 0, "matched": 0}

    print(f"Descargando feed: {name} -> {url}")
    parsed = feedparser.parse(url)
    entries = getattr(parsed, "entries", []) or []
    if args.max_items_per_feed and len(entries) > args.max_items_per_feed:
        entries = entries[: args.max_items_per_feed]

    topics_all = list(args.topics)
    if topics:
        topics_all.extend(topics)
    # Construir regex de tópicos (OR)
    escaped = [re.escape(t.lower()) for t in topics_all if t]
    topics_regex = re.compile(r"(" + r"|".join(escaped) + r")") if escaped else re.compile(r"^")

    processed = 0
    matched = 0
    results = []

    for e in entries:
        processed += 1
        title = normalize_text(getattr(e, "title", ""))
        summary = normalize_text(getattr(e, "summary", ""))
        link = normalize_text(getattr(e, "link", ""))
        # Fecha (ISO si posible)
        published = normalize_text(getattr(e, "published", "") or getattr(e, "updated", ""))
        try:
            published_parsed = getattr(e, "published_parsed", None) or getattr(e, "updated_parsed", None)
            if published_parsed:
                published = datetime(*published_parsed[:6]).isoformat()
        except Exception:
            pass

        entry_id = normalize_text(getattr(e, "id", "")) or link or f"{url}#{title[:50]}"
        _id = f"{url}|{entry_id}"
        if _id in existing_ids:
            continue

        lang = entry_language(e) or feed_lang
        if args.languages and lang and lang[:2] not in args.languages:
            continue

        text = f"{title} {summary}"
        is_match = True
        if topics_all:
            is_match = matches_topics(text, topics_regex)

        if is_match:
            matched += 1
            results.append({
                "_id": _id,
                "feed": url,
                "feed_name": name,
                "title": title,
                "summary": summary,
                "link": link,
                "published": published,
                "language": lang,
                "topics": topics_all,
                "ingested_at": datetime.utcnow().isoformat() + "Z",
                "source_priority": priority,
            })

    return results, {"processed": processed, "matched": matched}


def main():
    parser = argparse.ArgumentParser(description="Ingesta RSS para investigación con autogestión")
    parser.add_argument("--feeds", type=str, default="datasets/rss_feeds.json", help="Ruta del JSON de feeds")
    parser.add_argument("--out", type=str, default="datasets/rss_research.jsonl", help="Salida JSONL de entradas")
    parser.add_argument("--stats", type=str, default="ai_runs/rss_stats.json", help="Archivo JSON de métricas")
    parser.add_argument("--languages", type=str, default="es,en", help="Idiomas permitidos, separados por coma")
    parser.add_argument("--topics", type=str, default="ia;inteligencia artificial;machine learning;ml;física cuántica;neurociencia", help="Tópicos clave, separados por ';'")
    parser.add_argument("--max-items-per-feed", type=int, default=50, help="Límite de artículos por feed")
    parser.add_argument("--auto-manage", action="store_true", help="Autogestionar feeds (desactivar por baja relevancia)")
    parser.add_argument("--deactivate-threshold", type=float, default=0.15, help="Umbral de tasa de coincidencia para desactivar feeds")
    parser.add_argument("--min-processed-to-evaluate", type=int, default=20, help="Mínimo de artículos procesados para evaluar relevancia")

    args = parser.parse_args()
    feeds_path = Path(args.feeds)
    out_path = Path(args.out)
    stats_path = Path(args.stats)

    languages = [l.strip().lower() for l in (args.languages or "").split(",") if l.strip()]
    args.languages = languages
    topics = [t.strip().lower() for t in (args.topics or "").split(";") if t.strip()]
    args.topics = topics

    feeds_json = load_json(feeds_path, default={"feeds": []})
    feeds = feeds_json.get("feeds", [])
    stats = load_json(stats_path, default={})
    existing_ids = load_existing_ids(out_path)

    total_new = 0
    updated_stats = {}
    new_entries_all = []

    for feed in feeds:
        if not feed.get("active", True):
            continue
        new_entries, s = ingest_feed(feed, args, existing_ids)
        new_entries_all.extend(new_entries)
        updated_stats[feed.get("url")] = s
        total_new += len(new_entries)

    # Guardar nuevas entradas
    if new_entries_all:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("a", encoding="utf-8") as f:
            for obj in new_entries_all:
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    # Actualizar métricas acumuladas
    for url, s in updated_stats.items():
        prev = stats.get(url, {"items_ingested": 0, "processed": 0, "matched": 0, "last_ingest": None})
        accum = {
            "items_ingested": prev.get("items_ingested", 0) + s["matched"],
            "processed": prev.get("processed", 0) + s["processed"],
            "matched": prev.get("matched", 0) + s["matched"],
            "last_ingest": datetime.utcnow().isoformat() + "Z",
        }
        accum["match_rate"] = round((accum["matched"] / max(1, accum["processed"])), 3)
        stats[url] = accum

    save_json(stats_path, stats)

    # Autogestión de feeds
    if args.auto_manage:
        changed = False
        for feed in feeds:
            url = feed.get("url")
            if not url:
                continue
            prio = (feed.get("priority") or "medium").lower()
            st = stats.get(url, {})
            match_rate = st.get("match_rate", 0.0)
            processed = st.get("processed", 0)
            if prio == "high":
                continue  # No desactivar fuentes de alta prioridad automáticamente
            if processed >= args.min_processed_to_evaluate and match_rate < args.deactivate_threshold:
                if feed.get("active", True):
                    feed["active"] = False
                    changed = True
                    print(f"Autogestión: desactivado feed por baja relevancia -> {url} (match_rate={match_rate})")
        if changed:
            save_json(feeds_path, {"feeds": feeds})

    print(f"Total de nuevas entradas guardadas: {total_new}")


if __name__ == "__main__":
    main()