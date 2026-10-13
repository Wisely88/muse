"""
engine/providers/mock_adapter.py
本地高仿真实体适配器：用于离线演示、自动化测试与架构验证
"""

import time
import os
import subprocess
from ..adapter_base import BaseVideoAdapter, VideoTask, TaskStatus, ProviderCapabilities

class MockLocalAdapter(BaseVideoAdapter):
    """
    仿真适配器：在本地快速模拟视频生成状态流转，并可通过 FFmpeg 动态生成一个带时间码的有效 MP4 片段
    """
    def __init__(self):
        super().__init__(
            provider_id="mock_simulator",
            name="本地离线仿真引擎 (Mock Studio)",
            capabilities=ProviderCapabilities(
                supports_t2v=True,
                supports_i2v=True,
                supports_first_last_frame=True,
                supports_camera_control=True,
                max_duration=10,
                recommended_for="测试与零成本流程验证"
            )
        )

    def is_configured(self) -> bool:
        return True

    def submit_task(self, task: VideoTask) -> str:
        task.status = TaskStatus.PROCESSING
        task.progress = 10.0
        task.updated_at = time.time()
        self.tasks[task.task_id] = task
        return task.task_id

    def query_status(self, task_id: str) -> VideoTask:
        task = self.tasks.get(task_id)
        if not task:
            raise KeyError(f"Task {task_id} not found")

        if task.status == TaskStatus.PROCESSING:
            elapsed = time.time() - task.created_at
            # 模拟 3 秒完成生成
            if elapsed < 3.0:
                task.progress = min(90.0, 10.0 + elapsed * 28.0)
            else:
                task.status = TaskStatus.COMPLETED
                task.progress = 100.0
                
                # 尝试用本地 FFmpeg 生成一个带纯色和时间戳文字的真实 4 秒 MP4 视频
                out_dir = os.path.expanduser("~/muse/output")
                os.makedirs(out_dir, exist_ok=True)
                out_file = os.path.join(out_dir, f"{task.task_id}.mp4")
                
                # 如果 FFmpeg 可用，快速渲染一个轻量测试视频，否则生成占位文件
                try:
                    cmd = [
                        "ffmpeg", "-y", "-f", "lavfi",
                        "-i", f"color=c=0x181824:s=1280x720:d={int(task.duration_seconds)}",
                        "-vf", f"drawtext=text='Muse Shot {task.task_id[:6]} | {task.aspect_ratio}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=(h-text_h)/2",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        out_file
                    ]
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    task.local_path = out_file
                    task.video_url = f"/output/{os.path.basename(out_file)}"
                except Exception:
                    # 容错：写一个空文件标识
                    with open(out_file, "wb") as f:
                        f.write(b"MOCK_VIDEO_DATA")
                    task.local_path = out_file
                    task.video_url = f"/output/{os.path.basename(out_file)}"

        task.updated_at = time.time()
        return task
