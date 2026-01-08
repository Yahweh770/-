#!/usr/bin/env python3
"""
Установочный скрипт для проекта Strod-Service Technology
Позволяет легко собрать исполняемый файл приложения
"""

import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Установить зависимости из requirements.txt"""
    print("Устанавливаю основные зависимости из requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Основные зависимости успешно установлены!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке зависимостей: {e}")
        return False

def build_executable():
    """Запустить процесс сборки исполняемого файла"""
    print("Запускаю процесс сборки исполняемого файла...")
    try:
        # Импортируем и вызываем функцию из build_exe.py
        import build_exe
        return build_exe.main()
    except ImportError as e:
        print(f"Ошибка импорта build_exe: {e}")
        return False
    except Exception as e:
        print(f"Ошибка при сборке: {e}")
        return False

def main():
    print("Установка и сборка проекта Strod-Service Technology")
    print("="*50)
    
    # Проверяем, что мы в правильной директории
    if not Path("requirements.txt").exists():
        print("Ошибка: файл requirements.txt не найден. Убедитесь, что вы запускаете скрипт из корня проекта.")
        sys.exit(1)
    
    # Устанавливаем зависимости
    if not install_dependencies():
        print("Не удалось установить зависимости. Завершение работы.")
        sys.exit(1)
    
    # Запускаем сборку
    build_executable()

if __name__ == "__main__":
    main()