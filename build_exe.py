#!/usr/bin/env python3
"""
Скрипт для автоматической компиляции проекта Strod-Service Technology в исполняемый файл (exe).
После запуска этого скрипта будет создан exe-файл, который можно запустить из коробки.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import platform

def install_pyinstaller():
    """Установить PyInstaller, если он не установлен"""
    try:
        import PyInstaller
        print("PyInstaller уже установлен")
    except ImportError:
        print("Устанавливаю PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller успешно установлен")

def create_executable():
    """Создать исполняемый файл из проекта"""
    print("Начинаю процесс компиляции проекта в исполняемый файл...")
    
    # Убедимся, что мы в корне проекта
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Установим PyInstaller
    install_pyinstaller()
    
    # Путь к основному файлу приложения
    main_script = "run_app.py"
    
    # Проверим, существует ли основной скрипт
    if not Path(main_script).exists():
        print(f"Ошибка: файл {main_script} не найден!")
        return False
    
    # Определяем правильный разделитель для --add-data в зависимости от ОС
    if platform.system() == "Windows":
        separator = ";"
    else:
        separator = ":"
    
    # Опции для PyInstaller
    pyinstaller_options = [
        "--onefile",           # Создать один исполняемый файл
        "--windowed",          # Не показывать консольное окно (для GUI приложений)
        "--name=StrodService", # Имя исполняемого файла
        f"--add-data=assets{separator}assets", # Добавить папку assets
        f"--add-data=data{separator}data",     # Добавить папку data
        f"--add-data=docs{separator}docs",     # Добавить папку docs
        f"--add-data=filestorage{separator}filestorage", # Добавить папку filestorage
        "--hidden-import=sqlalchemy.sql.default_comparator", # Добавить импорт для SQLAlchemy
        "--hidden-import=sqlalchemy.dialects.sqlite", # Добавить импорт для SQLite
        "--collect-all=PyQt5", # Собрать все модули PyQt5
        "--clean",             # Очистить кэш перед компиляцией
    ]
    
    # Команда для PyInstaller
    cmd = [sys.executable, "-m", "PyInstaller"] + pyinstaller_options + [main_script]
    
    print(f"Выполняю команду: {' '.join(cmd)}")
    
    try:
        # Запускаем PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Компиляция завершена успешно!")
        print(result.stdout)
        
        # Найдем созданный исполняемый файл
        dist_dir = project_root / "dist"
        
        # В зависимости от ОС, имя файла может отличаться
        if platform.system() == "Windows":
            exe_files = list(dist_dir.glob("*.exe"))
        else:
            # На Linux/Mac файл не имеет расширения .exe
            exe_files = list(dist_dir.glob("StrodService"))
        
        if exe_files:
            exe_path = exe_files[0]
            print(f"Исполняемый файл создан: {exe_path}")
            
            # Копируем exe в корень проекта для удобства
            if platform.system() == "Windows":
                final_exe = project_root / f"{exe_path.name}"
            else:
                final_exe = project_root / f"{exe_path.name}"
            shutil.copy2(exe_path, final_exe)
            print(f"Исполняемый файл скопирован в: {final_exe}")
            
            return True
        else:
            print("Не удалось найти созданный исполняемый файл")
            # Покажем, что есть в директории dist
            print(f"Содержимое директории dist: {list(dist_dir.iterdir())}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при компиляции: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return False

def create_launcher_script():
    """Создать скрипт для запуска компиляции"""
    launcher_content = '''@echo off
echo Компилирую проект Strod-Service Technology в исполняемый файл...
python build_exe.py
echo.
echo Процесс компиляции завершен. Нажмите любую клавишу для выхода...
pause >nul
'''
    
    with open("compile_to_exe.bat", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print("Создан скрипт compile_to_exe.bat для Windows")

def create_launcher_script_sh():
    """Создать bash-скрипт для запуска компиляции"""
    launcher_content = '''#!/bin/bash
echo "Компилирую проект Strod-Service Technology в исполняемый файл..."
python3 build_exe.py
echo
echo "Процесс компиляции завершен."
'''
    
    with open("compile_to_exe.sh", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    # Сделаем скрипт исполняемым
    os.chmod("compile_to_exe.sh", 0o755)
    
    print("Создан скрипт compile_to_exe.sh для Linux/Mac")

def main():
    print("Скрипт автоматической компиляции проекта Strod-Service Technology")
    print("="*60)
    
    success = create_executable()
    
    if success:
        create_launcher_script()
        create_launcher_script_sh()
        print("\n" + "="*60)
        print("Компиляция завершена успешно!")
        print("Теперь вы можете:")
        if platform.system() == "Windows":
            print("1. Запустить 'StrodService.exe' для запуска приложения")
        else:
            print("1. Запустить './StrodService' для запуска приложения")
        print("2. Использовать 'compile_to_exe.bat' или 'compile_to_exe.sh' для повторной компиляции")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("Произошла ошибка при компиляции проекта")
        print("="*60)
        sys.exit(1)

if __name__ == "__main__":
    main()