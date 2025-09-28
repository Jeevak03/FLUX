# main_minimal.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="FLUX - Minimal")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("FLUX starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    print("FLUX shutting down...")

@app.get("/")
async def root():
    return {"message": "FLUX API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "groq_key": "set" if os.getenv("GROQ_API_KEY") else "not set"}