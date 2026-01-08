# API Documentation for Strod-Service Technology Application

## Overview

This document describes the APIs and interfaces available in the Strod-Service Technology application.

## Configuration API

### Settings Management

The application uses a centralized settings management system located at `src/strodservice/config/settings.py`.

#### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./ksk.db` |
| `DATABASE_POOL_SIZE` | Size of the database connection pool | `5` |
| `DATABASE_POOL_TIMEOUT` | Timeout for database connections | `30` |
| `APP_NAME` | Name of the application | `Strod-Service Technology` |
| `APP_VERSION` | Version of the application | `1.0.0` |
| `DEBUG` | Enable debug mode | `False` |
| `STORAGE_PATH` | Path for file storage | `./storage` |
| `MAX_FILE_SIZE` | Maximum file size in bytes | `52428800` (50MB) |
| `ALLOWED_FILE_EXTENSIONS` | Comma-separated list of allowed extensions | `pdf,doc,docx,xls,xlsx,txt,jpg,jpeg,png` |
| `SECRET_KEY` | Secret key for security features | `dev-secret-key-change-in-production` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_FILE` | Path to log file | `app.log` |
| `LOG_MAX_SIZE` | Maximum log file size in bytes | `10485760` (10MB) |
| `API_BASE_URL` | Base URL for API calls | `http://localhost:8000` |
| `API_TIMEOUT` | Timeout for API calls | `30` |
| `ENVIRONMENT` | Application environment | `development` |

## Database Models API

### Organization Model

Represents an organization in the system.

#### Fields
- `id` (Integer, Primary Key, Auto-increment)
- `name` (String(255), Required) - Organization name
- `address` (String(500), Optional) - Organization address
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

#### Methods
- `__init__(name, address=None)` - Constructor with validation
- `_validate()` - Validation method

### Material Model

Represents a material used in construction projects.

#### Fields
- `id` (Integer, Primary Key, Auto-increment)
- `name` (String(255), Required) - Material name
- `unit` (String(50), Required) - Unit of measurement
- `norm` (Float, Optional) - Standard consumption rate
- `description` (Text, Optional) - Material description
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

### LineType Model

Represents a type of line in construction projects.

#### Fields
- `id` (Integer, Primary Key, Auto-increment)
- `name` (String(255), Required) - Line type name
- `width` (Float, Required) - Width of the line
- `material_id` (Integer, Foreign Key, Required) - Reference to material
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

### Object Model

Represents a construction object.

#### Fields
- `id` (Integer, Primary Key, Auto-increment)
- `name` (String(255), Required) - Object name
- `location` (String(500), Optional) - Object location
- `organization_id` (Integer, Foreign Key, Optional) - Reference to organization
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

### Document Model

Represents a document associated with an object.

#### Fields
- `id` (Integer, Primary Key, Auto-increment)
- `object_id` (Integer, Foreign Key, Required) - Reference to object
- `type` (String(100), Required) - Document type (e.g., ИД, Акт, Протокол)
- `path` (String(500), Required) - Path to the document file
- `title` (String(255), Optional) - Document title
- `description` (Text, Optional) - Document description
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

### Contractor Model

Represents a contractor involved in projects.

#### Fields
- `id` (Integer, Primary Key, Auto-increment)
- `name` (String(255), Required) - Contractor name
- `inn` (String(50), Optional) - Tax identification number
- `address` (String(500), Optional) - Contractor address
- `phone` (String(50), Optional) - Contact phone
- `email` (String(255), Optional) - Email address
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

### FieldData Model

Represents field data collected during construction.

#### Fields
- `id` (Integer, Primary Key, Auto-increment)
- `object_id` (Integer, Foreign Key, Required) - Reference to object
- `line_type_id` (Integer, Foreign Key, Required) - Reference to line type
- `length` (Float, Optional) - Length measurement
- `width` (Float, Optional) - Width measurement
- `material_used` (Float, Optional) - Amount of material used
- `photo_path` (String(500), Optional) - Path to photo report
- `date` (DateTime) - Date of data collection
- `notes` (Text, Optional) - Additional notes
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

## File Storage API

The file storage system is located at `src/strodservice/filestorage/file_storage.py`.

### FileStorage Class

#### Constructor
`FileStorage(storage_path=None, index_file="file_index.json")`
- `storage_path` (str, optional): Path for file storage. Uses configured path if None.
- `index_file` (str): Name of the index file.

#### Methods

##### `store_file(source_path, filename=None, tags=None)`
Store a file in the storage system with validation.
- `source_path` (str): Path to the source file
- `filename` (str, optional): Desired filename in storage
- `tags` (list[str], optional): Tags to associate with the file
- Returns: Path to the stored file
- Raises: `FileValidationError`, `FileStorageError`

##### `search_files(query=None, tags=None, extension=None)`
Search for files in the storage system.
- `query` (str, optional): Text query to search in filenames
- `tags` (list[str], optional): Tags to filter by
- `extension` (str, optional): File extension to filter by
- Returns: List of matching file information dictionaries

##### `get_file_path(filename)`
Get the path to a stored file by its name.
- `filename` (str): Name of the file to retrieve
- Returns: Path to the file or None if not found

##### `load_file_content(filename)`
Load the content of a stored file with security checks.
- `filename` (str): Name of the file to load
- Returns: File content as bytes
- Raises: `FileNotFoundError`, `FileStorageError`

##### `list_all_files()`
List all files in the storage.
- Returns: List of all file information dictionaries

##### `delete_file(filename)`
Delete a file from storage with security checks.
- `filename` (str): Name of the file to delete
- Returns: True if deletion was successful, False otherwise

##### `add_tags(filename, tags)`
Add tags to a file.
- `filename` (str): Name of the file
- `tags` (list[str]): Tags to add
- Returns: True if successful, False otherwise

##### `get_all_tags()`
Get all unique tags in the storage.
- Returns: List of all unique tags

## Exception Classes

The application defines several custom exception classes in `src/strodservice/exceptions.py`:

- `BaseStrodServiceException` - Base exception class
- `DatabaseError` - Database operation failures
- `ValidationError` - Input validation failures
- `FileStorageError` - File storage operation failures
- `AuthenticationError` - Authentication failures
- `AuthorizationError` - Authorization failures
- `ConfigurationError` - Invalid configuration
- `FileValidationError` - File validation failures
- `ModelValidationError` - Model validation failures
- `APIError` - API operation failures
- `IntegrationError` - External integration failures

## Session Management

Database sessions are managed using a context manager pattern in `src/strodservice/database/session.py`.

### `get_db_session()`
Context manager for database sessions with automatic commit/rollback.
- Usage: `with get_db_session() as session:`

## Logging API

The logging system is configured in `src/strodservice/utils/logger.py`.

### `setup_logger(name, log_file, level)`
Setup a configured logger instance.
- `name` (str): Name of the logger
- `log_file` (Path, optional): Path to log file
- `level` (int, optional): Logging level
- Returns: Configured logger instance