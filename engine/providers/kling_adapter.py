"""
engine/providers/kling_adapter.py
快手可灵 (Kling AI) 开放平台 API 适配器
用于商业化短剧交付、大动态动作与首尾帧精准闭环
"""

import os
import time
from ..adapter_base import BaseVideoAdapter, VideoTask, TaskStatus, ProviderCapabilities

class KlingVideoAdapter(BaseVideoAdapter):
    def __init__(self):
        super().__init__(
            provider_id="kling_ai",
            name="快手可灵 (Kling 1.5/2.0 API)",
            capabilities=ProviderCapabilities(
                supports_t2v=True,
                supports_i2v=True,
                supports_first_last_frame=True,
                supports_camera_control=True,
                max_duration=10,
                recommended_for="影视短剧商业交付、人物大幅度肢体动作、首尾帧拼接"
            )
        )
        self.access_key = os.environ.get("KLING_ACCESS_KEY")
        self.secret_key = os.environ.get("KLING_SECRET_KEY")

    def is_configured(self) -> bool:
        return bool(self.access_key and self.secret_key)

    def submit_task(self, task: VideoTask) -> str:
        if not self.is_configured():
            task.status = TaskStatus.FAILED
            task.error_message = "未配置 KLING_ACCESS_KEY / KLING_SECRET_KEY 凭证。"
            self.tasks[task.task_id] = task
            return task.task_id

        task.status = TaskStatus.PROCESSING
        task.progress = 5.0
        self.tasks[task.task_id] = task
        return task.task_id

    def query_status(self, task_id: str) -> VideoTask:
        task = self.tasks.get(task_id)
        if not task:
            raise KeyError(f"Task {task_id} not found")
        task.updated_at = time.time()
        return task
