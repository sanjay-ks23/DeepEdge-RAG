@echo off
echo Starting RAG System...
echo.

REM Check for Python installation
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher and try again.
    goto :end
)

REM Check for virtual environment
if not exist env (
    echo Creating virtual environment...
    python -m venv env
)

REM Activate virtual environment
call env\Scripts\activate

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Start Flask backend in a new window
echo Starting Flask backend...
start cmd /k "call env\Scripts\activate && cd flask_app && python app.py"

REM Wait for Flask to start
echo Waiting for Flask to start...
timeout /t 5 /nobreak > nul

REM Start Streamlit frontend in a new window
echo Starting Streamlit frontend...
start cmd /k "call env\Scripts\activate && cd streamlit_app && streamlit run app.py"

echo.
echo RAG System is now running!
echo Flask backend: http://localhost:5001
echo Streamlit frontend: http://localhost:8501
echo.
echo Press any key to shut down the system...

pause > nul

REM Kill the processes when the user presses a key
taskkill /f /im python.exe > nul 2>&1

:end