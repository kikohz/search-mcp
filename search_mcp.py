#!/usr/bin/env python3
"""
搜索 MCP 服务器 - 使用 SearXNG 作为后端
提供免费、隐私保护的网络搜索功能
"""

import sys
import json
import urllib.request
import urllib.parse

# SearXNG 服务器配置
SEARXNG_URL = "http://100.126.219.109:7070"

# MCP 工具定义
TOOLS = [
    {
        "name": "web_search",
        "description": "搜索网络信息",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"},
                "max_results": {"type": "integer", "description": "返回结果数量 (默认 10，最多 30)", "default": 10}
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
                "max_results": {"type": "integer", "description": "返回结果数量 (默认 10)", "default": 10}
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

def searxng_search(query, categories=None, max_results=10):
    """调用 SearXNG API 搜索"""
    try:
        # 构建 URL
        params = {
            'q': query,
            'format': 'json',
            'pageno': 1,
            'language': 'zh-CN'
        }
        
        if categories:
            params['categories'] = categories
        
        url = f"{SEARXNG_URL}/search?{urllib.parse.urlencode(params)}"
        
        # 发送请求
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (compatible; SearchMCP/1.0)')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # 提取结果
        results = data.get('results', [])[:max_results]
        
        return results
    
    except Exception as e:
        return [{"error": f"搜索失败：{str(e)}"}]

def web_search(query, max_results=10):
    """搜索网页"""
    max_results = min(max_results, 30)
    results = searxng_search(query, categories='general', max_results=max_results)
    
    formatted = []
    for r in results:
        if 'error' in r:
            return [r]
        formatted.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", ""),
            "source": r.get("engine", ""),
            "publishedDate": r.get("publishedDate", "")
        })
    
    return formatted

def news_search(query, max_results=10):
    """搜索新闻"""
    max_results = min(max_results, 30)
    results = searxng_search(query, categories='news', max_results=max_results)
    
    formatted = []
    for r in results:
        if 'error' in r:
            return [r]
        formatted.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", ""),
            "source": r.get("engine", ""),
            "publishedDate": r.get("publishedDate", "")
        })
    
    return formatted

def search_summary(query):
    """搜索并生成摘要"""
    results = searxng_search(query, categories='general', max_results=10)
    
    if not results or 'error' in results[0]:
        return "未找到相关结果"
    
    summary = f"搜索「{query}」找到 {len(results)} 个结果：\n\n"
    for i, r in enumerate(results, 1):
        summary += f"{i}. **{r.get('title', '')}**\n"
        summary += f"   {r.get('content', '')}\n"
        summary += f"   来源：{r.get('engine', '')}\n"
        if r.get('publishedDate'):
            summary += f"   日期：{r.get('publishedDate')}\n"
        summary += f"   链接：{r.get('url', '')}\n\n"
    
    return summary

if __name__ == "__main__":
    print("🔍 搜索 MCP 服务器 (SearXNG)")
    print("=" * 50)
    print(f"SearXNG 服务器：{SEARXNG_URL}")
    print("=" * 50)
    print("")
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
                "args": ["/root/.openclaw/workspace/mcp-search-server/search_mcp.py"]
            }
        }
    }, indent=2))
    print("")
    print("测试调用:")
    print("  web_search(query='Python 教程', max_results=5)")
    print("")
    
    # 简单测试
    print("运行测试...")
    result = web_search("Python 教程", 3)
    print(f"测试结果：{len(result)} 条结果")
    for r in result:
        print(f"  - {r.get('title', 'N/A')}")
