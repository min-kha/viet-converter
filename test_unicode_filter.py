# -*- coding: utf-8 -*-
"""
Script demo các tính năng mới
"""
from convert_excel_tcvn3 import looks_like_unicode_vietnamese

# Test cases
test_cases = [
    ("Nguyễn Văn A", "Chữ Việt Unicode chuẩn"),
    ("Hà Nội", "Chữ Việt Unicode chuẩn"),
    ("Hµ Néi", "TCVN3 - có ký tự lạ µ, É"),
    ("Th¸nh phè Hå ChÝ Minh", "TCVN3 - nhiều ký tự lạ"),
    ("Hello World 123", "Tiếng Anh + số"),
    ("Giá: 1,000,000đ", "Chữ Việt + số + ký tự đặc biệt"),
    ("Email: test@example.com", "Chữ Việt + email"),
    ("", "Chuỗi rỗng"),
    ("123456", "Chỉ có số"),
    ("Tổng: 50% (100/200)", "Chữ Việt + toán học"),
]

print("=" * 80)
print("TEST BỘ LỌC UNICODE VIETNAMESE")
print("=" * 80)
print()

for text, description in test_cases:
    result = looks_like_unicode_vietnamese(text)
    status = "✅ Unicode chuẩn" if result else "🔄 Cần kiểm tra (TCVN3?)"
    
    print(f"Text: {text!r}")
    print(f"Mô tả: {description}")
    print(f"Kết quả: {status}")
    print("-" * 80)

print()
print("📝 Tổng kết:")
print("✅ = Bỏ qua (đã là Unicode chuẩn)")
print("🔄 = Cần convert (có thể là TCVN3)")
