from dataclasses import dataclass


@dataclass
class InputGuard:
    forbidden_phrases: tuple[str, ...] = ("ignore previous", "system prompt")

    def validate(self, user_input: str):
        text = user_input.strip()
        if not text:
            return {"safe": False, "message": "Please enter a message."}
        lowered = text.lower()
        for phrase in self.forbidden_phrases:
            if phrase in lowered:
                return {"safe": False, "message": "Your message contains disallowed content."}
        return {"safe": True, "message": "ok"}
