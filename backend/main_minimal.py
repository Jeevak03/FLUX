# main_minimal.py - Absolutely minimal multi-agent system
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("❌ ERROR: GROQ_API_KEY not found in environment variables!")
    exit(1)

# Import Groq client
try:
    from groq import Groq
    groq_client = Groq(api_key=GROQ_API_KEY)
except ImportError:
    print("❌ ERROR: groq library not installed. Run: pip install groq")
    exit(1)

# Agent definitions
AGENTS = {
    "sara": {
        "name": "Sara (Requirements Analyst)",
        "role": "requirements_analyst",
        "personality": "I'm Sara, your Requirements Analyst. I help analyze and document project requirements, user stories, and specifications."
    },
    "marc": {
        "name": "Marc (Software Architect)", 
        "role": "software_architect",
        "personality": "I'm Marc, your Software Architect. I design system architecture, technical specifications, and ensure scalable solutions."
    },
    "alex": {
        "name": "Alex (Developer)",
        "role": "developer", 
        "personality": "I'm Alex, your Developer. I write code, implement features, and turn requirements into working software."
    },
    "jess": {
        "name": "Jess (QA Tester)",
        "role": "qa_tester",
        "personality": "I'm Jess, your QA Tester. I test software, find bugs, and ensure quality standards are met."
    },
    "dave": {
        "name": "Dave (DevOps Engineer)",
        "role": "devops_engineer", 
        "personality": "I'm Dave, your DevOps Engineer. I handle deployment, infrastructure, CI/CD pipelines, and system operations."
    },
    "emma": {
        "name": "Emma (Project Manager)",
        "role": "project_manager",
        "personality": "I'm Emma, your Project Manager. I coordinate teams, manage timelines, and ensure projects stay on track."
    },
    "robt": {
        "name": "Robt (Security Expert)",
        "role": "security_expert",
        "personality": "I'm Robt, your Security Expert. I assess security risks, implement security measures, ensure applications are secure."
    }
}

# Active WebSocket connections
active_connections = {}

app = FastAPI(title="FLUX - Minimal Multi-Agent System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def detect_target_agents(message: str) -> list:
    """
    Detect which agents are being called directly.
    Simple string matching - no complex regex or state management.
    """
    message_lower = message.lower()
    called_agents = []
    
    print(f"[ROUTE] 🔍 Analyzing message: '{message}'")
    
    # Check for direct agent calls
    for agent_key, agent_info in AGENTS.items():
        if agent_key in message_lower or agent_info["name"].lower() in message_lower:
            called_agents.append(agent_key)
            print(f"[ROUTE] ✅ DIRECT: Found '{agent_key}' → {agent_info['name']}")
    
    # Special handling for common variations
    if "rob" in message_lower and "robt" not in called_agents:
        called_agents.append("robt")
        print(f"[ROUTE] ✅ ALIAS: 'rob' → Robt (Security Expert)")
    
    # If no specific agents called, don't default to anyone
    if not called_agents:
        print(f"[ROUTE] ⚠️ No direct agent name detected - ending workflow")
    
    return called_agents

async def generate_agent_response(agent_key: str, message: str, context: dict = None) -> str:
    """Generate response from specific agent using Groq"""
    try:
        agent = AGENTS[agent_key]
        print(f"[AGENT] 💭 {agent['name']} generating response...")
        
        # Create system prompt for the agent
        system_prompt = f"""You are {agent['name']}, a {agent['role']} in a software development team.

{agent['personality']}

Instructions:
- Respond as {agent['name']} in character
- Keep responses concise but helpful
- Focus on your area of expertise
- Be collaborative and professional
- Don't mention other agents unless directly relevant"""

        # Generate response using Groq
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=1024,
            temperature=0.7
        )
        
        agent_response = response.choices[0].message.content
        print(f"[AGENT] ✅ {agent['name']} response generated: {len(agent_response)} chars")
        return agent_response
        
    except Exception as e:
        print(f"[AGENT] ❌ Error generating response for {agent_key}: {e}")
        return f"Sorry, I'm having trouble responding right now. Error: {e}"

async def send_websocket_message(websocket: WebSocket, message_type: str, data: dict):
    """Send message via WebSocket"""
    try:
        message = {
            "type": message_type,
            "timestamp": datetime.now().isoformat(),
            **data
        }
        await websocket.send_text(json.dumps(message))
    except Exception as e:
        print(f"[WS] ❌ Error sending message: {e}")

