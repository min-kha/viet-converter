# -*- coding: utf-8 -*-
"""
Script để build file .exe từ GUI converter
Sử dụng PyInstaller để tạo file standalone executable
"""
import PyInstaller.__main__
import sys
from pathlib import Path

def build_exe():
    """Build executable file"""
    
    # Đường dẫn hiện tại
    current_dir = Path(__file__).parent
    
    # Tham số PyInstaller
    pyinstaller_args = [
        'gui_converter.py',                    # File chính
        '--name=TCVN3_Converter_Pro',          # Tên file exe
        '--onefile',                            # Đóng gói thành 1 file duy nhất
        '--windowed',                           # Không hiện console (GUI app)
        '--icon=icon.ico',                      # Icon cho file exe (nếu có)
        
        # Thêm các file cần thiết
        '--add-data=convert_excel_tcvn3.py;.',
        '--add-data=tcvn3_map.json;.',
        '--add-data=icon.ico;.',                # Icon cho runtime (taskbar)
        '--add-data=icon_preview.png;.',        # Fallback icon
        
        # Metadata
        '--version-file=version_info.txt',      # Version info (tạo sau)
        
        # Optimization
        '--optimize=2',                         # Optimize bytecode
        '--clean',                              # Clean cache trước khi build
        
        # Thư mục output
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.',
        
        # Hidden imports (nếu cần)
        '--hidden-import=openpyxl',
        '--hidden-import=pandas',
        '--hidden-import=tkinter',
        
        # Console hiển thị (tắt cho production)
        # '--noconsole',  # Không hiện console window
    ]
    
    print("="*60)
    print("Building TCVN3 Converter Pro executable...")
    print("="*60)
    
    try:
        PyInstaller.__main__.run(pyinstaller_args)
        print("\n" + "="*60)
        print("✅ Build thành công!")
        print(f"📁 File exe: {current_dir / 'dist' / 'TCVN3_Converter_Pro.exe'}")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Lỗi khi build: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
