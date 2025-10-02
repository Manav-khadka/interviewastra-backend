# LaTeX Setup Guide for PDF Generation

## Overview
The resume PDF generation feature requires a LaTeX distribution to be installed on your system. Without it, the application will save the `.tex` file that you can compile manually or online.

## Installation Options

### Option 1: Install LaTeX Distribution (Recommended for Production)

#### Windows
1. **MiKTeX (Recommended for Windows)**
   - Download: https://miktex.org/download
   - Install the basic system
   - MiKTeX will automatically install missing packages on first use
   - Add to PATH (installer usually does this automatically)

2. **TeX Live**
   - Download: https://www.tug.org/texlive/
   - Larger download (~4GB) but more complete
   - Includes all packages

#### macOS
```bash
# Using Homebrew
brew install --cask mactex

# Or BasicTeX (smaller, faster)
brew install --cask basictex
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install texlive-latex-extra texlive-fonts-recommended
```

#### Linux (Fedora)
```bash
sudo dnf install texlive-scheme-basic texlive-collection-latexextra
```

### Option 2: Verify Installation
After installation, verify pdflatex is available:
```bash
pdflatex --version
```

You should see output like:
```
pdfLaTeX 3.141592653-2.6-1.40.XX (TeX Live 2024)
```

### Option 3: Use Online LaTeX Compilation (Development/Testing)

If you don't want to install LaTeX locally, you can:

1. **Get the .tex file** from the API response when PDF generation fails
2. **Use Overleaf**: https://www.overleaf.com/
   - Upload the `.tex` file
   - Compile online
   - Download the PDF

3. **Use LaTeX.Online API** (Alternative Implementation)
   - Service: https://latexonline.cc/
   - Can be integrated into the backend for serverless PDF generation

## Required LaTeX Packages

The Jake's Resume Template requires these packages (auto-installed by MiKTeX):
- `latexsym`
- `fullpage`
- `titlesec`
- `marvosym`
- `color`
- `verbatim`
- `enumitem`
- `hyperref`
- `fancyhdr`
- `tabularx`
- `fontawesome5`
- `multicol`

## Troubleshooting

### Issue: "pdflatex: command not found"
**Solution**: LaTeX is not installed or not in PATH
- Reinstall and ensure "Add to PATH" is checked
- Or manually add to PATH:
  - Windows: Add `C:\Program Files\MiKTeX\miktex\bin\x64\` to PATH
  - macOS: Add `/Library/TeX/texbin` to PATH

### Issue: Missing packages during compilation
**Solution**: 
- MiKTeX: Will prompt to auto-install (allow it)
- TeX Live: Install manually with `tlmgr install <package-name>`

### Issue: Compilation errors
**Solution**: 
- Check the saved `.tex` file for syntax errors
- Verify all template variables are properly replaced
- Look at the `.log` file for detailed error messages

## Testing PDF Generation

1. **Create a resume** using the API
2. **Generate PDF** with POST `/resumes/{resume_id}/generate-pdf`
3. **Check response**:
   - Success: `{ "status": "success", "pdf_url": "..." }`
   - Failure: `{ "status": "error", "latex_url": "...", "message": "..." }`

## Development Without LaTeX

For development without LaTeX installed:
1. API will save `.tex` files to `static/resumes/`
2. Access via: `http://localhost:8000/static/resumes/{resume_id}.tex`
3. Copy content to Overleaf for manual compilation
4. Or use the LaTeX.Online API integration (see below)

## Future: LaTeX.Online API Integration

To avoid local LaTeX installation, consider integrating:
```python
import requests

def compile_latex_online(latex_content: str) -> bytes:
    response = requests.post(
        "https://latexonline.cc/compile",
        files={"file": ("resume.tex", latex_content)}
    )
    return response.content  # PDF bytes
```

This would make the service serverless and avoid installation requirements.
