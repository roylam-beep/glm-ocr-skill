# HK GLM OCR Skill

使用 Z.ai 的 GLM-OCR 模型，掃描本地資料夾中的單據（圖片 / PDF / WebP），輸出結構化的 OCR 辨識結果。專為香港會計服務場景設計，支援發票、收據、銀行單據等文件的文字辨識與版面分析。

## 快速開始

### 1. 環境需求

- Python 3.10+
- pip

### 2. 安裝

```bash
git clone <repo-url>
cd hk-glm-ocr-skill
pip install -r requirements.txt
```

### 3. 設定 API Key

```bash
cp .env.example .env
```

編輯 `.env`，填入你的 Z.ai API Key：

```
ZAI_API_KEY=你的_API_Key
```

> 在 [Z.ai Open Platform](https://open.bigmodel.cn/) 註冊並建立 API Key。

### 4. 放入單據

將要掃描的圖片或 PDF 檔案放入 `scans/` 目錄：

```
scans/
├── invoice_001.jpg
├── receipt_may.pdf
└── bank_statement.png
```

### 5. 執行掃描

```bash
python scripts/main.py
```

## 進階用法

```bash
# 指定掃描目錄
python scripts/main.py --dir /path/to/documents

# 指定輸出目錄
python scripts/main.py --dir ./scans --output ./results

# 只輸出 Markdown（不產 JSON）
python scripts/main.py --no-json

# 不產生合併檔
python scripts/main.py --no-combined
```

## 支援的檔案格式

| 格式 | 附檔名 | 大小上限 |
|------|--------|---------|
| JPEG | `.jpg` `.jpeg` | 10 MB |
| PNG | `.png` | 10 MB |
| WebP | `.webp` | 10 MB（自動轉 PNG） |
| PDF | `.pdf` | 50 MB |

## 輸出說明

掃描完成後，`output/` 目錄會產生以下檔案：

| 檔案 | 說明 |
|------|------|
| `{檔名}_ocr.md` | 單一檔案的 OCR 文字結果（Markdown 格式） |
| `{檔名}_ocr.json` | 單一檔案的完整 API 回應（含版面分析） |
| `combined_ocr.md` | 所有檔案合併的 Markdown 報告 |
| `summary.json` | 處理彙總（成功/失敗、頁數、Token 用量） |

## 專案結構

```
hk-glm-ocr-skill/
├── .env.example            # API Key 範本
├── .gitignore
├── SKILL.md                # Qoder Skill 定義
├── README.md
├── requirements.txt        # Python 依賴
├── scans/                  # 待掃描單據（gitignore）
├── output/                 # OCR 輸出（gitignore）
└── scripts/
    ├── main.py             # 入口腳本
    ├── file_utils.py       # 檔案掃描與格式轉換
    ├── ocr_processor.py    # Z.ai GLM-OCR API 封裝
    └── output_formatter.py # 輸出格式化
```

## 常見問題

**Q: 收到「未設定 ZAI_API_KEY」錯誤？**

確認 `.env` 檔案存在且 `ZAI_API_KEY` 已正確設定。

**Q: 收到 401 錯誤？**

API Key 可能已過期或不正確，請到 [Z.ai Open Platform](https://open.bigmodel.cn/) 重新產生。

**Q: 收到 429 錯誤？**

API 呼叫頻率過高，程式會自動等待並重試（最多 3 次）。如果持續發生，請降低檔案數量分批處理。

**Q: 支援子目錄嗎？**

不支援。`scans/` 下的檔案會直接處理，子目錄內的檔案會被忽略。

---

MIT License

Copyright (c) 2026 [geniushub.cc](https://geniushub.cc)

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

<p align="center"><a href="https://geniushub.cc">geniushub.cc</a> 開發</p>
