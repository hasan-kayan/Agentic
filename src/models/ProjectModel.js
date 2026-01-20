/**
 * Project Data Model
 * Basit proje veri modeli
 */
class ProjectModel {
  constructor(data = {}) {
    this.id = data.id || this.generateId()
    this.name = data.name || 'Untitled Project'
    this.nodes = data.nodes || this.getDefaultNodes()
    this.edges = data.edges || []
    this.createdAt = data.createdAt || new Date().toISOString()
    this.updatedAt = data.updatedAt || new Date().toISOString()
    this.description = data.description || ''
    this.tags = data.tags || []
  }

  /**
   * Benzersiz ID oluştur
   */
  generateId() {
    return `project-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  }

  /**
   * Varsayılan node'ları döndür
   */
  getDefaultNodes() {
    return [
      {
        id: '1',
        type: 'default',
        position: { x: 400, y: 200 },
        data: { label: 'Start Node' },
      },
    ]
  }

  /**
   * Projeyi güncelle
   */
  update(updates) {
    Object.assign(this, updates, {
      updatedAt: new Date().toISOString(),
    })
    return this
  }

  /**
   * Proje istatistiklerini döndür
   */
  getStats() {
    return {
      nodeCount: this.nodes.length,
      edgeCount: this.edges.length,
      connectionCount: this.edges.length,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    }
  }

  /**
   * Projeyi JSON formatına çevir
   */
  toJSON() {
    return {
      id: this.id,
      name: this.name,
      nodes: this.nodes,
      edges: this.edges,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
      description: this.description,
      tags: this.tags,
    }
  }

  /**
   * JSON'dan proje oluştur
   */
  static fromJSON(json) {
    return new ProjectModel(json)
  }

  /**
   * Yeni proje oluştur
   */
  static create(name, options = {}) {
    return new ProjectModel({
      name,
      ...options,
    })
  }

  /**
   * Projeyi klonla
   */
  clone(newName = null) {
    const cloned = new ProjectModel({
      ...this.toJSON(),
      id: this.generateId(),
      name: newName || `${this.name} (Copy)`,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    })
    // Deep clone nodes and edges
    cloned.nodes = JSON.parse(JSON.stringify(this.nodes))
    cloned.edges = JSON.parse(JSON.stringify(this.edges))
    return cloned
  }

  /**
   * Projenin geçerli olup olmadığını kontrol et
   */
  validate() {
    const errors = []

    if (!this.name || this.name.trim().length === 0) {
      errors.push('Project name is required')
    }

    if (!Array.isArray(this.nodes)) {
      errors.push('Nodes must be an array')
    }

    if (!Array.isArray(this.edges)) {
      errors.push('Edges must be an array')
    }

    return {
      isValid: errors.length === 0,
      errors,
    }
  }
}

export default ProjectModel
