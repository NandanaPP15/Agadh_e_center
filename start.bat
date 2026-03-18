@echo off
echo Starting Agadh e-Center Digitization Platform...
echo.

echo Step 1: Starting Django Backend...
cd /d "django\akshaya_backend"
start cmd /k "python manage.py runserver 8000"

timeout /t 3 /nobreak >nul

echo Step 2: Starting Rasa Chatbot...
cd /d "..\..\rasa_bot"
start cmd /k "rasa run --cors "*" --port 5005"

timeout /t 3 /nobreak >nul

echo Step 3: Starting Rasa Actions Server...
start cmd /k "rasa run actions --port 5055"

timeout /t 3 /nobreak >nul

echo Step 4: Opening Frontend in Browser...
start http://localhost:8000

echo.
echo All services started successfully!
echo.
echo Dashboard: http://localhost:8000
echo Rasa Server: http://localhost:5005
echo Actions Server: http://localhost:5055
pause