#!/usr/bin/env python3
# macOS打包脚本 - Intel x86_64架构
import subprocess
import sys
import os
import platform

def build():
    print("开始打包macOS应用（Intel x86_64）...")
    
    # 确保在正确目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 检查系统架构
    arch = platform.machine()
    print(f"当前系统架构: {arch}")
    
    if arch != 'x86_64':
        print("⚠️ 警告：当前不是Intel x86_64架构")
        print("   请在Intel Mac或虚拟机上运行此脚本")
    
    # 打包命令
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', '柏慧学堂',
        '--osx-bundle-identifier', 'com.baihuixuetang.app',
        '--clean',
        '--noconfirm',
        'run_app.py'
    ]
    
    print(f"\n执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✅ macOS应用打包成功！")
        print("📦 输出位置: dist/柏慧学堂")
        
        # 验证架构
        try:
            verify = subprocess.run(['file', 'dist/柏慧学堂'], 
                                  capture_output=True, text=True)
            if verify.returncode == 0:
                print(f"\n文件信息:\n{verify.stdout}")
        except Exception as e:
            print(f"验证失败: {e}")
    else:
        print(f"\n❌ 打包失败: {result.stderr[-500:]}")
        sys.exit(1)

if __name__ == '__main__':
    build()
