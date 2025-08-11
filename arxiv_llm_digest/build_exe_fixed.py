#!/usr/bin/env python3
"""
修复版本的打包脚本
解决PySide6打包问题
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build():
    """清理之前的构建文件"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 清理.pyc文件
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def create_fixed_spec():
    """创建修复版本的spec文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('arxiv_digest.py', '.'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        # 核心依赖
        'arxiv',
        'openai',
        
        # PySide6 完整模块
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtWidgets', 
        'PySide6.QtGui',
        'PySide6.QtNetwork',
        'PySide6.QtOpenGL',
        'PySide6.QtPrintSupport',
        'PySide6.QtSvg',
        'PySide6.QtTest',
        'PySide6.QtXml',
        'shiboken6',
        
        # Python核心模块
        'importlib',
        'importlib.util',
        'importlib.machinery',
        'importlib.metadata',
        'importlib._bootstrap',
        'importlib._bootstrap_external',
        'site',
        'encodings',
        'encodings.utf_8',
        'encodings.cp1252',
        'encodings.latin_1',
        'encodings.ascii',
        'encodings.mbcs',
        
        # 系统相关
        'platform',
        'errno',
        'ctypes',
        'winreg',
        'msvcrt',
        'winsound',
        'locale',
        'collections',
        'types',
        'copy',
        'enum',
        'numbers',
        'math',
        'cmath',
        'random',
        'itertools',
        'functools',
        'operator',
        'pathlib',
        'os.path',
        'stat',
        'tempfile',
        'glob',
        'fnmatch',
        'linecache',
        'shutil',
        'hashlib',
        'hmac',
        'ssl',
        'socket',
        'contextlib',
        'abc',
        'traceback',
        'warnings',
        'dataclasses',
        'builtins',
        
        # 网络和HTTP
        'email',
        'xml',
        'html',
        'http',
        'urllib',
        'urllib.request',
        'urllib.parse',
        'urllib.error',
        
        # 线程和进程
        'threading',
        'subprocess',
        
        # 日志和参数解析
        'argparse',
        'logging',
        
        # 其他必需模块
        'pprint',
        'reprlib',
        'unicodedata',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 只排除明确不需要的大型库
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy', 
        'pandas',
        'PIL',
        'cv2',
        'torch',
        'tensorflow',
        'jupyter',
        'IPython',
        'notebook',
        'pytest',
    ],
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
    name='ArXiv_LLM_论文摘要生成器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 禁用UPX压缩，避免兼容性问题
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)
'''
    
    with open('arxiv_llm_fixed.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("创建修复版本的spec文件: arxiv_llm_fixed.spec")

def build_exe():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    try:
        # 使用修复版本的spec文件
        cmd = [sys.executable, '-m', 'PyInstaller', 'arxiv_llm_fixed.spec', '--clean']
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("构建成功!")
        print("输出:", result.stdout)
        
        # 检查生成的文件
        exe_path = Path('dist/ArXiv_LLM_论文摘要生成器.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"生成的可执行文件: {exe_path}")
            print(f"文件大小: {size_mb:.1f} MB")
        else:
            print("警告: 未找到生成的可执行文件")
            
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        print("错误输出:", e.stderr)
        return False
    
    return True

def main():
    """主函数"""
    print("=== ArXiv LLM 修复版打包脚本 ===")
    
    # 检查依赖
    try:
        import PyInstaller
        print(f"PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("错误: 未安装PyInstaller")
        print("请运行: pip install pyinstaller")
        return
    
    try:
        import PySide6
        print(f"PySide6版本: {PySide6.__version__}")
    except ImportError:
        print("错误: 未安装PySide6")
        print("请运行: pip install PySide6")
        return
    
    # 清理之前的构建
    clean_build()
    
    # 创建修复版本的spec文件
    create_fixed_spec()
    
    # 构建可执行文件
    if build_exe():
        print("\n=== 构建完成 ===")
        print("可执行文件位置: dist/ArXiv_LLM_论文摘要生成器.exe")
        print("\n修复内容:")
        print("1. 修复了PyQt5/PySide6混用问题")
        print("2. 添加了所有必需的PySide6模块")
        print("3. 包含了importlib等核心Python模块")
        print("4. 禁用了UPX压缩以避免兼容性问题")
        print("5. 减少了过度的模块排除")
    else:
        print("\n=== 构建失败 ===")
        print("请检查错误信息并重试")

if __name__ == "__main__":
    main()
