# Minimal FLUX API for debugging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime

app = FastAPI(title="FLUX API - Debug Version")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "FLUX Multi-Agent System API",
        "status": "running",
        "debug": {
            "groq_key_exists": "GROQ_API_KEY" in os.environ,
            "groq_key_length": len(os.environ.get("GROQ_API_KEY", "")),
            "node_env": os.environ.get("NODE_ENV", "not_set"),
            "vercel": os.environ.get("VERCEL", "not_set"),
            "vercel_env": os.environ.get("VERCEL_ENV", "not_set")
        }
    }

@app.get("/health")
async def health():
    groq_key = os.environ.get("GROQ_API_KEY", "")
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "groq_configured": len(groq_key) > 50,
        "groq_prefix": groq_key[:10] + "..." if len(groq_key) > 10 else "not_found"
    }

@app.get("/agents")
async def agents():
    return {
        "agents": {
            "sara": {"name": "Sara (Requirements Analyst)", "status": "online"},
            "marc": {"name": "Marc (Software Architect)", "status": "online"},
            "alex": {"name": "Alex (Developer)", "status": "online"},
            "jess": {"name": "Jess (QA Tester)", "status": "online"},
            "dave": {"name": "Dave (DevOps Engineer)", "status": "online"},
            "emma": {"name": "Emma (Project Manager)", "status": "online"},
            "robt": {"name": "Robt (Security Expert)", "status": "online"}
        }
    }

# For Vercel
handler = app