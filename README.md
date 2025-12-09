# 国产化虚拟样机 (VirMachine)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

**国产化虚拟样机平台** - 用于产品设计、仿真和测试的虚拟原型系统

**Localized Virtual Prototyping Machine** - A platform for product design, simulation and testing

## 简介 / Introduction

VirMachine 是一个轻量级的虚拟样机系统，提供以下核心功能：

- 🔧 **组件化设计** - 模块化的组件系统，便于构建复杂产品模型
- 🧪 **仿真测试** - 支持基础仿真、压力测试、性能测试等多种测试类型
- 🌐 **多语言支持** - 内置中英文双语支持，易于国产化应用
- 💾 **数据持久化** - JSON格式的数据存储，便于版本控制和共享
- 🖥️ **交互式界面** - 菜单驱动的交互式CLI，无需编程即可使用
- 🎯 **简单易用** - 清晰的API设计，快速上手

VirMachine is a lightweight virtual prototyping system with the following core features:

- 🔧 **Component-based Design** - Modular component system for building complex product models
- 🧪 **Simulation & Testing** - Support for basic simulation, stress testing, performance testing, and more
- 🌐 **Multi-language Support** - Built-in Chinese and English support for localization
- 💾 **Data Persistence** - JSON-based data storage for version control and sharing
- 🖥️ **Interactive Interface** - Menu-driven interactive CLI for no-code usage
- 🎯 **Easy to Use** - Clear API design for quick start

## 快速开始 / Quick Start

### 安装 / Installation

```bash
# 克隆仓库 / Clone repository
git clone https://github.com/forfire912/virmachine.git
cd virmachine

# 安装 / Install
pip install -e .

# 或使用开发模式 / Or install in development mode
pip install -e .[dev]
```

### 基本使用 / Basic Usage

```python
from virmachine import VirtualPrototype, Component, Simulator

# 创建虚拟样机 / Create a virtual prototype
prototype = VirtualPrototype(
    name="智能机器人 / Smart Robot",
    description="多传感器智能机器人 / Multi-sensor smart robot"
)

# 添加组件 / Add components
motor = Component("电机 / Motor", "motor", {"power": 100, "voltage": 24})
sensor = Component("传感器 / Sensor", "sensor", {"type": "infrared", "range": 5})
controller = Component("控制器 / Controller", "controller", {"cpu": "ARM"})

prototype.add_component(motor)
prototype.add_component(sensor)
prototype.add_component(controller)

# 创建仿真器并运行测试 / Create simulator and run tests
simulator = Simulator()
result = simulator.run_simulation(prototype)

print(f"仿真结果 / Result: {result}")
print(f"组件数量 / Components: {result.data['component_count']}")
```

### 运行示例 / Run Examples

```bash
# 运行交互式界面 / Run interactive interface (推荐 / Recommended)
python virmachine_interactive.py

# 运行演示程序 / Run demo program
python examples/demo.py

# 运行测试 / Run tests
python -m pytest tests/
```

## 主要功能 / Main Features

### 0. 交互式界面 / Interactive Interface (新功能 / New!)

无需编程，通过菜单驱动的交互式界面使用虚拟样机系统：

Use the virtual prototyping system through a menu-driven interface without coding:

```bash
# 启动交互式界面 / Launch interactive interface
python virmachine_interactive.py
```

**功能特性 / Features:**
- ✅ 创建和管理虚拟样机 / Create and manage virtual prototypes
- ✅ 添加和配置组件 / Add and configure components
- ✅ 运行各类仿真测试 / Run various simulation tests
- ✅ 保存和加载样机数据 / Save and load prototype data
- ✅ 中英文界面切换 / Switch between Chinese and English
- ✅ 友好的菜单导航 / User-friendly menu navigation

**界面示例 / Interface Example:**
```
======================================================================
║                                                                    ║
║                  国产化虚拟样机系统 - 交互式界面                       ║
║        Virtual Prototyping Machine - Interactive Interface         ║
║                                                                    ║
======================================================================

【主菜单】
  1. 创建新的虚拟样机
  2. 添加组件
  3. 查看虚拟样机信息
  4. 运行仿真测试
  5. 保存虚拟样机
  6. 加载虚拟样机
  7. 切换语言 (当前: 中文)
  0. 退出系统
----------------------------------------------------------------------
```

