import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import UploadResponse, ChatRequest, ChatResponse, SearchPartsRequest, PartItem, TicketRequest, TroubleshootRequest, TroubleshootResponse
from .ingest import ingest_file
from .chat import answer_question
from .troubleshoot import analyze_troubleshoot
from .parts import search_parts as search_parts_semantic
from .audit import (
    append_ticket_log, load_logs, stats_top_problems, stats_top_machines,
    stats_troubleshoot_urgency, stats_troubleshoot_confidence, 
    stats_chat_confidence, get_recent_activity
)
import shutil
from .utils import ensure_dirs
import csv

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(BASE_DIR, 'data')
MANUALS_DIR = os.path.join(DATA_DIR, 'manuals')
PARTS_FILE = os.path.join(DATA_DIR, 'parts', 'sample_parts.csv')
ensure_dirs(MANUALS_DIR)

app = FastAPI(title="DM Packaging AI Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_api_key(x_api_key: str = Header(None)):
    """Dependency per verificare API key."""
    expected = os.environ.get('ADMIN_API_KEY')
    if not expected or x_api_key != expected:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return True


@app.post('/upload', response_model=UploadResponse)
async def upload_manual(file: UploadFile = File(...), api_key: str = Depends(verify_api_key)):
    """Upload manuale tecnico in formato PDF o TXT."""
    # Accetta sia PDF che TXT per flessibilità
    if file.filename.lower().endswith(('.pdf', '.txt')):
        dest = os.path.join(MANUALS_DIR, file.filename)
        with open(dest, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        # ingest file
        res = ingest_file(dest)
        return {"filename": file.filename, "status": "ingested", "chunks_count": res.get('chunks', 0)}
    else:
        raise HTTPException(status_code=400, detail='Solo PDF e TXT supportati')


@app.post('/chat')
async def chat_endpoint(req: ChatRequest):
    out = answer_question(req.question)
    return out


@app.post('/troubleshoot', response_model=TroubleshootResponse)
async def troubleshoot_endpoint(req: TroubleshootRequest):
    """
    Analizza problemi di macchina usando RAG.
    Input: modello_macchina e sintomo
    Output: cause possibili, azioni consigliate, ricambi probabili, urgenza
    """
    result = analyze_troubleshoot(req.modello_macchina, req.sintomo)
    return result


@app.post('/search-parts')
async def search_parts(req: SearchPartsRequest):
    """
    Ricerca ricambi con supporto semantico e ranking per rilevanza.
    Restituisce risultati ordinati per rilevanza (0-1).
    """
    # Costruisci query di ricerca
    query_parts = []
    if req.error:
        query_parts.append(req.error)
    if req.description:
        query_parts.append(req.description)
    
    search_query = " ".join(query_parts) if query_parts else None
    
    # Usa ricerca semantica migliorata
    results = search_parts_semantic(
        query=search_query,
        model=req.model,
        limit=20
    )
    
    return results


@app.post('/tickets')
async def create_ticket(req: TicketRequest):
    # build a simple structured ticket
    ticket = {
        'machine': req.machine,
        'problem': req.problem,
        'urgency': req.urgency,
        'suggested_solution': 'Verificare manuale e contattare tecnico; possibile ricambio: TBD'
    }
    try:
        append_ticket_log(ticket)
    except Exception:
        pass
    return {"ticket": ticket}


@app.get('/admin/logs')
async def admin_logs(kind: str = 'chats', api_key: str = Depends(verify_api_key)):
    items = load_logs(kind='chats' if kind=='chats' else 'tickets')
    return {"logs": items}


@app.get('/admin/stats')
async def admin_stats(api_key: str = Depends(verify_api_key)):
    top_problems = stats_top_problems()
    top_machines = stats_top_machines()
    return {
        "top_problems": top_problems,
        "top_machines": top_machines
    }


@app.get('/admin/dashboard')
async def admin_dashboard(api_key: str = Depends(verify_api_key)):
    """
    Dashboard completa con statistiche dettagliate per supporto tecnico.
    Mostra: top problemi, top macchine, distribuzioni urgenza/confidenza, attività recente.
    """
    return {
        "top_problems": stats_top_problems(limit=10),
        "top_machines": stats_top_machines(limit=10),
        "troubleshoot_urgency": stats_troubleshoot_urgency(),
        "troubleshoot_confidence": stats_troubleshoot_confidence(),
        "chat_confidence": stats_chat_confidence(),
        "recent_activity": get_recent_activity(hours=24, limit=20)
    }


@app.get('/admin/activity')
async def admin_activity(hours: int = 24, limit: int = 50, api_key: str = Depends(verify_api_key)):
    """
    Attività recente del sistema (chat e troubleshoot).
    """
    return {
        "activity": get_recent_activity(hours=hours, limit=limit)
    }
