import React, { useState } from 'react'
import useProjectStore from '../store/useProjectStore'
import '../App.css'

const ProjectPanel = () => {
  const {
    projects,
    currentProjectId,
    createProject,
    loadProject,
    deleteProject,
    updateProject,
  } = useProjectStore()

  const [isCreating, setIsCreating] = useState(false)
  const [newProjectName, setNewProjectName] = useState('')
  const [editingId, setEditingId] = useState(null)
  const [editName, setEditName] = useState('')

  const currentProject = projects.find((p) => p.id === currentProjectId)

  const handleCreateProject = () => {
    if (newProjectName.trim()) {
      createProject(newProjectName.trim())
      setNewProjectName('')
      setIsCreating(false)
    }
  }

  const handleStartEdit = (project) => {
    setEditingId(project.id)
    setEditName(project.name)
  }

  const handleSaveEdit = (projectId) => {
    if (editName.trim()) {
      updateProject(projectId, { name: editName.trim() })
      setEditingId(null)
      setEditName('')
    }
  }

  const handleCancelEdit = () => {
    setEditingId(null)
    setEditName('')
  }

  return (
    <div className="project-panel">
      <div className="project-panel-header">
        <h2>Projects</h2>
        <button
          className="project-add-button"
          onClick={() => setIsCreating(true)}
        >
          ➕ New
        </button>
      </div>

      {isCreating && (
        <div className="project-create-form">
          <input
            type="text"
            value={newProjectName}
            onChange={(e) => setNewProjectName(e.target.value)}
            placeholder="Project name..."
            className="project-input"
            autoFocus
            onKeyPress={(e) => {
              if (e.key === 'Enter') handleCreateProject()
              if (e.key === 'Escape') {
                setIsCreating(false)
                setNewProjectName('')
              }
            }}
          />
          <div className="project-form-actions">
            <button
              className="project-form-button save"
              onClick={handleCreateProject}
            >
              Save
            </button>
            <button
              className="project-form-button cancel"
              onClick={() => {
                setIsCreating(false)
                setNewProjectName('')
              }}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      <div className="project-list">
        {projects.length === 0 ? (
          <div className="project-empty">No projects yet</div>
        ) : (
          projects.map((project) => (
            <div
              key={project.id}
              className={`project-item ${
                project.id === currentProjectId ? 'active' : ''
              }`}
            >
              {editingId === project.id ? (
                <div className="project-edit-form">
                  <input
                    type="text"
                    value={editName}
                    onChange={(e) => setEditName(e.target.value)}
                    className="project-input"
                    autoFocus
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') handleSaveEdit(project.id)
                      if (e.key === 'Escape') handleCancelEdit()
                    }}
                  />
                  <div className="project-form-actions">
                    <button
                      className="project-form-button save"
                      onClick={() => handleSaveEdit(project.id)}
                    >
                      ✓
                    </button>
                    <button
                      className="project-form-button cancel"
                      onClick={handleCancelEdit}
                    >
                      ✕
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <div
                    className="project-item-content"
                    onClick={() => loadProject(project.id)}
                  >
                    <div className="project-item-name">{project.name}</div>
                    <div className="project-item-meta">
                      {project.nodes.length} nodes
                    </div>
                  </div>
                  <div className="project-item-actions">
                    <button
                      className="project-action-button"
                      onClick={() => handleStartEdit(project)}
                      title="Edit"
                    >
                      ✏️
                    </button>
                    <button
                      className="project-action-button"
                      onClick={() => {
                        if (
                          window.confirm(
                            `Delete "${project.name}"? This cannot be undone.`
                          )
                        ) {
                          deleteProject(project.id)
                        }
                      }}
                      title="Delete"
                    >
                      🗑️
                    </button>
                  </div>
                </>
              )}
            </div>
          ))
        )}
      </div>

      {currentProject && (
        <div className="project-info">
          <div className="project-info-label">Current Project:</div>
          <div className="project-info-name">{currentProject.name}</div>
          <div className="project-info-stats">
            {currentProject.nodes.length} nodes • {currentProject.edges.length}{' '}
            connections
          </div>
        </div>
      )}
    </div>
  )
}

export default ProjectPanel
