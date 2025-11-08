# 📦 Hướng Dẫn Build & Publish TCVN3 Converter Pro

## 🎯 Tổng Quan

Hướng dẫn này sẽ giúp bạn:
1. ✅ Tạo icon chuyên nghiệp
2. ✅ Build file `.exe` standalone
3. ✅ Đóng gói phân phối
4. ✅ Tạo installer (tùy chọn)

---

## 📋 Yêu Cầu

### 1. Cài đặt PyInstaller
```bash
pip install pyinstaller
```

### 2. Cài đặt Pillow (để tạo icon)
```bash
pip install pillow
```

### 3. Cài đặt thêm (tùy chọn)
```bash
pip install auto-py-to-exe  # GUI cho PyInstaller
```

---

## 🎨 Bước 1: Tạo Icon

### Option A: Tạo Icon Tự Động (Mặc định)
```bash
python create_icon.py
```
➡️ Tạo file `icon.ico` và `icon_preview.png`

### Option B: Từ Ảnh Có Sẵn
```bash
python create_icon.py your_image.png
```

### Option C: Tải Icon Từ Internet
- Tải icon miễn phí: 
  - https://www.flaticon.com/
  - https://icons8.com/
  - https://www.iconfinder.com/
- Chọn icon liên quan đến: Excel, convert, văn bản, Việt Nam
- Lưu thành `icon.png` hoặc `icon.ico`

### Option D: Tạo Icon Chuyên Nghiệp (Adobe/Figma)
1. Thiết kế icon với kích thước 512x512px
2. Export thành PNG
3. Dùng `create_icon.py` để convert sang `.ico`

---

## 🔨 Bước 2: Build File EXE

### Quick Build (Đơn Giản)
```bash
python build_exe.py
```

### Manual Build (Tùy Chỉnh)
```bash
pyinstaller --name="TCVN3_Converter_Pro" ^
            --onefile ^
            --windowed ^
            --icon=icon.ico ^
            --add-data="convert_excel_tcvn3.py;." ^
            --add-data="tcvn3_map.json;." ^
            gui_converter.py
```

### Với Console (Debug)
Nếu gặp lỗi, build với console để xem log:
```bash
pyinstaller --name="TCVN3_Converter_Pro" ^
            --onefile ^
            --console ^
            --icon=icon.ico ^
            gui_converter.py
```

---

## 📁 Bước 3: Kiểm Tra Output

Sau khi build xong:

```
dist/
  └── TCVN3_Converter_Pro.exe   ← File chính (50-80MB)

build/                            ← Cache (có thể xóa)
TCVN3_Converter_Pro.spec         ← Config (có thể giữ để build lại)
```

### Test File EXE
1. Copy `dist/TCVN3_Converter_Pro.exe` ra ngoài
2. Copy file `tcvn3_map.json` cùng thư mục (nếu cần)
3. Double-click để chạy
4. Test tất cả tính năng

---

## 📦 Bước 4: Đóng Gói Phân Phối

### Option A: ZIP Package (Đơn Giản)

Tạo folder:
```
TCVN3_Converter_Pro_v2.1/
  ├── TCVN3_Converter_Pro.exe
  ├── tcvn3_map.json
  ├── README.txt
  ├── LICENSE.txt
  └── CHANGELOG.txt
```

Nén thành: `TCVN3_Converter_Pro_v2.1.zip`

### Option B: Self-Extracting Archive (7-Zip)
```bash
# Cài 7-Zip: https://www.7-zip.org/
7z a -sfx TCVN3_Converter_Pro_v2.1_Setup.exe dist/*
```

### Option C: Inno Setup (Windows Installer)

#### Cài Inno Setup
Download: https://jrsoftware.org/isinfo.php

#### Tạo file setup script
```iss
; TCVN3_Converter_Setup.iss
[Setup]
AppName=TCVN3 Converter Pro
AppVersion=2.1
DefaultDirName={pf}\TCVN3_Converter_Pro
DefaultGroupName=TCVN3 Converter Pro
OutputBaseFilename=TCVN3_Converter_Pro_v2.1_Setup
Compression=lzma2
SolidCompression=yes
SetupIconFile=icon.ico

[Files]
Source: "dist\TCVN3_Converter_Pro.exe"; DestDir: "{app}"
Source: "tcvn3_map.json"; DestDir: "{app}"
Source: "README.txt"; DestDir: "{app}"

[Icons]
Name: "{group}\TCVN3 Converter Pro"; Filename: "{app}\TCVN3_Converter_Pro.exe"
Name: "{commondesktop}\TCVN3 Converter Pro"; Filename: "{app}\TCVN3_Converter_Pro.exe"
```

Build installer:
```bash
iscc TCVN3_Converter_Setup.iss
```

---

## 🚀 Bước 5: Publish

