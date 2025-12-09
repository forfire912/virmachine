#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
内存模型实现
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass

from virmachine.models import BaseModel, ModelConfig, ModelType, registry


@dataclass
class MemoryConfig(ModelConfig):
    """内存模型配置"""
    size_mb: int = 1024
    access_time_ns: float = 10.0
    data_width: int = 64  # 数据总线宽度（位）


class MemoryModel(BaseModel):
    """内存模型实现"""
    
    def __init__(self, config: MemoryConfig):
        super().__init__(config)
        self.config: MemoryConfig = config
        self.memory: bytearray = bytearray()
        self.access_count = 0
    
    def initialize(self) -> bool:
        """初始化内存"""
        try:
            # 分配内存空间
            size_bytes = self.config.size_mb * 1024 * 1024
            self.memory = bytearray(size_bytes)
            
            self.state = {
                "size_mb": self.config.size_mb,
                "access_count": 0,
                "used_bytes": 0,
            }
            
            self._initialized = True
            return True
        except Exception as e:
            print(f"Memory initialization failed: {e}")
            return False
    
    def reset(self) -> None:
        """重置内存"""
        self.memory = bytearray(len(self.memory))
        self.access_count = 0
    
    def update(self, delta_time: float) -> None:
        """更新内存状态"""
        pass  # 内存通常是被动组件，不需要主动更新
    
    def get_state(self) -> Dict[str, Any]:
        """获取当前状态"""
        used_bytes = sum(1 for b in self.memory if b != 0)
        return {
            "size_mb": self.config.size_mb,
            "size_bytes": len(self.memory),
            "access_count": self.access_count,
            "used_bytes": used_bytes,
            "utilization": used_bytes / len(self.memory) if len(self.memory) > 0 else 0,
        }
    
    def set_state(self, state: Dict[str, Any]) -> None:
        """设置状态"""
        if "access_count" in state:
            self.access_count = state["access_count"]
    
    def read(self, address: int, size: int) -> Optional[bytes]:
        """读取内存"""
        if address < 0 or address + size > len(self.memory):
            return None
        
        self.access_count += 1
        return bytes(self.memory[address:address + size])
    
    def write(self, address: int, data: bytes) -> bool:
        """写入内存"""
        if address < 0 or address + len(data) > len(self.memory):
            return False
        
        self.access_count += 1
        self.memory[address:address + len(data)] = data
        return True


# 注册内存模型
registry.register("memory", MemoryModel)


__all__ = [
    "MemoryConfig",
    "MemoryModel",
]
