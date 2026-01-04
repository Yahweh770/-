from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def export_field_data_to_excel(filepath):
    from utils.offline_storage import load_field_data_offline
    data = load_field_data_offline()

    if not data:
        QMessageBox.warning(None, "Экспорт", "Нет данных для экспорта.")
        return

    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False)
    QMessageBox.information(None, "Экспорт", f"Данные экспортированы в: {filepath}")