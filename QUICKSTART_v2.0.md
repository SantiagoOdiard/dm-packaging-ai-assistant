QUICK START - TEST NUOVE FEATURES v2.0
======================================

Guida rapida per testare i miglioramenti del sistema.

---

## SETUP INIZIALE

### 1. Start Backend
```bash
cd backend
python -m venv .venv
.\\.venv\\Scripts\\activate
pip install -r requirements.txt

# Set environment variables
set OPENAI_API_KEY=sk-xxx...
set ADMIN_API_KEY=demo123

uvicorn app.main:app --reload --port 8000
```

### 2. Caricare Manuale Tecnico

Usa Postman o curl per caricare il manuale:

```bash
curl -X POST http://localhost:8000/upload \
  -H "x-api-key: demo123" \
  -F "file=@backend/data/manuals/FLOWPACK_Manuale_Tecnico_2024.txt"
```

Risposta attesa:
```json
{
  "filename": "FLOWPACK_Manuale_Tecnico_2024.txt",
  "status": "ingested",
  "chunks_count": 45
}
```

---

## TEST NUOVE FEATURES

### 1. TROUBLESHOOTING ENDPOINT (MAIN FEATURE)

#### Scenario 1: Blocco Nastro Trasportatore
```bash
curl -X POST http://localhost:8000/troubleshoot \
  -H "Content-Type: application/json" \
  -d '{
    "modello_macchina": "FLOWPACK-1000",
    "sintomo": "Nastro trasportatore bloccato, macchina non si avvia"
  }'
```

**Risposta Attesa:**
- cause_possibili: ["Cinghia rotta", "Cuscinetti bloccati", "Motore difettoso"]
- azioni_consigliate: ["Ispezionare cinghia", "Verificare cuscinetti", "Testare motore"]
- ricambi_probabili: [{"nome": "Cinghia nastro", "codice": "CING-100", ...}]
- urgenza: "alta"
- livello_confidenza: "alto"

---

#### Scenario 2: Allarme Temperatura Saldatura
```bash
curl -X POST http://localhost:8000/troubleshoot \
  -H "Content-Type: application/json" \
  -d '{
    "modello_macchina": "FLOWPACK-2000",
    "sintomo": "Allarme sovraccarico termico bobina saldatura, temperatura oltre 240°C"
  }'
```

**Risposta Attesa:**
- cause_possibili: ["Sensore temperatura difettoso", "Bobina danneggiata", "Ventilazione insufficiente"]
- ricambi_probabili: [SENS-TEMP, BOB-SALD-1]
- urgenza: "alta"

---

#### Scenario 3: Perdita Pressione Pneumatica
```bash
curl -X POST http://localhost:8000/troubleshoot \
  -H "Content-Type: application/json" \
  -d '{
    "modello_macchina": "FLOWPACK-2000",
    "sintomo": "Pressione pneumatica cala rapidamente, cilindri non spingono"
  }'
```

**Risposta Attesa:**
- cause_possibili: ["Tubi danneggiati", "Connessioni allentate", "Guarnizioni usurate"]
- ricambi_probabili: [GUARD-VITON-30, VALV-SOL-24]
- urgenza: "media"

---

### 2. CHAT MIGLIORATO (STRUCTURED RAG)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Come devo controllare la temperatura della saldatura su FLOWPACK-2000?"
  }'
```

**Risposta con Struttura:**
```json
{
  "answer": "Risposta dettagliata...",
  "problem_analyzed": "Monitoraggio temperatura saldatura",
  "possible_cause": "Sensore temperatura (SENS-TEMP) legge in tempo reale",
  "recommended_solution": "Consultare menu diagnostico...",
  "confidence_level": "alto",
  "sources": ["FLOWPACK_Manuale_Tecnico_2024.txt"]
}
```

---

### 3. SEARCH PARTS SEMANTICA

#### Esempio 1: Ricerca per Sintomo
```bash
curl -X POST http://localhost:8000/search-parts \
  -H "Content-Type: application/json" \
  -d '{
    "error": "Sensore temperatura non risponde",
    "model": "FLOWPACK-2000"
  }'
