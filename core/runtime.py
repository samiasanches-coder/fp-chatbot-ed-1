from dataclasses import dataclass


@dataclass
class Runtime:
    session_manager: object = None
    active_session_id: str | None = None

    def __post_init__(self):
        if self.session_manager is None:
            from core.session import SessionManager
            self.session_manager = SessionManager()

    def set_session(self, session_id: str):
        self.active_session_id = session_id
