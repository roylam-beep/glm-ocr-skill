"""
main.py — GLM-OCR Skill 入口腳本

掃描本地資料夾中的所有圖片/PDF，透過 Z.ai GLM-OCR API 進行 OCR 辨識，
輸出結構化 Markdown 與 JSON 結果。

使用方式:
    python scripts/main.py                     # 使用 .env 中的預設目錄
    python scripts/main.py --dir ./my_scans    # 指定掃描目錄
    python scripts/main.py --dir ./scans --output ./results  # 指定輸出目錄
"""

import argparse
import os
import sys
from pathlib import Path

# 修正 Windows CP950 終端編碼問題
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 確保可以 import scripts/ 下的模組
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

from scripts.file_utils import encode_file_to_data_uri, find_supported_files, validate_file
from scripts.ocr_processor import GLMOCRProcessor
from scripts.output_formatter import (
    ensure_output_dir,
    save_combined_markdown,
    save_single_json,
    save_single_markdown,
    save_summary_json,
)


def load_api_key() -> str:
    """從環境變數載入 API Key。"""
    load_dotenv()
    api_key = os.getenv("ZAI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        raise RuntimeError(
            "未設定 ZAI_API_KEY。請在 .env 檔案中設定，或複製 .env.example 為 .env 後填入 API Key。"
        )
    return api_key


def main():
    parser = argparse.ArgumentParser(
        description="GLM-OCR Skill — 香港會計單據 OCR 掃描工具"
    )
    parser.add_argument(
        "--dir",
        default=os.getenv("DEFAULT_SCAN_DIR", "./scans"),
        help="要掃描的目錄 (預設: ./scans)",
    )
    parser.add_argument(
        "--output",
        default=os.getenv("DEFAULT_OUTPUT_DIR", "./output"),
        help="輸出目錄 (預設: ./output)",
    )
    parser.add_argument(
        "--no-combined",
        action="store_true",
        help="不產生合併的 Markdown 檔案",
    )
    parser.add_argument(
        "--no-json",
        action="store_true",
        help="不產生逐檔 JSON 檔案",
    )
    args = parser.parse_args()

    # 載入設定
    load_dotenv()
    api_key = load_api_key()
    scan_dir = args.dir
    output_dir = args.output

    # 初始化
    processor = GLMOCRProcessor(api_key=api_key)
    out_path = ensure_output_dir(output_dir)

    # 掃描檔案
    print(f"[SCAN] 掃描目錄: {os.path.abspath(scan_dir)}")
    files = find_supported_files(scan_dir)

    if not files:
        print("[WARN] 未找到任何支援的檔案（jpg, jpeg, png, pdf, webp）。")
        return

    print(f"[FILE] 找到 {len(files)} 個檔案，開始 OCR 處理...\n")

    results: list[dict] = []
    success_count = 0
    fail_count = 0

    for i, file_path in enumerate(files, 1):
        filename = file_path.name
        print(f"[{i}/{len(files)}] {filename} ...")

        # 驗證檔案
        error = validate_file(file_path)
        if error:
            print(f"  [ERROR] 跳過: {error}")
            results.append({
                "filename": filename,
                "status": "skipped",
                "error": error,
            })
            fail_count += 1
            continue

        # 編碼並呼叫 API
        try:
            data_uri = encode_file_to_data_uri(file_path)
            response = processor.process_file(data_uri)
            markdown_text = processor.extract_markdown(response)
            metadata = processor.extract_metadata(response)

            # 儲存結果
            if not args.no_json:
                json_path = save_single_json(out_path, filename, response)
                print(f"  [FILE] JSON: {json_path.name}")

            md_path = save_single_markdown(out_path, filename, markdown_text)
            print(f"  [MD] Markdown: {md_path.name}")
            print(f"  [INFO] 頁數: {metadata['pages']}, "
                  f"Tokens: {metadata['tokens_total']} "
                  f"(入:{metadata['tokens_input']} / 出:{metadata['tokens_output']})")

            results.append({
                "filename": filename,
                "status": "success",
                "pages": metadata["pages"],
                "tokens_total": metadata["tokens_total"],
                "markdown": markdown_text[:500],  # 摘要前 500 字
            })
            success_count += 1

        except Exception as e:
            print(f"  [ERROR] 失敗: {e}")
            results.append({
                "filename": filename,
                "status": "failed",
                "error": str(e),
            })
            fail_count += 1

        print()

    # 輸出彙總
    print("=" * 50)
    print(f"[OK] 完成: {success_count} 成功 / [ERROR] {fail_count} 失敗 / 共 {len(files)} 個檔案")

    # 儲存彙總
    summary_json = save_summary_json(out_path, results)
    print(f"[SUMMARY] 彙總 JSON: {summary_json}")

    if not args.no_combined:
        combined_md = save_combined_markdown(out_path, results)
        print(f"[COMBINED] 合併 Markdown: {combined_md}")

    print(f"\n所有輸出檔案位於: {out_path.resolve()}")


if __name__ == "__main__":
    main()
