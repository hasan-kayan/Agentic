import React from 'react'
import useProjectStore from '../store/useProjectStore'
import '../App.css'

const ToolPanel = () => {
  const { addNode } = useProjectStore()

  const handleAddDefaultNode = () => {
    addNode('default', 'New Node')
  }

  const handleAddRectangle = () => {
    addNode('default', 'Rectangle')
  }

  const handleAddCircle = () => {
    addNode('default', 'Circle')
  }

  return (
    <div className="tool-panel">
      <h2>Tools</h2>
      <button className="tool-button" onClick={handleAddDefaultNode}>
        ➕ Add Node
      </button>
      <button className="tool-button" onClick={handleAddRectangle}>
        ▭ Rectangle
      </button>
      <button className="tool-button" onClick={handleAddCircle}>
        ⭕ Circle
      </button>
    </div>
  )
}

export default ToolPanel
