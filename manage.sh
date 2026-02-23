#!/bin/bash
# 搜索 MCP 服务器启动脚本

SERVICE_NAME="search-mcp"
SCRIPT_PATH="/root/.openclaw/workspace/mcp-search-server/search_mcp.py"
LOG_DIR="/root/.openclaw/workspace/logs"
PID_FILE="/var/run/${SERVICE_NAME}.pid"
PORT=8765

case "$1" in
    start)
        echo "启动搜索 MCP 服务器..."
        mkdir -p $LOG_DIR
        nohup python3 $SCRIPT_PATH --transport http --port $PORT \
            > $LOG_DIR/search_mcp.log 2>&1 &
        echo $! > $PID_FILE
        echo "✅ 搜索 MCP 服务器已启动 (端口 $PORT)"
        echo "📋 日志：tail -f $LOG_DIR/search_mcp.log"
        ;;
    
    stop)
        echo "停止搜索 MCP 服务器..."
        if [ -f $PID_FILE ]; then
            kill $(cat $PID_FILE) 2>/dev/null
            rm -f $PID_FILE
            echo "✅ 已停止"
        else
            pkill -f search_mcp.py
            echo "✅ 已停止 (通过进程名)"
        fi
        ;;
    
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    
    status)
        if pgrep -f search_mcp.py > /dev/null; then
            echo "✅ 运行中"
            pgrep -af search_mcp.py
        else
            echo "❌ 未运行"
        fi
        ;;
    
    log)
        tail -f $LOG_DIR/search_mcp.log
        ;;
    
    *)
        echo "用法：$0 {start|stop|restart|status|log}"
        exit 1
        ;;
esac
