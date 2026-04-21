@echo off
echo Starting Jarvis API Server...
.venv\Scripts\uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
