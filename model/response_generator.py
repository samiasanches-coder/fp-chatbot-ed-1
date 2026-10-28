class ResponseGenerator:
    def generate(self, prompt: str) -> str:
        user_text = prompt.split("User: ", 1)[1].split("\nAssistant:", 1)[0].strip()
        if not user_text:
            return "I’m ready to help."

        lowered = user_text.lower()
        if "hello" in lowered or "hi" in lowered:
            return "Hello! How can I help you today?"
        if "how are you" in lowered:
            return "I’m doing well and ready to help."
        if "name" in lowered and "your" in lowered:
            return "I’m FP Chatbot Edition 1."
        return f"You said: '{user_text}'. I’m here to help with your chatbot project."
