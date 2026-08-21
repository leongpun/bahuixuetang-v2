#!/usr/bin/env python3
# macOS打包脚本
import subprocess
import sys
import os

def build():
    print("开始打包macOS应用...")
    
    # 确保在正确目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 打包命令
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name=柏慧学堂',
        '--add-data', 'config:config',
        '--add-data', 'ui:ui',
        '--add-data', 'core:core',
        '--hidden-import=customtkinter',
        '--hidden-import=requests',
        '--hidden-import=PIL',
        'run_app.py'
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✅ macOS应用打包成功！")
        print("📦 输出位置: dist/柏慧学堂.app")
    else:
        print(f"\n❌ 打包失败: {result.stderr[-500:]}")
        sys.exit(1)

if __name__ == '__main__':
    build()