### 1. GitHub Releases
```bash
# Tag version
git tag v2.1.0
git push origin v2.1.0

# Upload files:
# - TCVN3_Converter_Pro_v2.1.zip (portable)
# - TCVN3_Converter_Pro_v2.1_Setup.exe (installer)
```

### 2. Google Drive / OneDrive
- Upload file ZIP hoặc installer
- Chia sẻ link công khai
- Tạo QR code cho link download

### 3. Website Riêng
- Upload lên hosting
- Tạo landing page với:
  - Screenshots
  - Features
  - Download button
  - Tutorial video

### 4. Microsoft Store (Advanced)
- Convert thành MSIX package
- Submit lên Microsoft Store
- Requires: $19 registration fee

---

## 🔐 Digital Signature (Chuyên Nghiệp)

### Mua Code Signing Certificate
- Comodo/Sectigo: ~$70-200/year
- DigiCert: ~$200-400/year

### Sign EXE File
```bash
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com TCVN3_Converter_Pro.exe
```

**Lợi ích:**
- ✅ Không có cảnh báo "Unknown Publisher"
- ✅ Tăng độ tin cậy
- ✅ Bảo vệ khỏi malware false-positive

---

## 📊 Build Optimization

### Giảm Kích Thước File

1. **UPX Compression**
```bash
pip install pyinstaller[encryption]
pyinstaller --upx-dir=/path/to/upx ...
```

2. **Exclude Unused Modules**
```bash
pyinstaller --exclude-module matplotlib --exclude-module numpy ...
```

3. **Strip Debug Info**
```bash
pyinstaller --strip ...
```

### Performance

1. **Optimize Python Code**
```bash
python -OO build_exe.py  # Remove docstrings, assertions
```

2. **Use PyInstaller Bootloader**
```bash
pyinstaller --bootloader-ignore-signals ...
```

---

## 🐛 Troubleshooting

### Lỗi: "Failed to execute script"
**Giải pháp:**
```bash
# Build với console để xem lỗi
pyinstaller --onefile --console gui_converter.py
```

### Lỗi: Icon không hiển thị
**Giải pháp:**
- Đảm bảo `icon.ico` có multiple sizes (16, 32, 48, 64, 128, 256)
- Dùng `create_icon.py` để tạo đúng format

### Lỗi: Missing modules
**Giải pháp:**
```bash
pyinstaller --hidden-import=missing_module ...
```

### Lỗi: Antivirus chặn
**Giải pháp:**
- Build không nén: `--noupx`
- Thêm exception trong antivirus
- Sign với certificate (best)

---

## 📝 Checklist Trước Khi Release

- [ ] Icon đẹp, chuyên nghiệp
- [ ] Version info đầy đủ
- [ ] Test trên Windows 10/11 clean
- [ ] Test tất cả features
- [ ] README.txt rõ ràng
- [ ] LICENSE.txt (nếu có)
- [ ] CHANGELOG.txt
- [ ] Screenshots/Video demo
- [ ] Virus scan (VirusTotal)
- [ ] Digital signature (nếu có)

---

## 🎁 Template README.txt

```
╔══════════════════════════════════════════════════════════╗
║   TCVN3 CONVERTER PRO v2.1                               ║
║   Excel TCVN3 to Unicode Converter                      ║
╚══════════════════════════════════════════════════════════╝

📥 CÁCH SỬ DỤNG:
1. Double-click TCVN3_Converter_Pro.exe
2. Chọn file Excel TCVN3 cần convert
3. Chọn vị trí lưu file output
4. Nhấn "Chuyển Đổi"

🎨 TÍNH NĂNG PRO:
• Review & chọn cells cần convert
• Đánh dấu màu cells đã convert
• Tự động bỏ qua Unicode chuẩn
• Backup tự động

🔑 KÍCH HOẠT BẢN QUYỀN:
1. Nhấn nút "🔑 Bản Quyền"
2. Nhập email
3. Generate Trial Key
4. Kích hoạt

💡 HỖ TRỢ:
Email: your-email@example.com
Website: https://your-website.com

© 2025 Nguyen Minh Kha. All rights reserved.
```

---

## 🚀 Quick Start Commands

```bash
# 1. Tạo icon
python create_icon.py

# 2. Build exe
python build_exe.py

# 3. Test
cd dist
TCVN3_Converter_Pro.exe

# 4. Đóng gói
# Copy dist/*.exe + tcvn3_map.json + README.txt
# Nén thành ZIP

# 5. Upload & Share! 🎉
```

---

## 📚 Resources

- PyInstaller Docs: https://pyinstaller.org/
- Inno Setup: https://jrsoftware.org/isinfo.php
- Icon Tools: https://www.favicon-generator.org/
- Code Signing: https://comodosslstore.com/code-signing

---

**Good luck with your release! 🚀**
