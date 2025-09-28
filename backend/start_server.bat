@echo off
cd /d "c:\YOKA\Research\sdlc-assistant\backend"
echo Starting SDLC Multi-Agent Assistant Backend...
python -m uvicorn main_ultra_minimal:app --host 127.0.0.1 --port 8082 --log-level info
pause