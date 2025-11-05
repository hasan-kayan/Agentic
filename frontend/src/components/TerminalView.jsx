import { useRef, useEffect } from 'react'
import { FaTerminal, FaCheck, FaTimes, FaInfo, FaCog } from 'react-icons/fa'
import './TerminalView.css'

function TerminalView({ logs, isExecuting }) {
  const logsEndRef = useRef(null)

  const scrollToBottom = () => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [logs])

  const getLogIcon = (type) => {
    switch (type) {
      case 'success':
        return <FaCheck className="log-icon success" />
      case 'error':
        return <FaTimes className="log-icon error" />
      case 'system':
        return <FaCog className="log-icon system" />
      default:
        return <FaInfo className="log-icon info" />
    }
  }

  return (
    <div className="terminal-view">
      <div className="terminal-header">
        <FaTerminal className="terminal-icon" />
        <h2>Terminal Output</h2>
        <span className="terminal-subtitle">Real-time execution logs</span>
      </div>
      
      <div className="terminal-content">
        {logs.length === 0 ? (
          <div className="terminal-empty">
            <FaTerminal className="empty-icon" />
            <p>Waiting for tasks...</p>
            <p className="empty-subtitle">Execution logs will appear here</p>
          </div>
        ) : (
          <>
            {logs.map((log, index) => (
              <div key={index} className={`terminal-log ${log.type}`}>
                {getLogIcon(log.type)}
                <span className="log-time">[{log.timestamp}]</span>
                <span className="log-message">{log.message}</span>
              </div>
            ))}
            <div ref={logsEndRef} />
          </>
        )}
        
        {isExecuting && (
          <div className="terminal-log system blinking">
            <FaCog className="log-icon system spinning" />
            <span className="log-time">[{new Date().toLocaleTimeString()}]</span>
            <span className="log-message">AI is processing...</span>
          </div>
        )}
      </div>
    </div>
  )
}

export default TerminalView


