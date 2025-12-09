#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
网络拓扑管理 (Network Topology Management)

支持多种网络拓扑结构构建，包括环形、星状、网状等拓扑构建
"""

from typing import Dict, Any, List, Optional, Set, Tuple
from enum import Enum
from dataclasses import dataclass, field
import networkx as nx


class TopologyType(Enum):
    """拓扑类型"""
    STAR = "star"           # 星状拓扑
    RING = "ring"           # 环形拓扑
    MESH = "mesh"           # 网状拓扑
    TREE = "tree"           # 树形拓扑
    BUS = "bus"             # 总线拓扑
    HYBRID = "hybrid"       # 混合拓扑


@dataclass
class NetworkNode:
    """网络节点"""
    node_id: str
    node_type: str  # router, switch, host, etc.
    name: str
    position: Tuple[float, float] = (0.0, 0.0)  # x, y坐标
    properties: Dict[str, Any] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)
    status: str = "active"  # active, inactive, failed


@dataclass
class NetworkLink:
    """网络链路"""
    link_id: str
    source: str
    target: str
    bandwidth_mbps: float = 100.0
    latency_ms: float = 1.0
    loss_rate: float = 0.0
    properties: Dict[str, Any] = field(default_factory=dict)
    status: str = "up"  # up, down


class NetworkTopology:
    """网络拓扑"""
    
    def __init__(self, name: str, topology_type: TopologyType):
        self.name = name
        self.topology_type = topology_type
        self.graph = nx.Graph()
        self.nodes: Dict[str, NetworkNode] = {}
        self.links: Dict[str, NetworkLink] = {}
    
    def add_node(self, node: NetworkNode) -> None:
        """添加节点"""
        if node.node_id in self.nodes:
            raise ValueError(f"Node {node.node_id} already exists")
        
        self.nodes[node.node_id] = node
        self.graph.add_node(
            node.node_id,
            **{
                "type": node.node_type,
                "name": node.name,
                "position": node.position,
            }
        )
    
    def remove_node(self, node_id: str) -> bool:
        """移除节点"""
        if node_id not in self.nodes:
            return False
        
        # 移除相关的链路
        links_to_remove = [
            link_id for link_id, link in self.links.items()
            if link.source == node_id or link.target == node_id
        ]
        for link_id in links_to_remove:
            self.remove_link(link_id)
        
        del self.nodes[node_id]
        self.graph.remove_node(node_id)
        return True
    
    def add_link(self, link: NetworkLink) -> None:
        """添加链路"""
        if link.source not in self.nodes or link.target not in self.nodes:
            raise ValueError("Source or target node does not exist")
        
        if link.link_id in self.links:
            raise ValueError(f"Link {link.link_id} already exists")
        
        self.links[link.link_id] = link
        self.graph.add_edge(
            link.source,
            link.target,
            link_id=link.link_id,
            bandwidth=link.bandwidth_mbps,
            latency=link.latency_ms,
        )
    
    def remove_link(self, link_id: str) -> bool:
        """移除链路"""
        if link_id not in self.links:
            return False
        
        link = self.links[link_id]
        if self.graph.has_edge(link.source, link.target):
            self.graph.remove_edge(link.source, link.target)
        
        del self.links[link_id]
        return True
    
    def get_node(self, node_id: str) -> Optional[NetworkNode]:
        """获取节点"""
        return self.nodes.get(node_id)
    
    def get_link(self, link_id: str) -> Optional[NetworkLink]:
        """获取链路"""
        return self.links.get(link_id)
    
    def get_neighbors(self, node_id: str) -> List[str]:
        """获取邻居节点"""
        if node_id not in self.nodes:
            return []
        return list(self.graph.neighbors(node_id))
    
    def find_path(self, source: str, target: str) -> Optional[List[str]]:
        """查找路径"""
        try:
            return nx.shortest_path(self.graph, source, target)
        except nx.NetworkXNoPath:
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取拓扑统计信息"""
        return {
            "name": self.name,
            "topology_type": self.topology_type.value,
            "node_count": len(self.nodes),
            "link_count": len(self.links),
            "is_connected": nx.is_connected(self.graph),
            "density": nx.density(self.graph),
            "average_degree": sum(dict(self.graph.degree()).values()) / len(self.nodes) if self.nodes else 0,
        }
    
    def export_topology(self) -> Dict[str, Any]:
        """导出拓扑配置"""
        return {
            "name": self.name,
            "topology_type": self.topology_type.value,
            "nodes": [
                {
                    "node_id": node.node_id,
                    "node_type": node.node_type,
                    "name": node.name,
                    "position": node.position,
                    "properties": node.properties,
                    "config": node.config,
                    "status": node.status,
                }
                for node in self.nodes.values()
            ],
            "links": [
                {
                    "link_id": link.link_id,
                    "source": link.source,
                    "target": link.target,
                    "bandwidth_mbps": link.bandwidth_mbps,
                    "latency_ms": link.latency_ms,
                    "loss_rate": link.loss_rate,
                    "properties": link.properties,
                    "status": link.status,
                }
                for link in self.links.values()
            ]
        }


class TopologyBuilder:
    """拓扑构建器"""
    
    @staticmethod
    def build_star_topology(
        name: str,
        center_node: NetworkNode,
        leaf_nodes: List[NetworkNode],
        link_bandwidth: float = 100.0
    ) -> NetworkTopology:
        """构建星状拓扑"""
        topology = NetworkTopology(name, TopologyType.STAR)
        
        # 添加中心节点
        topology.add_node(center_node)
        
        # 添加叶子节点和链路
        for i, leaf in enumerate(leaf_nodes):
            topology.add_node(leaf)
            link = NetworkLink(
                link_id=f"link_{center_node.node_id}_{leaf.node_id}",
                source=center_node.node_id,
                target=leaf.node_id,
                bandwidth_mbps=link_bandwidth,
            )
            topology.add_link(link)
        
        return topology
    
    @staticmethod
    def build_ring_topology(
        name: str,
        nodes: List[NetworkNode],
        link_bandwidth: float = 100.0
    ) -> NetworkTopology:
        """构建环形拓扑"""
        topology = NetworkTopology(name, TopologyType.RING)
        
        # 添加节点
        for node in nodes:
            topology.add_node(node)
        
        # 添加链路形成环
        for i in range(len(nodes)):
            source = nodes[i]
            target = nodes[(i + 1) % len(nodes)]
            link = NetworkLink(
                link_id=f"link_{source.node_id}_{target.node_id}",
                source=source.node_id,
                target=target.node_id,
                bandwidth_mbps=link_bandwidth,
            )
            topology.add_link(link)
        
        return topology
    
    @staticmethod
    def build_mesh_topology(
        name: str,
        nodes: List[NetworkNode],
        link_bandwidth: float = 100.0,
        full_mesh: bool = True
    ) -> NetworkTopology:
        """构建网状拓扑"""
        topology = NetworkTopology(name, TopologyType.MESH)
        
        # 添加节点
        for node in nodes:
            topology.add_node(node)
        
        if full_mesh:
            # 全网状：每个节点连接到所有其他节点
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    source = nodes[i]
                    target = nodes[j]
                    link = NetworkLink(
                        link_id=f"link_{source.node_id}_{target.node_id}",
                        source=source.node_id,
                        target=target.node_id,
                        bandwidth_mbps=link_bandwidth,
                    )
                    topology.add_link(link)
        
        return topology


__all__ = [
    "TopologyType",
    "NetworkNode",
    "NetworkLink",
    "NetworkTopology",
    "TopologyBuilder",
]
