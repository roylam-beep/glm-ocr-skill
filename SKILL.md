# GLM OCR Skill

使用 Z.ai 的 GLM-OCR 模型，掃描本地資料夾中的單據（圖片/PDF/WebP），輸出結構化的 OCR 辨識結果。支援發票、收據、銀行單據等文件的文字辨識與版面分析。

## 何時使用此 Skill

- 使用者需要掃描本地資料夾中的會計單據進行 OCR 辨識時
- 使用者提到「OCR」、「掃描單據」、「辨識發票」、「會計文件數位化」等關鍵字
- 使用者需要批量處理圖片/PDF 文件的文字擷取

## 前置需求

1. Python 3.10+
2. 安裝依賴：`pip install -r requirements.txt`
3. 設定 `.env` 檔案中的 `ZAI_API_KEY`

## 使用方式

### 命令列執行

```bash
# 使用預設目錄 (./scans → ./output)
python scripts/main.py

# 指定掃描目錄與輸出目錄
python scripts/main.py --dir /path/to/scans --output /path/to/output

# 僅輸出 Markdown（不產生 JSON）
python scripts/main.py --dir ./scans --no-json

# 不產生合併 Markdown
python scripts/main.py --dir ./scans --no-combined
```

### 在 Qoder 對話中使用

當使用者要求掃描單據時，執行以下步驟：

1. 確認 `.env` 中已設定 `ZAI_API_KEY`
2. 確認掃描目錄存在且內含支援的檔案格式
3. 執行 `python scripts/main.py --dir <掃描目錄> --output <輸出目錄>`
4. 將結果摘要回報給使用者，並提供輸出檔案路徑

## 支援的檔案格式

| 格式 | 附檔名 | 檔案大小上限 |
|------|--------|-------------|
| JPEG | .jpg, .jpeg | 10 MB |
| PNG | .png | 10 MB |
| WebP | .webp | 10 MB（自動轉 PNG） |
| PDF | .pdf | 50 MB |

## 輸出格式

每次掃描會產生以下輸出：

- `{檔名}_ocr.md` — 每個檔案的 OCR 結果（Markdown 格式）
- `{檔名}_ocr.json` — 每個檔案的完整 API 回應（含版面分析）
- `summary.json` — 所有檔案的處理彙總
- `combined_ocr.md` — 所有檔案合併的 Markdown 檔案

## API 參考

- **端點**: `POST https://api.z.ai/api/paas/v4/layout_parsing`
- **模型**: `glm-ocr`
- **認證**: Bearer Token（API Key）
- **文件**: https://docs.z.ai/guides/vlm/glm-ocr

## 錯誤處理

Skill 內建重試機制：
- 速率限制（429）: 自動等待後重試（最多 3 次）
- 連線逾時: 自動重試
- 檔案格式/大小問題: 跳過並記錄錯誤
- 所有失敗項目均記錄於 `summary.json`
