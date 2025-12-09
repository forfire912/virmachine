#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CPU模型实现

支持国产CPU模型构建，包括但不限于龙芯系列、飞腾系列等处理器模型构建
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass, field

from virmachine.models import BaseModel, ModelConfig, ModelType, registry


class CPUArchitecture(Enum):
    """CPU架构类型"""
    X86_64 = "x86_64"
    ARM64 = "arm64"
    LOONGARCH = "loongarch"  # 龙芯架构
    MIPS = "mips"
    RISC_V = "riscv"


class DomesticCPUType(Enum):
    """国产CPU类型"""
    LOONGSON_3A5000 = "loongson_3a5000"  # 龙芯3A5000
    LOONGSON_3C5000 = "loongson_3c5000"  # 龙芯3C5000
    PHYTIUM_FT2000 = "phytium_ft2000"    # 飞腾FT-2000
    PHYTIUM_FT2500 = "phytium_ft2500"    # 飞腾FT-2500
    ZHAOXIN_KX6000 = "zhaoxin_kx6000"    # 兆芯KX-6000
    HYGON_C86 = "hygon_c86"              # 海光C86


@dataclass
class CPUConfig(ModelConfig):
    """CPU模型配置"""
    architecture: CPUArchitecture = CPUArchitecture.X86_64
    domestic_type: Optional[DomesticCPUType] = None
    num_cores: int = 1
    clock_speed_mhz: float = 2000.0
    cache_l1_kb: int = 32
    cache_l2_kb: int = 256
    cache_l3_kb: int = 2048
    features: List[str] = field(default_factory=list)


class CPUModel(BaseModel):
    """CPU模型实现"""
    
    def __init__(self, config: CPUConfig):
        super().__init__(config)
        self.config: CPUConfig = config
        self.registers: Dict[str, int] = {}
        self.instruction_count = 0
        self.cycle_count = 0
        self.running = False
    
    def initialize(self) -> bool:
        """初始化CPU模型"""
        try:
            # 初始化寄存器
            self._init_registers()
            
            # 设置初始状态
            self.state = {
                "running": False,
                "instruction_count": 0,
                "cycle_count": 0,
                "pc": 0,  # 程序计数器
                "registers": self.registers.copy(),
            }
            
            self._initialized = True
            return True
        except Exception as e:
            print(f"CPU initialization failed: {e}")
            return False
    
    def _init_registers(self) -> None:
        """初始化寄存器"""
        # 根据架构初始化不同的寄存器
        if self.config.architecture == CPUArchitecture.LOONGARCH:
            # 龙芯架构寄存器
            for i in range(32):
                self.registers[f"r{i}"] = 0
        elif self.config.architecture == CPUArchitecture.X86_64:
            # x86_64通用寄存器
            for reg in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rsp", "rbp"]:
                self.registers[reg] = 0
        elif self.config.architecture == CPUArchitecture.ARM64:
            # ARM64寄存器
            for i in range(31):
                self.registers[f"x{i}"] = 0
            self.registers["sp"] = 0
            self.registers["pc"] = 0
    
    def reset(self) -> None:
        """重置CPU状态"""
        self.instruction_count = 0
        self.cycle_count = 0
        self.running = False
        for reg in self.registers:
            self.registers[reg] = 0
    
    def update(self, delta_time: float) -> None:
        """更新CPU状态"""
        if self.running:
            # 根据时钟频率计算执行的周期数
            cycles = int(delta_time * self.config.clock_speed_mhz * 1000)
            self.cycle_count += cycles
            # 简化模拟：假设每条指令1个周期
            self.instruction_count += cycles
    
    def get_state(self) -> Dict[str, Any]:
        """获取当前状态"""
        return {
            "running": self.running,
            "instruction_count": self.instruction_count,
            "cycle_count": self.cycle_count,
            "registers": self.registers.copy(),
            "config": {
                "architecture": self.config.architecture.value,
                "domestic_type": self.config.domestic_type.value if self.config.domestic_type else None,
                "num_cores": self.config.num_cores,
                "clock_speed_mhz": self.config.clock_speed_mhz,
            }
        }
    
    def set_state(self, state: Dict[str, Any]) -> None:
        """设置状态"""
        if "running" in state:
            self.running = state["running"]
        if "instruction_count" in state:
            self.instruction_count = state["instruction_count"]
        if "cycle_count" in state:
            self.cycle_count = state["cycle_count"]
        if "registers" in state:
            self.registers.update(state["registers"])
    
    def execute_instruction(self, instruction: str) -> None:
        """执行指令（模拟）"""
        self.instruction_count += 1
        self.cycle_count += 1
    
    def start(self) -> None:
        """启动CPU"""
        self.running = True
    
    def stop(self) -> None:
        """停止CPU"""
        self.running = False


# 注册CPU模型
def _init_cpu_models():
    """初始化并注册CPU模型"""
    registry.register("cpu", CPUModel)
    
    # 可以注册更多CPU变体
    # registry.register("loongson_cpu", LoongsonCPUModel)
    # registry.register("phytium_cpu", PhytiumCPUModel)


_init_cpu_models()


__all__ = [
    "CPUArchitecture",
    "DomesticCPUType",
    "CPUConfig",
    "CPUModel",
]
