# -*- coding: utf-8 -*-
"""
Tạo icon cho ứng dụng
Sử dụng Pillow để tạo icon từ text/emoji hoặc từ ảnh có sẵn
"""
from PIL import Image, ImageDraw, ImageFont
import sys

def create_simple_icon():
    """Tạo icon đơn giản với emoji/text"""
    
    # Tạo image với nhiều kích thước (Windows ico format)
    sizes = [256, 128, 64, 48, 32, 16]
    images = []
    
    for size in sizes:
        # Tạo background gradient
        img = Image.new('RGB', (size, size), color='#1e1e2e')
        draw = ImageDraw.Draw(img)
        
        # Vẽ hình tròn nền
        margin = size // 8
        draw.ellipse(
            [margin, margin, size-margin, size-margin],
            fill='#89b4fa',
            outline='#cdd6f4',
            width=max(1, size//32)
        )
        
        # Vẽ text (có thể dùng emoji nếu font hỗ trợ)
        try:
            # Thử dùng font hệ thống
            font_size = size // 2
            font = ImageFont.truetype("seguiemj.ttf", font_size)  # Segoe UI Emoji
            text = "🔄"
        except:
            # Fallback: dùng text thông thường
            try:
                font_size = size // 3
                font = ImageFont.truetype("arial.ttf", font_size)
                text = "TC"
            except:
                font = ImageFont.load_default()
                text = "TC"
        
        # Căn giữa text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((size - text_width) // 2, (size - text_height) // 2 - size//20)
        
        draw.text(position, text, fill='#1e1e2e', font=font)
        
        images.append(img)
    
    # Lưu thành file .ico
    images[0].save(
        'icon.ico',
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:]
    )
    
    print("✅ Đã tạo icon.ico thành công!")
    print("📁 File: icon.ico")
    
    # Tạo thêm PNG cho preview
    images[0].save('icon_preview.png', format='PNG')
    print("📁 Preview: icon_preview.png")

def create_icon_from_image(image_path):
    """Tạo icon từ ảnh có sẵn"""
    try:
        img = Image.open(image_path)
        
        # Resize và lưu
        sizes = [256, 128, 64, 48, 32, 16]
        images = []
        
        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            images.append(resized)
        
        images[0].save(
            'icon.ico',
            format='ICO',
            sizes=[(img.width, img.height) for img in images],
            append_images=images[1:]
        )
        
        print(f"✅ Đã tạo icon từ {image_path}")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        print("Sẽ tạo icon mặc định...")
        create_simple_icon()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Nếu có đường dẫn ảnh
        create_icon_from_image(sys.argv[1])
    else:
        # Tạo icon mặc định
        create_simple_icon()
