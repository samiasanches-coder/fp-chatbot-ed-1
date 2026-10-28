from __future__ import annotations

from pathlib import Path

try:
    import whisper
except Exception:  # pragma: no cover
    whisper = None

from tools.base_tool import BaseTool


class STTTool(BaseTool):
    name = "stt"

    def run(self, text: str):
        audio_path = Path("data/generated/audio/input.wav")
        audio_path.parent.mkdir(parents=True, exist_ok=True)

        if not audio_path.exists():
            return {
                "tool": self.name,
                "status": "enabled",
                "transcript": "No audio file exists yet. Put a .wav file into data/generated/audio/input.wav to transcribe it.",
            }

        if whisper is None:
            return {
                "tool": self.name,
                "status": "enabled",
                "transcript": "Whisper is not installed; this is a placeholder transcription result.",
                "source_file": str(audio_path),
            }

        try:
            model = whisper.load_model("base")
            result = model.transcribe(str(audio_path), fp16=False)
            return {"tool": self.name, "status": "enabled", "transcript": result["text"], "source_file": str(audio_path)}
        except Exception as exc:
            return {"tool": self.name, "status": "error", "message": str(exc), "source_file": str(audio_path)}
