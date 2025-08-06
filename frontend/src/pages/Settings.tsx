import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Save, Server, Key, Globe, RefreshCw } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { syncConfigApi, SyncConfig } from '@/lib/api'
import { useWebSocket } from '@/lib/websocket'
import toast from 'react-hot-toast'

export function Settings() {
  const [config, setConfig] = useState<SyncConfig>({
    server: '',
    sessionId: '',
    token: ''
  })
  const [hasChanges, setHasChanges] = useState(false)
  const queryClient = useQueryClient()
  const { isConnected } = useWebSocket()

  // Fetch sync config
  const { data: syncConfig, isLoading, error } = useQuery({
    queryKey: ['syncConfig'],
    queryFn: syncConfigApi.get,
  })

  // Update sync config mutation
  const updateConfigMutation = useMutation({
    mutationFn: syncConfigApi.update,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['syncConfig'] })
      setHasChanges(false)
      toast.success('Configuration updated successfully')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update configuration')
    },
  })

  useEffect(() => {
    if (syncConfig) {
      setConfig(syncConfig)
    }
  }, [syncConfig])

  useEffect(() => {
    if (syncConfig) {
      const hasChanges = 
        config.server !== syncConfig.server ||
        config.sessionId !== syncConfig.sessionId ||
        config.token !== syncConfig.token
      setHasChanges(hasChanges)
    }
  }, [config, syncConfig])

  const handleSave = () => {
    if (!config.server.trim() || !config.sessionId.trim()) {
      toast.error('Server URL and Session ID are required')
      return
    }
    updateConfigMutation.mutate(config)
  }

  const handleReset = () => {
    if (syncConfig) {
      setConfig(syncConfig)
    }
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <p className="text-destructive mb-4">Failed to load settings</p>
          <Button onClick={() => queryClient.invalidateQueries({ queryKey: ['syncConfig'] })}>
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
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">
          Configure your D3E Agent and remote synchronization
        </p>
      </div>

      {/* Connection Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Globe className="h-5 w-5 mr-2" />
            Connection Status
          </CardTitle>
          <CardDescription>
            Real-time connection status with the backend
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
              <span className="font-medium">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
            <Badge variant={isConnected ? 'default' : 'destructive'}>
              {isConnected ? 'Online' : 'Offline'}
            </Badge>
          </div>
          <p className="text-sm text-muted-foreground mt-2">
            {isConnected 
              ? 'Real-time updates are enabled' 
              : 'Real-time updates are disabled. Check your connection.'
            }
          </p>
        </CardContent>
      </Card>

      {/* D3E Studio Sync Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Server className="h-5 w-5 mr-2" />
            D3E Studio Sync
          </CardTitle>
          <CardDescription>
            Configure connection to your remote D3E Studio instance
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {isLoading ? (
            <div className="space-y-4">
              <div className="h-10 bg-muted rounded animate-pulse" />
              <div className="h-10 bg-muted rounded animate-pulse" />
              <div className="h-10 bg-muted rounded animate-pulse" />
            </div>
          ) : (
            <>
              <div className="space-y-2">
                <label className="text-sm font-medium">Server URL</label>
                <Input
                  placeholder="https://dev.d3e.studio"
                  value={config.server}
                  onChange={(e) => setConfig(prev => ({ ...prev, server: e.target.value }))}
                />
                <p className="text-xs text-muted-foreground">
                  The base URL of your D3E Studio instance
                </p>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Session ID</label>
                <Input
                  placeholder="ef00a1a1-3a6a-40df-a75b-08d4360fcd36"
                  value={config.sessionId}
                  onChange={(e) => setConfig(prev => ({ ...prev, sessionId: e.target.value }))}
                />
                <p className="text-xs text-muted-foreground">
                  Your session ID for authentication with D3E Studio
                </p>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">
                  Authentication Token
                  <Badge variant="secondary" className="ml-2">Optional</Badge>
                </label>
                <Input
                  type="password"
                  placeholder="Enter token if required"
                  value={config.token || ''}
                  onChange={(e) => setConfig(prev => ({ ...prev, token: e.target.value }))}
                />
                <p className="text-xs text-muted-foreground">
                  Additional authentication token if required by your D3E Studio instance
                </p>
              </div>

              <div className="flex items-center space-x-2 pt-4">
                <Button
                  onClick={handleSave}
                  disabled={!hasChanges || updateConfigMutation.isPending}
                >
                  <Save className="h-4 w-4 mr-2" />
                  {updateConfigMutation.isPending ? 'Saving...' : 'Save Changes'}
                </Button>
                {hasChanges && (
                  <Button variant="outline" onClick={handleReset}>
                    Reset
                  </Button>
                )}
                {hasChanges && (
                  <Badge variant="secondary">Unsaved changes</Badge>
                )}
              </div>
            </>
          )}
        </CardContent>
      </Card>

      {/* API Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Key className="h-5 w-5 mr-2" />
            AI API Configuration
          </CardTitle>
          <CardDescription>
            AI API keys are configured via environment variables on the server
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 border rounded-lg">
                <h4 className="font-medium mb-2">Claude API</h4>
                <Badge variant="outline">Server-side</Badge>
                <p className="text-xs text-muted-foreground mt-2">
                  CLAUDE_API_KEY environment variable
                </p>
              </div>
              <div className="p-4 border rounded-lg">
                <h4 className="font-medium mb-2">OpenAI API</h4>
                <Badge variant="outline">Server-side</Badge>
                <p className="text-xs text-muted-foreground mt-2">
                  OPENAI_API_KEY environment variable
                </p>
              </div>
              <div className="p-4 border rounded-lg">
                <h4 className="font-medium mb-2">Gemini API</h4>
                <Badge variant="outline">Server-side</Badge>
                <p className="text-xs text-muted-foreground mt-2">
                  GEMINI_API_KEY environment variable
                </p>
              </div>
            </div>
            <p className="text-sm text-muted-foreground">
              API keys are securely stored on the server. The AI generation will automatically 
              fall back between available providers.
            </p>
          </div>
        </CardContent>
      </Card>

      {/* About */}
      <Card>
        <CardHeader>
          <CardTitle>About D3E Agent</CardTitle>
          <CardDescription>
            Version and system information
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Version:</span>
              <span className="text-sm font-medium">1.0.0</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Frontend:</span>
              <span className="text-sm font-medium">React + TypeScript</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Backend:</span>
              <span className="text-sm font-medium">FastAPI + Python</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Real-time:</span>
              <span className="text-sm font-medium">WebSocket</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
