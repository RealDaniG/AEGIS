#!/usr/bin/env python
"""
RAG ligero sin dependencias externas: construye un índice TF-IDF básico sobre un corpus JSONL
y permite recuperar los top-K fragmentos relevantes para una consulta.

Formato esperado del JSONL: cada línea es un objeto con alguno de estos campos:
- "text" | "content" | "summary" | "body" | "title" (se concatenan en ese orden si existen)
- Campos opcionales como "source", "url", "language" se conservan como metadatos.

Uso:
  from simple_rag import RagRetriever
  rr = RagRetriever("datasets/rss_research.jsonl")
  hits = rr.search("¿Qué avances recientes hay en modelos de lenguaje?")
  ctx = rr.make_context(hits, max_chars=1200)
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple


TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def normalize_text(s: str) -> str:
    return (s or "").strip()


def tokenize(s: str) -> List[str]:
    return [t.lower() for t in TOKEN_RE.findall(s or "") if t]


class RagRetriever:
    def __init__(self, corpus_path: str | Path):
        self.corpus_path = Path(corpus_path)
        if not self.corpus_path.exists():
            raise FileNotFoundError(f"No existe el corpus: {self.corpus_path}")
        self.docs: List[Dict[str, Any]] = []
        self.df: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.doc_tf: List[Dict[str, float]] = []
        self.doc_norms: List[float] = []
        self._load()

    def _compose_text(self, obj: Dict[str, Any]) -> str:
        parts = []
        for key in ("text", "content", "summary", "body", "title"):
            v = obj.get(key)
            if isinstance(v, str) and v.strip():
                parts.append(v.strip())
        return normalize_text("\n".join(parts))

    def _load(self):
        N = 0
        with self.corpus_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                text = self._compose_text(obj)
                if not text:
                    continue
                meta = {k: obj.get(k) for k in ("source", "url", "language", "title") if k in obj}
                toks = tokenize(text)
                if not toks:
                    continue
                N += 1
                tf: Dict[str, float] = {}
                for t in toks:
                    tf[t] = tf.get(t, 0.0) + 1.0
                for t in tf:
                    self.df[t] = self.df.get(t, 0) + 1
                self.docs.append({"text": text, "meta": meta, "toks": toks})
                self.doc_tf.append(tf)

        # IDF y normalización
        self.idf = {t: math.log((N + 1) / (df + 1)) + 1.0 for t, df in self.df.items()}
        self.doc_norms = []
        for tf in self.doc_tf:
            s = 0.0
            for t, f in tf.items():
                w = f * self.idf.get(t, 0.0)
                s += w * w
            self.doc_norms.append(math.sqrt(s) if s > 0 else 1.0)

    def _query_vector(self, query: str) -> Dict[str, float]:
        toks = tokenize(query)
        tf: Dict[str, float] = {}
        for t in toks:
            tf[t] = tf.get(t, 0.0) + 1.0
        q: Dict[str, float] = {}
        for t, f in tf.items():
            q[t] = f * self.idf.get(t, 0.0)
        return q

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float, Dict[str, Any]]]:
        q = self._query_vector(query)
        if not q:
            return []
        # Producto punto coseno entre q y cada doc
        scores = []
        q_norm = math.sqrt(sum(w * w for w in q.values())) or 1.0
        for i, tf in enumerate(self.doc_tf):
            dot = 0.0
            for t, qw in q.items():
                fw = tf.get(t, 0.0) * self.idf.get(t, 0.0)
                if fw:
                    dot += qw * fw
            denom = q_norm * (self.doc_norms[i] or 1.0)
            s = dot / denom if denom > 0 else 0.0
            scores.append((i, s))
        scores.sort(key=lambda x: x[1], reverse=True)
        out = []
        for i, s in scores[:max(1, top_k)]:
            d = self.docs[i]
            out.append((d["text"], float(s), d["meta"]))
        return out

    def make_context(self, hits: List[Tuple[str, float, Dict[str, Any]]], max_chars: int = 1200) -> str:
        """Concatena los textos recuperados con cabeceras simples, respetando max_chars."""
        parts = []
        for text, score, meta in hits:
            header = f"[src={meta.get('source') or meta.get('url') or ''} score={score:.3f}]"
            parts.append(header + "\n" + text.strip())
        ctx = "\n\n".join(parts)
        if len(ctx) > max_chars:
            return ctx[:max_chars] + "\n..."
        return ctx