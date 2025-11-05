import { useState, useRef, useEffect } from 'react'
import { FaPaperPlane, FaUser, FaRobot } from 'react-icons/fa'
import './ChatInterface.css'

function ChatInterface({ messages, onSendMessage, isExecuting }) {
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim() && !isExecuting) {
      onSendMessage(input.trim())
      setInput('')
    }
  }

  const formatMessage = (content) => {
    // Simple markdown-like formatting
    return content
      .split('\n')
      .map((line, i) => {
        // Bold
        line = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Code
        line = line.replace(/`(.*?)`/g, '<code>$1</code>')
        return line
      })
      .join('<br/>')
  }

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>💬 Chat Interface</h2>
        <span className="chat-subtitle">Talk to your AI coding assistant</span>
      </div>
      
      <div className="messages-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'user' ? <FaUser /> : <FaRobot />}
            </div>
            <div className="message-content">
              <div className="message-header">
                <span className="message-sender">
                  {msg.role === 'user' ? 'You' : 'AI Agent'}
                </span>
                <span className="message-time">
                  {msg.timestamp?.toLocaleTimeString()}
                </span>
              </div>
              <div 
                className="message-text"
                dangerouslySetInnerHTML={{ __html: formatMessage(msg.content) }}
              />
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={isExecuting ? "AI is working..." : "Type your task here... (e.g., 'Create a todo app with React')"}
          disabled={isExecuting}
          className="chat-input"
        />
        <button 
          type="submit" 
          disabled={isExecuting || !input.trim()}
          className="send-button"
        >
          <FaPaperPlane />
        </button>
      </form>
    </div>
  )
}

export default ChatInterface


