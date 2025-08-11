import sys
import os
from datetime import datetime

# Set Qt plugin path for Windows (PySide6)
if os.name == 'nt':
    import site
    try:
        # Try to find PySide6 plugins path
        for site_package in site.getsitepackages():
            qt_plugin_path = os.path.join(site_package, 'PySide6', 'plugins')
            if os.path.exists(qt_plugin_path):
                os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path
                break
    except:
        pass  # Ignore if site packages not found

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                           QPushButton, QTextEdit, QProgressBar, QFileDialog, QFrame, QGroupBox)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt, QThread, Signal as pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPalette, QColor
import arxiv_digest

class ApiTestWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, api_key, model):
        super().__init__()
        self.api_key = api_key
        self.model = model

    def run(self):
        try:
            import openai
            client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://api.siliconflow.cn/v1"
            )
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                timeout=10
            )
            self.finished.emit("API connection test successful! ✅")
            
        except Exception as e:
            self.error.emit(f"API connection test failed: {str(e)}")

class ArxivWorker(QThread):
    progress = pyqtSignal(str)
    progress_value = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, params):
        super().__init__()
        self.params = params
        self.current_progress = 0

    def progress_callback(self, message):
        self.progress.emit(message)
        
        # 更精确的进度计算
        if "开始分析" in message and "篇论文" in message:
            self.current_progress = 15
        elif "正在分析论文" in message and "(" in message and "/" in message:
            try:
                parts = message.split("(")[1].split(")")[0].split("/")
                current = int(parts[0])
                total = int(parts[1])
                # 分析阶段占总进度的60%，从15%到75%
                analysis_progress = int(15 + (current / total) * 60)
                self.current_progress = analysis_progress
            except:
                pass
        elif "成功分析了" in message:
            self.current_progress = 75
        elif "Translating abstract" in message or "正在翻译摘要" in message:
            self.current_progress = 85
        elif "创建结果目录" in message:
            self.current_progress = 90
        elif "正在保存报告" in message:
            self.current_progress = 95
        elif "摘要报告生成成功" in message:
            self.current_progress = 100
        
        self.progress_value.emit(self.current_progress)

    def run(self):
        try:
            # Set environment variables
            os.environ['SILICONFLOW_API_KEY'] = self.params['api_key']
            self.progress.emit("✨ Initializing...")
            self.progress_value.emit(10)
            
            # Create command line arguments
            sys.argv = [
                'arxiv_digest.py',
                '--provider', self.params['provider'],
                '--model', self.params['model'],
                '--lang', self.params['lang'],
                '--days', str(self.params['days']),
                '--max-results', str(self.params['max_results']),
                '--category', self.params['category']
            ]
            
            # Run main program
            arxiv_digest.main(self.progress_callback)
            
            # Read generated file
            report_date = datetime.now().strftime("%Y-%m-%d")
            result_filename = os.path.join("result", f"digest_{report_date}.md")
            
            if os.path.exists(result_filename):
                with open(result_filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if no papers found
                if "今日未发现新论文" in content or "No new papers found" in content:
                    content = "❌ 未搜索到相关文章\n\n请尝试：\n1. 调整搜索分类\n2. 增加搜索天数\n3. 检查网络连接"
                
                self.progress.emit("\n✨ Processing complete!")
                self.progress_value.emit(100)
                self.finished.emit(content)
            else:
                self.error.emit("生成的报告文件未找到")
            
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ArXiv LLM 论文摘要生成器 v2.0")
        self.setMinimumSize(900, 700)
        self.setStyleSheet(self.get_stylesheet())
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建布局
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建标题
        title_label = QLabel("🚀 ArXiv LLM 论文摘要生成器")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建设置区域
        settings_group = QGroupBox("⚙️ 配置设置")
        settings_group.setObjectName("settingsGroup")
        settings_layout = QVBoxLayout(settings_group)
        
        # Model selection
        model_layout = QHBoxLayout()
        model_label = QLabel("🤖 Model:")
        model_label.setObjectName("label")
        self.model_combo = QComboBox()
        self.model_combo.setObjectName("combo")
        models = [
            "Qwen/Qwen3-30B-A3B-Instruct-2507", "Qwen/Qwen3-235B-A22B-Thinking-2507", 
            "Qwen/Qwen3-235B-A22B-Instruct-2507", "baidu/ERNIE-4.5-300B-A47B", 
            "moonshotai/Kimi-K2-Instruct", "ascend-tribe/pangu-pro-moe", 
            "tencent/Hunyuan-A13B-Instruct", "MiniMaxAI/MiniMax-M1-80k", 
            "Tongyi-Zhiwen/QwenLong-L1-32B", "Qwen/Qwen3-30B-A3B", "Qwen/Qwen3-32B", 
            "Qwen/Qwen3-14B", "Qwen/Qwen3-8B", "Qwen/Qwen3-235B-A22B", 
            "THUDM/GLM-Z1-32B-0414", "THUDM/GLM-4-32B-0414", "THUDM/GLM-Z1-Rumination-32B-0414", 
            "THUDM/GLM-4-9B-0414", "Qwen/QwQ-32B", "Pro/deepseek-ai/DeepSeek-R1", 
            "Pro/deepseek-ai/DeepSeek-V3", "deepseek-ai/DeepSeek-R1", "deepseek-ai/DeepSeek-V3", 
            "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B", "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", 
            "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B", "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B", 
            "Pro/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B", "deepseek-ai/DeepSeek-V2.5", 
            "Qwen/Qwen2.5-72B-Instruct-128K", "Qwen/Qwen2.5-72B-Instruct", "Qwen/Qwen2.5-32B-Instruct", 
            "Qwen/Qwen2.5-14B-Instruct", "Qwen/Qwen2.5-7B-Instruct", "Qwen/Qwen2.5-Coder-32B-Instruct", 
            "Qwen/Qwen2.5-Coder-7B-Instruct", "Qwen/Qwen2-7B-Instruct", "TeleAI/TeleChat2", 
            "THUDM/glm-4-9b-chat", "Vendor-A/Qwen/Qwen2.5-72B-Instruct", "internlm/internlm2_5-7b-chat", 
            "Pro/Qwen/Qwen2.5-7B-Instruct", "Pro/Qwen/Qwen2-7B-Instruct", "Pro/THUDM/glm-4-9b-chat"
        ]
        self.model_combo.addItems(models)
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        model_layout.addStretch()
        settings_layout.addLayout(model_layout)
        
        # API key input
        api_layout = QHBoxLayout()
        api_label = QLabel("🔑 SiliconFlow API Key:")
        api_label.setObjectName("label")
        self.api_input = QLineEdit()
        self.api_input.setObjectName("input")
        self.api_input.setEchoMode(QLineEdit.Password)
        self.api_input.setPlaceholderText("Enter your SiliconFlow API key")
        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_input)
        settings_layout.addLayout(api_layout)
        
        # ArXiv category selection
        category_layout = QHBoxLayout()
        category_label = QLabel("📚 ArXiv官方分类:")
        category_label.setObjectName("label")
        self.category_combo = QComboBox()
        self.category_combo.setObjectName("combo")
        categories = [
            "q-bio.QM OR q-bio.BM OR cs.LG (推荐: 计算生物学)",
            "cs.CL OR cs.AI OR cs.LG (LLM与AI)",
            "q-bio.QM OR q-bio.BM OR q-bio.GN (生物信息学)",
            "cs.AI OR cs.LG OR q-bio.QM (AI与计算生物)",
            "q-bio.BM OR q-bio.SC OR q-bio.MN (分子生物学)",
            "cs.CL OR q-bio.QM OR q-bio.NC (语言模型与神经)",
            "stat.ML OR q-bio.QM OR cs.LG (统计与生物)",
            "q-bio.PE OR q-bio.NC OR cs.AI (进化与神经)",
            "q-bio.TO OR q-bio.CB OR cs.LG (组织与细胞)",
            "cs.CV OR q-bio.QM OR q-bio.BM (图像与生物)",
            "q-bio.QM (定量方法)",
            "q-bio.BM (生物分子)",
            "q-bio.GN (基因组学)",
            "q-bio.MN (分子网络)",
            "q-bio.NC (神经与认知)",
            "q-bio.CB (细胞行为)",
            "q-bio.PE (群体与进化)",
            "q-bio.SC (亚细胞过程)",
            "q-bio.TO (组织与器官)",
            "q-bio.OT (其他定量生物)",
            "cs.AI (人工智能)",
            "cs.LG (机器学习)",
            "cs.CL (计算语言学)",
            "cs.CV (计算机视觉)",
            "stat.ML (统计机器学习)",
            "cs (所有计算机科学)",
            "stat (统计学)"
        ]
        self.category_combo.addItems(categories)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        category_layout.addStretch()
        settings_layout.addLayout(category_layout)
        
        # 语言选择
        lang_layout = QHBoxLayout()
        lang_label = QLabel("🌐 输出语言:")
        lang_label.setObjectName("label")
        self.lang_combo = QComboBox()
        self.lang_combo.setObjectName("combo")
        self.lang_combo.addItems(["中文 (zh)", "英文 (en)"])
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        settings_layout.addLayout(lang_layout)
        
        # 天数和最大结果数设置（改为QLineEdit并限制只能输入数字）
        params_layout = QHBoxLayout()
        days_label = QLabel("📅 搜索天数:")
        days_label.setObjectName("label")
        self.days_input = QLineEdit()
        self.days_input.setObjectName("lineedit")
        self.days_input.setPlaceholderText("输入0表示无限搜索")
        self.days_input.setText("2")
        self.days_input.setFixedWidth(120)
        self.days_input.setValidator(QIntValidator(0, 365, self))

        max_results_label = QLabel("📊 最大文章数:")
        max_results_label.setObjectName("label")
        self.max_results_input = QLineEdit()
        self.max_results_input.setObjectName("lineedit")
        self.max_results_input.setPlaceholderText("如20")
        self.max_results_input.setText("20")
        self.max_results_input.setFixedWidth(80)
        self.max_results_input.setValidator(QIntValidator(1, 1000, self))

        # 添加说明标签
        help_label = QLabel("💡 提示: 天数设为0可搜索任意时期的论文")
        help_label.setObjectName("helpLabel")
        help_label.setStyleSheet("color: #7f8c8d; font-size: 10px; font-style: italic;")

        params_layout.addWidget(days_label)
        params_layout.addWidget(self.days_input)
        params_layout.addWidget(max_results_label)
        params_layout.addWidget(self.max_results_input)
        params_layout.addStretch()
        settings_layout.addLayout(params_layout)
        settings_layout.addWidget(help_label)
        
        # 添加测试按钮和开始按钮
        buttons_layout = QHBoxLayout()
        self.test_button = QPushButton("🔍 测试API连接")
        self.test_button.setObjectName("testButton")
        self.start_button = QPushButton("🚀 开始生成")
        self.start_button.setObjectName("startButton")
        buttons_layout.addWidget(self.test_button)
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addStretch()
        settings_layout.addLayout(buttons_layout)
        
        layout.addWidget(settings_group)
        
        # 添加进度区域
        progress_group = QGroupBox("📈 生成进度")
        progress_group.setObjectName("progressGroup")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        self.progress_label = QLabel("准备就绪...")
        self.progress_label.setObjectName("progressLabel")
        self.progress_label.setAlignment(Qt.AlignCenter)
        
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addWidget(progress_group)
        
        # 添加结果显示区域
        result_group = QGroupBox("📄 生成结果")
        result_group.setObjectName("resultGroup")
        result_layout = QVBoxLayout(result_group)
        
        self.result_text = QTextEdit()
        self.result_text.setObjectName("resultText")
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("生成的论文摘要将在这里显示...")
        
        result_layout.addWidget(self.result_text)
        layout.addWidget(result_group)
        
        # Connect signals
        self.start_button.clicked.connect(self.start_generation)
        self.test_button.clicked.connect(self.test_api)
        
        # Initialize
        self.worker = None
        self.api_test_worker = None

    def get_stylesheet(self):
        return """
        QMainWindow {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f8f9fa, stop: 1 #e9ecef);
        }
        
        #title {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            padding: 20px;
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                      stop: 0 #667eea, stop: 1 #764ba2);
            color: white;
            border-radius: 15px;
            margin-bottom: 10px;
        }
        
        QGroupBox {
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
            border: 2px solid #bdc3c7;
            border-radius: 12px;
            margin-top: 10px;
            padding-top: 10px;
            background: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 8px 0 8px;
            color: #34495e;
        }
        
        #label {
            font-size: 12px;
            font-weight: bold;
            color: #34495e;
            min-width: 100px;
        }
        
        #combo, #spinbox {
            padding: 8px 12px;
            border: 2px solid #bdc3c7;
            border-radius: 8px;
            background: white;
            font-size: 12px;
            min-height: 20px;
        }
        
        #combo:focus, #spinbox:focus {
            border-color: #3498db;
            outline: none;
        }
        
        #input {
            padding: 10px 15px;
            border: 2px solid #bdc3c7;
            border-radius: 8px;
            background: white;
            font-size: 12px;
            min-height: 20px;
        }
        
        #input:focus {
            border-color: #3498db;
            outline: none;
        }
        
        #lineedit {
            padding: 8px 12px;
            border: 2px solid #bdc3c7;
            border-radius: 8px;
            background: white;
            font-size: 12px;
            min-height: 20px;
        }
        
        #lineedit:focus {
            border-color: #3498db;
            outline: none;
        }
        
        #testButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #74b9ff, stop: 1 #0984e3);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: bold;
            min-width: 140px;
        }
        
        #testButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #81c784, stop: 1 #4caf50);
        }
        
        #testButton:pressed {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #5dade2, stop: 1 #3498db);
        }
        
        #testButton:disabled {
            background: #bdc3c7;
            color: #7f8c8d;
        }
        
        #startButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #fd79a8, stop: 1 #e84393);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: bold;
            min-width: 140px;
        }
        
        #startButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #ff7675, stop: 1 #d63031);
        }
        
        #startButton:pressed {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #fab1a0, stop: 1 #e17055);
        }
        
        #startButton:disabled {
            background: #bdc3c7;
            color: #7f8c8d;
        }
        
        #progressBar {
            border: 2px solid #bdc3c7;
            border-radius: 8px;
            background: #ecf0f1;
            text-align: center;
            font-weight: bold;
            color: #2c3e50;
            min-height: 25px;
        }
        
        #progressBar::chunk {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                      stop: 0 #667eea, stop: 1 #764ba2);
            border-radius: 6px;
            margin: 2px;
        }
        
        #progressLabel {
            font-size: 12px;
            color: #34495e;
            font-weight: bold;
            padding: 5px;
        }
        
        #resultText {
            border: 2px solid #bdc3c7;
            border-radius: 8px;
            background: white;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 11px;
            padding: 10px;
            line-height: 1.4;
        }
        
        #resultText:focus {
            border-color: #3498db;
            outline: none;
        }
        """

    def test_api(self):
        api_key = self.api_input.text()
        model = self.model_combo.currentText()
        
        if not api_key:
            self.result_text.setText("❌ Please enter API key")
            return
            
        # Disable test button and show testing status
        self.test_button.setEnabled(False)
        self.test_button.setText("🔄 Testing...")
        self.result_text.setText("🔍 Testing API connection...")
        self.progress_label.setText("Testing API connection...")
        
        # Create and start API test thread
        self.api_test_worker = ApiTestWorker(api_key, model)
        self.api_test_worker.finished.connect(self.api_test_finished)
        self.api_test_worker.error.connect(self.api_test_error)
        self.api_test_worker.start()
    
    def api_test_finished(self, message):
        self.result_text.setText(message)
        self.progress_label.setText("API测试完成")
        self.test_button.setEnabled(True)
        self.test_button.setText("🔍 测试API连接")
        
    def api_test_error(self, error_message):
        self.result_text.setText(f"❌ {error_message}")
        self.progress_label.setText("API测试失败")
        self.test_button.setEnabled(True)
        self.test_button.setText("🔍 测试API连接")

    def start_generation(self):
        # Get parameters
        try:
            days = int(self.days_input.text())
            max_results = int(self.max_results_input.text())
        except Exception:
            self.result_text.setText("Please enter valid days and article count (positive integers)")
            return
            
        # Get selected category
        category_text = self.category_combo.currentText()
        if "推荐: 计算生物学" in category_text:
            category = "q-bio.QM OR q-bio.BM OR cs.LG"
        else:
            category = category_text.split(" (")[0]
            
        params = {
            'provider': 'siliconflow',
            'model': self.model_combo.currentText(),
            'api_key': self.api_input.text(),
            'lang': self.lang_combo.currentText()[-3:-1],
            'days': days,
            'max_results': max_results,
            'category': category
        }
        
        # Validate API key
        if not params['api_key']:
            self.result_text.setText("Please enter API key")
            return
            
        # Disable buttons
        self.start_button.setEnabled(False)
        self.test_button.setEnabled(False)
        self.start_button.setText("🔄 Generating...")
        
        # Reset progress bar
        self.progress_bar.setValue(0)
        self.progress_label.setText("Starting generation...")
        
        # Create and start worker thread
        self.worker = ArxivWorker(params)
        self.worker.progress.connect(self.update_progress)
        self.worker.progress_value.connect(self.update_progress_bar)
        self.worker.finished.connect(self.generation_complete)
        self.worker.error.connect(self.handle_error)
        self.worker.start()
        
    def update_progress(self, message):
        self.result_text.append(message)
        self.progress_label.setText(message.replace("✨", "").strip())
        
    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)
        
    def generation_complete(self, content):
        self.result_text.setText(content)
        self.progress_bar.setValue(100)
        self.progress_label.setText("✅ 生成完成！")
        self.start_button.setEnabled(True)
        self.test_button.setEnabled(True)
        self.start_button.setText("🚀 开始生成")
        
    def handle_error(self, error_message):
        self.result_text.setText(f"❌ 发生错误：{error_message}")
        self.progress_label.setText("❌ 生成失败")
        self.progress_bar.setValue(0)
        self.start_button.setEnabled(True)
        self.test_button.setEnabled(True)
        self.start_button.setText("🚀 开始生成")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    # 设置应用程序图标和信息
    app.setApplicationName("ArXiv LLM 论文摘要生成器")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("ArXiv Tools")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