### 1. 虚拟样机管理 / Virtual Prototype Management

```python
from virmachine import VirtualPrototype, Component

# 创建样机 / Create prototype
prototype = VirtualPrototype("无人机原型", "四旋翼无人机")

# 添加组件 / Add components
prototype.add_component(Component("螺旋桨1", "propeller", {"diameter": 10}))
prototype.add_component(Component("飞控", "flight_controller", {"type": "APM"}))

# 设置元数据 / Set metadata
prototype.set_metadata("weight", 1.5)
prototype.set_metadata("max_speed", 50)

# 保存到文件 / Save to file
prototype.to_json("drone.json")

# 从文件加载 / Load from file
loaded = VirtualPrototype.from_json("drone.json")
```

### 2. 仿真与测试 / Simulation & Testing

```python
from virmachine import Simulator

simulator = Simulator()

# 基本仿真 / Basic simulation
result = simulator.run_simulation(prototype, "basic")

# 压力测试 / Stress test
stress_result = simulator.run_stress_test(prototype, stress_level=5.0)

# 性能测试 / Performance test
perf_result = simulator.run_performance_test(prototype)

# 自定义测试 / Custom test
def custom_test(component, params):
    # 自定义测试逻辑 / Custom test logic
    return {"result": "passed"}

simulator.register_test("custom_type", custom_test)
```

### 3. 多语言支持 / Multi-language Support

```python
from virmachine import set_language, get_text

# 使用中文 / Use Chinese
set_language('zh_CN')
print(get_text('simulation_completed'))  # 输出: 仿真已完成

# 使用英文 / Use English
set_language('en_US')
print(get_text('simulation_completed'))  # Output: Simulation completed
```

## 应用场景 / Use Cases

- 🚗 **汽车工程** - 引擎、底盘、传动系统的虚拟原型设计
- ✈️ **航空航天** - 飞行器部件和系统的数字化建模与测试
- 🤖 **机器人技术** - 机器人结构和控制系统的虚拟验证
- 🏭 **工业设备** - 生产设备和机械系统的虚拟样机开发
- 🔬 **科研教育** - 工程教学和研究中的虚拟实验平台

## 项目结构 / Project Structure

```
virmachine/
├── virmachine/                  # 主包 / Main package
│   ├── __init__.py             # 包初始化 / Package init
│   ├── core.py                 # 核心类定义 / Core classes
│   ├── simulator.py            # 仿真器 / Simulator
│   ├── localization.py         # 本地化支持 / Localization
│   └── interactive.py          # 交互式界面 / Interactive interface
├── examples/                   # 示例代码 / Example code
│   └── demo.py                # 演示程序 / Demo program
├── tests/                      # 测试代码 / Test code
│   └── test_virmachine.py
├── virmachine_interactive.py   # 交互式启动脚本 / Interactive launcher
├── setup.py                    # 安装配置 / Setup config
├── LICENSE                     # 许可证 / License
└── README.md                   # 说明文档 / Documentation
```

## 开发 / Development

```bash
# 克隆仓库 / Clone repository
git clone https://github.com/forfire912/virmachine.git
cd virmachine

# 安装开发依赖 / Install development dependencies
pip install -e .[dev]

# 运行测试 / Run tests
python -m pytest tests/ -v

# 运行测试并生成覆盖率报告 / Run tests with coverage
python -m pytest tests/ --cov=virmachine --cov-report=html
```

## 许可证 / License

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 贡献 / Contributing

欢迎提交问题和拉取请求！/ Issues and pull requests are welcome!

## 联系方式 / Contact

- GitHub: https://github.com/forfire912/virmachine
- Issues: https://github.com/forfire912/virmachine/issues

---

**国产化虚拟样机 - 让产品设计更简单、更高效**

**Localized Virtual Prototyping - Making product design simpler and more efficient**
