#!/bin/bash
# Script chạy GUI trên Linux/Mac

echo "========================================"
echo "TCVN3 to Unicode Excel Converter"
echo "========================================"
echo

# Kiểm tra Python
if command -v python3 &> /dev/null; then
    echo "✓ Đã tìm thấy Python3"
    python3 gui_converter.py
elif command -v python &> /dev/null; then
    echo "✓ Đã tìm thấy Python"
    python gui_converter.py
else
    echo "❌ Không tìm thấy Python!"
    echo
    echo "Vui lòng cài đặt Python 3.8 trở lên:"
    echo "- Ubuntu/Debian: sudo apt install python3 python3-pip python3-tk"
    echo "- macOS: brew install python3"
    echo
    echo "Sau đó chạy: pip install -r requirements.txt"
    exit 1
fi
