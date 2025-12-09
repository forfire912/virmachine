# VirMachine 系统架构文档

## 概述

VirMachine是一个综合性的国产化虚拟样机系统，旨在提供完整的数字样机建模、仿真和管理解决方案。系统采用模块化、可扩展的架构设计，支持多种国产CPU架构和操作系统。

## 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        VirMachine System                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Execution  │  │ Environment  │  │   Business   │          │
│  │     Unit     │  │  Build Unit  │  │ Generation   │          │
│  │              │  │              │  │     Unit     │          │
│  │ - CPU Model  │  │ - Runtime    │  │ - Lifecycle  │          │
│  │ - Memory     │  │ - Plugin     │  │ - Workload   │          │
│  │ - Bus        │  │ - Compiler   │  │ - Resource   │          │
│  │ - Interrupt  │  │ - Builder    │  │   Mgmt       │          │
│  │ - Loader     │  │              │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────────────────────┐            │
│  │   Analysis   │  │      Management Unit         │            │
│  │     Unit     │  │                              │            │
│  │              │  │ - Network Topology           │            │
│  │ - Collector  │  │ - Traffic Simulation         │            │
│  │ - Extractor  │  │ - Fault Modeling             │            │
│  │ - Processor  │  │ - Communication Protocols    │            │
│  │              │  │ - HA Monitoring              │            │
│  └──────────────┘  └──────────────────────────────┘            │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                       Common Libraries                           │
│  - Model Registry  - Configuration  - Utilities                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. 计算执行单元 (Execution Unit)

#### 1.1 模型库 (Models)

**基础模型框架**
- `BaseModel`: 所有模型的抽象基类
- `ModelConfig`: 模型配置基类
- `ModelRegistry`: 模型注册和管理

**CPU模型**
- 支持架构: x86_64, ARM64, LoongArch, MIPS, RISC-V
- 国产CPU类型:
  - 龙芯系列: 3A5000, 3C5000
  - 飞腾系列: FT-2000, FT-2500
  - 兆芯: KX-6000
  - 海光: C86
- 特性:
  - 寄存器模拟
  - 指令计数
  - 周期精确模拟
  - 可配置主频和缓存

**内存模型**
- 可配置容量
- 读写操作模拟
- 访问计数统计
- 利用率监控

**总线模型**
- 支持总线类型:
  - FC (光纤通道)
  - RS422
  - ARINC429
  - CAN
  - Ethernet
  - PCI, I2C
- 特性:
  - 设备连接管理
  - 消息路由
  - 带宽模拟
  - 错误率模拟

**中断控制器**
- 可配置中断向量数
- 优先级管理
- 中断嵌套支持
- 周期性中断生成器

#### 1.2 系统加载器 (Loader)

支持的操作系统:
- VxWorks (实时操作系统)
- 银河麒麟 (Kylin)
- 统信UOS
- 开放麒麟 (OpenKylin)
- LoongArch Linux
- 深度操作系统 (Deepin)
- 中标麒麟 (NeoKylin)

功能:
- 操作系统镜像加载
- 启动参数配置
- 启动日志记录
- 生命周期管理

### 2. 执行环境构建单元 (Environment Building Unit)

#### 2.1 运行时环境 (Runtime)

**PrototypeRuntime**
- 模型生命周期管理
- 状态更新和同步
- 快照保存和恢复
- 跨平台支持

**RuntimeEngine**
- 多运行时实例管理
- 活动运行时切换
- 批量更新

特性:
- 可配置仿真速度
- 调试支持
- 状态导出/导入

### 3. 业务生成单元 (Business Generation Unit)

#### 3.1 生命周期管理 (Lifecycle)

**任务状态**
```
Created -> Configured -> Ready -> Running
                                    ↓
                                 Paused
                                    ↓
                              Terminated -> Archived
                                    ↓
                                Destroyed
```

**资源管理**
- CPU核心数
- 内存大小
- 存储空间
- 网络带宽
- GPU数量
- 自定义资源

**任务操作**
- 创建和配置
- 启动和停止
- 暂停和恢复
- 克隆和备份
- 归档和销毁

### 4. 数据分析单元 (Analysis Unit)

