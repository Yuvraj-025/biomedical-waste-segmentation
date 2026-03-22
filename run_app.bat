@echo off
echo ==================================================
echo Starting Biomedical Waste Detection Application...
echo ==================================================

:: Start the Flask Backend in a new terminal window
echo [API] Starting Flask Backend...
start "Biomedical API Backend" cmd /k "call .\.venv\Scripts\activate.bat && set PYTHONPATH=%cd%\backend && python backend\app.py"

:: Delay momentarily to ensure the backend is spinning up
timeout /t 2 /nobreak >nul

:: Start the React Frontend in a new terminal window
echo [UI] Starting React Frontend...
start "Biomedical React Frontend" cmd /k "cd frontend && npm run dev -- --open"

echo.
echo Both services are starting in separate windows!
echo Feel free to close this window.
