import { Routes, Route } from 'react-router-dom'
import { ThemeProvider } from '@/components/theme-provider'
import { Layout } from '@/components/layout'
import { Dashboard } from '@/pages/Dashboard'
import { ProjectView } from '@/pages/ProjectView'
import { Settings } from '@/pages/Settings'

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="d3e-ui-theme">
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/project/:projectName" element={<ProjectView />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </ThemeProvider>
  )
}

export default App
