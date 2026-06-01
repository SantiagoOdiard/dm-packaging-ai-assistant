import React, { useState, useEffect } from 'react'
import './App.css'
import Sidebar from './components/Sidebar'
import Home from './components/Home'
import Chat from './components/Chat'
import Troubleshoot from './components/Troubleshoot'
import Parts from './components/Parts'
import HowItWorks from './components/HowItWorks'
import Admin from './components/Admin'
import OnboardingModal from './components/OnboardingModal'

function App() {
  const [currentPage, setCurrentPage] = useState('home')
  const [showOnboarding, setShowOnboarding] = useState(false)

  useEffect(() => {
    // Check if user has seen onboarding
    const hasSeenOnboarding = localStorage.getItem('hasSeenOnboarding')
    if (!hasSeenOnboarding) {
      setShowOnboarding(true)
      localStorage.setItem('hasSeenOnboarding', 'true')
    }
  }, [])

  const handleNavigate = (page) => {
    setCurrentPage(page)
  }

  const handleOnboardingStart = () => {
    setShowOnboarding(false)
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <Home onNavigate={handleNavigate} />
      case 'chat':
        return <Chat />
      case 'troubleshoot':
        return <Troubleshoot />
      case 'parts':
        return <Parts />
      case 'how-it-works':
        return <HowItWorks onNavigate={handleNavigate} />
      case 'admin':
        return <Admin />
      default:
        return <Home onNavigate={handleNavigate} />
    }
  }

  return (
    <div className="app-container">
      <Sidebar currentPage={currentPage} onNavigate={handleNavigate} />
      <main className="main-content">
        {renderPage()}
      </main>
      {showOnboarding && <OnboardingModal onStart={handleOnboardingStart} onNavigate={handleNavigate} />}
    </div>
  )
}

export default App
