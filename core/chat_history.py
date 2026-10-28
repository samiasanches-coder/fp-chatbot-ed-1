from dataclasses import dataclass, field
import json
from pathlib import Path


@dataclass
class Session:
    session_id: str
    user_message_history: list[str] = field(default_factory=list)
    assistant_message_history: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def add_user_message(self, message: str):
        self.user_message_history.append(message)

    def add_assistant_message(self, message: str):
        self.assistant_message_history.append(message)

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "user_message_history": self.user_message_history,
            "assistant_message_history": self.assistant_message_history,
            "metadata": self.metadata,
        }


class SessionManager:
    def __init__(self, storage_dir: str = "data/sessions"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def get_session_path(self, session_id: str) -> Path:
        return self.storage_dir / f"{session_id}.json"

    def load_session(self, session_id: str) -> Session:
        path = self.get_session_path(session_id)
        if path.exists():
            payload = json.loads(path.read_text(encoding="utf-8"))
            session = Session(
                session_id=payload.get("session_id", session_id),
                user_message_history=payload.get("user_message_history", []),
                assistant_message_history=payload.get("assistant_message_history", []),
                metadata=payload.get("metadata", {}),
            )
            return session
        return Session(session_id=session_id)

    def save_session(self, session: Session):
        path = self.get_session_path(session.session_id)
        path.write_text(json.dumps(session.to_dict(), indent=2), encoding="utf-8")

    def load_last_session(self):
        sessions = sorted(self.storage_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not sessions:
            return Session(session_id="default")
        return self.load_session(sessions[0].stem)

    def append_history(self, session_id: str, role: str, message: str):
        path = Path("data/chat_history.jsonl")
        path.parent.mkdir(parents=True, exist_ok=True)
        entry = {"session_id": session_id, "role": role, "message": message}
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")
