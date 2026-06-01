import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
LOGS_DIR = os.path.join(DATA_DIR, 'logs')
CHAT_LOG = os.path.join(LOGS_DIR, 'chats.jsonl')
TICKET_LOG = os.path.join(LOGS_DIR, 'tickets.jsonl')
TROUBLESHOOT_LOG = os.path.join(LOGS_DIR, 'troubleshoot.jsonl')

def ensure():
    os.makedirs(LOGS_DIR, exist_ok=True)

def append_chat_log(entry: dict):
    ensure()
    entry['timestamp'] = datetime.utcnow().isoformat()
    with open(CHAT_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

def append_ticket_log(entry: dict):
    ensure()
    entry['timestamp'] = datetime.utcnow().isoformat()
    with open(TICKET_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

def append_troubleshoot_log(entry: dict):
    ensure()
    entry['timestamp'] = datetime.utcnow().isoformat()
    with open(TROUBLESHOOT_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

def load_logs(kind='chats'):
    path = CHAT_LOG if kind=='chats' else TICKET_LOG
    items = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    items.append(json.loads(line))
                except Exception:
                    continue
    return items

def stats_top_problems(limit=10):
    tickets = load_logs(kind='tickets')
    counts = {}
    for t in tickets:
        p = t.get('problem','unknown')
        counts[p] = counts.get(p, 0) + 1
    items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    return [{'problem': k, 'count': v} for k, v in items]

def stats_top_machines(limit=10):
    """Top 10 macchine con più problemi riportati."""
    troubleshoot = []
    if os.path.exists(TROUBLESHOOT_LOG):
        with open(TROUBLESHOOT_LOG, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    troubleshoot.append(json.loads(line))
                except Exception:
                    continue
    
    counts = {}
    for t in troubleshoot:
        m = t.get('modello_macchina', 'unknown')
        counts[m] = counts.get(m, 0) + 1
    items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    return [{'machine_model': k, 'issues_count': v} for k, v in items]

def stats_troubleshoot_urgency():
    """Statistiche urgenza problemi."""
    troubleshoot = []
    if os.path.exists(TROUBLESHOOT_LOG):
        with open(TROUBLESHOOT_LOG, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    troubleshoot.append(json.loads(line))
                except Exception:
                    continue
    
    urgency_counts = {'bassa': 0, 'media': 0, 'alta': 0}
    for t in troubleshoot:
        u = t.get('urgenza', 'media')
        if u in urgency_counts:
            urgency_counts[u] += 1
    
    return urgency_counts

def stats_troubleshoot_confidence():
    """Statistiche confidenza risposte."""
    troubleshoot = []
    if os.path.exists(TROUBLESHOOT_LOG):
        with open(TROUBLESHOOT_LOG, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    troubleshoot.append(json.loads(line))
                except Exception:
                    continue
    
    confidence_counts = {'basso': 0, 'medio': 0, 'alto': 0}
    for t in troubleshoot:
        c = t.get('confidenza', 'medio')
        if c in confidence_counts:
            confidence_counts[c] += 1
    
    return confidence_counts

def stats_chat_confidence():
    """Statistiche confidenza risposte chat."""
    chats = load_logs(kind='chats')
    confidence_counts = {'basso': 0, 'medio': 0, 'alto': 0}
    
    for c in chats:
        conf = c.get('confidence', 'medio')
        if conf in confidence_counts:
            confidence_counts[conf] += 1
    
    return confidence_counts

def get_recent_activity(hours=24, limit=20):
    """Attività recente (ultimi N ore)."""
    from datetime import datetime, timedelta
    
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    activity = []
    
    # Carica chat logs
    chats = load_logs(kind='chats')
    for entry in chats:
        try:
            ts = datetime.fromisoformat(entry.get('timestamp', ''))
            if ts > cutoff_time:
                activity.append({
                    'type': 'chat',
                    'timestamp': entry['timestamp'],
                    'question': entry.get('question', '')[:50],
                    'confidence': entry.get('confidence', 'unknown')
                })
        except Exception:
            pass
    
    # Carica troubleshoot logs
    troubleshoot = []
    if os.path.exists(TROUBLESHOOT_LOG):
        with open(TROUBLESHOOT_LOG, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    troubleshoot.append(json.loads(line))
                except Exception:
                    continue
    
    for entry in troubleshoot:
        try:
            ts = datetime.fromisoformat(entry.get('timestamp', ''))
            if ts > cutoff_time:
                activity.append({
                    'type': 'troubleshoot',
                    'timestamp': entry['timestamp'],
                    'machine': entry.get('modello_macchina', 'unknown'),
                    'urgency': entry.get('urgenza', 'unknown')
                })
        except Exception:
            pass
    
    # Ordina per timestamp decrescente
    activity.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return activity[:limit]

