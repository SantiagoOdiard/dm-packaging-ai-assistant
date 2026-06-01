import React from 'react'

function OnboardingModal({ onStart, onNavigate }) {
  return (
    <div className="onboarding-overlay">
      <div className="onboarding-modal">
        <h2 className="onboarding-title">Benvenuto in DM Packaging AI Assistant</h2>
        <p className="onboarding-description">
          Il tuo spazio per assistenza tecnica, troubleshooting e gestione ricambi in ambiente industriale.
        </p>
        <div className="onboarding-buttons">
          <button className="btn btn-primary" onClick={() => { onStart(); }}>
            Inizia subito
          </button>
          <button className="btn btn-secondary" onClick={() => { onNavigate('admin'); onStart(); }}>
            Carica manuali
          </button>
          <button className="btn btn-outline" onClick={() => { onNavigate('how-it-works'); onStart(); }}>
            Vedi guida
          </button>
        </div>
      </div>
    </div>
  )
}

export default OnboardingModal
