# Search MCP Server

🔍 免费的网络搜索 MCP (Model Context Protocol) 服务器，使用 **SearXNG** 作为后端。

## ✨ 特性

- 🆓 **完全免费** - 无需 API 密钥，无使用限制
- 🔍 **多种搜索** - 网页搜索、新闻搜索、搜索摘要
- 🚀 **快速部署** - 一键安装脚本
- 🔌 **标准 MCP** - 兼容 Claude Desktop、Cursor 等所有 MCP 客户端
- 🛡️ **隐私保护** - 本地部署，数据不经过第三方
- 🌐 **多引擎聚合** - 聚合 Google、DuckDuckGo、Brave、Wikipedia 等多个搜索引擎

## 📦 安装

### 方法 1：一键安装（推荐）

```bash
# 一键安装（自动下载并安装）
curl -fsSL https://raw.githubusercontent.com/kikohz/search-mcp/main/install.sh | bash
```

或分步执行：
```bash
# 下载安装脚本
curl -fsSL https://raw.githubusercontent.com/kikohz/search-mcp/main/install.sh -o install.sh

# 运行安装
bash install.sh
```

### 方法 2：Git 克隆

```bash
# 克隆仓库
git clone https://github.com/kikohz/search-mcp.git

# 进入目录
cd search-mcp

# 安装依赖
pip3 install -r requirements.txt

# 测试
python3 search_mcp.py
```

### 方法 3：手动下载

```bash
# 创建目录
mkdir -p ~/.local/search-mcp
cd ~/.local/search-mcp

# 下载主程序
curl -fsSL https://raw.githubusercontent.com/kikohz/search-mcp/main/search_mcp.py -o search_mcp.py

# 安装依赖（只需要 urllib，Python 内置）
# pip3 install mcp  # 可选，用于 MCP 开发

# 测试
python3 search_mcp.py
```

### 自定义 SearXNG 服务器

编辑 `search_mcp.py`，修改：

```python
# 第 14 行
SEARXNG_URL = "http://你的-searxng-server:端口"
```

默认配置：`http://100.126.219.109:7070`

## 🔌 配置

### Claude Desktop

编辑配置文件：

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

> 💡 **提示：** 将 `/home/用户名/` 替换为你的实际用户目录（Windows 使用 `C:\\Users\\用户名\\`）

### Cursor IDE

在项目根目录创建 `.cursor/mcp.json`:

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

### 其他 MCP 客户端

```json
{
  "mcpServers": {
    "search": {
      "command": "python3",
      "args": ["~/.local/search-mcp/search_mcp.py"]
    }
  }
}
```

## 🛠️ 使用

### 可用工具

#### 1. `web_search` - 网页搜索

```python
# MCP 工具调用
{
  "name": "web_search",
  "arguments": {
    "query": "Python 教程",
    "max_results": 5
  }
}
```

**返回示例:**
```json
[
  {
    "title": "Python 官方教程",
    "url": "https://docs.python.org/3/tutorial/",
    "snippet": "Python 编程语言官方文档...",
    "source": "docs.python.org"
  }
]
```

#### 2. `news_search` - 新闻搜索

```python
{
  "name": "news_search",
  "arguments": {
    "query": "AI 最新进展",
    "max_results": 5
  }
}
```

#### 3. `search_summary` - 搜索摘要

```python
{
  "name": "search_summary",
  "arguments": {
    "query": "如何学习机器学习"
  }
}
```

**返回示例:**
```
搜索「如何学习机器学习」找到 5 个结果：

1. **机器学习入门指南**
   本文介绍机器学习的基础知识...
   来源：zhuanlan.zhihu.com
   链接：https://...

2. **...**
```

## 📋 命令行测试

```bash
# 测试网页搜索
python3 -c "
from search_mcp import web_search
results = web_search('Python 教程', 3)
for r in results:
    print(f\"- {r['title']}\")
    print(f\"  {r['url']}\")
"

# 测试新闻搜索
python3 -c "
from search_mcp import news_search
results = news_search('AI 新闻', 3)
for r in results:
    print(f\"- {r['title']} ({r['date']})\")
"

# 测试搜索摘要
python3 -c "
from search_mcp import search_summary
print(search_summary('MCP 教程'))
"
```

## 🚀 高级用法

### HTTP 模式（远程访问）

```bash
# 安装额外依赖
pip3 install uvicorn fastapi

# 运行 HTTP 服务器
python3 search_mcp.py --transport http --port 8765

# 后台运行
nohup python3 search_mcp.py --transport http --port 8765 &
```

远程客户端配置：
```json
{
  "mcpServers": {
    "search": {
      "url": "http://server-ip:8765/mcp"
    }
  }
}
```

### 使用代理

```bash
# 设置环境变量
export HTTP_PROXY=http://proxy-server:port
export HTTPS_PROXY=http://proxy-server:port

# 运行
python3 search_mcp.py
```

### systemd 服务（Linux）

```bash
# 创建服务文件
sudo nano /etc/systemd/system/search-mcp.service
```

```ini
[Unit]
Description=Search MCP Server
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/.local/search-mcp
ExecStart=/usr/bin/python3 /home/your-username/.local/search-mcp/search_mcp.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable search-mcp
sudo systemctl start search-mcp
```

## 📊 对比其他方案

| 服务 | 免费额度 | 价格 | 优点 | 缺点 |
|------|---------|------|------|------|
| **Search MCP** | ✅ 无限 | 免费 | 无需 API 密钥 | 可能被限流 |
| Brave Search | 2000 次/月 | $3/月起 | 稳定 | 需要付费 |
| Google Custom | 100 次/天 | $5/1000 次 | 准确 | 贵 |
| Bing Search | 1000 次/月 | $15/1000 次 | 稳定 | 需要信用卡 |

## 🛠️ 开发

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/search-mcp.git
cd search-mcp

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行
python3 search_mcp.py
```

### 添加新工具

在 `search_mcp.py` 中添加：

```python
@mcp.tool()
async def image_search(query: str, max_results: int = 5) -> list[dict]:
    """搜索图片"""
    # 实现代码
    pass
```

## 📚 相关资源

- [MCP 官方文档](https://modelcontextprotocol.io)
- [DuckDuckGo Search API](https://pypi.org/project/ddgs/)
- [Claude Desktop](https://claude.ai/desktop)
- [Cursor IDE](https://cursor.sh)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 更新日志

### v1.0.0 (2026-02-21)
- ✨ 初始版本
- 🔍 支持网页搜索、新闻搜索、搜索摘要
- 🚀 一键安装脚本
- 📚 完整文档

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👤 作者

- **elok** - [GitHub](https://github.com/YOUR_USERNAME)

## 🙏 致谢

- [MCP](https://modelcontextprotocol.io) - Model Context Protocol
- [DuckDuckGo Search](https://pypi.org/project/ddgs/) - 搜索后端
- [Claude](https://claude.ai) - AI 助手

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
