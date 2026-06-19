@echo off
echo Setup iniciando...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no encontrado
    pause
    exit /b 1
)
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
python -c "import librosa, spotipy, sklearn; print('OK')"
if not exist ".env" (
    copy .env.example .env >nul
)
echo Setup completado!