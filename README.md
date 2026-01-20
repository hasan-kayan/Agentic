# React Flow Application

A React application built with React Flow (xyflow) featuring Zustand state management, project management, and an interactive node-based canvas.

## Getting Started

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173` (or the port shown in the terminal)

## Project Structure

```
src/
  ├── App.jsx              # Main application component
  ├── App.css              # Application styles
  ├── main.jsx             # Entry point
  ├── index.css            # Global styles
  ├── store/
  │   └── useProjectStore.js  # Zustand store for state management
  └── components/
      ├── ToolPanel.jsx    # Tool panel for adding nodes
      └── ProjectPanel.jsx # Project management panel
```

## Features

- **React Flow Canvas**: Interactive flow diagram with draggable nodes
- **Zustand State Management**: Centralized state management with persistence
- **Project Management**: Create, save, load, and delete multiple projects
- **Node Connections**: Connect nodes by dragging from one node's handle to another
- **Tool Panel**: Add new nodes with different types
- **Auto-save**: Projects are automatically saved to localStorage
- **Controls**: Zoom, pan, and minimap controls
- **Background Grid**: Visual grid background for better alignment

## Project Management

### Creating a Project

1. Click the "➕ New" button in the Project Panel (leftmost sidebar)
2. Enter a project name
3. Press Enter or click "Save"
4. The new project will be created and automatically loaded

### Loading a Project

- Click on any project in the Project Panel to load it
- The current project is highlighted in blue
- All nodes and connections from that project will be displayed

### Editing a Project Name

1. Click the edit icon (✏️) next to a project
2. Modify the name
3. Press Enter or click the checkmark (✓) to save
4. Press Escape or click the X to cancel

### Deleting a Project

1. Click the delete icon (🗑️) next to a project
2. Confirm the deletion in the dialog
3. If the deleted project was active, the first remaining project will be loaded

## How to Add New Objects/Nodes

### Method 1: Using the Tool Panel

1. Click any button in the Tool Panel (middle sidebar):
   - **➕ Add Node**: Adds a default node
   - **▭ Rectangle**: Adds a rectangle-shaped node
   - **⭕ Circle**: Adds a circle-shaped node
2. A new node will appear at a random position on the canvas
3. You can drag the node to reposition it

### Method 2: Using the Store

You can add nodes programmatically using the Zustand store:

```javascript
import useProjectStore from './store/useProjectStore'

const { addNode } = useProjectStore()

// Add a node
addNode('default', 'My New Node')
```

### Method 3: Add Custom Node Types

1. Create a custom node component in `src/components/`:

```javascript
// src/components/CustomNode.jsx
import React from 'react'

const CustomNode = ({ data }) => {
  return (
    <div style={{ 
      padding: '10px', 
      background: '#007bff', 
      color: 'white',
      borderRadius: '8px'
    }}>
      {data.label}
    </div>
  )
}

export default CustomNode
```

2. Register the node type in `App.jsx`:

```javascript
import CustomNode from './components/CustomNode'

const nodeTypes = {
  custom: CustomNode,
}

// Then use it in ReactFlow:
<ReactFlow
  nodes={nodes}
  edges={edges}
  nodeTypes={nodeTypes}
  // ... other props
>
```

3. Add nodes with the custom type using the store:

```javascript
const { addNode } = useProjectStore()

// Modify addNode in store to support custom types, or:
const newNode = {
  id: `node-${Date.now()}`,
  type: 'custom',
  position: { x: 100, y: 100 },
  data: { label: 'Custom Node' },
}
setNodes([...nodes, newNode])
```

## Connecting Nodes

**Nodes can be connected to each other!**

1. Hover over a node to see connection handles (small dots on the edges)
2. Click and drag from one node's handle to another node's handle
3. A connection (edge) will be created between the two nodes
4. Connections are automatically saved to the current project
5. You can delete connections by selecting them and pressing Delete

### Connection Features

- **Visual Feedback**: Connection line appears while dragging
- **Auto-save**: Connections are automatically saved to the project
- **Styled Connections**: Blue colored connections with 2px stroke width
- **Multiple Connections**: Nodes can have multiple incoming and outgoing connections

## Zustand Store API

The store (`useProjectStore`) provides the following methods:

### Node Management
- `addNode(type, label)`: Add a new node
- `deleteNode(nodeId)`: Delete a node and its connections
- `setNodes(nodes)`: Update all nodes (auto-saves to current project)
- `setEdges(edges)`: Update all edges (auto-saves to current project)

### Project Management
- `createProject(name)`: Create a new project
- `loadProject(projectId)`: Load a project
- `updateProject(projectId, updates)`: Update project metadata
- `deleteProject(projectId)`: Delete a project
- `initialize()`: Initialize store (creates default project if none exists)

### State Access
- `nodes`: Current project's nodes
- `edges`: Current project's edges
- `projects`: Array of all projects
- `currentProjectId`: ID of the currently loaded project

## Data Persistence

- Projects are automatically saved to **localStorage** using Zustand's persist middleware
- Data persists across browser sessions
- Only projects and current project ID are persisted (nodes/edges are stored within projects)

## Customization

### Styling Nodes

You can customize node appearance by:
1. Creating custom node components (see Method 3 above)
2. Using CSS classes in the node data
3. Modifying the default node styles in React Flow

### Adding More Tools

To add more tools to the panel, edit `src/components/ToolPanel.jsx`:

```javascript
import useProjectStore from '../store/useProjectStore'

const { addNode } = useProjectStore()

const handleAddYourTool = () => {
  addNode('your-type', 'Your Label')
}

// Add button:
<button className="tool-button" onClick={handleAddYourTool}>
  Your Tool Name
</button>
```

## Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Technologies Used

- **React 18**: UI library
- **React Flow (xyflow) 11**: Flow diagram library
- **Zustand 4**: State management with persistence
- **Vite**: Build tool and dev server
- **CSS3**: Styling

## Tips

- **Multiple Projects**: Use different projects to organize different flow diagrams
- **Node Positioning**: Drag nodes to reposition them
- **Zoom Controls**: Use the zoom controls in the bottom-right corner
- **Minimap**: Use the minimap to navigate large diagrams
- **Auto-save**: All changes are automatically saved - no need to manually save!
