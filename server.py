#!/usr/bin/env python3
"""
Muse & AI 视频提示词工坊 - 本地极速启动服务
"""
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 允许跨域与无缓存开发
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    global PORT
    for attempt_port in range(PORT, PORT + 20):
        try:
            with socketserver.TCPServer(("", attempt_port), Handler) as httpd:
                url = f"http://localhost:{attempt_port}"
                print("=" * 60)
                print(f"🎬 Muse & AI 视频提示词工坊 已启动！")
                print(f"🌐 本地访问地址: {url}")
                print(f"💡 双击 index.html 亦可直接在任何现代浏览器中免服务器运行")
                print(f"按 Ctrl+C 可停止本地服务")
                print("=" * 60)
                webbrowser.open(url)
                httpd.serve_forever()
        except OSError:
            continue
    print("❌ 无法绑定可用端口，请直接在浏览器中打开 index.html")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n服务已停止。")
