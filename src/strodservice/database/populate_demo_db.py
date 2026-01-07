# strodservice/database/populate_demo_db.py
import sys
from pathlib import Path
from datetime import datetime

# --- Установка корня проекта в sys.path ---
BASE_DIR = Path(__file__).resolve().parent.parent  # один уровень вверх от database
sys.path.insert(0, str(BASE_DIR))

from sqlalchemy.orm import sessionmaker
from strodservice.database.session import engine, SessionLocal
from strodservice.models.models import (
    Object, Material, Organization, LineType, Contractor, Document, FieldData, Base
)

# --- Создание таблиц ---
Base.metadata.create_all(bind=engine)

# --- Создание сессии ---
session = SessionLocal()

# --- Объекты (например, участки дороги) ---
obj1 = Object(name="Main Street Section 1", location="North Zone")
obj2 = Object(name="Highway Entrance", location="South Zone")
obj3 = Object(name="City Center Crossroad", location="Center Zone")
session.add_all([obj1, obj2, obj3])

# --- Материалы (краска, бетон, асфальт и т.п.) ---
mat1 = Material(name="Road Paint White", unit="liter", norm=0.5)
mat2 = Material(name="Road Paint Yellow", unit="liter", norm=0.6)
mat3 = Material(name="Asphalt Mix", unit="ton", norm=2.0)
session.add_all([mat1, mat2, mat3])

# --- Организации ---
org1 = Organization(name="RoadWorks Ltd", address="123 Industrial St")
org2 = Organization(name="City Infrastructure Corp", address="456 Urban Ave")
session.add_all([org1, org2])

# --- Типы линий (разметка) ---
lt1 = LineType(name="Solid White Line", width=0.15, material_id=mat1.id)
lt2 = LineType(name="Dashed Yellow Line", width=0.15, material_id=mat2.id)
lt3 = LineType(name="Pedestrian Crossing", width=3.0, material_id=mat3.id)
session.add_all([lt1, lt2, lt3])

# --- Подрядчики ---
cont1 = Contractor(name="Alpha Builders", inn="1234567890")
cont2 = Contractor(name="Beta Contractors", inn="0987654321")
session.add_all([cont1, cont2])

# --- Документы ---
doc1 = Document(object_id=obj1.id, type="Blueprint", path="docs/main_street_blueprint.pdf", created_at=datetime.now())
doc2 = Document(object_id=obj2.id, type="Act", path="docs/highway_entrance_act.pdf", created_at=datetime.now())
doc3 = Document(object_id=obj3.id, type="Report", path="docs/city_crossroad_report.pdf", created_at=datetime.now())
session.add_all([doc1, doc2, doc3])

# --- Данные полей (фактическая разметка/использование материалов) ---
fd1 = FieldData(
    object_id=obj1.id, line_type_id=lt1.id, length=500, width=0.15,
    material_used=25, photo_path="photos/main_street_section1.jpg",
    date=datetime.now(), notes="Solid line freshly painted"
)
fd2 = FieldData(
    object_id=obj2.id, line_type_id=lt2.id, length=300, width=0.15,
    material_used=18, photo_path="photos/highway_entrance.jpg",
    date=datetime.now(), notes="Dashed yellow line installed"
)
fd3 = FieldData(
    object_id=obj3.id, line_type_id=lt3.id, length=10, width=3.0,
    material_used=20, photo_path="photos/city_crossroad.jpg",
    date=datetime.now(), notes="Pedestrian crossing marked with asphalt"
)
session.add_all([fd1, fd2, fd3])

# --- Сохраняем всё ---
session.commit()
session.close()

print("✅ Demo база данных для дорожной разметки успешно заполнена!")
