"""
Модуль инициализации базы данных для приложения KSK Shop.

Этот модуль отвечает за создание таблиц в базе данных.
"""

from .base import Base
from models.models import *  # импортируем все модели для регистрации


def init_db(engine):
    """
    Инициализация базы данных и создание таблиц.
    
    Args:
        engine: Объект SQLAlchemy engine для подключения к базе данных
    """
    Base.metadata.create_all(bind=engine)