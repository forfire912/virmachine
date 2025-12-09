# VirMachine Release Process
# 虚拟样机发布流程

## 概述 / Overview

本文档说明如何创建VirMachine的新版本发布，包括Windows可执行文件的自动构建。

This document explains how to create a new release of VirMachine, including automated Windows executable builds.

## 发布步骤 / Release Steps

### 1. 准备发布 / Prepare Release

确保所有更改已提交并推送到主分支：

Ensure all changes are committed and pushed to the main branch:

```bash
git status
git add .
git commit -m "Prepare for release v1.0.0"
git push origin main
```

### 2. 创建版本标签 / Create Version Tag

使用语义化版本号创建标签：

Create a tag using semantic versioning:

```bash
# 格式: vMAJOR.MINOR.PATCH
# Format: vMAJOR.MINOR.PATCH

git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 3. 自动构建流程 / Automated Build Process

当版本标签被推送后，GitHub Actions会自动执行以下操作：

When a version tag is pushed, GitHub Actions automatically:

1. **构建Windows可执行文件** / Build Windows executable
   - 使用PyInstaller打包Python应用
   - 创建独立的.exe文件
   - 不需要Python运行时

2. **创建发布包** / Create distribution package
   - 包含VirMachine.exe
   - 包含README.md
   - 包含LICENSE
   - 打包为ZIP文件

3. **创建GitHub Release** / Create GitHub Release
   - 自动创建Release页面
   - 上传Windows可执行文件ZIP
   - 生成发布说明

### 4. 验证发布 / Verify Release

1. 访问 https://github.com/forfire912/virmachine/releases
2. 确认新版本已创建
3. 下载并测试Windows可执行文件
4. 验证所有功能正常工作

Visit https://github.com/forfire912/virmachine/releases
Confirm the new version is created
Download and test the Windows executable
Verify all features work correctly

## 手动构建 / Manual Build

如需手动构建Windows可执行文件：

To manually build the Windows executable:

### Windows系统 / On Windows:

```cmd
# 1. 安装依赖 / Install dependencies
pip install pyinstaller
pip install -e .

# 2. 运行构建脚本 / Run build script
build_exe.bat

# 3. 测试可执行文件 / Test executable
dist\VirMachine.exe
```

### Linux/Mac系统 / On Linux/Mac:

```bash
# 1. 安装依赖 / Install dependencies
pip install pyinstaller
pip install -e .

# 2. 运行构建脚本 / Run build script
chmod +x build_exe.sh
./build_exe.sh

# 3. 输出位置 / Output location
ls -lh dist/VirMachine.exe
```

## 发布检查清单 / Release Checklist

在创建新发布之前，请确保：

Before creating a new release, ensure:

- [ ] 所有测试通过 / All tests pass
- [ ] 文档已更新 / Documentation updated
- [ ] 版本号已更新 / Version numbers updated
  - [ ] `setup.py`
  - [ ] `virmachine/__init__.py`
  - [ ] `version_info.txt`
- [ ] CHANGELOG.md已更新 / CHANGELOG.md updated
- [ ] 功能已在本地测试 / Features tested locally
- [ ] 代码审查完成 / Code review completed

## 版本号规则 / Version Numbering

使用语义化版本：MAJOR.MINOR.PATCH

Use semantic versioning: MAJOR.MINOR.PATCH

- **MAJOR**: 不兼容的API更改 / Incompatible API changes
- **MINOR**: 向后兼容的功能添加 / Backward-compatible feature additions
- **PATCH**: 向后兼容的问题修复 / Backward-compatible bug fixes

## 回滚发布 / Rollback Release

如果发布有问题，可以删除标签和发布：

If there's an issue with a release, you can delete the tag and release:

```bash
# 删除远程标签 / Delete remote tag
git push --delete origin v1.0.0

# 删除本地标签 / Delete local tag
git tag -d v1.0.0

# 然后在GitHub上手动删除Release
# Then manually delete the Release on GitHub
```

## 故障排除 / Troubleshooting

### 构建失败 / Build Fails

1. 检查GitHub Actions日志
2. 确保所有依赖已正确安装
3. 验证virmachine.spec文件配置

Check GitHub Actions logs
Ensure all dependencies are correctly installed
Verify virmachine.spec file configuration

### 可执行文件无法运行 / Executable Won't Run

1. 检查Windows Defender或杀毒软件
2. 确保在Windows 10/11上运行
3. 尝试以管理员权限运行

Check Windows Defender or antivirus
Ensure running on Windows 10/11
Try running with administrator privileges

## 联系方式 / Contact

如有问题，请提交Issue:
For issues, please submit an Issue:

https://github.com/forfire912/virmachine/issues
