#!/bin/bash
# Script để chạy GUI Backtesting System

echo "🚀 Khởi động AI-Indicator GUI..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit chưa được cài đặt!"
    echo "Đang cài đặt..."
    pip install -r requirements.txt
fi

echo "✅ Mở trình duyệt và vào: http://localhost:8501"
echo ""

# Run streamlit
streamlit run gui_app.py
