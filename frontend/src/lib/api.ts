import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

export interface Project {
  name: string
}

export interface Component {
  name: string
  type: string
  content: string
  path: string
}

export interface SyncConfig {
  server: string
  sessionId: string
  token?: string
}

export interface AIGenerationRequest {
  prompt: string
  project: string
}

// Project API
export const projectsApi = {
  getAll: async (): Promise<{ projects: string[] }> => {
    const response = await api.get('/projects')
    return response.data
  },

  create: async (name: string): Promise<{ message: string }> => {
    const response = await api.post('/projects', { name })
    return response.data
  },

  delete: async (name: string): Promise<{ message: string }> => {
    const response = await api.delete(`/projects/${name}`)
    return response.data
  },

  getComponents: async (projectName: string): Promise<{ components: Component[] }> => {
    const response = await api.get(`/projects/${projectName}/components`)
    return response.data
  },

  createComponent: async (
    projectName: string,
    component: Omit<Component, 'path'>
  ): Promise<{ message: string }> => {
    const response = await api.post(`/projects/${projectName}/components`, component)
    return response.data
  },

  sync: async (projectName: string): Promise<{ message: string }> => {
    const response = await api.post(`/projects/${projectName}/sync`)
    return response.data
  },
}

// AI API
export const aiApi = {
  generate: async (request: AIGenerationRequest): Promise<{ result: string }> => {
    const response = await api.post('/ai/generate', request)
    return response.data
  },
}

// Sync Config API
export const syncConfigApi = {
  get: async (): Promise<SyncConfig> => {
    const response = await api.get('/sync/config')
    return response.data
  },

  update: async (config: SyncConfig): Promise<{ message: string }> => {
    const response = await api.put('/sync/config', config)
    return response.data
  },
}

export default api
