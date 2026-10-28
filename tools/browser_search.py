from __future__ import annotations

import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup

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

        url = f"https://duckduckgo.com/html/?q={query}"
        try:
            page = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            page.raise_for_status()
            soup = BeautifulSoup(page.text, "html.parser")
            results = []
            for item in soup.select(".result")[:5]:
                title = item.select_one(".result__title")
                snippet = item.select_one(".result__snippet")
                link = item.select_one("a")
                results.append({
                    "title": title.get_text(" ", strip=True) if title else "",
                    "snippet": snippet.get_text(" ", strip=True) if snippet else "",
                    "url": link.get("href", "") if link else "",
                })
            return {"tool": self.name, "status": "enabled", "query": query, "results": results}
        except Exception as exc:
            return {"tool": self.name, "status": "error", "query": query, "message": str(exc)}