#### 4.1 数据采集 (Collector)

**采集模式**
- 按需采集 (On-demand)
- 抽样采集 (Sampling)
- 全量实时采集 (Full Realtime)
- 半流量实时采集 (Half Realtime)

**数据分类**
- 网络流量
- 系统指标
- 应用日志
- 性能数据

**流量分析**
- 源/目标地址统计
- 端口分析
- 协议分布
- IP类型分析

#### 4.2 数据提取 (Extractor)

支持格式:
- JSON
- XML
- CSV
- YAML

功能:
- 格式转换
- 文件导入/导出
- 批量处理

### 5. 执行管理单元 (Management Unit)

#### 5.1 网络拓扑 (Topology)

**拓扑类型**
- 星状 (Star)
- 环形 (Ring)
- 网状 (Mesh)
- 树形 (Tree)
- 总线 (Bus)
- 混合 (Hybrid)

**节点管理**
- 节点类型: 路由器、交换机、主机等
- 位置信息
- 配置管理
- 状态监控

**链路管理**
- 带宽配置
- 延迟模拟
- 丢包率设置
- 状态监控

**功能**
- 拓扑构建
- 路径查找
- 拓扑导出
- 统计分析

## 设计模式

### 1. 注册模式 (Registry Pattern)

模型注册表用于管理和创建模型实例:

```python
# 注册模型
registry.register("cpu", CPUModel)

# 创建模型实例
config = CPUConfig(...)
cpu = registry.create("cpu", config)
```

### 2. 观察者模式 (Observer Pattern)

数据采集器支持回调机制:

```python
def on_data_collected(data):
    process(data)

collector.add_callback(on_data_collected)
```

### 3. 策略模式 (Strategy Pattern)

不同的数据提取策略:

```python
json_extractor = JSONExtractor()
xml_extractor = XMLExtractor()
csv_extractor = CSVExtractor()
```

### 4. 构建者模式 (Builder Pattern)

拓扑构建器:

```python
topology = TopologyBuilder.build_star_topology(
    name="network",
    center_node=center,
    leaf_nodes=nodes
)
```

## 扩展机制

### 添加新模型

1. 继承 `BaseModel`
2. 实现必需方法
3. 注册到 `ModelRegistry`

```python
class CustomModel(BaseModel):
    def initialize(self) -> bool:
        # 实现初始化
        pass
    
    # 实现其他必需方法...

registry.register("custom", CustomModel)
```

### 添加新数据格式

1. 继承 `DataExtractor`
2. 实现提取和解析方法
3. 注册到导出服务

```python
class CustomExtractor(DataExtractor):
    def extract(self, data) -> str:
        # 实现数据提取
        pass
    
    def parse(self, content) -> Any:
        # 实现数据解析
        pass

service.register_extractor(DataFormat.CUSTOM, CustomExtractor())
```

## 性能考虑

### 优化策略

1. **批量处理**: 数据采集使用批量处理减少开销
2. **缓冲机制**: 总线消息使用队列缓冲
3. **懒加载**: 模型在需要时才初始化
4. **快照机制**: 定期保存状态避免重新计算

### 资源管理

1. **内存管理**: 及时清理不需要的数据
2. **并发控制**: 支持多运行时并发执行
3. **状态同步**: 最小化状态同步开销

## 安全性

### 数据保护

1. 敏感配置加密存储
2. 访问权限控制
3. 审计日志记录

### 模型隔离

1. 运行时环境隔离
2. 资源配额限制
3. 故障隔离

## 测试策略

### 单元测试

- 模型功能测试
- 接口兼容性测试
- 边界条件测试

### 集成测试

- 组件协作测试
- 端到端流程测试
- 性能测试

### 仿真验证

- 模型精度验证
- 时序正确性验证
- 负载测试

## 未来规划

1. **分布式仿真**: 支持多节点分布式仿真
2. **云原生支持**: 容器化部署和Kubernetes集成
3. **AI辅助**: 智能故障诊断和性能优化
4. **可视化**: Web界面和图形化建模工具
5. **更多模型**: 扩展硬件模型库
6. **标准化**: 支持行业标准接口和协议
