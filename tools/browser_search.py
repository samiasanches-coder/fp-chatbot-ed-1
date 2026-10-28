from tools.base_tool import BaseTool


class VisionPlugin(BaseTool):
    name = "image_read"

    def run(self, text: str):
        return {
            "tool": self.name,
            "status": "enabled",
            "summary": "This is a mocked image analysis result. The image can be read when a real image file is provided.",
            "image_path": "data/generated/images/example.png",
        }
