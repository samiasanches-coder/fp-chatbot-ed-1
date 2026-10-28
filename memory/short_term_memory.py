class ShortTermMemory:
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages = []

    def add(self, message: str):
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_context(self) -> str:
        return "\n".join(self.messages)
