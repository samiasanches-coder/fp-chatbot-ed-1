from dataclasses import dataclass


@dataclass
class Orchestrator:
    def handle(self, user_message: str):
        from model.response_generator import ResponseGenerator

        response = ResponseGenerator().generate(
            f"System: You are a helpful assistant.\nUser: {user_message}\nAssistant:"
        )
        return {"response": response, "status": "ok"}
