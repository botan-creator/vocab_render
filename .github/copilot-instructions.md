# Copilot Instructions - vocab_render

## Project Overview
A Flask-based web application that generates customizable English vocabulary test PDFs for language learners. Students input vocabulary pairs (English word + Korean meaning) in a browser form, and the system generates a two-page PDF: a test page with hidden columns and an answer key.

## Architecture

### Core Components
- **app.py** - Flask web server with two routes:
  - `GET /` - Serves the HTML form (index.html)
  - `POST /generate` - Receives form data and returns PDF file
- **pdf_generator.py** - PDF creation utility using `fpdf2` library with Korean font support
- **templates/index.html** - Frontend form with 30 vocabulary input rows (JavaScript-generated)
- **static/style.css** - Minimal styling using flexbox layout
- **NanumGothic.ttf** - Required Korean font file in project root (critical dependency)

### Data Flow
1. User fills 30 English/Korean input fields in browser
2. Selects hide mode (hide Korean or English) and optional student name
3. Form POST to `/generate` submits arrays: `english[]` and `korean[]`
4. `app.py` receives form data, calls `pdf_generator.py`
5. PDF returned as attachment with filename `vocab_test.pdf`

## Key Patterns & Conventions

### PDF Generation (fpdf2)
- Always check `NanumGothic.ttf` exists before calling `pdf.add_font()` - raises `FileNotFoundError` if missing
- Font path constructed with `os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")`
- Three-column table structure: Number (20px) | English | Meaning (split remaining width by 3)
- Two-page PDF: page 1 = test (with blanks), page 2 = answer key (both columns filled)
- Header row uses `fill=True` with `set_fill_color(230, 230, 230)` for gray background
- Cell dimensions: 20px height for header, 9px for data rows

### Form Input Handling (Flask)
- Use `request.form.getlist("english[]")` for array inputs from multiple `<input name="english[]">`
- Zip paired lists: `list(zip(english, korean))` before PDF generation
- Optional fields handled by `request.form.get("key")` returning `None` if missing
- Form submits via POST to `/generate` with multipart form data

### Hide Mode Logic
- `hide_mode='korean'` → show English, blank Korean column (test difficulty: harder)
- `hide_mode='english'` → blank English, show Korean (test difficulty: easier, reverse translation)
- Implemented in pdf_generator.py with conditional cell rendering

## Development & Deployment

### Local Development
```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run Flask development server
python app.py
```
Server runs on `http://localhost:5000` (host 0.0.0.0, port 5000)

### Dependencies
- Flask 2.3.3 - Web framework
- fpdf2 2.5.8 - PDF generation (replaces reportlab in some codepaths)
- gunicorn 21.2.0 - Production WSGI server (see Procfile)

### Production Deployment
- Uses Procfile: `web: gunicorn app:app`
- Set `PORT` environment variable (default 5000 in app.py hardcoded)
- Requires `NanumGothic.ttf` in root directory on production server

## Common Modifications

- **Add new form fields** - Add `<input name="new_field[]">` in index.html, handle with `request.form.getlist()` in app.py
- **Change table column count** - Modify `col_w = (pdf.w - 2 * pdf.l_margin) / 3.0` divisor in pdf_generator.py
- **Adjust PDF formatting** - Edit cell heights (9px data rows, 10px header), font sizes, colors in pdf_generator.py
- **Randomize order** - Currently enabled: `random.shuffle(pairs)` in app.py (remove line to keep input order)

## Important Notes

- **Font dependency is critical**: `NanumGothic.ttf` must exist in project root for Korean text rendering. If missing, copy from `C:\Windows\Fonts\NanumGothic.ttf` (Windows) or install NanumGothic font. pdf_generator.py automatically searches project root first, then system fonts.
- **Korean text rendering**: If Korean characters appear garbled:
  1. Verify `NanumGothic.ttf` exists in project root: `Test-Path NanumGothic.ttf`
  2. If missing, copy from Windows: `Copy-Item "C:\Windows\Fonts\NanumGothic.ttf" -Destination "."`
  3. Restart Flask app
- **No database**: All data is ephemeral; generated PDFs are in-memory (BytesIO)
- **No validation**: Form inputs are not sanitized; trust user data or add validation layer
- **Hardcoded limits**: 30 vocabulary rows in form; adjust loop in index.html JavaScript and PDF margin calculations
- **Active PDF library**: `pdf_generator.py` uses fpdf2; `app.py` legacy reportlab imports removed
