import { useEffect, useRef } from 'react'
import * as monaco from 'monaco-editor'

interface MonacoEditorProps {
  value: string
  onChange: (value: string) => void
  language?: string
  height?: string | number
  theme?: string
  options?: monaco.editor.IStandaloneEditorConstructionOptions
}

export function MonacoEditor({
  value,
  onChange,
  language = 'javascript',
  height = '400px',
  theme = 'vs-dark',
  options = {}
}: MonacoEditorProps) {
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current) return

    // Create editor
    editorRef.current = monaco.editor.create(containerRef.current, {
      value,
      language,
      theme,
      automaticLayout: true,
      minimap: { enabled: false },
      scrollBeyondLastLine: false,
      fontSize: 14,
      lineNumbers: 'on',
      roundedSelection: false,
      scrollbar: {
        vertical: 'auto',
        horizontal: 'auto',
      },
      wordWrap: 'on',
      ...options,
    })

    // Set up change listener
    const disposable = editorRef.current.onDidChangeModelContent(() => {
      const currentValue = editorRef.current?.getValue() || ''
      onChange(currentValue)
    })

    return () => {
      disposable.dispose()
      editorRef.current?.dispose()
    }
  }, [])

  // Update value when prop changes
  useEffect(() => {
    if (editorRef.current && editorRef.current.getValue() !== value) {
      editorRef.current.setValue(value)
    }
  }, [value])

  // Update theme when prop changes
  useEffect(() => {
    monaco.editor.setTheme(theme)
  }, [theme])

  return (
    <div
      ref={containerRef}
      style={{ height: typeof height === 'number' ? `${height}px` : height }}
      className="w-full"
    />
  )
}
