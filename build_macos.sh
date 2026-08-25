#!/bin/bash
# 柏慧学堂 macOS 打包脚本 (Intel x86_64)
# 使用方法: chmod +x build_macos.sh && ./build_macos.sh

set -e

echo "🚀 柏慧学堂 macOS 打包脚本 (Intel x86_64)"
echo "================================================"

# 检查架构
ARCH=$(uname -m)
echo "系统架构: $ARCH"

if [ "$ARCH" != "x86_64" ]; then
    echo "⚠️  警告: 当前架构为 $ARCH，此脚本专为 Intel Mac 设计"
    echo "   如需在 ARM Mac 上运行，请使用 Rosetta 2:"
    echo "   softwareupdate --install-rosetta"
    echo "   rosetta2 bash build_macos.sh"
fi

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装"
    echo "   brew install python@3.12"
    exit 1
fi

PYTHON=$(which python3)
echo "📍 Python: $PYTHON ($($PYTHON --version 2>&1))"

# 检查PyInstaller
if ! $PYTHON -m PyInstaller --version &> /dev/null; then
    echo "📦 安装 PyInstaller..."
    $PYTHON -m pip install --upgrade pip
    $PYTHON -m pip install pyinstaller==6.4.0
fi

# 进入项目目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "🔧 开始打包..."
echo "   项目目录: $SCRIPT_DIR"
echo ""

# 清理旧构建
if [ -d "build" ]; then
    echo "🗑️  清理旧构建目录..."
    rm -rf build dist *.spec
fi

# 执行打包
echo "📦 运行 PyInstaller..."
$PYTHON -m PyInstaller \
    --onefile \
    --windowed \
    --name "柏慧学堂" \
    --osx-bundle-identifier com.baihuixuetang.app \
    --clean \
    --noconfirm \
    run_app.py

# 验证产物
echo ""
echo "✅ 构建完成！"
echo "📦 输出位置: dist/柏慧学堂"

if [ -f "dist/柏慧学堂" ]; then
    SIZE=$(ls -lh dist/柏慧学堂 | awk '{print $5}')
    echo "💾 文件大小: $SIZE"
    
    echo ""
    echo "📋 文件信息:"
    file dist/柏慧学堂
    
    # 验证架构
    if file dist/柏慧学堂 | grep -q "x86_64"; then
        echo "✓ 确认: Intel x86_64 二进制文件"
    else
        echo "⚠️  请手动验证架构"
    fi
else
    echo "❌ 构建失败：未找到输出文件"
    exit 1
fi

echo ""
echo "🎉 一键运行:"
echo "   open dist/柏慧学堂"
echo ""
echo "📱 分发方法:"
echo "   cd dist"
echo "   zip -r 柏慧学堂_macos.zip 柏慧学堂"
echo "   # 传输到目标设备后解压运行"
