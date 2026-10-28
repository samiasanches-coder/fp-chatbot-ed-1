class SessionStore:
    def __init__(self):
        self.store = {}

    def save(self, session_id: str, value):
        self.store[session_id] = value

    def get(self, session_id: str):
        return self.store.get(session_id)
