from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import json
from database.models import FieldData
from database.init_db import Session
from datetime import datetime

DATA_FILE = "offline_data.json"

def sync_offline_to_db():
    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    session = Session()
    for record in records:
        # Проверяем, есть ли уже запись с такой датой и объектом
        existing = session.query(FieldData).filter(
            FieldData.date == datetime.fromisoformat(record["date"]),
            FieldData.object_id == record.get("object_id", 0)  # или имя объекта
        ).first()

        if not existing:
            new_record = FieldData(
                object_id=0,  # можно искать по имени, если объекты есть
                line_type_id=0,  # аналогично
                length=record["length"],
                width=record["width"],
                material_used=record["material_used"],
                photo_path=record["photo_path"],
                date=datetime.fromisoformat(record["date"]),
                notes=record["notes"]
            )
            session.add(new_record)

    session.commit()
    session.close()

    # Удалить JSON после синхронизации
    os.remove(DATA_FILE)