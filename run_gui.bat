@echo off
REM Script để chạy GUI Backtesting System trên Windows

echo ========================================
echo   AI-Indicator GUI Launcher
echo ========================================
echo.

REM Check if streamlit is installed
python -c "import streamlit" 2>NUL
if errorlevel 1 (
    echo [ERROR] Streamlit chua duoc cai dat!
    echo.
    echo Dang cai dat...
    pip install -r requirements.txt
    echo.
)

echo Khoi dong GUI...
echo Mo trinh duyet va vao: http://localhost:8501
echo.
echo Nhan Ctrl+C de thoat
echo.

streamlit run gui_app.py

pause
