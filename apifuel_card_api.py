from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import requests

def get_fuel_balance(card_id):
    try:
        response = requests.get(f"https://api.fuelcard.com/balance/{card_id}")
        response.raise_for_status()
        data = response.json()
        return data.get('balance', 0.0)
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return 0.0

def get_fuel_transactions(card_id, limit=10):
    try:
        response = requests.get(f"https://api.fuelcard.com/transactions/{card_id}?limit={limit}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка при запросе транзакций: {e}")
        return []