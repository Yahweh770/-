import sys
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

from ..config.settings import settings


def setup_logger(
    name: str = "strodservice",
    log_file: Optional[Path] = None,
    level: int = None
) -> logging.Logger:
    """
    Настройка ротационного логгера с поддержкой путей проекта
    
    Args:
        name: Имя логгера (по умолчанию 'strodservice')
        log_file: Путь к файлу лога (по умолчанию BASE_DIR/logs/app.log)
        level: Уровень логирования (берется из настроек по умолчанию)
    
    Returns:
        logging.Logger: настроенный логгер
    """
    # Use configured log level if not provided
    if level is None:
        level = getattr(logging, settings.LOG_LEVEL)
    
    # Use configured log directory
    logs_dir = Path(settings.LOG_FILE).parent if log_file is None else Path(log_file).parent
    logs_dir.mkdir(exist_ok=True)
    
    # Use configured log file if not provided
    default_log_file = logs_dir / settings.LOG_FILE if log_file is None else log_file
    log_file = log_file or default_log_file
    
    # Formatter with more detailed information
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s'
    )
    
    # Rotational handler with configured max size
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=settings.LOG_MAX_SIZE, 
        backupCount=3,
        encoding='utf-8'
    )
    handler.setFormatter(formatter)
    handler.setLevel(level)
    
    # Create/get logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove old handlers (avoid duplication)
    logger.handlers.clear()
    logger.addHandler(handler)
    
    # Console handler for development (conditionally based on debug mode)
    if settings.DEBUG:
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s'
        )
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG if level == logging.DEBUG else logging.INFO)
        logger.addHandler(console_handler)
    
    return logger