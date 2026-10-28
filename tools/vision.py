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

        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                image_bytes = image_path.read_bytes()
                response = model.generate_content([
                    {"mime_type": "image/png", "data": image_bytes},
                    "Describe this image in a concise, helpful way."
                ])
                return {"tool": self.name, "status": "enabled", "summary": response.text, "image_path": str(image_path)}
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