```

**Risposta con Rilevanza:**
```json
[
  {
    "name": "Sensore temperatura",
    "code": "SENS-TEMP",
    "compatibility": "FLOWPACK-2000;FLOWPACK-3000",
    "description": "Sensore NTC per monitoraggio temperatura saldatura",
    "rilevanza": 0.965
  },
  {
    "name": "Trasformatore 220/24V",
    "code": "TRASF-500W",
    "rilevanza": 0.412
  }
]
```

#### Esempio 2: Ricerca per Descrizione
```bash
curl -X POST http://localhost:8000/search-parts \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Cinghia nastro usura",
    "model": "FLOWPACK-1000"
  }'
```

---

### 4. DASHBOARD ADMIN

```bash
curl -X GET "http://localhost:8000/admin/dashboard" \
  -H "x-api-key: demo123"
```

**Risposta:**
```json
{
  "top_problems": [
    {"problem": "Sensore non riconosciuto", "count": 5},
    {"problem": "Perdita pressione", "count": 3}
  ],
  "top_machines": [
    {"machine_model": "FLOWPACK-2000", "issues_count": 12},
    {"machine_model": "FLOWPACK-1000", "issues_count": 8}
  ],
  "troubleshoot_urgency": {
    "bassa": 3,
    "media": 7,
    "alta": 2
  },
  "troubleshoot_confidence": {
    "basso": 1,
    "medio": 5,
    "alto": 6
  },
  "chat_confidence": {
    "basso": 0,
    "medio": 3,
    "alto": 8
  },
  "recent_activity": [
    {
      "type": "troubleshoot",
      "timestamp": "2026-05-31T15:30:45.123456",
      "machine": "FLOWPACK-2000",
      "urgency": "alta"
    }
  ]
}
```

---

### 5. ACTIVITY LOG

```bash
curl -X GET "http://localhost:8000/admin/activity?hours=24&limit=10" \
  -H "x-api-key: demo123"
```

---

## TESTING CHECKLIST

- [ ] Upload manuale completato con N chunks
- [ ] POST /troubleshoot restituisce urgenza + confidenza
- [ ] POST /chat restituisce struttura with confidence_level
- [ ] POST /search-parts restituisce risultati con rilevanza ordinata
- [ ] GET /admin/dashboard ritorna statistiche complete
- [ ] GET /admin/activity mostra attività recente
- [ ] Troubleshoot log è creato in data/logs/troubleshoot.jsonl
- [ ] Chat log contiene confidence_level
- [ ] Admin può vedere top_machines in /admin/stats

---

## INTEGRATION NOTES

### Per Frontend React
- Endpoint `/troubleshoot` - Display urgenza + confidenza in UI
- Endpoint `/search-parts` - Ordina per rilevanza, mostra score
- Endpoint `/admin/dashboard` - New dashboard con grafici
- ChatResponse estesa - Mostra problem_analyzed, confidence_level

### Per Database/Storage
- FAISS index creato al primo upload (backend/data/faiss_index.idx)
- Documenti salvati in JSONL (backend/data/docs.jsonl)
- Log ricerca ricambi in JSON cache (backend/data/parts_embeddings.json)
- Audit log in backend/data/logs/*.jsonl

### Per Monitoring
- Check troubleshoot.jsonl per analytics urgenza/confidenza
- Check chats.jsonl per tracking quality
- Query /admin/dashboard per metriche real-time

---

## TROUBLESHOOTING

### Errore: "OPENAI_API_KEY not set"
Verificare che la variabile di ambiente sia impostata.

### Errore: "faiss not installed"
Il file ingest.py fallisce se FAISS non trovato. Comunque continua.

### Embedding cache non trovato
Al primo uso, gli embeddings per parts.py vengono calcolati.
Questo richiede chiama API OpenAI (costo $).

### Manuale non indicizzato
Verificare che il caricamento via POST /upload sia completato
e che il file sia in formato .txt o .pdf

---

Fine Quick Start Guide.
