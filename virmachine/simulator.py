"""
仿真模块 - 虚拟样机仿真和测试
Simulation Module - Virtual Prototype Simulation and Testing
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from .core import VirtualPrototype, Component
from .localization import get_text


class SimulationResult:
    """
    仿真结果类
    Simulation Result Class
    """
    
    def __init__(self, success: bool, message: str, data: Optional[Dict[str, Any]] = None):
        """
        初始化仿真结果
        Initialize simulation result
        
        Args:
            success: 是否成功 / Whether successful
            message: 结果消息 / Result message
            data: 结果数据 / Result data
        """
        self.success = success
        self.message = message
        self.data = data or {}
        self.timestamp = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式 / Convert to dictionary format"""
        return {
            'success': self.success,
            'message': self.message,
            'data': self.data,
            'timestamp': self.timestamp.isoformat()
        }
    
    def __repr__(self) -> str:
        status = get_text('success') if self.success else get_text('error')
        return f"SimulationResult({status}: {self.message})"


class Simulator:
    """
    仿真器类 - 执行虚拟样机仿真
    Simulator Class - Execute virtual prototype simulations
    """
    
    def __init__(self):
        """初始化仿真器 / Initialize simulator"""
        self.results: List[SimulationResult] = []
        self.test_functions: Dict[str, Callable] = {}
        
    def register_test(self, name: str, test_func: Callable) -> None:
        """
        注册测试函数
        Register test function
        
        Args:
            name: 测试名称 / Test name
            test_func: 测试函数 / Test function
        """
        self.test_functions[name] = test_func
        
    def run_simulation(self, prototype: VirtualPrototype, 
                      simulation_type: str = "basic",
                      parameters: Optional[Dict[str, Any]] = None) -> SimulationResult:
        """
        运行仿真
        Run simulation
        
        Args:
            prototype: 虚拟样机 / Virtual prototype
            simulation_type: 仿真类型 / Simulation type
            parameters: 仿真参数 / Simulation parameters
            
        Returns:
            SimulationResult: 仿真结果 / Simulation result
        """
        parameters = parameters or {}
        
        try:
            # 基础验证
            if not prototype.components:
                return SimulationResult(
                    False,
                    f"{get_text('error')}: 虚拟样机没有组件 / No components in prototype",
                    {}
                )
            
            # 执行仿真
            result_data = {
                'prototype_name': prototype.name,
                'simulation_type': simulation_type,
                'component_count': len(prototype.components),
                'parameters': parameters,
                'components_tested': []
            }
            
            # 测试每个组件
            for component in prototype.components:
                component_result = self._test_component(component, parameters)
                result_data['components_tested'].append(component_result)
            
            result = SimulationResult(
                True,
                f"{get_text('simulation_completed')} - {simulation_type}",
                result_data
            )
            
        except Exception as e:
            result = SimulationResult(
                False,
                f"{get_text('error')}: {str(e)}",
                {'error': str(e)}
            )
        
        self.results.append(result)
        return result
    
    def _test_component(self, component: Component, 
                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        测试组件
        Test component
        
        Args:
            component: 组件 / Component
            parameters: 测试参数 / Test parameters
            
        Returns:
            Dict: 测试结果 / Test result
        """
        result = {
            'component_name': component.name,
            'component_type': component.component_type,
            'status': 'passed',
            'properties_validated': len(component.properties)
        }
        
        # 如果有注册的测试函数，执行它
        if component.component_type in self.test_functions:
            try:
                test_result = self.test_functions[component.component_type](component, parameters)
                result['custom_test'] = test_result
            except Exception as e:
                result['status'] = 'failed'
                result['error'] = str(e)
        
        return result
    
    def run_stress_test(self, prototype: VirtualPrototype,
                       stress_level: float = 1.0) -> SimulationResult:
        """
        运行压力测试
        Run stress test
        
        Args:
            prototype: 虚拟样机 / Virtual prototype
            stress_level: 压力等级 (0.0-10.0) / Stress level (0.0-10.0)
            
        Returns:
            SimulationResult: 测试结果 / Test result
        """
        parameters = {
            'stress_level': stress_level,
            'test_type': 'stress'
        }
        
        return self.run_simulation(prototype, "stress_test", parameters)
    
    def run_performance_test(self, prototype: VirtualPrototype) -> SimulationResult:
        """
        运行性能测试
        Run performance test
        
        Args:
            prototype: 虚拟样机 / Virtual prototype
            
        Returns:
            SimulationResult: 测试结果 / Test result
        """
        parameters = {
            'test_type': 'performance',
            'metrics': ['speed', 'efficiency', 'reliability']
        }
        
        return self.run_simulation(prototype, "performance_test", parameters)
    
    def get_results(self) -> List[SimulationResult]:
        """
        获取所有仿真结果
        Get all simulation results
        
        Returns:
            List[SimulationResult]: 仿真结果列表 / List of simulation results
        """
        return self.results
    
    def clear_results(self) -> None:
        """清除所有仿真结果 / Clear all simulation results"""
        self.results.clear()
    
    def __repr__(self) -> str:
        return f"Simulator(results={len(self.results)}, tests={len(self.test_functions)})"
