import sys
from cx_Freeze import setup, Executable

# 指定要打包的主程序
main_script = "gui_module.py"  # 修改为您的主程序文件名

# 依赖包
build_exe_options = {
    "packages": ["os", "json", "openai", "typing", "tkinter", "threading"],
    "excludes": ["tkinter.test", "unittest"],
    "include_files": [],
}

# 创建 base
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="Franklin-Research-Assistant",
    version="1.0",
    description="Franklin Research Assistant - Paper Analysis Tool",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            main_script,
            base=base,
            target_name="Franklin.exe",
            icon=None  # 如果有图标文件，可以在这里指定路径
        )
    ]
)
