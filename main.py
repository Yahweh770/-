"""
Основной модуль запуска приложения KSK Shop.

Этот модуль отвечает за:
- Настройку путей к ресурсам
- Инициализацию логирования
- Создание подключения к базе данных
- Запуск графического интерфейса
"""

import sys
from pathlib import Path
import logging

# --- Определение корня проекта и ресурсов ---
if getattr(sys, 'frozen', False):
    # Приложение запускается из exe-файла
    BASE_DIR = Path(sys.executable).parent
    MEIPASS_DIR = Path(sys._MEIPASS)  # Временная папка PyInstaller
else:
    # Обычный запуск из Python
    BASE_DIR = Path(__file__).resolve().parent
    MEIPASS_DIR = BASE_DIR

# Добавляем корень проекта в sys.path для корректной работы импортов
sys.path.insert(0, str(BASE_DIR))

def resource_path(relative_path):
    """
    Возвращает абсолютный путь к ресурсу.
    
    Args:
        relative_path: Относительный путь к ресурсу
    
    Returns:
        Path: Абсолютный путь к ресурсу
    """
    return MEIPASS_DIR / relative_path

# Пути к папкам данных и логов
DATA_DIR = resource_path("data")
LOGS_DIR = resource_path("logs")

# Создаем директории, если они не существуют
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# --- Импорты внешних библиотек ---
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Импорт собственных модулей ---
from utils.logger import setup_logger
from database.init_db import init_db
from desktop.main_window import MainWindow
from PyQt5.QtWidgets import QApplication

# --- Настройка подключения к базе данных ---
DB_FILE = DATA_DIR / "ksk.db"
engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def main():
    """
    Основная функция запуска приложения.
    """
    # Настройка логирования
    logger = setup_logger(name="ksk-main", level=logging.INFO, logs_dir=LOGS_DIR)
    logger.info("🚀 Запуск KSK Shop приложения")

    # Инициализация базы данных
    init_db(engine)
    logger.info("✅ База данных инициализирована")

    # Создание и запуск Qt приложения
    qt_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    logger.info("Главное окно отображено")
    
    # Запуск цикла обработки событий
    exit_code = qt_app.exec()
    logger.info("Приложение завершено")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
