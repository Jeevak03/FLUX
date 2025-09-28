# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from utils.websocket_manager import WebSocketManager
from utils.session_manager import SessionManager
from workflows.sdlc_workflow import SDLCWorkflow
from models.schemas import UserRequest, AgentMessage
from routes.github_routes import router as github_router

websocket_manager = WebSocketManager()
session_manager = SessionManager()
sdlc_workflow = None  # Pre-initialized at startup for faster responses

def get_sdlc_workflow():
    global sdlc_workflow
    # Force recreation to pick up latest workflow changes during development
    print("[INIT] Creating new SDLC workflow...")
    sdlc_workflow = SDLCWorkflow()
    print("[INIT] SDLC workflow ready")
    return sdlc_workflow

app = FastAPI(title="FLUX - Where Agents Meet Agile")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include GitHub API routes
app.include_router(github_router)

@app.on_event("startup")
async def startup_event():
    print("FLUX - Where Agents Meet Agile starting up...")
    # Pre-initialize workflow to avoid first-request delay
    workflow = get_sdlc_workflow()
    print("[STARTUP] Pre-initialized workflow for faster responses")
    
    # Warm up Groq models for faster first responses
    try:
        from models.groq_models import GroqModelManager
        groq_manager = GroqModelManager()
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, groq_manager.warm_up_models)
        print("[STARTUP] Started model warm-up process")
    except Exception as e:
        print(f"[STARTUP] Model warm-up failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    print("FLUX - Where Agents Meet Agile shutting down...")

@app.get("/")
async def root():
    return {"message": "FLUX - Where Agents Meet Agile API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint with detailed logging and initial ack."""
    try:
        print(f"[WS] Incoming connection session={session_id}")
        await websocket_manager.connect(websocket, session_id)
        print(f"[WS] Accepted session={session_id}")
        # Immediate ack so frontend can confirm open
        await websocket_manager.send_status_update(session_id, "connected", "WebSocket connected")

        session_data = session_manager.get_session(session_id)
        if not session_data:
            session_manager.create_session(session_id)
            print(f"[WS] Created session store {session_id}")
        else:
            print(f"[WS] Loaded existing session store {session_id}")

        while True:
            try:
                raw = await websocket.receive_text()
            except WebSocketDisconnect:
                raise
            except Exception as rec_err:
                print(f"[WS] Receive error session={session_id}: {rec_err}")
                await websocket_manager.send_agent_response(session_id, "system", f"Receive error: {rec_err}", "error")
                continue

            try:
                message_data = json.loads(raw)
            except json.JSONDecodeError as je:
                await websocket_manager.send_agent_response(session_id, "system", f"Invalid JSON: {je}", "error")
                continue

            try:
                user_request = UserRequest(**message_data)
            except Exception as e:
                await websocket_manager.send_agent_response(session_id, "system", f"Invalid request format: {e}", "error")
                continue

            session_manager.update_session(session_id, {
                "last_request": user_request.dict(),
                "project_context": user_request.context.dict() if user_request.context else {}
            })

            await websocket_manager.send_status_update(session_id, "processing", "Initializing agents...")

            try:
                print(f"[WS] Received request: {user_request}")
                print(f"[WS] Requested agents: {user_request.requested_agents}")
                
                initial_state = {
                    "user_request": user_request.request,
                    "current_phase": "initial",
                    "agent_outputs": {},
                    "conversation_history": [msg.dict() for msg in user_request.history],
                    "project_context": user_request.context.dict() if user_request.context else {},
                    "uploaded_files": [file.dict() for file in user_request.uploaded_files],
                    "next_agent": "",
                    "final_response": "",
                    "requested_agents": user_request.requested_agents
                }
                if user_request.requested_agents:
                    initial_state["current_phase"] = "collaboration"

                await websocket_manager.send_status_update(session_id, "processing", "Running agent workflow...")
                workflow = get_sdlc_workflow()
                
                # Track response count for progress updates
                response_count = 0
                all_responses = {}  # Track all responses across state updates
                
                print(f"[WS] Starting workflow execution with state: {list(initial_state.keys())}")
                try:
                    async for state_update in workflow.workflow.astream(initial_state):
                        current_state = state_update
                        print(f"[WS] State update keys: {list(current_state.keys())}")
                        
                        # LangGraph returns node results, but we need the actual state.
                        # Each node result should contain the updated state
                        for node_name, node_result in current_state.items():
                            print(f"[WS] Checking node {node_name}, result type: {type(node_result)}")
                            
                            # The node result IS the updated state for that node
                            if isinstance(node_result, dict) and "agent_outputs" in node_result:
                                current_outputs = node_result["agent_outputs"]
                                print(f"[WS] Found agent_outputs in {node_name}: {list(current_outputs.keys())}")
                                
                                for agent_name, response in current_outputs.items():
                                    if agent_name not in all_responses and response and response.strip():  # New non-empty response
                                        all_responses[agent_name] = response
                                        response_count += 1
                                        print(f"[WS] New response from {agent_name}: {len(str(response))} chars")
                                        
                                        # Send immediate status update per agent
                                        await websocket_manager.send_status_update(session_id, "processing", f"{agent_name} is responding...")
                                        
                                        # Send the complete response
                                        response_str = str(response)
                                        await websocket_manager.send_agent_response(session_id, agent_name, response_str)
                                        
                                        # Broadcast collaboration update when new agents join
                                        current_active_agents = list(all_responses.keys())
                                        if len(current_active_agents) > len(user_request.requested_agents):
                                            print(f"[WS] A2A triggered - broadcasting new active agents: {current_active_agents}")
                                            await websocket_manager.broadcast_collaboration(session_id, current_active_agents, "active")
                                        
                                        message = AgentMessage(
                                            type="agent_response",
                                            agent=agent_name,
                                            message=response_str,
                                            timestamp=datetime.now().isoformat()
                                        )
                                        session_manager.add_message_to_history(session_id, message.dict())
                        
                        if len(user_request.requested_agents) > 1:
                            await websocket_manager.broadcast_collaboration(session_id, user_request.requested_agents, "active")
                
                except Exception as workflow_error:
                    print(f"[WS] Workflow execution error: {workflow_error}")
                    print(f"[WS] Workflow error type: {type(workflow_error).__name__}")
                    raise workflow_error

                await websocket_manager.send_status_update(session_id, "completed", f"Completed with {response_count} agent responses")
                session_manager.update_session(session_id, {
                    "last_completion": datetime.now().isoformat(),
                    "current_phase": current_state.get("current_phase", "completed")
                })
            except Exception as e:
                error_msg = f"Error processing request: {e}"
                print(f"[WS] Processing error session={session_id}: {error_msg}")
                print(f"[WS] Error details: {type(e).__name__}: {str(e)}")
                
                # Handle specific conversation management scenarios
                if "Invalid argument" in str(e) or "Errno 22" in str(e):
                    print(f"[WS] Detected conversation management scenario - attempting graceful handling")
                    try:
                        # Try to send a helpful response instead of an error
                        helpful_message = "I understand you want to manage the conversation participants. Let me help coordinate that for you."
                        await websocket_manager.send_agent_response(session_id, "system", helpful_message, "info")
                        await websocket_manager.send_status_update(session_id, "ready", "Ready for your next request")
                        return  # Don't send error, just continue
                    except Exception:
                        pass  # Fall through to error handling
                
                import traceback
                print(f"[WS] Full traceback: {traceback.format_exc()}")
                
                # Send user-friendly error message
                user_friendly_error = "I'm having trouble processing that request. Please try rephrasing or let me know specifically which agents you'd like to work with."
                await websocket_manager.send_agent_response(session_id, "system", user_friendly_error, "error")
                await websocket_manager.send_status_update(session_id, "error", "Please try again")
    except WebSocketDisconnect:
        print(f"[WS] Disconnect session={session_id}")
        websocket_manager.disconnect(session_id)
    except Exception as fatal:
        print(f"[WS] Fatal error session={session_id}: {fatal}")
        try:
            await websocket_manager.send_agent_response(session_id, "system", f"Fatal error: {fatal}", "error")
        except Exception:
            pass
        websocket_manager.disconnect(session_id)

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

if __name__ == "__main__":
    import uvicorn
    print("[MAIN] Running uvicorn directly from main.py")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False, log_level="info")