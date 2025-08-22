import PyInstaller.__main__
import os
import sys

def build_exe():
    """使用PyInstaller打包生物学AI论文分析器为exe文件"""
    
    # 确保在正确的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # PyInstaller参数
    args = [
        'bio_ai_gui.py',                    # 主程序文件
        '--name=BioAI-Paper-Analyzer',      # 可执行文件名
        '--onefile',                        # 打包成单个exe文件
        '--windowed',                       # 不显示控制台窗口
        '--icon=icon.ico',                  # 图标文件（如果有的话）
        '--add-data=requirements.txt;.',    # 包含依赖文件
        '--hidden-import=bio_ai_paper_analyzer',  # 隐式导入
        '--hidden-import=habanero',         # Crossref库
        '--hidden-import=openai',           # OpenAI库
        '--hidden-import=PySide6',          # GUI库
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtWidgets',
        '--collect-all=PySide6',            # 收集所有PySide6文件
        '--noconfirm',                      # 不询问覆盖
        '--clean',                          # 清理临时文件
        '--distpath=dist',                  # 输出目录
        '--workpath=build',                 # 工作目录
        '--specpath=.',                     # spec文件位置
    ]
    
    print("🚀 开始打包生物学AI论文分析器...")
    print(f"📁 工作目录: {script_dir}")
    print("📦 打包参数:")
    for arg in args:
        print(f"   {arg}")
    
    try:
        # 运行PyInstaller
        PyInstaller.__main__.run(args)
        print("\n✅ 打包完成！")
        print("📁 可执行文件位置: dist/BioAI-Paper-Analyzer.exe")
        
    except Exception as e:
        print(f"\n❌ 打包失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = build_exe()
    if success:
        print("\n🎉 生物学AI论文分析器已成功打包为exe文件！")
        print("💡 使用方法：双击 dist/BioAI-Paper-Analyzer.exe 运行程序")
    else:
        print("\n😞 打包失败，请检查错误信息并重试")
        sys.exit(1)
