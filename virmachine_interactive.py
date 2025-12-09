#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虚拟样机系统 - 交互式启动脚本
VirMachine - Interactive Launcher

快速启动交互式界面
Quick launch for interactive interface
"""

if __name__ == "__main__":
    try:
        from virmachine.interactive import main
        main()
    except ImportError:
        print("错误: 请先安装 virmachine 包")
        print("Error: Please install virmachine package first")
        print("\n运行: pip install -e .")
        print("Run: pip install -e .")
