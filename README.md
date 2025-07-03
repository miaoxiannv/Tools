# IDconvert 工具

## 简介

**IDconvert** 是一个基于 Python 的图形界面小工具，用于将 GTF 注释文件中的 `gene_id` 映射为 `gene_name`，并自动为原始 TSV 文件添加 `gene_name` 列，生成新的结果文件。适用于基因ID批量转换等生信分析场景。

## 功能特色

- 支持 GTF 注释文件与 TSV 原始文件的 ID 转换
- 自动生成带 `gene_name` 列的新 TSV 文件
- 简洁美观的图形界面，操作简单
- 转换过程带进度条与友好提示
- 支持 Windows 下一键打包为 exe 可执行文件

## 使用方法

1. **安装依赖**

   ```bash
   pip install tk
   ```

2. **运行工具**

   ```bash
   python IDconvert/main.py
   ```

3. **操作流程**

   - 打开工具后，点击"选择"按钮，依次选择 GTF 注释文件和 TSV 原始文件。
   - 工具会自动生成输出文件名（在原始文件名后加 `_gene_name`）。
   - 点击"开始转换"，等待进度条完成，弹窗提示"转换完成！"并显示新文件名。

4. **输出说明**

   - 新文件会与原始 TSV 文件在同一目录下，文件名为 `原始文件名_gene_name.tsv`。

## 打包为可执行文件（可选）

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
