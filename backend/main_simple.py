# main_simple.py - Simplified main without LangGraph complexity
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from utils.websocket_manager import WebSocketManager
from utils.session_manager import SessionManager
from core.simple_websocket_handler import SimpleWebSocketHandler
from routes.github_routes import router as github_router

# Initialize managers
websocket_manager = WebSocketManager()
session_manager = SessionManager()
ws_handler = SimpleWebSocketHandler(websocket_manager, session_manager)

app = FastAPI(title="FLUX - Simple Multi-Agent System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include GitHub API routes
app.include_router(github_router)

@app.on_event("startup")
async def startup_event():
    print("🚀 FLUX - Simple Multi-Agent System starting up...")
    print("✅ No LangGraph workflow caching issues!")
    print("✅ Direct agent routing enabled!")

@app.on_event("shutdown")
async def shutdown_event():
    print("👋 FLUX - Simple Multi-Agent System shutting down...")

@app.get("/")
async def root():
    return {
        "message": "FLUX - Simple Multi-Agent System", 
        "status": "running",
        "architecture": "Direct routing (no LangGraph)",
        "agents": ["Sara", "Marc", "Alex", "Jess", "Dave", "Emma", "Robt"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "system": "simple_multi_agent"
    }

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    Simplified WebSocket endpoint with direct agent routing.
    No complex workflow state management or LangGraph caching.
    """
    try:
        print(f"\n{'='*60}")
        print(f"[WS] 🔌 Connection request: {session_id}")
        print(f"[WS] 🚀 Using SIMPLE routing (no LangGraph)")
        print(f"{'='*60}")
        
        # Accept connection
        await websocket_manager.connect(websocket, session_id)
        
        # Send immediate connection confirmation
        await websocket_manager.send_status_update(
            session_id, "connected", "Connected to Simple Multi-Agent System"
        )
        
        # Initialize or load session
        session_data = session_manager.get_session(session_id)
        if not session_data:
            session_manager.create_session(session_id)
            print(f"[WS] ✅ Created new session: {session_id}")
        else:
            print(f"[WS] ♻️  Loaded existing session: {session_id}")
        
        # Message handling loop
        while True:
            try:
                # Receive message
                raw_message = await websocket.receive_text()
                print(f"[WS] 📨 Raw message received: {raw_message[:100]}...")
                
                # Parse JSON
                try:
                    message_data = json.loads(raw_message)
                except json.JSONDecodeError as e:
                    await websocket_manager.send_agent_response(
                        session_id, "system", f"Invalid JSON format: {e}", "error"
                    )
                    continue
                
                # Handle message using simple handler (NO LANGGRAPH)
                await ws_handler.handle_message(session_id, message_data)
                
            except WebSocketDisconnect:
                print(f"[WS] 👋 Client disconnected: {session_id}")
                break
                
            except Exception as e:
                print(f"[WS] ❌ Message processing error: {e}")
                try:
                    await websocket_manager.send_agent_response(
                        session_id, "system", 
                        f"Error processing message: {e}", "error"
                    )
                except Exception:
                    print(f"[WS] ❌ Failed to send error message: {e}")
                    break
    
    except Exception as e:
        print(f"[WS] ❌ Fatal WebSocket error: {e}")
    
    finally:
        # Clean up connection
        websocket_manager.disconnect(session_id)
        print(f"[WS] 🧹 Cleaned up connection: {session_id}")

# Session management endpoints
@app.get("/sessions/{session_id}")
async def get_session_info(session_id: str):
    """Get session information"""
    session_data = session_manager.get_session(session_id)
    if session_data:
        return {"session_id": session_id, "data": session_data}
    return {"error": "Session not found"}

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    success = session_manager.delete_session(session_id)
    return {"success": success}

@app.get("/sessions")
async def list_sessions():
    """List all active sessions"""
    sessions = session_manager.get_active_sessions()
    return {"active_sessions": sessions}

# Agent status endpoint
@app.get("/agents")
async def list_agents():
    """List all available agents"""
    return {
        "agents": {
            "sara": "Sara (Requirements Analyst)",
            "marc": "Marc (Software Architect)",
            "alex": "Alex (Developer)", 
            "jess": "Jess (QA Tester)",
            "dave": "Dave (DevOps Engineer)",
            "emma": "Emma (Project Manager)",
            "robt": "Robt (Security Expert)"
        },
        "routing": "Direct (no workflow caching)",
        "system": "SimpleAgentRouter"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FLUX Simple Multi-Agent System...")
    print("✅ No LangGraph workflow complexity!")
    print("✅ Direct agent routing enabled!")
    uvicorn.run("main_simple:app", host="127.0.0.1", port=8000, reload=False, log_level="info")