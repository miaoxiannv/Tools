# build_with_pyinstaller.py
import PyInstaller.__main__

PyInstaller.__main__.run([
    'gui_module.py',
    '--name=Franklin',
    '--onefile',
    '--windowed',
    '--add-data=config.json;.',
    '--icon=NONE',
    '--clean',
    '--noconfirm'
])
