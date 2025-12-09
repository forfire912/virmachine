#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据采集器 (Data Collector)

支持多种数据采集方式，包括按需抽样采集、接近全量实时采集、半流量实时采集
"""

from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import random


class CollectionMode(Enum):
    """采集模式"""
    ON_DEMAND = "on_demand"           # 按需采集
    SAMPLING = "sampling"             # 抽样采集
    FULL_REALTIME = "full_realtime"   # 全量实时采集
    HALF_REALTIME = "half_realtime"   # 半流量实时采集


class DataCategory(Enum):
    """数据分类"""
    NETWORK_TRAFFIC = "network_traffic"
    SYSTEM_METRICS = "system_metrics"
    APPLICATION_LOGS = "application_logs"
    PERFORMANCE_DATA = "performance_data"
    CUSTOM = "custom"


@dataclass
class NetworkTrafficData:
    """网络流量数据"""
    timestamp: datetime
    source_addr: str
    dest_addr: str
    source_port: int
    dest_port: int
    ip_type: str  # IPv4 or IPv6
    protocol: str  # TCP, UDP, etc.
    packet_size: int
    payload: bytes = b""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CollectorConfig:
    """采集器配置"""
    mode: CollectionMode
    category: DataCategory
    sampling_rate: float = 1.0  # 采样率 (0-1)
    buffer_size: int = 1000
    batch_size: int = 100
    enable_compression: bool = False


class DataCollector:
    """数据采集器"""
    
    def __init__(self, config: CollectorConfig):
        self.config = config
        self.buffer: List[Any] = []
        self.collected_count = 0
        self.dropped_count = 0
        self.filters: List[Callable[[Any], bool]] = []
        self.callbacks: List[Callable[[List[Any]], None]] = []
    
    def collect(self, data: Any) -> bool:
        """采集数据"""
        # 根据采集模式决定是否采集
        if not self._should_collect():
            self.dropped_count += 1
            return False
        
        # 应用过滤器
        for filter_func in self.filters:
            if not filter_func(data):
                self.dropped_count += 1
                return False
        
        # 添加到缓冲区
        if len(self.buffer) >= self.config.buffer_size:
            # 缓冲区满，移除最旧的数据
            self.buffer.pop(0)
        
        self.buffer.append(data)
        self.collected_count += 1
        
        # 检查是否需要批量处理
        if len(self.buffer) >= self.config.batch_size:
            self._process_batch()
        
        return True
    
    def _should_collect(self) -> bool:
        """判断是否应该采集"""
        if self.config.mode == CollectionMode.ON_DEMAND:
            return False  # 按需采集需要显式触发
        elif self.config.mode == CollectionMode.FULL_REALTIME:
            return True
        elif self.config.mode in [CollectionMode.SAMPLING, CollectionMode.HALF_REALTIME]:
            return random.random() < self.config.sampling_rate
        return True
    
    def _process_batch(self) -> None:
        """处理批量数据"""
        if not self.buffer:
            return
        
        batch = self.buffer[:self.config.batch_size]
        
        # 调用所有回调函数
        for callback in self.callbacks:
            callback(batch)
        
        # 清空已处理的数据
        self.buffer = self.buffer[self.config.batch_size:]
    
    def add_filter(self, filter_func: Callable[[Any], bool]) -> None:
        """添加过滤器"""
        self.filters.append(filter_func)
    
    def add_callback(self, callback: Callable[[List[Any]], None]) -> None:
        """添加回调函数"""
        self.callbacks.append(callback)
    
    def flush(self) -> List[Any]:
        """刷新缓冲区，返回所有数据"""
        data = self.buffer.copy()
        self.buffer.clear()
        return data
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "mode": self.config.mode.value,
            "category": self.config.category.value,
            "collected_count": self.collected_count,
            "dropped_count": self.dropped_count,
            "buffer_size": len(self.buffer),
            "collection_rate": self.collected_count / (self.collected_count + self.dropped_count) 
                if (self.collected_count + self.dropped_count) > 0 else 0,
        }


class TrafficAnalyzer:
    """流量分析器 - 实时多维特征分析"""
    
    def __init__(self):
        self.traffic_stats: Dict[str, Any] = {
            "by_source": {},
            "by_dest": {},
            "by_port": {},
            "by_protocol": {},
            "by_ip_type": {},
        }
    
    def analyze(self, traffic_data: NetworkTrafficData) -> Dict[str, Any]:
        """分析流量数据"""
        # 按源地址统计
        self._update_stats(self.traffic_stats["by_source"], traffic_data.source_addr, traffic_data.packet_size)
        
        # 按目标地址统计
        self._update_stats(self.traffic_stats["by_dest"], traffic_data.dest_addr, traffic_data.packet_size)
        
        # 按端口统计
        self._update_stats(self.traffic_stats["by_port"], f"src:{traffic_data.source_port}", traffic_data.packet_size)
        self._update_stats(self.traffic_stats["by_port"], f"dst:{traffic_data.dest_port}", traffic_data.packet_size)
        
        # 按协议统计
        self._update_stats(self.traffic_stats["by_protocol"], traffic_data.protocol, traffic_data.packet_size)
        
        # 按IP类型统计
        self._update_stats(self.traffic_stats["by_ip_type"], traffic_data.ip_type, traffic_data.packet_size)
        
        return self.get_analysis_result()
    
    def _update_stats(self, stats_dict: Dict, key: str, packet_size: int) -> None:
        """更新统计信息"""
        if key not in stats_dict:
            stats_dict[key] = {"count": 0, "total_bytes": 0}
        
        stats_dict[key]["count"] += 1
        stats_dict[key]["total_bytes"] += packet_size
    
    def get_analysis_result(self) -> Dict[str, Any]:
        """获取分析结果"""
        return {
            "by_source": self._format_stats(self.traffic_stats["by_source"]),
            "by_dest": self._format_stats(self.traffic_stats["by_dest"]),
            "by_port": self._format_stats(self.traffic_stats["by_port"]),
            "by_protocol": self._format_stats(self.traffic_stats["by_protocol"]),
            "by_ip_type": self._format_stats(self.traffic_stats["by_ip_type"]),
        }
    
    def _format_stats(self, stats: Dict) -> List[Dict[str, Any]]:
        """格式化统计结果"""
        return [
            {
                "key": key,
                "count": value["count"],
                "total_bytes": value["total_bytes"],
                "avg_packet_size": value["total_bytes"] / value["count"]
            }
            for key, value in sorted(
                stats.items(),
                key=lambda x: x[1]["total_bytes"],
                reverse=True
            )
        ]
    
    def reset(self) -> None:
        """重置分析器"""
        self.traffic_stats = {
            "by_source": {},
            "by_dest": {},
            "by_port": {},
            "by_protocol": {},
            "by_ip_type": {},
        }


__all__ = [
    "CollectionMode",
    "DataCategory",
    "NetworkTrafficData",
    "CollectorConfig",
    "DataCollector",
    "TrafficAnalyzer",
]
