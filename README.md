# GLM OCR Skill

![GitHub Topics](https://img.shields.io/badge/topics-ocr%20%7C%20glm%20%7C%20zai%20%7C%20invoice%20%7C%20receipt%20%7C%20accounting%20%7C%20document--parsing%20%7C%20vision--llm-blue)

A CLI tool that scans local folders of receipts, invoices, and documents using Z.ai's GLM-OCR model. Outputs structured Markdown + JSON with layout analysis. Zero-config, single-command: `python scripts/main.py`.

## Quick Start

### 1. Requirements

- Python 3.10+
- pip

### 2. Install

```bash
git clone <repo-url>
cd hk-glm-ocr-skill
pip install -r requirements.txt
```

### 3. Set API Key

```bash
cp .env.example .env
```

Edit `.env` and paste your Z.ai API Key:

```
ZAI_API_KEY=your_api_key_here
```

> Get your key at <a href="https://open.bigmodel.cn/" target="_blank" rel="noopener noreferrer">Z.ai Open Platform</a>.

### 4. Place Documents

Drop your images or PDFs into the `scans/` folder:

```
scans/
├── invoice_001.jpg
├── receipt_may.pdf
└── bank_statement.png
```

### 5. Run

```bash
python scripts/main.py
```

## Advanced Usage

```bash
# Custom scan directory
python scripts/main.py --dir /path/to/documents

# Custom output directory
python scripts/main.py --dir ./scans --output ./results

# Markdown only (skip per-file JSON)
python scripts/main.py --no-json

# Skip combined output
python scripts/main.py --no-combined
```

## Supported Formats

| Format | Extensions | Max Size |
|--------|-----------|----------|
| JPEG | `.jpg` `.jpeg` | 10 MB |
| PNG | `.png` | 10 MB |
| WebP | `.webp` | 10 MB (auto-converted to PNG) |
| PDF | `.pdf` | 50 MB |

## Output

After scanning, the `output/` directory contains:

| File | Description |
|------|-------------|
| `{name}_ocr.md` | Per-file OCR result in Markdown |
| `{name}_ocr.json` | Full API response with layout analysis |
| `combined_ocr.md` | All results merged into a single Markdown report |
| `summary.json` | Processing summary (success/fail, pages, token usage) |

## Project Structure

```
hk-glm-ocr-skill/
├── .env.example            # API key template
├── .gitignore
├── SKILL.md                # Qoder Skill definition
├── README.md
├── requirements.txt        # Python dependencies
├── scans/                  # Input documents (gitignored)
├── output/                 # OCR results (gitignored)
└── scripts/
    ├── main.py             # Entry point
    ├── file_utils.py       # File scanning & format conversion
    ├── ocr_processor.py    # Z.ai GLM-OCR API wrapper
    └── output_formatter.py # Output formatting
```

## FAQ

**Q: "ZAI_API_KEY not set" error?**

Make sure `.env` exists and `ZAI_API_KEY` is correctly configured.

**Q: 401 error?**

Your API key may be expired or invalid. Generate a new one at <a href="https://open.bigmodel.cn/" target="_blank" rel="noopener noreferrer">Z.ai Open Platform</a>.

**Q: 429 error?**

Rate limit hit. The tool will automatically wait and retry (up to 3 times). If it persists, split your files into smaller batches.

**Q: Does it scan subdirectories?**

No. Only files directly inside `scans/` are processed. Subdirectory contents are ignored.

---

MIT License

Copyright (c) 2026 <a href="https://geniushub.cc" target="_blank" rel="noopener noreferrer">geniushub.cc</a>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

<p align="center">Built by <a href="https://geniushub.cc" target="_blank" rel="noopener noreferrer">geniushub.cc</a></p>
