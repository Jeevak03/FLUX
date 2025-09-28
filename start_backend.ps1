# SDLC Assistant Backend Launcher
Write-Host "Setting up environment variables..." -ForegroundColor Green
# Environment variables should be set in .env file
# Please ensure GROQ_API_KEY is configured
Write-Host "GROQ_API_KEY set successfully" -ForegroundColor Green

Write-Host "Starting FLUX Backend..." -ForegroundColor Green
Set-Location "C:\YOKA\Research\sdlc-assistant\backend"
uvicorn main:app --reload --host 127.0.0.1 --port 8000