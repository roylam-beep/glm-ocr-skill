"""
GLM-OCR API 呼叫模組：將檔案送入 Z.ai layout_parsing 端點進行 OCR 辨識。
"""

import json
import os
import time
from typing import Any

import requests


class GLMOCRProcessor:
    """封裝 Z.ai GLM-OCR API 的處理器。"""

    API_URL = "https://api.z.ai/api/paas/v4/layout_parsing"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def process_file(
        self,
        data_uri: str,
        start_page: int = 1,
        end_page: int | None = None,
        retries: int = 3,
    ) -> dict[str, Any]:
        """送出 OCR 請求並回傳完整的 API response JSON。"""
        payload: dict[str, Any] = {
            "model": "glm-ocr",
            "file": data_uri,
        }

        if end_page is not None:
            payload["start_page_id"] = start_page
            payload["end_page_id"] = end_page

        last_error = None
        for attempt in range(retries):
            try:
                resp = requests.post(
                    self.API_URL,
                    json=payload,
                    headers=self.headers,
                    timeout=120,
                )

                if resp.status_code == 200:
                    return resp.json()

                # 處理已知錯誤碼
                error_data = resp.json() if resp.text else {}
                error_msg = error_data.get("error", {}).get("message", resp.text)

                if resp.status_code == 429:
                    # 速率限制 — 等待後重試
                    wait = (attempt + 1) * 10
                    print(f"  [WARN] 速率限制，{wait} 秒後重試 (第 {attempt + 1}/{retries} 次)...")
                    time.sleep(wait)
                    continue

                if resp.status_code in (400, 401, 434, 435):
                    # 不可重試的錯誤
                    raise RuntimeError(
                        f"API 錯誤 (HTTP {resp.status_code}): {error_msg}"
                    )

                last_error = RuntimeError(
                    f"API 錯誤 (HTTP {resp.status_code}): {error_msg}"
                )

            except requests.exceptions.Timeout:
                print(f"  [WARN] 請求逾時，重試中 (第 {attempt + 1}/{retries} 次)...")
                last_error = RuntimeError("請求逾時")
                time.sleep(5)
                continue
            except requests.exceptions.ConnectionError as e:
                print(f"  [WARN] 連線錯誤，重試中 (第 {attempt + 1}/{retries} 次)...")
                last_error = e
                time.sleep(5)
                continue

        raise last_error or RuntimeError("OCR 處理失敗（已達最大重試次數）")

    def extract_markdown(self, response: dict[str, Any]) -> str:
        """從 API response 中提取 Markdown 結果。"""
        md = response.get("md_results", "")
        if not md:
            return "(無 OCR 結果)"
        return md

    def extract_metadata(self, response: dict[str, Any]) -> dict[str, Any]:
        """從 API response 中提取使用量與檔案資訊。"""
        data_info = response.get("data_info", {})
        usage = response.get("usage", {})

        return {
            "model": response.get("model", "glm-ocr"),
            "pages": data_info.get("num_pages", 0),
            "tokens_input": usage.get("prompt_tokens", 0),
            "tokens_output": usage.get("completion_tokens", 0),
            "tokens_total": usage.get("total_tokens", 0),
            "request_id": response.get("id", ""),
        }
