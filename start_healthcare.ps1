# Startup Script for MedNLP-RAG Core (Healthcare NLP)
# Launches both FastAPI Backend and Streamlit Frontend.

$VenvPath = ".venv"
$PythonPath = "C:\Users\rajag\AppData\Local\Programs\Python\Python312\python.exe"

# Recreate venv if missing
if (-not (Test-Path $VenvPath)) {
    Write-Host "Virtual environment not found. Re-initializing..." -ForegroundColor Yellow
    if (-not (Test-Path $PythonPath)) {
        Write-Error "Python 3.12 not found. Cannot auto-setup. Please run setup_all.ps1 first."
        Exit 1
    }
    & $PythonPath -m venv $VenvPath
    & (Join-Path $VenvPath "Scripts\pip.exe") install -r requirements.txt
}

Write-Host "Starting MedNLP-RAG System..." -ForegroundColor Cyan

# 1. Start Backend FastAPI
Write-Host "Launching FastAPI Backend on http://localhost:8000..." -ForegroundColor Gray
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "Write-Host 'Healthcare NLP API Running' -ForegroundColor Cyan; .venv\Scripts\python.exe -m uvicorn src.main:app --host 0.0.0.0 --port 8000"

# 2. Start Frontend Streamlit
Write-Host "Launching Streamlit Frontend on http://localhost:8501..." -ForegroundColor Gray
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "Write-Host 'Healthcare NLP Frontend Running' -ForegroundColor Cyan; .venv\Scripts\streamlit.exe run frontend/app.py"

# 3. Open Browser
Start-Sleep -Seconds 4
Write-Host "Opening browser..." -ForegroundColor Green
Start-Process "http://localhost:8501"
