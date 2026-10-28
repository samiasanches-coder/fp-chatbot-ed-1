from __future__ import annotations

import json
import os
from pathlib import Path

from tools.base_tool import BaseTool


class G4FChatModel(BaseTool):
    name = "chat_model"

    def run(self, text: str):
        try:
            import g4f
        except Exception:
            return {"tool": self.name, "status": "unavailable", "content": "g4f is not installed. Install dependencies and try again."}

        try:
            if hasattr(g4f, "ChatCompletion"):
                response = g4f.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": text}],
                )
                return {"tool": self.name, "status": "enabled", "content": response if isinstance(response, str) else str(response)}

            if hasattr(g4f, "client"):
                try:
                    client = g4f.client.Client()
                    completion = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": text}])
                    response_text = getattr(completion, "choices", [{}])[0].message.content
                    return {"tool": self.name, "status": "enabled", "content": response_text}
                except Exception:
                    pass

            return {"tool": self.name, "status": "unavailable", "content": "g4f is installed but the API surface changed; please update the model client call."}
        except Exception as exc:
            return {"tool": self.name, "status": "error", "content": str(exc)}
