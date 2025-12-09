#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
中断控制器模型 (Interrupt Controller)

支持对XX计算执行单元样机中断业务模拟，可设置中断周期与次数
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import time

from virmachine.models import BaseModel, ModelConfig, registry


class InterruptType(Enum):
    """中断类型"""
    HARDWARE = "hardware"    # 硬件中断
    SOFTWARE = "software"    # 软件中断
    EXCEPTION = "exception"  # 异常
    TIMER = "timer"          # 定时器中断
    IO = "io"                # I/O中断


@dataclass
class InterruptConfig(ModelConfig):
    """中断控制器配置"""
    num_vectors: int = 256
    priority_levels: int = 8
    support_nesting: bool = True  # 是否支持中断嵌套


@dataclass
class Interrupt:
    """中断描述"""
    vector: int
    interrupt_type: InterruptType
    priority: int = 0
    handler: Optional[Callable] = None
    enabled: bool = True
    count: int = 0
    timestamp: float = field(default_factory=time.time)


class InterruptController(BaseModel):
    """中断控制器实现"""
    
    def __init__(self, config: InterruptConfig):
        super().__init__(config)
        self.config: InterruptConfig = config
        self.interrupts: Dict[int, Interrupt] = {}
        self.pending_interrupts: List[int] = []
        self.active_interrupt: Optional[int] = None
        self.interrupt_enabled = True
        self.total_interrupts = 0
    
    def initialize(self) -> bool:
        """初始化中断控制器"""
        try:
            # 初始化中断向量表
            for i in range(self.config.num_vectors):
                self.interrupts[i] = Interrupt(
                    vector=i,
                    interrupt_type=InterruptType.HARDWARE,
                    priority=0,
                    enabled=False
                )
            
            self.state = {
                "interrupt_enabled": True,
                "total_interrupts": 0,
                "pending_count": 0,
                "active_interrupt": None,
            }
            
            self._initialized = True
            return True
        except Exception as e:
            print(f"Interrupt controller initialization failed: {e}")
            return False
    
    def reset(self) -> None:
        """重置中断控制器"""
        self.pending_interrupts.clear()
        self.active_interrupt = None
        self.total_interrupts = 0
        for interrupt in self.interrupts.values():
            interrupt.count = 0
    
    def update(self, delta_time: float) -> None:
        """更新中断控制器状态"""
        if not self.interrupt_enabled:
            return
        
        # 处理挂起的中断
        if self.pending_interrupts and self.active_interrupt is None:
            # 按优先级排序
            self.pending_interrupts.sort(
                key=lambda v: self.interrupts[v].priority,
                reverse=True
            )
            
            # 处理最高优先级的中断
            vector = self.pending_interrupts.pop(0)
            self._handle_interrupt(vector)
    
    def _handle_interrupt(self, vector: int) -> None:
        """处理中断"""
        interrupt = self.interrupts[vector]
        self.active_interrupt = vector
        self.total_interrupts += 1
        interrupt.count += 1
        
        # 调用中断处理程序
        if interrupt.handler:
            interrupt.handler(interrupt)
        
        # 中断处理完成
        self.active_interrupt = None
    
    def get_state(self) -> Dict[str, Any]:
        """获取当前状态"""
        return {
            "interrupt_enabled": self.interrupt_enabled,
            "total_interrupts": self.total_interrupts,
            "pending_count": len(self.pending_interrupts),
            "active_interrupt": self.active_interrupt,
            "interrupt_counts": {
                v: i.count for v, i in self.interrupts.items() if i.count > 0
            }
        }
    
    def set_state(self, state: Dict[str, Any]) -> None:
        """设置状态"""
        if "interrupt_enabled" in state:
            self.interrupt_enabled = state["interrupt_enabled"]
        if "total_interrupts" in state:
            self.total_interrupts = state["total_interrupts"]
    
    def register_interrupt(
        self,
        vector: int,
        interrupt_type: InterruptType,
        priority: int,
        handler: Optional[Callable] = None
    ) -> None:
        """注册中断"""
        if vector not in self.interrupts:
            raise ValueError(f"Invalid interrupt vector: {vector}")
        
        interrupt = self.interrupts[vector]
        interrupt.interrupt_type = interrupt_type
        interrupt.priority = priority
        interrupt.handler = handler
        interrupt.enabled = True
    
    def raise_interrupt(self, vector: int) -> None:
        """触发中断"""
        if vector not in self.interrupts:
            raise ValueError(f"Invalid interrupt vector: {vector}")
        
        interrupt = self.interrupts[vector]
        if not interrupt.enabled or not self.interrupt_enabled:
            return
        
        if vector not in self.pending_interrupts:
            self.pending_interrupts.append(vector)
    
    def enable_interrupt(self, vector: int) -> None:
        """启用中断"""
        if vector in self.interrupts:
            self.interrupts[vector].enabled = True
    
    def disable_interrupt(self, vector: int) -> None:
        """禁用中断"""
        if vector in self.interrupts:
            self.interrupts[vector].enabled = False
    
    def enable_all(self) -> None:
        """启用全局中断"""
        self.interrupt_enabled = True
    
    def disable_all(self) -> None:
        """禁用全局中断"""
        self.interrupt_enabled = False


class PeriodicInterruptGenerator:
    """周期性中断生成器"""
    
    def __init__(
        self,
        controller: InterruptController,
        vector: int,
        period_ms: float,
        count: Optional[int] = None
    ):
        """
        Args:
            controller: 中断控制器
            vector: 中断向量
            period_ms: 中断周期（毫秒）
            count: 中断次数（None表示无限）
        """
        self.controller = controller
        self.vector = vector
        self.period_ms = period_ms
        self.max_count = count
        self.current_count = 0
        self.elapsed_time = 0.0
        self.enabled = True
    
    def update(self, delta_time: float) -> None:
        """更新生成器"""
        if not self.enabled:
            return
        
        if self.max_count is not None and self.current_count >= self.max_count:
            return
        
        self.elapsed_time += delta_time * 1000  # 转换为毫秒
        
        while self.elapsed_time >= self.period_ms:
            self.controller.raise_interrupt(self.vector)
            self.current_count += 1
            self.elapsed_time -= self.period_ms
            
            if self.max_count is not None and self.current_count >= self.max_count:
                break
    
    def reset(self) -> None:
        """重置生成器"""
        self.current_count = 0
        self.elapsed_time = 0.0
    
    def enable(self) -> None:
        """启用生成器"""
        self.enabled = True
    
    def disable(self) -> None:
        """禁用生成器"""
        self.enabled = False


# 注册中断控制器模型
registry.register("interrupt_controller", InterruptController)


__all__ = [
    "InterruptType",
    "InterruptConfig",
    "Interrupt",
    "InterruptController",
    "PeriodicInterruptGenerator",
]
