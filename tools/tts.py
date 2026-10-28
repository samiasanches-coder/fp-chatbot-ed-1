from __future__ import annotations

from pathlib import Path

try:
    import pyttsx3
except Exception:  # pragma: no cover
    pyttsx3 = None

try:
    from gtts import gTTS
except Exception:  # pragma: no cover
    gTTS = None

from tools.base_tool import BaseTool


class TTSTool(BaseTool):
    name = "tts"

    def run(self, text: str):
        clean_text = text.replace("tts", "").replace("text to speech", "").replace("say", "").strip() or "Hello from FP Gemini Edition 1."
        output_dir = Path("data/generated/audio")
        output_dir.mkdir(parents=True, exist_ok=True)
        output = output_dir / "voice_output.mp3"

        if pyttsx3 is not None:
            try:
                engine = pyttsx3.init()
                engine.save_to_file(clean_text, str(output))
                engine.runAndWait()
                return {"tool": self.name, "status": "enabled", "audio_path": str(output), "text": clean_text}
            except Exception:
                pass

        if gTTS is not None:
            try:
                gTTS(clean_text, lang="en").save(output)
                return {"tool": self.name, "status": "enabled", "audio_path": str(output), "text": clean_text}
            except Exception as exc:
                return {"tool": self.name, "status": "error", "message": str(exc)}

        fallback = output_dir / "voice_output.txt"
        fallback.write_text(clean_text, encoding="utf-8")
        return {
            "tool": self.name,
            "status": "enabled",
            "audio_path": str(fallback),
            "text": clean_text,
            "note": "No TTS engine installed; text fallback generated.",
        }
