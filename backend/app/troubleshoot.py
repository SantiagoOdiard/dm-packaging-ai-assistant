import os
import json
import openai
from .retrieval import retrieve
from .audit import append_troubleshoot_log

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def analyze_troubleshoot(modello_macchina: str, sintomo: str):
    """
    Analizza un problema di una macchina usando RAG.
    Restituisce cause possibili, azioni consigliate, ricambi probabili e urgenza.
    """
    
    # Recupera documenti rilevanti dal knowledge base
    search_query = f"Macchina {modello_macchina} {sintomo} errore problema manutenzione"
    docs = retrieve(search_query, k=5)
    
    if not docs:
        # Fallback per sintomi comuni senza documentazione
        return generate_generic_troubleshoot(modello_macchina, sintomo)
    
    # Prepara il contesto dai documenti
    context_texts = []
    sources = []
    for d in docs:
        t = d.get('text', '')
        s = d.get('source', '')
        context_texts.append(f"Source: {s}\n{t}")
        sources.append(s)
    
    system_prompt = (
        "Sei un esperto di manutenzione e troubleshooting per macchine di packaging DM. "
        "Devi analizzare il problema descritto usando SOLO le informazioni nei manuali forniti. "
        "Fornisci una risposta in formato JSON strutturato con:\n"
        "{\n"
        '  "cause_possibili": ["causa1", "causa2", ...],\n'
        '  "azioni_consigliate": ["azione1", "azione2", ...],\n'
        '  "ricambi_probabili": [{"nome": "...", "codice": "...", "compatibilità": "..."}],\n'
        '  "urgenza": "bassa|media|alta",\n'
        '  "livello_confidenza": "basso|medio|alto",\n'
        '  "dettagli": "spiegazione dettagliata del problema"\n'
        "}\n"
        "Se non trovi informazioni specifiche nei manuali, rispondi comunque in JSON "
        "ma usa 'livello_confidenza: basso' e spiega che le informazioni sono limitate."
    )
    
    user_prompt = (
        f"MACCHINA: {modello_macchina}\n"
        f"SINTOMO/PROBLEMA: {sintomo}\n\n"
        f"DOCUMENTAZIONE DISPONIBILE:\n"
        f"{chr(10).join(context_texts)}\n\n"
        f"Analizza il problema e fornisci la diagnosi in formato JSON."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=600,
            temperature=0.3  # Bassa temperatura per risultati più strutturati
        )
        response_text = resp["choices"][0]["message"]["content"].strip()
        
        # Parse JSON response
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # Se la risposta non è JSON valido, prova a estrarre il JSON
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start >= 0 and end > start:
                result = json.loads(response_text[start:end])
            else:
                result = generate_generic_troubleshoot(modello_macchina, sintomo)
        
        # Assicura che tutti i campi siano presenti
        result.setdefault('cause_possibili', [])
        result.setdefault('azioni_consigliate', [])
        result.setdefault('ricambi_probabili', [])
        result.setdefault('urgenza', 'media')
        result.setdefault('livello_confidenza', 'medio')
        result.setdefault('dettagli', '')
        
        # Log per analytics
        try:
            append_troubleshoot_log({
                "modello_macchina": modello_macchina,
                "sintomo": sintomo,
                "documenti_consultati": sources,
                "urgenza": result['urgenza'],
                "confidenza": result['livello_confidenza']
            })
        except Exception:
            pass
        
        return result
        
    except Exception as e:
        # Fallback se c'è errore
        return generate_generic_troubleshoot(modello_macchina, sintomo)


def generate_generic_troubleshoot(modello_macchina: str, sintomo: str):
    """
    Genera una risposta di troubleshooting generica quando non ci sono documenti disponibili.
    """
    return {
        "cause_possibili": [
            "Problema meccanico non diagnosticato",
            "Usura componenti",
            "Configurazione errata"
        ],
        "azioni_consigliate": [
            "Consultare il manuale tecnico della macchina",
            "Contattare il supporto tecnico DM",
            "Eseguire ispezione visiva dei componenti principali"
        ],
        "ricambi_probabili": [],
        "urgenza": "media",
        "livello_confidenza": "basso",
        "dettagli": f"Informazione specifica per '{modello_macchina}' e sintomo '{sintomo}' non presente nei manuali tecnici caricati. Contattare il supporto tecnico per una diagnosi accurata."
    }
