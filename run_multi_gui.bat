@echo off
REM Multi-Symbol Multi-Timeframe GUI Launcher

echo ========================================
echo   Multi-Symbol Optimizer GUI
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

streamlit run gui_app_multi.py

pause
