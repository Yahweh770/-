from sqlalchemy import (
    Column, Integer, String, Float,
    ForeignKey, DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime

from kskapp.database.base import Base

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)

class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit = Column(String)
    norm = Column(Float)  # расход по ГОСТ

class LineType(Base):
    __tablename__ = 'line_types'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    width = Column(Float)
    material_id = Column(Integer, ForeignKey('materials.id'))

class Object(Base):
    __tablename__ = "objects"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    object_id = Column(Integer, ForeignKey('objects.id'))
    type = Column(String)  # ИД, Акт, Протокол
    path = Column(String)  # путь к файлу
    created_at = Column(DateTime)

class Contractor(Base):
    __tablename__ = 'contractors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    inn = Column(String)

class FieldData(Base):
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