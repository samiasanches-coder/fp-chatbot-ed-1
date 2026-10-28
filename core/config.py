import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "fp-chatbot-ed-1")
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    model_name: str = os.getenv("MODEL_NAME", "local-chatbot")
    session_db_path: str = os.getenv("SESSION_DB_PATH", "data/sessions.db")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")


settings = Settings()
