# 🚀 QUICK START GUIDE

## Cài đặt nhanh (3 bước)

### 1️⃣ Cài Python (nếu chưa có)
- Tải từ: https://www.python.org/downloads/
- ⚠️ **QUAN TRỌNG**: Tick chọn "Add Python to PATH" khi cài

### 2️⃣ Cài dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Chạy chương trình

**Windows:**
```bash
# Cách 1: Double click vào file
run_gui.bat

# Cách 2: Command line
python gui_converter.py
```

**Linux/Mac:**
```bash
# Cách 1:
chmod +x run_gui.sh
./run_gui.sh

# Cách 2:
python3 gui_converter.py
```

## 📖 Hướng dẫn sử dụng (5 bước)

### 1. Chọn file
- **File Input**: File Excel TCVN3 cần convert
- **File Output**: Nơi lưu kết quả (tự động đề xuất)

### 2. Chọn tùy chọn
- ✅ **Bỏ qua Unicode chuẩn**: Khuyến nghị BẬT (tăng tốc độ)
- ✅ **Backup tự động**: Khuyến nghị BẬT (an toàn)

### 3. Preview (Tùy chọn nhưng nên làm)
- Nhấn "👁️ Xem Trước"
- Kiểm tra các cell sẽ được convert
- Xem phân loại: Unicode/TCVN3

### 4. Convert
- Nhấn "🚀 Chuyển Đổi"
- Theo dõi tiến trình
- Đợi hoàn thành

### 5. Kiểm tra kết quả
- Tab **Conversion Log**: Danh sách cells đã convert
- Tab **Thống Kê**: Số liệu tổng hợp
- Nhấn "📄 Xuất Log" để lưu báo cáo

## 🎯 Demo nhanh

### Test bộ lọc Unicode
```bash
python test_unicode_filter.py
```

Output:
```
✅ "Nguyễn Văn A" → Unicode chuẩn (bỏ qua)
✅ "Hà Nội" → Unicode chuẩn (bỏ qua)
🔄 "Hµ Néi" → Cần convert (TCVN3)
🔄 "Th¸nh phè" → Cần convert (TCVN3)
```

### Convert từ code
```python
from convert_excel_tcvn3 import convert_excel

stats = convert_excel(
    "input_tcvn3.xlsx",
    "output_unicode.xlsx",
    skip_unicode=True
)

print(f"✅ Đã convert {stats.converted_cells} cells")
```

## ⚡ Tips & Tricks

### Tăng tốc độ
1. **BẬT** "Bỏ qua Unicode chuẩn"
2. Đóng Excel trước khi convert
3. Convert từng file thay vì nhiều file cùng lúc

### Xử lý file lớn
- File > 100MB: Có thể mất 2-5 phút
- Preview chỉ hiển thị 50-100 mẫu đầu tiên
- Log đầy đủ vẫn được ghi

### Batch conversion
Tạo script Python:
```python
from pathlib import Path
from convert_excel_tcvn3 import convert_excel

input_dir = Path("input_folder")
output_dir = Path("output_folder")
output_dir.mkdir(exist_ok=True)

for file in input_dir.glob("*.xlsx"):
    output_file = output_dir / f"{file.stem}_unicode.xlsx"
    stats = convert_excel(file, output_file, skip_unicode=True)
    print(f"✅ {file.name}: {stats.converted_cells} cells")
```

## ❓ FAQ

**Q: File sau convert vẫn hiển thị sai font?**  
A: Đổi font trong Excel sang Arial, Times New Roman, hoặc Calibri.

**Q: Có mất dữ liệu không?**  
A: Không. Backup tự động được tạo. Chỉ text được convert, số liệu/công thức giữ nguyên.

**Q: Convert được file .xls cũ không?**  
A: Khuyến nghị mở bằng Excel → Save as .xlsx trước.

**Q: Mất bao lâu?**  
A: Tùy kích thước file:
- < 1MB: < 10 giây
- 1-10MB: 10-60 giây
- 10-100MB: 1-5 phút

**Q: Có tự động convert tất cả files trong folder không?**  
A: Hiện chưa có trong GUI. Dùng batch script (xem phần Tips).

## 🆘 Cần trợ giúp?

1. Đọc README.md chi tiết
2. Chạy demo: `python test_unicode_filter.py`
3. Kiểm tra file log sau khi convert
4. Tạo issue với thông tin chi tiết

---
**Chúc bạn convert thành công! 🎉**
