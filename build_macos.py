#!/usr/bin/env python3
"""macOS Build Script - Intel x86_64 Architecture
Usage: chmod +x build_macos.py && python3 build_macos.py
"""
import subprocess
import sys
import os
import platform
import shutil

def check_architecture():
    """Verify we're running on Intel x86_64"""
    arch = platform.machine()
    print(f"Current architecture: {arch}")
    
    if arch != 'x86_64':
        print(f"⚠️  Warning: Expected x86_64 but got {arch}")
        print("   This script is designed for Intel Macs.")
        print("   For ARM Macs, use Rosetta 2 or cross-compile.")
        return False
    return True

def build():
    print("=" * 50)
    print("柏慧学堂 macOS Build (Intel x86_64)")
    print("=" * 50)
    
    # Check architecture
    if not check_architecture():
        print("\n❌ Please run this script on an Intel Mac")
        sys.exit(1)
    
    # Change to project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Clean previous builds
    print("\n🧹 Cleaning previous builds...")
    for dir_name in ['build', 'dist', '__pycache__']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    for spec_file in ['柏慧学堂.spec']:
        if os.path.exists(spec_file):
            os.remove(spec_file)
    
    # Build command
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
    
    print(f"\n🔨 Building application...")
    print(f"   Command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"\n❌ Build failed!")
        print(f"STDERR: {result.stderr[-1000:]}")
        sys.exit(1)
    
    # Verify output
    output_path = 'dist/柏慧学堂'
    if os.path.exists(output_path):
        print(f"\n✅ Build successful!")
        print(f"📦 Output: {output_path}")
        size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"💾 Size: {size:.1f} MB")
        
        # Verify architecture
        try:
            verify = subprocess.run(['file', output_path], 
                                  capture_output=True, text=True)
            if verify.returncode == 0:
                print(f"\n📋 File info:")
                for line in verify.stdout.split('\n'):
                    print(f"   {line}")
                
                # Check for x86_64
                if 'x86_64' in verify.stdout:
                    print("\n✓ Confirmed: Intel x86_64 binary")
                elif 'arm64' in verify.stdout:
                    print("\n⚠️  Warning: ARM64 binary detected!")
                    print("   This may not run on your Intel Mac.")
        except Exception as e:
            print(f"⚠️  Verification skipped: {e}")
    else:
        print(f"\n❌ Output not found at {output_path}")
        sys.exit(1)

if __name__ == '__main__':
    build()
