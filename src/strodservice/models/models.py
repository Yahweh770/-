from sqlalchemy import (
    Column, Integer, String, Float,
    ForeignKey, DateTime, Text
)
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import event

from ..database.base import Base
from ..exceptions import ModelValidationError


class AuditMixin:
    """Mixin class to add audit fields to all models."""
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Organization(Base, AuditMixin):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=True)
    
    # Relationship
    objects = relationship("Object", back_populates="organization", cascade="all, delete-orphan")
    
    def __init__(self, name, address=None):
        super().__init__()
        self.name = name
        self.address = address
        self._validate()
    
    def _validate(self):
        if not self.name or len(self.name.strip()) == 0:
            raise ModelValidationError("Organization name cannot be empty")
        if len(self.name) > 255:
            raise ModelValidationError("Organization name cannot exceed 255 characters")


class Material(Base, AuditMixin):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    unit = Column(String(50), nullable=False)
    norm = Column(Float)  # расход по ГОСТ
    description = Column(Text, nullable=True)
    
    # Relationship
    line_types = relationship("LineType", back_populates="material")
    
    def __init__(self, name, unit, norm=None, description=None):
        super().__init__()
        self.name = name
        self.unit = unit
        self.norm = norm
        self.description = description
        self._validate()
    
    def _validate(self):
        if not self.name or len(self.name.strip()) == 0:
            raise ModelValidationError("Material name cannot be empty")
        if len(self.name) > 255:
            raise ModelValidationError("Material name cannot exceed 255 characters")
        if not self.unit or len(self.unit.strip()) == 0:
            raise ModelValidationError("Material unit cannot be empty")
        if len(self.unit) > 50:
            raise ModelValidationError("Material unit cannot exceed 50 characters")
        if self.norm is not None and self.norm < 0:
            raise ModelValidationError("Material norm cannot be negative")


class LineType(Base, AuditMixin):
    __tablename__ = 'line_types'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    width = Column(Float, nullable=False)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    
    # Relationships
    material = relationship("Material", back_populates="line_types")
    field_data = relationship("FieldData", back_populates="line_type")
    
    def __init__(self, name, width, material_id):
        super().__init__()
        self.name = name
        self.width = width
        self.material_id = material_id
        self._validate()
    
    def _validate(self):
        if not self.name or len(self.name.strip()) == 0:
            raise ModelValidationError("Line type name cannot be empty")
        if len(self.name) > 255:
            raise ModelValidationError("Line type name cannot exceed 255 characters")
        if self.width is not None and self.width <= 0:
            raise ModelValidationError("Line type width must be positive")


class Object(Base, AuditMixin):
    __tablename__ = "objects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(500), nullable=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="objects")
    documents = relationship("Document", back_populates="object", cascade="all, delete-orphan")
    field_data = relationship("FieldData", back_populates="object")
    
    def __init__(self, name, location=None, organization_id=None):
        super().__init__()
        self.name = name
        self.location = location
        self.organization_id = organization_id
        self._validate()
    
    def _validate(self):
        if not self.name or len(self.name.strip()) == 0:
            raise ModelValidationError("Object name cannot be empty")
        if len(self.name) > 255:
            raise ModelValidationError("Object name cannot exceed 255 characters")


class Document(Base, AuditMixin):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    object_id = Column(Integer, ForeignKey('objects.id'), nullable=False)
    type = Column(String(100), nullable=False)  # ИД, Акт, Протокол
    path = Column(String(500), nullable=False)  # путь к файлу
    title = Column(String(255), nullable=True)  # документ title
    description = Column(Text, nullable=True)
    
    # Relationships
    object = relationship("Object", back_populates="documents")
    
    def __init__(self, object_id, type, path, title=None, description=None):
        super().__init__()
        self.object_id = object_id
        self.type = type
        self.path = path
        self.title = title
        self.description = description
        self._validate()
    
    def _validate(self):
        if self.type and len(self.type) > 100:
            raise ModelValidationError("Document type cannot exceed 100 characters")
        if not self.path or len(self.path.strip()) == 0:
            raise ModelValidationError("Document path cannot be empty")
        if len(self.path) > 500:
            raise ModelValidationError("Document path cannot exceed 500 characters")
        if self.title and len(self.title) > 255:
            raise ModelValidationError("Document title cannot exceed 255 characters")


class Contractor(Base, AuditMixin):
    __tablename__ = 'contractors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    inn = Column(String(50), nullable=True)  # ИНН
    address = Column(String(500), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    
    def __init__(self, name, inn=None, address=None, phone=None, email=None):
        super().__init__()
        self.name = name
        self.inn = inn
        self.address = address
        self.phone = phone
        self.email = email
        self._validate()
    
    def _validate(self):
        if not self.name or len(self.name.strip()) == 0:
            raise ModelValidationError("Contractor name cannot be empty")
        if len(self.name) > 255:
            raise ModelValidationError("Contractor name cannot exceed 255 characters")
        if self.inn and len(self.inn) > 50:
            raise ModelValidationError("Contractor INN cannot exceed 50 characters")
        if self.phone and len(self.phone) > 50:
            raise ModelValidationError("Contractor phone cannot exceed 50 characters")
        if self.email and len(self.email) > 255:
            raise ModelValidationError("Contractor email cannot exceed 255 characters")


class FieldData(Base, AuditMixin):
    __tablename__ = 'field_data'
    id = Column(Integer, primary_key=True, index=True)
    object_id = Column(Integer, ForeignKey('objects.id'), nullable=False)
    line_type_id = Column(Integer, ForeignKey('line_types.id'), nullable=False)
    length = Column(Float)  # в метрах
    width = Column(Float)   # в метрах
    material_used = Column(Float)  # использовано материала
    photo_path = Column(String(500))    # путь к фотоотчёту
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)         # заметки
    
    # Relationships
    object = relationship("Object", back_populates="field_data")
    line_type = relationship("LineType", back_populates="field_data")
    
    def __init__(self, object_id, line_type_id, length=None, width=None, material_used=None, 
                 photo_path=None, notes=None):
        super().__init__()
        self.object_id = object_id
        self.line_type_id = line_type_id
        self.length = length
        self.width = width
        self.material_used = material_used
        self.photo_path = photo_path
        self.notes = notes
        self._validate()
    
    def _validate(self):
        if self.length is not None and self.length <= 0:
            raise ModelValidationError("Field data length must be positive")
        if self.width is not None and self.width <= 0:
            raise ModelValidationError("Field data width must be positive")
        if self.material_used is not None and self.material_used < 0:
            raise ModelValidationError("Field data material used cannot be negative")
        if self.photo_path and len(self.photo_path) > 500:
            raise ModelValidationError("Photo path cannot exceed 500 characters")


# Update the relationships after all classes are defined
Material.line_types = relationship("LineType", back_populates="material")
Object.documents = relationship("Document", back_populates="object", cascade="all, delete-orphan")
Object.field_data = relationship("FieldData", back_populates="object")
Document.object = relationship("Object", back_populates="documents")
FieldData.object = relationship("Object", back_populates="field_data")
FieldData.line_type = relationship("LineType", back_populates="field_data")
LineType.field_data = relationship("FieldData", back_populates="line_type")
Organization.objects = relationship("Object", back_populates="organization", cascade="all, delete-orphan")