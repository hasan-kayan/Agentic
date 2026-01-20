import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useProjectStore = create(
  persist(
    (set, get) => ({
      // Current project state
      currentProjectId: null,
      projects: [],

      // Current flow state
      nodes: [
        {
          id: '1',
          type: 'default',
          position: { x: 400, y: 200 },
          data: { label: 'Start Node' },
        },
      ],
      edges: [],

      // Node actions
      setNodes: (nodes) => {
        set({ nodes })
        // Auto-save to current project
        const { currentProjectId, projects } = get()
        if (currentProjectId) {
          const updatedProjects = projects.map((p) =>
            p.id === currentProjectId
              ? {
                  ...p,
                  nodes: JSON.parse(JSON.stringify(nodes)), // Deep clone
                  updatedAt: new Date().toISOString(),
                }
              : p
          )
          set({ projects: updatedProjects })
        }
      },

      setEdges: (edges) => {
        set({ edges })
        // Auto-save to current project
        const { currentProjectId, projects } = get()
        if (currentProjectId) {
          const updatedProjects = projects.map((p) =>
            p.id === currentProjectId
              ? {
                  ...p,
                  edges: JSON.parse(JSON.stringify(edges)), // Deep clone
                  updatedAt: new Date().toISOString(),
                }
              : p
          )
          set({ projects: updatedProjects })
        }
      },

      addNode: (type, label) => {
        const { nodes } = get()
        const newNode = {
          id: `node-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
          type: type || 'default',
          position: {
            x: Math.random() * 500 + 200,
            y: Math.random() * 400 + 100,
          },
          data: { label: label || `Node ${nodes.length + 1}` },
        }
        get().setNodes([...nodes, newNode])
      },

      deleteNode: (nodeId) => {
        const { nodes, edges } = get()
        const updatedNodes = nodes.filter((n) => n.id !== nodeId)
        const updatedEdges = edges.filter(
          (e) => e.source !== nodeId && e.target !== nodeId
        )
        get().setNodes(updatedNodes)
        get().setEdges(updatedEdges)
      },

      // Project management
      createProject: (name) => {
        const { projects } = get()
        const newProject = {
          id: `project-${Date.now()}`,
          name: name || `Project ${projects.length + 1}`,
          nodes: [
            {
              id: '1',
              type: 'default',
              position: { x: 400, y: 200 },
              data: { label: 'Start Node' },
            },
          ],
          edges: [],
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        }
        set({
          projects: [...projects, newProject],
          currentProjectId: newProject.id,
          nodes: newProject.nodes,
          edges: newProject.edges,
        })
        return newProject.id
      },

      loadProject: (projectId) => {
        const { projects } = get()
        const project = projects.find((p) => p.id === projectId)
        if (project) {
          set({
            currentProjectId: projectId,
            nodes: JSON.parse(JSON.stringify(project.nodes)), // Deep clone
            edges: JSON.parse(JSON.stringify(project.edges)), // Deep clone
          })
        }
      },

      updateProject: (projectId, updates) => {
        const { projects } = get()
        const updatedProjects = projects.map((p) =>
          p.id === projectId
            ? {
                ...p,
                ...updates,
                updatedAt: new Date().toISOString(),
              }
            : p
        )
        set({ projects: updatedProjects })
      },

      deleteProject: (projectId) => {
        const { projects, currentProjectId } = get()
        const updatedProjects = projects.filter((p) => p.id !== projectId)
        set({ projects: updatedProjects })
        
        // If deleted project was current, switch to first project or create new
        if (currentProjectId === projectId) {
          if (updatedProjects.length > 0) {
            get().loadProject(updatedProjects[0].id)
          } else {
            set({
              currentProjectId: null,
              nodes: [
                {
                  id: '1',
                  type: 'default',
                  position: { x: 400, y: 200 },
                  data: { label: 'Start Node' },
                },
              ],
              edges: [],
            })
          }
        }
      },

      // Initialize with a default project if none exists
      initialize: () => {
        const { projects, currentProjectId } = get()
        if (projects.length === 0) {
          get().createProject('My First Project')
        } else if (!currentProjectId) {
          get().loadProject(projects[0].id)
        }
      },
    }),
    {
      name: 'react-flow-projects-storage',
      partialize: (state) => ({
        projects: state.projects,
        currentProjectId: state.currentProjectId,
      }),
    }
  )
)

export default useProjectStore
