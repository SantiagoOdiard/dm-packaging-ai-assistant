import React from 'react'

function Home({ onNavigate }) {
  return (
    <div className="page-container">
      <section className="home-hero">
        <div className="page-header">
          <h1 className="home-hero-title">DM Packaging AI Assistant</h1>
          <p className="home-hero-subtitle">
            Sistema intelligente per supporto tecnico e gestione macchine industriali.
            Tutti i tool in un unico spazio per i tecnici di manutenzione.
          </p>
        </div>

        <div className="home-cta-buttons">
          <button className="btn btn-primary btn-large" onClick={() => onNavigate('chat')}>
            Inizia Chat
          </button>
          <button className="btn btn-secondary btn-large" onClick={() => onNavigate('admin')}>
            Carica Manuali
          </button>
          <button className="btn btn-outline btn-large" onClick={() => onNavigate('how-it-works')}>
            Come si usa
          </button>
        </div>
      </section>

      <div className="home-features">
        <div className="card feature-card">
          <div className="feature-icon">🛠️</div>
          <div className="feature-title">Supporto tecnico rapido</div>
          <div className="feature-description">
            Fai domande sui manuali, sulla manutenzione e sui componenti in modo semplice.
          </div>
        </div>
        <div className="card feature-card">
          <div className="feature-icon">📄</div>
          <div className="feature-title">Documentazione sempre a portata</div>
          <div className="feature-description">
            Carica manuali macchina e ottieni risposte contestuali dai tuoi documenti.
          </div>
        </div>
        <div className="card feature-card">
          <div className="feature-icon">⚙️</div>
          <div className="feature-title">Ricambi e troubleshooting</div>
          <div className="feature-description">
            Identifica cause, azioni consigliate e parti da sostituire con un’interfaccia tecnica chiara.
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
