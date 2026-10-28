import requests

from tools.base_tool import BaseTool


class ExternalAPITool(BaseTool):
    name = "external_api"

    def run(self, text: str):
        url = "https://httpbin.org/get"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return {"tool": self.name, "status": "enabled", "endpoint": url, "response": response.json()}
        except Exception as exc:
            return {"tool": self.name, "status": "error", "message": str(exc)}
