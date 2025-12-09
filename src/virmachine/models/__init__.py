#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数字体模型库 (Digital Prototype Model Library)

提供多种数字体模型库，包括CPU、内存、寄存器、串口、网口等模型
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, field


class ModelType(Enum):
    """模型类型枚举"""
    CPU = "cpu"
    MEMORY = "memory"
    REGISTER = "register"
    SERIAL_PORT = "serial_port"
    NETWORK_PORT = "network_port"
    BUS = "bus"
    INTERRUPT_CONTROLLER = "interrupt_controller"


@dataclass
class ModelConfig:
    """模型配置基类"""
    name: str
    model_type: ModelType
    properties: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseModel(ABC):
    """数字体模型基类"""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.state: Dict[str, Any] = {}
        self._initialized = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """初始化模型"""
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """重置模型状态"""
        pass
    
    @abstractmethod
    def update(self, delta_time: float) -> None:
        """更新模型状态"""
        pass
    
    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """获取当前状态"""
        pass
    
    @abstractmethod
    def set_state(self, state: Dict[str, Any]) -> None:
        """设置状态"""
        pass
    
    def is_initialized(self) -> bool:
        """检查是否已初始化"""
        return self._initialized


class ModelRegistry:
    """模型注册表"""
    
    def __init__(self):
        self._models: Dict[str, type] = {}
    
    def register(self, model_type: str, model_class: type) -> None:
        """注册模型类"""
        if not issubclass(model_class, BaseModel):
            raise ValueError(f"Model class must inherit from BaseModel")
        self._models[model_type] = model_class
    
    def create(self, model_type: str, config: ModelConfig) -> BaseModel:
        """创建模型实例"""
        if model_type not in self._models:
            raise ValueError(f"Unknown model type: {model_type}")
        return self._models[model_type](config)
    
    def list_models(self) -> List[str]:
        """列出所有注册的模型类型"""
        return list(self._models.keys())


# 全局模型注册表
registry = ModelRegistry()


__all__ = [
    "ModelType",
    "ModelConfig",
    "BaseModel",
    "ModelRegistry",
    "registry",
]
