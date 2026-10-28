from dataclasses import dataclass, field


@dataclass
class PromptBuilder:
    system_message: str = "You are a helpful assistant. Keep answers concise and friendly."
    examples: list[str] = field(default_factory=list)

    def build(self, user_message: str) -> str:
        return self.system_message + "\nUser: " + user_message + "\nAssistant:"
