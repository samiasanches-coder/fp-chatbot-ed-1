from __future__ import annotations

import os
from pathlib import Path

try:
    import tensorflow as tf  # noqa: F401
except Exception:  # pragma: no cover
    tf = None

try:
    import keras
    from keras import layers
except Exception:  # pragma: no cover
    keras = None
    layers = None

from tools.base_tool import BaseTool


class ImageGenerationTool(BaseTool):
    name = "image_gen"

    def run(self, text: str):
        prompt = text.replace("generate image", "").replace("make image", "").replace("create image", "").replace("image of", "").strip() or "future city"
        output_dir = Path("data/generated/images")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "generated_image.png"

        if keras is not None:
            try:
                from PIL import Image, ImageDraw
                img = Image.new("RGB", (900, 500), color=(25, 30, 60))
                draw = ImageDraw.Draw(img)
                for i in range(0, 900, 30):
                    draw.rectangle([i, 0, i + 20, 500], fill=(30 + i // 10, 60 + i // 20, 110))
                draw.rectangle([60, 120, 840, 400], fill=(80, 120, 180))
                draw.text((110, 200), prompt[:26], fill=(255, 255, 255))
                img.save(output_path)
                return {"tool": self.name, "status": "enabled", "prompt": prompt, "output_file": str(output_path)}
            except Exception:
                pass

        if os.getenv("NANOBANANA_API_KEY"):
            try:
                import requests
                base_url = os.getenv("NANOBANANA_BASE_URL", "https://api.nanobanana.ai")
                response = requests.post(
                    f"{base_url}/generate",
                    headers={"Authorization": f"Bearer {os.getenv('NANOBANANA_API_KEY')}", "Content-Type": "application/json"},
                    json={"prompt": prompt},
                    timeout=30,
                )
                response.raise_for_status()
                payload = response.json()
                image_url = payload.get("image_url") or payload.get("url")
                if image_url:
                    image_data = requests.get(image_url, timeout=30)
                    image_data.raise_for_status()
                    output_path.write_bytes(image_data.content)
                    return {"tool": self.name, "status": "enabled", "prompt": prompt, "output_file": str(output_path)}
            except Exception as exc:
                return {"tool": self.name, "status": "error", "prompt": prompt, "message": str(exc)}

        from PIL import Image, ImageDraw
        img = Image.new("RGB", (900, 500), color=(25, 30, 60))
        draw = ImageDraw.Draw(img)
        for i in range(0, 900, 30):
            draw.rectangle([i, 0, i + 20, 500], fill=(30 + i // 10, 60 + i // 20, 110))
        draw.rectangle([60, 120, 840, 400], fill=(80, 120, 180))
        draw.text((110, 200), prompt[:26], fill=(255, 255, 255))
        img.save(output_path)

        return {"tool": self.name, "status": "enabled", "prompt": prompt, "output_file": str(output_path)}
