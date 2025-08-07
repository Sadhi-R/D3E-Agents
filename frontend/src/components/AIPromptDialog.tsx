import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { Bot, Send, X, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { aiApi } from '@/lib/api'
import { MonacoEditor } from '@/components/MonacoEditor'
import toast from 'react-hot-toast'

interface AIPromptDialogProps {
  open: boolean
  onClose: () => void
  projectName: string
  onGenerate: () => void
}

export function AIPromptDialog({ open, onClose, projectName, onGenerate }: AIPromptDialogProps) {
  const [prompt, setPrompt] = useState('')
  const [result, setResult] = useState('')

  // AI generation mutation
  const generateMutation = useMutation({
    mutationFn: (prompt: string) => aiApi.generate({ prompt, project: projectName }),
    onSuccess: (data) => {
      console.log('AI Generation Response:', data);
      console.log('Result type:', typeof data.result);
      console.log('Result length:', data.result?.length);
      
      // Clean the result to extract just the D3E code
      let cleanedResult = data.result;
      
      // Remove explanatory text before the code
      const codeBlockStart = cleanedResult.indexOf('```d3e');
      if (codeBlockStart !== -1) {
        cleanedResult = cleanedResult.substring(codeBlockStart + 6); // Remove ```d3e
      } else {
        // Look for Widget { pattern
        const widgetStart = cleanedResult.indexOf('Widget {');
        const modelStart = cleanedResult.indexOf('Model {');
        const pageStart = cleanedResult.indexOf('Page {');
        
        const starts = [widgetStart, modelStart, pageStart].filter(s => s !== -1);
        if (starts.length > 0) {
          cleanedResult = cleanedResult.substring(Math.min(...starts));
        }
      }
      
      // Remove closing ``` and any text after it
      const codeBlockEnd = cleanedResult.indexOf('```');
      if (codeBlockEnd !== -1) {
        cleanedResult = cleanedResult.substring(0, codeBlockEnd);
      }
      
      // Clean up the result
      cleanedResult = cleanedResult.trim();
      
      console.log('Cleaned result:', cleanedResult);
      setResult(cleanedResult);
      
      // Show success message indicating files were created
      toast.success('AI generation completed! Files have been created automatically.');
      onGenerate(); // This will refresh the project view to show new components
    },
    onError: (error: any) => {
      console.error('AI Generation Error:', error);
      toast.error(error.response?.data?.detail || 'Failed to generate code');
    },
  })

  const handleGenerate = () => {
    if (!prompt.trim()) {
      toast.error('Please enter a prompt')
      return
    }
    generateMutation.mutate(prompt.trim())
  }

  const handleClose = () => {
    setPrompt('')
    setResult('')
    onClose()
  }

  const examplePrompts = [
    "Create a Student model with name, email, phone, and enrollmentDate fields",
    "Create a course registration widget with student selection and course inputs",
    "Create a teacher dashboard page with course management features",
    "Create a login widget with username, password, and remember me checkbox",
    "Create a user profile model with personal and contact information",
    "Create a modern theme with blue primary colors and rounded corners"
  ]

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
      <Card className="w-full max-w-5xl max-h-[90vh] flex flex-col">
        <CardHeader className="flex-shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <Bot className="h-6 w-6 text-primary" />
              </div>
              <div>
                <CardTitle className="flex items-center">
                  AI Code Generator
                  <Sparkles className="h-4 w-4 ml-2 text-yellow-500" />
                </CardTitle>
                <CardDescription>
                  Generate D3E components using natural language
                </CardDescription>
              </div>
            </div>
            <Button variant="ghost" size="icon" onClick={handleClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>
        </CardHeader>
        
        <CardContent className="flex-1 flex flex-col space-y-6 min-h-0">
          {/* Project info */}
          <div className="flex items-center space-x-2">
            <span className="text-sm text-muted-foreground">Project:</span>
            <Badge variant="secondary">{projectName}</Badge>
          </div>

          {/* Example prompts */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Example prompts:</label>
            <div className="flex flex-wrap gap-2">
              {examplePrompts.map((example, index) => (
                <Button
                  key={index}
                  variant="outline"
                  size="sm"
                  className="text-xs h-auto py-1 px-2"
                  onClick={() => setPrompt(example)}
                >
                  {example}
                </Button>
              ))}
            </div>
          </div>

          {/* Prompt input */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Describe what you want to create:</label>
            <Textarea
              placeholder="e.g., Create a User model with firstName, lastName, email, and password properties..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={4}
              className="resize-none"
            />
          </div>

          {/* Generate button */}
          <div className="flex justify-end">
            <Button
              onClick={handleGenerate}
              disabled={!prompt.trim() || generateMutation.isPending}
              className="min-w-[120px]"
            >
              {generateMutation.isPending ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                  Generating...
                </>
              ) : (
                <>
                  <Send className="h-4 w-4 mr-2" />
                  Generate
                </>
              )}
            </Button>
          </div>

          {/* Result */}
          {result && (
            <div className="flex-1 min-h-0 space-y-2">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium">Generated D3E Code:</label>
                <div className="flex items-center space-x-2">
                  <Badge variant="secondary">Files Created Automatically</Badge>
                  <Badge variant="outline" className="text-green-600">✅ Ready</Badge>
                </div>
              </div>
              <div className="border rounded-md overflow-hidden h-full min-h-[300px]">
                <MonacoEditor
                  value={result}
                  onChange={() => {}} // Read-only
                  language="typescript"
                  height="100%"
                  options={{
                    readOnly: true,
                    minimap: { enabled: false },
                    wordWrap: 'on',
                    scrollBeyondLastLine: false,
                  }}
                />
              </div>
              <div className="text-sm text-muted-foreground bg-muted/50 p-3 rounded-lg">
                <p className="font-medium mb-1">✅ Components Generated Successfully</p>
                <p>Files have been automatically created and saved to your project. You can now see them in the component list above and edit them as needed.</p>
              </div>
            </div>
          )}

          {/* Loading state */}
          {generateMutation.isPending && (
            <div className="flex-1 flex items-center justify-center min-h-[200px]">
              <div className="text-center space-y-4">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto" />
                <p className="text-muted-foreground">Generating D3E code...</p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
