#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例：龙芯CPU模型仿真

演示如何创建和运行龙芯架构的CPU模型
"""

from virmachine.models.cpu import CPUModel, CPUConfig, CPUArchitecture, DomesticCPUType
from virmachine.models import ModelType
import time


def main():
    print("=" * 60)
    print("龙芯CPU模型仿真示例")
    print("=" * 60)
    
    # 创建龙芯3A5000 CPU配置
    config = CPUConfig(
        name="loongson_3a5000",
        model_type=ModelType.CPU,
        architecture=CPUArchitecture.LOONGARCH,
        domestic_type=DomesticCPUType.LOONGSON_3A5000,
        num_cores=4,
        clock_speed_mhz=2500.0,
        cache_l1_kb=64,
        cache_l2_kb=256,
        cache_l3_kb=16384,
        features=["LoongArch64", "LSX", "LASX", "FPU"]
    )
    
    print(f"\n创建CPU模型: {config.name}")
    print(f"架构: {config.architecture.value}")
    print(f"类型: {config.domestic_type.value}")
    print(f"核心数: {config.num_cores}")
    print(f"主频: {config.clock_speed_mhz} MHz")
    
    # 创建并初始化CPU模型
    cpu = CPUModel(config)
    
    print("\n初始化CPU...")
    if cpu.initialize():
        print("✓ CPU初始化成功")
    else:
        print("✗ CPU初始化失败")
        return
    
    # 启动CPU
    print("\n启动CPU...")
    cpu.start()
    print("✓ CPU已启动")
    
    # 模拟运行
    print("\n运行模拟...")
    for i in range(5):
        # 模拟100ms的时间流逝
        cpu.update(0.1)
        state = cpu.get_state()
        
        print(f"\n时间片 {i+1}:")
        print(f"  运行状态: {'运行中' if state['running'] else '停止'}")
        print(f"  执行指令数: {state['instruction_count']:,}")
        print(f"  周期数: {state['cycle_count']:,}")
        
        time.sleep(0.5)
    
    # 停止CPU
    print("\n停止CPU...")
    cpu.stop()
    print("✓ CPU已停止")
    
    # 显示最终状态
    final_state = cpu.get_state()
    print("\n最终状态:")
    print(f"  总执行指令数: {final_state['instruction_count']:,}")
    print(f"  总周期数: {final_state['cycle_count']:,}")
    print(f"  平均IPC: {final_state['instruction_count'] / final_state['cycle_count']:.2f}")
    
    print("\n" + "=" * 60)
    print("仿真完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
