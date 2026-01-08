"""Unit tests for the database models."""
import pytest
from datetime import datetime
from unittest.mock import Mock, patch

from src.strodservice.models.models import (
    Organization, Material, LineType, Object, Document, Contractor, FieldData
)
from src.strodservice.exceptions import ModelValidationError


class TestOrganizationModel:
    """Test cases for the Organization model."""
    
    def test_organization_creation_valid(self):
        """Test creating an organization with valid data."""
        org = Organization(name="Test Organization", address="Test Address")
        
        assert org.name == "Test Organization"
        assert org.address == "Test Address"
        assert org.created_at is not None
        assert org.updated_at is not None
    
    def test_organization_creation_invalid_empty_name(self):
        """Test creating an organization with empty name raises validation error."""
        with pytest.raises(ModelValidationError, match="Organization name cannot be empty"):
            Organization(name="")
    
    def test_organization_creation_invalid_long_name(self):
        """Test creating an organization with too long name raises validation error."""
        with pytest.raises(ModelValidationError, match="Organization name cannot exceed 255 characters"):
            Organization(name="A" * 256)


class TestMaterialModel:
    """Test cases for the Material model."""
    
    def test_material_creation_valid(self):
        """Test creating a material with valid data."""
        material = Material(name="Test Material", unit="kg", norm=10.5)
        
        assert material.name == "Test Material"
        assert material.unit == "kg"
        assert material.norm == 10.5
        assert material.created_at is not None
    
    def test_material_creation_invalid_empty_name(self):
        """Test creating a material with empty name raises validation error."""
        with pytest.raises(ModelValidationError, match="Material name cannot be empty"):
            Material(name="", unit="kg")
    
    def test_material_creation_invalid_negative_norm(self):
        """Test creating a material with negative norm raises validation error."""
        with pytest.raises(ModelValidationError, match="Material norm cannot be negative"):
            Material(name="Test Material", unit="kg", norm=-5.0)


class TestLineTypeModel:
    """Test cases for the LineType model."""
    
    def test_line_type_creation_valid(self):
        """Test creating a line type with valid data."""
        line_type = LineType(name="Test Line Type", width=1.5, material_id=1)
        
        assert line_type.name == "Test Line Type"
        assert line_type.width == 1.5
        assert line_type.material_id == 1
        assert line_type.created_at is not None
    
    def test_line_type_creation_invalid_zero_width(self):
        """Test creating a line type with zero width raises validation error."""
        with pytest.raises(ModelValidationError, match="Line type width must be positive"):
            LineType(name="Test Line Type", width=0, material_id=1)


class TestObjectModel:
    """Test cases for the Object model."""
    
    def test_object_creation_valid(self):
        """Test creating an object with valid data."""
        obj = Object(name="Test Object", location="Test Location", organization_id=1)
        
        assert obj.name == "Test Object"
        assert obj.location == "Test Location"
        assert obj.organization_id == 1
        assert obj.created_at is not None
    
    def test_object_creation_invalid_empty_name(self):
        """Test creating an object with empty name raises validation error."""
        with pytest.raises(ModelValidationError, match="Object name cannot be empty"):
            Object(name="")


class TestDocumentModel:
    """Test cases for the Document model."""
    
    def test_document_creation_valid(self):
        """Test creating a document with valid data."""
        doc = Document(object_id=1, type="Акт", path="/path/to/doc.pdf", title="Test Document")
        
        assert doc.object_id == 1
        assert doc.type == "Акт"
        assert doc.path == "/path/to/doc.pdf"
        assert doc.title == "Test Document"
        assert doc.created_at is not None
    
    def test_document_creation_invalid_empty_path(self):
        """Test creating a document with empty path raises validation error."""
        with pytest.raises(ModelValidationError, match="Document path cannot be empty"):
            Document(object_id=1, type="Акт", path="")


class TestContractorModel:
    """Test cases for the Contractor model."""
    
    def test_contractor_creation_valid(self):
        """Test creating a contractor with valid data."""
        contractor = Contractor(name="Test Contractor", inn="123456789", phone="+1234567890")
        
        assert contractor.name == "Test Contractor"
        assert contractor.inn == "123456789"
        assert contractor.phone == "+1234567890"
        assert contractor.created_at is not None
    
    def test_contractor_creation_invalid_empty_name(self):
        """Test creating a contractor with empty name raises validation error."""
        with pytest.raises(ModelValidationError, match="Contractor name cannot be empty"):
            Contractor(name="")


class TestFieldDataModel:
    """Test cases for the FieldData model."""
    
    def test_field_data_creation_valid(self):
        """Test creating field data with valid data."""
        field_data = FieldData(
            object_id=1,
            line_type_id=1,
            length=10.5,
            width=2.0,
            material_used=5.5,
            photo_path="/path/to/photo.jpg",
            notes="Test notes"
        )
        
        assert field_data.object_id == 1
        assert field_data.line_type_id == 1
        assert field_data.length == 10.5
        assert field_data.width == 2.0
        assert field_data.material_used == 5.5
        assert field_data.photo_path == "/path/to/photo.jpg"
        assert field_data.notes == "Test notes"
        assert field_data.created_at is not None
    
    def test_field_data_creation_invalid_negative_length(self):
        """Test creating field data with negative length raises validation error."""
        with pytest.raises(ModelValidationError, match="Field data length must be positive"):
            FieldData(object_id=1, line_type_id=1, length=-5.0)
    
    def test_field_data_creation_invalid_negative_material_used(self):
        """Test creating field data with negative material used raises validation error."""
        with pytest.raises(ModelValidationError, match="Field data material used cannot be negative"):
            FieldData(object_id=1, line_type_id=1, length=10.0, material_used=-2.0)