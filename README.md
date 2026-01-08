# Strod-Service Technology Application

Advanced construction service management system with integrated file storage and reporting capabilities.

## Установщики

В дополнение к основному приложению, в репозитории представлены два варианта установщика:

- **`installer_demo.py`** - графический установщик с интерфейсом на tkinter
- **`console_installer.py`** - консольный установщик для терминальных систем
- **`INSTALLER_README.md`** - подробная документация по установщикам
- **`INSTALLERS_OVERVIEW.md`** - сводный обзор всех установщиков и их возможностей
- **`run_installers.sh`** - скрипт для удобного запуска установщиков
- **`test_installers.py`** - скрипт для проверки работоспособности установщиков
- **`setup_installers.py`** - файл для установки установщиков как Python-пакета
- **`INSTALLER_COMPARISON.md`** - сравнение демонстрационных и настоящих установщиков
- **`USAGE_GUIDE.md`** - руководство по использованию установщиков
- **`nsis_example.nsi`** - пример скрипта для NSIS

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