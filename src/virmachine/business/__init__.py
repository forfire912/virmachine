#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
计算执行业务生成单元 (Computation Execution Business Generation Unit)

提供插件化开发单元，具备代码编辑、编译、调试等图形用户界面；
支持对计算执行环境任务创建、运行、暂停/重启、终止、归档以及销毁等过程的全生命周期管理与控制；
支持指定资源需求、配置和初始状态的新数字虚拟化任务工作负载；
支持数字虚拟化任务工作负载克隆、环境复制和备份创建、暂停/恢复、销毁功能数字样机实体任务工作负载。
"""

__all__ = [
    "lifecycle",
    "workload",
    "plugin",
]
