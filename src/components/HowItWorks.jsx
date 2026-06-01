import React from 'react'

const steps = [
  {
    title: 'Carica i manuali PDF delle macchine',
    description: 'Aggiungi i documenti tecnici delle linee e tienili sempre aggiornati nel sistema.',
  },
  {
    title: 'Fai domande nella Chat Tecnica',
    description: 'Chiedi subito informazioni sulle macchine, sui sensori e sulle procedure di manutenzione.',
  },
  {
    title: 'Usa Troubleshooting per problemi macchina',
    description: 'Descrivi il sintomo e ricevi cause possibili, azioni consigliate e priorità.',
  },
  {
    title: 'Cerca ricambi direttamente',
    description: 'Trova codici parti, descrizioni e rilevanza con un solo click.',
  },
  {
    title: 'Genera ticket automatici',
    description: 'Registra le richieste di intervento o apri un ticket ai tecnici direttamente dall’interfaccia.',
  },
]

function HowItWorks({ onNavigate }) {
  return (
    <div className="page-container how-it-works-container">
      <div className="page-header">
        <h1 className="page-title">Come si usa</h1>
        <p className="page-description">
          Segui il flusso rapido per ottenere supporto tecnico senza perdere tempo.
        </p>
      </div>

      <div className="steps-grid">
        {steps.map((step, index) => (
          <div key={step.title} className="step-card">
            <div className="step-number">{index + 1}</div>
            <div className="step-content">
              <h3>{step.title}</h3>
              <p>{step.description}</p>
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        <button className="btn btn-primary" onClick={() => onNavigate('chat')}>
          Vai a Chat Tecnica
        </button>
        <button className="btn btn-secondary" onClick={() => onNavigate('troubleshoot')}>
          Vai a Troubleshooting
        </button>
      </div>
    </div>
  )
}

export default HowItWorks
