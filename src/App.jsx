import React, { useCallback, useEffect, useRef } from 'react'
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  addEdge,
  useNodesState,
  useEdgesState,
} from 'reactflow'
import 'reactflow/dist/style.css'
import ToolPanel from './components/ToolPanel'
import ProjectPanel from './components/ProjectPanel'
import useProjectStore from './store/useProjectStore'
import './App.css'

function App() {
  const {
    nodes: storeNodes,
    edges: storeEdges,
    setNodes: setStoreNodes,
    setEdges: setStoreEdges,
    initialize,
  } = useProjectStore()

  const [nodes, setNodes, onNodesChange] = useNodesState(storeNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(storeEdges)

  const isUpdatingFromStore = useRef(false)

  // Initialize store on mount
  useEffect(() => {
    initialize()
  }, [initialize])

  // Sync store nodes with ReactFlow when store changes (from external actions)
  useEffect(() => {
    if (!isUpdatingFromStore.current) {
      const nodesStr = JSON.stringify(nodes)
      const storeNodesStr = JSON.stringify(storeNodes)
      if (nodesStr !== storeNodesStr) {
        isUpdatingFromStore.current = true
        setNodes(storeNodes)
        setTimeout(() => {
          isUpdatingFromStore.current = false
        }, 0)
      }
    }
  }, [storeNodes, setNodes])

  // Sync store edges with ReactFlow when store changes (from external actions)
  useEffect(() => {
    if (!isUpdatingFromStore.current) {
      const edgesStr = JSON.stringify(edges)
      const storeEdgesStr = JSON.stringify(storeEdges)
      if (edgesStr !== storeEdgesStr) {
        isUpdatingFromStore.current = true
        setEdges(storeEdges)
        setTimeout(() => {
          isUpdatingFromStore.current = false
        }, 0)
      }
    }
  }, [storeEdges, setEdges])

  // Sync ReactFlow nodes back to store
  const handleNodesChange = useCallback(
    (changes) => {
      onNodesChange(changes)
      if (!isUpdatingFromStore.current) {
        // Use a small delay to ensure ReactFlow has processed the changes
        setTimeout(() => {
          setNodes((currentNodes) => {
            setStoreNodes(currentNodes)
            return currentNodes
          })
        }, 10)
      }
    },
    [onNodesChange, setNodes, setStoreNodes]
  )

  // Sync ReactFlow edges back to store
  const handleEdgesChange = useCallback(
    (changes) => {
      onEdgesChange(changes)
      if (!isUpdatingFromStore.current) {
        // Use a small delay to ensure ReactFlow has processed the changes
        setTimeout(() => {
          setEdges((currentEdges) => {
            setStoreEdges(currentEdges)
            return currentEdges
          })
        }, 10)
      }
    },
    [onEdgesChange, setEdges, setStoreEdges]
  )

  const onConnect = useCallback(
    (params) => {
      const newEdge = addEdge(params, edges)
      setEdges(newEdge)
      setStoreEdges(newEdge)
    },
    [edges, setEdges, setStoreEdges]
  )

  return (
    <div className="app-container">
      <ProjectPanel />
      <ToolPanel />
      <div className="flow-container">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={handleNodesChange}
          onEdgesChange={handleEdgesChange}
          onConnect={onConnect}
          fitView
          connectionLineStyle={{ stroke: '#007bff', strokeWidth: 2 }}
          defaultEdgeOptions={{ style: { stroke: '#007bff', strokeWidth: 2 } }}
        >
          <Background />
          <Controls />
          <MiniMap />
        </ReactFlow>
      </div>
    </div>
  )
}

export default App
