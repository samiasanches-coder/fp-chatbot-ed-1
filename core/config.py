from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "fp-gemini-edition-1")
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    model_name: str = os.getenv("MODEL_NAME", "deepseek-chat")
    default_language: str = os.getenv("DEFAULT_LANGUAGE", "en")
    session_db_path: str = os.getenv("SESSION_DB_PATH", "data/sessions.db")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    nanobanana_api_key: str = os.getenv("NANOBANANA_API_KEY", "")
    nanobanana_base_url: str = os.getenv("NANOBANANA_BASE_URL", "https://api.nanobanana.ai")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    whisper_model: str = os.getenv("WHISPER_MODEL", "base")


settings = Settings()
