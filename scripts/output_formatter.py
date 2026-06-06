"""
輸出格式化模組：將 OCR 結果輸出為 Markdown / JSON / 合併檔案。
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any


def ensure_output_dir(output_dir: str) -> Path:
    """確保輸出目錄存在並回傳 Path。"""
    p = Path(output_dir)
    p.mkdir(parents=True, exist_ok=True)
    return p


def sanitize_filename(name: str) -> str:
    """清理檔名，移除不安全字元。"""
    safe = name.replace("/", "_").replace("\\", "_")
    safe = safe.replace(":", "_").replace("*", "_")
    safe = safe.replace("?", "_").replace('"', "_")
    safe = safe.replace("<", "_").replace(">", "_").replace("|", "_")
    return safe


def save_single_markdown(
    output_dir: Path,
    original_filename: str,
    markdown_text: str,
) -> Path:
    """將單一檔案的 OCR 結果存為 .md 檔。"""
    stem = Path(original_filename).stem
    safe_stem = sanitize_filename(stem)
    out_path = output_dir / f"{safe_stem}_ocr.md"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# OCR 結果: {original_filename}\n\n")
        f.write(f"產生時間: {datetime.now().isoformat()}\n\n---\n\n")
        f.write(markdown_text)

    return out_path


def save_single_json(
    output_dir: Path,
    original_filename: str,
    response: dict[str, Any],
) -> Path:
    """將單一檔案的完整 API response 存為 .json 檔。"""
    stem = Path(original_filename).stem
    safe_stem = sanitize_filename(stem)
    out_path = output_dir / f"{safe_stem}_ocr.json"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(response, f, ensure_ascii=False, indent=2)

    return out_path


def save_summary_json(
    output_dir: Path,
    results: list[dict[str, Any]],
) -> Path:
    """將所有檔案的彙總資訊存為 summary.json。"""
    out_path = output_dir / "summary.json"

    summary: dict[str, Any] = {
        "generated_at": datetime.now().isoformat(),
        "total_files": len(results),
        "results": results,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    return out_path


def save_combined_markdown(
    output_dir: Path,
    results: list[dict[str, Any]],
) -> Path:
    """將所有 OCR 結果合併為單一 .md 檔案。"""
    out_path = output_dir / "combined_ocr.md"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# 合併 OCR 結果\n\n")
        f.write(f"產生時間: {datetime.now().isoformat()}\n")
        f.write(f"檔案總數: {len(results)}\n\n")
        f.write("---\n\n")

        for i, item in enumerate(results, 1):
            f.write(f"## {i}. {item['filename']}\n\n")
            f.write(item.get("markdown", "(無結果)"))
            f.write("\n\n---\n\n")

    return out_path
