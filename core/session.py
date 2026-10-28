from dataclasses import dataclass, field


@dataclass
class Session:
    session_id: str
    user_message_history: list[str] = field(default_factory=list)
    assistant_message_history: list[str] = field(default_factory=list)

    def add_user_message(self, message: str):
        self.user_message_history.append(message)

    def add_assistant_message(self, message: str):
        self.assistant_message_history.append(message)


@dataclass
class SessionManager:
    sessions: dict[str, Session] = field(default_factory=dict)

    def get_or_create(self, session_id: str) -> Session:
        if session_id not in self.sessions:
            self.sessions[session_id] = Session(session_id=session_id)
        return self.sessions[session_id]
