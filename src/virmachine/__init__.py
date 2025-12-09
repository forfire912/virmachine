#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VirMachine - 国产化虚拟样机系统
Virtual Prototype System for Domestic Computing
"""

__version__ = "0.1.0"
__author__ = "VirMachine Team"
__all__ = [
    "execution",
    "environment",
    "business",
    "analysis",
    "management",
]

from . import execution
from . import environment
from . import business
from . import analysis
from . import management
