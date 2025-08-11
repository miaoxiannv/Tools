"""
ArXiv LLM 论文摘要生成器 - 打包脚本
使用PyInstaller将应用程序打包成exe文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """安装PyInstaller"""
    print("📦 正在安装PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller安装成功！")
        return True
    except subprocess.CalledProcessError:
        print("❌ PyInstaller安装失败！")
        return False

def create_spec_file():
    """创建PyInstaller配置文件"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

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
        'arxiv',
        'openai',
        'PySide6.QtCore',
        'PySide6.QtWidgets',
        'PySide6.QtGui',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
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
        'setuptools',
        'distutils',
        'email',
        'xml',
        'unittest',
        'test',
        'tests',
        'doctest',
        'pydoc',
        'sqlite3',
        'multiprocessing',
        'concurrent',
        'asyncio',
        'queue',
        'threading',
        'subprocess',
        'pickle',
        'shelve',
        'dbm',
        'csv',
        'html',
        'http',
        'urllib',
        'ftplib',
        'smtplib',
        'poplib',
        'imaplib',
        'nntplib',
        'telnetlib',
        'socketserver',
        'xmlrpc',
        'wsgiref',
        'webbrowser',
        'cgi',
        'cgitb',
        'pprint',
        'reprlib',
        'difflib',
        'textwrap',
        'unicodedata',
        'stringprep',
        'readline',
        'rlcompleter',
        'cmd',
        'shlex',
        'getopt',
        'argparse',
        'logging',
        'getpass',
        'curses',
        'platform',
        'errno',
        'ctypes',
        'mmap',
        'winreg',
        'msvcrt',
        'winsound',
        'locale',
        'calendar',
        'collections',
        'heapq',
        'bisect',
        'array',
        'weakref',
        'types',
        'copy',
        'pprint',
        'reprlib',
        'enum',
        'numbers',
        'math',
        'cmath',
        'decimal',
        'fractions',
        'random',
        'statistics',
        'itertools',
        'functools',
        'operator',
        'pathlib',
        'os.path',
        'fileinput',
        'stat',
        'filecmp',
        'tempfile',
        'glob',
        'fnmatch',
        'linecache',
        'shutil',
        'macpath',
        'zipfile',
        'tarfile',
        'gzip',
        'bz2',
        'lzma',
        'zlib',
        'hashlib',
        'hmac',
        'secrets',
        'ssl',
        'socket',
        'select',
        'selectors',
        'signal',
        'mmap',
        'contextlib',
        'abc',
        'atexit',
        'traceback',
        'future',
        'gc',
        'inspect',
        'site',
        'user',
        'builtins',
        'warnings',
        'dataclasses',
        'contextlib',
        'importlib',
        'pkgutil',
        'modulefinder',
        'runpy',
        'parser',
        'ast',
        'symtable',
        'symbol',
        'token',
        'keyword',
        'tokenize',
        'tabnanny',
        'pyclbr',
        'py_compile',
        'compileall',
        'dis',
        'pickletools',
        'formatter',
        'msilib',
        'msvcrt',
        'winreg',
        'winsound'
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
    upx=True,
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
    
    with open('arxiv_llm.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content.strip())
    
    print("✅ 已创建PyInstaller配置文件: arxiv_llm.spec")

def create_version_info():
    """创建版本信息文件"""
    version_info = '''
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2,0,0,0),
    prodvers=(2,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'080404B0',
        [StringStruct(u'CompanyName', u'ArXiv Tools'),
        StringStruct(u'FileDescription', u'ArXiv LLM 论文摘要生成器'),
        StringStruct(u'FileVersion', u'2.0.0.0'),
        StringStruct(u'InternalName', u'ArXiv_LLM_Generator'),
        StringStruct(u'LegalCopyright', u'Copyright © 2025 ArXiv Tools'),
        StringStruct(u'OriginalFilename', u'ArXiv_LLM_论文摘要生成器.exe'),
        StringStruct(u'ProductName', u'ArXiv LLM 论文摘要生成器'),
        StringStruct(u'ProductVersion', u'2.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [2052, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info.strip())
    
    print("✅ 已创建版本信息文件: version_info.txt")

def create_icon():
    """创建应用程序图标（如果不存在）"""
    if not os.path.exists('icon.ico'):
        print("⚠️  未找到icon.ico文件，将使用默认图标")
        print("💡 提示：您可以将自定义的icon.ico文件放在项目根目录下")

def build_exe():
    """构建exe文件"""
    print("🔨 开始构建exe文件...")
    
    try:
        # 清理之前的构建文件
        if os.path.exists('build'):
            shutil.rmtree('build')
            print("🧹 已清理build目录")
        
        if os.path.exists('dist'):
            shutil.rmtree('dist')
            print("🧹 已清理dist目录")
        
        # 运行PyInstaller
        cmd = [sys.executable, "-m", "PyInstaller", "arxiv_llm.spec", "--clean"]
        subprocess.check_call(cmd)
        
        print("✅ exe文件构建成功！")
        print(f"📁 输出目录: {os.path.abspath('dist')}")
        
        # 检查生成的文件
        exe_path = os.path.join('dist', 'ArXiv_LLM_论文摘要生成器.exe')
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"📊 文件大小: {file_size:.1f} MB")
            print(f"🎯 可执行文件: {exe_path}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

def create_installer_script():
    """创建安装脚本"""
    installer_content = '''
@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   ArXiv LLM 论文摘要生成器 v2.0
echo   一键安装脚本
echo ========================================
echo.

echo 📦 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python环境，请先安装Python 3.8+
    echo 💡 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境检查通过

echo.
echo 📦 正在安装依赖包...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ 依赖包安装失败
    pause
    exit /b 1
)

echo ✅ 依赖包安装完成

echo.
echo 🚀 正在启动应用程序...
python gui.py

pause
'''
    
    with open('install_and_run.bat', 'w', encoding='utf-8') as f:
        f.write(installer_content.strip())
    
    print("✅ 已创建安装脚本: install_and_run.bat")

def main():
    """主函数"""
    print("🚀 ArXiv LLM 论文摘要生成器 - 打包工具")
    print("=" * 50)
    
    # 检查必要文件
    required_files = ['gui.py', 'arxiv_digest.py', 'requirements.txt']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺少必要文件: {file}")
            return False
    
    print("✅ 必要文件检查通过")
    
    # 安装PyInstaller
    if not install_pyinstaller():
        return False
    
    # 创建配置文件
    create_spec_file()
    create_version_info()
    create_icon()
    create_installer_script()
    
    # 构建exe
    if build_exe():
        print("\n🎉 打包完成！")
        print("\n📋 生成的文件:")
        print("  📁 dist/ArXiv_LLM_论文摘要生成器.exe - 可执行文件")
        print("  📄 install_and_run.bat - 源码运行脚本")
        print("  📄 arxiv_llm.spec - PyInstaller配置文件")
        print("  📄 version_info.txt - 版本信息文件")
        
        print("\n💡 使用说明:")
        print("  1. 直接运行 dist/ArXiv_LLM_论文摘要生成器.exe")
        print("  2. 或者双击 install_and_run.bat 从源码运行")
        
        return True
    else:
        print("\n❌ 打包失败！")
        return False

if __name__ == "__main__":
    success = main()
    input("\n按任意键退出...")
    sys.exit(0 if success else 1)
