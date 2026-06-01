import React from 'react'

const navItems = [
  { key: 'home', label: 'Home', icon: '🏠' },
  { key: 'chat', label: 'Chat Tecnica', icon: '🧠' },
  { key: 'troubleshoot', label: 'Troubleshooting', icon: '🔧' },
  { key: 'parts', label: 'Ricambi', icon: '🔩' },
  { key: 'admin', label: 'Admin', icon: '📊' },
  { key: 'how-it-works', label: 'Come si usa', icon: '📘' },
]

function Sidebar({ currentPage, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <img src="/logo.svg" alt="DM Packaging Group" className="sidebar-logo-image" />
        <div>
          <div className="sidebar-title">DM Packaging AI</div>
          <div style={{ fontSize: '0.8rem', color: 'rgba(255,255,255,0.85)' }}>Assistant tecnico</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <button
            type="button"
            key={item.key}
            className={`nav-item ${currentPage === item.key ? 'active' : ''}`}
            onClick={() => onNavigate(item.key)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">Software tecnico industriale</div>
    </aside>
  )
}

export default Sidebar
