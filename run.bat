@echo off
chcp 65001 >nul
title Muse 视频专业提示词工坊 - 一键启动

echo ==========================================================
echo  🎬 Muse 视频专业提示词工坊 · Studio Max 旗舰版
echo ==========================================================

set PORT=8080

where python >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] 检测到 Python 环境，正在启动本地服务端口 %PORT%...
    start http://localhost:%PORT%
    python -m http.server %PORT%
    goto end
)

where docker >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] 检测到 Docker 环境，正在使用 Docker Compose 启动...
    docker compose up -d --build
    start http://localhost:%PORT%
    echo 容器已启动完成！
    goto end
)

echo [提示] 正在使用默认浏览器直接打开离线网页...
start index.html

:end
pause
