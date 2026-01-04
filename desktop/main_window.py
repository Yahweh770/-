"""
Модуль главного окна приложения KSK Shop.

Этот модуль содержит класс главного окна приложения с базовым интерфейсом.
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    """
    Класс главного окна приложения.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KSK Shop - Система управления проектами")
        self.setGeometry(100, 100, 800, 600)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Макет
        layout = QVBoxLayout()
        
        # Заголовок
        title_label = QLabel("Добро пожаловать в KSK Shop")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        # Описание системы
        description_label = QLabel(
            "Система управления проектами KSK Shop для учета материалов и объектов"
        )
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        btn_objects = QPushButton("Объекты")
        btn_materials = QPushButton("Материалы")
        btn_reports = QPushButton("Отчеты")
        
        button_layout.addWidget(btn_objects)
        button_layout.addWidget(btn_materials)
        button_layout.addWidget(btn_reports)
        
        # Добавляем элементы в основной макет
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addLayout(button_layout)
        
        # Растягиваемый элемент для центрирования
        layout.addStretch()
        
        central_widget.setLayout(layout)
        
        # Подключаем сигналы
        btn_objects.clicked.connect(self.show_objects)
        btn_materials.clicked.connect(self.show_materials)
        btn_reports.clicked.connect(self.show_reports)
    
    def show_objects(self):
        """
        Открытие окна объектов.
        """
        print("Открытие окна объектов")
    
    def show_materials(self):
        """
        Открытие окна материалов.
        """
        print("Открытие окна материалов")
    
    def show_reports(self):
        """
        Открытие окна отчетов.
        """
        print("Открытие окна отчетов")