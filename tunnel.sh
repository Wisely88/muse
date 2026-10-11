#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# 杀掉残留的 8080 端口与旧 cloudflared 进程
killall -9 cloudflared 2>/dev/null
lsof -ti:8080 | xargs kill -9 2>/dev/null
sleep 1

# 启动本地 Web 服务器 (0.0.0.0 允许同一局域网访问)
python3 -m http.server 8080 --bind 0.0.0.0 > server.log 2>&1 &
SERVER_PID=$!
echo "Local server started with PID $SERVER_PID on 0.0.0.0:8080"

# 强制使用 HTTP/2 (TCP) 协议，彻底解决国内网络环境下 QUIC (UDP) 超时断联与 Error 1033
/opt/homebrew/bin/cloudflared tunnel --protocol http2 --url http://127.0.0.1:8080 2>&1 | tee tunnel.log
