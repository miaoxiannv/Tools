
# Tools 项目总览

本仓库包含多个生信与 AI 工具，核心模块如下：

## Franklin

> 生物学论文智能分析系统 - 基于深度学习模型，帮助研究者快速筛选、分析和理解生物学相关论文。

**核心功能：**
- 🔍 智能关键词提取：从研究主题自动提取精准关键词
- 📚 论文自动检索：基于 Crossref API 搜索相关论文
- 🤖 AI 深度分析：评估论文的新颖性、生物影响力和技术创新性
- 🌐 中文摘要翻译：自动翻译论文摘要
- 📊 结构化报告：生成清晰的分析报告

**使用方法：**
```bash
cd Franklin
python gui_module.py
```

或直接运行打包好的可执行文件：
```bash
cd Franklin/dist
Franklin.exe
```

=======
>>>>>>> 19ea3f909ea1d2d3b39b1e37e1cb8217b555cb0c
---

## arXiv_llm_digest

> 自动抓取 arXiv 上最新 LLM 相关论文，利用大模型（如 OpenAI GPT）分析摘要与新颖度，生成每日结构化报告。

**主要特性：**
- 一键检索 LLM 相关论文（可按日期/数量筛选）
- LLM 自动分析摘要与新颖性，输出精炼结论
- 结果以 Markdown 格式每日归档，便于查阅
- 提供美观易用的 PySide6 图形界面

**依赖安装：**
```bash
pip install -r arxiv_llm_digest/requirements.txt
```

**命令行用法：**
```bash
python arxiv_llm_digest/arxiv_digest.py
```
**图形界面启动：**
```bash
python arxiv_llm_digest/gui.py
```

**结果输出：**
每日分析结果保存在 `arxiv_llm_digest/result/`，文件名如 `digest_YYYY-MM-DD.md`。

---

## IDconvert

> GTF 注释文件与 TSV 文件的基因 ID 批量转换工具，自动添加 gene_name 列，适合生信分析。

**快速使用：**
```bash
pip install tk
python IDconvert/main.py
```

---

## DNAtranslate

> DNA 序列翻译与相关小工具（详见 DNAtranslate/ 目录）。

如需在无 Python 环境下运行，可用 PyInstaller 打包：

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile IDconvert/main.py
```

打包后在 `dist` 目录下生成 `main.exe`，可直接运行。

## 依赖环境

- Python 3.6+
- tkinter（标准库自带）
- Windows（推荐打包为 exe）

## 目录结构

```
Tools/
├── IDconvert/
│   ├── main.py
│   ├── logo.ico         # 可选，窗口logo
│   └── ...
├── README.md
└── ...
```

## 常见问题

- 若界面显示异常或中文乱码，请确保系统支持中文字体。
- 若打包后 exe 无法运行，请检查依赖是否齐全，或尝试以管理员身份运行。

---

如有问题或建议，欢迎反馈！
