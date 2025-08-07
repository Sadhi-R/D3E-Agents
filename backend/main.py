import asyncio
import json
import os
import sys
from typing import List, Optional, Dict, Any
import threading
import time

# Add the Agent directory to the Python path
agent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Agent')
if agent_path not in sys.path:
    sys.path.insert(0, agent_path)

try:
    from project_manager import list_projects, create_project, cleanup_project
    from file_manager import create_or_update_file
    from sync_manager import update_code, Context, sync_all_d3e_files, find_d3e_files
    from component_extractor import save_components_from_d3e_output
    from context_loader import ContextManager
    from config import CLAUDE_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY, remote_config
except ImportError as e:
    print(f"Warning: Could not import Agent modules: {e}")
    print(f"Agent path: {agent_path}")
    print("This is normal during static analysis, but imports should work at runtime.")

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests

app = FastAPI(title="D3E Agent API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React/Vite dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API requests/responses
class ProjectCreate(BaseModel):
    name: str

class ComponentCreate(BaseModel):
    type: str  # model, widget, page, style, theme, optionset
    name: str
    content: str

class AIPromptRequest(BaseModel):
    prompt: str
    project: str

class SyncConfigUpdate(BaseModel):
    server: str
    sessionId: str
    token: Optional[str] = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# AI API functions (copied from agent.py)
def build_system_message(project: str = None):
    context_manager = ContextManager()
    ctx = context_manager.build_context()
    
    # Load README.md context
    try:
        readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()[:3000]  # First 3000 chars
            ctx["README Context"] = readme_content
    except Exception:
        pass
    
    # Load Documentation structures
    try:
        doc_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documentation')
        
        # Load Widget structure
        widget_structure_path = os.path.join(doc_path, 'Widgets', 'STRUCTURE.md')
        if os.path.exists(widget_structure_path):
            with open(widget_structure_path, 'r', encoding='utf-8') as f:
                ctx["Widget Structure"] = f.read()[:2000]
        
        # Load basic widget examples
        basic_widget_path = os.path.join(doc_path, 'Widgets', 'basic-widget.md')
        if os.path.exists(basic_widget_path):
            with open(basic_widget_path, 'r', encoding='utf-8') as f:
                ctx["Widget Examples"] = f.read()[:2000]
                
        # Load Model structure if generating models
        model_structure_path = os.path.join(doc_path, 'Models', 'STRUCTURE.md')
        if os.path.exists(model_structure_path):
            with open(model_structure_path, 'r', encoding='utf-8') as f:
                ctx["Model Structure"] = f.read()[:2000]
                
        # Load Page structure if generating pages
        page_structure_path = os.path.join(doc_path, 'Pages', 'STRUCTURE.md')
        if os.path.exists(page_structure_path):
            with open(page_structure_path, 'r', encoding='utf-8') as f:
                ctx["Page Structure"] = f.read()[:2000]
                
    except Exception:
        pass
    
    # Add project-specific theme and style information
    if project:
        try:
            base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Projects', project)
            theme_dir = os.path.join(base_dir, 'StyleTheme')
            if os.path.exists(theme_dir):
                theme_files = [t for t in os.listdir(theme_dir) if t.endswith('.d3e')]
                if theme_files:
                    ctx["Available Themes"] = "\n".join([f"- {t.replace('.d3e', '')}" for t in theme_files])
            style_dir = os.path.join(base_dir, 'Style')
            if os.path.exists(style_dir):
                style_files = [s for s in os.listdir(style_dir) if s.endswith('.d3e')]
                if style_files:
                    ctx["Available Styles"] = "\n".join([f"- {s.replace('.d3e', '')}" for s in style_files])
        except Exception:
            pass

    context_str = "\n".join([f"=== {k} ===\n{v}" for k, v in ctx.items()])
    return f"""
You are a D3E Programming Language Expert. D3E is a domain-specific language for creating UI components and business logic.

{context_str}

=== D3E SYNTAX RULES ===
- D3E uses a specific DSL syntax, NOT JSON
- Components use curly braces: Widget {{ ... }}
- Properties use single quotes: name 'ComponentName'
- Arrays use square brackets without commas: children [ item1 item2 item3 ]
- Child objects use identity syntax: child TextView {{ ... }}
- Theme colors use @c1, @c2, @c3, @c4 notation
- Expressions use backticks: `variableName` or `expression`
- No commas between array items or object properties

=== EXAMPLE D3E WIDGET SYNTAX ===
Widget {{
    package 'projectname.com'
    name 'LoginWidget'
    category 'UserDefined'
    build Column {{
        name 'MainColumn'
        data {{
            mainAxisAlignment 'center'
            padding '20'
        }}
        children [
            TextView {{
                name 'Title'
                data {{
                    data 'Login'
                    fontSize '24'
                    color '@c1'
                }}
            }}
            LabelField {{
                name 'EmailField'
                data {{
                    label 'Email'
                    placeHolder 'Enter email'
                    value `email`
                }}
            }}
        ]
    }}
    eventHandlers [
        {{
            name 'loginHandler'
            type OnEvent
            on loginButton
            event onPressed
            block ```
                // Your D3E code here
            ```
        }}
    ]
}}

=== ENFORCEMENT ===
- ONLY generate D3E DSL syntax (NOT JSON)
- Use proper D3E component types from the structures
- Reference existing themes and styles when available
- Follow D3E syntax rules strictly (no commas in arrays)
- Use theme colors (@c1, @c2, etc.) instead of hardcoded colors
- Wrap expressions in backticks for data binding
"""

def build_user_prompt(user_prompt: str):
    return f"""
Generate D3E programming language code for: {user_prompt}

Requirements:
- Output must be valid D3E DSL syntax (NOT JSON)
- Use proper D3E syntax: Widget {{ name 'ComponentName' ... }}
- Follow D3E syntax rules from the README and Documentation
- Use available D3E component types (Column, Row, TextView, Button, LabelField, etc.)
- Include build tree for UI structure using 'build' property
- Use theme colors (@c1, @c2, @c3, @c4)
- Wrap expressions in backticks for data binding: `variableName`
- No commas between array items or object properties
- Use single quotes for string values: 'value'
- No HTML, CSS, JavaScript, or other web code

Example D3E syntax:
Widget {{
    package 'projectname.com'
    name 'ComponentName'
    category 'UserDefined'
    build Column {{
        name 'MainContainer'
        data {{
            mainAxisAlignment 'center'
        }}
        children [
            TextView {{
                name 'Title'
                data {{
                    data 'Hello World'
                }}
            }}
        ]
    }}
}}
"""

async def call_claude(user_prompt: str, project: str = None):
    if not CLAUDE_API_KEY:
        raise HTTPException(status_code=500, detail="Claude API key not configured")
    
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 4096,
        "temperature": 0.7,
        "top_p": 0.95,
        "system": build_system_message(project),
        "messages": [
            {"role": "user", "content": build_user_prompt(user_prompt)}
        ]
    }

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return ''.join([part.get("text", "") for part in data.get("content", [])])
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Claude API Error: {str(e)}")

