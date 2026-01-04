from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import requests
import subprocess
import sys
import os
from PyQt5.QtWidgets import QMessageBox

def check_for_updates():
    try:
        response = requests.get("https://api.github.com/repos/yourusername/yourrepo/releases/latest")
        latest_version = response.json()["tag_name"]
        current_version = "v1.0.0"  # Укажите текущую версию

        if latest_version != current_version:
            return latest_version
        return None
    except Exception as e:
        print(f"Ошибка проверки обновлений: {e}")
        return None

def download_update(url, filename):
    try:
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Ошибка скачивания: {e}")
        return False

def update_app():
    latest_version = check_for_updates()
    if latest_version:
        reply = QMessageBox.question(None, "Обновление", f"Доступна новая версия: {latest_version}. Обновить?")
        if reply == QMessageBox.Yes:
            # Здесь можно скачать и установить новую версию
            QMessageBox.information(None, "Обновление", "Функция обновления в разработке.")
    else:
        QMessageBox.information(None, "Обновление", "У вас последняя версия.")