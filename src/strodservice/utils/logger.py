import sys
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

# Определяем корень проекта на основе расположения этого файла
BASE_DIR = Path(__file__).resolve().parents[3]  # utils → strodservice → src → корень

def setup_logger(
    name: str = "strodservice",
    log_file: Optional[Path] = None,
    level: int = logging.INFO
) -> logging.Logger:
    """
    Настройка ротационного логгера с поддержкой путей проекта
    
    Args:
        name: Имя логгера (по умолчанию 'strodservice')
        log_file: Путь к файлу лога (по умолчанию BASE_DIR/logs/app.log)
        level: Уровень логирования (INFO по умолчанию)
    
    Returns:
        logging.Logger: настроенный логгер
    """
    # Создаём папку logs в корне проекта
    logs_dir = BASE_DIR / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Путь к основному лог-файлу
    default_log_file = logs_dir / "app.log"
    log_file = log_file or default_log_file
    
    # Форматтер
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )
    
    # Ротационный обработчик (5MB x 3 файла)
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024, 
        backupCount=3,
        encoding='utf-8'
    )
    handler.setFormatter(formatter)
    handler.setLevel(level)
    
    # Создаём/получаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Удаляем старые обработчики (избегаем дублирования)
    logger.handlers.clear()
    logger.addHandler(handler)
    
    # Консольный обработчик для разработки (опционально)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if level == logging.DEBUG else logging.INFO)
    logger.addHandler(console_handler)
    
    return logger