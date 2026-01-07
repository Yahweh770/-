from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))

# Теперь можно безопасно импортировать PyInstaller
import PyInstaller.__main__
from PyInstaller.utils.hooks import collect_data_files

PyInstaller.__main__.run([
    '--name=StrodServiceTechnology',
    '--windowed',
    '--add-data=data;data',
    '--add-data=assets;assets',
    '--hidden-import=PyQt5.sip',
    '--hidden-import=sqlalchemy',
    '--hidden-import=PIL',
    '--hidden-import=PIL.Image',
    'main.py'
])