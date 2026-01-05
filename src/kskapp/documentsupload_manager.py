from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import os
from werkzeug.utils import secure_filename

def save_document(file, object_id, doc_type):
    filename = secure_filename(file.filename)
    path = f"documents/generated/{object_id}/{doc_type}/{filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path)
    # Сохранить в БД