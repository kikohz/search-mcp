#!/bin/bash
# 搜索 MCP 服务器 - 一键安装脚本
# 用法：curl -fsSL https://raw.githubusercontent.com/kikohz/search-mcp/main/install.sh | bash

set -e

echo "🔍 搜索 MCP 服务器安装程序"
echo "================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检测操作系统
OS="$(uname -s)"
echo "📋 检测系统：$OS"

# 检查 Python
echo "📋 检查系统依赖..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误：需要 Python 3.8+${NC}"
    if [[ "$OS" == "Darwin" ]]; then
        echo "请安装：brew install python3"
    else
        echo "请安装：sudo apt install python3 python3-pip"
    fi
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION 已安装"

# 检查 pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  安装 pip3...${NC}"
    if [[ "$OS" == "Darwin" ]]; then
        brew install python3
    else
        sudo apt install -y python3-pip
    fi
fi

# 创建安装目录
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/search-mcp}"
echo ""
echo "📁 安装目录：$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# 下载文件
echo ""
echo "📥 下载文件..."

# 从 GitHub 下载主程序
echo "  - 下载 search_mcp.py..."
curl -fsSL https://raw.githubusercontent.com/kikohz/search-mcp/main/search_mcp.py -o "$INSTALL_DIR/search_mcp.py" || {
    echo -e "${RED}❌ 下载失败，请检查网络连接${NC}"
    exit 1
}

# 下载 requirements.txt
echo "  - 下载 requirements.txt..."
curl -fsSL https://raw.githubusercontent.com/kikohz/search-mcp/main/requirements.txt -o "$INSTALL_DIR/requirements.txt" || {
    # 如果 requirements.txt 不存在，创建默认的
    cat > "$INSTALL_DIR/requirements.txt" << 'EOF'
mcp>=1.0.0
ddgs>=8.0.0
EOF
}

# 设置权限
echo "  - 设置文件权限..."
chmod +x "$INSTALL_DIR/search_mcp.py"

# 安装依赖
echo ""
echo "📦 安装 Python 依赖..."
if [[ "$OS" == "Darwin" ]]; then
    # macOS 使用 --user 参数
    pip3 install --user -r "$INSTALL_DIR/requirements.txt"
else
    # Linux 尝试系统安装，失败则用 --user
    pip3 install -r "$INSTALL_DIR/requirements.txt" 2>/dev/null || pip3 install --user -r "$INSTALL_DIR/requirements.txt"
fi

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
