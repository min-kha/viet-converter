@echo off
chcp 65001 >nul
echo ========================================
echo TCVN3 to Unicode Excel Converter
echo ========================================
echo.

REM Tìm Python
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Đã tìm thấy Python
    python gui_converter.py
    goto :end
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    echo Đã tìm thấy Python Launcher
    py gui_converter.py
    goto :end
)

echo ❌ Không tìm thấy Python!
echo.
echo Vui lòng:
echo 1. Cài đặt Python từ https://www.python.org/downloads/
echo 2. Chọn "Add Python to PATH" khi cài đặt
echo 3. Cài dependencies: pip install -r requirements.txt
echo.
pause

:end
pause
