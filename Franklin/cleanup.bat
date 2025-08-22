@echo off
echo Cleaning up redundant files...

:: 1. 创建备份目录（如果不存在）
if not exist backup_files mkdir backup_files

:: 2. 备份现有文件
if exist search_module.py copy search_module.py backup_files\
if exist keyword_extractor.py copy keyword_extractor.py backup_files\
if exist analysis_module.py copy analysis_module.py backup_files\
if exist main.py copy main.py backup_files\
if exist test_keyword_extraction.py copy test_keyword_extraction.py backup_files\

:: 3. 删除现有的标准版本文件
if exist search_module.py del search_module.py
if exist keyword_extractor.py del keyword_extractor.py
if exist analysis_module.py del analysis_module.py

:: 4. 重命名 clean 版本为标准版本
if exist search_module_clean.py rename search_module_clean.py search_module.py
if exist keyword_extractor_clean.py rename keyword_extractor_clean.py keyword_extractor.py
if exist analysis_module_clean.py rename analysis_module_clean.py analysis_module.py

:: 5. 删除不需要的文件
if exist main.py del main.py
if exist test_keyword_extraction.py del test_keyword_extraction.py

:: 6. 清理临时文件和缓存
if exist __pycache__ rmdir /s /q __pycache__

echo Done! Original files have been backed up to 'backup_files' directory.
echo Current project structure is now clean and optimized.
pause
