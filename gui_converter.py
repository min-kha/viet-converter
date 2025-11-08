# -*- coding: utf-8 -*-
"""
GUI Converter TCVN3 → Unicode cho Excel
Modern Dark Theme with Beautiful UI
Pro Edition với License Management
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, font
from pathlib import Path
import threading
from datetime import datetime
import shutil
import json
import hashlib
from typing import Dict, Set

from convert_excel_tcvn3 import (
    convert_excel,
    preview_conversion,
    export_conversion_log,
    looks_like_unicode_vietnamese,
    ConversionStats,
    ConversionLog,
)


# ==================== MODERN DARK THEME COLORS ====================
class ModernTheme:
    """Modern Dark Theme Color Palette"""
    # Background colors
    BG_DARK = "#1e1e2e"          # Main background
    BG_DARKER = "#181825"        # Darker elements
    BG_LIGHT = "#313244"         # Light background (panels)
    BG_HOVER = "#45475a"         # Hover state
    
    # Accent colors
    ACCENT_PRIMARY = "#89b4fa"   # Blue - primary actions
    ACCENT_SUCCESS = "#a6e3a1"   # Green - success
    ACCENT_WARNING = "#f9e2af"   # Yellow - warning
    ACCENT_ERROR = "#f38ba8"     # Red - error
    ACCENT_INFO = "#89dceb"      # Cyan - info
    ACCENT_PURPLE = "#cba6f7"    # Purple - special
    
    # Text colors
    TEXT_PRIMARY = "#cdd6f4"     # Main text
    TEXT_SECONDARY = "#9399b2"   # Secondary text
    TEXT_MUTED = "#6c7086"       # Muted text
    
    # Border & divider
    BORDER = "#45475a"
    DIVIDER = "#313244"
    
    # Special
    SELECTION = "#585b70"
    SHADOW = "#11111b"


class ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔄 KH - TCVN3 → Unicode Converter Pro")
        self.root.geometry("1200x850")
        self.root.resizable(True, True)
        
        # Set window icon (cho titlebar và taskbar)
        self.set_window_icon()
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.skip_unicode = tk.BooleanVar(value=True)
        self.auto_backup = tk.BooleanVar(value=True)
        self.highlight_converted = tk.BooleanVar(value=False)
        self.highlight_color = tk.StringVar(value="#FFFF00")  # Yellow
        self.preview_data = []
        self.conversion_stats = None
        
        # New: Skip selection tracking
        self.skip_selection: Dict[str, bool] = {}  # cell_id -> should_skip
        self.unicode_cells_to_review = []
        
        # License info
        self.license_info = self.load_license()
        
        # Apply modern theme
        self.apply_modern_theme()
        self.setup_ui()
        
        # Show license info
        self.display_license_info()
    
    def get_resource_path(self, relative_path: str) -> Path:
        """Get absolute path to resource (works for dev and exe)"""
        import sys
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = Path(sys._MEIPASS)
        except Exception:
            base_path = Path(__file__).parent
        
        return base_path / relative_path
    
    def set_window_icon(self):
        """Set window icon for titlebar and taskbar"""
        try:
            # Thử load icon.ico từ resource path
            icon_path = self.get_resource_path("icon.ico")
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
                return
        except Exception as e:
            print(f"Warning: Could not load icon.ico: {e}")
        
        try:
            # Fallback: Tạo icon từ PhotoImage (PNG)
            icon_png = self.get_resource_path("icon_preview.png")
            if icon_png.exists():
                from PIL import Image, ImageTk
                img = Image.open(icon_png)
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.root.iconphoto(True, photo)
                # Giữ reference để không bị garbage collect
                self.root._icon_photo = photo
                return
        except Exception as e:
            print(f"Warning: Could not load icon PNG: {e}")
        
        # Nếu không có icon nào, dùng default
        try:
            self.root.iconbitmap(default='')
        except:
            pass
    
    def apply_modern_theme(self):
        """Apply modern dark theme to the application"""
        self.root.configure(bg=ModernTheme.BG_DARK)
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure main background
        style.configure(".", 
            background=ModernTheme.BG_DARK,
            foreground=ModernTheme.TEXT_PRIMARY,
            borderwidth=0,
            focuscolor=ModernTheme.ACCENT_PRIMARY
        )
        
        # LabelFrame style
        style.configure("Modern.TLabelframe",
            background=ModernTheme.BG_LIGHT,
            foreground=ModernTheme.TEXT_PRIMARY,
            borderwidth=2,
            relief="flat",
            bordercolor=ModernTheme.BORDER
        )
        style.configure("Modern.TLabelframe.Label",
            background=ModernTheme.BG_LIGHT,
            foreground=ModernTheme.ACCENT_PRIMARY,
            font=("Segoe UI", 10, "bold")
        )
        
        # Entry style
        style.configure("Modern.TEntry",
            fieldbackground=ModernTheme.BG_DARKER,
            background=ModernTheme.BG_DARKER,
            foreground=ModernTheme.TEXT_PRIMARY,
            borderwidth=2,
            relief="flat",
            insertcolor=ModernTheme.TEXT_PRIMARY
        )
        style.map("Modern.TEntry",
            fieldbackground=[('focus', ModernTheme.BG_LIGHT)],
            bordercolor=[('focus', ModernTheme.ACCENT_PRIMARY)]
        )
        
        # Button styles
        style.configure("Primary.TButton",
            background=ModernTheme.ACCENT_PRIMARY,
            foreground=ModernTheme.BG_DARK,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padding=(20, 10)
        )
        style.map("Primary.TButton",
            background=[('active', ModernTheme.ACCENT_INFO), ('pressed', ModernTheme.ACCENT_PRIMARY)]
        )
        
        style.configure("Success.TButton",
            background=ModernTheme.ACCENT_SUCCESS,
            foreground=ModernTheme.BG_DARK,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padding=(20, 10)
        )
        
        style.configure("Secondary.TButton",
            background=ModernTheme.BG_LIGHT,
            foreground=ModernTheme.TEXT_PRIMARY,
            borderwidth=1,
            relief="flat",
            font=("Segoe UI", 9),
            padding=(15, 8)
        )
        style.map("Secondary.TButton",
            background=[('active', ModernTheme.BG_HOVER)]
        )
        
        # Label style
        style.configure("Modern.TLabel",
            background=ModernTheme.BG_LIGHT,
            foreground=ModernTheme.TEXT_PRIMARY,
            font=("Segoe UI", 9)
        )
        
        style.configure("Header.TLabel",
            background=ModernTheme.BG_DARK,
            foreground=ModernTheme.ACCENT_PRIMARY,
            font=("Segoe UI", 11, "bold")
        )
        
        # Checkbutton style
        style.configure("Modern.TCheckbutton",
            background=ModernTheme.BG_LIGHT,
            foreground=ModernTheme.TEXT_PRIMARY,
            font=("Segoe UI", 9)
        )
        style.map("Modern.TCheckbutton",
            background=[('active', ModernTheme.BG_LIGHT)],
            foreground=[('active', ModernTheme.ACCENT_PRIMARY)]
        )
        
        # Progressbar style
        style.configure("Modern.Horizontal.TProgressbar",
            background=ModernTheme.ACCENT_PRIMARY,
            troughcolor=ModernTheme.BG_DARKER,
            borderwidth=0,
            thickness=8
        )
        
        # Notebook style
        style.configure("Modern.TNotebook",
            background=ModernTheme.BG_LIGHT,
            borderwidth=0
        )
        style.configure("Modern.TNotebook.Tab",
            background=ModernTheme.BG_DARKER,
            foreground=ModernTheme.TEXT_SECONDARY,
            padding=(20, 10),
            borderwidth=0,
            font=("Segoe UI", 9, "bold")
        )
        style.map("Modern.TNotebook.Tab",
            background=[('selected', ModernTheme.BG_LIGHT)],
            foreground=[('selected', ModernTheme.ACCENT_PRIMARY)]
        )
        
        # Frame style
        style.configure("Modern.TFrame",
            background=ModernTheme.BG_DARK
        )
    
    def get_license_file_path(self) -> Path:
        """Get license file path (works for both dev and exe)"""
        import os
        import sys
        
        # Nếu chạy từ exe (PyInstaller)
        if getattr(sys, 'frozen', False):
            # Lưu vào AppData để persistent
            appdata = os.getenv('APPDATA')
            if appdata:
                app_dir = Path(appdata) / "TCVN3_Converter_Pro"
                app_dir.mkdir(parents=True, exist_ok=True)
                return app_dir / "license.json"
            else:
                # Fallback: cùng thư mục exe
                return Path(sys.executable).parent / "license.json"
        else:
            # Development mode: cùng thư mục script
            return Path(__file__).parent / "license.json"
    
    def load_license(self) -> dict:
        """Load license information from file or create new"""
        license_file = self.get_license_file_path()
        
        if license_file.exists():
            try:
                with open(license_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load license: {e}")
        
        # Default free license
        return {
            "type": "Free",
            "user": "Demo User",
            "email": "",
            "company": "",
            "license_key": "",
            "features": ["basic_conversion", "preview"],
            "registered": False
        }
    
    def save_license(self, license_data: dict):
        """Save license information"""
        try:
            license_file = self.get_license_file_path()
            # Ensure parent directory exists
            license_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(license_file, 'w', encoding='utf-8') as f:
                json.dump(license_data, f, indent=2, ensure_ascii=False)
            
            self.license_info = license_data
            print(f"✅ License saved to: {license_file}")
        except Exception as e:
            print(f"❌ Could not save license: {e}")
            messagebox.showerror("Lỗi", f"Không thể lưu license:\n{e}")
    
    def verify_license_key(self, key: str, email: str) -> bool:
        """Verify license key (simple hash-based verification)"""
        # Simple verification: hash of email + secret
        secret = "NGUYEN_MINH_KHA"
        expected = hashlib.sha256(f"{email}{secret}".encode()).hexdigest()[:16].upper()
        return key.upper() == expected
    
    def display_license_info(self):
        """Display license info in title"""
        if self.license_info.get("registered"):
            user = self.license_info.get("user", "User")
            self.root.title(f"🔄 KH - TCVN3 → Unicode Converter Pro - Licensed to: {user}")
        else:
            self.root.title("🔄 KH - TCVN3 → Unicode Converter Pro - Free Edition")
        
    def setup_ui(self):
        """Thiết lập giao diện hiện đại"""
        # Main container with padding
        main_container = ttk.Frame(self.root, style="Modern.TFrame", padding=15)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ========== HEADER ==========
        header_frame = ttk.Frame(main_container, style="Modern.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(
            header_frame,
            text="🔄 TCVN3 → Unicode Excel Converter",
            style="Header.TLabel",
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="v2.0 Modern Edition",
            background=ModernTheme.BG_DARK,
            foreground=ModernTheme.TEXT_MUTED,
            font=("Segoe UI", 9)
        )
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # ========== SECTION 1: File Selection ==========
        file_frame = ttk.LabelFrame(
            main_container,
            text="  📁  Chọn File Excel",
            padding=20,
            style="Modern.TLabelframe"
        )
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Input file
        input_label = ttk.Label(
            file_frame,
            text="📥 File Input (TCVN3):",
            style="Modern.TLabel",
            font=("Segoe UI", 9, "bold")
        )
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        input_entry = ttk.Entry(
            file_frame,
            textvariable=self.input_file,
            width=70,
            style="Modern.TEntry",
            font=("Consolas", 9)
        )
        input_entry.grid(row=0, column=1, padx=(10, 10), pady=(0, 8), sticky=tk.EW)
        
        input_btn = ttk.Button(
            file_frame,
            text="📂 Chọn",
            command=self.browse_input,
            style="Secondary.TButton"
        )
        input_btn.grid(row=0, column=2, pady=(0, 8))
        
        # Output file
        output_label = ttk.Label(
            file_frame,
            text="📤 File Output (Unicode):",
            style="Modern.TLabel",
            font=("Segoe UI", 9, "bold")
        )
        output_label.grid(row=1, column=0, sticky=tk.W)
        
        output_entry = ttk.Entry(
            file_frame,
            textvariable=self.output_file,
            width=70,
            style="Modern.TEntry",
            font=("Consolas", 9)
        )
        output_entry.grid(row=1, column=1, padx=(10, 10), sticky=tk.EW)
        
        output_btn = ttk.Button(
            file_frame,
            text="💾 Chọn",
            command=self.browse_output,
            style="Secondary.TButton"
        )
        output_btn.grid(row=1, column=2)
        
        file_frame.columnconfigure(1, weight=1)
        
        # ========== SECTION 2: Options ==========
        options_frame = ttk.LabelFrame(
            main_container,
            text="  ⚙️  Tùy Chọn  ",
            padding=20,
            style="Modern.TLabelframe"
        )
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Left column - Basic options
        left_opts = ttk.Frame(options_frame, style="Modern.TFrame")
        left_opts.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        opt1 = ttk.Checkbutton(
            left_opts,
            text="⚡ Bỏ qua cells đã là Unicode chuẩn",
            variable=self.skip_unicode,
            style="Modern.TCheckbutton",
            command=self.on_skip_unicode_changed
        )
        opt1.pack(anchor=tk.W, pady=5)
        
        opt2 = ttk.Checkbutton(
            left_opts,
            text="💾 Tự động backup file gốc trước khi convert (an toàn)",
            variable=self.auto_backup,
            style="Modern.TCheckbutton"
        )
        opt2.pack(anchor=tk.W, pady=5)
        
        # Right column - Advanced options (Pro)
        right_opts = ttk.Frame(options_frame, style="Modern.TFrame")
        right_opts.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        opt3 = ttk.Checkbutton(
            right_opts,
            text="🎨 Đánh dấu màu cells đã convert (Pro)",
            variable=self.highlight_converted,
            style="Modern.TCheckbutton",
            command=self.on_highlight_changed
        )
        opt3.pack(anchor=tk.W, pady=5)
        
        # Color picker frame
        color_frame = ttk.Frame(right_opts, style="Modern.TFrame")
        color_frame.pack(anchor=tk.W, pady=(0, 5), padx=(25, 0))
        
        ttk.Label(
            color_frame,
            text="Màu đánh dấu:",
            style="Modern.TLabel",
            font=("Segoe UI", 8)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.color_picker = ttk.Combobox(
            color_frame,
            textvariable=self.highlight_color,
            values=["#FFFF00", "#00FF00", "#00FFFF", "#FF00FF", "#FFA500", "#FFB6C1"],
            width=10,
            state="readonly",
            font=("Consolas", 8)
        )
        self.color_picker.pack(side=tk.LEFT)
        
        # Preview color button
        self.color_preview_btn = tk.Button(
            color_frame,
            text="  ",
            width=3,
            bg=self.highlight_color.get(),
            relief="raised",
            command=self.show_color_preview
        )
        self.color_preview_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Update color preview when changed
        self.highlight_color.trace('w', self.update_color_preview)
        
        # ========== SECTION 3: Actions ==========
        action_frame = ttk.Frame(main_container, style="Modern.TFrame")
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.btn_preview = ttk.Button(
            action_frame,
            text="👁️  Xem Trước",
            command=self.show_preview,
            style="Primary.TButton"
        )
        self.btn_preview.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        self.btn_review = ttk.Button(
            action_frame,
            text="🔍  Review & Chọn",
            command=self.show_review_dialog,
            state=tk.DISABLED,
            style="Primary.TButton"
        )
        self.btn_review.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        self.btn_convert = ttk.Button(
            action_frame,
            text="🚀  Chuyển Đổi",
            command=self.start_conversion,
            style="Success.TButton"
        )
        self.btn_convert.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        self.btn_export_log = ttk.Button(
            action_frame,
            text="📄  Xuất Log",
            command=self.export_log,
            state=tk.DISABLED,
            style="Secondary.TButton"
        )
        self.btn_export_log.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        self.btn_license = ttk.Button(
            action_frame,
            text="🔑  Bản Quyền",
            command=self.show_license_dialog,
            style="Secondary.TButton"
        )
        self.btn_license.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # ========== SECTION 4: Progress ==========
        progress_frame = ttk.LabelFrame(
            main_container,
            text="  📊  Tiến Trình  ",
            padding=20,
            style="Modern.TLabelframe"
        )
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_label = ttk.Label(
            progress_frame,
            text="⏳ Sẵn sàng để bắt đầu...",
            style="Modern.TLabel",
            font=("Segoe UI", 10)
        )
        self.progress_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode="indeterminate",
            style="Modern.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X)
        
        # ========== SECTION 5: Results/Log ==========
        result_frame = ttk.LabelFrame(
            main_container,
            text="  📝  Kết Quả & Log  ",
            padding=15,
            style="Modern.TLabelframe"
        )
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(result_frame, style="Modern.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Preview
        preview_tab = ttk.Frame(self.notebook, style="Modern.TFrame")
        self.notebook.add(preview_tab, text="  👁️  Preview  ")
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_tab,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=ModernTheme.BG_DARKER,
            fg=ModernTheme.TEXT_PRIMARY,
            insertbackground=ModernTheme.TEXT_PRIMARY,
            selectbackground=ModernTheme.SELECTION,
            selectforeground=ModernTheme.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 2: Conversion Log
        log_tab = ttk.Frame(self.notebook, style="Modern.TFrame")
        self.notebook.add(log_tab, text="  📄  Conversion Log  ")
        
        self.log_text = scrolledtext.ScrolledText(
            log_tab,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=ModernTheme.BG_DARKER,
            fg=ModernTheme.TEXT_PRIMARY,
            insertbackground=ModernTheme.TEXT_PRIMARY,
            selectbackground=ModernTheme.SELECTION,
            selectforeground=ModernTheme.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 3: Statistics
        stats_tab = ttk.Frame(self.notebook, style="Modern.TFrame")
        self.notebook.add(stats_tab, text="  📊  Thống Kê  ")
        
        self.stats_text = scrolledtext.ScrolledText(
            stats_tab,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg=ModernTheme.BG_DARKER,
            fg=ModernTheme.TEXT_PRIMARY,
            insertbackground=ModernTheme.TEXT_PRIMARY,
            selectbackground=ModernTheme.SELECTION,
            selectforeground=ModernTheme.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure text tags for colored output
        self._configure_text_tags()
    
    def _configure_text_tags(self):
        """Configure color tags for text widgets"""
        for text_widget in [self.preview_text, self.log_text, self.stats_text]:
            text_widget.tag_config("success", foreground=ModernTheme.ACCENT_SUCCESS, font=("Consolas", 10, "bold"))
            text_widget.tag_config("error", foreground=ModernTheme.ACCENT_ERROR, font=("Consolas", 10, "bold"))
            text_widget.tag_config("warning", foreground=ModernTheme.ACCENT_WARNING, font=("Consolas", 10, "bold"))
            text_widget.tag_config("info", foreground=ModernTheme.ACCENT_INFO, font=("Consolas", 10, "bold"))
            text_widget.tag_config("primary", foreground=ModernTheme.ACCENT_PRIMARY, font=("Consolas", 10, "bold"))
            text_widget.tag_config("purple", foreground=ModernTheme.ACCENT_PURPLE, font=("Consolas", 10, "bold"))
            text_widget.tag_config("muted", foreground=ModernTheme.TEXT_MUTED)
            text_widget.tag_config("header", foreground=ModernTheme.ACCENT_PRIMARY, font=("Consolas", 12, "bold"))
        
    def browse_input(self):
        """Chọn file input"""
        filename = filedialog.askopenfilename(
            title="Chọn file Excel TCVN3",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.input_file.set(filename)
            # Auto suggest output filename
            if not self.output_file.get():
                input_path = Path(filename)
                output_path = input_path.parent / f"{input_path.stem}_unicode{input_path.suffix}"
                self.output_file.set(str(output_path))
    
    def browse_output(self):
        """Chọn file output"""
        filename = filedialog.asksaveasfilename(
            title="Lưu file Unicode",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.output_file.set(filename)
    
    def validate_files(self) -> bool:
        """Kiểm tra file input/output"""
        if not self.input_file.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn file input!")
            return False
        
        if not Path(self.input_file.get()).exists():
            messagebox.showerror("Lỗi", "File input không tồn tại!")
            return False
        
        if not self.output_file.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn file output!")
            return False
        
        return True
    
    def show_preview(self):
        """Hiển thị preview các cell sẽ được convert"""
        if not self.validate_files():
            return
        
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, "🔍 Đang quét file...\n\n")
        self.root.update()
        
        try:
            # Run preview in thread to avoid freezing UI
            def preview_thread():
                # Lấy TẤT CẢ cells (không giới hạn) để review đầy đủ
                samples = preview_conversion(self.input_file.get(), max_samples=None)
                self.preview_data = samples
                
                # Update UI in main thread
                self.root.after(0, lambda: self.display_preview(samples))
            
            threading.Thread(target=preview_thread, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể preview: {e}")
            self.preview_text.insert(tk.END, f"❌ Lỗi: {e}\n")
    
    def display_preview(self, samples: list[ConversionLog]):
        """Hiển thị kết quả preview"""
        self.preview_text.delete(1.0, tk.END)
        
        if not samples:
            self.preview_text.insert(tk.END, "✅ Không tìm thấy cell nào cần convert!\n")
            self.preview_text.insert(tk.END, "Có thể file đã được convert sang Unicode rồi.\n")
            self.btn_review.config(state=tk.DISABLED)
            return
        
        # Enable review button if skip_unicode is on
        if self.skip_unicode.get():
            self.btn_review.config(state=tk.NORMAL)
        
        # Group by status
        unicode_cells = [s for s in samples if s.was_unicode]
        tcvn3_cells = [s for s in samples if not s.was_unicode]
        
        self.preview_text.insert(tk.END, f"📊 Tìm thấy {len(samples)} cells có text:\n\n")
        
        if unicode_cells:
            self.preview_text.insert(tk.END, f"✅ {len(unicode_cells)} cells đã là Unicode chuẩn")
            if self.skip_unicode.get():
                self.preview_text.insert(tk.END, " → SẼ BỎ QUA\n")
            else:
                self.preview_text.insert(tk.END, " → SẼ VẪN XỬ LÝ\n")
        
        if tcvn3_cells:
            self.preview_text.insert(tk.END, f"🔄 {len(tcvn3_cells)} cells cần convert từ TCVN3\n")
        
        self.preview_text.insert(tk.END, "\n" + "="*80 + "\n\n")
        
        # Show samples (chỉ hiển thị 50 đầu tiên để không lag UI, nhưng data đầy đủ)
        display_limit = 50
        for i, log in enumerate(samples[:display_limit], 1):
            status = "✅ Unicode" if log.was_unicode else "🔄 TCVN3"
            self.preview_text.insert(tk.END, f"[{i}] {status} | Sheet: {log.sheet} | Row: {log.row} | Col: {log.col_name}\n")
            self.preview_text.insert(tk.END, f"    TRƯỚC:  {log.original}\n")
            self.preview_text.insert(tk.END, f"    SAU:    {log.converted}\n")
            
            if log.original != log.converted:
                self.preview_text.insert(tk.END, "    ⚠️  CÓ THAY ĐỔI\n")
            else:
                self.preview_text.insert(tk.END, "    ℹ️  Không đổi\n")
            
            self.preview_text.insert(tk.END, "\n")
        
        if len(samples) > display_limit:
            self.preview_text.insert(tk.END, f"\n... và {len(samples) - display_limit} cells khác\n")
            self.preview_text.insert(tk.END, f"💡 Xem đầy đủ {len(unicode_cells)} cells Unicode trong 'Review & Chọn'\n")
        
        # Ask for confirmation
        msg = f"Tìm thấy {len(tcvn3_cells)} cells cần convert.\n\n"
        if unicode_cells:
            msg += f"{len(unicode_cells)} cells đã là Unicode chuẩn"
            if self.skip_unicode.get():
                msg += " sẽ được BỎ QUA.\n\n"
            else:
                msg += " sẽ VẪN được xử lý.\n\n"
        msg += "Bạn có muốn tiếp tục convert?"
        
        if messagebox.askyesno("Xác nhận", msg):
            self.start_conversion()
    
    def start_conversion(self):
        """Bắt đầu convert"""
        if not self.validate_files():
            return
        
        # Backup if enabled
        if self.auto_backup.get():
            try:
                input_path = Path(self.input_file.get())
                backup_path = input_path.parent / f"{input_path.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{input_path.suffix}"
                shutil.copy2(input_path, backup_path)
                self.log_message(f"✅ Đã backup: {backup_path.name}\n")
            except Exception as e:
                if not messagebox.askyesno("Cảnh báo", f"Không thể backup file: {e}\n\nVẫn tiếp tục?"):
                    return
        
        # Disable buttons
        self.btn_preview.config(state=tk.DISABLED)
        self.btn_convert.config(state=tk.DISABLED)
        
        # Start progress
        self.progress_bar.config(mode="indeterminate")
        self.progress_bar.start()
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        self.stats_text.delete(1.0, tk.END)
        
        # Run conversion in thread
        def convert_thread():
            try:
                stats = convert_excel(
                    self.input_file.get(),
                    self.output_file.get(),
                    skip_unicode=self.skip_unicode.get(),
                    progress_callback=self.update_progress,
                    skip_selection=self.skip_selection if self.skip_selection else None,
                    highlight_converted=self.highlight_converted.get(),
                    highlight_color=self.highlight_color.get()
                )
                
                self.conversion_stats = stats
                
                # Update UI in main thread
                self.root.after(0, lambda: self.conversion_complete(stats))
                
            except Exception as e:
                self.root.after(0, lambda: self.conversion_error(e))
        
        threading.Thread(target=convert_thread, daemon=True).start()
    
    def update_progress(self, sheet_name, sheet_idx, total_sheets):
        """Cập nhật tiến trình"""
        percent = ((sheet_idx + 1) / total_sheets) * 100
        self.progress_label.config(
            text=f"⚙️ Đang xử lý sheet {sheet_idx + 1}/{total_sheets}: {sheet_name} [{percent:.0f}%]"
        )
        self.root.update()
    
    def conversion_complete(self, stats: ConversionStats):
        """Hoàn thành conversion"""
        self.progress_bar.stop()
        self.progress_bar.config(mode="determinate", value=100)
        self.progress_label.config(text="✅ Hoàn thành! Convert thành công.")
        
        # Enable buttons
        self.btn_preview.config(state=tk.NORMAL)
        self.btn_convert.config(state=tk.NORMAL)
        self.btn_export_log.config(state=tk.NORMAL)
        
        # Display log
        self.display_conversion_log(stats)
        
        # Display stats
        self.display_statistics(stats)
        
        # Switch to log tab
        self.notebook.select(1)
        
        # Show message
        msg = f"✅ Chuyển đổi thành công!\n\n"
        msg += f"📊 Thống kê:\n"
        msg += f"  • Tổng cells: {stats.total_cells:,}\n"
        msg += f"  • Cells text: {stats.string_cells:,}\n"
        msg += f"  • Đã là Unicode: {stats.already_unicode:,}\n"
        msg += f"  • Đã convert: {stats.converted_cells:,}\n"
        msg += f"  • Không đổi: {stats.unchanged_cells:,}\n"
        msg += f"\n📁 File output: {self.output_file.get()}"
        
        messagebox.showinfo("Thành công", msg)
    
    def conversion_error(self, error):
        """Xử lý lỗi conversion"""
        self.progress_bar.stop()
        self.progress_label.config(text="❌ Có lỗi xảy ra!")
        
        # Enable buttons
        self.btn_preview.config(state=tk.NORMAL)
        self.btn_convert.config(state=tk.NORMAL)
        
        # Show error
        self.log_message(f"❌ Lỗi: {error}\n")
        messagebox.showerror("Lỗi", f"Không thể chuyển đổi:\n\n{error}")
    
    def display_conversion_log(self, stats: ConversionStats):
        """Hiển thị log chi tiết"""
        self.log_text.delete(1.0, tk.END)
        
        self.log_text.insert(tk.END, "="*80 + "\n")
        self.log_text.insert(tk.END, "TCVN3 → Unicode Conversion Log\n")
        self.log_text.insert(tk.END, f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.log_text.insert(tk.END, "="*80 + "\n\n")
        
        if stats.logs:
            self.log_text.insert(tk.END, f"📝 Chi tiết {len(stats.logs)} cells đã convert:\n")
            self.log_text.insert(tk.END, "-"*80 + "\n\n")
            
            for i, log in enumerate(stats.logs, 1):
                self.log_text.insert(tk.END, f"[{i}] Sheet: {log.sheet} | Row: {log.row} | Col: {log.col_name}\n")
                self.log_text.insert(tk.END, f"    TRƯỚC:  {log.original}\n")
                self.log_text.insert(tk.END, f"    SAU:    {log.converted}\n\n")
        else:
            self.log_text.insert(tk.END, "Không có cell nào cần convert.\n")
    
    def display_statistics(self, stats: ConversionStats):
        """Hiển thị thống kê"""
        self.stats_text.delete(1.0, tk.END)
        
        self.stats_text.insert(tk.END, "="*60 + "\n")
        self.stats_text.insert(tk.END, "📊 THỐNG KÊ CHUYỂN ĐỔI\n")
        self.stats_text.insert(tk.END, "="*60 + "\n\n")
        
        self.stats_text.insert(tk.END, f"📁 File Input:  {self.input_file.get()}\n")
        self.stats_text.insert(tk.END, f"📁 File Output: {self.output_file.get()}\n\n")
        
        self.stats_text.insert(tk.END, f"📊 Tổng quan:\n")
        self.stats_text.insert(tk.END, f"   • Tổng số cells:        {stats.total_cells:>10,}\n")
        self.stats_text.insert(tk.END, f"   • Cells chứa text:      {stats.string_cells:>10,}\n")
        self.stats_text.insert(tk.END, f"   • Đã là Unicode chuẩn:  {stats.already_unicode:>10,}\n")
        self.stats_text.insert(tk.END, f"   • Đã convert:           {stats.converted_cells:>10,}\n")
        self.stats_text.insert(tk.END, f"   • Không thay đổi:       {stats.unchanged_cells:>10,}\n")
        self.stats_text.insert(tk.END, f"   • Số sheets:            {stats.sheets_processed:>10}\n\n")
        
        # Calculate percentages
        if stats.string_cells > 0:
            unicode_pct = (stats.already_unicode / stats.string_cells) * 100
            convert_pct = (stats.converted_cells / stats.string_cells) * 100
            
            self.stats_text.insert(tk.END, f"📈 Tỷ lệ:\n")
            self.stats_text.insert(tk.END, f"   • Unicode chuẩn:        {unicode_pct:>9.2f}%\n")
            self.stats_text.insert(tk.END, f"   • Cần convert:          {convert_pct:>9.2f}%\n\n")
        
        # Efficiency
        if self.skip_unicode.get() and stats.already_unicode > 0:
            self.stats_text.insert(tk.END, f"⚡ Hiệu quả:\n")
            self.stats_text.insert(tk.END, f"   Đã bỏ qua {stats.already_unicode:,} cells Unicode chuẩn\n")
            self.stats_text.insert(tk.END, f"   → Tiết kiệm thời gian xử lý!\n\n")
        
        self.stats_text.insert(tk.END, "="*60 + "\n")
        self.stats_text.insert(tk.END, f"✅ Hoàn thành lúc: {datetime.now().strftime('%H:%M:%S')}\n")
    
    def export_log(self):
        """Xuất log ra file"""
        if not self.conversion_stats:
            messagebox.showwarning("Cảnh báo", "Chưa có dữ liệu log để xuất!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Xuất log",
            defaultextension=".txt",
            initialfile=f"conversion_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                export_conversion_log(self.conversion_stats, filename)
                messagebox.showinfo("Thành công", f"Đã xuất log:\n{filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất log:\n{e}")
    
    def log_message(self, message):
        """Thêm message vào log"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
    
    def on_skip_unicode_changed(self):
        """Handle skip unicode checkbox change"""
        # Enable/disable review button based on skip_unicode
        if self.skip_unicode.get() and self.preview_data:
            self.btn_review.config(state=tk.NORMAL)
        else:
            self.btn_review.config(state=tk.DISABLED)
    
    def on_highlight_changed(self):
        """Handle highlight checkbox change"""
        if self.highlight_converted.get():
            if not self.license_info.get("registered"):
                messagebox.showwarning(
                    "Tính năng Pro",
                    "Đánh dấu màu cells là tính năng Pro.\n\n"
                    "Vui lòng đăng ký bản quyền để sử dụng.\n"
                    "Nhấn nút '🔑 Bản Quyền' để đăng ký."
                )
                self.highlight_converted.set(False)
    
    def update_color_preview(self, *args):
        """Update color preview button"""
        try:
            self.color_preview_btn.config(bg=self.highlight_color.get())
        except:
            pass
    
    def show_color_preview(self):
        """Show color picker or preview"""
        messagebox.showinfo(
            "Màu đánh dấu",
            f"Màu hiện tại: {self.highlight_color.get()}\n\n"
            f"Chọn màu từ dropdown menu."
        )
    
    def show_review_dialog(self):
        """Show dialog to review and select which Unicode cells to skip"""
        if not self.preview_data:
            messagebox.showwarning("Cảnh báo", "Vui lòng Preview trước!")
            return
        
        # Import helper function
        from convert_excel_tcvn3 import is_likely_non_text_content
        
        # Filter Unicode cells
        all_unicode_cells = [cell for cell in self.preview_data if cell.was_unicode]
        
        # Filter out non-text content (số, dấu, date...)
        unicode_cells = [
            cell for cell in all_unicode_cells 
            if not is_likely_non_text_content(cell.original)
        ]
        
        filtered_count = len(all_unicode_cells) - len(unicode_cells)
        
        if not unicode_cells:
            msg = "Không có cells Unicode text nào cần review!"
            if filtered_count > 0:
                msg += f"\n\n(Đã lọc {filtered_count} cells không phải text: số, dấu, date...)"
            messagebox.showinfo("Thông báo", msg)
            return
        
        # Create review dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("🔍 Review Unicode Cells")
        dialog.geometry("900x650")
        dialog.configure(bg=ModernTheme.BG_DARK)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header
        header_frame = ttk.Frame(dialog, style="Modern.TFrame", padding=15)
        header_frame.pack(fill=tk.X)
        
        title_text = f"🔍 Review {len(unicode_cells)} Unicode Text Cells"
        if filtered_count > 0:
            title_text += f" (lọc {filtered_count} không phải text)"
        
        ttk.Label(
            header_frame,
            text=title_text,
            style="Header.TLabel",
            font=("Segoe UI", 14, "bold")
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            header_frame,
            text="Bỏ tick = Vẫn convert | Giữ tick = Bỏ qua",
            background=ModernTheme.BG_DARK,
            foreground=ModernTheme.TEXT_MUTED,
            font=("Segoe UI", 9)
        ).pack(side=tk.RIGHT)
        
        # Toolbar Row 1 - Basic actions
        toolbar1 = ttk.Frame(dialog, style="Modern.TFrame", padding=(15, 0, 15, 5))
        toolbar1.pack(fill=tk.X)
        
        ttk.Button(
            toolbar1,
            text="✅ Chọn Tất Cả",
            command=lambda: self.select_all_review(tree, True),
            style="Secondary.TButton"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            toolbar1,
            text="❌ Bỏ Chọn Tất Cả",
            command=lambda: self.select_all_review(tree, False),
            style="Secondary.TButton"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            toolbar1,
            text="🔄 Đảo Ngược",
            command=lambda: self.invert_selection_review(tree),
            style="Secondary.TButton"
        ).pack(side=tk.LEFT)
        
        # Toolbar Row 2 - Advanced selection
        toolbar2 = ttk.Frame(dialog, style="Modern.TFrame", padding=(15, 0, 15, 10))
        toolbar2.pack(fill=tk.X)
        
        # Quick filter input
        ttk.Label(
            toolbar2,
            text="🔍 Chọn nhanh:",
            background=ModernTheme.BG_DARK,
            foreground=ModernTheme.TEXT_PRIMARY,
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        filter_var = tk.StringVar()
        filter_entry = ttk.Entry(
            toolbar2,
            textvariable=filter_var,
            width=20,
            style="Modern.TEntry",
            font=("Segoe UI", 9)
        )
        filter_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            toolbar2,
            text="✓ Chọn có chứa",
            command=lambda: self.select_by_text(tree, filter_var.get(), True),
            style="Secondary.TButton"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            toolbar2,
            text="✗ Bỏ chọn có chứa",
            command=lambda: self.select_by_text(tree, filter_var.get(), False),
            style="Secondary.TButton"
        ).pack(side=tk.LEFT)
        
        # Treeview frame
        tree_frame = ttk.Frame(dialog, style="Modern.TFrame", padding=(15, 0, 15, 15))
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview with scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("Skip", "Sheet", "Row", "Col", "Text")
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll.set,
            height=20
        )
        tree_scroll.config(command=tree.yview)
        
        # Configure columns
        tree.heading("Skip", text="Bỏ Qua")
        tree.heading("Sheet", text="Sheet")
        tree.heading("Row", text="Row")
        tree.heading("Col", text="Column")
        tree.heading("Text", text="Text")
        
        tree.column("Skip", width=80, anchor="center")
        tree.column("Sheet", width=120)
        tree.column("Row", width=60, anchor="center")
        tree.column("Col", width=100)
        tree.column("Text", width=400)
        
        # Style treeview
        style = ttk.Style()
        style.configure("Treeview",
            background=ModernTheme.BG_DARKER,
            foreground=ModernTheme.TEXT_PRIMARY,
            fieldbackground=ModernTheme.BG_DARKER,
            borderwidth=0
        )
        style.configure("Treeview.Heading",
            background=ModernTheme.BG_LIGHT,
            foreground=ModernTheme.ACCENT_PRIMARY,
            borderwidth=1
        )
        style.map("Treeview",
            background=[('selected', ModernTheme.SELECTION)],
            foreground=[('selected', ModernTheme.TEXT_PRIMARY)]
        )
        
        # Insert data
        for i, cell in enumerate(unicode_cells):
            cell_id = f"{cell.sheet}_{cell.row}_{cell.col}"
            skip_status = "✅ Bỏ qua" if self.skip_selection.get(cell_id, True) else "❌ Convert"
            
            tree.insert("", tk.END, iid=str(i), values=(
                skip_status,
                cell.sheet,
                cell.row,
                cell.col_name,
                cell.original[:50] + "..." if len(cell.original) > 50 else cell.original
            ), tags=(cell_id,))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        def toggle_skip(event):
            item = tree.selection()[0] if tree.selection() else None
            if item:
                cell_id = tree.item(item)["tags"][0]
                current = self.skip_selection.get(cell_id, True)
                self.skip_selection[cell_id] = not current
                
                # Update display
                new_status = "✅ Bỏ qua" if not current else "❌ Convert"
                values = list(tree.item(item)["values"])
                values[0] = new_status
                tree.item(item, values=values)
        
        tree.bind("<Double-1>", toggle_skip)
        tree.bind("<Return>", toggle_skip)
        tree.bind("<space>", toggle_skip)  # Spacebar cũng toggle
        
        # Right-click context menu
        context_menu = tk.Menu(tree, tearoff=0, bg=ModernTheme.BG_LIGHT, fg=ModernTheme.TEXT_PRIMARY)
        context_menu.add_command(label="✅ Chọn (Bỏ qua)", command=lambda: self.toggle_selected_items(tree, True))
        context_menu.add_command(label="❌ Bỏ chọn (Convert)", command=lambda: self.toggle_selected_items(tree, False))
        context_menu.add_separator()
        context_menu.add_command(label=" Chọn tất cả giống text này", command=lambda: self.select_by_current_text(tree, True))
        context_menu.add_command(label=" Bỏ chọn tất cả giống text này", command=lambda: self.select_by_current_text(tree, False))
        
        def show_context_menu(event):
            # Check item under cursor
            item = tree.identify_row(event.y)
            if item:
                # Only change selection if right-clicked item is NOT already selected
                if item not in tree.selection():
                    tree.selection_set(item)
                # Show menu
                context_menu.post(event.x_root, event.y_root)
        
        tree.bind("<Button-3>", show_context_menu)  # Right-click
        
        # Shift+Click for range selection
        last_clicked_item = [None]  # Use list to allow modification in nested function
        
        def on_tree_click(event):
            item = tree.identify_row(event.y)
            if not item:
                return
            
            # Check if Shift is pressed
            if event.state & 0x0001:  # Shift key
                if last_clicked_item[0] and last_clicked_item[0] in tree.get_children():
                    # Select range
                    all_items = tree.get_children()
                    start_idx = all_items.index(last_clicked_item[0])
                    end_idx = all_items.index(item)
                    
                    # Ensure start < end
                    if start_idx > end_idx:
                        start_idx, end_idx = end_idx, start_idx
                    
                    # Select range
                    for i in range(start_idx, end_idx + 1):
                        tree.selection_add(all_items[i])
                else:
                    # No previous selection, just select current
                    tree.selection_set(item)
                    last_clicked_item[0] = item
            else:
                # Normal click, remember this item
                last_clicked_item[0] = item
        
        tree.bind("<Button-1>", on_tree_click, add="+")  # Add to existing bindings
        
        # Bottom buttons
        bottom_frame = ttk.Frame(dialog, style="Modern.TFrame", padding=15)
        bottom_frame.pack(fill=tk.X)
        
        info_label = ttk.Label(
            bottom_frame,
            text="💡 Tips: Shift+Click = chọn dãy | Right-click = menu hàng loạt | Double-click/Enter/Space = toggle 1 ô",
            background=ModernTheme.BG_DARK,
            foreground=ModernTheme.TEXT_MUTED,
            font=("Segoe UI", 8)
        )
        info_label.pack(side=tk.LEFT)
        
        ttk.Button(
            bottom_frame,
            text="✅ OK - Áp Dụng",
            command=dialog.destroy,
            style="Success.TButton"
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(
            bottom_frame,
            text="❌ Hủy",
            command=lambda: self.cancel_review(dialog),
            style="Secondary.TButton"
        ).pack(side=tk.RIGHT)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
    
    def select_all_review(self, tree, select: bool):
        """Select or deselect all items in review"""
        for item in tree.get_children():
            cell_id = tree.item(item)["tags"][0]
            self.skip_selection[cell_id] = select
            
            status = "✅ Bỏ qua" if select else "❌ Convert"
            values = list(tree.item(item)["values"])
            values[0] = status
            tree.item(item, values=values)
    
    def invert_selection_review(self, tree):
        """Invert selection in review"""
        for item in tree.get_children():
            cell_id = tree.item(item)["tags"][0]
            current = self.skip_selection.get(cell_id, True)
            self.skip_selection[cell_id] = not current
            
            status = "✅ Bỏ qua" if not current else "❌ Convert"
            values = list(tree.item(item)["values"])
            values[0] = status
            tree.item(item, values=values)
    
    def select_by_text(self, tree, search_text: str, select: bool):
        """Select/deselect items containing search text"""
        if not search_text.strip():
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập text cần tìm")
            return
        
        search_text = search_text.strip().lower()
        count = 0
        
        for item in tree.get_children():
            values = tree.item(item)["values"]
            cell_text = str(values[4]).lower()  # Text column
            
            if search_text in cell_text:
                cell_id = tree.item(item)["tags"][0]
                self.skip_selection[cell_id] = select
                
                status = "✅ Bỏ qua" if select else "❌ Convert"
                values = list(values)
                values[0] = status
                tree.item(item, values=values)
                count += 1
        
        if count > 0:
            messagebox.showinfo("Thành công", f"Đã {'chọn' if select else 'bỏ chọn'} {count} ô chứa '{search_text}'")
        else:
            messagebox.showinfo("Thông báo", f"Không tìm thấy ô nào chứa '{search_text}'")
    
    def toggle_selected_items(self, tree, select: bool):
        """Toggle currently selected tree items"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một ô")
            return
        
        for item in selection:
            cell_id = tree.item(item)["tags"][0]
            self.skip_selection[cell_id] = select
            
            status = "✅ Bỏ qua" if select else "❌ Convert"
            values = list(tree.item(item)["values"])
            values[0] = status
            tree.item(item, values=values)
    
    def select_by_current_text(self, tree, select: bool = True):
        """Select/deselect all items with same text as current"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một ô để lấy text mẫu")
            return
        
        current_item = selection[0]
        current_text = str(tree.item(current_item)["values"][4]).strip()
        
        count = 0
        for item in tree.get_children():
            values = tree.item(item)["values"]
            if str(values[4]).strip() == current_text:
                cell_id = tree.item(item)["tags"][0]
                self.skip_selection[cell_id] = select
                
                status = "✅ Bỏ qua" if select else "❌ Convert"
                values = list(values)
                values[0] = status
                tree.item(item, values=values)
                count += 1
        
        action = "chọn" if select else "bỏ chọn"
        messagebox.showinfo("Thành công", f"Đã {action} {count} ô giống text '{current_text}'")
    
    def cancel_review(self, dialog):
        """Cancel review and reset selections"""
        if messagebox.askyesno("Xác nhận", "Hủy bỏ các thay đổi?"):
            self.skip_selection.clear()
            dialog.destroy()
    
    def show_license_dialog(self):
        """Show license registration dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔑 Quản Lý Bản Quyền")
        dialog.geometry("650x750")  # Tăng chiều cao từ 500 → 650
        dialog.configure(bg=ModernTheme.BG_DARK)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header
        header_frame = ttk.Frame(dialog, style="Modern.TFrame", padding=20)
        header_frame.pack(fill=tk.X)
        
        ttk.Label(
            header_frame,
            text="🔑 Thông Tin Bản Quyền",
            style="Header.TLabel",
            font=("Segoe UI", 14, "bold")
        ).pack()
        
        # Current license info
        info_frame = ttk.LabelFrame(
            dialog,
            text="  📋  Thông Tin Hiện Tại  ",
            padding=20,
            style="Modern.TLabelframe"
        )
        info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        license_type = self.license_info.get("type", "Free")
        is_registered = self.license_info.get("registered", False)
        
        ttk.Label(
            info_frame,
            text=f"Loại: {license_type} {'✅' if is_registered else '❌'}",
            style="Modern.TLabel",
            font=("Segoe UI", 10, "bold"),
            foreground=ModernTheme.ACCENT_SUCCESS if is_registered else ModernTheme.ACCENT_WARNING
        ).pack(anchor=tk.W, pady=2)
        
        if is_registered:
            ttk.Label(
                info_frame,
                text=f"Người dùng: {self.license_info.get('user', 'N/A')}",
                style="Modern.TLabel"
            ).pack(anchor=tk.W, pady=2)
            
            ttk.Label(
                info_frame,
                text=f"Email: {self.license_info.get('email', 'N/A')}",
                style="Modern.TLabel"
            ).pack(anchor=tk.W, pady=2)
            
            if self.license_info.get('company'):
                ttk.Label(
                    info_frame,
                    text=f"Công ty: {self.license_info.get('company')}",
                    style="Modern.TLabel"
                ).pack(anchor=tk.W, pady=2)
        
        # Registration form
        form_frame = ttk.LabelFrame(
            dialog,
            text="  📝  Đăng Ký Bản Quyền  ",
            padding=20,
            style="Modern.TLabelframe"
        )
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Name
        ttk.Label(form_frame, text="Họ tên:", style="Modern.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar(value=self.license_info.get("user", ""))
        ttk.Entry(form_frame, textvariable=name_var, width=40, style="Modern.TEntry").grid(row=0, column=1, pady=5, sticky=tk.EW)
        
        # Email
        ttk.Label(form_frame, text="Email:", style="Modern.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        email_var = tk.StringVar(value=self.license_info.get("email", ""))
        ttk.Entry(form_frame, textvariable=email_var, width=40, style="Modern.TEntry").grid(row=1, column=1, pady=5, sticky=tk.EW)
        
        # Company
        ttk.Label(form_frame, text="Công ty:", style="Modern.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5)
        company_var = tk.StringVar(value=self.license_info.get("company", ""))
        ttk.Entry(form_frame, textvariable=company_var, width=40, style="Modern.TEntry").grid(row=2, column=1, pady=5, sticky=tk.EW)
        
        # License key
        ttk.Label(form_frame, text="License Key:", style="Modern.TLabel").grid(row=3, column=0, sticky=tk.W, pady=5)
        key_var = tk.StringVar()
        key_entry = ttk.Entry(form_frame, textvariable=key_var, width=40, style="Modern.TEntry", show="*")
        key_entry.grid(row=3, column=1, pady=5, sticky=tk.EW)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Info text - Tăng height để dễ đọc hơn
        info_text = scrolledtext.ScrolledText(
            form_frame,
            height=10,  # Tăng từ 6 → 10 dòng
            wrap=tk.WORD,
            bg=ModernTheme.BG_DARKER,
            fg=ModernTheme.TEXT_SECONDARY,
            font=("Segoe UI", 9),
            relief="flat",
            borderwidth=0
        )
        info_text.grid(row=4, column=0, columnspan=2, pady=(15, 0), sticky=tk.EW)
        info_text.insert(tk.END, 
            "💡 Cách lấy License Key:\n\n"
            "1. Nhập Email của bạn\n"
            "2. Nhấn nút 'Generate Trial Key' bên dưới\n"
            "3. Copy License Key hiển thị\n"
            "4. Paste vào ô License Key\n"
            "5. Nhấn 'Kích Hoạt'\n\n"
            "🎁 Tính năng Pro được mở khóa:\n\n"
            "• 🎨 Đánh dấu màu cells đã convert\n"
            "• 🔍 Review & Cherry-pick đầy đủ\n"
            "• 📊 Xuất Excel với highlight\n"
            "• 🚀 Hỗ trợ ưu tiên\n"
            "• ⚡ Không giới hạn tính năng\n"
        )
        info_text.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = ttk.Frame(dialog, style="Modern.TFrame", padding=(20, 0, 20, 20))
        button_frame.pack(fill=tk.X)
        
        def activate_license():
            name = name_var.get().strip()
            email = email_var.get().strip()
            company = company_var.get().strip()
            key = key_var.get().strip()
            
            if not name or not email:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ Họ tên và Email!")
                return
            
            if not key:
                messagebox.showerror("Lỗi", "Vui lòng nhập License Key!")
                return
            
            # Verify key
            if self.verify_license_key(key, email):
                license_data = {
                    "type": "Pro",
                    "user": name,
                    "email": email,
                    "company": company,
                    "license_key": key,
                    "features": ["basic_conversion", "preview", "highlight", "advanced_export"],
                    "registered": True
                }
                self.save_license(license_data)
                self.display_license_info()
                
                messagebox.showinfo(
                    "Thành công",
                    f"🎉 Kích hoạt thành công!\n\n"
                    f"Chào mừng {name}!\n"
                    f"Bạn đã kích hoạt TCVN3 Converter Pro.\n\n"
                    f"Tất cả tính năng Pro đã được mở khóa."
                )
                dialog.destroy()
            else:
                messagebox.showerror(
                    "Lỗi",
                    "License Key không hợp lệ!\n\n"
                    "Vui lòng kiểm tra lại hoặc liên hệ support."
                )
        
        def generate_trial_key():
            """Generate trial key for demo"""
            email = email_var.get().strip()
            if not email:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập Email trước!")
                return
            
            secret = "NGUYEN_MINH_KHA"
            trial_key = hashlib.sha256(f"{email}{secret}".encode()).hexdigest()[:16].upper()
            
            # Auto fill key vào ô License Key
            key_var.set(trial_key)
            key_entry.config(show="")  # Hiển thị key
            
            messagebox.showinfo(
                "✅ Trial Key Generated",
                f"🔑 Trial Key cho:\n{email}\n\n"
                f"Key: {trial_key}\n\n"
                f"✅ Đã tự động điền vào ô License Key!\n"
                f"Nhấn 'Kích Hoạt' để hoàn tất."
            )
        
        ttk.Button(
            button_frame,
            text="🔑 Generate Trial Key",
            command=generate_trial_key,
            style="Secondary.TButton"
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            button_frame,
            text="❌ Đóng",
            command=dialog.destroy,
            style="Secondary.TButton"
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(
            button_frame,
            text="✅ Kích Hoạt",
            command=activate_license,
            style="Success.TButton"
        ).pack(side=tk.RIGHT)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")


def main():
    root = tk.Tk()
    app = ConverterGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
