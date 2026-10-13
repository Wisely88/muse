"""
engine/registry.py
统一视频模型适配器注册中心与管理网关
"""

from typing import Dict, List, Optional
from .adapter_base import BaseVideoAdapter
from .providers.mock_adapter import MockLocalAdapter
from .providers.gemini_veo_adapter import GeminiVeoAdapter
from .providers.comfyui_wan_adapter import ComfyUIWanAdapter
from .providers.kling_adapter import KlingVideoAdapter

class AdapterRegistry:
    def __init__(self):
        self._adapters: Dict[str, BaseVideoAdapter] = {}
        self._default_provider_id = "mock_simulator"
        self._init_builtin_adapters()

    def _init_builtin_adapters(self):
        # 注册开箱即用的官方与本地插件
        self.register(MockLocalAdapter())
        self.register(GeminiVeoAdapter())
        self.register(ComfyUIWanAdapter())
        self.register(KlingVideoAdapter())

    def register(self, adapter: BaseVideoAdapter):
        self._adapters[adapter.provider_id] = adapter

    def get(self, provider_id: str) -> Optional[BaseVideoAdapter]:
        return self._adapters.get(provider_id)

    def list_providers(self) -> List[dict]:
        res = []
        for pid, ad in self._adapters.items():
            res.append({
                "id": pid,
                "name": ad.name,
                "is_configured": ad.is_configured(),
                "capabilities": {
                    "supports_t2v": ad.capabilities.supports_t2v,
                    "supports_i2v": ad.capabilities.supports_i2v,
                    "supports_first_last_frame": ad.capabilities.supports_first_last_frame,
                    "supports_camera_control": ad.capabilities.supports_camera_control,
                    "max_duration": ad.capabilities.max_duration,
                    "recommended_for": ad.capabilities.recommended_for
                }
            })
        return res

# 单例全局网关
gateway_registry = AdapterRegistry()
