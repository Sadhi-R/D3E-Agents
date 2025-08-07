import { useState, useEffect } from 'react'
import { useMutation } from '@tanstack/react-query'
import { X, Save, Code } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Textarea } from '@/components/ui/textarea'
import { projectsApi, Component } from '@/lib/api'
import { MonacoEditor } from '@/components/MonacoEditor'
import toast from 'react-hot-toast'

interface ComponentEditorProps {
  component: Component
  projectName: string
  onClose: () => void
  onSave: () => void
}

export function ComponentEditor({ component, projectName, onClose, onSave }: ComponentEditorProps) {
  // Debug logging
  console.log('ComponentEditor received component:', component)
  console.log('Component content:', component.content)
  console.log('Component content length:', component.content?.length || 0)
  console.log('Component content type:', typeof component.content)
  
  const [editedComponent, setEditedComponent] = useState({
    name: component.name,
    type: component.type,
    content: component.content || '' // Ensure content is never undefined
  })
  const [hasChanges, setHasChanges] = useState(false)
  const [useTextarea, setUseTextarea] = useState(false)

  // Debug the edited component state
  console.log('Edited component content:', editedComponent.content)

  useEffect(() => {
    console.log('Component prop changed, updating state:', component)
    
    // Normalize the type name (remove 's' if plural)
    let normalizedType = component.type;
    if (normalizedType.endsWith('s')) {
      normalizedType = normalizedType.slice(0, -1); // Remove 's' from 'widgets' -> 'widget'
    }
    
    setEditedComponent({
      name: component.name,
      type: normalizedType,
      content: component.content || ''
    })
  }, [component])

  useEffect(() => {
    const hasChanges = 
      editedComponent.name !== component.name ||
      editedComponent.type !== component.type ||
      editedComponent.content !== component.content
    setHasChanges(hasChanges)
  }, [editedComponent, component])

  // Update component mutation
  const updateComponentMutation = useMutation({
    mutationFn: () => projectsApi.createComponent(projectName, editedComponent),
    onSuccess: () => {
      toast.success('Component updated successfully')
      onSave()
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update component')
    },
  })

  const handleSave = () => {
    if (!editedComponent.name.trim() || !editedComponent.content.trim()) {
      toast.error('Name and content are required')
      return
    }
    updateComponentMutation.mutate()
  }

  const handleClose = () => {
    if (hasChanges) {
      if (window.confirm('You have unsaved changes. Are you sure you want to close?')) {
        onClose()
      }
    } else {
      onClose()
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

  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
      <Card className="w-full max-w-7xl max-h-[95vh] flex flex-col">
        <CardHeader className="flex-shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Code className="h-6 w-6 text-primary" />
              <div>
                <CardTitle className="flex items-center">
                  <div className={`w-3 h-3 rounded-full ${getTypeColor(component.type)} mr-2`} />
                  Edit Component
                </CardTitle>
                <CardDescription>
                  Modify your D3E component code
                </CardDescription>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              {hasChanges && (
                <Badge variant="secondary">Unsaved changes</Badge>
              )}
              <Button
                variant="outline"
                size="sm"
                onClick={handleSave}
                disabled={!hasChanges || updateComponentMutation.isPending}
              >
                <Save className="h-4 w-4 mr-2" />
                {updateComponentMutation.isPending ? 'Saving...' : 'Save'}
              </Button>
              <Button variant="ghost" size="icon" onClick={handleClose}>
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="flex-1 flex flex-col space-y-4 min-h-0 p-6">
          {/* Component metadata */}
          <div className="grid grid-cols-2 gap-4 flex-shrink-0">
            <div>
              <label className="text-sm font-medium mb-2 block">Name</label>
              <Input
                value={editedComponent.name}
                onChange={(e) => setEditedComponent(prev => ({ ...prev, name: e.target.value }))}
                placeholder="Component name"
              />
            </div>
            <div>
              <label className="text-sm font-medium mb-2 block">Type</label>
              <select
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
                value={editedComponent.type}
                onChange={(e) => setEditedComponent(prev => ({ ...prev, type: e.target.value }))}
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

          {/* Code editor */}
          <div className="flex-1 flex flex-col min-h-0">
            <div className="flex items-center justify-between mb-3">
              <label className="text-sm font-medium">Content</label>
              <div className="flex items-center space-x-2">
                <span className="text-xs text-muted-foreground">
                  {editedComponent.content.length} characters
                </span>
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => setUseTextarea(!useTextarea)}
                >
                  {useTextarea ? 'Monaco Editor' : 'Simple Editor'}
                </Button>
              </div>
            </div>
            
            <div className="flex-1 border rounded-md overflow-hidden" style={{ minHeight: '500px' }}>
              {useTextarea ? (
                <Textarea
                  value={editedComponent.content}
                  onChange={(e) => setEditedComponent(prev => ({ ...prev, content: e.target.value }))}
                  className="w-full h-full resize-none font-mono text-sm border-0 focus:ring-0"
                  style={{ minHeight: '500px' }}
                  placeholder="Enter your D3E component code here..."
                />
              ) : (
                <MonacoEditor
                  value={editedComponent.content}
                  onChange={(value) => {
                    console.log('Monaco editor onChange called with value:', value)
                    setEditedComponent(prev => ({ ...prev, content: value || '' }))
                  }}
                  language="typescript"
                  height="500px"
                  options={{
                    wordWrap: 'on',
                    scrollBeyondLastLine: false,
                    minimap: { enabled: true },
                    fontSize: 14,
                    automaticLayout: true,
                    padding: { top: 10, bottom: 10 },
                    lineNumbers: 'on',
                    folding: true,
                    bracketPairColorization: { enabled: true },
                  }}
                />
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
