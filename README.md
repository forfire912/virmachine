# VirMachine - 国产化虚拟样机系统

VirMachine是一个综合性的虚拟样机系统，专为国产化计算环境设计，提供完整的数字样机建模、仿真和管理解决方案。

## 系统架构

VirMachine系统由五个主要功能单元组成：

### 1. 计算执行单元 (Computation Execution Unit)

提供数字体构建和模型库功能：

- **数字体构建组件**: 包括设计单元、编译单元
- **模型库**: CPU、内存、寄存器、串口、网口等核心模型
- **国产CPU支持**: 龙芯系列（LoongArch）、飞腾系列（Phytium）等
- **操作系统支持**: VxWorks、银河麒麟、LoongArch Linux等
- **中断模拟**: 支持可配置的中断周期与次数
- **总线模型**: FC（光纤通道）、RS422、ARINC429等总线模拟
- **高扩展性**: 支持模型升级和模块替换

### 2. 计算执行环境构建单元 (Execution Environment Building Unit)

提供编译和运行环境：

- **插件化开发单元**: 支持代码编辑、编译、调试
- **运行时环境**: 模型加载引擎和生命周期管理
- **跨平台支持**: 在X86环境运行多种架构的样机
- **图形化建模**: 可视化样机实体建模
- **多模型配置**: 构建与真实环境一致的数字环境

### 3. 计算执行业务生成单元 (Business Generation Unit)

提供任务管理和工作负载控制：

- **插件化开发**: 图形用户界面支持
- **生命周期管理**: 任务创建、运行、暂停/重启、终止、归档、销毁
- **资源管理**: 指定资源需求、配置和初始状态
- **工作负载操作**: 克隆、环境复制、备份创建、暂停/恢复

### 4. 计算结果数据分析单元 (Data Analysis Unit)

提供数据采集和分析功能：

- **多种采集方式**: 按需抽样、全量实时、半流量实时采集
- **异构数据分类**: 分类存储和管理
- **多维特征分析**: 源地址、目标地址、IP类型、端口号等实时分析
- **数据提取**: 支持XML、JSON、CSV等格式转换
- **数据同步**: 数据订阅和通信
- **数据处理**: 压缩、切片、规则筛选等功能

### 5. 计算执行管理单元 (Execution Management Unit)

提供网络管理和监控功能：

- **网络样机建模**: 网元建图、部署、配置统一建模
- **生命周期管理**: 样机创建、删除、修改、停用
- **网络拓扑**: 环形、星状、网状等拓扑构建
- **流量模拟**: 基于特征的流量复现与模拟
- **故障模型**: 可视化网络故障构建和复现
- **通信协议**: SFTP、HTTPS、HTTP、UDP、TCP、ZMQ、DDS等
- **高可用管理**: 关键服务监控和高可用保障

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/forfire912/virmachine.git
cd virmachine

# 安装依赖
pip install -r requirements.txt

# 开发环境安装
pip install -r requirements-dev.txt

# 安装VirMachine
pip install -e .
```

### 基础使用示例

#### 1. 创建CPU模型

```python
from virmachine.models.cpu import CPUModel, CPUConfig, CPUArchitecture, DomesticCPUType
from virmachine.models import ModelType

# 创建龙芯CPU配置
config = CPUConfig(
    name="loongson_3a5000",
    model_type=ModelType.CPU,
    architecture=CPUArchitecture.LOONGARCH,
    domestic_type=DomesticCPUType.LOONGSON_3A5000,
    num_cores=4,
    clock_speed_mhz=2500.0
)

# 创建并初始化CPU模型
cpu = CPUModel(config)
cpu.initialize()
cpu.start()

# 获取CPU状态
print(cpu.get_state())
```

#### 2. 构建网络拓扑

```python
from virmachine.management.topology import (
    TopologyBuilder, NetworkNode, TopologyType
)

# 创建节点
center = NetworkNode(node_id="router1", node_type="router", name="中心路由器")
nodes = [
    NetworkNode(node_id=f"host{i}", node_type="host", name=f"主机{i}")
    for i in range(1, 5)
]

# 构建星状拓扑
topology = TopologyBuilder.build_star_topology(
    name="办公网络",
    center_node=center,
    leaf_nodes=nodes,
    link_bandwidth=1000.0
)

