#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
总线模型库 (Bus Model Library)

提供样机总线模型库，完成对设备之间通信业务模拟
总线型号包括FC、RS422、429等总线业务模拟
"""

from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
from queue import Queue
import time
import random

from virmachine.models import BaseModel, ModelConfig, ModelType, registry


class BusType(Enum):
    """总线类型"""
    FC = "fc"              # Fibre Channel 光纤通道
    RS422 = "rs422"        # RS-422串行总线
    ARINC429 = "arinc429"  # ARINC 429航空总线
    CAN = "can"            # CAN总线
    ETHERNET = "ethernet"  # 以太网
    PCI = "pci"            # PCI总线
    I2C = "i2c"            # I2C总线


@dataclass
class BusConfig(ModelConfig):
    """总线模型配置"""
    bus_type: BusType = BusType.ETHERNET
    bandwidth_mbps: float = 100.0
    max_devices: int = 16
    protocol_version: str = "1.0"
    error_rate: float = 0.0  # 错误率（0-1）


@dataclass
class BusMessage:
    """总线消息"""
    source: str
    destination: str
    data: bytes
    timestamp: float = field(default_factory=time.time)
    priority: int = 0
    message_id: Optional[int] = None


class BusDevice:
    """总线设备抽象"""
    
    def __init__(self, device_id: str):
        self.device_id = device_id
        self.rx_queue: Queue = Queue()
        self.tx_queue: Queue = Queue()
        self.message_handler: Optional[Callable[[BusMessage], None]] = None
    
    def send(self, message: BusMessage) -> None:
        """发送消息"""
        self.tx_queue.put(message)
    
    def receive(self) -> Optional[BusMessage]:
        """接收消息"""
        if not self.rx_queue.empty():
            return self.rx_queue.get()
        return None
    
    def set_message_handler(self, handler: Callable[[BusMessage], None]) -> None:
        """设置消息处理器"""
        self.message_handler = handler


class BusModel(BaseModel):
    """总线模型实现"""
    
    def __init__(self, config: BusConfig):
        super().__init__(config)
        self.config: BusConfig = config
        self.devices: Dict[str, BusDevice] = {}
        self.message_count = 0
        self.error_count = 0
        self.total_bytes = 0
    
    def initialize(self) -> bool:
        """初始化总线"""
        try:
            self.state = {
                "bus_type": self.config.bus_type.value,
                "bandwidth_mbps": self.config.bandwidth_mbps,
                "device_count": 0,
                "message_count": 0,
                "error_count": 0,
                "total_bytes": 0,
            }
            
            self._initialized = True
            return True
        except Exception as e:
            print(f"Bus initialization failed: {e}")
            return False
    
    def reset(self) -> None:
        """重置总线"""
        self.devices.clear()
        self.message_count = 0
        self.error_count = 0
        self.total_bytes = 0
    
    def update(self, delta_time: float) -> None:
        """更新总线状态，处理消息传输"""
        # 处理所有设备的发送队列
        for device_id, device in self.devices.items():
            while not device.tx_queue.empty():
                message = device.tx_queue.get()
                self._route_message(message)
    
    def _route_message(self, message: BusMessage) -> None:
        """路由消息到目标设备"""
        self.message_count += 1
        self.total_bytes += len(message.data)
        
        # 模拟错误率
        if random.random() < self.config.error_rate:
            self.error_count += 1
            return
        
        # 根据目标地址路由
        if message.destination == "broadcast":
            # 广播消息
            for device_id, device in self.devices.items():
                if device_id != message.source:
                    device.rx_queue.put(message)
                    if device.message_handler:
                        device.message_handler(message)
        elif message.destination in self.devices:
            # 点对点消息
            device = self.devices[message.destination]
            device.rx_queue.put(message)
            if device.message_handler:
                device.message_handler(message)
    
    def get_state(self) -> Dict[str, Any]:
        """获取当前状态"""
        return {
            "bus_type": self.config.bus_type.value,
            "bandwidth_mbps": self.config.bandwidth_mbps,
            "device_count": len(self.devices),
            "message_count": self.message_count,
            "error_count": self.error_count,
            "total_bytes": self.total_bytes,
            "error_rate": self.error_count / self.message_count if self.message_count > 0 else 0,
        }
    
    def set_state(self, state: Dict[str, Any]) -> None:
        """设置状态"""
        if "message_count" in state:
            self.message_count = state["message_count"]
        if "error_count" in state:
            self.error_count = state["error_count"]
        if "total_bytes" in state:
            self.total_bytes = state["total_bytes"]
    
    def attach_device(self, device_id: str) -> BusDevice:
        """连接设备到总线"""
        if len(self.devices) >= self.config.max_devices:
            raise ValueError(f"Bus full: max {self.config.max_devices} devices")
        
        if device_id in self.devices:
            raise ValueError(f"Device {device_id} already attached")
        
        device = BusDevice(device_id)
        self.devices[device_id] = device
        return device
    
    def detach_device(self, device_id: str) -> None:
        """从总线分离设备"""
        if device_id in self.devices:
            del self.devices[device_id]


# 特定总线类型的实现

class RS422BusModel(BusModel):
    """RS-422总线模型"""
    
    def __init__(self, config: BusConfig):
        config.bus_type = BusType.RS422
        config.bandwidth_mbps = 10.0  # RS-422典型速率
        config.max_devices = 10
        super().__init__(config)


class ARINC429BusModel(BusModel):
    """ARINC 429航空总线模型"""
    
    def __init__(self, config: BusConfig):
        config.bus_type = BusType.ARINC429
        config.bandwidth_mbps = 0.1  # ARINC 429为低速或高速（12.5或100 kbps）
        config.max_devices = 20
        super().__init__(config)


class FCBusModel(BusModel):
    """光纤通道(FC)总线模型"""
    
    def __init__(self, config: BusConfig):
        config.bus_type = BusType.FC
        config.bandwidth_mbps = 1000.0  # FC典型速率
        config.max_devices = 127
        super().__init__(config)


# 注册总线模型
registry.register("bus", BusModel)
registry.register("rs422_bus", RS422BusModel)
registry.register("arinc429_bus", ARINC429BusModel)
registry.register("fc_bus", FCBusModel)


__all__ = [
    "BusType",
    "BusConfig",
    "BusMessage",
    "BusDevice",
    "BusModel",
    "RS422BusModel",
    "ARINC429BusModel",
    "FCBusModel",
]
