from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import os
from jinja2 import Template
from core.stamp_manager import add_stamp

def generate_executive_document(object_id, template_path, output_path):
    # Загрузка шаблона
    with open(template_path, 'r', encoding='utf-8') as f:
        template = Template(f.read())

    # Данные из БД
    context = get_context_from_db(object_id)
    result = template.render(context)

    # Сохранение документа
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    # Автоштамп
    add_stamp(output_path)