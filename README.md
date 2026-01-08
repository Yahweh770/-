# Strod-Service Technology Application

Advanced construction service management system with integrated file storage and reporting capabilities.

## Features

- Comprehensive database management for construction projects
- Advanced file storage system with tagging and search capabilities
- Integrated reporting and document generation
- Modern GUI interface built with PyQt5
- Configurable settings and environment management
- Comprehensive error handling and logging

## Project Structure

```
/workspace/
├── src/
│   └── strodservice/           # Main application source code
│       ├── config/             # Configuration management
│       ├── database/           # Database models and operations
│       ├── desktop/            # GUI components
│       ├── filestorage/        # File storage system
│       ├── models/             # Data models
│       ├── services/           # Business logic services
│       ├── utils/              # Utility functions
│       └── main.py             # Application entry point
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── storage/                    # Default file storage directory
├── data/                       # Database files
├── docs/                       # Documentation
├── requirements.txt            # Dependencies
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with configuration variables:
   ```env
   DATABASE_URL=sqlite:///./data/strodservice.db
   STORAGE_PATH=./storage
   DEBUG=true
   LOG_LEVEL=INFO
   ```

## Running the Application

```bash
python -m src.strodservice.main
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_models.py

# Run with coverage
pytest --cov=src.strodservice
```

## Configuration

The application uses a settings management system with the following hierarchy:
1. Environment variables
2. `.env` file
3. Default values

Key configuration options:
- `DATABASE_URL`: Database connection string
- `STORAGE_PATH`: Directory for file storage
- `MAX_FILE_SIZE`: Maximum allowed file size in bytes
- `ALLOWED_FILE_EXTENSIONS`: Comma-separated list of allowed file extensions
- `DEBUG`: Enable/disable debug mode
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Development

To contribute to the project:
1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Run tests to ensure everything works
5. Submit a pull request

## License

MIT License