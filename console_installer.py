#!/usr/bin/env python3
"""
Консольный установщик с интерактивным интерфейсом.
Демонстрирует логику установки с согласиями, выбором пути и визуализацией прогресса.
"""

import os
import time
import shutil
from pathlib import Path


def print_header():
    """Печать заголовка установщика"""
    print("="*60)
    print("                    УСТАНОВКА ПРИЛОЖЕНИЯ")
    print("="*60)


def show_license():
    """Показать лицензионное соглашение и получить согласие"""
    print("\nЛИЦЕНЗИОННОЕ СОГЛАШЕНИЕ")
    print("-" * 30)
    print("""
Данное программное обеспечение защищено законами об авторских правах.
Устанавливая и используя это приложение, вы соглашаетесь со следующими условиями:

1. Вы можете использовать это программное обеспечение в личных целях.
2. Запрещено распространять это программное обеспечение без разрешения.
3. Автор не несет ответственности за ущерб, причиненный использованием этого ПО.
4. Все права собственности принадлежат разработчику.

Нажмите 'y' чтобы согласиться с условиями лицензии или 'n' для отказа.
    """)
    
    while True:
        choice = input("Соглашаетесь с лицензией? (y/n): ").lower().strip()
        if choice in ['y', 'yes', 'да']:
            return True
        elif choice in ['n', 'no', 'нет']:
            return False
        else:
            print("Пожалуйста, введите 'y' для согласия или 'n' для отказа.")


def get_install_path():
    """Получить путь установки от пользователя"""
    print("\nПУТЬ УСТАНОВКИ")
    print("-" * 30)
    
    default_path = os.path.join(os.path.expanduser("~"), "MyApp")
    path = input(f"Введите путь для установки (по умолчанию: {default_path}): ").strip()
    
    if not path:
        path = default_path
    
    # Проверить и создать папку при необходимости
    path = os.path.abspath(path)
    os.makedirs(path, exist_ok=True)
    
    print(f"Приложение будет установлено в: {path}")
    confirm = input("Продолжить? (y/n): ").lower().strip()
    
    if confirm in ['y', 'yes', 'да']:
        return path
    else:
        print("Установка отменена пользователем.")
        return None


def simulate_installation(path):
    """Имитация процесса установки"""
    print("\nПРОЦЕСС УСТАНОВКИ")
    print("-" * 30)
    
    steps = [
        ("Проверка системы", 1),
        ("Создание папки установки", 1),
        ("Копирование файлов", 3),
        ("Настройка параметров", 1),
        ("Создание ярлыков", 1),
        ("Завершение установки", 1)
    ]
    
    total_steps = len(steps)
    for i, (step, duration) in enumerate(steps, 1):
        progress = int((i / total_steps) * 100)
        print(f"[{progress:3d}%] {step}...", end="", flush=True)
        
        # Имитация работы
        time.sleep(duration)
        
        # Создание фиктивных файлов в процессе установки
        if step == "Копирование файлов":
            create_app_files(path)
        elif step == "Создание ярлыков":
            create_shortcut(path)
        
        print(" Готово")
    
    print(f"\nУстановка завершена успешно!")
    print(f"Приложение установлено в: {path}")


def create_app_files(path):
    """Создать фиктивные файлы приложения"""
    app_dir = Path(path) / "app"
    app_dir.mkdir(exist_ok=True)
    
    # Создать фиктивные файлы приложения
    files = [
        "main.py",
        "config.json", 
        "data.txt",
        "__init__.py"
    ]
    
    for file in files:
        (app_dir / file).touch()


def create_shortcut(path):
    """Создать ярлык/скрипт запуска"""
    launcher_script = Path(path) / "launch_app.sh"
    launcher_script.write_text("#!/bin/bash\necho 'Запуск приложения...'\n", encoding='utf-8')
    launcher_script.chmod(0o755)  # Сделать исполняемым


def create_readme(path):
    """Создать файл README"""
    readme_path = Path(path) / "README.txt"
    readme_path.write_text("""
ДОБРО ПОЖАЛОВАТЬ В УСТАНОВЛЕННОЕ ПРИЛОЖЕНИЕ!

Это файл README, содержащий информацию о приложении.
Здесь вы можете найти инструкции по использованию и другие полезные сведения.

СТРУКТУРА УСТАНОВКИ:
- app/ - основные файлы приложения
- launch_app.sh - скрипт для запуска приложения
- README.txt - этот файл

СПАСИБО ЗА УСТАНОВКУ!
    """, encoding='utf-8')


def post_installation_options(path):
    """Предложить действия после установки"""
    print("\nДОПОЛНИТЕЛЬНЫЕ ДЕЙСТВИЯ")
    print("-" * 30)
    
    print("1. Открыть файл README")
    print("2. Запустить приложение")
    print("3. Завершить установку")
    
    while True:
        try:
            choice = int(input("Выберите действие (1-3): "))
            if choice == 1:
                readme_path = os.path.join(path, "README.txt")
                print(f"\nСодержимое {readme_path}:")
                print("-" * 40)
                with open(readme_path, 'r', encoding='utf-8') as f:
                    print(f.read())
                print("-" * 40)
                continue
            elif choice == 2:
                print(f"\nЗапуск приложения из {path}")
                print("Имитация запуска приложения...")
                time.sleep(2)
                print("Приложение успешно запущено (в реальности здесь будет запуск настоящего приложения)")
                break
            elif choice == 3:
                break
            else:
                print("Пожалуйста, выберите число от 1 до 3.")
        except ValueError:
            print("Пожалуйста, введите число.")


def main():
    print_header()
    
    # Показать лицензию и получить согласие
    if not show_license():
        print("\nУстановка отменена: пользователь не согласился с лицензией.")
        return
    
    # Получить путь установки
    install_path = get_install_path()
    if not install_path:
        return
    
    # Создать README до установки
    create_readme(install_path)
    
    # Имитация процесса установки
    simulate_installation(install_path)
    
    # Действия после установки
    post_installation_options(install_path)
    
    print(f"\nУстановка завершена успешно!")
    print(f"Приложение установлено в: {install_path}")
    print("Спасибо за установку!")


if __name__ == "__main__":
    main()