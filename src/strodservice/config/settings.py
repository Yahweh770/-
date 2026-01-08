"""Application settings and configuration management."""
import os
from typing import Optional, Set
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_allowed_extensions() -> Set[str]:
    """Helper function to get allowed file extensions."""
    return set(
        os.getenv("ALLOWED_FILE_EXTENSIONS", "pdf,doc,docx,xls,xlsx,txt,jpg,jpeg,png").split(",")
    )


@dataclass
class Settings:
    """Application settings class."""
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ksk.db")
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    DATABASE_POOL_TIMEOUT: int = int(os.getenv("DATABASE_POOL_TIMEOUT", "30"))
    
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "Strod-Service Technology")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # File storage settings
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "./storage")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", str(50 * 1024 * 1024)))  # 50MB default
    ALLOWED_FILE_EXTENSIONS: Set[str] = field(default_factory=get_allowed_extensions)
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    PASSWORD_HASH_ALGORITHM: str = os.getenv("PASSWORD_HASH_ALGORITHM", "sha256")
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "app.log")
    LOG_MAX_SIZE: int = int(os.getenv("LOG_MAX_SIZE", str(10 * 1024 * 1024)))  # 10MB default
    
    # API settings
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    
    # Environment settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development").lower()
    
    def __post_init__(self):
        """Validate settings after initialization."""
        if self.ENVIRONMENT not in ["development", "production", "testing"]:
            raise ValueError(f"Invalid environment: {self.ENVIRONMENT}")
        
        if not os.path.exists(self.STORAGE_PATH):
            os.makedirs(self.STORAGE_PATH, exist_ok=True)

# Create a single instance of settings
settings = Settings()