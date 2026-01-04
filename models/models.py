"""
Модели базы данных для приложения KSK Shop.

Этот модуль содержит все SQLAlchemy модели для приложения.
"""

from sqlalchemy import (
    Column, Integer, String, Float,
    ForeignKey, DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime

from database.base import Base


class Organization(Base):
    """
    Модель организации.
    
    Attributes:
        id (int): Уникальный идентификатор
        name (str): Название организации
        address (str): Адрес организации
    """
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)


class Material(Base):
    """
    Модель материала.
    
    Attributes:
        id (int): Уникальный идентификатор
        name (str): Название материала
        unit (str): Единица измерения
        norm (float): Норма расхода по ГОСТ
    """
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit = Column(String)
    norm = Column(Float)  # расход по ГОСТ


class LineType(Base):
    """
    Модель типа линии.
    
    Attributes:
        id (int): Уникальный идентификатор
        name (str): Название типа линии
        width (float): Ширина
        material_id (int): Ссылка на материал
    """
    __tablename__ = 'line_types'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    width = Column(Float)
    material_id = Column(Integer, ForeignKey('materials.id'))


class Object(Base):
    """
    Модель объекта.
    
    Attributes:
        id (int): Уникальный идентификатор
        name (str): Название объекта
        location (str): Местоположение объекта
    """
    __tablename__ = "objects"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)


class Document(Base):
    """
    Модель документа.
    
    Attributes:
        id (int): Уникальный идентификатор
        object_id (int): Ссылка на объект
        type (str): Тип документа (ИД, Акт, Протокол)
        path (str): Путь к файлу
        created_at (datetime): Дата создания
    """
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    object_id = Column(Integer, ForeignKey('objects.id'))
    type = Column(String)  # ИД, Акт, Протокол
    path = Column(String)  # путь к файлу
    created_at = Column(DateTime)


class Contractor(Base):
    """
    Модель подрядчика.
    
    Attributes:
        id (int): Уникальный идентификатор
        name (str): Название подрядчика
        inn (str): ИНН подрядчика
    """
    __tablename__ = 'contractors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    inn = Column(String)


class FieldData(Base):
    """
    Модель полевых данных.
    
    Attributes:
        id (int): Уникальный идентификатор
        object_id (int): Ссылка на объект
        line_type_id (int): Ссылка на тип линии
        length (float): Длина в метрах
        width (float): Ширина в метрах
        material_used (float): Количество использованного материала
        photo_path (str): Путь к фотоотчёту
        date (datetime): Дата
        notes (str): Заметки
    """
    __tablename__ = 'field_data'
    id = Column(Integer, primary_key=True)
    object_id = Column(Integer, ForeignKey('objects.id'))
    line_type_id = Column(Integer, ForeignKey('line_types.id'))
    length = Column(Float)  # в метрах
    width = Column(Float)   # в метрах
    material_used = Column(Float)  # использовано материала
    photo_path = Column(String)    # путь к фотоотчёту
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String)         # заметки