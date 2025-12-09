"""
虚拟样机系统 (Virtual Prototyping Machine System)
国产化虚拟样机平台 - 用于产品设计、仿真和测试

Virtual Prototyping Machine - A platform for product design, simulation and testing
"""

__version__ = "1.0.0"
__author__ = "VirMachine Team"

from .core import VirtualPrototype, Component
from .simulator import Simulator
from .localization import get_text, set_language
from .interactive import VirMachineInteractive

__all__ = [
    'VirtualPrototype',
    'Component', 
    'Simulator',
    'get_text',
    'set_language',
    'VirMachineInteractive'
]
