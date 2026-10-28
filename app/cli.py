from __future__ import annotations

import json
from pathlib import Path

from core.chat_history import ChatHistoryStore
from core.session import SessionManager, Session
from tools.registry import ToolRegistry
from tools.tts import TTSPlugin
from tools.stt import STTPlugin
from tools.image_gen import ImageGeneratorPlugin
from tools.vision import VisionPlugin
from tools.browser_search import BrowserSearchPlugin
from tools.voice_clone import VoiceClonePlugin
from tools.calculator import CalculatorPlugin
from tools.file_editor import FileEditorPlugin
from tools.external_api import ExternalApiPlugin


class Chatbot:
    def __init__(self, features_path: str = "config/features.json"):
        self.registry = ToolRegistry(features_path)
        self.registry.register("tts", TTSPlugin())
        self.registry.register("stt", STTPlugin())
        self.registry.register("image_gen", ImageGeneratorPlugin())
        self.registry.register("image_read", VisionPlugin())
        self.registry.register("web_search", BrowserSearchPlugin())
        self.registry.register("voice_clone", VoiceClonePlugin())
        self.registry.register("calculator", CalculatorPlugin())
        self.registry.register("file_editor", FileEditorPlugin())
        self.registry.register("external_api", ExternalApiPlugin())

        self.session_manager = SessionManager(storage_dir="data/sessions")
        self.history_store = ChatHistoryStore(path="data/chat_history.jsonl")

    def _guess_tool(self, text: str):
        lowered = text.lower()
        if "generate image" in lowered or "make image" in lowered or "draw" in lowered:
            return "image_gen"
        if "read image" in lowered or "analyze image" in lowered or "describe image" in lowered:
            return "image_read"
        if "transcribe" in lowered or "speech to text" in lowered or "stt" in lowered:
            return "stt"
        if "tts" in lowered or "text to speech" in lowered or "voice" in lowered and "say" in lowered:
            return "tts"
        if "search" in lowered or "web search" in lowered or "lookup" in lowered:
            return "web_search"
        if "clone voice" in lowered or "voice clone" in lowered:
            return "voice_clone"
        if "calculate" in lowered or "math" in lowered or "sum" in lowered:
            return "calculator"
        if "write file" in lowered or "edit file" in lowered:
            return "file_editor"
        if "api" in lowered or "call api" in lowered:
            return "external_api"
        return None

    def _dispatch_tool(self, tool_name: str, message: str):
        tool = self.registry.get(tool_name)
        if not tool:
            return "That tool is not enabled in the feature config."
        return tool.run(message)

    def respond(self, user_message: str, session_id: str = "default") -> str:
        session = self.session_manager.load_session(session_id)
        session.add_user_message(user_message)

        tool_name = self._guess_tool(user_message)
        if tool_name:
            result = self._dispatch_tool(tool_name, user_message)
            response = f"Tool: {tool_name}\n{result}"
        else:
            response = self._default_reply(user_message)

        session.add_assistant_message(response)
        self.session_manager.save_session(session)
        self.history_store.append(session_id, "user", user_message)
        self.history_store.append(session_id, "assistant", response)
        return response

    def _default_reply(self, text: str) -> str:
        lowered = text.lower().strip()
        if not lowered:
            return "Please say something to start the conversation."
        if "hello" in lowered or "hi" in lowered:
            return "Hello! I’m ready to help. I can generate images, read images, transcribe audio, synthesize speech, search the web, and more."
        if "how are you" in lowered:
            return "I’m doing well and ready to help with your next request."
        if "bye" in lowered or "goodbye" in lowered:
            return "Goodbye! I’ll be here when you want to continue."
        return f"You said: '{text}'. I can handle voice, speech, image generation, image reading, web search, file operations, and more when enabled in the config."

    def resume_last_session(self):
        session = self.session_manager.load_last_session()
        return session
