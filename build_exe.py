from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
from PyInstaller.utils.hooks import collect_data_files
import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=ExecutiveDocTool',
    '--windowed',
    '--add-data=templates;templates',
    '--add-data=config;config',
    '--add-data=utils;utils',
    '--add-data=core;core',
    '--add-data=database;database',
    '--add-data=api;api',
    '--hidden-import=PyQt5.sip',
    'desktop/main_window.py'
])