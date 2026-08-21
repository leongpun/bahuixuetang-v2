# 柏慧学堂 macOS 版打包指南

## 📋 系统要求
- macOS 10.14 (Mojave) 或更高版本
- Python 3.10+
- 约 200MB 可用磁盘空间

## 🚀 快速开始

### 1. 准备环境
```bash
# 安装Python（如果没有）
brew install python@3.12

# 安装依赖
pip3 install customtkinter Pillow openpyxl python-docx pyinstaller
```

### 2. 运行打包脚本
```bash
cd /path/to/baihuixuetang_v2
chmod +x build_macos.sh
./build_macos.sh
```

### 3. 验证和运行
```bash
# 检查生成的App
ls -lh dist/柏慧学堂/柏慧学堂.app

# 运行应用
open dist/柏慧学堂/柏慧学堂.app
```

## 📦 分发方式

### 方法1: 直接分发App Bundle
```bash
# 压缩App
cd dist
zip -r 柏慧学堂_v2.0_macos.zip 柏慧学堂.app

# 传输到目标macOS设备后解压运行
unzip 柏慧学堂_v2.0_macos.zip
open 柏慧学堂.app
```

### 方法2: 使用Notarize（推荐，避免Gatekeeper警告）
```bash
# 代码签名
codesign --sign "你的开发者ID" --force --deep dist/柏慧学堂/柏慧学堂.app

# Notarize（需要Apple Developer账号）
xcrun notarytool submit dist/柏慧学堂/柏慧学堂.app \
  --apple-id your@apple.com \
  --password @keychain:AC_PASSWORD \
  --team-id TEAMID

#  Staple（绑定签名到App）
xcrun stapler staple dist/柏慧学堂/柏慧学堂.app
```

## ⚠️ 注意事项

### Gatekeeper问题
首次运行时可能遇到"无法打开，因为无法验证开发者"：
1. 右键点击App → 打开
2. 在弹出的对话框中点击"打开"

### 资源路径配置
App启动后需要配置本地资源路径：
- 点击左侧"设置"菜单
- 设置"空中课堂"视频目录（如 `/Volumes/你的硬盘/空中课堂`）
- 设置"初中课本"PDF目录（可选）

## 🔧 常见问题

### Q: 打包后App打不开？
A: 检查Python版本兼容性，建议使用Python 3.10-3.12

### Q: 视频无法播放？
A: macOS默认使用QuickTime Player，支持MP4格式

### Q: 中文显示乱码？
A: 确保系统语言设置为中文，或使用英文界面

## 📊 文件大小预估
- 基础打包: ~150MB
- 包含完整依赖: ~200-250MB
