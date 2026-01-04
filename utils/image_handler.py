"""
Модуль для обработки изображений и фотоотчетов в приложении KSK Shop.

Этот модуль предоставляет функции для:
- Загрузки и сохранения изображений
- Масштабирования изображений
- Конвертации форматов изображений
- Валидации изображений
"""

import os
from pathlib import Path
from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
import logging


class ImageHandler:
    """
    Класс для обработки изображений.
    """
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    
    def __init__(self, logger=None):
        """
        Инициализация обработчика изображений.
        
        Args:
            logger: Объект логгера (опционально)
        """
        self.logger = logger or logging.getLogger(__name__)
        
    def validate_image(self, file_path):
        """
        Проверяет, является ли файл допустимым изображением.
        
        Args:
            file_path (str): Путь к файлу изображения
            
        Returns:
            bool: True, если файл является допустимым изображением, иначе False
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"Файл не существует: {file_path}")
                return False
            
            if file_path.suffix.lower() not in self.SUPPORTED_FORMATS:
                self.logger.error(f"Неподдерживаемый формат изображения: {file_path.suffix}")
                return False
            
            # Проверяем, можно ли открыть изображение
            with Image.open(file_path) as img:
                img.verify()
            
            # Повторно открываем изображение, так как verify() закрывает его
            with Image.open(file_path):
                pass
            
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при валидации изображения {file_path}: {str(e)}")
            return False
    
    def load_image(self, file_path, max_size=(800, 600)):
        """
        Загружает изображение и возвращает его в формате QPixmap.
        
        Args:
            file_path (str): Путь к файлу изображения
            max_size (tuple): Максимальный размер изображения (ширина, высота)
            
        Returns:
            QPixmap: Изображение в формате QPixmap или None в случае ошибки
        """
        try:
            if not self.validate_image(file_path):
                return None
            
            # Открываем изображение с помощью PIL
            with Image.open(file_path) as img:
                # Конвертируем в RGB, если изображение в другом формате (например, RGBA)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Масштабируем изображение, если оно больше максимального размера
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Конвертируем в QPixmap
                qt_image = ImageQt.ImageQt(img)
                pixmap = QPixmap.fromImage(qt_image)
                
                return pixmap
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке изображения {file_path}: {str(e)}")
            return None
    
    def save_image(self, pixmap, file_path, quality=85):
        """
        Сохраняет QPixmap в файл.
        
        Args:
            pixmap: Объект QPixmap
            file_path (str): Путь для сохранения файла
            quality (int): Качество сохранения (для JPEG)
            
        Returns:
            bool: True при успешном сохранении, иначе False
        """
        try:
            # Конвертируем QPixmap в PIL Image
            qimage = pixmap.toImage()
            img = Image.frombytes("RGBA", (qimage.width(), qimage.height()), qimage.bits().asstring())
            
            # Сохраняем изображение
            img.save(file_path, quality=quality, optimize=True)
            self.logger.info(f"Изображение сохранено: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении изображения {file_path}: {str(e)}")
            return False
    
    def resize_image(self, file_path, output_path, size, maintain_aspect_ratio=True):
        """
        Изменяет размер изображения.
        
        Args:
            file_path (str): Путь к исходному файлу
            output_path (str): Путь для сохранения измененного изображения
            size (tuple): Новый размер (ширина, высота)
            maintain_aspect_ratio (bool): Сохранять ли пропорции изображения
            
        Returns:
            bool: True при успешном изменении размера, иначе False
        """
        try:
            if not self.validate_image(file_path):
                return False
            
            with Image.open(file_path) as img:
                if maintain_aspect_ratio:
                    # Масштабируем с сохранением пропорций
                    img.thumbnail(size, Image.Resampling.LANCZOS)
                else:
                    # Изменяем размер без сохранения пропорций
                    img = img.resize(size, Image.Resampling.LANCZOS)
                
                # Сохраняем изображение
                img.save(output_path)
                self.logger.info(f"Размер изображения изменен: {file_path} -> {output_path}")
                return True
        except Exception as e:
            self.logger.error(f"Ошибка при изменении размера изображения {file_path}: {str(e)}")
            return False
    
    def get_image_info(self, file_path):
        """
        Получает информацию об изображении.
        
        Args:
            file_path (str): Путь к файлу изображения
            
        Returns:
            dict: Словарь с информацией об изображении
        """
        try:
            if not self.validate_image(file_path):
                return None
            
            with Image.open(file_path) as img:
                info = {
                    'format': img.format,
                    'size': img.size,  # (ширина, высота)
                    'mode': img.mode,
                    'file_path': str(file_path),
                    'file_size': os.path.getsize(file_path)
                }
                return info
        except Exception as e:
            self.logger.error(f"Ошибка при получении информации об изображении {file_path}: {str(e)}")
            return None


def scale_pixmap(pixmap, max_width, max_height, keep_aspect_ratio=True):
    """
    Масштабирует QPixmap до заданных максимальных размеров.
    
    Args:
        pixmap (QPixmap): Исходное изображение
        max_width (int): Максимальная ширина
        max_height (int): Максимальная высота
        keep_aspect_ratio (bool): Сохранять ли пропорции изображения
        
    Returns:
        QPixmap: Масштабированное изображение
    """
    if keep_aspect_ratio:
        return pixmap.scaled(
            max_width, max_height,
            aspectRatioMode=1,  # Qt.KeepAspectRatio
            transformMode=2     # Qt.SmoothTransformation
        )
    else:
        return pixmap.scaled(
            max_width, max_height,
            aspectRatioMode=0,  # Qt.IgnoreAspectRatio
            transformMode=2     # Qt.SmoothTransformation
        )