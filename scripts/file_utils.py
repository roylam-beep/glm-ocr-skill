"""
檔案處理工具：掃描目錄、格式轉換（WebP → PNG）、base64 編碼。
"""

import base64
import os
from pathlib import Path
from typing import Optional

from PIL import Image

# 支援的檔案格式
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf", ".webp"}

# MIME 對照表
MIME_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".pdf": "application/pdf",
}


def find_supported_files(scan_dir: str) -> list[Path]:
    """掃描目錄，回傳所有支援的檔案路徑（僅當前目錄，不遞迴）。"""
    scan_path = Path(scan_dir)
    if not scan_path.is_dir():
        raise FileNotFoundError(f"目錄不存在: {scan_dir}")

    files: list[Path] = []
    for f in sorted(scan_path.iterdir()):
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(f)
    return files


def convert_webp_to_png(webp_path: Path) -> Path:
    """將 WebP 檔案轉為 PNG，回傳 PNG 路徑。"""
    png_path = webp_path.with_suffix(".png")
    img = Image.open(webp_path)
    img.save(png_path, "PNG")
    return png_path


def encode_file_to_data_uri(file_path: Path) -> str:
    """將檔案編碼為 base64 data URI（供 API 使用）。"""
    ext = file_path.suffix.lower()
    converted = False

    # WebP 先轉成 PNG
    if ext == ".webp":
        file_path = convert_webp_to_png(file_path)
        ext = ".png"
        converted = True

    mime_type = MIME_MAP.get(ext, "application/octet-stream")

    try:
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        encoded = base64.b64encode(file_bytes).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"
    finally:
        # 清除 WebP 轉換產生的暫存 PNG
        if converted:
            file_path.unlink(missing_ok=True)


def get_file_size_mb(file_path: Path) -> float:
    """取得檔案大小（MB）。"""
    return os.path.getsize(file_path) / (1024 * 1024)


def validate_file(file_path: Path) -> Optional[str]:
    """驗證檔案是否符合 API 限制。回傳錯誤訊息，通過則回傳 None。

    注意：WebP 會先轉為 PNG 再上傳，此處以 WebP 原始大小估算，
    極端情況下壓縮率高的 WebP 轉 PNG 後可能膨脹超過 10MB 上限。
    """
    ext = file_path.suffix.lower()

    # 判斷實際處理後的格式（WebP → PNG）
    if ext == ".webp":
        ext = ".png"

    if ext == ".pdf":
        max_size = 50  # MB
    elif ext in (".jpg", ".jpeg", ".png"):
        max_size = 10  # MB
    else:
        return f"不支援的檔案格式: {ext}"

    size_mb = get_file_size_mb(file_path)
    if size_mb > max_size:
        return f"檔案過大: {file_path.name} ({size_mb:.1f}MB)，上限 {max_size}MB"

    return None
