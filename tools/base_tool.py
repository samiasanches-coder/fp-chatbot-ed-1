import json
from pathlib import Path


class ToolRegistry:
    def __init__(self, features_path: str = "config/features.json"):
        self.features_path = Path(features_path)
        self.enabled_tools = self._load_enabled_tools()
        self.tools = {}

    def _load_enabled_tools(self):
        if not self.features_path.exists():
            return {}
        payload = json.loads(self.features_path.read_text(encoding="utf-8"))
        return payload.get("enabled_tools", {})

    def register(self, tool_name: str, tool_instance):
        if self.enabled_tools.get(tool_name, False):
            self.tools[tool_name] = tool_instance

    def get(self, tool_name: str):
        return self.tools.get(tool_name)

    def list_tools(self):
        return sorted(self.tools.keys())
