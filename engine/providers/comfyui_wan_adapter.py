"""
engine/providers/comfyui_wan_adapter.py
阿里开源 Wan 2.1 (Wan-Video) + ComfyUI 本地/远程工作流适配器
针对真人实拍高保真、无伪影运动与极致性价比私有化算力
"""

import os
import json
import time
import urllib.request
import urllib.error
from ..adapter_base import BaseVideoAdapter, VideoTask, TaskStatus, ProviderCapabilities

class ComfyUIWanAdapter(BaseVideoAdapter):
    def __init__(self, host: str = "http://127.0.0.1:8188"):
        super().__init__(
            provider_id="comfyui_wan21",
            name="阿里 Wan 2.1 (ComfyUI 本地私有化算力)",
            capabilities=ProviderCapabilities(
                supports_t2v=True,
                supports_i2v=True,
                supports_first_last_frame=True,
                supports_camera_control=True,
                max_duration=8,
                recommended_for="真人实拍高保真、微表情连续性、零成本私有化跑片"
            )
        )
        self.host = os.environ.get("COMFYUI_HOST", host).rstrip("/")

    def is_configured(self) -> bool:
        """检查本地 ComfyUI 8188 端口是否处于存活状态"""
        try:
            req = urllib.request.Request(f"{self.host}/system_stats", headers={"User-Agent": "MuseEngine/1.0"})
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                return resp.status == 200
        except Exception:
            return False

    def submit_task(self, task: VideoTask) -> str:
        if not self.is_configured():
            # 若本地尚未启动 ComfyUI，退回到挂起提示状态
            task.status = TaskStatus.FAILED
            task.error_message = f"未检测到本地 ComfyUI 服务 ({self.host})，请确认已启动并加载 Wan 2.1 节点。"
            self.tasks[task.task_id] = task
            return task.task_id

        # 真实环境构造 ComfyUI API Prompt payload:
        # prompt_payload = {"prompt": wan_workflow_json, "client_id": task.task_id}
        # post 到 /prompt 接口
        task.status = TaskStatus.PROCESSING
        task.progress = 10.0
        self.tasks[task.task_id] = task
        return task.task_id

    def query_status(self, task_id: str) -> VideoTask:
        task = self.tasks.get(task_id)
        if not task:
            raise KeyError(f"Task {task_id} not found")
        # 轮询 ComfyUI /history/{prompt_id}
        task.updated_at = time.time()
        return task
