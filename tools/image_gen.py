from tools.base_tool import BaseTool


class STTPlugin(BaseTool):
    name = "stt"

    def run(self, text: str):
        return {
            "tool": self.name,
            "status": "enabled",
            "transcript": "This is a mocked speech-to-text result from the configured STT tool.",
            "source_file": "data/generated/audio/input.wav",
        }
