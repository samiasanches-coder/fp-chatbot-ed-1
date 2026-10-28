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

        if any(token in lowered for token in ["generate image", "make image", "create image", "image of"]):
            return "image_gen"
        if any(token in lowered for token in ["read image", "analyze image", "describe image", "inspect image"]):
            return "image_read"
        if any(token in lowered for token in ["transcribe", "speech to text", "stt"]):
            return "stt"
        if any(token in lowered for token in ["tts", "text to speech", "say this", "read this"]):
            return "tts"
        if any(token in lowered for token in ["search the web", "web search", "look up", "search for"]):
            return "web_search"
        if any(token in lowered for token in ["voice clone", "clone voice"]):
            return "voice_clone"
        if any(token in lowered for token in ["calculate", "math", "sum", "total", "+"]):
            return "calculator"
        if any(token in lowered for token in ["write file", "edit file", "create file", "save file"]):
            return "file_editor"
        if any(token in lowered for token in ["api", "call api", "http request"]):
            return "external_api"
        return None

    def _dispatch_tool(self, tool_name: str, message: str):
        tool = self.registry.get(tool_name)
        if tool is None:
            return {"tool": tool_name, "status": "disabled", "message": "This tool is not enabled in config/features.json."}
        return tool.run(message)

    def _default_reply(self, message: str) -> str:
        lower = message.strip().lower()
        if not message.strip():
            return "Please say something so I can help."
        if any(token in lower for token in ["hello", "hi"]):
            return "Hello! I can generate images, analyze images, search the web, synthesize speech, transcribe audio, and save your chat history."
        if "how are you" in lower:
            return "I’m doing well and ready to help."
        if any(token in lower for token in ["bye", "goodbye"]):
            return "Goodbye! Your session is saved and I’ll be ready when you return."
        return (
            f"You said: '{message}'. I can help with voice, image generation, image reading, web search, file actions, "
            "and more as long as the feature is enabled in config/features.json."
        )

    def respond(self, user_message: str, session_id: str = "default") -> str:
        session = self.session_manager.load_session(session_id)
        session.add_user_message(user_message)

        tool_name = self._guess_tool(user_message)
        if tool_name:
            result = self._dispatch_tool(tool_name, user_message)
            response = json.dumps(result, indent=2, ensure_ascii=False) if isinstance(result, dict) else str(result)
        else:
            response = self._default_reply(user_message)

        session.add_assistant_message(response)
        self.session_manager.save_session(session)
        self.history_store.append(session_id, "user", user_message)
        self.history_store.append(session_id, "assistant", response)
        return response

    def resume_last_session(self):
        return self.session_manager.load_last_session()

    def list_sessions(self):
        return self.session_manager.list_sessions()
