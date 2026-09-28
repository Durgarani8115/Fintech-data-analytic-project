@echo off
title Django Backend Server
cd /d "%~dp0"
echo Starting Django Backend at http://127.0.0.1:8000...
venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
pause
