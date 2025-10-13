import sys, os
from pathlib import Path
REPO_ROOT = Path(r"C:\\Users\\damep\\Documents\\Personales\\AI\\consciousness_engine\\consciousness_engine")
rag_path = REPO_ROOT / "consciousness_engine" / "scripts"
print("rag_path:", rag_path)
print("exists:", rag_path.exists())
print("files:", os.listdir(rag_path))
sys.path.insert(0, str(rag_path))
print("sys.path[0]", sys.path[0])
from simple_rag import RagRetriever
uploads = REPO_ROOT / "ai_runs" / "webchat_corpus" / "uploads.jsonl"
rr = RagRetriever(str(uploads))
for q in [
    "discord government ids leaked",
    "california signs law opt out browsers",
    "Y Combinator Forecasting Company"
]:
    hits = rr.search(q, top_k=3)
    print("QUERY:", q)
    print("HITS:", [(round(s,3), m) for _, s, m in hits])
    print()
