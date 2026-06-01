import React, { useState } from 'react'

const initialParts = [
  { code: 'PN-1024', name: 'Sensore pressione', description: 'Sensore per controllo pressione di linea', category: 'Sensori', location: 'Linea A', relevance: 0.92 },
  { code: 'PN-1250', name: 'Filtro aria', description: 'Filtro aria per circuito pneumatico', category: 'Pneumatica', location: 'Magazzino 1', relevance: 0.86 },
  { code: 'PN-1337', name: 'Tenuta meccanica', description: 'Tenuta per albero motore', category: 'Meccanica', location: 'Magazzino 2', relevance: 0.78 },
]

function Parts() {
  const [query, setQuery] = useState('')
  const [parts, setParts] = useState(initialParts)
  const [filteredParts, setFilteredParts] = useState(initialParts)
  const [newPart, setNewPart] = useState({ code: '', name: '', description: '', category: '', location: '', relevance: 80 })
  const [message, setMessage] = useState(null)

  const handleSearch = (event) => {
    event.preventDefault()
    const normalizedQuery = query.trim().toLowerCase()
    if (!normalizedQuery) {
      setFilteredParts(parts)
      return
    }
    const filtered = parts.filter((part) =>
      part.name.toLowerCase().includes(normalizedQuery) ||
      part.code.toLowerCase().includes(normalizedQuery) ||
      part.description.toLowerCase().includes(normalizedQuery)
    )
    setFilteredParts(filtered)
  }

  const handleInputChange = (field, value) => {
    setNewPart((current) => ({ ...current, [field]: value }))
  }

  const handleAddPart = (event) => {
    event.preventDefault()
    if (!newPart.code || !newPart.name || !newPart.description) {
      setMessage({ type: 'error', text: 'Completa almeno codice, nome e descrizione del ricambio.' })
      return
    }

    const addedPart = {
      ...newPart,
      relevance: Number(newPart.relevance) / 100,
    }

    setParts((current) => [addedPart, ...current])
    setFilteredParts((current) => [addedPart, ...current])
    setNewPart({ code: '', name: '', description: '', category: '', location: '', relevance: 80 })
    setMessage({ type: 'success', text: `Ricambio ${addedPart.code} aggiunto con successo.` })
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Ricambi</h1>
        <p className="page-description">
          Trova più velocemente i ricambi, aggiungi nuovi componenti e conserva tutti i dettagli del prodotto.
        </p>
      </div>

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <form onSubmit={handleSearch}>
          <div className="form-group">
            <label className="form-label">Cerca codice o nome ricambio</label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="form-input"
              placeholder="Es. Sensore pressione"
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Cerca ricambi
          </button>
        </form>
      </div>

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div className="card-header">
          <div className="card-title">Aggiungi nuovo ricambio</div>
        </div>
        <div className="card-content">
          <form onSubmit={handleAddPart} className="parts-form">
            <div className="parts-form-grid">
              <div className="form-group">
                <label className="form-label">Codice ricambio</label>
                <input
                  type="text"
                  value={newPart.code}
                  onChange={(e) => handleInputChange('code', e.target.value)}
                  className="form-input"
                  placeholder="Es. PN-2024"
                />
              </div>
              <div className="form-group">
                <label className="form-label">Nome ricambio</label>
                <input
                  type="text"
                  value={newPart.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  className="form-input"
                  placeholder="Es. Sensore temperatura"
                />
              </div>
              <div className="form-group">
                <label className="form-label">Categoria</label>
                <input
                  type="text"
                  value={newPart.category}
                  onChange={(e) => handleInputChange('category', e.target.value)}
                  className="form-input"
                  placeholder="Es. Sensori"
                />
              </div>
              <div className="form-group">
                <label className="form-label">Posizione</label>
                <input
                  type="text"
                  value={newPart.location}
                  onChange={(e) => handleInputChange('location', e.target.value)}
                  className="form-input"
                  placeholder="Es. Magazzino 2"
                />
              </div>
              <div className="form-group full-width">
                <label className="form-label">Descrizione</label>
                <textarea
                  value={newPart.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  className="form-textarea"
                  placeholder="Es. Sensore per rilevazione pressioni nel circuito di riempimento"
                />
              </div>
              <div className="form-group">
                <label className="form-label">Rilevanza (%)</label>
                <input
                  type="number"
                  value={newPart.relevance}
                  min="0"
                  max="100"
                  onChange={(e) => handleInputChange('relevance', e.target.value)}
                  className="form-input"
                />
              </div>
            </div>
            <button type="submit" className="btn btn-secondary" style={{ marginTop: '1rem' }}>
              Aggiungi ricambio
            </button>
          </form>
          {message && (
            <div className={`upload-status ${message.type === 'error' ? 'status-error' : 'status-success'}`}>
              {message.text}
            </div>
          )}
        </div>
      </div>

      <div className="parts-grid">
        {filteredParts.map((part) => (
          <div key={part.code} className="part-card">
            <div className="part-code">{part.code}</div>
            <div className="part-name">{part.name}</div>
            <div className="part-desc">{part.description}</div>
            <div className="part-meta">Categoria: {part.category || 'N/D'} • Posizione: {part.location || 'N/D'}</div>
            <div className="part-relevance">
              <span className="relevance-label">Rilevanza</span>
              <div className="relevance-bar">
                <div className="relevance-fill" style={{ width: `${part.relevance * 100}%` }} />
              </div>
              <span className="relevance-score">{Math.round(part.relevance * 100)}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Parts
