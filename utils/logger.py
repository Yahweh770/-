"""
Модуль настройки логирования для приложения KSK Shop.

Этот модуль предоставляет функцию для настройки логгера с выводом в файл и консоль.
"""

import logging
from pathlib import Path
import sys


def setup_logger(name: str, level=logging.INFO, logs_dir=None):
    """
    Настройка логгера с выводом в файл и консоль.
    
    Args:
        name (str): Имя логгера
        level: Уровень логирования (по умолчанию logging.INFO)
        logs_dir: Директория для файлов логов (по умолчанию None)
    
    Returns:
        logging.Logger: Настроенный объект логгера
    """
    if logs_dir is None:
        # Если не передан logs_dir, создаем в текущей директории
        logs_dir = Path("logs")
        logs_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Обработчик для файла
    log_file = logs_dir / f"{name}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger