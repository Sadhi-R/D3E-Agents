import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  Plus, 
  Code, 
  FileText, 
  Layers, 
  Palette, 
  Settings as SettingsIcon,
  Bot,
  RefreshCw
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Textarea } from '@/components/ui/textarea'
import { Input } from '@/components/ui/input'
import { projectsApi, Component } from '@/lib/api'
import { ComponentEditor } from '@/components/ComponentEditor'
import { AIPromptDialog } from '@/components/AIPromptDialog'
import toast from 'react-hot-toast'

export function ProjectView() {
  const { projectName } = useParams<{ projectName: string }>()
  const [selectedComponent, setSelectedComponent] = useState<Component | null>(null)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [showAIDialog, setShowAIDialog] = useState(false)
  const [newComponent, setNewComponent] = useState({
    name: '',
    type: 'model',
    content: ''
  })
  const queryClient = useQueryClient()

  // Fetch project components
  const { data: componentsData, isLoading, error } = useQuery({
    queryKey: ['components', projectName],
    queryFn: () => projectsApi.getComponents(projectName!),
    enabled: !!projectName,
  })

  // Sync project mutation
  const syncProjectMutation = useMutation({
    mutationFn: () => projectsApi.sync(projectName!),
    onSuccess: () => {
      toast.success('Project synced successfully')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to sync project')
    },
  })

  // Create component mutation
  const createComponentMutation = useMutation({
    mutationFn: (component: Omit<Component, 'path'>) => 
      projectsApi.createComponent(projectName!, component),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['components', projectName] })
      setShowCreateForm(false)
      setNewComponent({ name: '', type: 'model', content: '' })
      toast.success('Component created successfully')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create component')
    },
  })

  const components = componentsData?.components || []

  const componentsByType = components.reduce((acc, component) => {
    if (!acc[component.type]) {
      acc[component.type] = []
    }
    acc[component.type].push(component)
    return acc
  }, {} as Record<string, Component[]>)

  const getTypeIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'model': return FileText
      case 'widget': return Layers
      case 'page': return Code
      case 'style': return Palette
      case 'theme': case 'styletheme': return SettingsIcon
      default: return FileText
    }
  }

  const getTypeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'model': return 'bg-blue-500'
      case 'widget': return 'bg-green-500'
      case 'page': return 'bg-purple-500'
      case 'style': return 'bg-orange-500'
      case 'theme': case 'styletheme': return 'bg-pink-500'
      default: return 'bg-gray-500'
    }
  }

  const generateD3EStructure = (type: string, name: string, content: string) => {
    // If content already looks like D3E code, return it as-is
    if (content.includes('{') && content.includes('}')) {
      return content
    }

    // Generate proper D3E structure based on type
    switch (type.toLowerCase()) {
      case 'model':
        return `Model {
  name "${name}"
  
  ${content}
}`

      case 'widget':
        return `Widget {
  name "${name}"
  
  ${content}
}`

      case 'page':
        return `Page {
  name "${name}"
  
  ${content}
}`

      case 'style':
        return `Style {
  name "${name}"
  
  ${content}
}`

      case 'theme':
        return `StyleTheme {
  name "${name}"
  
  ${content}
}`

      case 'optionset':
        return `OptionSet {
  name "${name}"
  
  ${content}
}`

      default:
        return content
    }
  }

  const handleCreateComponent = (e: React.FormEvent) => {
    e.preventDefault()
    if (!newComponent.name.trim()) return
    
    // Generate D3E structure even if content is empty
    const content = newComponent.content.trim() || '// Add your D3E code here'
    const d3eContent = generateD3EStructure(newComponent.type, newComponent.name, content)
    
    createComponentMutation.mutate({
      ...newComponent,
      content: d3eContent
    })
  }

  if (!projectName) {
    return <div>Project not found</div>
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <p className="text-destructive mb-4">Failed to load project components</p>
          <Button onClick={() => queryClient.invalidateQueries({ queryKey: ['components', projectName] })}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Retry
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{projectName}</h1>
          <p className="text-muted-foreground">
            Manage components and generate D3E code
          </p>
        </div>
        <div className="flex gap-2">
          <Button 
            variant="outline" 
            onClick={() => setShowAIDialog(true)}
          >
            <Bot className="h-4 w-4 mr-2" />
            AI Generate
          </Button>
          <Button 
            variant="outline" 
            onClick={() => syncProjectMutation.mutate()}
            disabled={syncProjectMutation.isPending}
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            {syncProjectMutation.isPending ? 'Syncing...' : 'Sync'}
          </Button>
          <Button onClick={() => setShowCreateForm(true)}>
            <Plus className="h-4 w-4 mr-2" />
            New Component
          </Button>
        </div>
      </div>

      {/* Create Component Form */}
      {showCreateForm && (
        <Card>
          <CardHeader>
            <CardTitle>Create New Component</CardTitle>
            <CardDescription>
              Add a new D3E component to your project
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleCreateComponent} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">Name</label>
                  <Input
                    placeholder="Component name"
                    value={newComponent.name}
                    onChange={(e) => setNewComponent(prev => ({ ...prev, name: e.target.value }))}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">Type</label>
                  <select
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
                    value={newComponent.type}
                    onChange={(e) => setNewComponent(prev => ({ ...prev, type: e.target.value }))}
                  >
                    <option value="model">Model</option>
                    <option value="widget">Widget</option>
                    <option value="page">Page</option>
                    <option value="style">Style</option>
                    <option value="theme">Theme</option>
                    <option value="optionset">Option Set</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">Content</label>
                <Textarea
                  placeholder="Enter D3E code content (optional - structure will be auto-generated)..."
                  value={newComponent.content}
                  onChange={(e) => setNewComponent(prev => ({ ...prev, content: e.target.value }))}
                  rows={10}
                />
                <p className="text-xs text-muted-foreground mt-1">
                  Leave empty to auto-generate basic D3E structure, or add your own content
                </p>
              </div>
              <div className="flex gap-2">
                <Button 
                  type="submit" 
                  disabled={!newComponent.name.trim() || createComponentMutation.isPending}
                >
                  {createComponentMutation.isPending ? 'Creating...' : 'Create'}
                </Button>
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={() => {
                    setShowCreateForm(false)
                    setNewComponent({ name: '', type: 'model', content: '' })
                  }}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Components by Type */}
      <div className="space-y-6">
        {Object.entries(componentsByType).map(([type, typeComponents]) => {
          const Icon = getTypeIcon(type)
          const colorClass = getTypeColor(type)
          
          return (
            <Card key={type}>
              <CardHeader>
                <CardTitle className="flex items-center capitalize">
                  <div className={`w-3 h-3 rounded-full ${colorClass} mr-3`} />
                  {type}s
                  <Badge variant="secondary" className="ml-2">
                    {typeComponents.length}
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
                  {typeComponents.map((component) => (
                    <div
                      key={component.name}
                      className="flex items-center justify-between p-3 border rounded-lg hover:bg-accent cursor-pointer transition-colors"
                      onClick={() => setSelectedComponent(component)}
                    >
                      <div className="flex items-center">
                        <Icon className="h-4 w-4 mr-2 text-muted-foreground" />
                        <span className="font-medium">{component.name}</span>
                      </div>
                      <Button variant="ghost" size="sm">
                        <Code className="h-3 w-3" />
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )
        })}

        {/* Empty state */}
        {components.length === 0 && !isLoading && (
          <Card className="text-center py-12">
            <CardContent>
              <Code className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">No components yet</h3>
              <p className="text-muted-foreground mb-4">
                Create your first component or use AI to generate D3E code
              </p>
              <div className="flex gap-2 justify-center">
                <Button onClick={() => setShowCreateForm(true)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Create Component
                </Button>
                <Button variant="outline" onClick={() => setShowAIDialog(true)}>
                  <Bot className="h-4 w-4 mr-2" />
                  AI Generate
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Loading state */}
        {isLoading && (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <Card key={i} className="animate-pulse">
                <CardContent className="p-4">
                  <div className="h-4 bg-muted rounded w-3/4 mb-2" />
                  <div className="h-3 bg-muted rounded w-1/2" />
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Component Editor Modal */}
      {selectedComponent && (
        <ComponentEditor
          component={selectedComponent}
          projectName={projectName}
          onClose={() => setSelectedComponent(null)}
          onSave={() => {
            queryClient.invalidateQueries({ queryKey: ['components', projectName] })
            setSelectedComponent(null)
          }}
        />
      )}

      {/* AI Prompt Dialog */}
      <AIPromptDialog
        open={showAIDialog}
        onClose={() => setShowAIDialog(false)}
        projectName={projectName}
        onGenerate={() => {
          queryClient.invalidateQueries({ queryKey: ['components', projectName] })
        }}
      />
    </div>
  )
}
