# D3E Agent - Modern Frontend Interface

A modern, responsive web interface for the D3E Agent application, built with React, TypeScript, and Tailwind CSS.

## 🚀 Features

### ✨ Modern UI/UX
- **Dark/Light Theme Support** - Automatic system theme detection with manual toggle
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- **Modern Components** - Built with Radix UI primitives and custom styling
- **Smooth Animations** - Tailwind CSS animations and transitions

### 🎯 Core Functionality
- **Project Management** - Create, view, and manage D3E projects
- **Component Editor** - Monaco Editor integration for D3E code editing
- **AI Code Generation** - Natural language to D3E code conversion
- **Real-time Sync** - WebSocket connection for live updates
- **Component Browser** - Organized view of models, widgets, pages, styles, and themes

### 🔧 Technical Features
- **TypeScript** - Full type safety and IntelliSense
- **React Query** - Efficient data fetching and caching
- **WebSocket Integration** - Real-time updates and notifications
- **API Integration** - RESTful API communication with the backend
- **Hot Reload** - Development server with instant updates

## 📋 Prerequisites

- **Node.js 18+** - [Download from nodejs.org](https://nodejs.org/)
- **npm** - Included with Node.js
- **Backend Server** - D3E Agent FastAPI backend running on port 8000

## 🛠️ Installation

### Option 1: Automatic Setup (Recommended)
```bash
# Start both frontend and backend
python start_app.py

# Or start frontend only
python start_frontend.py
```

### Option 2: Manual Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🎮 Usage

### Starting the Application
1. **Automatic**: Run `python start_app.py` from the project root
2. **Manual**: Start backend first, then run `npm run dev` in the frontend directory

### Accessing the Interface
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Key Features

#### 🏠 Dashboard
- View all D3E projects
- Create new projects
- Quick project statistics
- Project management actions

#### 📁 Project View
- Browse project components by type
- Create new components manually
- Generate components with AI
- Edit existing components
- Sync with remote D3E Studio

#### ⚙️ Settings
- Configure D3E Studio connection
- View connection status
- Manage sync settings
- System information

#### 🤖 AI Code Generation
- Natural language prompts
- Example prompt suggestions
- Real-time code generation
- Automatic component extraction

## 🎨 UI Components

### Design System
- **Colors**: CSS custom properties with dark/light theme support
- **Typography**: Tailwind CSS typography scale
- **Spacing**: Consistent spacing using Tailwind utilities
- **Components**: Radix UI primitives with custom styling

### Key Components
- `Button` - Various styles and sizes
- `Card` - Content containers with headers and footers
- `Input/Textarea` - Form inputs with validation states
- `Badge` - Status indicators and labels
- `MonacoEditor` - Code editor with syntax highlighting

## 🔧 Development

### Project Structure
```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── ui/             # Base UI components
│   │   ├── layout.tsx      # Main layout component
│   │   ├── ComponentEditor.tsx
│   │   ├── AIPromptDialog.tsx
│   │   └── MonacoEditor.tsx
│   ├── pages/              # Page components
│   │   ├── Dashboard.tsx
│   │   ├── ProjectView.tsx
│   │   └── Settings.tsx
│   ├── lib/                # Utilities and services
│   │   ├── api.ts          # API client
│   │   ├── websocket.ts    # WebSocket hook
│   │   └── utils.ts        # Helper functions
│   ├── App.tsx             # Main app component
│   ├── main.tsx            # Entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies and scripts
├── vite.config.ts          # Vite configuration
├── tailwind.config.js      # Tailwind CSS configuration
└── tsconfig.json           # TypeScript configuration
```

### Available Scripts
```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

### Environment Configuration
The frontend automatically proxies API requests to the backend server. Configuration is handled in `vite.config.ts`:

```typescript
server: {
  port: 3000,
  proxy: {
    '/api': 'http://localhost:8000',
    '/ws': 'ws://localhost:8000',
  },
}
```

## 🌐 API Integration

### REST API
- **Projects**: CRUD operations for D3E projects
- **Components**: Manage project components
- **AI Generation**: Natural language to code conversion
- **Sync Configuration**: D3E Studio connection settings

### WebSocket
- **Real-time Updates**: Component sync status
- **Notifications**: Success/error messages
- **Connection Status**: Live connection monitoring

## 🎯 Key Features Explained

### Theme System
The application supports automatic theme detection and manual theme switching:
- **System**: Follows OS preference
- **Light**: Light theme
- **Dark**: Dark theme (default)

### Component Editor
Monaco Editor integration provides:
- Syntax highlighting for D3E code
- Auto-completion and IntelliSense
- Error detection and validation
- Full-screen editing mode

### AI Integration
Natural language processing for D3E code generation:
- Multiple AI provider support (Claude, OpenAI, Gemini)
- Automatic fallback between providers
- Context-aware generation based on project
- Real-time component extraction

### Real-time Sync
WebSocket connection provides:
- Live sync status updates
- Real-time notifications
- Connection status monitoring
- Automatic reconnection

## 🚨 Troubleshooting

### Common Issues

1. **Port 3000 already in use**
   ```bash
   # Kill process using port 3000
   npx kill-port 3000
   ```

2. **Dependencies not installing**
   ```bash
   # Clear npm cache and reinstall
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Backend connection issues**
   - Ensure backend is running on port 8000
   - Check API proxy configuration in `vite.config.ts`
   - Verify CORS settings in backend

4. **WebSocket connection fails**
   - Check backend WebSocket endpoint
   - Verify firewall settings
   - Ensure proper protocol (ws/wss)

### Development Tips

1. **Hot Reload**: Changes are automatically reflected in the browser
2. **TypeScript**: Use TypeScript for better development experience
3. **React DevTools**: Install browser extension for debugging
4. **Network Tab**: Monitor API calls in browser developer tools

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Radix UI](https://www.radix-ui.com/)
- [Vite Guide](https://vitejs.dev/guide/)

## 🤝 Contributing

1. Follow the existing code style and patterns
2. Use TypeScript for all new components
3. Add proper error handling and loading states
4. Test responsive design on different screen sizes
5. Update documentation for new features
