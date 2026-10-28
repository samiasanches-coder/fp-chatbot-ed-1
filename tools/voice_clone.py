from __future__ import annotations

import os
from urllib.parse import quote_plus

import requests

from tools.base_tool import BaseTool


class BrowserSearchTool(BaseTool):
    name = "web_search"

    def run(self, text: str):
        query = text.replace("search the web for", "").replace("search for", "").replace("web search", "").replace("look up", "").strip() or "latest AI news"
        tavily_api_key = os.getenv("TAVILY_API_KEY", "")
        if tavily_api_key:
            try:
                response = requests.post(
                    "https://api.tavily.com/search",
                    json={"api_key": tavily_api_key, "query": query, "max_results": 5},
                    timeout=30,
                )
                response.raise_for_status()
                payload = response.json()
                return {"tool": self.name, "status": "enabled", "query": query, "results": payload.get("results", [])}
            except Exception as exc:
                return {"tool": self.name, "status": "error", "query": query, "message": str(exc)}

        url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_redirect=1&no_html=1"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            payload = response.json()
            related = payload.get("RelatedTopics", [])
            results = []
            for item in related[:5]:
                if isinstance(item, dict):
                    results.append({"text": item.get("Text", ""), "first_url": item.get("FirstURL", "")})
            return {"tool": self.name, "status": "enabled", "query": query, "results": results}
        except Exception as exc:
            return {"tool": self.name, "status": "error", "query": query, "message": str(exc)}
