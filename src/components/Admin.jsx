import React, { useState } from 'react'

function Admin() {
  const [file, setFile] = useState(null)
  const [apiKey, setApiKey] = useState('')
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!file) {
      setStatus({ type: 'error', message: 'Seleziona un file PDF o TXT prima di inviare.' })
      return
    }
    if (!apiKey) {
      setStatus({ type: 'error', message: 'Inserisci la tua API key di amministrazione.' })
      return
    }

    setLoading(true)
    setStatus(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        headers: {
          'x-api-key': apiKey,
        },
        body: formData,
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Errore durante l\'upload')
      }

      const result = await response.json()
      setStatus({ type: 'success', message: `File caricato: ${result.filename} (chunks: ${result.chunks_count})` })
      setFile(null)
    } catch (error) {
      setStatus({ type: 'error', message: error.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Admin</h1>
        <p className="page-description">
          Usa questa sezione per caricare manuali, controllare lo stato dei documenti e gestire i dati tecnici.
        </p>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="card-title">Caricamento manuali</div>
        </div>
        <div className="card-content">
          <p>
            Qui puoi inviare nuovi manuali e aggiornare la base documentale. Il backend gestisce il caricamento e la generazione degli embeddings.
          </p>
          <form onSubmit={handleSubmit} style={{ marginTop: '1.5rem' }}>
            <div className="form-group">
              <label className="form-label">API Key amministratore</label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                className="form-input"
                placeholder="Inserisci la tua API key"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Seleziona file PDF o TXT</label>
              <input
                type="file"
                accept=".pdf,.txt"
                onChange={(e) => setFile(e.target.files[0] || null)}
                className="form-input"
              />
            </div>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Caricamento...' : 'Carica file'}
            </button>
          </form>

          {status && (
            <div className={`upload-status ${status.type === 'error' ? 'status-error' : 'status-success'}`}>
              {status.message}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Admin
