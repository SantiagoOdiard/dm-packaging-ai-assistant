from pydantic import BaseModel
from typing import List, Optional, Literal

class UploadResponse(BaseModel):
    filename: str
    status: str
    chunks_count: Optional[int] = None

class ChatRequest(BaseModel):
    question: str
    machine_model: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []
    # Struttura migliorata RAG
    problem_analyzed: Optional[str] = None
    possible_cause: Optional[str] = None
    recommended_solution: Optional[str] = None
    confidence_level: Optional[Literal["basso", "medio", "alto"]] = "medio"

class SearchPartsRequest(BaseModel):
    model: Optional[str] = None
    description: Optional[str] = None
    error: Optional[str] = None

class PartItem(BaseModel):
    name: str
    code: str
    compatibility: str
    description: str
    rilevanza: Optional[float] = 1.0  # 0-1 relevance score

class TicketRequest(BaseModel):
    machine: str
    problem: str
    urgency: Optional[str] = "medium"

class TicketResponse(BaseModel):
    ticket: dict

# Modelli per Troubleshooting (NUOVA FEATURE)
class TroubleshootRequest(BaseModel):
    modello_macchina: str
    sintomo: str

class TroubleshootResponse(BaseModel):
    cause_possibili: List[str]
    azioni_consigliate: List[str]
    ricambi_probabili: List[dict]  # [{"nome": "", "codice": "", "compatibilità": ""}]
    urgenza: Literal["bassa", "media", "alta"]
    documenti_consultati: List[str] = []
    livello_confidenza: Literal["basso", "medio", "alto"] = "medio"