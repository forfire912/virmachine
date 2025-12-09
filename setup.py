#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VirMachine - 国产化虚拟样机系统
Virtual Prototype System for Domestic Computing
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="virmachine",
    version="0.1.0",
    author="VirMachine Team",
    description="国产化虚拟样机系统 - Domestic Virtual Prototype System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/forfire912/virmachine",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Emulators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "click>=8.0",
        "rich>=10.0",
        "pydantic>=2.0",
        "networkx>=2.6",
        "pyzmq>=24.0",
        "aiohttp>=3.8",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "pytest-asyncio>=0.20",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "virmachine=virmachine.cli:main",
        ],
    },
)
