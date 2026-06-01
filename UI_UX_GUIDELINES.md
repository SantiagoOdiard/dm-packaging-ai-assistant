UI/UX RECOMMENDATIONS - INDUSTRIAL INTERFACE
===============================================

Questo documento fornisce linee guida per renderizzare l'interfaccia React 
più industriale (per future implementazioni frontend).

---

## STILE VISIVO

### Palette Colori
- **Primario**: Blu scuro (#1E3A5F) - Trust, professionalità
- **Secondario**: Grigio (#4A5568) - Neutro, moderno
- **Accenti**: Arancione (#FF6B35) - Urgenza alta
- **Success**: Verde (#27AE60) - Problema risolto
- **Warning**: Giallo (#F39C12) - Urgenza media
- **Info**: Celeste (#3498DB) - Informazione

### Font
- Titoli: Inter Bold 24px / 20px
- Body: Roboto Regular 14px
- Monospace: Courier New 12px (per codici ricambi)

### Layout
- Minimal, grid-based (12 colonne)
- Densità media (non troppo spazi)
- Dark mode friendly

---

## PAGINE PRINCIPALI

### 1. CHAT TECNICA
**URL:** `/chat`

Layout: 2 colonne
```
┌─────────────────────────────────────────┐
│  Chat Tecnica - DM Packaging Assistant  │
├──────────────────┬──────────────────────┤
│                  │                      │
│ Input:           │   Cronologia Risposte
│ [Domanda...] [→] │   ┌────────────────┐
│                  │   │ Problem:       │
│ Machine Model:   │   │ Saldatura      │
│ [FLOWPACK-1000]  │   │                │
│                  │   │ Cause:         │
│                  │   │ Temperatura    │
│                  │   │ bassa          │
│                  │   │                │
│                  │   │ Solution:      │
│                  │   │ Controllare... │
│                  │   │                │
│                  │   │ [HIGH]         │
│                  │   │ Confidenza: 85%│
│                  │   │ Fonti: manual1 │
│                  │   └────────────────┘
└──────────────────┴──────────────────────┘
```

**Card Risposta - Struttura:**
```
┌────────────────────────────────┐
│ PROBLEMA ANALIZZATO            │
│ Saldatura non raggiunge temp.  │
├────────────────────────────────┤
│ ⚠️ CAUSA PROBABILE             │
│ Sensore temp. difettoso        │
├────────────────────────────────┤
│ ✓ SOLUZIONE CONSIGLIATA        │
│ 1. Verificare sensore SENS-TEMP
│ 2. Controllare cavi            │
│ 3. Se non funziona, sostituire │
├────────────────────────────────┤
│ Confidenza: ALTO ■■■■■         │
│ Fonte: FLOWPACK_Manual_2024    │
└────────────────────────────────┘
```

---

### 2. TROUBLESHOOTING (MAIN FEATURE)
**URL:** `/troubleshoot`

Layout: Form + Result
```
┌──────────────────────────────────────┐
│  🔧 MODALITÀ TROUBLESHOOTING          │
├──────────────────────────────────────┤
│                                      │
│  Seleziona Macchina:                 │
│  [FLOWPACK-1000 ▼]  [FLOWPACK-2000] │
│  [FLOWPACK-3000]                    │
│                                      │
│  Descrivi Sintomo (problema):        │
│  ┌────────────────────────────────┐ │
│  │ Es: Macchina non avvia,        │ │
│  │ nessuna alimentazione 220V     │ │
│  │                                │ │
│  │                                │ │
│  └────────────────────────────────┘ │
│                [ANALIZZA] (oppure)   │
│  [DOMANDA AL SUPPORTO]              │
│                                      │
└──────────────────────────────────────┘

RISULTATO:
┌─────────────────────────────────────┐
│ 🔴 URGENZA: ALTA                     │
├─────────────────────────────────────┤
│                                     │
│ CAUSE POSSIBILI:                   │
│ □ Nessuna alimentazione 220V       │
│ □ Fusibile saltato (FUSI-10A)      │
│ □ Relè temporizzato difettoso      │
│                                     │
│ AZIONI CONSIGLIATE:                │
│ 1. Verificare presa di corrente    │
│ 2. Controllare fusibile            │
│ 3. Testare relè con multimetro     │
│                                     │
│ RICAMBI PROBABILI:                 │
│ • Fusibile 10A [FUSI-10A] - Stock  │
│ • Relè 24VDC [RELE-TIME-24] - 3gg │
│                                     │
│ Confidenza: MEDIO ■■■□□             │
│ Consulta anche: Cap. 4 del Manuale │
│                                     │
│ [CREA TICKET] [CONTATTA SUPPORTO]  │
└─────────────────────────────────────┘
```

---

### 3. RICERCA RICAMBI
**URL:** `/parts`

Layout: Search + Grid Results
```
┌─────────────────────────────────────┐
│  🔍 RICERCA RICAMBI                  │
├─────────────────────────────────────┤
│                                     │
│ Filtri:                            │
│ Macchina: [FLOWPACK-2000 ▼]       │
│ Descrizione: [Sensore temp.]      │
│ Errore: [Non risponde]            │
│                                     │
│                [CERCA]             │
│                                     │
│ Risultati: 7 ricambi trovati       │
├─────────────────────────────────────┤
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ SENSORE TEMPERATURA             │ │
│ │ Cod: SENS-TEMP                  │ │
│ │ Compatibilità: FLOWPACK-2000/3K │ │
│ │ "Sensore NTC per monitoraggio.."│ │
│ │ Rilevanza: ████████░░ 96%       │ │
│ │                    [DETTAGLI]   │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ TRASFORMATORE 220/24V           │ │
│ │ Cod: TRASF-500W                 │ │
│ │ Compatibilità: ALL              │ │
│ │ Rilevanza: ████░░░░░░ 41%       │ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

**Card Ricambio Dettagliato:**
```
┌─────────────────────────────────┐
│ Sensore Temperatura [SENS-TEMP] │
├─────────────────────────────────┤
│ • Modello: NTC                  │
│ • Temp Range: -50 to +100°C     │
│ • Output: 4-20mA                │
│ • Compatibile: FLOWPACK-2000,   │
│             FLOWPACK-3000       │
│                                 │
│ Disponibilità: 🟢 IN STOCK      │
│ Prezzo indicativo: €145         │
│ Lead Time: Immediato            │
│                                 │
│ [AGGIUNGI A TICKET]             │
│ [CONTATTA FORNITORE]            │
└─────────────────────────────────┘
```

---

### 4. UPLOAD MANUALE
**URL:** `/admin/upload`

Layout: Drag & Drop + Progress
```
┌──────────────────────────────────────┐
│  📤 CARICA MANUALE TECNICO            │
├──────────────────────────────────────┤
│                                      │
│  ┌────────────────────────────────┐ │
│  │                                │ │
│  │   Trascina file qui oppure     │ │
│  │         [SFOGLIA]              │ │
│  │                                │ │
│  │  Formati supportati: PDF, TXT  │ │
│  │                                │ │
│  └────────────────────────────────┘ │
│                                      │
│ Ultimo caricamento:                  │
│ ✓ FLOWPACK_Manuale_Tecnico_2024.txt │
│   Caricato: 31/05/2026 14:32        │
│   Stato: Indicizzazione completata  │
│   Chunk: 45 documenti / 120 KB      │
│   Qualità indice: ALTA ████████░    │
│                                      │
│ Macchine indicizzate:                │
│ ✓ FLOWPACK-1000, FLOWPACK-2000       │
│ ✓ FLOWPACK-3000                      │
│                                      │
└──────────────────────────────────────┘
```

---

### 5. ADMIN DASHBOARD
**URL:** `/admin/dashboard`

Layout: 4 quadranti + grafici
```
┌──────────────────────────────────────────────────┐
│  📊 DASHBOARD SUPPORTO TECNICO                    │
├──────────────────────────────────────────────────┤
│                                                  │
│ ┌────────────────┐  ┌────────────────┐         │
│ │ TOP PROBLEMI   │  │ TOP MACCHINE   │         │
│ │────────────────│  │────────────────│         │
│ │ 1. Sensore     │  │ 1. FLOWPACK-   │         │
│ │    non ris: 12 │  │    2000: 34    │         │
│ │ 2. Perdita     │  │ 2. FLOWPACK-   │         │
│ │    pressione: 8│  │    1000: 21    │         │
│ │ 3. Temp alta: 6│  │ 3. FLOWPACK-   │         │
│ │ 4. Motore: 4   │  │    3000: 15    │         │
│ └────────────────┘  └────────────────┘         │
│                                                  │
│ ┌────────────────┐  ┌────────────────┐         │
│ │ URGENZA        │  │ CONFIDENZA     │         │
│ │ PROBLEMI       │  │ RISPOSTE       │         │
│ │────────────────│  │────────────────│         │
│ │ 🔴 Alta:    6  │  │ ✓ Alto:  25   │         │
│ │ 🟡 Media:   14 │  │ ~ Medio: 12   │         │
│ │ 🟢 Bassa:   4  │  │ ✗ Basso:  2   │         │
│ │                │  │                │         │
│ │ [DETTAGLI]     │  │ [DETTAGLI]     │         │
│ └────────────────┘  └────────────────┘         │
│                                                  │
├──────────────────────────────────────────────────┤
│ ATTIVITÀ RECENTE (ultimi 24 ore)                 │
├──────────────────────────────────────────────────┤
│                                                  │
│ 🔧 14:32 | Troubleshoot | FLOWPACK-2000 | ALTA │
│ 💬 14:28 | Chat Tecnica | Temp. saldatura      │
│ 🔧 14:15 | Troubleshoot | FLOWPACK-1000 | MED  │
│ 💬 13:50 | Chat Tecnica | Sensore ottico       │
│ 🛠️  13:22 | Upload Manual | 45 chunk caricati  │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## COMPONENTI REUSABILI

### Button Style
```
Primary:   [ANALIZZA] - Blue #1E3A5F
Secondary: [DETTAGLI] - Gray #4A5568
Danger:    [ELIMINA]  - Red #E74C3C
Success:   [RISOLTO]  - Green #27AE60
```

### Alert/Status
```
🔴 ALTA      - Red alert
🟡 MEDIA     - Yellow warning
🟢 BASSA     - Green info
🔵 INFO      - Blue info
```

### Loading States
```
Indicizzazione... ⟳
Caricamento: ████░░░░░░ 40%
Processing... ○○○○○ (5 dots)
```

### Responsive Design
- Mobile (<768px): Stack verticale, tab menu
- Tablet (768-1024px): 2 colonne
- Desktop (>1024px): 3 colonne + sidebar

---

## ACCESSIBILITÀ

✓ Contrasto colori WCAG AA minimo
✓ Icone + etichette testuali
✓ Keyboard navigation support
✓ Screen reader friendly
✓ Form labels espliciti
✓ Error messages chiari

---

## PERFORMANCE

✓ Chat lazy-load conversation history
✓ Dashboard data refresh ogni 5 min
✓ Parts search debounce 300ms
✓ Image optimize (if any)
✓ API calls cache where possible

---

Fine UI/UX Guidelines.
