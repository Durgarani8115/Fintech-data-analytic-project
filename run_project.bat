@echo off
title Personal Finance Tracker - Starting Services
echo ========================================================
echo   Starting Personal Finance Tracker with AI Prediction  
echo ========================================================
echo.

echo [1/2] Starting Django REST Backend on http://127.0.0.1:8000...
start "Django Backend API" cmd /k "cd /d %~dp0 && backend\venv\Scripts\python.exe backend\manage.py runserver 127.0.0.1:8000"

echo [2/2] Starting React Frontend on http://127.0.0.1:5173...
start "React Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================================
echo Services launched!
echo - Backend API: http://127.0.0.1:8000/api/
echo - Frontend UI:  http://127.0.0.1:5173/
echo ========================================================
pause
