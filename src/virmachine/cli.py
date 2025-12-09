#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VirMachine CLI - Command Line Interface

虚拟样机系统命令行接口
"""

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """VirMachine - 国产化虚拟样机系统"""
    pass


@main.group()
def model():
    """模型管理命令"""
    pass


@model.command()
def list():
    """列出所有可用模型"""
    from virmachine.models import registry
    
    table = Table(title="可用模型")
    table.add_column("模型类型", style="cyan")
    
    for model_type in registry.list_models():
        table.add_row(model_type)
    
    console.print(table)


@main.group()
def task():
    """任务管理命令"""
    pass


@task.command()
@click.argument("name")
@click.option("--cores", default=1, help="CPU核心数")
@click.option("--memory", default=1024, help="内存大小(MB)")
def create(name, cores, memory):
    """创建新任务"""
    from virmachine.business.lifecycle import TaskManager, TaskConfig, ResourceRequirements
    
    resources = ResourceRequirements(cpu_cores=cores, memory_mb=memory)
    config = TaskConfig(name=name, resources=resources)
    
    manager = TaskManager()
    task = manager.create_task(config)
    
    console.print(f"[green]任务创建成功: {task.task_id}[/green]")
    console.print(f"名称: {name}")
    console.print(f"CPU核心: {cores}")
    console.print(f"内存: {memory}MB")


@main.group()
def topology():
    """网络拓扑命令"""
    pass


@topology.command()
@click.argument("name")
@click.option("--type", "topo_type", default="star", help="拓扑类型: star, ring, mesh")
@click.option("--nodes", default=4, help="节点数量")
def create(name, topo_type, nodes):
    """创建网络拓扑"""
    from virmachine.management.topology import (
        TopologyBuilder, NetworkNode, TopologyType
    )
    
    # 创建节点
    if topo_type == "star":
        center = NetworkNode(node_id="center", node_type="router", name="中心节点")
        leaf_nodes = [
            NetworkNode(node_id=f"node{i}", node_type="host", name=f"节点{i}")
            for i in range(nodes)
        ]
        topo = TopologyBuilder.build_star_topology(name, center, leaf_nodes)
    elif topo_type == "ring":
        node_list = [
            NetworkNode(node_id=f"node{i}", node_type="host", name=f"节点{i}")
            for i in range(nodes)
        ]
        topo = TopologyBuilder.build_ring_topology(name, node_list)
    elif topo_type == "mesh":
        node_list = [
            NetworkNode(node_id=f"node{i}", node_type="host", name=f"节点{i}")
            for i in range(nodes)
        ]
        topo = TopologyBuilder.build_mesh_topology(name, node_list)
    else:
        console.print(f"[red]不支持的拓扑类型: {topo_type}[/red]")
        return
    
    stats = topo.get_statistics()
    console.print(f"[green]拓扑创建成功: {name}[/green]")
    console.print(f"类型: {stats['topology_type']}")
    console.print(f"节点数: {stats['node_count']}")
    console.print(f"链路数: {stats['link_count']}")


if __name__ == "__main__":
    main()
