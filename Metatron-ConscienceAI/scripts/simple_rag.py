#!/usr/bin/env python
"""
Simple RAG implementation without external dependencies.
Builds a basic TF-IDF index over a JSONL corpus and allows retrieving
top-K relevant fragments for a query.

Expected JSONL format: each line is an object with some of these fields:
- "text" | "content" | "summary" | "body" | "title" (concatenated in that order if present)
- Optional fields like "source", "url", "language" are preserved as metadata.

Usage:
  from simple_rag import RagRetriever
  rr = RagRetriever("datasets/rss_research.jsonl")
  hits = rr.search("What recent advances are there in language models?")
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
            raise FileNotFoundError(f"Corpus not found: {self.corpus_path}")
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

        # IDF and normalization
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
        # Cosine dot product between q and each doc
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
        """Concatenate retrieved texts with simple headers, respecting max_chars."""
        parts = []
        for text, score, meta in hits:
            header = f"[src={meta.get('source') or meta.get('url') or ''} score={score:.3f}]"
            parts.append(header + "\n" + text.strip())
        ctx = "\n\n".join(parts)
        if len(ctx) > max_chars:
            return ctx[:max_chars] + "\n..."
        return ctx