# 搜索 MCP 服务器 - 部署指南

## 🚀 快速安装（推荐）

### 方法 1：一键安装脚本

在**目标电脑**上运行：

```bash
# 下载安装脚本
curl -o install-search-mcp.sh https://your-server.com/install.sh

# 或使用本地文件
bash /path/to/install.sh
```

### 方法 2：手动安装

```bash
# 1. 创建目录
mkdir -p ~/.local/search-mcp
cd ~/.local/search-mcp

# 2. 下载主程序
wget https://your-server.com/search_mcp.py

# 3. 安装依赖
pip3 install mcp ddgs

# 4. 测试
python3 search_mcp.py
```

### 方法 3：从本机复制

```bash
# 在本机打包
cd /root/.openclaw/workspace/mcp-search-server
tar -czf search-mcp.tar.gz search_mcp.py requirements.txt install.sh

# 复制到目标电脑
scp search-mcp.tar.gz user@target-computer:~/

# 在目标电脑解压安装
cd ~
tar -xzf search-mcp.tar.gz
bash install.sh
```

---

## 📋 系统要求

| 要求 | 说明 |
|------|------|
| **操作系统** | Linux / macOS / Windows (WSL) |
| **Python** | 3.8 或更高版本 |
| **网络** | 需要能访问 DuckDuckGo |
| **内存** | 最少 50MB |

### 检查系统

```bash
# 检查 Python 版本
python3 --version

# 检查网络连接
curl -I https://duckduckgo.com

# 测试 DuckDuckGo 访问
python3 -c "from duckduckgo_search import DDGS; print(DDGS().text('test', max_results=1))"
```

---

## 🔌 MCP 客户端配置

### Claude Desktop (macOS)

编辑配置文件：
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

添加配置：
```json
{
  "mcpServers": {
    "search": {
      "command": "python3",
      "args": ["/home/username/.local/search-mcp/search_mcp.py"]
    }
  }
}
```

### Claude Desktop (Windows)

编辑配置文件：
```
%APPDATA%\Claude\claude_desktop_config.json
```

添加配置：
```json
{
  "mcpServers": {
    "search": {
      "command": "python",
      "args": ["C:\\Users\\username\\.local\\search-mcp\\search_mcp.py"]
    }
  }
}
```

### Cursor IDE

在项目根目录创建 `.cursor/mcp.json`：
```json
{
  "mcpServers": {
    "search": {
      "command": "python3",
      "args": ["/home/username/.local/search-mcp/search_mcp.py"]
    }
  }
}
```

### 其他 MCP 客户端

参考 [MCP 官方文档](https://modelcontextprotocol.io/docs)

---

## 🛠️ 高级配置

### 使用 HTTP 模式（远程访问）

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

### 使用代理（如果 DuckDuckGo 被限制）

```bash
# 设置环境变量
export HTTP_PROXY=http://proxy-server:port
export HTTPS_PROXY=http://proxy-server:port

# 或在代码中配置
python3 -c "
import os
os.environ['HTTP_PROXY'] = 'http://proxy-server:port'
os.environ['HTTPS_PROXY'] = 'http://proxy-server:port'
from duckduckgo_search import DDGS
print(DDGS().text('test'))
"
```

### systemd 服务（Linux 服务器）

创建服务文件：
```bash
sudo nano /etc/systemd/system/search-mcp.service
```

内容：
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

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable search-mcp
sudo systemctl start search-mcp
sudo systemctl status search-mcp
```

---

## 🧪 测试

### 测试工具调用

```bash
# 网页搜索
python3 -c "
from search_mcp import web_search
results = web_search('Python 教程', 3)
for r in results:
    print(f\"- {r['title']}\")
    print(f\"  {r['url']}\")
"

# 新闻搜索
python3 -c "
from search_mcp import news_search
results = news_search('AI 新闻', 3)
for r in results:
    print(f\"- {r['title']} ({r['date']})\")
"

# 搜索摘要
python3 -c "
from search_mcp import search_summary
print(search_summary('MCP 教程'))
"
```

### 测试 MCP 连接

```bash
# 使用 mcp 客户端工具
mcp list-tools search
mcp call web_search --query "测试" --max_results 3
```

---

## ❓ 故障排除

### 问题 1：依赖安装失败

```bash
# 升级 pip
pip3 install --upgrade pip

# 使用国内镜像
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 2：DuckDuckGo 无法访问

```bash
# 检查网络
curl -I https://duckduckgo.com

# 使用代理
export HTTPS_PROXY=http://proxy:port
python3 search_mcp.py

# 或切换到其他搜索引擎（需要修改代码）
```

### 问题 3：MCP 客户端无法连接

```bash
# 检查脚本权限
chmod +x ~/.local/search-mcp/search_mcp.py

# 测试直接运行
python3 ~/.local/search-mcp/search_mcp.py

# 查看日志
tail -f ~/.local/search-mcp/mcp.log
```

### 问题 4：搜索结果不准确

- 尝试使用英文关键词
- 增加 `max_results` 参数
- 使用更具体的搜索词
- 考虑使用付费 API（Google Custom Search 等）

---

## 📦 卸载

```bash
# 删除安装目录
rm -rf ~/.local/search-mcp

# 删除配置（可选）
# 编辑 MCP 客户端配置，移除 search 服务器配置

# 删除 systemd 服务（如果安装了）
sudo systemctl stop search-mcp
sudo systemctl disable search-mcp
sudo rm /etc/systemd/system/search-mcp.service
```

---

## 📚 相关资源

- [MCP 官方文档](https://modelcontextprotocol.io)
- [DuckDuckGo Search API](https://pypi.org/project/ddgs/)
- [Claude Desktop 配置](https://claude.ai/desktop)
- [本项目源码](https://github.com/your-repo/search-mcp)

---

**版本**: 1.0.0  
**更新日期**: 2026-02-21  
**作者**: elok
