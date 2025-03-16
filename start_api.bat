@echo off
cd /d "%~dp0"

:: Activate virtual environment (adjust path if needed)
call venv\Scripts\activate.bat

:: Run Uvicorn
python -m uvicorn src.API.ChessAPI:app --host 127.0.0.1 --port 8000 --reload

:: Keep terminal open
pause