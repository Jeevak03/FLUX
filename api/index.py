# Vercel serverless function handler for FLUX backend
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
from typing import Dict, List
import asyncio
from datetime import datetime

# Import the main backend logic
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from groq import Groq
    
    # Get Groq API key from environment
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable is required")
    
    groq_client = Groq(api_key=GROQ_API_KEY)
except ImportError:
    raise ImportError("groq library not installed")

# Agent definitions (simplified for serverless)
AGENTS = {
    "sara": {
        "name": "Sara (Requirements Analyst)",
        "role": "requirements_analyst",
        "personality": "I'm Sara, your Requirements Analyst. I work closely with the team to analyze and document project requirements, user stories, and specifications."
    },
    "marc": {
        "name": "Marc (Software Architect)", 
        "role": "software_architect",
        "personality": "I'm Marc, your Software Architect. I design system architecture and technical specifications."
    },
    "alex": {
        "name": "Alex (Developer)",
        "role": "developer", 
        "personality": "I'm Alex, your Developer. I write code and implement features based on Marc's architecture and Sara's requirements."
    },
    "jess": {
        "name": "Jess (QA Tester)",
        "role": "qa_tester",
        "personality": "I'm Jess, your QA Tester. I ensure quality through comprehensive testing."
    },
    "dave": {
        "name": "Dave (DevOps Engineer)",
        "role": "devops_engineer", 
        "personality": "I'm Dave, your DevOps Engineer. I handle deployment, infrastructure, and CI/CD pipelines."
    },
    "emma": {
        "name": "Emma (Project Manager)",
        "role": "project_manager",
        "personality": "I'm Emma, your Project Manager. I coordinate the entire team and manage timelines."
    },
    "robt": {
        "name": "Robt (Security Expert)",
        "role": "security_expert",
        "personality": "I'm Robt, your Security Expert. I assess security risks and implement protective measures."
    }
}

app = FastAPI(title="FLUX API - Vercel Deployment")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def detect_target_agents(message: str) -> List[str]:
    """Detect which agents are being called"""
    message_lower = message.lower()
    called_agents = []
    
    # Check for collaboration keywords
    collaboration_keywords = [
        "everyone", "all agents", "team", "collaborate", "work together",
        "call your team", "team members", "all of you", "everybody"
    ]
    
    is_collaboration_request = any(keyword in message_lower for keyword in collaboration_keywords)
    
    if is_collaboration_request:
        return list(AGENTS.keys())
    
    # Check for direct agent mentions
    agent_name_map = {
        "sara": "sara", "sarah": "sara",
        "marc": "marc", "marcus": "marc", "mark": "marc",
        "alex": "alex", "alexander": "alex",
        "jess": "jess", "jessica": "jess",
        "dave": "dave", "david": "dave",
        "emma": "emma", "emily": "emma",
        "robt": "robt", "robert": "robt", "rob": "robt"
    }
    
    for name_variant, agent_key in agent_name_map.items():
        if name_variant in message_lower:
            called_agents.append(agent_key)
    
    return called_agents if called_agents else ["sara"]  # Default to Sara

async def generate_agent_response(agent_key: str, message: str, context: dict = None) -> str:
    """Generate response from specific agent"""
    if agent_key not in AGENTS:
        return "Agent not found."
    
    agent = AGENTS[agent_key]
    
    try:
        system_prompt = f"""You are {agent['name']}, a specialized AI agent with this personality:

{agent['personality']}

Respond naturally and professionally. Keep responses concise but helpful. Always stay in character as {agent['name']}.
"""
        
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=512,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"I'm having trouble responding right now. Error: {str(e)}"

@app.get("/")
async def root():
    return {"message": "FLUX Multi-Agent System API", "status": "running", "agents": len(AGENTS)}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/agents")
async def get_agents():
    return {"agents": AGENTS}

@app.post("/chat")
async def chat_endpoint(request: Request):
    """REST endpoint for chat (fallback for WebSocket)"""
    try:
        data = await request.json()
        message = data.get("message", "")
        
        if not message:
            return JSONResponse({"error": "Message is required"}, status_code=400)
        
        # Detect target agents
        target_agents = detect_target_agents(message)
        
        # Generate responses
        responses = []
        for agent_key in target_agents:
            response = await generate_agent_response(agent_key, message)
            responses.append({
                "agent": AGENTS[agent_key]["name"],
                "role": AGENTS[agent_key]["role"],
                "message": response,
                "timestamp": datetime.now().isoformat()
            })
        
        return {"responses": responses}
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# WebSocket support (limited in serverless, but keeping for compatibility)
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint - limited in serverless environment"""
    await websocket.accept()
    try:
        await websocket.send_json({
            "type": "system",
            "message": "Connected to FLUX API (Serverless mode - limited WebSocket support)"
        })
        
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "user_message":
                message = message_data.get("message", "")
                target_agents = detect_target_agents(message)
                
                for agent_key in target_agents:
                    response = await generate_agent_response(agent_key, message)
                    await websocket.send_json({
                        "type": "agent_response",
                        "agent": AGENTS[agent_key]["name"],
                        "role": AGENTS[agent_key]["role"],
                        "message": response,
                        "timestamp": datetime.now().isoformat()
                    })
                    
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": f"Error: {str(e)}"
        })

# Export for Vercel
handler = app