# 🚀 TCVN3 Converter Pro - Tính năng mới v2.1

## 🎉 Các tính năng Pro đã thêm

### 1. 🔍 Review & Cherry-pick Unicode Cells

#### Mô tả
Khi bật tùy chọn "Bỏ qua cells đã là Unicode chuẩn", bạn có thể:
- Xem danh sách tất cả cells Unicode
- Chọn lọc từng cell: Bỏ qua hay vẫn convert
- Tùy chỉnh theo nhu cầu cụ thể

#### Cách sử dụng
1. Chọn file input
2. Bật ✅ "Bỏ qua cells đã là Unicode chuẩn"
3. Nhấn **"👁️ Xem Trước"** để scan file
4. Nhấn **"🔍 Review & Chọn"** (nút mới xuất hiện)
5. Trong dialog Review:
   - Xem danh sách cells Unicode
   - **Double-click** hoặc **Enter** để toggle Skip/Convert
   - ✅ **Chọn Tất Cả** - Bỏ qua tất cả
   - ❌ **Bỏ Chọn Tất Cả** - Convert tất cả
   - 🔄 **Đảo Ngược** - Đảo ngược lựa chọn
6. Nhấn **"✅ OK - Áp Dụng"**
7. Nhấn **"🚀 Chuyển Đổi"**

#### Lợi ích
- ⚡ **Kiểm soát hoàn toàn** - Quyết định từng cell
- 🎯 **Chính xác cao** - Không bỏ sót
- 💡 **Linh hoạt** - Xử lý trường hợp đặc biệt
- 👁️ **Minh bạch** - Xem được tất cả thay đổi

#### Ví dụ use case
```
Bạn có file với:
- 100 cells tiếng Việt Unicode chuẩn
- 20 cells TCVN3 cần convert
- 5 cells Unicode nhưng bạn muốn "re-convert" để đảm bảo

→ Preview → Review → Bỏ tick 5 cells cần re-convert
→ Chuyển đổi: Converts 20 TCVN3 + 5 Unicode cells
```

---

### 2. 🎨 Highlight Converted Cells (Pro Feature)

#### Mô tả
Đánh dấu màu các cells đã được convert trong file Excel output.
Dễ dàng nhận diện cells nào đã thay đổi.

#### Cách sử dụng
1. **Đăng ký bản quyền Pro** (bắt buộc)
   - Nhấn **"🔑 Bản Quyền"**
   - Nhập thông tin và License Key
   - Hoặc nhấn "Generate Trial Key" để test
