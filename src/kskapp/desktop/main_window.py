"""
Модуль главного окна приложения KSK Shop.

Этот модуль содержит класс главного окна приложения с расширенным интерфейсом.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, 
    QHBoxLayout, QFileDialog, QMessageBox, QScrollArea, QFrame,
    QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
from utils.image_handler import ImageHandler
from desktop.objects_window import ObjectsWindow
from desktop.materials_window import MaterialsWindow
from desktop.reports_window import ReportsWindow


class MainWindow(QMainWindow):
    """
    Класс главного окна приложения.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KSK Shop - Система управления проектами")
        self.setGeometry(100, 100, 1000, 700)
        
        # Инициализация обработчика изображений
        self.image_handler = ImageHandler()
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной макет
        main_layout = QVBoxLayout()
        
        # Заголовок
        title_label = QLabel("Добро пожаловать в KSK Shop")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        
        # Описание системы
        description_label = QLabel(
            "Система управления проектами KSK Shop для учета материалов и объектов"
        )
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        description_label.setStyleSheet("margin: 10px;")
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        btn_objects = QPushButton("Объекты")
        btn_materials = QPushButton("Материалы")
        btn_reports = QPushButton("Отчеты")
        btn_upload_photo = QPushButton("Загрузить фото")
        
        # Устанавливаем фиксированный размер для кнопок
        for btn in [btn_objects, btn_materials, btn_reports, btn_upload_photo]:
            btn.setFixedSize(120, 40)
        
        button_layout.addWidget(btn_objects)
        button_layout.addWidget(btn_materials)
        button_layout.addWidget(btn_reports)
        button_layout.addWidget(btn_upload_photo)
        
        # Добавляем вертикальный разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        
        # Группа для фотоотчетов
        photo_group = QGroupBox("Фотоотчеты")
        photo_layout = QVBoxLayout()
        
        # Область для отображения фото
        self.photo_area = QScrollArea()
        self.photo_area.setMinimumHeight(300)
        self.photo_area.setAlignment(Qt.AlignCenter)
        
        # Метка для отображения фото
        self.photo_label = QLabel()
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setText("Фото не загружено")
        self.photo_label.setStyleSheet("border: 1px solid gray; padding: 20px;")
        self.photo_area.setWidget(self.photo_label)
        
        # Кнопка для очистки фото
        btn_clear_photo = QPushButton("Очистить фото")
        btn_clear_photo.setFixedSize(120, 30)
        btn_clear_photo.clicked.connect(self.clear_photo)
        
        # Добавляем элементы в макет группы фото
        photo_layout.addWidget(self.photo_area)
        photo_layout.addWidget(btn_clear_photo, 0, Qt.AlignCenter)
        photo_group.setLayout(photo_layout)
        
        # Добавляем элементы в основной макет
        main_layout.addWidget(title_label)
        main_layout.addWidget(description_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(separator)
        main_layout.addWidget(photo_group)
        
        central_widget.setLayout(main_layout)
        
        # Подключаем сигналы
        btn_objects.clicked.connect(self.show_objects)
        btn_materials.clicked.connect(self.show_materials)
        btn_reports.clicked.connect(self.show_reports)
        btn_upload_photo.clicked.connect(self.upload_photo)
    
    def show_objects(self):
        """
        Открытие окна объектов.
        """
        self.objects_window = ObjectsWindow()
        self.objects_window.show()
    
    def show_materials(self):
        """
        Открытие окна материалов.
        """
        self.materials_window = MaterialsWindow()
        self.materials_window.show()
    
    def show_reports(self):
        """
        Открытие окна отчетов.
        """
        self.reports_window = ReportsWindow()
        self.reports_window.show()
    
    def upload_photo(self):
        """
        Загрузка фото через диалоговое окно.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите фото",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"
        )
        
        if file_path:
            try:
                # Используем наш обработчик изображений
                pixmap = self.image_handler.load_image(file_path, max_size=(600, 400))
                
                if pixmap is None:
                    QMessageBox.warning(self, "Ошибка", "Невозможно загрузить изображение")
                    return
                
                # Отображаем изображение
                self.photo_label.setPixmap(pixmap)
                
                # Обновляем стиль для рамки фото
                self.photo_label.setStyleSheet("border: 1px solid gray;")
                
                print(f"Фото загружено: {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке фото: {str(e)}")
    
    def clear_photo(self):
        """
        Очистка отображаемого фото.
        """
        self.photo_label.clear()
        self.photo_label.setText("Фото не загружено")
        self.photo_label.setStyleSheet("border: 1px solid gray; padding: 20px;")
        print("Фото очищено")
