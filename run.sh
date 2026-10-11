#!/usr/bin/env bash
# ==========================================================
# Muse & AI 视频专业提示词工坊 · 一键极速启动脚本 (macOS / Linux)
# ==========================================================

PORT=8080
echo "=========================================================="
echo "🎬 启动 Muse 视频专业提示词工坊 · Studio Max 旗舰版"
echo "=========================================================="

if command -v docker &> /dev/null && docker info &> /dev/null; then
    echo "📦 检测到 Docker 环境，使用 Docker Compose 一键启动..."
    docker compose up -d --build
    echo "✅ Docker 容器已在后台运行！端口: $PORT"
elif command -v python3 &> /dev/null; then
    echo "🐍 使用 Python3 本地极速服务器启动..."
    echo "🌐 服务地址: http://localhost:$PORT"
    python3 -m http.server $PORT --bind 0.0.0.0
elif command -v npx &> /dev/null; then
    echo "🟢 使用 Node.js 本地服务器启动..."
    npx --yes serve -l $PORT .
else
    echo "⚠️ 正在使用默认浏览器直接打开 index.html..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open index.html
    else
        xdg-open index.html
    fi
    exit 0
fi

if [[ "$OSTYPE" == "darwin"* ]]; then
    sleep 1 && open "http://localhost:$PORT" &
fi
