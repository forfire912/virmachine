#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
执行管理单元 (Execution Management Unit)

支持全局网络环境中，网络设备数字样机构建，支持全局特征网元实物建图、部署位置、配置、策略、业务数据进行统一建模；
支持网络样机生命周期管理，包括样机创建、删除、修改、停用等；
支持多种网络拓扑结构构建，包括环形、星状、网状等拓扑构建；
提供流量数据智能模拟器，能够基于流量数据特征，完成流量复现与模拟；
提供网络故障模型库，支持可视化构建、复现网络故障行为；
提供通信组件，可支持多种通信协议如SFTP、HTTPS、HTTP、UDP、TCP、ZMQ、DDS等；
支持对平台关键服务的不间断监控与高可用管理。
"""

__all__ = [
    "network",
    "topology",
    "traffic",
    "fault",
    "communication",
    "monitoring",
]
