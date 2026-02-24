#!/usr/bin/env python3
"""搜索 MCP 服务器 - 使用 SearXNG 后端"""

import sys
import urllib.request
import urllib.parse
import json

# SearXNG 服务器地址
SEARXNG_URL = "http://100.126.219.109:7070"

def searxng_search(query, max_results=10):
    """调用 SearXNG API"""
    try:
        params = {'q': query, 'format': 'json'}
        url = f"{SEARXNG_URL}/search?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        return data.get('results', [])[:max_results]
    except Exception as e:
        return [{"error": f"搜索失败：{str(e)}"}]

def web_search(query, max_results=5):
    """搜索网页"""
    results = searxng_search(query, min(max_results, 30))
    return [{"title": r.get("title", ""), "url": r.get("url", ""), "snippet": r.get("content", ""), "source": r.get("engine", "")} for r in results]

def news_search(query, max_results=5):
    """搜索新闻"""
    results = searxng_search(query, min(max_results, 30))
    return [{"title": r.get("title", ""), "url": r.get("url", ""), "snippet": r.get("content", ""), "source": r.get("engine", ""), "date": r.get("publishedDate", "")} for r in results]

def search_summary(query):
    """搜索并生成摘要"""
    results = searxng_search(query, 10)
    if not results:
        return "未找到相关结果"
    summary = f"搜索「{query}」找到 {len(results)} 个结果：\n\n"
    for i, r in enumerate(results, 1):
        summary += f"{i}. **{r.get('title', '')}**\n   {r.get('content', '')}\n   来源：{r.get('engine', '')}\n   链接：{r.get('url', '')}\n\n"
    return summary

if __name__ == "__main__":
    print("🔍 搜索 MCP 服务器 (SearXNG)")
    print(f"服务器：{SEARXNG_URL}")
    print("工具：web_search, news_search, search_summary")
