import { useState, useEffect, useRef } from 'react'
import './App.css'
import ChatInterface from './components/ChatInterface'
import TerminalView from './components/TerminalView'
import Header from './components/Header'
import axios from 'axios'

function App() {
  const [messages, setMessages] = useState([])
  const [terminalLogs, setTerminalLogs] = useState([])
  const [isExecuting, setIsExecuting] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const [stats, setStats] = useState({
    filesCreated: 0,
    commandsExecuted: 0,
    iterations: 0
  })

  // Initialize session
  useEffect(() => {
    const newSessionId = Date.now().toString()
    setSessionId(newSessionId)
    
    // Welcome message
    setMessages([{
      role: 'assistant',
      content: '🤖 Welcome to AI Coding Agent!\n\nI can create complete projects, fix bugs, write tests, and more.\n\nTry commands like:\n• "Create a React todo app with beautiful UI"\n• "Build a FastAPI backend for a blog"\n• "Create a portfolio website with modern design"\n\nWhat would you like me to build?',
      timestamp: new Date()
    }])

    addTerminalLog('info', '🚀 AI Coding Agent initialized')
    addTerminalLog('info', `Session ID: ${newSessionId}`)
  }, [])

  const addTerminalLog = (type, message) => {
    const timestamp = new Date().toLocaleTimeString()
    setTerminalLogs(prev => [...prev, { type, message, timestamp }])
  }

  const handleSendMessage = async (message) => {
    // Add user message
    setMessages(prev => [...prev, {
      role: 'user',
      content: message,
      timestamp: new Date()
    }])

    setIsExecuting(true)
    addTerminalLog('info', `📝 Task received: ${message}`)
    addTerminalLog('system', '🤖 Starting autonomous execution...')

    try {
      // Call the autonomous agent API
      const response = await axios.post('http://localhost:8000/api/autonomous/execute', {
        task: message,
        session_id: sessionId,
        max_iterations: 50
      })

      const result = response.data

      // Update stats
      setStats({
        filesCreated: result.files_created || 0,
        commandsExecuted: result.commands_executed || 0,
        iterations: result.iterations || 0
      })

      // Add logs from execution
      if (result.success) {
        addTerminalLog('success', `✅ Task completed in ${result.iterations} iterations`)
        addTerminalLog('success', `📁 Created ${result.files_created} files`)
        addTerminalLog('success', `⚡ Executed ${result.commands_executed} commands`)
        if (result.project_path) {
          addTerminalLog('info', `📂 Project: ${result.project_path}`)
        }

        // Add AI response
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `✅ **Task Completed!**\n\n${result.summary}\n\n**Stats:**\n- Files created: ${result.files_created}\n- Commands executed: ${result.commands_executed}\n- Iterations: ${result.iterations}\n\n${result.project_path ? `**Project:** \`${result.project_path}\`` : ''}`,
          timestamp: new Date()
        }])
      } else {
        addTerminalLog('error', `❌ Task failed: ${result.error || 'Unknown error'}`)
        
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `⚠️ Task did not complete:\n\n${result.error || 'The task may be too complex or requires more iterations.'}\n\nTry breaking it down into smaller tasks or being more specific.`,
          timestamp: new Date()
        }])
      }
    } catch (error) {
      console.error('Error:', error)
      addTerminalLog('error', `❌ Error: ${error.message}`)
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `❌ Error communicating with the AI agent:\n\n${error.message}\n\nMake sure the backend is running on port 8000.`,
        timestamp: new Date()
      }])
    } finally {
      setIsExecuting(false)
    }
  }

  return (
    <div className="app">
      <Header stats={stats} isExecuting={isExecuting} />
      
      <div className="main-container">
        <div className="chat-section">
          <ChatInterface 
            messages={messages}
            onSendMessage={handleSendMessage}
            isExecuting={isExecuting}
          />
        </div>
        
        <div className="terminal-section">
          <TerminalView 
            logs={terminalLogs}
            isExecuting={isExecuting}
          />
        </div>
      </div>
    </div>
  )
}

export default App


