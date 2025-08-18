import PyInstaller.__main__
import os
import sys

def build_minimal_exe():
    """使用PyInstaller打包精简版生物学AI论文分析器"""
    
    # 确保在正确的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 精简版PyInstaller参数 - 排除大型不必要的库
    args = [
        'bio_ai_gui.py',                    # 主程序文件
        '--name=BioAI-Paper-Analyzer-Minimal',  # 可执行文件名
        '--onefile',                        # 打包成单个exe文件
        '--windowed',                       # 不显示控制台窗口
        '--hidden-import=bio_ai_paper_analyzer',  # 隐式导入核心模块
        '--hidden-import=habanero',         # Crossref库
        '--hidden-import=openai',           # OpenAI库
        '--hidden-import=PySide6.QtCore',   # 只包含必要的PySide6模块
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtWidgets',
        '--exclude-module=torch',           # 排除PyTorch
        '--exclude-module=tensorflow',      # 排除TensorFlow
        '--exclude-module=numpy',           # 排除NumPy（如果不需要）
        '--exclude-module=pandas',          # 排除Pandas
        '--exclude-module=scipy',           # 排除SciPy
        '--exclude-module=matplotlib',      # 排除Matplotlib
        '--exclude-module=PIL',             # 排除Pillow
        '--exclude-module=cv2',             # 排除OpenCV
        '--exclude-module=sklearn',         # 排除scikit-learn
        '--exclude-module=jupyter',         # 排除Jupyter
        '--exclude-module=IPython',         # 排除IPython
        '--exclude-module=notebook',        # 排除notebook
        '--exclude-module=tkinter',         # 排除tkinter
        '--exclude-module=PyQt5',           # 排除PyQt5
        '--exclude-module=PyQt6',           # 排除PyQt6
        '--exclude-module=wx',              # 排除wxPython
        '--exclude-module=kivy',            # 排除Kivy
        '--exclude-module=pygame',          # 排除Pygame
        '--exclude-module=plotly',          # 排除Plotly
        '--exclude-module=seaborn',         # 排除Seaborn
        '--exclude-module=bokeh',           # 排除Bokeh
        '--exclude-module=dash',            # 排除Dash
        '--exclude-module=streamlit',       # 排除Streamlit
        '--exclude-module=fastapi',         # 排除FastAPI
        '--exclude-module=flask',           # 排除Flask
        '--exclude-module=django',          # 排除Django
        '--exclude-module=sqlalchemy',      # 排除SQLAlchemy
        '--exclude-module=psycopg2',        # 排除PostgreSQL驱动
        '--exclude-module=pymongo',         # 排除MongoDB驱动
        '--exclude-module=redis',           # 排除Redis
        '--exclude-module=celery',          # 排除Celery
        '--exclude-module=pytest',          # 排除测试框架
        '--exclude-module=unittest',        # 排除unittest
        '--exclude-module=doctest',         # 排除doctest
        '--noconfirm',                      # 不询问覆盖
        '--clean',                          # 清理临时文件
        '--distpath=dist',                  # 输出目录
        '--workpath=build',                 # 工作目录
        '--specpath=.',                     # spec文件位置
        '--optimize=2',                     # 优化字节码
        '--strip',                          # 去除调试信息（Linux/Mac）
    ]
    
    print("🚀 开始打包精简版生物学AI论文分析器...")
    print(f"📁 工作目录: {script_dir}")
    print("📦 精简打包参数（排除大型库）:")
    for arg in args:
        print(f"   {arg}")
    
    try:
        # 运行PyInstaller
        PyInstaller.__main__.run(args)
        print("\n✅ 精简版打包完成！")
        print("📁 可执行文件位置: dist/BioAI-Paper-Analyzer-Minimal.exe")
        
        # 检查文件大小
        exe_path = os.path.join("dist", "BioAI-Paper-Analyzer-Minimal.exe")
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path)
            size_mb = file_size / (1024 * 1024)
            print(f"📊 文件大小: {size_mb:.1f} MB")
        
    except Exception as e:
        print(f"\n❌ 打包失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = build_minimal_exe()
    if success:
        print("\n🎉 精简版生物学AI论文分析器已成功打包！")
        print("💡 使用方法：双击 dist/BioAI-Paper-Analyzer-Minimal.exe 运行程序")
        print("📝 注意：此版本已排除大型机器学习库以减小文件大小")
    else:
        print("\n😞 打包失败，请检查错误信息并重试")
        sys.exit(1)
