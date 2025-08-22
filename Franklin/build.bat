@echo off
echo Building Franklin Research Assistant...

:: 检查 Python 环境
python --version > nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

:: 安装依赖
echo Installing dependencies...
pip install -r requirements.txt

:: 清理旧的构建文件
echo Cleaning old build files...
if exist "build" rd /s /q "build"
if exist "dist" rd /s /q "dist"

:: 运行打包脚本
echo Building executable...
python build_exe.py build

:: 检查构建结果
if exist "build\exe.win-amd64-3.10\Franklin.exe" (
    echo Build successful! Executable created at build\exe.win-amd64-3.10\Franklin.exe
) else (
    echo Build failed! Please check the error messages above.
)

echo Done.
pause
