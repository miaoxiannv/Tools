# gui_module.py
"""
可视化GUI模块 - Linus式设计 v2.0

核心原则：简洁、直接、无废话
"好品味意味着让特殊情况消失"
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import os
from datetime import datetime
from typing import List, Optional

from search_module import search_papers, Paper, SearchError
from analysis_module import analyze_paper
from translation_module import translate_abstract
from keyword_extractor import extract_keywords
from summary_module import generate_summary, SummaryError


class PaperAnalysisGUI:
    """论文分析GUI - 单一职责，美观设计"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Franklin - 生物学论文智能分析系统")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # 状态变量
        self.is_processing = False
        self.results: List[Paper] = []
        self.api_key = tk.StringVar()
        self.selected_model = tk.StringVar(value="deepseek-ai/DeepSeek-R1")
        self.query_text = ""
        self.keywords_used = []
        self.summary_text = ""
        
        # 可用模型列表
        self.available_models = [
            "deepseek-ai/DeepSeek-R1",
            "Qwen/Qwen3-235B-A22B-Thinking-2507", 
            "Qwen/Qwen3-Coder-480B-A35B-Instruct",
            "moonshotai/Kimi-K2-Instruct"
        ]
        
        self._setup_styles()
        self._setup_ui()
        self._load_api_key()
    
    def _setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 统一配置
        style.configure('Title.TLabel', 
                       font=('Microsoft YaHei', 16, 'bold'),
                       foreground='#2c3e50',
                       background='#f0f0f0')
        
        style.configure('Heading.TLabel',
                       font=('Microsoft YaHei', 10, 'bold'),
                       foreground='#34495e',
                       background='#f0f0f0')
        
        # 按钮样式
        for btn_type in ['Custom', 'Success']:
            style.configure(f'{btn_type}.TButton',
                          font=('Microsoft YaHei', 9),
                          foreground='white')
        
        style.map('Custom.TButton',
                 background=[('active', '#3498db'), ('!active', '#2980b9')])
        style.map('Success.TButton',
                 background=[('active', '#27ae60'), ('!active', '#2ecc71')])
    
    def _setup_ui(self):
        """设置UI - 美观布局"""
        # 主容器
        main_container = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=15)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_container, 
                               text="🧬 Franklin - 生物学论文智能分析系统", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # 配置区域
        self._create_config_section(main_container)
        
        # 查询区域
        self._create_query_section(main_container)
        
        # 进度区域
        self._create_progress_section(main_container)
        
        # 结果区域
        self._create_result_section(main_container)
    
    def _create_config_section(self, parent):
        """创建配置区域"""
        config_frame = ttk.LabelFrame(parent, text="⚙️ 系统配置", padding=15, style='Custom.TFrame')
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        # API配置
        api_frame = tk.Frame(config_frame, bg='#ecf0f1')
        api_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(api_frame, text="硅基流动 API Key:", style='Heading.TLabel').pack(side=tk.LEFT)
        
        api_entry = ttk.Entry(api_frame, textvariable=self.api_key, width=40, show='*')
        api_entry.pack(side=tk.LEFT, padx=(10, 5))
        
        save_api_btn = ttk.Button(api_frame, text="保存", 
                                 command=self._save_api_key, style='Custom.TButton')
        save_api_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # 模型选择
        model_frame = tk.Frame(config_frame, bg='#ecf0f1')
        model_frame.pack(fill=tk.X)
        
        ttk.Label(model_frame, text="选择模型:", style='Heading.TLabel').pack(side=tk.LEFT)
        
        model_combo = ttk.Combobox(model_frame, textvariable=self.selected_model,
                                  values=self.available_models, state='readonly', width=35)
        model_combo.pack(side=tk.LEFT, padx=(10, 0))
    
    def _create_query_section(self, parent):
        """创建查询区域"""
        query_frame = ttk.LabelFrame(parent, text="🔍 生物学论文查询", padding=15, style='Custom.TFrame')
        query_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 查询输入
        input_frame = tk.Frame(query_frame, bg='#ecf0f1')
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="生物学查询内容:", style='Heading.TLabel').pack(anchor=tk.W)
        self.query_entry = ttk.Entry(input_frame, width=70, font=('Microsoft YaHei', 10))
        self.query_entry.pack(fill=tk.X, pady=(5, 0))
        
        # 控制面板
        control_frame = tk.Frame(query_frame, bg='#ecf0f1')
        control_frame.pack(fill=tk.X)
        
        ttk.Label(control_frame, text="文章数量:", style='Heading.TLabel').pack(side=tk.LEFT)
        
        self.count_var = tk.StringVar(value="3")
        count_spinbox = ttk.Spinbox(control_frame, from_=1, to=10, 
                                   textvariable=self.count_var, width=8)
        count_spinbox.pack(side=tk.LEFT, padx=(10, 20))
        
        # 按钮组
        self.start_button = ttk.Button(control_frame, text="🚀 开始分析", 
                                      command=self._start_analysis, style='Custom.TButton')
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_button = ttk.Button(control_frame, text="💾 保存结果", 
                                     command=self._save_results, style='Success.TButton',
                                     state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT)
    
    def _create_progress_section(self, parent):
        """创建进度区域"""
        progress_frame = ttk.LabelFrame(parent, text="📊 处理进度", padding=15, style='Custom.TFrame')
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_var = tk.StringVar(value="🟢 系统就绪")
        progress_label = ttk.Label(progress_frame, textvariable=self.progress_var,
                                  font=('Microsoft YaHei', 9))
        progress_label.pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate',
                                           style='TProgressbar')
        self.progress_bar.pack(fill=tk.X, pady=(8, 0))
    
    def _create_result_section(self, parent):
        """创建结果区域"""
        result_frame = ttk.LabelFrame(parent, text="📋 分析结果", padding=15, style='Custom.TFrame')
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建带滚动条的文本框
        text_frame = tk.Frame(result_frame, bg='#ecf0f1')
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = scrolledtext.ScrolledText(
            text_frame, 
            height=15, 
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#ffffff',
            fg='#2c3e50',
            selectbackground='#3498db',
            selectforeground='white'
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
    
    def _load_api_key(self):
        """加载API密钥"""
        api_key = os.environ.get("SILICONFLOW_API_KEY", "")
        self.api_key.set(api_key)
    
    def _save_api_key(self):
        """保存API密钥"""
        key = self.api_key.get().strip()
        if key:
            os.environ["SILICONFLOW_API_KEY"] = key
            messagebox.showinfo("成功", "API Key 已保存到环境变量")
        else:
            messagebox.showerror("错误", "请输入有效的API Key")
    
    def _start_analysis(self):
        """开始分析 - 主要工作流程"""
        # 验证配置
        if not self.api_key.get().strip():
            messagebox.showerror("配置错误", "请先配置硅基流动 API Key")
            return
        
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showerror("输入错误", "请输入查询内容")
            return
        
        if self.is_processing:
            messagebox.showinfo("提示", "正在处理中，请稍候...")
            return
        
        try:
            count = int(self.count_var.get())
        except ValueError:
            messagebox.showerror("输入错误", "文章数量必须是数字")
            return
        
        # 确保API Key在环境变量中
        os.environ["SILICONFLOW_API_KEY"] = self.api_key.get().strip()
        
        # 在后台线程中执行分析
        self.is_processing = True
        self.start_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        
        thread = threading.Thread(target=self._analysis_worker, args=(query, count))
        thread.daemon = True
        thread.start()
    
    def _analysis_worker(self, query: str, count: int):
        """分析工作线程 - Linus式简洁流程"""
        try:
            model = self.selected_model.get()
            
            # 步骤1: 提取关键词
            self._update_progress("🔍 正在提取关键词...")
            keywords = extract_keywords(query, model=model)
            
            if not keywords:
                self._show_error("关键词提取失败")
                return
            
            keywords_str = ", ".join(keywords)
            self._update_progress(f"✅ 关键词提取完成: {keywords_str}")
            
            # 步骤2: 搜索论文
            self._update_progress(f"🔍 正在搜索论文 (目标数量: {count})...")
            papers = search_papers(query=keywords_str, limit=count)
            
            if not papers:
                self._show_error("未找到相关论文")
                return
            
            self._update_progress(f"✅ 找到 {len(papers)} 篇论文，开始分析...")
            
            # 步骤3: 分析和翻译每篇论文
            self.results = []
            for i, paper in enumerate(papers, 1):
                self._update_progress(f"📊 正在分析第 {i}/{len(papers)} 篇论文...")
                
                # 分析
                analyzed_paper = analyze_paper(paper, model_name=model)
                
                if analyzed_paper.status == 'ANALYZED':
                    # 翻译
                    self._update_progress(f"🌐 正在翻译第 {i}/{len(papers)} 篇论文...")
                    translated_paper = translate_abstract(analyzed_paper, model_name=model)
                    self.results.append(translated_paper)
                else:
                    self.results.append(analyzed_paper)
            
            # 步骤4: 生成总结
            self._update_progress("📝 正在生成总结...")
            try:
                self.summary_text = generate_summary(query, keywords, self.results, model)
                self.query_text = query
                self.keywords_used = keywords
            except SummaryError as e:
                self.summary_text = f"总结生成失败: {e}"
            
            # 步骤5: 显示结果
            self._update_progress("✅ 分析完成，正在生成报告...")
            self._display_results()
            
        except Exception as e:
            self._show_error(f"处理失败: {e}")
        finally:
            self._finish_processing()
    
    def _update_progress(self, message: str):
        """更新进度显示"""
        self.root.after(0, lambda: self.progress_var.set(message))
    
    def _show_error(self, message: str):
        """显示错误"""
        self.root.after(0, lambda: messagebox.showerror("错误", message))
    
    def _finish_processing(self):
        """完成处理"""
        self.root.after(0, self._reset_ui)
    
    def _reset_ui(self):
        """重置UI状态"""
        self.is_processing = False
        self.start_button.config(state=tk.NORMAL)
        self.progress_bar.stop()
        self.progress_var.set("🟢 处理完成")
        if self.results:
            self.save_button.config(state=tk.NORMAL)
    
    def _display_results(self):
        """显示分析结果"""
        def update_display():
            self.result_text.delete(1.0, tk.END)
            
            # 统计信息
            total = len(self.results)
            analyzed = sum(1 for p in self.results if p.status == 'ANALYZED')
            translated = sum(1 for p in self.results if p.translated_abstract)
            
            summary = "\n".join([
                "="*60,
                "📊 分析完成统计",
                "="*60,
                f"📚 总计论文: {total} 篇",
                f"✅ 成功分析: {analyzed} 篇",
                f"🌐 翻译完成: {translated} 篇",
                f"🤖 使用模型: {self.selected_model.get()}",
                "="*60 + "\n"
            ])
            
            self.result_text.insert(tk.END, summary)
            
            # 详细结果
            for i, paper in enumerate(self.results, 1):
                parts = [
                    f"📄 论文 {i}",
                    "─"*50,
                    f"📝 标题: {paper.title}",
                    f"🔗 DOI: {paper.doi}"
                ]
                
                if paper.authors:
                    parts.append(f"👥 作者: {', '.join(paper.authors[:3])}{'...' if len(paper.authors) > 3 else ''}")
                
                if paper.publication_year:
                    parts.append(f"📅 年份: {paper.publication_year}")
                
                if paper.status == 'ANALYZED' and paper.analysis_result:
                    result = paper.analysis_result
                    parts.extend([
                        "\n📊 分析结果:",
                        f"  💡 核心贡献: {result.contribution}",
                        f"  🌟 新颖性: {'★' * result.novelty}{'☆' * (5 - result.novelty)} ({result.novelty}/5)",
                        f"  🧬 生物影响: {'★' * result.biological_impact}{'☆' * (5 - result.biological_impact)} ({result.biological_impact}/5)",
                        f"  🔧 技术创新: {'★' * result.technical_innovation}{'☆' * (5 - result.technical_innovation)} ({result.technical_innovation}/5)"
                    ])
                else:
                    parts.extend([
                        f"\n❌ 分析状态: {paper.status}",
                        f"  错误信息: {paper.error_message}" if paper.error_message else ""
                    ])
                
                if paper.translated_abstract:
                    parts.extend(["", "🌐 中文摘要:", paper.translated_abstract])
                
                parts.extend(["", "="*60, ""])
                self.result_text.insert(tk.END, "\n".join(parts))
        
        self.root.after(0, update_display)
    
    def _save_results(self):
        """保存结果为Markdown文件到result目录"""
        if not self.results:
            messagebox.showwarning("警告", "没有结果可保存")
            return
        
        # 确保result目录存在
        result_dir = "result"
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(result_dir, f"论文分析结果_{timestamp}.md")
        
        try:
            self._generate_markdown_report(filename)
            messagebox.showinfo("保存成功", f"结果已保存到:\n{os.path.abspath(filename)}")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存失败: {e}")
    
    def _generate_markdown_report(self, filename: str):
        """生成Markdown报告"""
        with open(filename, 'w', encoding='utf-8') as f:
            lines = [
                f"# 生物学研究论文分析摘要 - {datetime.now().strftime('%Y-%m-%d')}\n",
                "您的生物学研究论文分析摘要，由 **Franklin** 智能分析。\n"
            ]
            
            if self.summary_text:
                lines.extend([
                    "## 📋 分析总结\n",
                    f"**查询内容**: {self.query_text}\n",
                    f"**关键词**: {', '.join(self.keywords_used)}\n",
                    f"**使用模型**: {self.selected_model.get()}\n",
                    f"{self.summary_text}\n",
                    "---\n"
                ])
            
            for i, paper in enumerate(self.results, 1):
                url = paper.url or f'https://doi.org/{paper.doi}'
                if paper.status == 'ANALYZED' and paper.analysis_result:
                    result = paper.analysis_result
                    paper_info = [
                        f"## {i}. [{paper.title}]({url})",
                        f"- **链接**: [{paper.doi}]({url})"
                    ]
                    
                    if paper.authors:
                        paper_info.append(f"- **作者**: {', '.join(paper.authors)}")
                    
                    if paper.publication_year:
                        paper_info.append(f"- **年份**: {paper.publication_year}")
                    
                    paper_info.extend([
                        f"- **DOI**: {paper.doi}",
                        f"- **新颖性评分**: {result.novelty}/5",
                        f"- **生物影响评分**: {result.biological_impact}/5",
                        f"- **技术创新评分**: {result.technical_innovation}/5",
                        f"- **核心贡献**: {result.contribution}"
                    ])
                    
                    if paper.translated_abstract:
                        paper_info.append(f"- **摘要**: {paper.translated_abstract}\n")
                    else:
                        paper_info.append("\n")
                else:
                    paper_info = [
                        f"## {i}. {paper.title}",
                        f"- **链接**: [{paper.doi}]({url})",
                        "- **状态**: 分析失败"
                    ]
                    if paper.error_message:
                        paper_info.append(f"- **错误**: {paper.error_message}")
                    paper_info.append("\n")
                
                lines.extend(paper_info)
            
            total = len(self.results)
            analyzed = sum(1 for p in self.results if p.status == 'ANALYZED')
            translated = sum(1 for p in self.results if p.translated_abstract)
            
            stats = [
                "---\n",
                "## 📊 分析统计\n",
                f"- 总计论文: {total} 篇",
                f"- 成功分析: {analyzed} 篇",
                f"- 翻译完成: {translated} 篇",
                f"- 成功率: {analyzed/total*100:.1f}%\n",
                f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
            ]
            
            lines.extend(stats)
            f.write('\n'.join(lines))
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()


def main():
    """主函数 - Linus式简洁启动"""
    print("--- Franklin GUI v2.0 启动 ---")
    print("新特性: API配置 + 模型选择 + 美观界面")
    print("设计原则: 简洁、直接、无废话")
    
    app = PaperAnalysisGUI()
    app.run()


if __name__ == "__main__":
    main()
