#!/usr/bin/env python3
"""
搜索 MCP 服务器 - 使用 DuckDuckGo 作为后端
提供免费的网络搜索功能
"""

import asyncio
import json
import sys
from duckduckgo_search import DDGS

# MCP 工具定义
TOOLS = [
    {
        "name": "web_search",
        "description": "搜索网络信息",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"},
                "max_results": {"type": "integer", "description": "返回结果数量 (默认 5，最多 10)", "default": 5}
            },
            "required": ["query"]
        }
    },
    {
        "name": "news_search",
        "description": "搜索新闻",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"},
                "max_results": {"type": "integer", "description": "返回结果数量 (默认 5)", "default": 5}
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_summary",
        "description": "搜索并生成摘要",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"}
            },
            "required": ["query"]
        }
    }
]

def web_search(query: str, max_results: int = 5) -> list:
    """搜索网页"""
    max_results = min(max_results, 10)
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return [{"title": r.get("title", ""), "url": r.get("href", ""), "snippet": r.get("body", ""), "source": r.get("source", "")} for r in results]
    except Exception as e:
        return [{"error": f"搜索失败：{str(e)}"}]

def news_search(query: str, max_results: int = 5) -> list:
    """搜索新闻"""
    max_results = min(max_results, 10)
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results))
        return [{"title": r.get("title", ""), "url": r.get("url", ""), "snippet": r.get("body", ""), "source": r.get("source", ""), "date": r.get("date", "")} for r in results]
    except Exception as e:
        return [{"error": f"新闻搜索失败：{str(e)}"}]

def search_summary(query: str) -> str:
    """搜索并生成摘要"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        if not results:
            return "未找到相关结果"
        summary = f"搜索「{query}」找到 {len(results)} 个结果：\n\n"
        for i, r in enumerate(results, 1):
            summary += f"{i}. **{r.get('title', '')}**\n   {r.get('body', '')}\n   来源：{r.get('source', '')}\n   链接：{r.get('href', '')}\n\n"
        return summary
    except Exception as e:
        return f"搜索失败：{str(e)}"

def handle_tool_call(tool_name: str, args: dict):
    """处理工具调用"""
    if tool_name == "web_search":
        return web_search(args.get("query", ""), args.get("max_results", 5))
    elif tool_name == "news_search":
        return news_search(args.get("query", ""), args.get("max_results", 5))
    elif tool_name == "search_summary":
        return search_summary(args.get("query", ""))
    else:
        return {"error": f"未知工具：{tool_name}"}

if __name__ == "__main__":
    print("🔍 搜索 MCP 服务器")
    print("=" * 50)
    print("可用工具:")
    for tool in TOOLS:
        print(f"  - {tool['name']}: {tool['description']}")
    print("=" * 50)
    print("")
    print("这是一个 MCP 服务器，需要通过 MCP 客户端调用。")
    print("")
    print("Claude Desktop 配置示例:")
    print(json.dumps({
        "mcpServers": {
            "search": {
                "command": "python3",
                "args": ["/root/.openclaw/workspace/mcp-search-server/search_mcp_stdio.py"]
            }
        }
    }, indent=2))
    print("")
    print("测试调用:")
    print("  web_search(query='Python 教程', max_results=3)")
    print("")
    
    # 简单测试
    print("运行测试...")
    result = web_search("Python 教程", 3)
    print(f"测试结果：{len(result)} 条结果")
    for r in result:
        print(f"  - {r.get('title', 'N/A')}")
