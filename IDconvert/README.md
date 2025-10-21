# IDconvert - GTF 注释补充 gene_name 工具

一个极简的桌面工具（Tkinter），用于：
- 解析 GTF 注释，构建 gene_id → gene_name 的映射
- 为带有 gene_id 列的 TSV 矩阵追加 gene_name 列
- 进度条与完成提示，适合日常数据处理

## 安装与运行

环境要求：
- Python 3.8+
- Tkinter（大多数发行版自带；Linux 可能需要 `sudo apt-get install python3-tk`）

运行：
```bash
python IDconvert/main.py
```

## 使用说明
1. 选择 GTF 注释文件（包含 gene_id 与 gene_name 条目）
2. 选择原始 TSV 文件（包含 gene_id 列）
3. 点击“开始转换”，程序会在同目录生成添加了 gene_name 的新文件（文件名后缀 `_gene_name`）

## 打包
可使用 PyInstaller 打包为独立可执行文件：
```bash
pyinstaller --onefile --noconsole IDconvert/main.py
```

## 许可证
未明确声明（默认保留）。
