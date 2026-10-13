"""
engine/adapter_base.py
统一视频生成模型适配器抽象基类与通用数据规范
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional, List
import time
import uuid

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class VideoTask:
    task_id: str
    prompt: str
    negative_prompt: str = ""
    aspect_ratio: str = "16:9"
    duration_seconds: float = 4.5
    image_url: Optional[str] = None  # 首帧或角色参考图 (I2V / Ref)
    model_name: str = ""
    extra_params: Dict[str, Any] = field(default_factory=dict)
    
    # 状态与产物
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0
    video_url: Optional[str] = None
    local_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

@dataclass
class ProviderCapabilities:
    supports_t2v: bool = True           # 支持文生视频
    supports_i2v: bool = True           # 支持图生视频 (首帧引导)
    supports_first_last_frame: bool = False  # 支持首尾帧过渡
    supports_camera_control: bool = True     # 支持运镜参数
    max_duration: int = 10              # 单段最长时间
    recommended_for: str = "通用"        # 推荐场景 (真人/写实/动漫/大动作)

class BaseVideoAdapter(ABC):
    """
    所有视频生成工具/模型必须实现的抽象协议接口
    支持热插拔、统一状态轮询与异步生成
    """
    
    def __init__(self, provider_id: str, name: str, capabilities: ProviderCapabilities):
        self.provider_id = provider_id
        self.name = name
        self.capabilities = capabilities
        self.tasks: Dict[str, VideoTask] = {}

    @abstractmethod
    def is_configured(self) -> bool:
        """检查必要的环境变量、API Key 或本地服务端口是否可用"""
        pass

    @abstractmethod
    def submit_task(self, task: VideoTask) -> str:
        """提交视频生成任务，返回 task_id"""
        pass

    @abstractmethod
    def query_status(self, task_id: str) -> VideoTask:
        """查询任务状态并更新"""
        pass

    def cancel_task(self, task_id: str) -> bool:
        """取消任务（可选）"""
        return False
