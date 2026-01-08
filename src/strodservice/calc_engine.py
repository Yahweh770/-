from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
from strodservice.models.models import LineType, Material
from strodservice.database.init_db import SessionLocal, engine
from strodservice.gost_engine import get_material_norm

def calculate_materials_for_object(object_id, line_data):
    """
    line_data = [
        {'type_id': 1, 'length': 100.0, 'width': 0.15},
        ...
    ]
    """
    total = 0
    session = SessionLocal()
    for line in line_data:
        line_type = session.query(LineType).get(line['type_id'])
        material = session.query(Material).get(line_type.material_id)
        norm = get_material_norm(material.name)
        volume = line['length'] * line['width'] * norm
        total += volume
    session.close()
    return total

def calculate_materials_with_gost(material_name, length, width):
    norm = get_material_norm(material_name)
    return length * width * norm