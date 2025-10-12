import os
import json
import argparse
from typing import List, Dict

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None


def read_pdf_text(path: str) -> str:
    if PdfReader is None:
        raise RuntimeError("pypdf no está instalado. Ejecuta: pip install pypdf")
    reader = PdfReader(path)
    texts: List[str] = []
    for page in reader.pages:
        try:
            t = page.extract_text() or ""
        except Exception:
            t = ""
        texts.append(t)
    return "\n".join(texts)


def clean_text(t: str) -> str:
    t = t.replace("\r", " ")
    t = "\n".join(line.strip() for line in t.splitlines())
    return t.strip()


def chunk_text(t: str, chunk_size: int = 1500, overlap: int = 200) -> List[str]:
    # chunk por caracteres, con solape opcional
    chunks: List[str] = []
    i = 0
    n = len(t)
    while i < n:
        end = min(i + chunk_size, n)
        chunk = t[i:end]
        chunks.append(chunk)
        if end >= n:
            break
        i = end - overlap if overlap > 0 else end
        i = max(i, 0)
    return chunks


def main():
    parser = argparse.ArgumentParser(description="Genera JSONL de entrenamiento desde PDFs (ES)")
    parser.add_argument("--src-dir", type=str, required=True, help="Carpeta con PDFs")
    parser.add_argument("--out-prefix", type=str, default="datasets/pdf_es", help="Prefijo de salida (sin extensión)")
    parser.add_argument("--chunk-size", type=int, default=1500, help="Tamaño de chunk en caracteres")
    parser.add_argument("--overlap", type=int, default=200, help="Solape entre chunks")
    parser.add_argument("--make-qa", action="store_true", help="Genera estructura QA (response vacío)")

    args = parser.parse_args()

    if not os.path.isdir(args.src_dir):
        raise FileNotFoundError(f"No existe la carpeta: {args.src_dir}")

    os.makedirs(os.path.dirname(args.out_prefix), exist_ok=True)
    raw_out = args.out_prefix + "_raw.jsonl"
    qa_out = args.out_prefix + "_qa.jsonl"

    raw_count = 0
    qa_count = 0
    with open(raw_out, "w", encoding="utf-8") as f_raw:
        f_qa = open(qa_out, "w", encoding="utf-8") if args.make_qa else None
        try:
            for name in sorted(os.listdir(args.src_dir)):
                if not name.lower().endswith(".pdf"):
                    continue
                pdf_path = os.path.join(args.src_dir, name)
                print(f"[INFO] Leyendo {pdf_path}")
                text = clean_text(read_pdf_text(pdf_path))
                if not text:
                    print(f"[WARN] Sin texto extraíble: {name}")
                    continue
                chunks = chunk_text(text, args.chunk_size, args.overlap)
                for idx, ch in enumerate(chunks):
                    rec_raw: Dict = {"text": ch, "source": name, "chunk_id": idx}
                    f_raw.write(json.dumps(rec_raw, ensure_ascii=False) + "\n")
                    raw_count += 1
                    if f_qa:
                        rec_qa: Dict = {
                            "instruction": "Resume el siguiente fragmento y extrae conceptos clave.",
                            "input": ch,
                            "response": ""
                        }
                        f_qa.write(json.dumps(rec_qa, ensure_ascii=False) + "\n")
                        qa_count += 1
        finally:
            if f_qa:
                f_qa.close()

    print(f"[OK] Guardado: {raw_out} (registros={raw_count})")
    if args.make_qa:
        print(f"[OK] Guardado: {qa_out} (registros={qa_count})")


if __name__ == "__main__":
    main()