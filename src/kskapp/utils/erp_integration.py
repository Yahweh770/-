from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import requests
import json

class ERPIntegration:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = (username, password)

    def sync_objects_to_erp(self, objects):
        """
        Отправка объектов в 1С
        """
        url = f"{self.base_url}/objects"
        headers = {"Content-Type": "application/json"}
        for obj in objects:
            data = {
                "name": obj.name,
                "location": obj.location
            }
            response = requests.post(url, data=json.dumps(data), auth=self.auth, headers=headers)
            if response.status_code != 200:
                print(f"Ошибка синхронизации объекта {obj.name}")

    def sync_materials_to_erp(self, materials):
        """
        Отправка материалов в 1С
        """
        url = f"{self.base_url}/materials"
        headers = {"Content-Type": "application/json"}
        for mat in materials:
            data = {
                "name": mat.name,
                "unit": mat.unit,
                "norm": mat.norm
            }
            response = requests.post(url, data=json.dumps(data), auth=self.auth, headers=headers)
            if response.status_code != 200:
                print(f"Ошибка синхронизации материала {mat.name}")