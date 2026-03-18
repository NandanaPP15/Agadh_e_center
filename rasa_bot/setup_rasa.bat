@echo off
echo Setting up Rasa chatbot...

echo Step 1: Creating virtual environment...
python -m venv venv

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 3: Installing Rasa...
pip install rasa==3.5.15
pip install sanic==21.12.1
pip install sqlalchemy==1.4.46

echo Step 4: Training the model...
rasa train

echo.
echo Rasa setup completed!
echo.
echo To run Rasa:
echo 1. Open a NEW terminal
echo 2. cd D:\akshaya_project\rasa_bot
echo 3. venv\Scripts\activate
echo 4. rasa run actions --port 5055
echo.
echo 5. Open ANOTHER terminal
echo 6. cd D:\akshaya_project\rasa_bot
echo 7. venv\Scripts\activate
echo 8. rasa run --cors "*" --port 5005
pause