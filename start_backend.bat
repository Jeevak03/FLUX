@echo off
REM SDLC Assistant Backend Launcher
echo Setting up environment variables...
REM Environment variables should be set in .env file
REM Please ensure GROQ_API_KEY is configured
echo GROQ_API_KEY set successfully

echo Starting FLUX Backend...
cd /d "C:\YOKA\Research\sdlc-assistant\backend"
uvicorn main:app --reload --host 127.0.0.1 --port 8000