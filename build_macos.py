#!/usr/bin/env python3
# macOS打包脚本 - Universal Binary支持
import subprocess
import sys
import os

def build():
    print("开始打包macOS通用应用（Universal Binary）...")
    
    # 确保在正确目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 检查是否为Apple Silicon
    import platform
    is_arm = platform.machine() == 'arm64'
    print(f"检测到架构: {platform.machine()}")
    
    # 打包命令 - 支持多架构
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', '柏慧学堂',
        '--osx-bundle-identifier', 'com.baihuixuetang.app',
        'run_app.py'
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
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
        except:
            pass
    else:
        print(f"\n❌ 打包失败: {result.stderr[-500:]}")
        sys.exit(1)

if __name__ == '__main__':
    build()
