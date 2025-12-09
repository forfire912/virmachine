#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例：网络拓扑构建和管理

演示如何构建和管理不同类型的网络拓扑
"""

from virmachine.management.topology import (
    TopologyBuilder,
    NetworkNode,
    NetworkLink,
    TopologyType
)
import json


def create_star_topology():
    """创建星状拓扑示例"""
    print("\n" + "=" * 60)
    print("创建星状拓扑")
    print("=" * 60)
    
    # 创建中心路由器
    center = NetworkNode(
        node_id="router1",
        node_type="router",
        name="中心路由器",
        position=(0, 0),
        properties={"vendor": "Huawei", "model": "NE40E"}
    )
    
    # 创建叶子节点（服务器）
    servers = [
        NetworkNode(
            node_id=f"server{i}",
            node_type="server",
            name=f"服务器{i}",
            position=(i * 2, 5),
            properties={"os": "Kylin Server V10", "cpu": "Phytium FT-2000"}
        )
        for i in range(1, 6)
    ]
    
    # 构建星状拓扑
    topology = TopologyBuilder.build_star_topology(
        name="数据中心网络",
        center_node=center,
        leaf_nodes=servers,
        link_bandwidth=10000.0  # 10Gbps
    )
    
    # 显示拓扑信息
    stats = topology.get_statistics()
    print(f"\n拓扑名称: {stats['name']}")
    print(f"拓扑类型: {stats['topology_type']}")
    print(f"节点数量: {stats['node_count']}")
    print(f"链路数量: {stats['link_count']}")
    print(f"网络密度: {stats['density']:.3f}")
    print(f"平均度数: {stats['average_degree']:.2f}")
    print(f"连通性: {'是' if stats['is_connected'] else '否'}")
    
    # 显示节点信息
    print("\n节点列表:")
    for node_id, node in topology.nodes.items():
        print(f"  - {node.name} ({node.node_type}): {node_id}")
    
    # 显示链路信息
    print("\n链路列表:")
    for link_id, link in topology.links.items():
        print(f"  - {link.source} -> {link.target}: {link.bandwidth_mbps}Mbps")
    
    return topology


def create_ring_topology():
    """创建环形拓扑示例"""
    print("\n" + "=" * 60)
    print("创建环形拓扑")
    print("=" * 60)
    
    # 创建节点
    nodes = [
        NetworkNode(
            node_id=f"router{i}",
            node_type="router",
            name=f"路由器{i}",
            position=(i * 3, 0)
        )
        for i in range(1, 5)
    ]
    
    # 构建环形拓扑
    topology = TopologyBuilder.build_ring_topology(
        name="环形骨干网",
        nodes=nodes,
        link_bandwidth=1000.0  # 1Gbps
    )
    
    stats = topology.get_statistics()
    print(f"\n拓扑名称: {stats['name']}")
    print(f"拓扑类型: {stats['topology_type']}")
    print(f"节点数量: {stats['node_count']}")
    print(f"链路数量: {stats['link_count']}")
    
    # 测试路径查找
    print("\n路径查找测试:")
    path = topology.find_path("router1", "router3")
    if path:
        print(f"  router1 -> router3: {' -> '.join(path)}")
    
    return topology


def create_mesh_topology():
    """创建网状拓扑示例"""
    print("\n" + "=" * 60)
    print("创建全网状拓扑")
    print("=" * 60)
    
    # 创建节点
    nodes = [
        NetworkNode(
            node_id=f"switch{i}",
            node_type="switch",
            name=f"交换机{i}",
            position=(i % 3 * 3, i // 3 * 3)
        )
        for i in range(1, 7)
    ]
    
    # 构建全网状拓扑
    topology = TopologyBuilder.build_mesh_topology(
        name="高可用网络",
        nodes=nodes,
        link_bandwidth=10000.0,
        full_mesh=True
    )
    
    stats = topology.get_statistics()
    print(f"\n拓扑名称: {stats['name']}")
    print(f"拓扑类型: {stats['topology_type']}")
    print(f"节点数量: {stats['node_count']}")
    print(f"链路数量: {stats['link_count']}")
    print(f"网络密度: {stats['density']:.3f}")
    
    # 显示每个节点的邻居
    print("\n节点连接:")
    for node_id in topology.nodes.keys():
        neighbors = topology.get_neighbors(node_id)
        print(f"  {node_id}: {len(neighbors)}个邻居 -> {', '.join(neighbors)}")
    
    return topology


def export_topology_config(topology):
    """导出拓扑配置"""
    print("\n" + "=" * 60)
    print("导出拓扑配置")
    print("=" * 60)
    
    config = topology.export_topology()
    
    # 保存为JSON文件
    filename = f"{topology.name.replace(' ', '_')}_topology.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n配置已导出到: {filename}")
    print(f"节点数: {len(config['nodes'])}")
    print(f"链路数: {len(config['links'])}")


def main():
    print("=" * 70)
    print("网络拓扑构建和管理示例")
    print("=" * 70)
    
    # 创建不同类型的拓扑
    star_topo = create_star_topology()
    ring_topo = create_ring_topology()
    mesh_topo = create_mesh_topology()
    
    # 导出拓扑配置
    export_topology_config(star_topo)
    
    print("\n" + "=" * 70)
    print("示例完成")
    print("=" * 70)


if __name__ == "__main__":
    main()
