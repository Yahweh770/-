"""
Модуль инициализации базы данных для приложения Strod-Service Technology.

Этот модуль отвечает за создание таблиц в базе данных.
"""

from .base import Base
from ..models.models import *  # импортируем все модели для регистрации
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path

# Глобальные переменные для подключения к базе данных
engine = None
SessionLocal = None


def init_db(db_path=None):
    """Инициализация базы данных и создание таблиц."""
    global engine, SessionLocal
    print("🔧 Инициализация базы данных...")
    # Если путь к базе данных не передан, используем путь по умолчанию
    if db_path is None:
        # Импортируем путь к данным из main, если возможно
        try:
            from ..main import DATA_DIR
            db_path = DATA_DIR / "ksk.db"
        except ImportError:
            # Если не удается импортировать, используем относительный путь
            db_path = Path.cwd() / "data" / "ksk.db"
    
    # Создаем директорию, если она не существует
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы:", list(Base.metadata.tables.keys()))
    return engine


if __name__ == "__main__":
    init_db()
