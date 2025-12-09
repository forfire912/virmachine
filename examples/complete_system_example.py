#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例：完整的虚拟样机系统

演示如何构建一个完整的虚拟样机，包括CPU、内存、总线、中断控制器等
"""

from virmachine.models.cpu import CPUModel, CPUConfig, CPUArchitecture, DomesticCPUType
from virmachine.models.memory import MemoryModel, MemoryConfig
from virmachine.models.bus import BusModel, BusConfig, BusType, BusMessage
from virmachine.models.interrupt import InterruptController, InterruptConfig, PeriodicInterruptGenerator, InterruptType
from virmachine.models import ModelType
from virmachine.environment.runtime import PrototypeRuntime, RuntimeConfig
from virmachine.execution.loader import SystemLoader, OSImage, OSType
import time


def main():
    print("=" * 70)
    print("完整虚拟样机系统示例")
    print("=" * 70)
    
    # 1. 创建运行时环境
    print("\n[1] 创建运行时环境")
    runtime_config = RuntimeConfig(
        name="loongson_prototype",
        target_platform="x86_64",
        simulation_speed=1.0,
        enable_debug=True
    )
    runtime = PrototypeRuntime(runtime_config)
    print(f"✓ 运行时环境已创建: {runtime_config.name}")
    
    # 2. 创建CPU模型
    print("\n[2] 创建龙芯CPU模型")
    cpu_config = CPUConfig(
        name="loongson_3a5000",
        model_type=ModelType.CPU,
        architecture=CPUArchitecture.LOONGARCH,
        domestic_type=DomesticCPUType.LOONGSON_3A5000,
        num_cores=4,
        clock_speed_mhz=2500.0
    )
    cpu = CPUModel(cpu_config)
    runtime.add_model("cpu", cpu)
    print(f"✓ CPU模型已添加: {cpu_config.name}")
    
    # 3. 创建内存模型
    print("\n[3] 创建内存模型")
    memory_config = MemoryConfig(
        name="main_memory",
        model_type=ModelType.MEMORY,
        size_mb=8192,
        access_time_ns=10.0
    )
    memory = MemoryModel(memory_config)
    runtime.add_model("memory", memory)
    print(f"✓ 内存模型已添加: {memory_config.size_mb}MB")
    
    # 4. 创建总线模型
    print("\n[4] 创建系统总线")
    bus_config = BusConfig(
        name="system_bus",
        model_type=ModelType.BUS,
        bus_type=BusType.ETHERNET,
        bandwidth_mbps=1000.0
    )
    bus = BusModel(bus_config)
    runtime.add_model("bus", bus)
    print(f"✓ 总线模型已添加: {bus_config.bus_type.value}")
    
    # 5. 创建中断控制器
    print("\n[5] 创建中断控制器")
    interrupt_config = InterruptConfig(
        name="interrupt_controller",
        model_type=ModelType.INTERRUPT_CONTROLLER,
        num_vectors=256,
        priority_levels=8
    )
    interrupt_ctrl = InterruptController(interrupt_config)
    runtime.add_model("interrupt_controller", interrupt_ctrl)
    print(f"✓ 中断控制器已添加: {interrupt_config.num_vectors}个中断向量")
    
    # 6. 初始化运行时
    print("\n[6] 初始化运行时环境")
    if runtime.initialize():
        print("✓ 所有模型初始化成功")
    else:
        print("✗ 初始化失败")
        return
    
    # 7. 加载操作系统
    print("\n[7] 加载银河麒麟操作系统")
    loader = SystemLoader()
    os_image = OSImage(
        os_type=OSType.KYLIN,
        name="Kylin Server",
        version="V10",
        kernel_path="/boot/vmlinuz-kylin",
        initrd_path="/boot/initrd.img",
        rootfs_path="/dev/vda1",
        boot_args=["root=/dev/vda1", "ro", "quiet"]
    )
    
    if loader.load_os(os_image):
        print("✓ 操作系统加载成功")
        if loader.boot():
            print("✓ 操作系统启动成功")
    
    # 8. 配置中断
    print("\n[8] 配置周期性中断")
    # 注册定时器中断处理程序
    def timer_interrupt_handler(interrupt):
        print(f"  [中断] 定时器中断触发 - 向量{interrupt.vector}, 次数{interrupt.count}")
    
    interrupt_ctrl.register_interrupt(
        vector=32,
        interrupt_type=InterruptType.TIMER,
        priority=5,
        handler=timer_interrupt_handler
    )
    
    # 创建周期性中断生成器 - 每100ms触发一次，共5次
    timer_gen = PeriodicInterruptGenerator(
        controller=interrupt_ctrl,
        vector=32,
        period_ms=100,
        count=5
    )
    print("✓ 定时器中断已配置 (100ms周期, 5次)")
    
    # 9. 启动运行时
    print("\n[9] 启动虚拟样机")
    runtime.start()
    cpu.start()
    print("✓ 虚拟样机运行中...")
    
    # 10. 运行模拟
    print("\n[10] 执行仿真循环")
    for i in range(10):
        delta_time = 0.1  # 100ms
        
        # 更新所有组件
        runtime.update(delta_time)
        timer_gen.update(delta_time)
        
        # 每2次循环显示一次状态
        if i % 2 == 0:
            state = runtime.get_state()
            print(f"\n  周期 {i+1}:")
            print(f"    仿真时间: {state['simulation_time']:.2f}s")
            print(f"    更新次数: {state['update_count']}")
            print(f"    CPU指令数: {cpu.get_state()['instruction_count']:,}")
            print(f"    中断总数: {interrupt_ctrl.get_state()['total_interrupts']}")
        
        time.sleep(0.2)
    
    # 11. 保存快照
    print("\n[11] 保存系统快照")
    snapshot = runtime.save_snapshot()
    print(f"✓ 快照已保存，包含 {len(snapshot['models'])} 个模型")
    
    # 12. 停止系统
    print("\n[12] 停止虚拟样机")
    runtime.stop()
    cpu.stop()
    loader.shutdown()
    print("✓ 虚拟样机已停止")
    
    # 13. 显示统计信息
    print("\n[13] 系统统计信息")
    print("-" * 70)
    final_state = runtime.get_state()
    print(f"总运行时间: {final_state['elapsed_time']:.2f}s")
    print(f"仿真时间: {final_state['simulation_time']:.2f}s")
    print(f"CPU执行指令: {cpu.get_state()['instruction_count']:,}")
    print(f"CPU周期数: {cpu.get_state()['cycle_count']:,}")
    print(f"内存访问: {memory.get_state()['access_count']}")
    print(f"总线消息: {bus.get_state()['message_count']}")
    print(f"中断触发: {interrupt_ctrl.get_state()['total_interrupts']}")
    
    print("\n" + "=" * 70)
    print("仿真完成")
    print("=" * 70)


if __name__ == "__main__":
    main()
