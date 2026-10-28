from tools.base_tool import BaseTool


class ImageGeneratorPlugin(BaseTool):
    name = "image_gen"

    def run(self, text: str):
        prompt = text.replace("generate image", "").replace("make image", "").replace("draw", "").strip() or "robot cityscape"
        return {
            "tool": self.name,
            "status": "enabled",
            "prompt": prompt,
            "output_file": "data/generated/images/generated_image.png",
        }
