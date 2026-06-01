import os
import json
import numpy as np
import faiss
from .embeddings import get_embedding

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
INDEX_PATH = os.path.join(DATA_DIR, 'faiss_index.idx')
DOCS_PATH = os.path.join(DATA_DIR, 'docs.jsonl')

def load_docs():
    docs = []
    if os.path.exists(DOCS_PATH):
        with open(DOCS_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                docs.append(json.loads(line))
    return docs

def get_index():
    if not os.path.exists(INDEX_PATH):
        return None
    return faiss.read_index(INDEX_PATH)

def retrieve(question: str, k=4):
    idx = get_index()
    if idx is None:
        return []
    q_emb = np.array(get_embedding(question)).astype('float32')
    q_emb = q_emb.reshape(1, -1)
    D, I = idx.search(q_emb, k)
    docs = load_docs()
    results = []
    for i in I[0]:
        if i < len(docs):
            results.append(docs[i])
    return results
