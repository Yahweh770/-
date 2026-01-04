from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
def get_gpr_data():
    # Пример данных
    return [
        {'object': 'Объект 1', 'plan': 100, 'fact': 95},
        {'object': 'Объект 2', 'plan': 80, 'fact': 85},
        {'object': 'Объект 3', 'plan': 120, 'fact': 110}
    ]