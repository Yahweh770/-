"""
Тестовый скрипт для проверки работоспособности приложения Strod-Service Technology.
"""

import sys
import os
from pathlib import Path

# Добавляем корень проекта в путь для импорта
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Тестирование импорта всех модулей приложения."""
    print("Проверка импорта модулей...")
    
    try:
        # Тестируем основные импорты
        from main import main
        print("✓ Успешно импортирован main")
        
        from utils.logger import setup_logger
        print("✓ Успешно импортирован logger")
        
        from database.init_db import init_db
        print("✓ Успешно импортирован init_db")
        
        from models.models import Object, Material, FieldData
        print("✓ Успешно импортированы модели")
        
        from desktop.main_window import MainWindow
        print("✓ Успешно импортировано главное окно")
        
        from desktop.objects_window import ObjectsWindow
        print("✓ Успешно импортировано окно объектов")
        
        from desktop.materials_window import MaterialsWindow
        print("✓ Успешно импортировано окно материалов")
        
        from desktop.reports_window import ReportsWindow
        print("✓ Успешно импортировано окно отчетов")
        
        from utils.image_handler import ImageHandler
        print("✓ Успешно импортирован обработчик изображений")
        
        return True
    except ImportError as e:
        print(f"✗ Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"✗ Неожиданная ошибка: {e}")
        return False

def test_database():
    """Тестирование инициализации базы данных."""
    print("\nПроверка инициализации базы данных...")
    
    try:
        from sqlalchemy import create_engine
        from database.init_db import init_db
        
        # Создаем временный движок для теста
        engine = create_engine("sqlite:///:memory:", echo=False)
        init_db(engine)
        print("✓ База данных успешно инициализирована")
        return True
    except Exception as e:
        print(f"✗ Ошибка инициализации базы данных: {e}")
        return False

def test_image_handler():
    """Тестирование обработчика изображений."""
    print("\nПроверка обработчика изображений...")
    
    try:
        from utils.image_handler import ImageHandler
        
        # Создаем обработчик изображений
        handler = ImageHandler()
        print("✓ Обработчик изображений успешно создан")
        
        # Проверяем поддерживаемые форматы
        expected_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
        if expected_formats.issubset(handler.SUPPORTED_FORMATS):
            print("✓ Поддерживаемые форматы изображений корректны")
        else:
            print(f"✗ Некорректные поддерживаемые форматы: {handler.SUPPORTED_FORMATS}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Ошибка обработчика изображений: {e}")
        return False

def main():
    """Основная функция тестирования."""
    print("Запуск тестирования приложения Strod-Service Technology...")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Выполняем тесты
    all_tests_passed &= test_imports()
    all_tests_passed &= test_database()
    all_tests_passed &= test_image_handler()
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("✓ Все тесты пройдены успешно!")
        print("Приложение готово к использованию.")
    else:
        print("✗ Некоторые тесты не пройдены.")
        print("Проверьте конфигурацию приложения.")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)