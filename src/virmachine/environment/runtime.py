#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
样机运行环境 (Prototype Runtime Environment)

提供样机运行加载引擎，实现数字样机模型运行周期管理
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass, field
import time

from virmachine.models import BaseModel


class RuntimeState(Enum):
    """运行时状态"""
    CREATED = "created"
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class RuntimeConfig:
    """运行时配置"""
    name: str
    target_platform: str = "x86_64"  # 目标平台
    max_models: int = 100
    simulation_speed: float = 1.0  # 仿真速度倍数
    enable_debug: bool = False
    properties: Dict[str, Any] = field(default_factory=dict)


class PrototypeRuntime:
    """样机运行时环境"""
    
    def __init__(self, config: RuntimeConfig):
        self.config = config
        self.state = RuntimeState.CREATED
        self.models: Dict[str, BaseModel] = {}
        self.start_time: Optional[float] = None
        self.elapsed_time: float = 0.0
        self.simulation_time: float = 0.0
        self.update_count: int = 0
    
    def initialize(self) -> bool:
        """初始化运行时环境"""
        try:
            # 初始化所有模型
            for name, model in self.models.items():
                if not model.initialize():
                    print(f"Failed to initialize model: {name}")
                    return False
            
            self.state = RuntimeState.INITIALIZED
            return True
        except Exception as e:
            print(f"Runtime initialization failed: {e}")
            self.state = RuntimeState.ERROR
            return False
    
    def add_model(self, name: str, model: BaseModel) -> None:
        """添加模型到运行时"""
        if len(self.models) >= self.config.max_models:
            raise ValueError(f"Maximum models limit reached: {self.config.max_models}")
        
        if name in self.models:
            raise ValueError(f"Model {name} already exists")
        
        self.models[name] = model
    
    def remove_model(self, name: str) -> None:
        """从运行时移除模型"""
        if name in self.models:
            del self.models[name]
    
    def get_model(self, name: str) -> Optional[BaseModel]:
        """获取模型"""
        return self.models.get(name)
    
    def start(self) -> bool:
        """启动运行时"""
        if self.state not in [RuntimeState.INITIALIZED, RuntimeState.PAUSED]:
            print(f"Cannot start runtime in state: {self.state}")
            return False
        
        self.start_time = time.time()
        self.state = RuntimeState.RUNNING
        return True
    
    def pause(self) -> bool:
        """暂停运行时"""
        if self.state != RuntimeState.RUNNING:
            return False
        
        self.state = RuntimeState.PAUSED
        return True
    
    def resume(self) -> bool:
        """恢复运行时"""
        if self.state != RuntimeState.PAUSED:
            return False
        
        self.state = RuntimeState.RUNNING
        return True
    
    def stop(self) -> bool:
        """停止运行时"""
        if self.state not in [RuntimeState.RUNNING, RuntimeState.PAUSED]:
            return False
        
        self.state = RuntimeState.STOPPED
        return True
    
    def update(self, delta_time: float) -> None:
        """更新运行时状态"""
        if self.state != RuntimeState.RUNNING:
            return
        
        # 应用仿真速度
        adjusted_delta = delta_time * self.config.simulation_speed
        
        # 更新所有模型
        for model in self.models.values():
            if model.is_initialized():
                model.update(adjusted_delta)
        
        self.elapsed_time += delta_time
        self.simulation_time += adjusted_delta
        self.update_count += 1
    
    def reset(self) -> None:
        """重置运行时"""
        for model in self.models.values():
            model.reset()
        
        self.start_time = None
        self.elapsed_time = 0.0
        self.simulation_time = 0.0
        self.update_count = 0
        self.state = RuntimeState.INITIALIZED
    
    def get_state(self) -> Dict[str, Any]:
        """获取运行时状态"""
        return {
            "name": self.config.name,
            "state": self.state.value,
            "target_platform": self.config.target_platform,
            "model_count": len(self.models),
            "elapsed_time": self.elapsed_time,
            "simulation_time": self.simulation_time,
            "update_count": self.update_count,
            "simulation_speed": self.config.simulation_speed,
            "models": {
                name: model.get_state() 
                for name, model in self.models.items()
                if model.is_initialized()
            }
        }
    
    def save_snapshot(self) -> Dict[str, Any]:
        """保存运行时快照"""
        return {
            "config": {
                "name": self.config.name,
                "target_platform": self.config.target_platform,
                "simulation_speed": self.config.simulation_speed,
            },
            "state": self.state.value,
            "elapsed_time": self.elapsed_time,
            "simulation_time": self.simulation_time,
            "models": {
                name: {
                    "type": type(model).__name__,
                    "state": model.get_state()
                }
                for name, model in self.models.items()
            }
        }
    
    def load_snapshot(self, snapshot: Dict[str, Any]) -> bool:
        """从快照恢复运行时"""
        try:
            self.elapsed_time = snapshot.get("elapsed_time", 0.0)
            self.simulation_time = snapshot.get("simulation_time", 0.0)
            
            # 恢复模型状态
            model_states = snapshot.get("models", {})
            for name, model_data in model_states.items():
                if name in self.models:
                    self.models[name].set_state(model_data["state"])
            
            return True
        except Exception as e:
            print(f"Failed to load snapshot: {e}")
            return False


class RuntimeEngine:
    """运行时引擎，管理多个运行时实例"""
    
    def __init__(self):
        self.runtimes: Dict[str, PrototypeRuntime] = {}
        self.active_runtime: Optional[str] = None
    
    def create_runtime(self, config: RuntimeConfig) -> PrototypeRuntime:
        """创建新的运行时实例"""
        if config.name in self.runtimes:
            raise ValueError(f"Runtime {config.name} already exists")
        
        runtime = PrototypeRuntime(config)
        self.runtimes[config.name] = runtime
        
        if self.active_runtime is None:
            self.active_runtime = config.name
        
        return runtime
    
    def get_runtime(self, name: str) -> Optional[PrototypeRuntime]:
        """获取运行时实例"""
        return self.runtimes.get(name)
    
    def remove_runtime(self, name: str) -> bool:
        """移除运行时实例"""
        if name not in self.runtimes:
            return False
        
        runtime = self.runtimes[name]
        runtime.stop()
        del self.runtimes[name]
        
        if self.active_runtime == name:
            self.active_runtime = None
        
        return True
    
    def set_active_runtime(self, name: str) -> bool:
        """设置活动运行时"""
        if name not in self.runtimes:
            return False
        
        self.active_runtime = name
        return True
    
    def get_active_runtime(self) -> Optional[PrototypeRuntime]:
        """获取活动运行时"""
        if self.active_runtime:
            return self.runtimes.get(self.active_runtime)
        return None
    
    def update_all(self, delta_time: float) -> None:
        """更新所有运行时"""
        for runtime in self.runtimes.values():
            runtime.update(delta_time)
    
    def list_runtimes(self) -> List[str]:
        """列出所有运行时"""
        return list(self.runtimes.keys())


__all__ = [
    "RuntimeState",
    "RuntimeConfig",
    "PrototypeRuntime",
    "RuntimeEngine",
]
