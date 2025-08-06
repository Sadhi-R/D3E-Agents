#!/usr/bin/env python3
"""
D3E Agent Frontend Startup Script
Installs dependencies and starts the React development server
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_node():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js found: {version}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org/")
    return False

def check_npm():
    """Check if npm is installed"""
    # Try different npm commands for Windows compatibility
    npm_commands = ["npm", "npm.cmd", "npm.exe"]
    
    for npm_cmd in npm_commands:
        try:
            result = subprocess.run([npm_cmd, "--version"], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ npm found: {version}")
                return True
        except FileNotFoundError:
            continue
    
    # If subprocess fails, try using shell=True with the command directly
    try:
        result = subprocess.run("npm --version", capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ npm found: {version}")
            return True
    except:
        pass
    
    print("❌ npm not found. Please install Node.js which includes npm.")
    return False

def install_dependencies():
    """Install frontend dependencies"""
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ package.json not found in frontend directory")
        return False
    
    node_modules = frontend_dir / "node_modules"
    if node_modules.exists():
        print("✅ Dependencies already installed")
        return True
    
    print("📦 Installing frontend dependencies...")
    try:
        result = subprocess.run(
            "npm install",
            cwd=frontend_dir,
            shell=True,
            check=True
        )
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_frontend():
    """Start the React development server"""
    print("🚀 Starting D3E Agent Frontend...")
    
    frontend_dir = Path("frontend")
    
    try:
        print("📡 Frontend will be available at: http://localhost:3000")
        print("🔄 Auto-reload enabled for development")
        print("🔗 Backend proxy configured for API calls")
        print("\nPress Ctrl+C to stop the server\n")
        
        # Start the development server
        subprocess.run(
            "npm run dev",
            cwd=frontend_dir,
            shell=True,
            check=True
        )
        
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start frontend: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("=" * 50)
    print("🎨 D3E Agent Frontend Startup")
    print("=" * 50)
    
    # Check Node.js
    if not check_node():
        sys.exit(1)
    
    # Check npm
    if not check_npm():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Start frontend
    start_frontend()

if __name__ == "__main__":
    main()
