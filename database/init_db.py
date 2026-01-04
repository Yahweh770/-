# kskapp/database/init_db.py
from kskapp.database import Base, engine

# ОБЯЗАТЕЛЬНО импортируем все модели, чтобы SQLAlchemy их "увидел"
import kskapp.models.models

def init_db():
    print("🔧 Инициализация базы данных...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы:", Base.metadata.tables.keys())

if __name__ == "__main__":
    init_db()
