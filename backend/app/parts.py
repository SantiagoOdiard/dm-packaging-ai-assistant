import os
import csv
import json
import numpy as np
from .embeddings import get_embedding

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
PARTS_FILE = os.path.join(DATA_DIR, 'parts', 'sample_parts.csv')
PARTS_EMBEDDINGS_FILE = os.path.join(DATA_DIR, 'parts_embeddings.json')

def load_parts():
    """Carica i ricambi dal CSV."""
    parts = []
    if os.path.exists(PARTS_FILE):
        with open(PARTS_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for r in reader:
                parts.append({
                    'name': r['name'],
                    'code': r['code'],
                    'compatibility': r['compatibility'],
                    'description': r['description']
                })
    return parts

def get_parts_embeddings():
    """
    Ottiene gli embeddings dei ricambi. Se non esistono, li calcola e li salva.
    """
    if os.path.exists(PARTS_EMBEDDINGS_FILE):
        try:
            with open(PARTS_EMBEDDINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    
    # Calcola gli embeddings se non esistono
    parts = load_parts()
    embeddings = {}
    
    for part in parts:
        # Usa il nome e la descrizione come testo di embedding
        text = f"{part['name']} {part['description']} {part['compatibility']}"
        try:
            emb = get_embedding(text)
            embeddings[part['code']] = {
                'text': text,
                'embedding': emb
            }
        except Exception:
            # Se l'API fallisce, continua senza embedding
            pass
    
    # Salva gli embeddings
    try:
        with open(PARTS_EMBEDDINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(embeddings, f, ensure_ascii=False)
    except Exception:
        pass
    
    return embeddings

def cosine_similarity(a, b):
    """Calcola la similarità coseno tra due vettori."""
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))

def search_parts_semantic(query: str, model: str = None, limit: int = 10):
    """
    Ricerca semantica dei ricambi usando embeddings.
    Supporta anche filtri per modello di macchina.
    """
    parts = load_parts()
    
    if not parts:
        return []
    
    try:
        query_embedding = get_embedding(query)
        embeddings = get_parts_embeddings()
    except Exception:
        # Fallback a ricerca lessicale se l'embedding fallisce
        return search_parts_lexical(query, model, limit)
    
    results = []
    
    for part in parts:
        # Filtro per modello se specificato
        if model and model.lower() not in part['compatibility'].lower():
            continue
        
        # Calcola similarità semantica
        code = part['code']
        if code in embeddings:
            similarity = cosine_similarity(
                query_embedding,
                embeddings[code]['embedding']
            )
        else:
            similarity = 0.0
        
        # Calcola anche match lessicale come bonus
        query_lower = query.lower()
        lexical_bonus = 0.0
        if query_lower in part['name'].lower():
            lexical_bonus = 0.1
        if query_lower in part['description'].lower():
            lexical_bonus = max(lexical_bonus, 0.05)
        
        relevance = min(1.0, similarity + lexical_bonus)  # Cap a 1.0
        
        if relevance > 0.1:  # Threshold minimo di rilevanza
            results.append({
                'name': part['name'],
                'code': part['code'],
                'compatibility': part['compatibility'],
                'description': part['description'],
                'rilevanza': round(relevance, 3)
            })
    
    # Ordina per rilevanza decrescente
    results.sort(key=lambda x: x['rilevanza'], reverse=True)
    
    return results[:limit]

def search_parts_lexical(query: str, model: str = None, limit: int = 10):
    """
    Ricerca lessicale come fallback quando embedding non disponibile.
    """
    parts = load_parts()
    results = []
    query_lower = query.lower()
    
    for part in parts:
        # Filtro per modello
        if model and model.lower() not in part['compatibility'].lower():
            continue
        
        # Calcola score lessicale
        score = 0.0
        if query_lower in part['name'].lower():
            score = 0.8
        if query_lower in part['description'].lower():
            score = max(score, 0.5)
        if query_lower in part['code'].lower():
            score = max(score, 0.6)
        
        if score > 0.0:
            results.append({
                'name': part['name'],
                'code': part['code'],
                'compatibility': part['compatibility'],
                'description': part['description'],
                'rilevanza': round(score, 3)
            })
    
    # Ordina per rilevanza
    results.sort(key=lambda x: x['rilevanza'], reverse=True)
    
    return results[:limit]

def search_parts(query: str = None, model: str = None, description: str = None, error: str = None, limit: int = 10):
    """
    Funzione di ricerca parts unificata che supporta sia query semantica che parametri specifici.
    """
    # Se non ci sono query, ritorna tutti i ricambi compatibili con il modello
    if not query and not description and not error:
        parts = load_parts()
        if model:
            parts = [p for p in parts if model.lower() in p['compatibility'].lower()]
        return [
            {
                'name': p['name'],
                'code': p['code'],
                'compatibility': p['compatibility'],
                'description': p['description'],
                'rilevanza': 1.0
            }
            for p in parts[:limit]
        ]
    
    # Costruisci query da parametri
    search_query_parts = []
    if query:
        search_query_parts.append(query)
    if description:
        search_query_parts.append(description)
    if error:
        search_query_parts.append(error)
    
    search_query = " ".join(search_query_parts)
    
    # Usa ricerca semantica
    return search_parts_semantic(search_query, model, limit)
