from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import json
import os
import sys
from typing import List, Optional, Dict, Any
import threading
import time

# Add the Agent directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Agent'))

from project_manager import list_projects, create_project, cleanup_project
from file_manager import create_or_update_file
from sync_manager import update_code, Context, sync_all_d3e_files, find_d3e_files
from component_extractor import save_components_from_d3e_output
from context_loader import ContextManager
from config import CLAUDE_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY, remote_config
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
You are a D3E Programming Language Expert. D3E is a standalone programming language like Dart, Java, or Python.
{context_str}
=== ENFORCEMENT ===
- ONLY generate D3E language code.
- NO HTML, CSS, JavaScript, or web framework code.
- D3E uses Widgets, Pages, Styles, Themes (Column, Row, TextView, etc.).
- ALWAYS reference existing themes and styles when creating widgets/pages.
- Use theme colors (@c1, @c2, etc.) instead of hardcoded colors.
- Reference existing styles where applicable (Primary, Secondary, Error, etc.).
- Consider any referenced models and their properties.
"""

def build_user_prompt(user_prompt: str):
    return f"""
Generate D3E programming language code for: {user_prompt}

IMPORTANT:
- Use only D3E syntax.
- No web or unrelated code.
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
        "model": "claude-opus-4-20250514",
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

async def call_with_fallback(user_prompt: str, project: str = None):
    providers = [
        ("Claude", call_claude),
        ("OpenAI", call_openai),
    ]
    
    for name, func in providers:
        try:
            return await func(user_prompt, project)
        except Exception as e:
            print(f"⚠️ {name} failed: {e}")
            continue
    
    raise HTTPException(status_code=500, detail="All AI providers failed")

# API Routes
@app.get("/")
async def root():
    return {"message": "D3E Agent API Server", "version": "1.0.0"}

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
