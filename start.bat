@echo off
chcp 65001 >nul 2>&1

echo ========================================
echo   Spectrum Insight - Start Services
echo ========================================
echo.

echo [1/2] Starting Backend FastAPI on port 8000
start "Backend" "%~dp0backend\run.bat"

echo [2/2] Starting Frontend Vite on port 3000
start "Frontend" "%~dp0frontend\run.bat"

echo.
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo.
pause >nul
