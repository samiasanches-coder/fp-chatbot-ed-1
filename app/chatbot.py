from dataclasses import dataclass, field

from agent.orchestrator import Orchestrator
from memory.short_term_memory import ShortTermMemory
from safety.input_guard import InputGuard


@dataclass
class Chatbot:
    orchestrator: Orchestrator = field(default_factory=Orchestrator)
    memory: ShortTermMemory = field(default_factory=ShortTermMemory)
    guard: InputGuard = field(default_factory=InputGuard)

    def respond(self, user_message: str) -> str:
        validation = self.guard.validate(user_message)
        if not validation["safe"]:
            return validation["message"]

        self.memory.add(user_message)
        result = self.orchestrator.handle(user_message)
        self.memory.add(result["response"])
        return result["response"]
