# FLUX API - Ultra Simple for Vercel Testing
import os
import json

# Environment check
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
groq_client = None

# Try to initialize Groq client
if GROQ_API_KEY:
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        groq_client = None

# Simple handler function for Vercel
def handler(event, context):
    try:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "message": "FLUX Multi-Agent System",
                "status": "running",
                "groq_configured": GROQ_API_KEY is not None,
                "groq_client_ready": groq_client is not None,
                "groq_key_length": len(GROQ_API_KEY) if GROQ_API_KEY else 0,
                "debug": {
                    "email_used": "ilamvazhuthi.pro@gmail.com",
                    "environment": os.environ.get("VERCEL_ENV", "unknown")
                }
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }

# Agents
AGENTS = {
    "sara": {"name": "Sara (Requirements Analyst)", "role": "requirements_analyst"},
    "marc": {"name": "Marc (Software Architect)", "role": "software_architect"},
    "alex": {"name": "Alex (Developer)", "role": "developer"},
    "jess": {"name": "Jess (QA Tester)", "role": "qa_tester"},
    "dave": {"name": "Dave (DevOps Engineer)", "role": "devops_engineer"},
    "emma": {"name": "Emma (Project Manager)", "role": "project_manager"},
    "robt": {"name": "Robt (Security Expert)", "role": "security_expert"}
}

@app.get("/")
async def root():
    return {
        "message": "FLUX Multi-Agent System API",
        "status": "running",
        "agents": len(AGENTS),
        "groq_configured": groq_client is not None
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "groq_api_key_configured": GROQ_API_KEY is not None,
        "groq_client_ready": groq_client is not None,
        "groq_key_length": len(GROQ_API_KEY) if GROQ_API_KEY else 0
    }

@app.get("/agents")
async def get_agents():
    return {"agents": AGENTS}

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "")
        
        if not message:
            return JSONResponse({"error": "Message is required"}, status_code=400)
        
        if not groq_client:
            return JSONResponse({
                "error": "Groq API is not configured. Please set GROQ_API_KEY environment variable.",
                "agent": "System",
                "message": "Hi! I'm currently unable to generate responses because the GROQ_API_KEY is not properly configured."
            }, status_code=200)
        
        # Simple agent selection (just use Sara for now)
        agent = AGENTS["sara"]
        
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": f"You are {agent['name']}, a helpful AI assistant."},
                    {"role": "user", "content": message}
                ],
                max_tokens=512,
                temperature=0.7
            )
            
            return {
                "agent": agent["name"],
                "role": agent["role"],
                "message": response.choices[0].message.content,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "agent": agent["name"],
                "role": agent["role"],
                "message": f"I'm having trouble generating a response right now. Error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# Vercel handler
handler = app