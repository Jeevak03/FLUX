#!/usr/bin/env python3
"""
Start the full SDLC Assistant backend server with all features
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting FLUX - Where Agents Meet Agile Backend with WebSocket support...")
    print("✨ This includes all agents and WebSocket endpoints")
    print("🔗 WebSocket endpoint: ws://localhost:8000/ws/{session_id}")
    print("🩺 Health check: http://localhost:8000/health")
    print("📋 Agent list: http://localhost:8000/agents")
    print("💬 Frontend should connect to: ws://localhost:8000")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        reload=True
    )