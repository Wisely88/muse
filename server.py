#!/usr/bin/env python3
"""
Muse & AI 视频工业级生产中枢服务 (Muse-Director Hub)
集成静态前端工作台 + 统一多模型生成 API 网关 (Gemini / Veo / Wan2.1 / Kling / Mock)
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import json
import uuid
import urllib.parse

from engine.registry import gateway_registry
from engine.director_agent import GeminiDirectorAgent
from engine.adapter_base import VideoTask, TaskStatus
from engine.assembler import VideoAssembler

PORT = 8080
director_agent = GeminiDirectorAgent()

class MuseGatewayHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def _send_json(self, data, status_code=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        content_len = int(self.headers.get('Content-Length', 0))
        if content_len <= 0:
            return {}
        raw = self.rfile.read(content_len)
        try:
            return json.loads(raw.decode('utf-8'))
        except Exception:
            return {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # API: 列出当前注册的所有模型生成工具
        if path == "/api/providers":
            providers = gateway_registry.list_providers()
            self._send_json({"status": "success", "providers": providers})
            return

        # API: 查询指定任务或全部任务状态
        if path == "/api/render/status":
            query = urllib.parse.parse_qs(parsed.query)
            provider_id = query.get("provider", ["mock_simulator"])[0]
            task_id = query.get("task_id", [None])[0]

            adapter = gateway_registry.get(provider_id)
            if not adapter:
                self._send_json({"status": "error", "message": f"未找到模型适配器: {provider_id}"}, 404)
                return

            if task_id:
                try:
                    task = adapter.query_status(task_id)
                    self._send_json({
                        "status": "success",
                        "task": {
                            "task_id": task.task_id,
                            "status": task.status.value,
                            "progress": task.progress,
                            "video_url": task.video_url,
                            "error": task.error_message
                        }
                    })
                except KeyError:
                    self._send_json({"status": "error", "message": "任务不存在"}, 404)
            else:
                # 返回所有任务
                tasks_info = []
                for tid in list(adapter.tasks.keys()):
                    t = adapter.query_status(tid)
                    tasks_info.append({
                        "task_id": t.task_id,
                        "status": t.status.value,
                        "progress": t.progress,
                        "video_url": t.video_url
                    })
                self._send_json({"status": "success", "tasks": tasks_info})
            return

        # 其他请求交由静态文件处理器
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self._read_json_body()

        # API: 调用 Gemini 智能导演扩写分镜台账
        if path == "/api/director/script":
            topic = body.get("topic", "").strip()
            if not topic:
                self._send_json({"status": "error", "message": "topic 不能为空"}, 400)
                return
            shot_count = int(body.get("shot_count", 5))
            style = body.get("style", "cinematic")
            storyboard = director_agent.expand_topic_to_storyboard(topic, shot_count, style)
            self._send_json({"status": "success", "storyboard": storyboard})
            return

        # API: 提交渲染任务
        if path == "/api/render/submit":
            provider_id = body.get("provider", "mock_simulator")
            shots = body.get("shots", [])

            adapter = gateway_registry.get(provider_id)
            if not adapter:
                self._send_json({"status": "error", "message": f"未知的生成引擎: {provider_id}"}, 400)
                return

            created_tasks = []
            for s in shots:
                tid = f"shot_{s.get('index', 1)}_{uuid.uuid4().hex[:6]}"
                task = VideoTask(
                    task_id=tid,
                    prompt=s.get("prompt_en", ""),
                    aspect_ratio=s.get("aspect_ratio", "16:9"),
                    duration_seconds=float(s.get("duration", 4.5)),
                    model_name=provider_id
                )
                adapter.submit_task(task)
                created_tasks.append({
                    "task_id": tid,
                    "index": s.get("index", 1),
                    "prompt": task.prompt
                })

            self._send_json({"status": "success", "provider": provider_id, "tasks": created_tasks})
            return

        # API: 全片自动化串联装配
        if path == "/api/render/assemble":
            video_files = body.get("video_files", [])
            output_name = body.get("output_name", "final_film.mp4")
            out_dir = os.path.expanduser("~/muse/output")
            os.makedirs(out_dir, exist_ok=True)
            output_path = os.path.join(out_dir, output_name)

            success = VideoAssembler.concatenate_shots(video_files, output_path)
            if success:
                self._send_json({
                    "status": "success",
                    "video_url": f"/output/{output_name}",
                    "local_path": output_path
                })
            else:
                self._send_json({"status": "error", "message": "视频合成失败，请检查输入片段是否存在。"}, 500)
            return

        self._send_json({"status": "error", "message": "Not Found"}, 404)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    global PORT
    for attempt_port in range(PORT, PORT + 20):
        try:
            with socketserver.TCPServer(("", attempt_port), MuseGatewayHandler) as httpd:
                url = f"http://localhost:{attempt_port}"
                print("=" * 65)
                print(f"🎬 Muse-Director 工业级多模型视频生产中枢已启动！")
                print(f"🌐 统一管理与工作台地址: {url}")
                print(f"🔌 支持的引擎适配器: {', '.join([p['name'] for p in gateway_registry.list_providers()])}")
                print(f"⚡ 支持端点: /api/providers, /api/director/script, /api/render/submit")
                print("=" * 65)
                httpd.serve_forever()
        except OSError:
            continue
    print("❌ 无法绑定可用端口")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n中枢服务已安全停止。")
