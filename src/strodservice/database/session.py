import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Путь к директории exe или скрипта
if getattr(sys, 'frozen', False):
    # Если запущено как exe через PyInstaller
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Путь к файлу базы
DB_PATH = os.path.join(BASE_DIR, "strodservice.db")

# Создаём папку, если её нет
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
