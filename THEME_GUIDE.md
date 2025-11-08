# 🌙 Modern Dark Theme v2.0

## ✨ Cải tiến giao diện

### 🎨 Dark Theme chuyên nghiệp
- **Catppuccin-inspired** color palette
- Dark background dễ nhìn cho mắt
- Contrast cao, dễ đọc
- Modern & minimalist design

### 🎯 Màu sắc

#### Background
- `#1e1e2e` - Main background (dark blue-gray)
- `#181825` - Darker elements
- `#313244` - Light panels
- `#45475a` - Hover states

#### Accent Colors
- 🔵 `#89b4fa` - Primary (Blue) - Actions chính
- 🟢 `#a6e3a1` - Success (Green) - Convert button
- 🟡 `#f9e2af` - Warning (Yellow) - Cảnh báo
- 🔴 `#f38ba8` - Error (Red) - Lỗi
- 🔷 `#89dceb` - Info (Cyan) - Thông tin
- 🟣 `#cba6f7` - Purple - Đặc biệt

#### Text
- `#cdd6f4` - Primary text (light)
- `#9399b2` - Secondary text (gray)
- `#6c7086` - Muted text (dim gray)

### 💫 Tính năng UI mới

#### 1. Header hiện đại
```
🔄 TCVN3 → Unicode Excel Converter
   v2.0 Modern Edition
```
- Title lớn, rõ ràng
- Subtitle version info
- Gradient-style headers

#### 2. File Selection Panel
- 📥 Input với icon
- 📤 Output với icon
- 📂 Buttons với emoji
- Monospace font cho đường dẫn (Consolas)
- Focus effects (highlight khi click)

#### 3. Options Panel
- ⚡ Icons cho mỗi option
- Hover effects
- Better spacing (20px padding)
- Checkboxes lớn hơn

#### 4. Action Buttons
- 👁️ **Xem Trước** (Primary Blue)
- 🚀 **Chuyển Đổi** (Success Green) 
- 📄 **Xuất Log** (Secondary Gray)
- Padding lớn (20x10)
- Bold font
- Hover effects

#### 5. Progress Bar
- Sleek 8px height
- Animated indeterminate
- Blue accent color
- Status text với emoji và percent

#### 6. Tabbed Interface
- 3 tabs đẹp mắt
- 👁️ Preview
- 📄 Conversion Log
- 📊 Thống Kê
- Selected tab highlighted
- Bigger tab padding (20x10)

#### 7. Text Areas
- Dark background (`#181825`)
- Light text (`#cdd6f4`)
- Consolas monospace font
- 10-11pt size
- Colored tags:
  - ✅ Success (Green)
  - ❌ Error (Red)
  - ⚠️ Warning (Yellow)
  - ℹ️ Info (Cyan)
  - 🔵 Primary (Blue)
  - 🟣 Purple

### 📐 Layout Improvements

#### Spacing
- Main container: 15px padding
- Sections: 15px vertical spacing
- Inside panels: 20px padding
- Elements: 8-10px spacing

#### Typography
- Headers: Segoe UI 16pt Bold
- Subtitles: Segoe UI 9pt
- Labels: Segoe UI 9pt Bold
- Body text: Segoe UI 9pt
- Code/paths: Consolas 9-11pt

#### Window
- Size: 1200x800 (lớn hơn)
- Centered on screen
- Resizable
- Minimum size: Auto

### 🎯 Visual Hierarchy

1. **Header** - Attention grabber
2. **File Selection** - Most important action
3. **Options** - Configuration
4. **Actions** - Primary operations
5. **Progress** - Feedback
6. **Results** - Detailed output

### ✨ Special Effects

#### Hover States
- Buttons brighten on hover
- Entries highlight on focus
- Tabs change color on hover

#### Focus Indicators
- Blue outline on focus
- Cursor color matches theme
- Selection color: `#585b70`

#### Color Tags in Text
```python
text.tag_config("success", fg="#a6e3a1", font="bold")
text.tag_config("error", fg="#f38ba8", font="bold")
text.tag_config("info", fg="#89dceb", font="bold")
text.tag_config("primary", fg="#89b4fa", font="bold")
```

### 📱 Responsive Design
- Window scales well
- Text wraps properly
- Scrollbars styled
- Grid layout with weights

### 🔧 Technical Details

#### Theme Implementation
```python
class ModernTheme:
    BG_DARK = "#1e1e2e"
    ACCENT_PRIMARY = "#89b4fa"
    TEXT_PRIMARY = "#cdd6f4"
    # ... more colors
```

#### Style Application
```python
def apply_modern_theme(self):
    style = ttk.Style()
    style.theme_use('clam')
    # Configure all widget styles
```

### 🎨 Color Palette Reference

#### Catppuccin Mocha (Inspired)
```
Background: #1e1e2e (Dark blue-gray)
Surface:    #313244 (Medium gray)
Overlay:    #45475a (Light gray)

Blue:   #89b4fa (Primary actions)
Green:  #a6e3a1 (Success/convert)
Yellow: #f9e2af (Warnings)
Red:    #f38ba8 (Errors)
Cyan:   #89dceb (Info)
Purple: #cba6f7 (Special)

Text:   #cdd6f4 (Main)
Subtext:#9399b2 (Secondary)
Muted:  #6c7086 (Dim)
```

### 🌟 Before vs After

#### Before (v1.0)
- ❌ Bright white background
- ❌ Default system theme
- ❌ Small fonts
- ❌ Cramped layout
- ❌ Basic buttons
- ❌ No visual hierarchy

#### After (v2.0)
- ✅ Professional dark theme
- ✅ Custom color palette
- ✅ Larger, readable fonts
- ✅ Spacious layout (20px padding)
- ✅ Styled buttons with icons
- ✅ Clear visual hierarchy
- ✅ Modern aesthetics
- ✅ Eye-friendly colors

### 💡 Design Philosophy

1. **Readability First** - High contrast text
2. **Visual Clarity** - Clear sections and spacing
3. **Modern Look** - Dark theme, flat design
4. **Professional** - Consistent colors and fonts
5. **Functional** - Icons convey meaning
6. **Comfortable** - Easy on the eyes

### 🚀 Usage Tips

- Dark theme works best in:
  - Low light environments
  - Long working sessions
  - Night-time usage
  
- Color coding helps:
  - 🔵 Blue = Actions
  - 🟢 Green = Success
  - 🟡 Yellow = Warning
  - 🔴 Red = Error

### 🎓 Customization

Want different colors? Edit `ModernTheme` class:

```python
class ModernTheme:
    # Change these to your preferred colors
    BG_DARK = "#your_color"
    ACCENT_PRIMARY = "#your_accent"
    # ...
```

---

**Enjoy the modern UI! 🌙✨**
