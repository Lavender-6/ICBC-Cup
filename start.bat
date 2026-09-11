@echo off
chcp 65001 >nul 2>&1

echo ========================================
echo   频谱智瞳 - 启动前后端服务
echo ========================================
echo.

echo [1/2] 启动后端 FastAPI 端口 8000
start "Backend" "%~dp0backend\run.bat"

echo [2/2] 启动前端 Vite 端口 3000
start "Frontend" "%~dp0frontend\run.bat"

echo.
echo 后端地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo 前端地址: http://localhost:3000
echo.
echo 按任意键关闭此窗口...
pause >nul
