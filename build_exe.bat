@echo off
REM Build script for creating Windows executable
REM 构建Windows可执行文件的脚本

echo ==================================================
echo VirMachine - Windows Executable Build Script
echo 国产化虚拟样机 - Windows可执行文件构建脚本
echo ==================================================
echo.

REM Check if PyInstaller is installed
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo Building Windows executable...
echo 正在构建Windows可执行文件...
echo.

REM Build the executable
pyinstaller --clean virmachine.spec

if %errorlevel% == 0 (
    echo.
    echo ==================================================
    echo √ Build successful! / 构建成功！
    echo ==================================================
    echo.
    echo Executable location / 可执行文件位置:
    echo   dist\VirMachine.exe
    echo.
    echo You can now distribute this executable to Windows users.
    echo 现在可以将此可执行文件分发给Windows用户。
    echo.
) else (
    echo.
    echo ==================================================
    echo × Build failed! / 构建失败！
    echo ==================================================
    exit /b 1
)