# 查看拓扑统计
print(topology.get_statistics())
```

#### 3. 任务生命周期管理

```python
from virmachine.business.lifecycle import (
    TaskManager, TaskConfig, ResourceRequirements
)

# 创建任务管理器
manager = TaskManager()

# 配置资源需求
resources = ResourceRequirements(
    cpu_cores=4,
    memory_mb=8192,
    storage_mb=102400
)

# 创建任务
config = TaskConfig(
    name="仿真任务1",
    description="龙芯CPU仿真测试",
    resources=resources,
    tags=["simulation", "loongson"]
)

task = manager.create_task(config)
task.configure({"environment": {"OS": "Kylin"}})
task.start()

# 查看任务状态
print(task.get_state())
```

#### 4. 数据采集和导出

```python
from virmachine.analysis.collector import (
    DataCollector, CollectorConfig, CollectionMode, DataCategory
)
from virmachine.analysis.extractor import DataExportService, DataFormat

# 创建数据采集器
config = CollectorConfig(
    mode=CollectionMode.SAMPLING,
    category=DataCategory.NETWORK_TRAFFIC,
    sampling_rate=0.5
)
collector = DataCollector(config)

# 采集数据
data = {"timestamp": "2024-01-01", "value": 100}
collector.collect(data)

# 导出数据
export_service = DataExportService()
json_data = export_service.export(collector.flush(), DataFormat.JSON)
print(json_data)
```

## 核心特性

### 国产化支持

- **国产CPU**: 龙芯(LoongArch)、飞腾(Phytium)、兆芯、海光等
- **国产操作系统**: 银河麒麟、统信UOS、开放麒麟、深度等
- **国产总线**: 支持国内航空航天领域常用总线标准

### 高扩展性

- 插件化架构设计
- 模型注册机制支持动态扩展
- 可替换的组件和模块

### 跨平台支持

- X86平台运行多架构样机
- 统一的模型接口
- 平台无关的运行时环境

## 项目结构

```
virmachine/
├── src/
│   └── virmachine/
│       ├── execution/          # 计算执行单元
│       │   └── loader.py       # 系统加载器
│       ├── environment/        # 执行环境构建单元
│       │   └── runtime.py      # 运行时环境
│       ├── business/           # 业务生成单元
│       │   └── lifecycle.py    # 生命周期管理
│       ├── analysis/           # 数据分析单元
│       │   ├── collector.py    # 数据采集
│       │   └── extractor.py    # 数据提取
│       ├── management/         # 执行管理单元
│       │   └── topology.py     # 网络拓扑
│       └── models/             # 模型库
│           ├── __init__.py     # 模型基类
│           ├── cpu.py          # CPU模型
│           ├── memory.py       # 内存模型
│           ├── bus.py          # 总线模型
│           └── interrupt.py    # 中断控制器
├── setup.py                    # 安装配置
├── requirements.txt            # 依赖列表
└── README.md                   # 项目文档
```

## 开发指南

### 添加新模型

1. 继承`BaseModel`基类
2. 实现必需的抽象方法
3. 注册模型到`ModelRegistry`

```python
from virmachine.models import BaseModel, ModelConfig, registry

class CustomModel(BaseModel):
    def initialize(self) -> bool:
        # 初始化逻辑
        return True
    
    def reset(self) -> None:
        # 重置逻辑
        pass
    
    def update(self, delta_time: float) -> None:
        # 更新逻辑
        pass
    
    def get_state(self) -> Dict[str, Any]:
        # 返回状态
        return {}
    
    def set_state(self, state: Dict[str, Any]) -> None:
        # 设置状态
        pass

# 注册模型
registry.register("custom_model", CustomModel)
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_models.py

# 生成覆盖率报告
pytest --cov=virmachine --cov-report=html
```

### 代码风格

项目使用以下工具保证代码质量：

- `black`: 代码格式化
- `flake8`: 代码检查
- `mypy`: 类型检查

```bash
# 格式化代码
black src/

# 检查代码
flake8 src/

# 类型检查
mypy src/
```

## 贡献指南

欢迎贡献代码、报告问题或提出新功能建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式

- 项目主页: https://github.com/forfire912/virmachine
- 问题反馈: https://github.com/forfire912/virmachine/issues

## 致谢

感谢所有为国产化虚拟样机系统做出贡献的开发者和用户！
