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
        "personality": "I'm Sara, your Requirements Analyst. I work closely with the team to analyze and document project requirements, user stories, and specifications. I often collaborate with Marc on architecture alignment and Emma on project planning."
    },
    "marc": {
        "name": "Marc (Software Architect)", 
        "role": "software_architect",
        "personality": "I'm Marc, your Software Architect. I design system architecture and technical specifications. I work closely with Sara on requirements, Alex on implementation feasibility, and Robt on security architecture."
    },
    "alex": {
        "name": "Alex (Developer)",
        "role": "developer", 
        "personality": "I'm Alex, your Developer. I write code and implement features based on Marc's architecture and Sara's requirements. I collaborate with Jess on testing strategies and Dave on deployment considerations."
    },
    "jess": {
        "name": "Jess (QA Tester)",
        "role": "qa_tester",
        "personality": "I'm Jess, your QA Tester. I ensure quality through comprehensive testing. I work closely with Alex on test cases, Sara on requirement validation, and Robt on security testing."
    },
    "dave": {
        "name": "Dave (DevOps Engineer)",
        "role": "devops_engineer", 
        "personality": "I'm Dave, your DevOps Engineer. I handle deployment, infrastructure, and CI/CD pipelines. I collaborate with Alex on deployment strategies, Marc on infrastructure requirements, and Robt on security measures."
    },
    "emma": {
        "name": "Emma (Project Manager)",
        "role": "project_manager",
        "personality": "I'm Emma, your Project Manager. I coordinate the entire team, manage timelines, and ensure smooth collaboration between Sara, Marc, Alex, Jess, Dave, and Robt. I facilitate team meetings and track progress."
    },
    "robt": {
        "name": "Robt (Security Expert)",
        "role": "security_expert",
        "personality": "I'm Robt, your Security Expert. I assess security risks and implement protective measures. I work with Marc on secure architecture, Alex on secure coding practices, and Dave on infrastructure security."
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
    Detect which agents are being called directly or if collaboration is needed.
    Enhanced with multi-agent collaboration support.
    """
    message_lower = message.lower()
    called_agents = []
    
    print(f"[ROUTE] 🔍 Analyzing message: '{message}'")
    
    # Check for collaboration keywords
    collaboration_keywords = [
        "everyone", "all agents", "team", "collaborate", "work together",
        "call your team", "team members", "all of you", "everybody",
        "discuss", "brainstorm", "meeting", "huddle"
    ]
    
    is_collaboration_request = any(keyword in message_lower for keyword in collaboration_keywords)
    
    if is_collaboration_request:
        print(f"[COLLAB] 🤝 Collaboration request detected - involving all agents")
        return list(AGENTS.keys())  # Return all agents for collaboration
    
    # Check for direct agent calls
    for agent_key, agent_info in AGENTS.items():
        if agent_key in message_lower or agent_info["name"].lower() in message_lower:
            called_agents.append(agent_key)
            print(f"[ROUTE] ✅ DIRECT: Found '{agent_key}' → {agent_info['name']}")
    
    # Special handling for common variations
    if "rob" in message_lower and "robt" not in called_agents:
        called_agents.append("robt")
        print(f"[ROUTE] ✅ ALIAS: 'rob' → Robt (Security Expert)")
    
    # If no specific agents called and no collaboration, use intelligent routing
    if not called_agents:
        called_agents = determine_relevant_agents(message_lower)
        if called_agents:
            print(f"[ROUTE] 🧠 INTELLIGENT: Auto-selected agents: {', '.join(called_agents)}")
        else:
            print(f"[ROUTE] ⚠️ No agents determined - ending workflow")
    
    return called_agents

def determine_relevant_agents(message: str) -> list:
    """
    Intelligently determine which agents should handle the request based on content.
    """
    # Keywords that indicate which agents should be involved
    agent_keywords = {
        "sara": ["requirements", "specification", "user story", "analyze", "document", "scope", "gather"],
        "marc": ["architecture", "design", "system", "technical", "scalability", "structure", "framework"],
        "alex": ["code", "implement", "develop", "programming", "bug", "feature", "coding", "build"],
        "jess": ["test", "testing", "quality", "bug", "validation", "verify", "qa", "check"],
        "dave": ["deploy", "deployment", "infrastructure", "server", "devops", "pipeline", "production"],
        "emma": ["project", "manage", "timeline", "coordination", "planning", "schedule", "milestone"],
        "robt": ["security", "secure", "vulnerability", "protect", "authentication", "authorization", "risk"]
    }
    
    relevant_agents = []
    
    for agent_key, keywords in agent_keywords.items():
        if any(keyword in message for keyword in keywords):
            relevant_agents.append(agent_key)
    
    # If it's a complex request, involve multiple key agents
    complex_indicators = ["project", "system", "application", "solution", "problem", "issue"]
    if any(indicator in message for indicator in complex_indicators) and len(relevant_agents) < 2:
        # For complex requests, ensure we have key roles
        base_team = ["sara", "marc", "alex"]  # Requirements, Architecture, Development
        for agent in base_team:
            if agent not in relevant_agents:
                relevant_agents.append(agent)
    
    return relevant_agents

async def generate_agent_response(agent_key: str, message: str, context: dict = None, collaborating_agents: list = None, is_followup: bool = False) -> str:
    """Generate response from specific agent using Groq with team awareness"""
    try:
        agent = AGENTS[agent_key]
        print(f"[AGENT] 💭 {agent['name']} generating response...")
        
        # Build team context
        team_info = get_team_context(agent_key, collaborating_agents)
        collaboration_context = ""
        
        if collaborating_agents and len(collaborating_agents) > 1:
            other_agents = [AGENTS[ak]["name"] for ak in collaborating_agents if ak != agent_key]
            if other_agents:
                collaboration_context = f"\n\nTEAM COLLABORATION CONTEXT:\n- You are working with: {', '.join(other_agents)}\n- This is a collaborative response where multiple team members are contributing\n- Acknowledge your teammates and build upon their expertise\n- You can suggest involving other team members if needed for specific tasks"
        
        if is_followup:
            collaboration_context += "\n- This is a follow-up response after initial collaboration"
        
        # Create enhanced system prompt with team awareness
        system_prompt = f"""You are {agent['name']}, a {agent['role']} in a software development team.

{agent['personality']}

TEAM MEMBERS YOU WORK WITH:
{team_info}

Instructions:
- Respond as {agent['name']} in character
- Keep responses concise but helpful  
- Focus on your area of expertise
- Be collaborative and acknowledge your team members
- When appropriate, suggest involving other team members: "I recommend we get [Name] involved for [specific task]"
- If asked about the team, mention your colleagues and their roles
- Work collaboratively - build on others' ideas and expertise{collaboration_context}"""

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
        
        # Check if agent wants to involve other team members
        additional_agents = extract_agent_mentions(agent_response, agent_key)
        if additional_agents:
            print(f"[COLLAB] 🔗 {agent['name']} mentioned: {', '.join([AGENTS[a]['name'] for a in additional_agents])}")
            return agent_response, additional_agents
        
        return agent_response
        
    except Exception as e:
        print(f"[AGENT] ❌ Error generating response for {agent_key}: {e}")
        return f"Sorry, I'm having trouble responding right now. Error: {e}"

def get_team_context(current_agent: str, collaborating_agents: list = None) -> str:
    """Generate team context information for the agent"""
    team_members = []
    
    for agent_key, agent_info in AGENTS.items():
        if agent_key != current_agent:
            role_desc = {
                "sara": "handles requirements gathering and user story analysis",
                "marc": "designs system architecture and technical specifications", 
                "alex": "implements features and writes code",
                "jess": "ensures quality through testing and validation",
                "dave": "manages deployment and infrastructure operations",
                "emma": "coordinates project timelines and team management",
                "robt": "oversees security measures and risk assessment"
            }
            
            status = "👥 ACTIVE" if collaborating_agents and agent_key in collaborating_agents else "📋 AVAILABLE"
            team_members.append(f"- {agent_info['name']} ({status}): {role_desc.get(agent_key, agent_info['role'])}")
    
    return "\n".join(team_members)

def extract_agent_mentions(response: str, current_agent: str) -> list:
    """Extract mentions of other agents from a response"""
    mentioned_agents = []
    response_lower = response.lower()
    
    # Look for phrases that suggest involving other agents
    for agent_key, agent_info in AGENTS.items():
        if agent_key != current_agent:
            agent_name = agent_info["name"].lower()
            first_name = agent_name.split()[0]  # Extract first name
            
            # Check for direct mentions or role-based suggestions
            mention_patterns = [
                f"get {first_name}",
                f"involve {first_name}",
                f"ask {first_name}",
                f"work with {first_name}",
                f"bring in {first_name}",
                f"{first_name} should",
                f"{first_name} can help",
                f"recommend {first_name}"
            ]
            
            if any(pattern in response_lower for pattern in mention_patterns):
                mentioned_agents.append(agent_key)
    
    return mentioned_agents

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
                is_collaboration = len(target_agents) > 1
                print(f"[WS] 🎯 Generating responses from: {target_agents}")
                if is_collaboration:
                    print(f"[COLLAB] 🤝 Multi-agent collaboration mode activated")
                
                additional_agents_to_call = []
                
                for agent_key in target_agents:
                    try:
                        result = await generate_agent_response(
                            agent_key, 
                            user_message, 
                            collaborating_agents=target_agents,
                            is_followup=False
                        )
                        
                        # Handle both single response and response with additional agents
                        if isinstance(result, tuple):
                            response, mentioned_agents = result
                            additional_agents_to_call.extend(mentioned_agents)
                        else:
                            response = result
                        
                        agent_name = AGENTS[agent_key]["name"]
                        
                        # Send agent response
                        await send_websocket_message(websocket, "agent_response", {
                            "agent": agent_key,  # Use agent_key instead of agent_name for consistency
                            "message": response,
                            "status": "success",
                            "collaboration": is_collaboration
                        })
                        
                        # Check if agent is leaving based on response content
                        response_lower = response.lower()
                        leaving_keywords = ["i'll step away", "leaving the chat", "signing off", 
                                          "catch up with you all later", "i'll be offline", 
                                          "stepping away", "going offline"]
                        
                        if any(keyword in response_lower for keyword in leaving_keywords):
                            print(f"[STATUS] 👋 {agent_name} is going offline")
                            await send_websocket_message(websocket, "agent_status", {
                                "agent": agent_key,
                                "status": "offline",
                                "message": f"{agent_name} has gone offline"
                            })
                        
                        print(f"[WS] ✅ Sent response from {agent_name}")
                        
                    except Exception as agent_error:
                        print(f"[WS] ❌ Error with agent {agent_key}: {agent_error}")
                        await send_websocket_message(websocket, "agent_response", {
                            "agent": AGENTS[agent_key]["name"],
                            "message": f"Sorry, I'm having trouble responding: {agent_error}",
                            "status": "error"
                        })
                
                # Handle agent-to-agent collaboration
                if additional_agents_to_call:
                    additional_agents_to_call = list(set(additional_agents_to_call))  # Remove duplicates
                    additional_agents_to_call = [a for a in additional_agents_to_call if a not in target_agents]  # Don't repeat
                    
                    if additional_agents_to_call:
                        print(f"[COLLAB] 🔗 Following up with mentioned agents: {', '.join([AGENTS[a]['name'] for a in additional_agents_to_call])}")
                        
                        followup_message = f"Following up on the previous discussion: {user_message}"
                        for agent_key in additional_agents_to_call:
                            try:
                                all_involved = target_agents + additional_agents_to_call
                                response = await generate_agent_response(
                                    agent_key,
                                    followup_message,
                                    collaborating_agents=all_involved,
                                    is_followup=True
                                )
                                
                                if isinstance(response, tuple):
                                    response = response[0]  # Just get the response text
                                
                                agent_name = AGENTS[agent_key]["name"]
                                
                                await send_websocket_message(websocket, "agent_response", {
                                    "agent": agent_key,  # Use agent_key for consistency
                                    "message": response,
                                    "status": "success",
                                    "collaboration": True,
                                    "followup": True
                                })
                                
                                # Check if follow-up agent is leaving based on response content
                                response_lower = response.lower()
                                leaving_keywords = ["i'll step away", "leaving the chat", "signing off", 
                                                  "catch up with you all later", "i'll be offline", 
                                                  "stepping away", "going offline"]
                                
                                if any(keyword in response_lower for keyword in leaving_keywords):
                                    print(f"[STATUS] 👋 {agent_name} is going offline (follow-up)")
                                    await send_websocket_message(websocket, "agent_status", {
                                        "agent": agent_key,
                                        "status": "offline",
                                        "message": f"{agent_name} has gone offline"
                                    })
                                
                                print(f"[COLLAB] ✅ Sent follow-up from {agent_name}")
                                
                            except Exception as agent_error:
                                print(f"[COLLAB] ❌ Error with follow-up agent {agent_key}: {agent_error}")
                        
                        target_agents.extend(additional_agents_to_call)
                
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