from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import os
import zipfile
from datetime import datetime
import requests

def backup_to_cloud(file_path, cloud_url, token):
    """
    Загружает файл в облако
    """
    headers = {"Authorization": f"Bearer {token}"}
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(cloud_url, files=files, headers=headers)
    return response.status_code == 200

def create_and_upload_backup():
    backup_path = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    with zipfile.ZipFile(backup_path, 'w') as zf:
        zf.write("app_data.db", "app_data.db")
    # Загрузка в облако
    success = backup_to_cloud(backup_path, "https://api.cloud.com/upload", "TOKEN")
    if success:
        print("Бэкап загружен в облако")
    else:
        print("Ошибка загрузки бэкапа")
    os.remove(backup_path)