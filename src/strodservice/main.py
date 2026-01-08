import sys
import traceback
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
    BASE_DIR = Path(__file__).resolve().parent.parent.parent  # /workspace
    MEIPASS_DIR = BASE_DIR

# При использовании proper package structure, sys.path добавление не требуется
# когда запускаем как python -m src.strodservice.main

# Функция для получения пути к ресурсам (иконки, база, файлы)
def resource_path(relative_path):
    return MEIPASS_DIR / relative_path

# Пути к папкам данных и логов
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# --- Импорты внешних библиотек ---
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Импорт собственных модулей ---
from .utils.logger import setup_logger
from .database.init_db import init_db
from .desktop.main_window import MainWindow  # ← исправлено на абсолютный импорт
from PyQt5.QtWidgets import QApplication
from .config.settings import settings
from .exceptions import BaseStrodServiceException

# --- Engine базы данных ---
DB_FILE = DATA_DIR / "ksk.db"
from .database.init_db import engine, SessionLocal

def main():
    """Main entry point for the application."""
    try:
        logger = setup_logger(name="strodservice-main", level=getattr(logging, settings.LOG_LEVEL))
        logger.info("🚀 Запуск Strod-Service Technology приложения")
        
        # Log important configuration values (without sensitive data)
        logger.info(f"App Version: {settings.APP_VERSION}")
        logger.info(f"Environment: {settings.ENVIRONMENT}")
        logger.info(f"Debug Mode: {settings.DEBUG}")
        
        # Инициализация базы данных
        init_db()
        logger.info("✅ База данных инициализирована")
        
        # Создание и запуск Qt приложения
        qt_app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        logger.info("Главное окно отображено")
        
        # Run the application and handle exit codes
        exit_code = qt_app.exec_()
        logger.info(f"Приложение завершено с кодом выхода: {exit_code}")
        return exit_code
        
    except BaseStrodServiceException as e:
        # Handle known application exceptions
        error_msg = f"Ошибка приложения: {e.message}"
        print(error_msg, file=sys.stderr)
        logging.error(error_msg)
        return 1
    except KeyboardInterrupt:
        print("\nПриложение прервано пользователем", file=sys.stderr)
        logging.info("Приложение прервано пользователем")
        return 0
    except Exception as e:
        # Handle unexpected errors
        error_msg = f"Неожиданная ошибка: {str(e)}"
        print(error_msg, file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        logging.error(error_msg, exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
