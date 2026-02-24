# Search MCP Server

🔍 免费的网络搜索 MCP 服务器，使用 SearXNG 作为后端。

## ✨ 特性

- 🆓 **完全免费** - 无需 API 密钥
- 🔍 **多种搜索** - 网页搜索、新闻搜索、搜索摘要
- 🚀 **快速部署** - 一键安装脚本
- 🔌 **标准 MCP** - 兼容所有 MCP 客户端

## 📦 安装

### 方法 1：一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/kikohz/search-mcp/main/install.sh | bash
```

### 方法 2：Git 克隆

```bash
git clone https://github.com/kikohz/search-mcp.git
cd search-mcp
pip3 install -r requirements.txt
python3 search_mcp.py
```

## 🔌 配置

### Claude Desktop

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "search": {
      "command": "python3",
      "args": ["/home/用户名/.local/search-mcp/search_mcp.py"]
    }
  }
}
```

## 🛠️ 使用

### web_search
```json
{
  "name": "web_search",
  "arguments": {
    "query": "Python 教程",
    "max_results": 5
  }
}
```

### news_search
```json
{
  "name": "news_search",
  "arguments": {
    "query": "AI 新闻",
    "max_results": 5
  }
}
```

### search_summary
```json
{
  "name": "search_summary",
  "arguments": {
    "query": "如何学习机器学习"
  }
}
```

## 📚 更多文档

详见 [DEPLOY.md](DEPLOY.md)

---

**版本**: 1.0.1  
**许可证**: MIT
