import React, { useState } from 'react'

function Troubleshoot() {
  const [machine, setMachine] = useState('')
  const [symptom, setSymptom] = useState('')
  const [result, setResult] = useState(null)

  const handleSubmit = (event) => {
    event.preventDefault()
    if (!machine || !symptom) return
    setResult({
      cause: ['Sensore bloccato', 'Bassa pressione nel circuito', 'Usura del componente'],
      actions: ['Verificare il cablaggio del sensore', 'Controllare le linee aria', 'Pulire il filtro del circuito'],
      parts: ['PN-1024 - Sensore pressione', 'PN-1250 - Filtro aria'],
      urgency: 'Media',
    })
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Troubleshooting</h1>
        <p className="page-description">
          Inserisci modello macchina e sintomo per ottenere un report tecnico rapido.
        </p>
      </div>

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Modello macchina</label>
            <input
              type="text"
              value={machine}
              onChange={(e) => setMachine(e.target.value)}
              className="form-input"
              placeholder="Es. FLOWPACK-1000"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Sintomo</label>
            <textarea
              value={symptom}
              onChange={(e) => setSymptom(e.target.value)}
              className="form-textarea"
              placeholder="Es. La macchina si blocca durante il riempimento"
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Nuova richiesta
          </button>
        </form>
      </div>

      {result && (
        <div className="troubleshoot-card">
          <div className="chat-card-label">Risultato troubleshooting</div>
          <div className="chat-card-section">
            <h4>Cause possibili</h4>
            <ul>
              {result.cause.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
          <div className="chat-card-section">
            <h4>Azioni consigliate</h4>
            <ul>
              {result.actions.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
          <div className="chat-card-section">
            <h4>Ricambi probabili</h4>
            <ul>
              {result.parts.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
          <div className="chat-card-section">
            <h4>Urgenza</h4>
            <span className={`urgency-badge urgency-${result.urgency.toLowerCase()}`}>{result.urgency}</span>
          </div>
        </div>
      )}
    </div>
  )
}

export default Troubleshoot
