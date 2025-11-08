# 🚀 Hướng Dẫn Đẩy Lên GitHub - TCVN3 Converter Pro

## 📋 Checklist Trước Khi Push

✅ Git repository đã init  
✅ All files đã được commit  
✅ README.md đã hoàn chỉnh  
✅ .gitignore đã được tạo  
✅ LICENSE file đã có  
✅ Documentation đầy đủ  

---

## 🎯 Các Bước Thực Hiện

### Bước 1: Tạo Repository Trên GitHub

1. Đăng nhập GitHub: https://github.com
2. Nhấn nút **"+"** → **"New repository"**
3. Điền thông tin:
   ```
   Repository name: excel-tcvn3-converter
   Description: 🔄 TCVN3 to Unicode Excel Converter Pro - Modern GUI with Dark Theme
   
   ☑️ Public
   ☐ Add README (đã có rồi)
   ☐ Add .gitignore (đã có rồi)
   ☐ Choose a license (đã có rồi)
   ```
4. Nhấn **"Create repository"**

### Bước 2: Kết Nối Local → GitHub

GitHub sẽ hiển thị instructions, làm theo Option 2 (push existing repository):

```bash
# 1. Add remote (thay YOUR_USERNAME bằng username GitHub của bạn)
git remote add origin https://github.com/YOUR_USERNAME/excel-tcvn3-converter.git

# 2. Đổi branch thành main (nếu cần)
git branch -M main

# 3. Push lên GitHub
git push -u origin main
```

**Hoặc dùng SSH** (nếu đã setup SSH key):
```bash
git remote add origin git@github.com:YOUR_USERNAME/excel-tcvn3-converter.git
git push -u origin main
```

---

## 🔐 Setup SSH (Khuyến Nghị)

Nếu chưa setup SSH key:

### Windows (PowerShell)
```powershell
# 1. Tạo SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"
# Nhấn Enter 3 lần (dùng default)

# 2. Copy public key
Get-Content ~\.ssh\id_ed25519.pub | Set-Clipboard

# 3. Add vào GitHub
# Settings → SSH and GPG keys → New SSH key → Paste
```

### Test SSH connection
```bash
ssh -T git@github.com
# Nếu thấy: "Hi username! You've successfully authenticated" → OK!
```

---

## 📦 Sau Khi Push

### 1. Kiểm Tra Repository

Truy cập: `https://github.com/YOUR_USERNAME/excel-tcvn3-converter`

Xem:
- ✅ README.md hiển thị đẹp
- ✅ Files đầy đủ
- ✅ LICENSE đúng
- ✅ Description rõ ràng

### 2. Cập Nhật README Links

Sửa các link trong README.md:

```bash
# Thay YOUR_USERNAME bằng username thật
yourusername → your_real_username
```

Các vị trí cần sửa:
- Badge links
- Download links
- Clone commands
- Author links
- Contact info

Sau đó commit & push:
```bash
git add README.md
git commit -m "docs: Update README with correct GitHub username"
git push
```

### 3. Tạo Topics (Tags)

Trên GitHub repo:
1. Nhấn ⚙️ bên cạnh "About"
2. Add topics:
   ```
   excel
   tcvn3
   unicode
   vietnamese
   converter
   python
   gui
   tkinter
   pandas
   openpyxl
   ```

### 4. Setup Repository Settings

#### A. Description & Website
```
About Section:
Description: 🔄 Excel TCVN3 to Unicode Converter with Modern GUI
Website: (để trống hoặc link docs)
Topics: (đã add ở trên)
```

#### B. Features
```
Settings → General:
☑️ Issues
☑️ Projects (optional)
☐ Wiki (dùng docs/ thay thế)
☑️ Discussions (nếu muốn community)
```

#### C. Branch Protection (Optional)
```
Settings → Branches → Add rule:
Branch name pattern: main
☑️ Require pull request reviews before merging
☑️ Require status checks to pass before merging
```

---

## 🎁 Tạo First Release

### Bước 1: Build Executable

```bash
# Tạo icon
python create_icon.py

# Build exe
python build_exe.py

# Test exe
cd dist
.\TCVN3_Converter_Pro.exe
```

### Bước 2: Đóng Gói Release

Tạo folder:
```
TCVN3_Converter_Pro_v2.1.0/
  ├── TCVN3_Converter_Pro.exe
  ├── tcvn3_map.json
  ├── README_RELEASE.txt
  └── LICENSE.txt
```

Nén thành ZIP:
```powershell
Compress-Archive -Path "TCVN3_Converter_Pro_v2.1.0/*" -DestinationPath "TCVN3_Converter_Pro_v2.1.0_Windows_x64.zip"
```

### Bước 3: Tạo GitHub Release

1. Trên repo → **Releases** → **Create a new release**
2. Điền thông tin:
   ```
   Tag: v2.1.0
   Release title: v2.1.0 - Modern GUI with Pro Features
   
   Description:
   ## 🎉 First Public Release!
   
   ### ✨ Features
   - 🎨 Modern dark theme GUI
   - ⚡ Smart Unicode detection
   - 🔍 Preview & Review
   - 🎨 Highlight converted cells (Pro)
   - 🔑 License management
   
   ### 📥 Download
   - **Windows**: TCVN3_Converter_Pro_v2.1.0_Windows_x64.zip
   - **Source**: Clone or download from main branch
   
   ### 📖 Documentation
   See [README.md](README.md) for full documentation
   
   ---
   
   **Full Changelog**: Initial release
   ```
