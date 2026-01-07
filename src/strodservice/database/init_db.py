"""
Модуль инициализации базы данных для приложения KSK Shop.

Этот модуль отвечает за создание таблиц в базе данных.
"""

from .base import Base
from ..models.models import *  # импортируем все модели для регистрации
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def init_db(engine):
    """
    Инициализация базы данных и создание таблиц.
    
    Args:
        engine: Объект SQLAlchemy engine для подключения к базе данных
    """
    Base.metadata.create_all(bind=engine)


# Глобальный объект SessionLocal для импорта в других модулях
SessionLocal = sessionmaker(autoflush=False, autocommit=False)
# Импорты для инициализации
from . import Base, engine

# ОБЯЗАТЕЛЬНО импортируем все модели, чтобы SQLAlchemy их "увидел"
from ..models import models

def init_db():
    print("🔧 Инициализация базы данных...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы:", Base.metadata.tables.keys())

if __name__ == "__main__":
    init_db()
