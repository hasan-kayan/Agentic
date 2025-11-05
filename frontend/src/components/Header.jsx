import React from 'react'
import { FaRobot, FaFile, FaTerminal, FaSync } from 'react-icons/fa'
import './Header.css'

function Header({ stats, isExecuting }) {
  return (
    <header className="header">
      <div className="header-left">
        <FaRobot className="logo-icon" />
        <div className="header-title">
          <h1>AI Coding Agent</h1>
          <p>Autonomous Development Assistant</p>
        </div>
      </div>
      
      <div className="header-stats">
        <div className="stat-item">
          <FaFile className="stat-icon" />
          <div className="stat-content">
            <span className="stat-value">{stats.filesCreated}</span>
            <span className="stat-label">Files</span>
          </div>
        </div>
        
        <div className="stat-item">
          <FaTerminal className="stat-icon" />
          <div className="stat-content">
            <span className="stat-value">{stats.commandsExecuted}</span>
            <span className="stat-label">Commands</span>
          </div>
        </div>
        
        <div className="stat-item">
          <FaSync className={`stat-icon ${isExecuting ? 'spinning' : ''}`} />
          <div className="stat-content">
            <span className="stat-value">{stats.iterations}</span>
            <span className="stat-label">Iterations</span>
          </div>
        </div>
      </div>
      
      {isExecuting && (
        <div className="execution-indicator">
          <div className="pulse"></div>
          <span>AI is working...</span>
        </div>
      )}
    </header>
  )
}

export default Header


