#!/usr/bin/env python3
"""
D3E Agent Backend Startup Script
Starts the FastAPI backend server with proper configuration
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import websockets
        import pydantic
        print("✅ All backend dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️ .env file not found. Creating template...")
        with open(".env", "w") as f:
            f.write("""# D3E Agent Environment Variables
# Add your API keys here

# AI API Keys (at least one is required)
CLAUDE_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Custom backend configuration
# BACKEND_HOST=0.0.0.0
# BACKEND_PORT=8000
""")
        print("📝 Created .env template. Please add your API keys.")
        return False
    
    print("✅ .env file found")
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting D3E Agent Backend...")
    
    # Get configuration from environment
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", "8000"))
    
    try:
        # Start uvicorn server
        cmd = [
            sys.executable, "-m", "uvicorn",
            "backend.main:app",
            "--host", host,
            "--port", str(port),
            "--reload",
            "--reload-dir", "backend",
            "--reload-dir", "Agent"
        ]
        
        print(f"📡 Backend will be available at: http://{host}:{port}")
        print("📚 API documentation: http://localhost:8000/docs")
        print("🔄 Auto-reload enabled for development")
        print("\nPress Ctrl+C to stop the server\n")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Backend server stopped")
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("=" * 50)
    print("🎯 D3E Agent Backend Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment file
    if not check_env_file():
        print("\n⚠️ Please configure your .env file with API keys before starting the backend.")
        sys.exit(1)
    
    # Start backend
    start_backend()

if __name__ == "__main__":
    main()