@app.on_event("startup")
async def startup_event():
    print("🚀 FLUX - Minimal Multi-Agent System starting up...")
    print("✅ Direct agent routing enabled!")
    print("✅ No LangGraph complexity!")
    print("✅ No caching issues!")

@app.get("/")
async def root():
    return {
        "message": "FLUX - Minimal Multi-Agent System", 
        "status": "running",
        "architecture": "Direct routing (minimal)",
        "agents": list(AGENTS.keys())
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat()
    }

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """Minimal WebSocket endpoint with direct agent routing"""
    try:
        print(f"\n{'='*60}")
        print(f"[WS] 🔌 Connection: {session_id}")
        print(f"[WS] 🚀 MINIMAL SYSTEM - Direct routing only")
        print(f"{'='*60}")
        
        # Accept connection
        await websocket.accept()
        active_connections[session_id] = websocket
        
        # Send connection confirmation
        await send_websocket_message(websocket, "status", {
            "status": "connected",
            "message": "Connected to Minimal Multi-Agent System"
        })
        
        # Message handling loop
        while True:
            try:
                # Receive message
                raw_message = await websocket.receive_text()
                print(f"[WS] 📨 Raw message: {raw_message[:100]}...")
                
                # Parse JSON
                try:
                    message_data = json.loads(raw_message)
                    user_message = message_data.get("request", "")
                except json.JSONDecodeError as e:
                    await send_websocket_message(websocket, "agent_response", {
                        "agent": "system",
                        "message": f"Invalid JSON format: {e}",
                        "status": "error"
                    })
                    continue
                
                if not user_message:
                    continue
                
                # Send processing status
                await send_websocket_message(websocket, "status", {
                    "status": "processing",
                    "message": "Processing your request..."
                })
                
                # Detect target agents (SIMPLE DETECTION)
                target_agents = detect_target_agents(user_message)
                
                if not target_agents:
                    # No agents detected - just acknowledge
                    await send_websocket_message(websocket, "status", {
                        "status": "completed",
                        "message": "No specific agent requested"
                    })
                    continue
                
                # Generate responses from detected agents
                print(f"[WS] 🎯 Generating responses from: {target_agents}")
                
                for agent_key in target_agents:
                    try:
                        response = await generate_agent_response(agent_key, user_message)
                        agent_name = AGENTS[agent_key]["name"]
                        
                        # Send agent response
                        await send_websocket_message(websocket, "agent_response", {
                            "agent": agent_name,
                            "message": response,
                            "status": "success"
                        })
                        
                        print(f"[WS] ✅ Sent response from {agent_name}")
                        
                    except Exception as agent_error:
                        print(f"[WS] ❌ Error with agent {agent_key}: {agent_error}")
                        await send_websocket_message(websocket, "agent_response", {
                            "agent": AGENTS[agent_key]["name"],
                            "message": f"Sorry, I'm having trouble responding: {agent_error}",
                            "status": "error"
                        })
                
                # Send completion status
                await send_websocket_message(websocket, "status", {
                    "status": "completed",
                    "message": f"Responses from: {', '.join([AGENTS[k]['name'] for k in target_agents])}"
                })
                
            except WebSocketDisconnect:
                print(f"[WS] 👋 Client disconnected: {session_id}")
                break
                
            except Exception as e:
                print(f"[WS] ❌ Message processing error: {e}")
                try:
                    await send_websocket_message(websocket, "agent_response", {
                        "agent": "system",
                        "message": f"Error processing message: {e}",
                        "status": "error"
                    })
                except Exception:
                    print(f"[WS] ❌ Failed to send error message")
                    break
    
    except Exception as e:
        print(f"[WS] ❌ Fatal WebSocket error: {e}")
    
    finally:
        # Clean up connection
        if session_id in active_connections:
            del active_connections[session_id]
        print(f"[WS] 🧹 Cleaned up connection: {session_id}")

@app.get("/agents")
async def list_agents():
    """List all available agents"""
    return {
        "agents": {k: v["name"] for k, v in AGENTS.items()},
        "routing": "Direct string matching",
        "system": "Minimal"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FLUX Minimal Multi-Agent System...")
    print("✅ Zero complexity - just direct routing!")
    uvicorn.run("main_minimal:app", host="127.0.0.1", port=8000, reload=False, log_level="info")