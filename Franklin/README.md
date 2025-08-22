# Franklin - 生物学论文智能分析系统

Franklin 是一个基于AI的生物学论文智能分析系统，能够自动搜索、分析和翻译生物学相关论文。

## 主要功能

- 🔍 智能关键词提取：根据用户输入自动提取搜索关键词
- 📚 论文智能搜索：基于Crossref API搜索相关论文
- 🤖 AI论文分析：分析论文的创新性、生物学影响和技术创新
- 🌐 自动翻译：将英文摘要翻译成中文
- 📊 可视化界面：简洁直观的用户界面
- 💾 结果导出：支持导出分析结果为Markdown格式

## 技术特点

- 简洁的设计风格，遵循"Less is More"原则
- 基于现代AI模型的智能分析
- 多线程处理确保界面响应
- 模块化架构，易于扩展
- 支持多种AI模型选择

## 安装使用

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/Franklin.git
cd Franklin
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行程序：
```bash
python gui_module.py
```

## 打包说明

项目支持使用PyInstaller打包为独立可执行文件：

```bash
python build_with_pyinstaller.py
```

生成的可执行文件将位于`dist`目录下。

## 系统要求

- Python 3.9+
- 硅基流动 API Key（用于AI分析）
- Windows/Linux/MacOS

## 项目结构

```
Franklin/
├── gui_module.py      # 主界面模块
├── search_module.py   # 论文搜索模块
├── analysis_module.py # 论文分析模块
├── translation_module.py # 翻译模块
├── keyword_extractor.py # 关键词提取
└── summary_module.py  # 总结生成模块
```

## 贡献

欢迎提交Pull Request或Issue！

## 许可证

MIT License
