@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
call npx vite --host 0.0.0.0 --port 3000
pause
