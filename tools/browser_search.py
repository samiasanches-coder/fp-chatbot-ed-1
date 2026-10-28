from __future__ import annotations

import os
from pathlib import Path

import requests

from tools.base_tool import BaseTool


class VisionTool(BaseTool):
    name = "image_read"

    def run(self, text: str):
        image_path = Path("data/generated/images/generated_image.png")
        if not image_path.exists():
            return {
                "tool": self.name,
                "status": "enabled",
                "summary": "No image exists yet. Generate one first with the image generation tool.",
            }

        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        if api_key:
            try:
                with open(image_path, "rb") as fh:
                    files = {"image": (image_path.name, fh, "image/png")}
                    headers = {"Authorization": f"Bearer {api_key}"}
                    response = requests.post("https://api.deepseek.com/v1/vision", headers=headers, files=files, timeout=30)
                    response.raise_for_status()
                    payload = response.json()
                    return {"tool": self.name, "status": "enabled", "summary": payload.get("content") or payload.get("text") or "Image analyzed successfully.", "image_path": str(image_path)}
            except Exception as exc:
                return {"tool": self.name, "status": "error", "message": str(exc), "image_path": str(image_path)}

        try:
            from PIL import Image
            with Image.open(image_path) as img:
                width, height = img.size
                mode = img.mode
            return {"tool": self.name, "status": "enabled", "summary": f"Image read successful. Size: {width}x{height}, mode: {mode}.", "image_path": str(image_path)}
        except Exception as exc:
            return {"tool": self.name, "status": "enabled", "summary": f"Basic image metadata fallback: {exc}", "image_path": str(image_path)}
