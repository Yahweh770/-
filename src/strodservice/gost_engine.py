from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
def get_material_norm(material_name):
    norms = {
        'Термопласт': 0.3,
        'Алкидная краска': 0.2
    }
    return norms.get(material_name, 0.0)