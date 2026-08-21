#!/bin/bash
# 柏慧学堂 macOS 打包脚本
# 使用方法: chmod +x build_macos.sh && ./build_macos.sh

set -e

echo "🚀 柏慧学堂 macOS 打包脚本"
echo "=========================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装"
    exit 1
fi

PYTHON=$(which python3)
echo "📍 Python: $PYTHON ($($PYTHON --version))"

# 检查PyInstaller
if ! $PYTHON -m PyInstaller --version &> /dev/null; then
    echo "📦 安装 PyInstaller..."
    $PYTHON -m pip install pyinstaller customtkinter Pillow requests
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
    rm -rf build dist
fi

# 执行打包
echo "📦 运行 PyInstaller..."
$PYTHON -m PyInstaller \
    --name="柏慧学堂" \
    --noconfirm \
    --clean \
    --windowed \
    --add-data="config:config" \
    --add-data="core:core" \
    --add-data="ui:ui" \
    --add-data="resources:resources" \
    --hidden-import=customtkinter \
    --hidden-import=PIL \
    --exclude-module=matplotlib \
    --exclude-module=numpy \
    --exclude-module=pandas \
    --exclude-module=pytest \
    run_app.py

echo ""
echo "✅ 打包完成！"
echo ""
echo "📂 输出位置:"
echo "   app: dist/柏慧学堂/柏慧学堂.app"
echo ""
echo "🚀 运行方式:"
echo "   open dist/柏慧学堂/柏慧学堂.app"
echo ""
echo "📋 分发说明:"
echo "   1. 复制到macOS设备"
echo "   2. 打开终端执行: open 柏慧学堂.app"
echo "   3. 首次运行可能需要右键→打开以绕过Gatekeeper"
echo ""

# 验证输出
if [ -f "dist/柏慧学堂/柏慧学堂.app" ]; then
    SIZE=$(du -sh "dist/柏慧学堂/柏慧学堂.app" | cut -f1)
    echo "📊 App大小: $SIZE"
fi
