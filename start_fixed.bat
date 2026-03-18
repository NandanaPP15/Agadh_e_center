@echo off
echo ========================================
echo    STARTING AGADH PLATFORM - FIXED VERSION
echo ========================================
echo.

echo [1/3] Starting Django Backend...
cd /d "django\akshaya_backend"
start "Django Server" cmd /k "venv\Scripts\activate && python manage.py runserver 8000"

timeout /t 5 /nobreak >nul

echo [2/3] Starting Rasa Actions Server...
cd /d "..\..\rasa_bot"
start "Rasa Actions" cmd /k "venv\Scripts\activate && rasa run actions --port 5055"

timeout /t 5 /nobreak >nul

echo [3/3] Starting Rasa Chatbot Server...
start "Rasa Chatbot" cmd /k "venv\Scripts\activate && rasa run --cors "*" --port 5005"

timeout /t 5 /nobreak >nul

echo ========================================
echo    ALL SERVICES STARTED!
echo ========================================
echo.
echo 🌐 OPEN YOUR BROWSER TO: file:///D:/akshaya_project/frontend/index.html
echo.
echo 💬 CHATBOT: Click bottom-right chat icon
echo.
echo 📞 TEST WITH THESE QUESTIONS:
echo 1. "What documents for ration card?"
echo 2. "What documents for passport?"
echo 3. "What documents for aadhaar?"
echo.
echo ⚠️  Make sure to wait 30 seconds for all services to fully start
echo.
pause