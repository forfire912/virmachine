#!/usr/bin/env python3
"""
示例程序 - 演示虚拟样机系统的使用
Example Program - Demonstrates the use of the virtual prototyping system
"""

from virmachine import VirtualPrototype, Component, Simulator, set_language, get_text


def example_basic_usage():
    """基本使用示例 / Basic usage example"""
    print("=" * 60)
    print("基本使用示例 / Basic Usage Example")
    print("=" * 60)
    
    # 创建虚拟样机
    prototype = VirtualPrototype(
        name="智能机器人原型 / Smart Robot Prototype",
        description="一个具有多传感器的智能机器人 / A smart robot with multiple sensors"
    )
    
    # 添加组件
    motor = Component("电机", "motor", {"power": 100, "voltage": 24})
    sensor = Component("传感器", "sensor", {"type": "infrared", "range": 5})
    controller = Component("控制器", "controller", {"cpu": "ARM", "memory": 512})
    
    prototype.add_component(motor)
    prototype.add_component(sensor)
    prototype.add_component(controller)
    
    print(f"\n创建的虚拟样机: {prototype}")
    print(f"组件数量: {len(prototype.components)}")
    
    for comp in prototype.components:
        print(f"  - {comp}")
    
    return prototype


def example_simulation():
    """仿真示例 / Simulation example"""
    print("\n" + "=" * 60)
    print("仿真测试示例 / Simulation Test Example")
    print("=" * 60)
    
    # 创建虚拟样机
    prototype = VirtualPrototype(
        name="汽车引擎原型",
        description="V6引擎虚拟样机"
    )
    
    # 添加引擎组件
    components = [
        Component("气缸1", "cylinder", {"displacement": 500, "compression": 10.5}),
        Component("气缸2", "cylinder", {"displacement": 500, "compression": 10.5}),
        Component("曲轴", "crankshaft", {"material": "steel", "weight": 15.5}),
        Component("活塞", "piston", {"material": "aluminum", "count": 6}),
    ]
    
    for comp in components:
        prototype.add_component(comp)
    
    # 创建仿真器
    simulator = Simulator()
    
    # 运行基本仿真
    print(f"\n运行基本仿真...")
    result = simulator.run_simulation(prototype, "basic")
    print(f"结果: {result}")
    print(f"测试的组件数: {result.data.get('component_count')}")
    
    # 运行压力测试
    print(f"\n运行压力测试...")
    stress_result = simulator.run_stress_test(prototype, stress_level=5.0)
    print(f"结果: {stress_result}")
    
    # 运行性能测试
    print(f"\n运行性能测试...")
    perf_result = simulator.run_performance_test(prototype)
    print(f"结果: {perf_result}")
    
    return simulator


def example_save_load():
    """保存和加载示例 / Save and load example"""
    print("\n" + "=" * 60)
    print("保存和加载示例 / Save and Load Example")
    print("=" * 60)
    
    # 创建虚拟样机
    prototype = VirtualPrototype(
        name="无人机原型",
        description="四旋翼无人机"
    )
    
    # 添加组件
    prototype.add_component(Component("螺旋桨1", "propeller", {"diameter": 10, "pitch": 4.5}))
    prototype.add_component(Component("螺旋桨2", "propeller", {"diameter": 10, "pitch": 4.5}))
    prototype.add_component(Component("螺旋桨3", "propeller", {"diameter": 10, "pitch": 4.5}))
    prototype.add_component(Component("螺旋桨4", "propeller", {"diameter": 10, "pitch": 4.5}))
    prototype.add_component(Component("飞控", "flight_controller", {"type": "APM"}))
    prototype.add_component(Component("电池", "battery", {"capacity": 5000, "voltage": 11.1}))
    
    # 设置元数据
    prototype.set_metadata("weight", 1.5)
    prototype.set_metadata("max_speed", 50)
    
    # 保存到文件
    import os
    filepath = "/tmp/drone_prototype.json"
    print(f"\n保存虚拟样机到: {filepath}")
    prototype.to_json(filepath)
    
    # 从文件加载
    print(f"从文件加载虚拟样机...")
    loaded_prototype = VirtualPrototype.from_json(filepath)
    print(f"加载的虚拟样机: {loaded_prototype}")
    print(f"组件数量: {len(loaded_prototype.components)}")
    print(f"元数据: {loaded_prototype.metadata}")
    
    # 清理
    if os.path.exists(filepath):
        os.remove(filepath)
    
    return loaded_prototype


def example_localization():
    """本地化示例 / Localization example"""
    print("\n" + "=" * 60)
    print("多语言支持示例 / Multi-language Support Example")
    print("=" * 60)
    
    # 使用中文
    set_language('zh_CN')
    print(f"\n当前语言: 中文")
    print(f"  - {get_text('prototype_created')}")
    print(f"  - {get_text('component_added')}")
    print(f"  - {get_text('simulation_completed')}")
    print(f"  - {get_text('test_passed')}")
    
    # 切换到英文
    set_language('en_US')
    print(f"\n当前语言: English")
    print(f"  - {get_text('prototype_created')}")
    print(f"  - {get_text('component_added')}")
    print(f"  - {get_text('simulation_completed')}")
    print(f"  - {get_text('test_passed')}")
    
    # 切换回中文
    set_language('zh_CN')


def main():
    """主函数 / Main function"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "   国产化虚拟样机系统演示程序".center(58) + "║")
    print("║" + "   Virtual Prototyping Machine Demo".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        # 运行示例
        example_basic_usage()
        example_simulation()
        example_save_load()
        example_localization()
        
        print("\n" + "=" * 60)
        print("所有示例运行完成！/ All examples completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误 / Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
