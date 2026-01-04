# kskapp/database/__init__.py

from .session import engine, SessionLocal
from ..models.models import Base  # вместо from kskapp.models.models import Base

__all__ = ["engine", "SessionLocal", "Base"]
