from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import winreg
import sys
import os

def add_to_startup():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "ExecutiveDocTool"
    app_path = os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, app_path)
        print("Добавлено в автозапуск")
    except Exception as e:
        print(f"Ошибка добавления в автозапуск: {e}")

def remove_from_startup():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "ExecutiveDocTool"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, app_name)
        print("Удалено из автозапуска")
    except FileNotFoundError:
        print("Приложение не найдено в автозапуске")
    except Exception as e:
        print(f"Ошибка удаления из автозапуска: {e}")