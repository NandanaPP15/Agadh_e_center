@echo off
echo Starting Agadh e-Center Digitization Platform...
echo.

echo [1/4] Starting Django Backend...
cd /d "django\akshaya_backend"
start cmd /k "venv\Scripts\activate && python manage.py runserver 8000"

timeout /t 5 /nobreak >nul

echo [2/4] Starting Rasa Actions Server...
cd /d "..\..\rasa_bot"
start cmd /k "venv\Scripts\activate && rasa run actions --port 5055"

timeout /t 5 /nobreak >nul

echo [3/4] Starting Rasa Chatbot Server...
start cmd /k "venv\Scripts\activate && rasa run --cors "*" --port 5005"

timeout /t 5 /nobreak >nul

echo [4/4] Opening Frontend in Browser...
start http://localhost:8000

echo.
echo ========================================
echo All services started successfully!
echo ========================================
echo.
echo Access URLs:
echo • Frontend: http://localhost:8000
echo • Admin: http://localhost:8000/admin
echo • API Docs: http://localhost:8000/swagger
echo • Rasa Server: http://localhost:5005
echo • Actions Server: http://localhost:5055
echo.
echo Login credentials:
echo • Admin: admin / admin@123
echo • Citizen: citizen1 / password123
echo • Employee: nandana / employee@123
echo.
echo Press any key to exit...
pause >nul