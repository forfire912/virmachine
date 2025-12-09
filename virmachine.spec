# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for building VirMachine Windows executable
国产化虚拟样机 - Windows可执行文件构建配置
"""

block_cipher = None

a = Analysis(
    ['virmachine_interactive.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('virmachine/*.py', 'virmachine'),
        ('README.md', '.'),
        ('LICENSE', '.'),
    ],
    hiddenimports=[
        'virmachine',
        'virmachine.core',
        'virmachine.simulator',
        'virmachine.localization',
        'virmachine.interactive',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VirMachine',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version='version_info.txt',
)
