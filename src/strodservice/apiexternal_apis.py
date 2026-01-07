from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import requests

def get_fuel_balance(card_id):
    response = requests.get(f"https://api.fuelcard.com/balance/{card_id}")
    return response.json()