3. Upload file ZIP
4. Nhấn **Publish release**

---

## 📸 Thêm Screenshots

### Tạo Thư Mục Docs

```bash
mkdir docs
```

### Chụp Screenshots

1. Chạy app: `python gui_converter.py`
2. Chụp các màn hình:
   - `screenshot_main.png` - Giao diện chính
   - `screenshot_preview.png` - Preview tab
   - `screenshot_review.png` - Review dialog
   - `screenshot_stats.png` - Statistics tab
   - `screenshot_license.png` - License dialog

### Add Screenshots Vào Repo

```bash
# Copy screenshots vào docs/
git add docs/*.png
git commit -m "docs: Add screenshots"
git push
```

### Update README

Sửa phần screenshots trong README.md với đường dẫn đúng:
```markdown
![Main Interface](docs/screenshot_main.png)
```

---

## 🌟 Marketing & Visibility

### 1. Social Media Announcement

**Facebook**:
```
🎉 Open Source Release: TCVN3 Converter Pro

Chuyển đổi Excel TCVN3 → Unicode với giao diện hiện đại!

✨ Features:
• Dark theme đẹp mắt
• Preview trước khi convert
• Tự động bỏ qua Unicode
• Highlight cells đã convert

🔗 GitHub: [link]
📥 Download: [link to releases]

#OpenSource #Python #Excel #Vietnamese
```

**LinkedIn**:
```
Excited to share my latest project: TCVN3 Converter Pro!

A modern desktop app for converting Excel files from TCVN3 to Unicode.

Tech stack: Python, tkinter, pandas, openpyxl

Check it out on GitHub: [link]
```

### 2. Reddit Posts

Subreddits:
- r/Python
- r/opensource
- r/learnprogramming
- r/Vietnam (nếu phù hợp)

Template:
```
Title: [Project] TCVN3 to Unicode Excel Converter with Modern GUI

Body:
I've built a tool to convert Excel files from TCVN3 (legacy Vietnamese encoding) to Unicode.

Features:
- Modern dark-themed GUI
- Smart Unicode detection
- Preview functionality
- Batch processing support

Built with Python, tkinter, and pandas. Contributions welcome!

GitHub: [link]
```

### 3. Dev.to / Medium Article

Viết blog post về:
- Why I built this
- Technical challenges
- Architecture decisions
- How to use
- Future roadmap

### 4. Product Hunt (Optional)

Nếu muốn reach broader audience:
- Submit to Product Hunt
- Cần:
  - Logo/Icon
  - Screenshots
  - Description
  - Demo video (optional)

---

## 📊 Analytics & Tracking

### GitHub Insights

Monitor:
- **Traffic** - Visitors, clones
- **Stars** - Popularity
- **Issues** - User feedback
- **Pull Requests** - Contributions

### Setup GitHub Actions (Optional)

Tạo `.github/workflows/build.yml` để auto-build on push:

```yaml
name: Build EXE

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python create_icon.py
      - run: python build_exe.py
      - uses: actions/upload-artifact@v3
        with:
          name: TCVN3_Converter_Pro
          path: dist/
```

---

## 🔄 Workflow Tiếp Theo

### Phát Triển Tính Năng Mới

```bash
# 1. Tạo branch mới
git checkout -b feature/new-feature

# 2. Develop & test
# ... code code code ...

# 3. Commit changes
git add .
git commit -m "feat: Add awesome feature"

# 4. Push branch
git push origin feature/new-feature

# 5. Tạo Pull Request trên GitHub
# 6. Merge vào main
# 7. Delete branch
git checkout main
git pull
git branch -d feature/new-feature
```

### Release Cycle

```bash
# Update version
# - version_info.txt
# - gui_converter.py
# - README.md

# Commit version bump
git add .
git commit -m "chore: Bump version to 2.2.0"

# Tag release
git tag v2.2.0
git push origin v2.2.0

# GitHub Actions auto-build (if setup)
# Or manual: python build_exe.py

# Create Release on GitHub with artifacts
```

---

## ✅ Final Checklist

### Before Public Release

- [ ] Code clean & commented
- [ ] README complete với screenshots
- [ ] LICENSE file có
- [ ] .gitignore đúng (không push secrets)
- [ ] No hardcoded passwords/keys
- [ ] Requirements.txt updated
- [ ] Build instructions tested
- [ ] Executable tested on clean Windows
- [ ] Documentation complete
- [ ] Contact info updated

### After Push

- [ ] Repository public
- [ ] Description & topics set
- [ ] First release created
- [ ] README displays correctly
- [ ] Issues enabled
- [ ] Social media announcement
- [ ] Star your own repo! ⭐

---

## 🎉 You're Done!

Repository của bạn giờ đã:
- ✅ Public trên GitHub
- ✅ Documentation đầy đủ
- ✅ Ready for contributions
- ✅ Professional looking
- ✅ Easy to discover

**Next Steps:**
1. Share với community
2. Respond to issues
3. Accept pull requests
4. Keep building! 🚀

---

## 📞 Need Help?

- GitHub Docs: https://docs.github.com
- Git Tutorial: https://git-scm.com/doc
- Markdown Guide: https://www.markdownguide.org

---

Made with ❤️ - Good luck! 🍀
