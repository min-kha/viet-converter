# Contributing to TCVN3 Converter Pro

First off, thank you for considering contributing to TCVN3 Converter Pro! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## 🤝 How Can I Contribute?

### 1. Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)
- **Sample files** if relevant (without sensitive data)

### 2. Suggesting Features

Feature requests are welcome! Please:

- **Check existing suggestions** first
- **Describe the feature** in detail
- **Explain why** it would be useful
- **Provide examples** of how it would work

### 3. Code Contributions

#### Small Changes
- Fix typos, improve documentation
- Small bug fixes
- → Create Pull Request directly

#### Large Changes
- New features, major refactoring
- → Open an issue first to discuss

## 🛠️ Development Setup

### Prerequisites

```bash
Python 3.8+
Git
```

### Setup Steps

```bash
# 1. Fork and clone
git clone https://github.com/yourusername/excel-tcvn3-converter.git
cd excel-tcvn3-converter

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create feature branch
git checkout -b feature/your-feature-name

# 5. Make changes and test
python gui_converter.py

# 6. Run tests (if available)
# python -m pytest tests/
```

## 📝 Coding Guidelines

### Python Style

Follow [PEP 8](https://pep8.org/) guidelines:

```python
# Good
def convert_tcvn3_to_unicode(text: str) -> str:
    """Convert TCVN3 text to Unicode.
    
    Args:
        text: Input text in TCVN3 encoding
        
    Returns:
        Converted Unicode text
    """
    # Implementation
    pass

# Use type hints
def process_file(file_path: Path) -> ConversionStats:
    pass

# Document functions
def complex_function(param1, param2):
    """
    Brief description.
    
    Detailed explanation if needed.
    """
    pass
```

### Code Structure

```python
# Imports order:
# 1. Standard library
import os
from pathlib import Path

# 2. Third-party
import pandas as pd
from tkinter import ttk

# 3. Local
from convert_excel_tcvn3 import convert_excel
```

### GUI Guidelines

- Use `ModernTheme` color palette
- Follow existing widget styles
- Add tooltips for unclear features
- Test on Windows 10/11
- Ensure responsive layout

### Commit Messages

Use conventional commits:

```bash
feat: Add batch conversion support
fix: Correct Unicode detection for diacritics
docs: Update README with new screenshots
style: Format code with black
refactor: Simplify license verification logic
test: Add unit tests for conversion
chore: Update dependencies
```

## 🚀 Submitting Changes

### Pull Request Process

1. **Update documentation** if needed
2. **Add/update tests** for new features
3. **Ensure code quality**:
   ```bash
   # Format code
   black .
   
   # Check style
   flake8 .
   
   # Type check
   mypy .
   ```
4. **Update CHANGELOG.md**
5. **Create Pull Request** with description:
   - What changed
   - Why it changed
   - How to test
   - Screenshots if UI changed

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How to test these changes

## Screenshots (if applicable)
Add screenshots

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests
- [ ] Tests pass locally
```

## 🐛 Reporting Bugs

### Bug Report Template

```markdown
**Describe the bug**
A clear description of the bug.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Windows 11]
- Python Version: [e.g. 3.10.5]
- App Version: [e.g. 2.1.0]

**Sample Files**
Attach sample files (without sensitive data).

**Additional context**
Any other context about the problem.
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
Clear description of what you want.

**Describe alternatives you've considered**
Other solutions you've considered.

**Additional context**
Any other context or screenshots.

**Would you like to implement this?**
Yes/No - willing to create PR?
```

## 🔍 Code Review Process

1. Maintainer reviews PR within 1-3 days
2. Feedback provided via comments
3. Author addresses feedback
4. Approved PRs merged to main
5. Included in next release

## 🏆 Recognition

Contributors are recognized in:
- README.md Contributors section
- CHANGELOG.md for their changes
- Release notes

## 📚 Additional Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)

## ❓ Questions?

Feel free to:
- Open an issue with `question` label
- Email: support@example.com
- Join discussion in existing issues

---

Thank you for contributing! 🙏
