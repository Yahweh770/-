"""Integration tests for the database functionality."""
import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.strodservice.database.base import Base
from src.strodservice.models.models import Organization, Material, Object
from src.strodservice.database.session import get_db_session


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    # Create a temporary database file
    temp_db_fd, temp_db_path = tempfile.mkstemp(suffix='.db')
    
    # Create engine with temporary database
    engine = create_engine(f"sqlite:///{temp_db_path}")
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield SessionLocal
    
    # Cleanup
    os.close(temp_db_fd)
    os.unlink(temp_db_path)


def test_create_organization_with_session_context(temp_db):
    """Test creating an organization using the session context manager."""
    SessionLocal = temp_db
    
    # Test using context manager
    with get_db_session() as db:
        org = Organization(name="Test Organization", address="Test Address")
        db.add(org)
        # Commit happens automatically at the end of the context
    
    # Verify the organization was created
    with get_db_session() as db:
        retrieved_org = db.query(Organization).filter(Organization.name == "Test Organization").first()
        assert retrieved_org is not None
        assert retrieved_org.name == "Test Organization"
        assert retrieved_org.address == "Test Address"


def test_relationships_between_models(temp_db):
    """Test relationships between different models."""
    SessionLocal = temp_db
    
    # Create organization
    with get_db_session() as db:
        org = Organization(name="Test Org", address="Test Address")
        db.add(org)
        db.flush()  # Get ID without committing
        
        # Create related object
        obj = Object(name="Test Object", organization_id=org.id)
        db.add(obj)
        # Commit happens automatically
    
    # Verify relationships work
    with get_db_session() as db:
        retrieved_org = db.query(Organization).filter(Organization.name == "Test Org").first()
        assert retrieved_org is not None
        assert len(retrieved_org.objects) == 1
        assert retrieved_org.objects[0].name == "Test Object"


def test_cascade_deletion(temp_db):
    """Test that deleting an organization also deletes related objects."""
    SessionLocal = temp_db
    
    # Create organization with related object
    with get_db_session() as db:
        org = Organization(name="Test Org", address="Test Address")
        db.add(org)
        db.flush()
        
        obj = Object(name="Test Object", organization_id=org.id)
        db.add(obj)
        # Commit happens automatically
    
    # Delete the organization
    with get_db_session() as db:
        org_to_delete = db.query(Organization).filter(Organization.name == "Test Org").first()
        db.delete(org_to_delete)
        # Commit happens automatically
    
    # Verify both organization and related object are deleted
    with get_db_session() as db:
        org_count = db.query(Organization).filter(Organization.name == "Test Org").count()
        obj_count = db.query(Object).filter(Object.name == "Test Object").count()
        
        assert org_count == 0
        assert obj_count == 0