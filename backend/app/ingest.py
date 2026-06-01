import os
import json
from typing import List
from .embeddings import get_embedding

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
INDEX_PATH = os.path.join(DATA_DIR, 'faiss_index.idx')
DOCS_PATH = os.path.join(DATA_DIR, 'docs.jsonl')

def extract_text_from_pdf(path: str) -> str:
    # Support PDF and plain text fallback for samples
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        try:
            import fitz
        except Exception:
            raise RuntimeError('PyMuPDF not installed; cannot parse PDF')
        doc = fitz.open(path)
        texts = []
        for page in doc:
            texts.append(page.get_text())
        return "\n".join(texts)
    else:
        # try reading as plain text
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            # fallback to pdf parsing attempt
            try:
                import fitz
            except Exception:
                raise RuntimeError('Cannot read file as text and PyMuPDF not installed')
            doc = fitz.open(path)
            texts = []
            for page in doc:
                texts.append(page.get_text())
            return "\n".join(texts)

def chunk_text(text: str, chunk_size=1000, overlap=200) -> List[str]:
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        chunk = tokens[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

def ensure_index(dim=1536):
    try:
        import faiss
    except Exception:
        raise RuntimeError('faiss not installed; install faiss-cpu or use hosted vector DB')
    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
    else:
        index = faiss.IndexFlatL2(dim)
    return index

def ingest_file(path: str, metadata: dict = None):
    text = extract_text_from_pdf(path)
    chunks = chunk_text(text)
    vectors = []
    metas = []
    for i, c in enumerate(chunks):
        emb = get_embedding(c)
        vectors.append(emb)
        meta = {"source": os.path.basename(path), "chunk_index": i, "text": c}
        if metadata:
            meta.update(metadata)
        metas.append(meta)

    # persist metadata
    with open(DOCS_PATH, 'a', encoding='utf-8') as f:
        for m in metas:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    import numpy as np
    vecs = np.array(vectors).astype('float32')
    index = ensure_index(dim=vecs.shape[1])
    index.add(vecs)
    try:
        import faiss
        faiss.write_index(index, INDEX_PATH)
    except Exception:
        # if faiss not available at runtime, skip persistence
        pass
    return {"status": "ok", "chunks": len(chunks)}
