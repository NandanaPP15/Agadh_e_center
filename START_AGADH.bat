@echo off
echo ========================================
echo    STARTING AGADH E-CENTER PLATFORM
echo ========================================
echo.

echo [1/3] Starting Django Backend (port 8000)...
cd /d "django\akshaya_backend"
start "Django" cmd /k "venv\Scripts\activate && echo Starting Django... && python manage.py runserver 8000"

timeout /t 8 /nobreak >nul

echo [2/3] Starting Rasa Actions Server (port 5055)...
cd /d "..\..\rasa_bot"
start "Rasa Actions" cmd /k "venv\Scripts\activate && echo Starting Rasa Actions... && rasa run actions --port 5055"

timeout /t 8 /nobreak >nul

echo [3/3] Starting Rasa Chatbot Server (port 5005)...
start "Rasa Chatbot" cmd /k "venv\Scripts\activate && echo Starting Rasa Chatbot... && rasa run --cors "*" --port 5005"

timeout /t 8 /nobreak >nul

echo ========================================
echo    ALL SERVICES STARTED!
echo ========================================
echo.
echo 🌐 OPEN FRONTEND:
echo 1. Go to: D:\akshaya_project\frontend
echo 2. Double-click: index.html
echo.
echo 💬 TEST CHATBOT:
echo 1. Click chat icon (bottom-right)
echo 2. Try: "What documents for ration card?"
echo 3. Try: "What documents for passport?"
echo.
echo ⏰ Wait 30 seconds for all services to fully start
echo.
pause