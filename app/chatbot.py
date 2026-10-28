from __future__ import annotations

import json
from pathlib import Path

from core.chat_history import ChatHistoryStore
from core.session import SessionManager
from tools.registry import ToolRegistry


class Chatbot:
    def __init__(self, features_path: str = "config/features.json"):
        self.features_path = Path(features_path)
        self.registry = ToolRegistry(str(self.features_path))
        self.session_manager = SessionManager(storage_dir="data/sessions")
        self.history_store = ChatHistoryStore(path="data/chat_history.jsonl")
        self._register_builtin_tools()

    def _register_builtin_tools(self):
        try:
            from tools.tts import TTSTool
            from tools.stt import STTTool
            from tools.image_gen import ImageGenerationTool
            from tools.vision import VisionTool
            from tools.browser_search import BrowserSearchTool
            from tools.voice_clone import VoiceCloneTool
            from tools.calculator import CalculatorTool
            from tools.file_editor import FileEditorTool
            from tools.external_api import ExternalAPITool
        except Exception:
            return

        self.registry.register("tts", TTSTool())
        self.registry.register("stt", STTTool())
        self.registry.register("image_gen", ImageGenerationTool())
        self.registry.register("image_read", VisionTool())
        self.registry.register("web_search", BrowserSearchTool())
        self.registry.register("voice_clone", VoiceCloneTool())
        self.registry.register("calculator", CalculatorTool())
        self.registry.register("file_editor", FileEditorTool())
        self.registry.register("external_api", ExternalAPITool())

    def _guess_tool(self, message: str):
        lowered = message.lower()
        if any(...)