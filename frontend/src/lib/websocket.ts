import { useEffect, useRef, useState } from 'react'
import toast from 'react-hot-toast'

export interface WebSocketMessage {
  type: string
  project?: string
  component?: string
  success?: boolean
  message?: string
  prompt?: string
}

export function useWebSocket(url: string = '/ws') {
  const [isConnected, setIsConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null)
  const ws = useRef<WebSocket | null>(null)

  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}${url}`
    
    const connect = () => {
      ws.current = new WebSocket(wsUrl)

      ws.current.onopen = () => {
        setIsConnected(true)
        console.log('WebSocket connected')
      }

      ws.current.onclose = () => {
        setIsConnected(false)
        console.log('WebSocket disconnected')
        // Attempt to reconnect after 3 seconds
        setTimeout(connect, 3000)
      }

      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error)
      }

      ws.current.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          setLastMessage(message)
          
          // Handle different message types
          switch (message.type) {
            case 'project_created':
              toast.success(`Project "${message.project}" created successfully`)
              break
            case 'project_deleted':
              toast.success(`Project "${message.project}" deleted`)
              break
            case 'component_synced':
              if (message.success) {
                toast.success(`Component "${message.component}" synced successfully`)
              } else {
                toast.error(`Failed to sync component "${message.component}": ${message.message}`)
              }
              break
            case 'project_synced':
              toast.success(`Project "${message.project}" synced successfully`)
              break
            case 'ai_generation_complete':
              toast.success('AI generation completed')
              break
            default:
              console.log('Unknown message type:', message.type)
          }
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }
    }

    connect()

    return () => {
      if (ws.current) {
        ws.current.close()
      }
    }
  }, [url])

  const sendMessage = (message: any) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message))
    }
  }

  return {
    isConnected,
    lastMessage,
    sendMessage,
  }
}
