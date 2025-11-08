# -*- coding: utf-8 -*-
"""
Example script: Sử dụng các API mới
"""

from pathlib import Path
from convert_excel_tcvn3 import (
    convert_excel,
    preview_conversion,
    export_conversion_log,
    looks_like_unicode_vietnamese,
)

def example_1_basic_conversion():
    """Ví dụ 1: Convert cơ bản"""
    print("="*80)
    print("VÍ DỤ 1: CONVERT CƠ BẢN")
    print("="*80)
    
    stats = convert_excel(
        "input_tcvn3.xlsx",
        "output_unicode.xlsx",
        skip_unicode=True  # Bỏ qua Unicode chuẩn
    )
    
    print(f"\n✅ Hoàn thành!")
    print(f"   • Đã convert: {stats.converted_cells} cells")
    print(f"   • Bỏ qua Unicode: {stats.already_unicode} cells")
    print(f"   • Tổng text cells: {stats.string_cells} cells")
    

def example_2_preview_first():
    """Ví dụ 2: Preview trước khi convert"""
    print("\n" + "="*80)
    print("VÍ DỤ 2: PREVIEW TRƯỚC KHI CONVERT")
    print("="*80)
    
    # Xem trước 20 mẫu
    samples = preview_conversion("input_tcvn3.xlsx", max_samples=20)
    
    print(f"\nTìm thấy {len(samples)} mẫu:")
    
    for i, sample in enumerate(samples[:5], 1):
        print(f"\n[{i}] Sheet: {sample.sheet}, Row: {sample.row}")
        print(f"    Status: {'Unicode ✅' if sample.was_unicode else 'TCVN3 🔄'}")
        print(f"    Trước:  {sample.original}")
        print(f"    Sau:    {sample.converted}")
    
    # Hỏi confirm
    response = input("\nTiếp tục convert? (y/n): ")
    if response.lower() == 'y':
        stats = convert_excel("input_tcvn3.xlsx", "output_unicode.xlsx")
        print(f"✅ Đã convert {stats.converted_cells} cells")


def example_3_with_logging():
    """Ví dụ 3: Convert và xuất log"""
    print("\n" + "="*80)
    print("VÍ DỤ 3: CONVERT VỚI LOG CHI TIẾT")
    print("="*80)
    
    stats = convert_excel(
        "input_tcvn3.xlsx",
        "output_unicode.xlsx",
        skip_unicode=True
    )
    
    # Xuất log
    log_file = "conversion_log.txt"
    export_conversion_log(stats, log_file)
    
    print(f"\n✅ Hoàn thành!")
    print(f"   • File output: output_unicode.xlsx")
    print(f"   • Log file: {log_file}")
    print(f"   • Converted: {stats.converted_cells} cells")


def example_4_batch_conversion():
    """Ví dụ 4: Convert hàng loạt files"""
    print("\n" + "="*80)
    print("VÍ DỤ 4: BATCH CONVERSION")
    print("="*80)
    
    input_dir = Path("input_folder")
    output_dir = Path("output_folder")
    output_dir.mkdir(exist_ok=True)
    
    excel_files = list(input_dir.glob("*.xlsx"))
    print(f"\nTìm thấy {len(excel_files)} files Excel")
    
    for i, file in enumerate(excel_files, 1):
        print(f"\n[{i}/{len(excel_files)}] Processing: {file.name}")
        
        output_file = output_dir / f"{file.stem}_unicode.xlsx"
        
        try:
            stats = convert_excel(file, output_file, skip_unicode=True)
            print(f"   ✅ Converted {stats.converted_cells} cells")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n✅ Hoàn thành batch conversion!")


def example_5_check_unicode():
    """Ví dụ 5: Kiểm tra text có phải Unicode không"""
    print("\n" + "="*80)
    print("VÍ DỤ 5: KIỂM TRA UNICODE")
    print("="*80)
    
    test_texts = [
        "Nguyễn Văn A",
        "Hà Nội",
        "Hµ Néi",  # TCVN3
        "Th¸nh phè Hå ChÝ Minh",  # TCVN3
        "Hello World 123",
        "Email: test@example.com",
    ]
    
    print("\nKiểm tra các chuỗi:")
    for text in test_texts:
        is_unicode = looks_like_unicode_vietnamese(text)
        status = "✅ Unicode" if is_unicode else "🔄 TCVN3?"
        print(f"{status:12} | {text}")


def example_6_with_progress():
    """Ví dụ 6: Hiển thị progress"""
    print("\n" + "="*80)
    print("VÍ DỤ 6: CONVERT VỚI PROGRESS CALLBACK")
    print("="*80)
    
    def show_progress(sheet_name, sheet_idx, total_sheets):
        percent = ((sheet_idx + 1) / total_sheets) * 100
        print(f"Progress: [{percent:5.1f}%] Sheet {sheet_idx+1}/{total_sheets}: {sheet_name}")
    
    stats = convert_excel(
        "input_tcvn3.xlsx",
        "output_unicode.xlsx",
        skip_unicode=True,
        progress_callback=show_progress
    )
    
    print(f"\n✅ Hoàn thành! Converted {stats.converted_cells} cells")


def main():
    """Chạy tất cả examples"""
    print("\n🎯 EXAMPLES - TCVN3 CONVERTER API")
    print("\nChọn example để chạy:")
    print("1. Convert cơ bản")
    print("2. Preview trước khi convert")
    print("3. Convert với log chi tiết")
    print("4. Batch conversion")
    print("5. Kiểm tra Unicode")
    print("6. Convert với progress callback")
    print("0. Thoát")
    
    choice = input("\nNhập số (0-6): ").strip()
    
    examples = {
        "1": example_1_basic_conversion,
        "2": example_2_preview_first,
        "3": example_3_with_logging,
        "4": example_4_batch_conversion,
        "5": example_5_check_unicode,
        "6": example_6_with_progress,
    }
    
    if choice in examples:
        try:
            examples[choice]()
        except FileNotFoundError as e:
            print(f"\n❌ Lỗi: Không tìm thấy file - {e}")
            print("   Vui lòng chuẩn bị file input trước!")
        except Exception as e:
            print(f"\n❌ Lỗi: {e}")
    elif choice == "0":
        print("Tạm biệt!")
    else:
        print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    # Chạy example 5 (không cần file) để demo
    example_5_check_unicode()
    
    # Hoặc uncomment dòng dưới để chạy interactive menu
    # main()
