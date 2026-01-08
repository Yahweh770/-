from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import pandas as pd
from strodservice.models.models import FieldData, Object
from strodservice.database.init_db import SessionLocal
from datetime import datetime

def generate_excel_report(filepath):
    session = SessionLocal()
    data = session.query(FieldData).all()
    objects = session.query(Object).all()
    session.close()

    df = pd.DataFrame([
        {
            'ID': d.id,
            'Объект': next((o.name for o in objects if o.id == d.object_id), 'Неизвестно'),
            'Тип линии': d.line_type,
            'Длина': d.length,
            'Ширина': d.width,
            'Расход': d.material_used,
            'Дата': d.date,
            'Заметки': d.notes
        }
        for d in data
    ])

    df.to_excel(filepath, index=False, engine='openpyxl')