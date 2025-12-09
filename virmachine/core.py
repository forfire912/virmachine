"""
核心模块 - 虚拟样机和组件定义
Core Module - Virtual Prototype and Component Definitions
"""

from typing import List, Dict, Any, Optional
import json
from datetime import datetime
from .localization import get_text


class Component:
    """
    组件类 - 表示虚拟样机的一个组成部分
    Component Class - Represents a part of the virtual prototype
    """
    
    def __init__(self, name: str, component_type: str, properties: Optional[Dict[str, Any]] = None):
        """
        初始化组件
        Initialize component
        
        Args:
            name: 组件名称 / Component name
            component_type: 组件类型 / Component type  
            properties: 组件属性 / Component properties
        """
        self.name = name
        self.component_type = component_type
        self.properties = properties or {}
        self.created_at = datetime.now()
        
    def set_property(self, key: str, value: Any) -> None:
        """设置组件属性 / Set component property"""
        self.properties[key] = value
        
    def get_property(self, key: str, default: Any = None) -> Any:
        """获取组件属性 / Get component property"""
        return self.properties.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式 / Convert to dictionary format"""
        return {
            'name': self.name,
            'type': self.component_type,
            'properties': self.properties,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self) -> str:
        return f"Component(name='{self.name}', type='{self.component_type}')"


class VirtualPrototype:
    """
    虚拟样机类 - 表示完整的虚拟产品模型
    Virtual Prototype Class - Represents a complete virtual product model
    """
    
    def __init__(self, name: str, description: str = ""):
        """
        初始化虚拟样机
        Initialize virtual prototype
        
        Args:
            name: 样机名称 / Prototype name
            description: 样机描述 / Prototype description
        """
        self.name = name
        self.description = description
        self.components: List[Component] = []
        self.metadata: Dict[str, Any] = {}
        self.created_at = datetime.now()
        self.version = "1.0.0"
        
    def add_component(self, component: Component) -> None:
        """
        添加组件到虚拟样机
        Add component to virtual prototype
        """
        self.components.append(component)
        
    def remove_component(self, component_name: str) -> bool:
        """
        从虚拟样机中移除组件
        Remove component from virtual prototype
        
        Returns:
            bool: 是否成功移除 / Whether removal was successful
        """
        for i, comp in enumerate(self.components):
            if comp.name == component_name:
                self.components.pop(i)
                return True
        return False
    
    def get_component(self, component_name: str) -> Optional[Component]:
        """
        获取指定名称的组件
        Get component by name
        """
        for comp in self.components:
            if comp.name == component_name:
                return comp
        return None
    
    def set_metadata(self, key: str, value: Any) -> None:
        """设置元数据 / Set metadata"""
        self.metadata[key] = value
        
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """获取元数据 / Get metadata"""
        return self.metadata.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式用于序列化
        Convert to dictionary format for serialization
        """
        return {
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'components': [comp.to_dict() for comp in self.components],
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat()
        }
    
    def to_json(self, filepath: str = None) -> str:
        """
        转换为JSON格式
        Convert to JSON format
        
        Args:
            filepath: 如果提供，将保存到文件 / If provided, will save to file
            
        Returns:
            str: JSON字符串 / JSON string
        """
        json_str = json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_str)
        return json_str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VirtualPrototype':
        """
        从字典创建虚拟样机
        Create virtual prototype from dictionary
        """
        prototype = cls(data['name'], data.get('description', ''))
        prototype.version = data.get('version', '1.0.0')
        prototype.metadata = data.get('metadata', {})
        
        for comp_data in data.get('components', []):
            component = Component(
                comp_data['name'],
                comp_data['type'],
                comp_data.get('properties', {})
            )
            prototype.add_component(component)
            
        return prototype
    
    @classmethod
    def from_json(cls, filepath: str) -> 'VirtualPrototype':
        """
        从JSON文件加载虚拟样机
        Load virtual prototype from JSON file
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def __repr__(self) -> str:
        return f"VirtualPrototype(name='{self.name}', components={len(self.components)})"
