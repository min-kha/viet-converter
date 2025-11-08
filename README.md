# 🔄 TCVN3 Converter Pro

<div align="center">

![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

**Công cụ chuyển đổi Excel từ TCVN3 sang Unicode chuyên nghiệp**

[Tải xuống](#-tải-xuống) • [Tính năng](#-tính-năng) • [Cài đặt](#-cài-đặt) • [Hướng dẫn](#-hướng-dẫn-sử-dụng) • [Build](#-build-từ-source)

</div>

---

## 📖 Giới thiệu

**TCVN3 Converter Pro** là ứng dụng desktop hiện đại giúp chuyển đổi file Excel từ font TCVN3 (VNI) sang Unicode chuẩn một cách nhanh chóng, chính xác và dễ dàng.

## ✨ Tính năng nổi bật

### 🎯 Tính năng chính
- ✅ **Bộ lọc Unicode thông minh**: Tự động nhận diện và bỏ qua các cell đã là Unicode chuẩn
- 🖥️ **Giao diện GUI trực quan**: Dễ sử dụng, không cần command line
- 👁️ **Preview trước khi convert**: Xem trước các thay đổi, xác nhận trước khi thực hiện
- 📊 **Hiển thị tiến trình realtime**: Biết chính xác đang xử lý sheet nào
- 📝 **Log chi tiết**: Ghi lại tất cả cells được convert
- 💾 **Backup tự động**: Tạo bản backup file gốc trước khi convert
- 📈 **Thống kê đầy đủ**: Báo cáo chi tiết về quá trình convert

### 🚀 Tính năng nâng cao
- **Xử lý đa sheet**: Tự động xử lý tất cả sheets trong file Excel
- **Tối ưu hiệu suất**: Bỏ qua cells Unicode chuẩn để tăng tốc độ
- **Xuất log**: Lưu log chi tiết ra file text để tham khảo
- **An toàn dữ liệu**: Backup tự động, không ghi đè file gốc

## 📦 Cài đặt

### Yêu cầu
- Python 3.8 trở lên
- Windows/Linux/Mac

### Các bước cài đặt

1. **Clone hoặc download project**
```bash
cd excel_tcvn3_converter
```

2. **Cài đặt dependencies**
```bash
pip install -r requirements.txt
```

3. **Chạy thử**
```bash
python gui_converter.py
```

## 🎮 Hướng dẫn sử dụng

### Sử dụng GUI (Đề xuất)

1. **Chạy chương trình**
```bash
python gui_converter.py
```

2. **Chọn file**
   - Nhấn "Chọn..." ở dòng "File Input" → Chọn file Excel TCVN3
   - File Output sẽ tự động đề xuất, hoặc bạn có thể chọn vị trí khác

3. **Cấu hình tùy chọn**
   - ✅ Bỏ qua cells đã là Unicode chuẩn (khuyến nghị bật)
   - ✅ Tự động backup file gốc (khuyến nghị bật)

4. **Preview (Tùy chọn)**
   - Nhấn "👁️ Xem Trước" để xem các cell sẽ được convert
   - Kiểm tra kết quả trước khi thực hiện
   - Xác nhận tiếp tục

5. **Chuyển đổi**
   - Nhấn "🚀 Chuyển Đổi"
   - Theo dõi tiến trình trên thanh progress
   - Xem kết quả trong các tab Log và Thống kê

6. **Xuất log (Tùy chọn)**
   - Nhấn "📄 Xuất Log" để lưu chi tiết ra file text

### Sử dụng Command Line

Nếu bạn muốn tích hợp vào script tự động:

```python
from convert_excel_tcvn3 import convert_excel, export_conversion_log

# Convert file
stats = convert_excel(
    input_path="input_tcvn3.xlsx",
    output_path="output_unicode.xlsx",
    skip_unicode=True  # Bỏ qua cells Unicode chuẩn
)

# In thống kê
print(f"Đã convert {stats.converted_cells} cells")
print(f"Bỏ qua {stats.already_unicode} cells Unicode chuẩn")

# Xuất log
export_conversion_log(stats, "conversion_log.txt")
```

### Preview trước khi convert

```python
from convert_excel_tcvn3 import preview_conversion

# Lấy danh sách các cell sẽ được convert
samples = preview_conversion("input_tcvn3.xlsx", max_samples=50)

for sample in samples:
    print(f"Sheet: {sample.sheet}, Row: {sample.row}")
    print(f"  Trước: {sample.original}")
    print(f"  Sau:   {sample.converted}")
    print(f"  Unicode: {sample.was_unicode}")
```

## 🔍 Cách thức hoạt động

### Bộ lọc Unicode thông minh

Chương trình sử dụng hàm `looks_like_unicode_vietnamese()` để kiểm tra từng cell:

```python
def looks_like_unicode_vietnamese(s: str) -> bool:
    """
    Kiểm tra xem chuỗi có phải là tiếng Việt Unicode hợp lệ.
    
    - Nếu toàn bộ ký tự nằm trong bảng chữ VN Unicode chuẩn → True (bỏ qua)
    - Nếu có ký tự lạ (có thể là TCVN3) → False (cần convert)
    """
```

**Bộ ký tự được chấp nhận:**
- Chữ cái Latin (a-z, A-Z)
- Chữ cái tiếng Việt có dấu (à, á, ả, ã, ạ, â, ă, ê, ô, ơ, ư, đ...)
- Số (0-9)
- Dấu câu thông dụng (. , ; : ! ? " ' ( ) [ ] { } - _ / \ | @ # % & * + =)
- Khoảng trắng, tab, xuống dòng
- Ký tự đặc biệt (€, $, ¥, £, ₫, °, ±, ×, ÷...)

**Lợi ích:**
- ⚡ Tăng tốc độ xử lý (không convert lại những gì đã đúng)
- 🛡️ An toàn dữ liệu (không làm hỏng text đã Unicode)
- 📊 Thống kê chính xác (biết đâu là TCVN3, đâu là Unicode)

### Quy trình chuyển đổi

```
1. Load bảng map TCVN3 → Unicode (từ tcvn3_map.json)
2. Đọc từng sheet trong file Excel
3. Với mỗi cell:
   a. Kiểm tra có phải string không?
   b. Kiểm tra đã là Unicode chuẩn chưa? (nếu bật skip_unicode)
   c. Nếu cần convert → Áp dụng map TCVN3 → Unicode
   d. Ghi log nếu có thay đổi
4. Ghi file output
5. Hiển thị thống kê
```

## 📊 Ví dụ Output

### Console Output
```
✅ Đã tải 291 mapping từ tcvn3_map.json
Đang xử lý sheet 1/3: Danh sách
Đang xử lý sheet 2/3: Thống kê
Đang xử lý sheet 3/3: Ghi chú
✅ Ghi xong: output_unicode.xlsx

📊 Thống kê:
  - Tổng số cells: 1,234
  - Cells chứa text: 567
  - Đã là Unicode chuẩn: 123
  - Đã convert: 444
  - Không đổi: 0
  - Số sheets: 3
```

### Log File
```
================================================================================
TCVN3 → Unicode Conversion Log
Thời gian: 2025-11-08 14:30:45
================================================================================

📊 Thống kê:
  - Tổng số cells: 1,234
  - Cells chứa text: 567
  - Đã là Unicode chuẩn: 123
  - Đã convert: 444
  - Không đổi: 0
  - Số sheets: 3

📝 Chi tiết 444 cells đã convert:
--------------------------------------------------------------------------------

[1] Sheet: Danh sách | Row: 2 | Col: Tên
    BEFORE: Nguyễn Văn A
    AFTER:  Nguyễn Văn A

[2] Sheet: Danh sách | Row: 3 | Col: Địa chỉ
    BEFORE: Hµ Néi
    AFTER:  Hà Nội
...
```

## 🎯 Use Cases

### 1. Chuyển đổi file Excel cũ
Bạn có file Excel từ thời VnTime, muốn mở được trên máy hiện đại.

### 2. Di chuyển dữ liệu legacy
Migrate dữ liệu từ hệ thống cũ sang hệ thống mới sử dụng Unicode.

### 3. Chuẩn hóa dữ liệu
Đồng nhất encoding trong toàn bộ hệ thống.

### 4. Batch processing
Xử lý hàng loạt files Excel trong thư mục.

## ⚙️ Cấu hình nâng cao

### Tùy chỉnh bộ ký tự Unicode

Nếu cần thêm ký tự đặc biệt, sửa trong `convert_excel_tcvn3.py`:

```python
_VIET_UNI_OK = set(
    "abcdefghijklmnopqrstuvwxyz..."
    "thêm ký tự của bạn vào đây"
)
```

### Tùy chỉnh số lượng preview

```python
samples = preview_conversion("input.xlsx", max_samples=100)  # Tăng lên 100
```

### Tắt backup tự động

Trong GUI: Bỏ tick "Tự động backup file gốc"

Hoặc trong code:
```python
convert_excel("input.xlsx", "output.xlsx", skip_unicode=True)
# Không backup
```

## 🐛 Xử lý lỗi thường gặp

### Lỗi: "Không tìm thấy file map"
**Giải pháp**: Chương trình sẽ tự động tải map từ web. Nếu không được:
```bash
python build_tcvn3_map.py --build
```

### Lỗi: "File Excel bị hỏng"
**Giải pháp**: 
- Thử mở file bằng Excel, Save as lại
- Đảm bảo file có đuôi .xlsx (không phải .xls cũ)

### Lỗi: "Không có quyền ghi file"
**Giải pháp**:
- Đóng file Excel nếu đang mở
- Chọn vị trí output khác
- Chạy Python với quyền Administrator

### Convert nhưng vẫn hiển thị lỗi font
**Giải pháp**: 
- File đã convert đúng, nhưng Excel đang dùng font không hỗ trợ tiếng Việt
- Đổi font sang: Arial, Times New Roman, Calibri...

## 🔧 Development

### Cấu trúc project

```
excel_tcvn3_converter/
├── convert_excel_tcvn3.py   # Core conversion logic
├── gui_converter.py          # GUI application
├── build_tcvn3_map.py       # Build TCVN3 mapping table
├── tcvn3_map.json           # TCVN3 → Unicode mapping
├── tcvn3_map.csv            # CSV version of mapping
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Chạy tests

```bash
# Test conversion
python convert_excel_tcvn3.py

# Test GUI
python gui_converter.py
```

### Đóng góp

Mọi đóng góp đều được hoan nghênh! Pull requests và issues đều OK.

## 📝 License

MIT License - Tự do sử dụng cho mục đích cá nhân và thương mại.

## 👨‍💻 Author

Phát triển với ❤️ bởi AI Assistant

## 🙏 Credits

- TCVN3 mapping table từ [vncharsets.com](http://vncharsets.com)
- Powered by: pandas, openpyxl, tkinter

## 📞 Support

Nếu gặp vấn đề, vui lòng:
1. Đọc phần "Xử lý lỗi thường gặp"
2. Kiểm tra file log
3. Tạo issue với thông tin chi tiết

---

**Happy Converting! 🎉**
