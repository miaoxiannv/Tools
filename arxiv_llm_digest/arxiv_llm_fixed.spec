# -*- mode: python ; coding: utf-8 -*-
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
