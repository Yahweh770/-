import sys
from pathlib import Path
import logging

# Добавляем путь к src в sys.path для правильного импорта модулей
src_path = Path(__file__).resolve().parent.parent  # /workspace/src
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# --- Корень проекта и ресурсы ---
if getattr(sys, 'frozen', False):
    # Запуск из exe
    BASE_DIR = Path(sys.executable).parent
    MEIPASS_DIR = Path(sys._MEIPASS)  # PyInstaller временная папка
else:
    # Обычный запуск из Python
    BASE_DIR = Path(__file__).resolve().parent.parent
    MEIPASS_DIR = BASE_DIR

# При использовании proper package structure, sys.path добавление не требуется
# когда запускаем как python -m src.strodservice.main

# Функция для получения пути к ресурсам (иконки, база, файлы)
def resource_path(relative_path):
    return MEIPASS_DIR / relative_path

# Пути к папкам данных и логов
DATA_DIR = resource_path("data")
LOGS_DIR = resource_path("logs")
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# --- Импорты внешних библиотек ---
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Импорт собственных модулей ---
from strodservice.utils.logger import setup_logger
from strodservice.database.init_db import init_db
from strodservice.desktop.main_window import MainWindow  # ← исправлено на абсолютный импорт
from PyQt5.QtWidgets import QApplication

# --- Engine базы данных ---
DB_FILE = DATA_DIR / "ksk.db"
from strodservice.database.init_db import engine, SessionLocal

def main():
    """Main entry point for the application."""
    logger = setup_logger(name="strodservice-main", level=logging.INFO)
    logger.info("🚀 Запуск Strod-Service Technology приложения")

    # Инициализация базы данных
    init_db()
    logger.info("✅ База данных инициализирована")

    # Создание и запуск Qt приложения
    qt_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    logger.info("Главное окно отображено")
    sys.exit(qt_app.exec())

if __name__ == "__main__":
    main()
