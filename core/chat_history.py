from __future__ import annotations

import json
from pathlib import Path


class ChatHistoryStore:
    def __init__(self, path: str = "data/chat_history.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, session_id: str, role: str, message: str):
        entry = {"session_id": session_id, "role": role, "message": message}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def read(self, session_id: str):
        if not self.path.exists():
            return []
        entries = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                item = json.loads(line)
                if item.get("session_id") == session_id:
                    entries.append(item)
        return entries
