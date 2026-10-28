from tools.base_tool import BaseTool


class BrowserSearchPlugin(BaseTool):
    name = "web_search"

    def run(self, text: str):
        query = text.replace("search", "").replace("web", "").replace("lookup", "").strip() or "latest AI news"
        return {
            "tool": self.name,
            "status": "enabled",
            "query": query,
            "results": [
                {"title": "Example search result", "snippet": "This is a mock web search result for the configured browser search tool."}
            ],
        }
