# tools/search_tools.py

import os, json, requests
from dotenv import load_dotenv
load_dotenv()
import streamlit as st

from crewai.tools import BaseTool

SERPER_API = os.getenv("SERPER_API_KEY")

class SearchInternetTool(BaseTool):
    name: str = "search_internet"
    description: str = "使用 SERPER API 在网上查询旅行相关信息"

    def _run(self, query: str) -> str:
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            "X-API-KEY": SERPER_API,
            "Content-Type": "application/json"
        }
        resp = requests.post(url, headers=headers, data=payload)
        data = resp.json()
        if "organic" not in data:
            return "未能获取到搜索结果，请检查 Serper API Key 配置。"
        snippets = []
        for item in data["organic"][:4]:
            title = item.get("title", "")
            link  = item.get("link", "")
            snip  = item.get("snippet", "")
            snippets.append(f"Title: {title}\nLink: {link}\nSnippet: {snip}\n---")
        return "\n".join(snippets)

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("SearchInternetTool 不支持异步调用")