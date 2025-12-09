#!/bin/bash
# Build script for creating Windows executable
# 构建Windows可执行文件的脚本

echo "=================================================="
echo "VirMachine - Windows Executable Build Script"
echo "国产化虚拟样机 - Windows可执行文件构建脚本"
echo "=================================================="
echo ""

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

echo "Building Windows executable..."
echo "正在构建Windows可执行文件..."
echo ""

# Build the executable
pyinstaller --clean virmachine.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✓ Build successful! / 构建成功！"
    echo "=================================================="
    echo ""
    echo "Executable location / 可执行文件位置:"
    echo "  dist/VirMachine.exe"
    echo ""
    echo "You can now distribute this executable to Windows users."
    echo "现在可以将此可执行文件分发给Windows用户。"
    echo ""
else
    echo ""
    echo "=================================================="
    echo "✗ Build failed! / 构建失败！"
    echo "=================================================="
    exit 1
fi
