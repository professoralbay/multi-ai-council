@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo Python bulunamadi. Lutfen Python 3.10 veya daha yeni bir surum kurun.
  pause
  exit /b 1
)

python -m venv .venv
if errorlevel 1 (
  echo Sanal ortam olusturulamadi.
  pause
  exit /b 1
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Kurulum tamamlandi. Baslatmak icin run.bat calistirin.
pause
