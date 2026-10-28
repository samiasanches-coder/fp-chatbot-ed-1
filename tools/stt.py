from tools.base_tool import BaseTool


class TTSPlugin(BaseTool):
    name = "tts"

    def run(self, text: str):
        phrase = text.replace("tts", "").replace("text to speech", "").strip()
        if not phrase:
            phrase = "Hello from FP Gemini Edition 1."
        return {
            "tool": self.name,
            "status": "enabled",
            "message": phrase,
            "voice": "default",
            "output_file": "data/generated/audio/voice_output.wav",
        }
