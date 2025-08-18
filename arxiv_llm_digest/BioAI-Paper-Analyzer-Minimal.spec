# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['bio_ai_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['bio_ai_paper_analyzer', 'habanero', 'openai', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'tensorflow', 'numpy', 'pandas', 'scipy', 'matplotlib', 'PIL', 'cv2', 'sklearn', 'jupyter', 'IPython', 'notebook', 'tkinter', 'PyQt5', 'PyQt6', 'wx', 'kivy', 'pygame', 'plotly', 'seaborn', 'bokeh', 'dash', 'streamlit', 'fastapi', 'flask', 'django', 'sqlalchemy', 'psycopg2', 'pymongo', 'redis', 'celery', 'pytest', 'unittest', 'doctest'],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='BioAI-Paper-Analyzer-Minimal',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
