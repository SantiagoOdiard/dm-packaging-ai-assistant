import os
import json
import openai
from .retrieval import retrieve
from .audit import append_chat_log

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def answer_question(question: str):
    docs = retrieve(question, k=4)
    
    # Se nessun documento trovato, ritorna risposta predefinita
    if not docs:
        return {
            "answer": "Informazione non presente nei manuali tecnici caricati.",
            "sources": [],
            "problem_analyzed": "Nessun documento pertinente trovato",
            "possible_cause": None,
            "recommended_solution": None,
            "confidence_level": "basso"
        }

    # Build context
    context_texts = []
    sources = []
    for d in docs:
        t = d.get('text','')
        s = d.get('source','')
        context_texts.append(f"Source: {s}\n{t}")
        sources.append(s)

    # Sistema prompt migliore per struttura RAG
    system = (
        "Sei un assistente tecnico esperto in macchine di packaging DM. "
        "Rispondi SOLO usando le informazioni fornite nei manuali tecnici. "
        "Struttura la risposta in format JSON con i seguenti campi:\n"
        "{\n"
        '  "problem_analyzed": "descrizione del problema analizzato",\n'
        '  "possible_cause": "causa più probabile basata sulla documentazione",\n'
        '  "recommended_solution": "soluzione consigliata passo per passo",\n'
        '  "confidence_level": "basso|medio|alto",\n'
        '  "answer": "risposta completa in formato leggibile",\n'
        '  "sources": ["elenco delle fonti usate"]\n'
        "}\n"
        "Se l'informazione non è nei manuali, usa confidence_level: 'basso' e indica chiaramente che l'informazione è limitata."
    )
    prompt = (
        f"Documentazione disponibile:\n{chr(10).join(context_texts)}\n\n"
        f"Domanda tecnica dell'utente: {question}\n\n"
        f"Fornisci la risposta in formato JSON strutturato."
    )

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=600,
            temperature=0.2  # Bassa temperatura per risposte strutturate
        )
        response_text = resp["choices"][0]["message"]["content"].strip()
        
        # Parse JSON response
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback se JSON non valido: estrai il blocco JSON
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start >= 0 and end > start:
                result = json.loads(response_text[start:end])
            else:
                result = {
                    "problem_analyzed": "Analisi incompleta",
                    "possible_cause": None,
                    "recommended_solution": response_text,
                    "confidence_level": "basso",
                    "answer": response_text,
                    "sources": sources
                }
        
        # Assicura che tutti i campi obbligatori siano presenti
        result.setdefault('answer', '')
        result.setdefault('sources', sources)
        result.setdefault('problem_analyzed', 'Problema analizzato')
        result.setdefault('possible_cause', None)
        result.setdefault('recommended_solution', None)
        result.setdefault('confidence_level', 'medio')
        
        # Log per analytics
        try:
            append_chat_log({
                "question": question,
                "answer": result.get('answer', ''),
                "sources": sources,
                "confidence": result.get('confidence_level', 'medio')
            })
        except Exception:
            pass
        
        return result
        
    except Exception as e:
        # Fallback per errori API
        return {
            "answer": "Errore nel recupero della risposta. Contattare il supporto.",
            "sources": sources,
            "problem_analyzed": "Errore di sistema",
            "possible_cause": None,
            "recommended_solution": None,
            "confidence_level": "basso"
        }

