import csv
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os

# 解析GTF文件，返回gene_id到gene_name的映射
def parse_gtf(gtf_path):
    gene_map = {}
    with open(gtf_path, encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            fields = line.strip().split('\t')
            if len(fields) < 9:
                continue
            attr_field = fields[8]
            gene_id_match = re.search(r'gene_id "([^"]+)"', attr_field)
            gene_name_match = re.search(r'gene_name "([^"]+)"', attr_field)
            if gene_id_match and gene_name_match:
                gene_id = gene_id_match.group(1)
                gene_name = gene_name_match.group(1)
                gene_map[gene_id] = gene_name
    return gene_map

# 读取TSV，添加gene_name列，带进度回调
def add_gene_name(tsv_path, out_path, gene_map, progress_callback=None):
    with open(tsv_path, encoding='utf-8') as infile:
        lines = infile.readlines()
    total = len(lines) - 1  # 除去表头
    with open(out_path, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(lines, delimiter='\t')
        fieldnames = reader.fieldnames + ['gene_name']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for i, row in enumerate(reader):
            gid = row.get('gene_id', '')
            row['gene_name'] = gene_map.get(gid, '')
            writer.writerow(row)
            if progress_callback and total > 0:
                progress_callback((i+1)/total*100)

def get_outfile_path(tsv_path):
    base, ext = os.path.splitext(tsv_path)
    return f"{base}_gene_name{ext}"

class App:
    def __init__(self, root):
        self.root = root
        root.title('GTF/TSV ID转换工具')
        try:
            root.iconbitmap('logo.ico')
        except Exception:
            pass
        root.geometry('400x300')
        root.minsize(400, 300)
        root.maxsize(400, 300)
        root.resizable(False, False)

        # 网格列比例设置
        root.grid_columnconfigure(0, minsize=90)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, minsize=60)

        # 简单logo（用Label实现，左上角）
        logo_label = tk.Label(root, text='🧬', font=('Arial', 18))
        logo_label.place(x=10, y=5)

        # 注释文件选择
        tk.Label(root, text='注释文件:', width=8, anchor='e').grid(row=0, column=0, sticky='e', padx=(40,10), pady=20)
        self.gtf_entry = tk.Entry(root, width=28)
        self.gtf_entry.grid(row=0, column=1, sticky='ew')
        tk.Button(root, text='选择', command=self.select_gtf).grid(row=0, column=2, padx=5)

        # 原始文件logo
        raw_logo_label = tk.Label(root, text='📄', font=('Arial', 16))
        raw_logo_label.place(x=10, y=60)

        # 原始文件选择
        tk.Label(root, text='原始文件:', width=8, anchor='e').grid(row=1, column=0, sticky='e', padx=(40,10), pady=10)
        self.tsv_entry = tk.Entry(root, width=28)
        self.tsv_entry.grid(row=1, column=1, sticky='ew')
        tk.Button(root, text='选择', command=self.select_tsv).grid(row=1, column=2, padx=5)

        # 输出文件名展示
        tk.Label(root, text='输出文件:', width=8, anchor='e').grid(row=2, column=0, sticky='e', padx=(40,10), pady=10)
        self.out_label = tk.Label(root, text='', anchor='w', width=28, fg='blue')
        self.out_label.grid(row=2, column=1, columnspan=2, sticky='w')

        # 进度条
        self.progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=3, pady=15)

        # 提示信息
        self.status_var = tk.StringVar()
        self.status_var.set('请选择注释文件和原始文件')
        self.status_label = tk.Label(root, textvariable=self.status_var, fg='green')
        self.status_label.grid(row=4, column=0, columnspan=3)

        # 圆角美化按钮
        self.run_btn = tk.Button(root, text='开始转换', width=20, relief='flat', bg='#e0e0e0', activebackground='#b0b0b0', borderwidth=0, font=('微软雅黑', 11), cursor='hand2', command=self.on_run)
        self.run_btn.grid(row=5, column=1, pady=18)
        self.run_btn.bind('<Enter>', self.on_btn_enter)
        self.run_btn.bind('<Leave>', self.on_btn_leave)

    def on_btn_enter(self, event):
        self.run_btn.config(bg='#b0b0b0')

    def on_btn_leave(self, event):
        self.run_btn.config(bg='#e0e0e0')

    def select_gtf(self):
        path = filedialog.askopenfilename(filetypes=[('GTF文件', '*.gtf'), ('所有文件', '*.*')])
        if path:
            self.gtf_entry.delete(0, tk.END)
            self.gtf_entry.insert(0, path)
            self.update_outfile()

    def select_tsv(self):
        path = filedialog.askopenfilename(filetypes=[('TSV文件', '*.tsv'), ('所有文件', '*.*')])
        if path:
            self.tsv_entry.delete(0, tk.END)
            self.tsv_entry.insert(0, path)
            self.update_outfile()

    def update_outfile(self):
        tsv = self.tsv_entry.get()
        if tsv:
            out = get_outfile_path(tsv)
            self.out_label.config(text=out)
        else:
            self.out_label.config(text='')

    def on_run(self):
        gtf = self.gtf_entry.get()
        tsv = self.tsv_entry.get()
        if not gtf or not tsv:
            messagebox.showwarning('提示', '请完整选择注释文件和原始文件')
            return
        out = get_outfile_path(tsv)
        self.progress['value'] = 0
        self.status_var.set('正在转换，请稍候...')
        self.run_btn.config(state='disabled')
        threading.Thread(target=self.run_convert, args=(gtf, tsv, out), daemon=True).start()

    def set_progress(self, value):
        self.progress['value'] = value
        self.root.update_idletasks()

    def run_convert(self, gtf, tsv, out):
        try:
            gene_map = parse_gtf(gtf)
            add_gene_name(tsv, out, gene_map, self.set_progress)
            self.status_var.set(f'转换完成！输出文件: {os.path.basename(out)}')
            messagebox.showinfo('完成', f'转换完成！\n输出文件: {os.path.basename(out)}')
        except Exception as e:
            self.status_var.set('转换失败')
            messagebox.showerror('错误', f'转换失败: {e}')
        finally:
            self.run_btn.config(state='normal')
            self.set_progress(0)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