async def call_openai(user_prompt: str, project: str = None):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": build_system_message(project)},
            {"role": "user", "content": build_user_prompt(user_prompt)}
        ]
    }
    
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")

async def call_demo_mode(user_prompt: str, project: str = None):
    """Demo mode - returns sample D3E code when no API keys are configured"""
    return f"""// Demo Mode - AI Generation for: {user_prompt}
// This is sample D3E code. Configure real API keys for actual generation.

model DemoWidget {{
    String title = "Generated for: {user_prompt}";
    String description = "This is a demo component created because no AI API keys are configured.";
    Boolean isDemo = true;
}}

widget DemoWidgetDisplay {{
    DemoWidget data;
    
    render() {{
        Container {{
            Text(data.title) {{
                style: "font-size: 24px; font-weight: bold; color: #2563eb;"
            }}
            Text(data.description) {{
                style: "font-size: 14px; color: #6b7280; margin-top: 8px;"
            }}
            Text("⚠️ Configure API keys in .env file for real AI generation") {{
                style: "font-size: 12px; color: #f59e0b; margin-top: 16px; padding: 8px; background: #fef3c7; border-radius: 4px;"
            }}
        }}
    }}
}}"""

async def call_with_fallback(user_prompt: str, project: str = None):
    # Check if any API keys are configured (not just placeholder values)
    has_claude = CLAUDE_API_KEY and CLAUDE_API_KEY != "your_claude_api_key_here"
    has_openai = OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here"
    
    providers = []
    if has_claude:
        providers.append(("Claude", call_claude))
    if has_openai:
        providers.append(("OpenAI", call_openai))
    
    # If no real API keys are configured, use demo mode
    if not providers:
        print("⚠️ No API keys configured, using demo mode")
        return await call_demo_mode(user_prompt, project)
    
    for name, func in providers:
        try:
            return await func(user_prompt, project)
        except Exception as e:
            print(f"⚠️ {name} failed: {e}")
            continue
    
    # If all configured providers failed, fall back to demo mode
    print("⚠️ All configured AI providers failed, falling back to demo mode")
    return await call_demo_mode(user_prompt, project)

