"""
Базовый модуль для SQLAlchemy.

Этот модуль содержит базовый класс для всех моделей SQLAlchemy.
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()