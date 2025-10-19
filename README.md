# BioAI Tools · 项目总览

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Platforms](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-ff69b4.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![License](https://img.shields.io/badge/License-Unspecified-lightgrey.svg)

本仓库是一个面向生信与文献工作流的多模块工具集，包含：
- Franklin：生物学论文智能分析桌面端（Tkinter）
- arxiv_llm_digest：Crossref 检索 + LLM 批量分析（CLI + PySide6 GUI）
- IDconvert：GTF 注释解析并为矩阵追加 gene_name 列（Tkinter 工具）
- DNAtranslate：浏览器端 DNA→蛋白翻译与相关计算小工具（JavaScript）

提示：仓库采用独立子目录模块化组织，每个子模块均可单独安装与运行。

## 目录

- [简介](#简介)
- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [目录结构](#目录结构)
- [快速开始](#快速开始)
  - [前置条件](#前置条件)
  - [安装](#安装)
  - [配置](#配置)
  - [本地运行](#本地运行)
- [各模块说明](#各模块说明)
  - [Franklin](#franklin)
  - [arxiv_llm_digest](#arxiv_llm_digest)
  - [IDconvert](#idconvert)
  - [DNAtranslate](#dnatranslate)
- [使用示例](#使用示例)
- [测试与代码质量检查](#测试与代码质量检查)
- [构建与发布](#构建与发布)
- [常见问题 FAQ](#常见问题-faq)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 简介

本仓库聚焦“生信 + AI 助力文献工作流”的常见需求：从关键词提取、Crossref 搜索，到 LLM 评分、摘要翻译与总结报告生成，并提供桌面端与命令行两种形态，支持 Windows/macOS/Linux。

## 功能特性

- 文献检索：基于 Crossref API 的论文搜索（含摘要过滤、时段筛选）
- 智能分析：调用 SiliconFlow 托管的 LLM（openai 兼容客户端）进行多维评价
- 摘要翻译：英文摘要→学术中文
- 报告生成：每日 Markdown 报告归档与桌面保存
- 桌面应用：Tkinter 与 PySide6 现代化界面
- 多模块独立：各模块可独立安装、运行与打包

## 技术栈

- Python：tkinter、requests、openai（兼容 SiliconFlow base_url）、habanero（Crossref 客户端）、PySide6
- 前端：原生 JavaScript（浏览器端工具）
- 打包：PyInstaller（Windows/Linux/macOS）

## 目录结构

```
.
├── Franklin/                     # 生物学论文智能分析（Tkinter 桌面端）
│   ├── gui_module.py             # GUI 入口
│   ├── search_module.py          # Crossref 检索
│   ├── keyword_extractor.py      # 关键词提取（LLM）
│   ├── analysis_module.py        # 论文分析（LLM）
│   ├── translation_module.py     # 摘要翻译（LLM）
│   ├── summary_module.py         # 汇总与报告摘要（LLM）
│   └── requirements.txt
├── arxiv_llm_digest/             # Crossref 批量检索 + LLM 分析（CLI + PySide6 GUI）
│   ├── bio_ai_paper_analyzer.py  # CLI 入口
│   ├── bio_ai_gui.py             # GUI 入口（PySide6）
│   ├── requirements.txt
│   └── result/                   # 每日 digest_YYYY-MM-DD.md
├── IDconvert/                    # GTF→gene_name 附加工具（Tkinter）
│   └── main.py                   # GUI 入口
├── DNAtranslate/                 # 浏览器端 DNA→蛋白质翻译与小工具
│   └── translate.js
├── .env.example                  # 环境变量示例（不自动加载，仅示例）
├── .gitignore
└── README.md
```

## 快速开始

### 前置条件

- Python 3.9+
- pip 和虚拟环境工具（推荐 venv）
- 网络可访问 Crossref 与 SiliconFlow API
- GUI 运行：
  - Tkinter 在大多数 Python 发行版自带；Linux 可能需要安装 python3-tk
  - PySide6 通过 pip 安装

### 安装

建议在仓库根目录创建虚拟环境，并安装所需子模块依赖：

```bash
# 克隆仓库
git clone <your-repo-url>
cd <repo-root>

# 创建并激活虚拟环境
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 安装依赖（可按需选择安装）
pip install -r Franklin/requirements.txt
pip install -r arxiv_llm_digest/requirements.txt
```

### 配置

- SiliconFlow API Key：用于 Franklin 与 arxiv_llm_digest 调用 LLM
- 环境变量名：SILICONFLOW_API_KEY

可选方式：

```bash
# 方式1：直接导出环境变量（推荐）
export SILICONFLOW_API_KEY=sk-xxxxxxxxxxxxxxxx

# 方式2：使用 .env 文件（仅示例，代码不会自动加载 .env）
# 将 .env.example 复制为 .env，随后在当前 shell 手动加载
set -a && source .env && set +a  # macOS/Linux
# Windows PowerShell
$env:SILICONFLOW_API_KEY = "sk-xxxxxxxxxxxxxxxx"
```

注意：arxiv_llm_digest 的 CLI 也支持通过参数显式传入密钥：

```bash
python arxiv_llm_digest/bio_ai_paper_analyzer.py \
  --siliconflow-api-key "$SILICONFLOW_API_KEY" \
  --query "computational biology" --days 2 --max-results 10
```

### 本地运行

- Franklin（桌面端）：

```bash
python Franklin/gui_module.py
```

- arxiv_llm_digest（CLI）：

```bash
python arxiv_llm_digest/bio_ai_paper_analyzer.py \
  --query "computational biology deep learning" \
  --days 2 --max-results 20 \
  --model Qwen/Qwen2.5-7B-Instruct \
  --lang zh
```

- arxiv_llm_digest（GUI）：

```bash
python arxiv_llm_digest/bio_ai_gui.py
```

- IDconvert（Tkinter 工具）：

```bash
python IDconvert/main.py
```

- DNAtranslate（浏览器端）：将 DNAtranslate/translate.js 引入到你的 HTML 页面中，或移植到任意前端工程。

## 各模块说明

### Franklin

- 功能：关键词提取 → Crossref 搜索 → 论文分析 → 中文摘要翻译 → 汇总与 Markdown 报告保存
- 依赖安装：`pip install -r Franklin/requirements.txt`
- 运行：`python Franklin/gui_module.py`
- 配置：通过环境变量 `SILICONFLOW_API_KEY`，GUI 中可输入并保存到当前进程环境变量
- 输出：`Franklin/result/论文分析结果_YYYYMMDD_HHMMSS.md`
- 截图占位符：![Franklin GUI 截图 占位](docs/images/franklin_gui.png)

### arxiv_llm_digest

- 作用：按关键词与时间范围抓取 Crossref 文献，用 LLM 分析评分与生成每日摘要
- 依赖安装：`pip install -r arxiv_llm_digest/requirements.txt`
- CLI：`python arxiv_llm_digest/bio_ai_paper_analyzer.py --query "..." --days 2 --max-results 20`
- GUI：`python arxiv_llm_digest/bio_ai_gui.py`
- 输出：`arxiv_llm_digest/result/digest_YYYY-MM-DD.md`
- 截图占位符：![arxiv GUI 截图 占位](docs/images/arxiv_gui.png)

提示：当前 CLI 模板中含历史合并标记（<<<<<<<、=======、>>>>>>），不影响 README 使用说明；如遇运行异常，请先清理冲突片段。

### IDconvert

- 作用：读取 GTF 注释，解析 gene_id→gene_name 映射，为 TSV 矩阵追加 gene_name 列
- 运行：`python IDconvert/main.py`
- 适配：适用于带 gene_id 列的 TSV 文件；处理过程带进度条与完成提示

### DNAtranslate

- 作用：DNA→蛋白翻译、密码子优化（多物种）、多肽评分、稀释/标签计算等
- 使用：前端引入 `translate.js`，调用公开函数并接管 DOM 渲染

## 使用示例

- Franklin 最小化示例：

```bash
export SILICONFLOW_API_KEY=sk-xxxxxxxx
python Franklin/gui_module.py  # 在 GUI 中输入检索内容并开始分析
```

- arxiv_llm_digest CLI 最小化示例：

```bash
export SILICONFLOW_API_KEY=sk-xxxxxxxx
python arxiv_llm_digest/bio_ai_paper_analyzer.py \
  --query "genomics deep learning" --days 7 --max-results 10 --lang zh
```

- IDconvert：

```bash
python IDconvert/main.py  # 选择 GTF 与 TSV，点击“开始转换”
```

## 测试与代码质量检查

本仓库暂未提供单元测试。推荐使用以下工具进行本地代码质量检查：

```bash
pip install ruff black
ruff check .
black --check .
```

Markdown 校验建议：markdownlint、Prettier（本 README 已按常见规则格式化）。

## 构建与发布

- Franklin（PyInstaller 打包）：

```bash
# 方式1（脚本）
python Franklin/build_with_pyinstaller.py
# 或方式2（直接命令）
pyinstaller --noconsole --onefile Franklin/gui_module.py
```

- arxiv_llm_digest（PyInstaller 打包）：

```bash
python arxiv_llm_digest/build_exe.py          # 完整版
python arxiv_llm_digest/build_exe_minimal.py  # 精简版
```

- IDconvert（PyInstaller 示例）：

```bash
pyinstaller --onefile --noconsole IDconvert/main.py
```

构建产物默认位于各模块的 `dist/` 目录下。

## 常见问题 FAQ

- LLM 报错 “SILICONFLOW_API_KEY 未设置” 或 401：请正确设置环境变量或通过参数显式传入
- Crossref 请求受限或失败：
  - Franklin/search_module.py 的 User-Agent 中包含 `mailto:your-email@example.com`，建议替换为你自己的邮箱
  - 适当降低速率、扩大时间范围，或重试
- Linux 运行 Tkinter：可能需要安装 `sudo apt-get install python3-tk`
- GUI 显示异常或中文字体：请确认系统可用中文字体
- 证书或网络错误：检查代理/证书链或更换网络环境

## 贡献指南

欢迎参与贡献（Bug 反馈 / 新功能 / 文档改进）：

- Fork 本仓库并创建特性分支：`git checkout -b feat/your-feature`
- 遵循简洁、模块化的代码风格；Python 推荐 Black + Ruff
- 提交 PR 前请确保：能正常运行最小路径、命令示例有效、README 已更新
- Commit 信息建议遵循 Conventional Commits 简要规范

## 许可证

本仓库当前未明确声明开源许可证（License Unspecified）。若需在特定场景使用或商用授权，请先在 Issue 中沟通或联系仓库维护者。
