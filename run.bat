@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\activate.bat" (
  echo Once install.bat calistirin.
  pause
  exit /b 1
)

call .venv\Scripts\activate.bat
python app.py
pause
