#!/usr/bin/env python3
"""
D3E Agent Full Application Startup Script
Starts both backend and frontend servers concurrently
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def run_backend():
    """Run the backend server"""
    try:
        print("🔧 Starting backend server...")
        subprocess.run([sys.executable, "start_backend.py"])
    except Exception as e:
        print(f"❌ Backend error: {e}")

def run_frontend():
    """Run the frontend server"""
    try:
        # Wait a bit for backend to start
        time.sleep(3)
        print("🎨 Starting frontend server...")
        subprocess.run([sys.executable, "start_frontend.py"])
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check Python
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Check if backend dependencies exist
    try:
        import fastapi
        print("✅ Backend dependencies available")
    except ImportError:
        print("❌ Backend dependencies missing. Run: pip install -r requirements.txt")
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found. Install from https://nodejs.org/")
        return False
    
    return True

def main():
    """Main application startup"""
    print("=" * 60)
    print("🚀 D3E Agent - Modern Development Interface")
    print("=" * 60)
    print()
    
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please install required dependencies.")
        sys.exit(1)
    
    print("\n🎯 Starting D3E Agent application...")
    backend_port = os.getenv("BACKEND_PORT", "8001")
    print(f"📡 Backend: http://localhost:{backend_port}")
    print("🎨 Frontend: http://localhost:3000")
    print(f"📚 API Docs: http://localhost:{backend_port}/docs")
    print("\nPress Ctrl+C to stop both servers")
    print("=" * 60)
    print()
    
    try:
        # Start backend and frontend in separate threads
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        frontend_thread = threading.Thread(target=run_frontend, daemon=True)
        
        backend_thread.start()
        frontend_thread.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down D3E Agent...")
        print("✅ Application stopped successfully")

if __name__ == "__main__":
    main()
