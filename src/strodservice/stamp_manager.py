from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
from PIL import Image, ImageDraw, ImageFont

def add_stamp(document_path):
    # Открытие PDF, добавление штампа
    # или использование reportlab для PDF
    pass