2. Bật ✅ **"🎨 Đánh dấu màu cells đã convert (Pro)"**
3. Chọn màu từ dropdown:
   - 🟡 Yellow (#FFFF00) - Mặc định
   - 🟢 Green (#00FF00)
   - 🔵 Cyan (#00FFFF)
   - 🟣 Magenta (#FF00FF)
   - 🟠 Orange (#FFA500)
   - 🌸 Pink (#FFB6C1)
4. Xem preview màu ở button bên cạnh
5. Convert như bình thường
6. File output sẽ có cells được highlight

#### Lợi ích
- 👁️ **Dễ kiểm tra** - Nhìn là biết cell nào đổi
- 📊 **Review nhanh** - Không cần đọc từng cell
- ✅ **QA thuận tiện** - Đảm bảo chất lượng
- 🎨 **Tùy chỉnh màu** - Chọn màu phù hợp

#### Technical Details
```python
# Sử dụng openpyxl PatternFill
fill = PatternFill(
    start_color="FFFF00",  # Yellow
    end_color="FFFF00",
    fill_type="solid"
)
cell.fill = fill
```

#### Lưu ý
- ⚠️ Chỉ có trong **Pro Edition**
- 📁 Cần license hợp lệ
- 🎨 Áp dụng sau khi ghi file
- 💾 File size tăng nhẹ (do formatting)

---

### 3. 🔑 License Management System

#### Mô tả
Hệ thống quản lý bản quyền và kích hoạt tính năng Pro.

#### Phiên bản

##### Free Edition
- ✅ Convert cơ bản TCVN3 → Unicode
- ✅ Preview trước khi convert
- ✅ Backup tự động
- ✅ Log chi tiết
- ✅ Thống kê
- ❌ Highlight cells
- ❌ Review & Cherry-pick (giới hạn)

##### Pro Edition
- ✅ Tất cả tính năng Free
- ✅ **Highlight converted cells** với màu tùy chọn
- ✅ **Review & Cherry-pick** không giới hạn
- ✅ Advanced export options
- ✅ Priority support

#### Cách đăng ký

##### Bước 1: Mở dialog Bản Quyền
Nhấn nút **"🔑 Bản Quyền"**

##### Bước 2: Nhập thông tin
```
Họ tên: Nguyễn Văn A
Email: user@example.com
Công ty: ABC Company (optional)
```

##### Bước 3: Lấy License Key

**Cách 1: Generate Trial Key (Demo)**
1. Nhập Email
2. Nhấn **"🔑 Generate Trial Key"**
3. Copy key hiển thị
4. Paste vào ô "License Key"

**Cách 2: Mua License chính thức**
1. Liên hệ: support@example.com
2. Nhận License Key qua email
3. Nhập vào ô "License Key"

##### Bước 4: Kích hoạt
1. Nhấn **"✅ Kích Hoạt"**
2. Hệ thống verify key
3. Thành công → Chuyển sang Pro Edition
4. Title bar hiển thị: "Licensed to: [Tên bạn]"

#### License Key Generation
```python
# Simple hash-based verification
secret = "TCVN3_CONVERTER_2025"
key = SHA256(email + secret)[:16].upper()
```

**Ví dụ:**
```
Email: test@example.com
Key: [16-char hash]
```

#### License File
Thông tin license được lưu trong `license.json`:
```json
{
  "type": "Pro",
  "user": "Nguyễn Văn A",
  "email": "user@example.com",
  "company": "ABC Company",
  "license_key": "XXXXXXXXXXXX",
  "features": [
    "basic_conversion",
    "preview",
    "highlight",
    "advanced_export"
  ],
  "registered": true
}
```

#### Security
- ✅ License key verification
- ✅ Email-based validation
- ✅ Local storage (không gửi thông tin ra ngoài)
- ✅ Có thể backup/restore file license.json

---

## 🎯 Workflow hoàn chỉnh

### Kịch bản 1: Convert thông thường
```
1. Chọn file
2. Bật "Bỏ qua Unicode"
3. Preview
4. Convert
→ Nhanh nhất
```

### Kịch bản 2: Review kỹ lưỡng
```
1. Chọn file
2. Bật "Bỏ qua Unicode"
3. Preview
4. Review & Chọn
   - Xem từng cell Unicode
   - Chọn cells cần convert
5. Convert
→ Kiểm soát tối đa
```

### Kịch bản 3: Convert với Highlight (Pro)
```
1. Đăng ký Pro (nếu chưa)
2. Chọn file
3. Bật "Đánh dấu màu cells"
4. Chọn màu yêu thích
5. Preview
6. Review (optional)
7. Convert
→ File output có highlight
→ Dễ kiểm tra
```

### Kịch bản 4: Batch với Review
```
1. File 1:
   - Preview
   - Review & lưu selection
   - Convert
2. File 2:
   - Preview
   - Review (dùng lại pattern)
   - Convert
3. ...
→ Nhất quán giữa các files
```

---

## 💡 Tips & Tricks

### Review hiệu quả
1. **Sort by sheet** - Xem theo sheet
2. **Pattern matching** - Tìm pattern trong Unicode cells
3. **Bulk operations** - Dùng "Chọn tất cả" / "Bỏ chọn tất cả"
4. **Save decision** - Selection được nhớ trong session

### Highlight màu sắc
| Màu | Khi nào dùng |
|-----|--------------|
| 🟡 Yellow | Mặc định, dễ nhìn |
| 🟢 Green | Cells quan trọng đã fix |
| 🔵 Cyan | Cells cần review thêm |
| 🟠 Orange | Cảnh báo, cần chú ý |
| 🟣 Magenta | Đặc biệt, VIP cells |
| 🌸 Pink | Soft, không chói |

### License management
- 📁 Backup `license.json` để không mất license
- 🔄 Copy file giữa các máy
- 👥 Mua license team nếu nhiều người dùng
- 🔑 Giữ License Key an toàn

---

## 🆕 What's New in v2.1

### Added
- ✅ Review & Cherry-pick Unicode cells dialog
- ✅ Highlight converted cells with color options
- ✅ License management system
- ✅ Pro Edition features
- ✅ Trial key generation
- ✅ Color picker for highlights
- ✅ Advanced skip selection logic

### Improved
- 🎨 Options panel layout (2 columns)
- 🔘 More action buttons
- 📊 Better cell tracking
- 💾 Enhanced conversion statistics
- 🎯 Precise cell coordinates for highlighting

### Technical
- 🏗️ Refactored conversion logic
- 📦 New dependencies: openpyxl PatternFill
- 💾 License file management
- 🔐 Hash-based license verification
- 🎨 Dynamic UI enabling/disabling

---

## 📊 Comparison: Free vs Pro

| Feature | Free | Pro |
|---------|------|-----|
| Basic conversion | ✅ | ✅ |
| Preview | ✅ | ✅ |
| Auto backup | ✅ | ✅ |
| Statistics | ✅ | ✅ |
| Export log | ✅ | ✅ |
| Review Unicode cells | ⚠️ Basic | ✅ Full |
| **Highlight cells** | ❌ | ✅ |
| Color options | ❌ | ✅ 6 colors |
| Advanced export | ❌ | ✅ |
| Priority support | ❌ | ✅ |
| Updates | ⚠️ Major only | ✅ All |

---

## 🎓 Tutorial: First-time Pro User

### Step 1: Install & Run
```bash
python gui_converter.py
```

### Step 2: Get License
1. Click **"🔑 Bản Quyền"**
2. Enter your email
3. Click **"🔑 Generate Trial Key"**
4. Copy and paste the key
5. Click **"✅ Kích Hoạt"**
6. See "Licensed to: [Your Name]" in title

### Step 3: Use Pro Features
1. ✅ Enable "🎨 Đánh dấu màu cells đã convert"
2. Select color (e.g., Yellow)
3. Choose file and Preview
4. Click **"🔍 Review & Chọn"**
5. Review Unicode cells, toggle as needed
6. Click **"🚀 Chuyển Đổi"**
7. Check output file - cells are highlighted! 🎨

### Step 4: Enjoy!
- Share with colleagues
- Report issues
- Request features

---

## 🆘 FAQ

### Q: Review button bị disabled?
**A:** Bật tùy chọn "Bỏ qua Unicode" và Preview trước.

### Q: Highlight không hoạt động?
**A:** Cần license Pro. Nhấn "🔑 Bản Quyền" để đăng ký.

### Q: License Key không hợp lệ?
**A:** Kiểm tra email đã nhập đúng chưa. Thử Generate Trial Key.

### Q: Muốn đổi màu highlight?
**A:** Chọn từ dropdown, màu preview hiển thị ngay.

### Q: File output không có màu?
**A:** Đảm bảo đã bật "Đánh dấu màu" và có license Pro.

### Q: Review dialog quá nhiều cells?
**A:** Dùng "Chọn tất cả" → "Bỏ chọn" những cells đặc biệt.

### Q: Làm sao backup license?
**A:** Copy file `license.json` ra nơi khác.

### Q: Trial key hết hạn?
**A:** Mua license chính thức hoặc generate key mới (demo).

---

## 🚀 Roadmap v2.2

### Planned Features
- [ ] Export selection presets
- [ ] Batch conversion with same settings
- [ ] Custom color picker (RGB)
- [ ] Highlight styles (bold, italic, border)
- [ ] Multi-color highlighting
- [ ] Undo/Redo for review
- [ ] Search/filter in review dialog
- [ ] License management API

---

**Chúc bạn sử dụng vui vẻ! 🎉**

*TCVN3 Converter Pro - Making legacy data modern again* ✨
