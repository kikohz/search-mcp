#!/usr/bin/env python3
"""
搜索 MCP 服务器 - 使用 DuckDuckGo 作为后端
提供免费的网络搜索功能
"""

import asyncio
from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS

# 创建 MCP 服务器
mcp = FastMCP("search-server")


@mcp.tool()
async def web_search(query: str, max_results: int = 5) -> list[dict]:
    """
    搜索网络信息
    
    Args:
        query: 搜索关键词
        max_results: 返回结果数量 (默认 5，最多 10)
    
    Returns:
        搜索结果列表，每个结果包含:
        - title: 标题
        - url: 链接
        - snippet: 摘要
        - source: 来源网站
    """
    max_results = min(max_results, 10)  # 限制最多 10 条
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        # 格式化结果
        formatted = []
        for r in results:
            formatted.append({
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
                "source": r.get("source", "")
            })
        
        return formatted
    
    except Exception as e:
        return [{"error": f"搜索失败：{str(e)}"}]


@mcp.tool()
async def news_search(query: str, max_results: int = 5) -> list[dict]:
    """
    搜索新闻
    
    Args:
        query: 搜索关键词
        max_results: 返回结果数量 (默认 5)
    
    Returns:
        新闻结果列表
    """
    max_results = min(max_results, 10)
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results))
        
        formatted = []
        for r in results:
            formatted.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("body", ""),
                "source": r.get("source", ""),
                "date": r.get("date", "")
            })
        
        return formatted
    
    except Exception as e:
        return [{"error": f"新闻搜索失败：{str(e)}"}]


@mcp.tool()
async def image_search(query: str, max_results: int = 5) -> list[dict]:
    """
    搜索图片
    
    Args:
        query: 搜索关键词
        max_results: 返回结果数量 (默认 5)
    
    Returns:
        图片结果列表，包含标题、图片 URL、缩略图 URL
    """
    max_results = min(max_results, 10)
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=max_results))
        
        formatted = []
        for r in results:
            formatted.append({
                "title": r.get("title", ""),
                "image_url": r.get("image", ""),
                "thumbnail": r.get("thumbnail", ""),
                "source": r.get("source", ""),
                "width": r.get("width", ""),
                "height": r.get("height", "")
            })
        
        return formatted
    
    except Exception as e:
        return [{"error": f"图片搜索失败：{str(e)}"}]


@mcp.tool()
async def search_summary(query: str) -> str:
    """
    搜索并生成摘要
    
    Args:
        query: 搜索关键词
    
    Returns:
        搜索结果的文字摘要
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        
        if not results:
            return "未找到相关结果"
        
        # 生成摘要
        summary = f"搜索「{query}」找到 {len(results)} 个结果：\n\n"
        for i, r in enumerate(results, 1):
            summary += f"{i}. **{r.get('title', '')}**\n"
            summary += f"   {r.get('body', '')}\n"
            summary += f"   来源：{r.get('source', '')}\n"
            summary += f"   链接：{r.get('href', '')}\n\n"
        
        return summary
    
    except Exception as e:
        return f"搜索失败：{str(e)}"


if __name__ == "__main__":
    import sys
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--transport":
        # HTTP 模式
        import uvicorn
        from mcp.server.sse import SseServerTransport
        from mcp.server.streamable_http import StreamableHTTPTransport
        
        print("🚀 启动搜索 MCP 服务器 (HTTP 模式)")
        print(f"📍 监听端口：{sys.argv[3] if len(sys.argv) > 3 else 8765}")
        print(f"🌐 访问：http://localhost:{sys.argv[3] if len(sys.argv) > 3 else 8765}")
        print(f"🔌 MCP 端点：http://localhost:{sys.argv[3] if len(sys.argv) > 3 else 8765}/mcp")
        print("")
        
        # 运行 HTTP 服务器
        mcp.run(transport="sse")
    else:
        # stdio 模式
        print("🚀 启动搜索 MCP 服务器 (stdio 模式)")
        mcp.run()
