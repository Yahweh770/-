"""Custom exception classes for the application."""
from typing import Optional


class BaseStrodServiceException(Exception):
    """Base exception class for Strod-Service application."""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class DatabaseError(BaseStrodServiceException):
    """Raised when database operations fail."""
    pass


class ValidationError(BaseStrodServiceException):
    """Raised when input validation fails."""
    pass


class FileStorageError(BaseStrodServiceException):
    """Raised when file storage operations fail."""
    pass


class AuthenticationError(BaseStrodServiceException):
    """Raised when authentication fails."""
    pass


class AuthorizationError(BaseStrodServiceException):
    """Raised when authorization fails."""
    pass


class ConfigurationError(BaseStrodServiceException):
    """Raised when configuration is invalid."""
    pass


class FileValidationError(ValidationError):
    """Raised when file validation fails."""
    pass


class ModelValidationError(ValidationError):
    """Raised when model validation fails."""
    pass


class APIError(BaseStrodServiceException):
    """Raised when API operations fail."""
    pass


class IntegrationError(BaseStrodServiceException):
    """Raised when external integrations fail."""
    pass