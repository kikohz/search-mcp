#!/bin/bash
# 搜索 MCP 服务器 - 一键安装脚本
# 用法：curl -sSL https://your-server.com/install-search-mcp.sh | bash

set -e

echo "🔍 搜索 MCP 服务器安装程序"
echo "================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Python
echo "📋 检查系统依赖..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误：需要 Python 3.8+${NC}"
    echo "请安装：sudo apt install python3 python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION 已安装"

# 检查 pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  安装 pip3...${NC}"
    sudo apt install -y python3-pip
fi

# 创建安装目录
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/search-mcp}"
echo ""
echo "📁 安装目录：$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# 下载文件
echo ""
echo "📥 下载文件..."

# search_mcp.py
cat > "$INSTALL_DIR/search_mcp.py" << 'PYTHON_EOF'
#!/usr/bin/env python3
"""搜索 MCP 服务器 - DuckDuckGo 后端"""

import sys
from duckduckgo_search import DDGS

TOOLS = [
    {
        "name": "web_search",
        "description": "搜索网络信息",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"},
                "max_results": {"type": "integer", "description": "返回结果数量 (1-10)", "default": 5}
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
                "max_results": {"type": "integer", "description": "返回结果数量 (1-10)", "default": 5}
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

def web_search(query, max_results=5):
    max_results = min(max_results, 10)
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return [{"title": r.get("title", ""), "url": r.get("href", ""), "snippet": r.get("body", ""), "source": r.get("source", "")} for r in results]
    except Exception as e:
        return [{"error": f"搜索失败：{str(e)}"}]

def news_search(query, max_results=5):
    max_results = min(max_results, 10)
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results))
        return [{"title": r.get("title", ""), "url": r.get("url", ""), "snippet": r.get("body", ""), "source": r.get("source", ""), "date": r.get("date", "")} for r in results]
    except Exception as e:
        return [{"error": f"新闻搜索失败：{str(e)}"}]

def search_summary(query):
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

if __name__ == "__main__":
    print("🔍 搜索 MCP 服务器已启动")
    print("可用工具：web_search, news_search, search_summary")
    print("配置 MCP 客户端连接到本脚本")
PYTHON_EOF

# requirements.txt
cat > "$INSTALL_DIR/requirements.txt" << 'REQ_EOF'
mcp>=1.0.0
ddgs>=8.0.0
REQ_EOF

# install.sh (本脚本)
cp "$0" "$INSTALL_DIR/install.sh" 2>/dev/null || true

# 设置权限
chmod +x "$INSTALL_DIR/search_mcp.py"
chmod +x "$INSTALL_DIR/install.sh"

# 安装依赖
echo ""
echo "📦 安装 Python 依赖..."
pip3 install --user -r "$INSTALL_DIR/requirements.txt"

# 创建配置文件
cat > "$INSTALL_DIR/config.json" << 'CONFIG_EOF'
{
  "name": "search-mcp",
  "version": "1.0.0",
  "description": "免费的网络搜索 MCP 服务",
  "tools": ["web_search", "news_search", "search_summary"]
}
CONFIG_EOF

# 测试安装
echo ""
echo "🧪 测试安装..."
if python3 "$INSTALL_DIR/search_mcp.py" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 安装成功！${NC}"
else
    echo -e "${RED}❌ 测试失败${NC}"
    exit 1
fi

# 显示配置说明
echo ""
echo "================================"
echo -e "${GREEN}🎉 安装完成！${NC}"
echo "================================"
echo ""
echo "📁 安装位置：$INSTALL_DIR"
echo ""
echo "🔌 配置 MCP 客户端："
echo ""
echo "在 Claude Desktop 或其他 MCP 客户端的配置中添加："
echo ""
echo '{'
echo '  "mcpServers": {'
echo '    "search": {'
echo '      "command": "python3",'
echo '      "args": ["'$INSTALL_DIR'/search_mcp.py"]'
echo '    }'
echo '  }'
echo '}'
echo ""
echo "📚 使用说明："
echo "  - 运行：python3 $INSTALL_DIR/search_mcp.py"
echo "  - 卸载：rm -rf $INSTALL_DIR"
echo ""
echo "✅ 可用工具:"
echo "  - web_search(query, max_results) - 网页搜索"
echo "  - news_search(query, max_results) - 新闻搜索"
echo "  - search_summary(query) - 搜索摘要"
echo ""