# API Routes
@app.get("/")
async def root():
    return {"message": "D3E Agent API Server", "version": "1.0.0"}

@app.get("/api/config/status")
async def get_config_status():
    """Get API configuration status"""
    has_claude = CLAUDE_API_KEY and CLAUDE_API_KEY != "your_claude_api_key_here"
    has_openai = OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here"
    has_gemini = GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here"
    
    return {
        "claude_configured": has_claude,
        "openai_configured": has_openai,
        "gemini_configured": has_gemini,
        "any_configured": has_claude or has_openai or has_gemini,
        "demo_mode": not (has_claude or has_openai or has_gemini)
    }

@app.get("/api/projects")
async def get_projects():
    """Get list of all projects"""
    try:
        projects = list_projects()
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projects")
async def create_new_project(project: ProjectCreate):
    """Create a new project"""
    try:
        success = create_project(project.name)
        if success:
            await manager.broadcast(json.dumps({
                "type": "project_created",
                "project": project.name
            }))
            return {"message": f"Project '{project.name}' created successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to create project")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/projects/{project_name}")
async def delete_project(project_name: str):
    """Delete a project (cleanup all files)"""
    try:
        cleanup_project(project_name)
        await manager.broadcast(json.dumps({
            "type": "project_deleted",
            "project": project_name
        }))
        return {"message": f"Project '{project_name}' deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects/{project_name}/components")
async def get_project_components(project_name: str):
    """Get all components in a project"""
    try:
        files = find_d3e_files(project_name)
        components = []
        
        for file_path, component_dir in files:
            component_name = os.path.splitext(os.path.basename(file_path))[0]
            component_type = component_dir.lower()
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                components.append({
                    "name": component_name,
                    "type": component_type,
                    "content": content,
                    "path": file_path
                })
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        
        return {"components": components}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projects/{project_name}/components")
async def create_component(project_name: str, component: ComponentCreate):
    """Create or update a component in a project"""
    try:
        success = create_or_update_file(
            component.type, 
            component.name, 
            component.content, 
            project=project_name
        )
        
        if success:
            # Sync to remote D3E studio
            d3e_type_map = {
                'model': 'Model',
                'optionset': 'OptionSet',
                'widget': 'Widget',
                'page': 'Page',
                'style': 'Style',
                'theme': 'StyleTheme'
            }
            
            if component.type in d3e_type_map:
                ctx = Context(remote_config)
                try:
                    sync_success, msg = await update_code(
                        ctx, 
                        d3e_type_map[component.type], 
                        component.name, 
                        component.content
                    )
                    
                    await manager.broadcast(json.dumps({
                        "type": "component_synced",
                        "project": project_name,
                        "component": component.name,
                        "success": sync_success,
                        "message": msg
                    }))
                except Exception as e:
                    print(f"Sync failed: {e}")
            
            return {"message": f"Component '{component.name}' created successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to create component")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/generate")
async def generate_with_ai(request: AIPromptRequest):
    """Generate D3E code using AI"""
    try:
        result = await call_with_fallback(request.prompt, request.project)
        
        # Extract and save components from AI output
        save_components_from_d3e_output(result, project=request.project)
        
        await manager.broadcast(json.dumps({
            "type": "ai_generation_complete",
            "project": request.project,
            "prompt": request.prompt
        }))
        
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projects/{project_name}/sync")
async def sync_project(project_name: str):
    """Sync all project files to remote D3E studio"""
    try:
        await sync_all_d3e_files(project_name)
        
        await manager.broadcast(json.dumps({
            "type": "project_synced",
            "project": project_name
        }))
        
        return {"message": f"Project '{project_name}' synced successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sync/config")
async def get_sync_config():
    """Get current sync configuration"""
    return remote_config

@app.put("/api/sync/config")
async def update_sync_config(config: SyncConfigUpdate):
    """Update sync configuration"""
    try:
        # Update the config
        new_config = {
            "server": config.server,
            "sessionId": config.sessionId
        }
        if config.token:
            new_config["token"] = config.token
        
        # Save to file
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Agent', 'remote_sync_config.json')
        with open(config_path, 'w') as f:
            json.dump(new_config, f, indent=2)
        
        # Update global config
        remote_config.update(new_config)
        
        return {"message": "Sync configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for now - can be extended for specific commands
            await manager.send_personal_message(f"Echo: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", "8001"))
    uvicorn.run(app, host="0.0.0.0", port=port)
