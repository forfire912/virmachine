"""
单元测试 - 虚拟样机核心功能
Unit Tests - Virtual Prototype Core Functions
"""

import unittest
import json
import tempfile
import os
from virmachine import VirtualPrototype, Component, Simulator, set_language, get_text


class TestComponent(unittest.TestCase):
    """测试组件类 / Test Component class"""
    
    def test_component_creation(self):
        """测试组件创建 / Test component creation"""
        comp = Component("测试组件", "test_type", {"prop1": "value1"})
        self.assertEqual(comp.name, "测试组件")
        self.assertEqual(comp.component_type, "test_type")
        self.assertEqual(comp.properties["prop1"], "value1")
    
    def test_component_properties(self):
        """测试组件属性操作 / Test component property operations"""
        comp = Component("测试", "type")
        comp.set_property("key1", "value1")
        self.assertEqual(comp.get_property("key1"), "value1")
        self.assertIsNone(comp.get_property("nonexistent"))
        self.assertEqual(comp.get_property("nonexistent", "default"), "default")
    
    def test_component_to_dict(self):
        """测试组件转字典 / Test component to dict conversion"""
        comp = Component("测试", "type", {"prop": "val"})
        data = comp.to_dict()
        self.assertEqual(data["name"], "测试")
        self.assertEqual(data["type"], "type")
        self.assertEqual(data["properties"]["prop"], "val")


class TestVirtualPrototype(unittest.TestCase):
    """测试虚拟样机类 / Test VirtualPrototype class"""
    
    def test_prototype_creation(self):
        """测试虚拟样机创建 / Test prototype creation"""
        proto = VirtualPrototype("测试样机", "测试描述")
        self.assertEqual(proto.name, "测试样机")
        self.assertEqual(proto.description, "测试描述")
        self.assertEqual(len(proto.components), 0)
    
    def test_add_remove_component(self):
        """测试添加和移除组件 / Test add and remove component"""
        proto = VirtualPrototype("测试")
        comp1 = Component("组件1", "type1")
        comp2 = Component("组件2", "type2")
        
        proto.add_component(comp1)
        proto.add_component(comp2)
        self.assertEqual(len(proto.components), 2)
        
        result = proto.remove_component("组件1")
        self.assertTrue(result)
        self.assertEqual(len(proto.components), 1)
        
        result = proto.remove_component("不存在")
        self.assertFalse(result)
    
    def test_get_component(self):
        """测试获取组件 / Test get component"""
        proto = VirtualPrototype("测试")
        comp = Component("目标组件", "type")
        proto.add_component(comp)
        
        found = proto.get_component("目标组件")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "目标组件")
        
        not_found = proto.get_component("不存在")
        self.assertIsNone(not_found)
    
    def test_metadata(self):
        """测试元数据操作 / Test metadata operations"""
        proto = VirtualPrototype("测试")
        proto.set_metadata("key1", "value1")
        proto.set_metadata("key2", 123)
        
        self.assertEqual(proto.get_metadata("key1"), "value1")
        self.assertEqual(proto.get_metadata("key2"), 123)
        self.assertIsNone(proto.get_metadata("nonexistent"))
    
    def test_save_load_json(self):
        """测试JSON保存和加载 / Test JSON save and load"""
        proto = VirtualPrototype("测试样机", "描述")
        proto.add_component(Component("组件1", "type1", {"prop": "val"}))
        proto.set_metadata("meta_key", "meta_value")
        
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            proto.to_json(filepath)
            
            # 加载
            loaded = VirtualPrototype.from_json(filepath)
            self.assertEqual(loaded.name, "测试样机")
            self.assertEqual(loaded.description, "描述")
            self.assertEqual(len(loaded.components), 1)
            self.assertEqual(loaded.get_metadata("meta_key"), "meta_value")
            self.assertEqual(loaded.components[0].name, "组件1")
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)


class TestSimulator(unittest.TestCase):
    """测试仿真器类 / Test Simulator class"""
    
    def test_simulator_creation(self):
        """测试仿真器创建 / Test simulator creation"""
        sim = Simulator()
        self.assertEqual(len(sim.results), 0)
        self.assertEqual(len(sim.test_functions), 0)
    
    def test_run_simulation(self):
        """测试运行仿真 / Test run simulation"""
        proto = VirtualPrototype("测试")
        proto.add_component(Component("组件1", "type1"))
        
        sim = Simulator()
        result = sim.run_simulation(proto)
        
        self.assertTrue(result.success)
        self.assertEqual(len(sim.results), 1)
        self.assertEqual(result.data["component_count"], 1)
    
    def test_empty_prototype_simulation(self):
        """测试空样机仿真 / Test empty prototype simulation"""
        proto = VirtualPrototype("空样机")
        sim = Simulator()
        result = sim.run_simulation(proto)
        
        self.assertFalse(result.success)
    
    def test_stress_test(self):
        """测试压力测试 / Test stress test"""
        proto = VirtualPrototype("测试")
        proto.add_component(Component("组件", "type"))
        
        sim = Simulator()
        result = sim.run_stress_test(proto, stress_level=5.0)
        
        self.assertTrue(result.success)
        self.assertEqual(result.data["parameters"]["stress_level"], 5.0)
    
    def test_performance_test(self):
        """测试性能测试 / Test performance test"""
        proto = VirtualPrototype("测试")
        proto.add_component(Component("组件", "type"))
        
        sim = Simulator()
        result = sim.run_performance_test(proto)
        
        self.assertTrue(result.success)
        self.assertEqual(result.data["parameters"]["test_type"], "performance")
    
    def test_custom_test_function(self):
        """测试自定义测试函数 / Test custom test function"""
        def custom_test(component, params):
            return {"custom_result": "passed"}
        
        proto = VirtualPrototype("测试")
        proto.add_component(Component("组件", "custom_type"))
        
        sim = Simulator()
        sim.register_test("custom_type", custom_test)
        result = sim.run_simulation(proto)
        
        self.assertTrue(result.success)
        components_tested = result.data["components_tested"]
        self.assertEqual(components_tested[0]["custom_test"]["custom_result"], "passed")


class TestLocalization(unittest.TestCase):
    """测试本地化功能 / Test localization features"""
    
    def test_set_language(self):
        """测试设置语言 / Test set language"""
        set_language('zh_CN')
        self.assertEqual(get_text('success'), '成功')
        
        set_language('en_US')
        self.assertEqual(get_text('success'), 'Success')
    
    def test_invalid_language(self):
        """测试无效语言 / Test invalid language"""
        with self.assertRaises(ValueError):
            set_language('invalid_lang')
    
    def test_get_text_default(self):
        """测试获取不存在的文本 / Test get text with default"""
        set_language('zh_CN')
        result = get_text('nonexistent_key', 'default_value')
        self.assertEqual(result, 'default_value')


if __name__ == '__main__':
    unittest.main()
