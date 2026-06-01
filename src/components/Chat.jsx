import React, { useState } from 'react'

const sampleResponse = {
  problema: 'Macchina non avvia il ciclo di confezionamento',
  analisi: 'Il sistema ha rilevato un blocco nel motore di trasporto e una possibile anomalia nel sensore di pressione.',
  causa: 'Il sensore di pressione potrebbe essere sporco o installato in modo errato, causando un falso stop.',
  soluzione: 'Controllare e pulire il sensore di pressione, verificare i collegamenti elettrici e riavviare la macchina.',
  confidenza: 'Alta',
}

function Chat() {
  const [query, setQuery] = useState('')
  const [answer, setAnswer] = useState(null)

  const handleSubmit = (event) => {
    event.preventDefault()
    if (!query) return

    setAnswer({
      ...sampleResponse,
      problema: query,
    })
    setQuery('')
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Chat Tecnica</h1>
        <p className="page-description">
          Scrivi il problema della macchina e ottieni una diagnosi tecnica in formato report.
        </p>
      </div>

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Descrivi il problema</label>
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="form-textarea"
              placeholder="Es. La linea X ferma all’avvio, compare un errore di pressione"
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Nuova richiesta
          </button>
        </form>
      </div>

      {answer && (
        <div className="chat-card">
          <div className="chat-card-label">Report tecnico</div>
          <div className="chat-card-section">
            <h4>Problema</h4>
            <p>{answer.problema}</p>
          </div>
          <div className="chat-card-section">
            <h4>Analisi</h4>
            <p>{answer.analisi}</p>
          </div>
          <div className="chat-card-section">
            <h4>Causa possibile</h4>
            <p>{answer.causa}</p>
          </div>
          <div className="chat-card-section">
            <h4>Soluzione</h4>
            <p>{answer.soluzione}</p>
          </div>
          <div className="chat-card-section">
            <h4>Confidenza</h4>
            <span className="confidence-badge confidence-high">{answer.confidenza}</span>
          </div>
        </div>
      )}
    </div>
  )
}

export default Chat
