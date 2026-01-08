"""
Модуль окна управления объектами для приложения Strod-Service Technology.

Этот модуль содержит класс окна для управления объектами проекта.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QGroupBox, QFormLayout, QMessageBox,
    QHeaderView
)
from PyQt5.QtCore import Qt
from strodservice.database.init_db import SessionLocal, engine
from strodservice.models.models import Object


class ObjectsWindow(QWidget):
    """
    Класс окна управления объектами.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление объектами")
        self.setGeometry(200, 200, 900, 600)
        
        # Создаем сессию базы данных
        from strodservice.database.init_db import engine
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        self.session = SessionLocal()
        
        self.init_ui()
        self.load_objects()
    
    def init_ui(self):
        """
        Инициализация пользовательского интерфейса.
        """
        layout = QVBoxLayout()
        
        # Группа для добавления нового объекта
        add_group = QGroupBox("Добавить новый объект")
        add_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.location_input = QLineEdit()
        
        add_layout.addRow("Название:", self.name_input)
        add_layout.addRow("Местоположение:", self.location_input)
        
        add_btn = QPushButton("Добавить объект")
        add_btn.clicked.connect(self.add_object)
        add_layout.addRow(add_btn)
        
        add_group.setLayout(add_layout)
        
        # Таблица для отображения объектов
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Местоположение"])
        
        # Настройка ширины столбцов
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        # Кнопки управления
        btn_layout = QHBoxLayout()
        
        edit_btn = QPushButton("Редактировать")
        delete_btn = QPushButton("Удалить")
        refresh_btn = QPushButton("Обновить")
        
        edit_btn.clicked.connect(self.edit_object)
        delete_btn.clicked.connect(self.delete_object)
        refresh_btn.clicked.connect(self.load_objects)
        
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        
        # Добавляем элементы в основной макет
        layout.addWidget(add_group)
        layout.addWidget(QLabel("Список объектов:"))
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def load_objects(self):
        """
        Загрузка и отображение объектов из базы данных.
        """
        try:
            # Очищаем таблицу
            self.table.setRowCount(0)
            
            # Получаем объекты из базы данных
            objects = self.session.query(Object).all()
            
            for row, obj in enumerate(objects):
                self.table.insertRow(row)
                
                # Заполняем ячейки
                self.table.setItem(row, 0, QTableWidgetItem(str(obj.id)))
                self.table.setItem(row, 1, QTableWidgetItem(obj.name))
                self.table.setItem(row, 2, QTableWidgetItem(obj.location))
                
                # Делаем ID не редактируемым
                self.table.item(row, 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке объектов: {str(e)}")
    
    def add_object(self):
        """
        Добавление нового объекта в базу данных.
        """
        name = self.name_input.text().strip()
        location = self.location_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Предупреждение", "Введите название объекта")
            return
        
        try:
            # Создаем новый объект
            new_object = Object(name=name, location=location)
            self.session.add(new_object)
            self.session.commit()
            
            # Очищаем поля ввода
            self.name_input.clear()
            self.location_input.clear()
            
            # Обновляем таблицу
            self.load_objects()
            
            QMessageBox.information(self, "Успех", "Объект успешно добавлен")
        
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении объекта: {str(e)}")
    
    def edit_object(self):
        """
        Редактирование выбранного объекта.
        """
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите объект для редактирования")
            return
        
        try:
            # Получаем ID выбранного объекта
            obj_id = int(self.table.item(current_row, 0).text())
            obj = self.session.query(Object).filter(Object.id == obj_id).first()
            
            if obj:
                # Обновляем данные объекта
                obj.name = self.table.item(current_row, 1).text()
                obj.location = self.table.item(current_row, 2).text()
                
                self.session.commit()
                QMessageBox.information(self, "Успех", "Объект успешно обновлен")
            else:
                QMessageBox.warning(self, "Предупреждение", "Объект не найден")
        
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при редактировании объекта: {str(e)}")
    
    def delete_object(self):
        """
        Удаление выбранного объекта.
        """
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите объект для удаления")
            return
        
        reply = QMessageBox.question(
            self, "Подтверждение", 
            "Вы уверены, что хотите удалить выбранный объект?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Получаем ID выбранного объекта
                obj_id = int(self.table.item(current_row, 0).text())
                obj = self.session.query(Object).filter(Object.id == obj_id).first()
                
                if obj:
                    self.session.delete(obj)
                    self.session.commit()
                    self.load_objects()
                    QMessageBox.information(self, "Успех", "Объект успешно удален")
                else:
                    QMessageBox.warning(self, "Предупреждение", "Объект не найден")
            
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении объекта: {str(e)}")
    
    def closeEvent(self, event):
        """
        Обработчик события закрытия окна.
        """
        self.session.close()
        event.accept()