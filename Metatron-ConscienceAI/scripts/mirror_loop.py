from __future__ import annotations

import time
from typing import Dict, Any, List, Optional, Tuple, Callable


class MirrorLoop:
    """Simple orchestrator for a mutual-improvement loop between two ChatService instances.

    This class is model-agnostic; it expects each service to expose a `chat(message, session_id, rag_enabled, top_k, max_chars, max_new_tokens)`
    method that returns a dict with keys: {response: str, sources: List[...], context: str}.
    """

    def __init__(self, service_a, service_b):
        self.service_a = service_a
        self.service_b = service_b

    def _score(self, text: str, sources: List[Dict[str, Any]], rubric: Dict[str, float]) -> Dict[str, float]:
        """Heuristic scoring using simple proxies. Values in [0,1]."""
        # Factualidad: proxy por citas presentes si hay RAG
        citations = 1.0 if sources and len(sources) > 0 else 0.0
        # Claridad: penaliza textos demasiado largos y con frases muy largas
        words = len((text or "").split())
        sentences = [s.strip() for s in (text or "").split('.') if s.strip()]
        avg_sent_len = (sum(len(s.split()) for s in sentences) / max(1, len(sentences))) if sentences else words
        clarity = max(0.0, min(1.0, 1.0 - (avg_sent_len / 40.0)))  # ideal ~20-25
        # Cobertura: proxy por longitud moderada (ni muy corta ni excesiva)
        coverage = max(0.0, min(1.0, words / 250.0))  # 250 palabras ~ buena cobertura breve
        # Creatividad: proxy por presencia de "ejemplo" o enumeraciones
        creativity = 1.0 if ("ejemplo" in text.lower() or ":" in text) else 0.3
        factualidad = citations  # sin verificación externa, usar citas como proxy
        # Componer puntaje ponderado
        weights = {"factualidad":0.4,"claridad":0.2,"cobertura":0.2,"creatividad":0.1,"citas":0.1}
        weights.update(rubric or {})
        total = (
            weights.get("factualidad",0.0)*factualidad +
            weights.get("claridad",0.0)*clarity +
            weights.get("cobertura",0.0)*coverage +
            weights.get("creatividad",0.0)*creativity +
            weights.get("citas",0.0)*citations
        )
        return {"factualidad":factualidad, "claridad":clarity, "cobertura":coverage, "creatividad":creativity, "citas":citations, "total": total}

    def run(self,
            objective: str,
            rounds: int,
            session_id: str,
            rag_enabled: bool = True,
            top_k: Optional[int] = None,
            max_chars: Optional[int] = None,
            max_new_tokens: Optional[int] = None,
            rubric: Optional[Dict[str, float]] = None,
            stop_event=None,
            on_round: Optional[Callable[[int, Dict[str, Any]], None]] = None,
        ) -> Tuple[str, List[Dict[str, Any]]]:
        """Execute the loop and return final result and per-round metrics.

        If provided, `on_round(round_number, round_info)` will be called after each round
        with a dict containing: {round, lead, score_lead, score_other, chosen}.
        """
        prev_answer = ""
        metrics: List[Dict[str, Any]] = []
        final_answer = ""
        # Alternate leadership: A starts, then B, etc.
        for r in range(1, int(rounds)+1):
            if stop_event and getattr(stop_event, "is_set", lambda: False)():
                break
            lead = 'A' if r % 2 == 1 else 'B'
            lead_service = self.service_a if lead == 'A' else self.service_b
            other_service = self.service_b if lead == 'A' else self.service_a

            # Step 1: lead proposes or refines
            if prev_answer:
                msg_lead = (f"{objective}\n\n[Respuesta previa]\n{prev_answer}\n\n"
                            f"Por favor, refina la respuesta manteniendo precisión, claridad y cita de fuentes cuando existan.")
            else:
                msg_lead = objective
            out_lead = lead_service.chat(
                message=msg_lead,
                session_id=session_id,
                rag_enabled=rag_enabled,
                top_k=top_k,
                max_chars=max_chars,
                max_new_tokens=max_new_tokens,
            )
            resp_lead = out_lead.get("response", "")

            # Step 2: other critiques and proposes improvements
            msg_other = (f"Evalúa la respuesta del otro agente según esta rúbrica y propone mejoras claras."
                         f"\nRúbrica: {rubric or {}}\n\nRespuesta a evaluar:\n{resp_lead}\n\n"
                         f"Devuelve una versión mejorada consolidada (no solo crítica), citando fuentes cuando existan.")
            out_other = other_service.chat(
                message=msg_other,
                session_id=session_id,
                rag_enabled=rag_enabled,
                top_k=top_k,
                max_chars=max_chars,
                max_new_tokens=max_new_tokens,
            )
            resp_other = out_other.get("response", "")

            # Choose the better one by heuristic score
            s_lead = self._score(resp_lead, out_lead.get("sources", []), rubric or {})
            s_other = self._score(resp_other, out_other.get("sources", []), rubric or {})
            chosen = resp_other if s_other.get("total",0) >= s_lead.get("total",0) else resp_lead
            prev_answer = chosen
            final_answer = chosen

            round_info = {
                "round": r,
                "lead": lead,
                "score_lead": s_lead,
                "score_other": s_other,
                "chosen": "other" if chosen == resp_other else "lead",
            }
            metrics.append(round_info)
            # Emit live progress if callback provided
            if on_round:
                try:
                    on_round(r, round_info)
                except Exception:
                    # Non-fatal: continue loop even if callback fails
                    pass

            # Small pause to be polite with device
            time.sleep(0.05)

        return final_answer, metrics