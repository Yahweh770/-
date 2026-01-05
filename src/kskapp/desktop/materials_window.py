"""
Модуль окна управления материалами для приложения KSK Shop.

Этот модуль содержит класс окна для управления материалами проекта.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QGroupBox, QFormLayout, QMessageBox,
    QHeaderView, QDoubleSpinBox
)
from PyQt5.QtCore import Qt
from database.init_db import SessionLocal
from models.models import Material
from main import engine


class MaterialsWindow(QWidget):
    """
    Класс окна управления материалами.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление материалами")
        self.setGeometry(200, 200, 900, 600)
        
        # Создаем сессию базы данных
        SessionLocal.configure(bind=engine)
        self.session = SessionLocal()
        
        self.init_ui()
        self.load_materials()
    
    def init_ui(self):
        """
        Инициализация пользовательского интерфейса.
        """
        layout = QVBoxLayout()
        
        # Группа для добавления нового материала
        add_group = QGroupBox("Добавить новый материал")
        add_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.unit_input = QLineEdit()
        self.norm_input = QDoubleSpinBox()
        self.norm_input.setRange(0.0, 999999.0)
        self.norm_input.setDecimals(3)
        self.norm_input.setValue(1.0)
        
        add_layout.addRow("Название:", self.name_input)
        add_layout.addRow("Единица измерения:", self.unit_input)
        add_layout.addRow("Норма расхода:", self.norm_input)
        
        add_btn = QPushButton("Добавить материал")
        add_btn.clicked.connect(self.add_material)
        add_layout.addRow(add_btn)
        
        add_group.setLayout(add_layout)
        
        # Таблица для отображения материалов
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Единица измерения", "Норма расхода"])
        
        # Настройка ширины столбцов
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        # Кнопки управления
        btn_layout = QHBoxLayout()
        
        edit_btn = QPushButton("Редактировать")
        delete_btn = QPushButton("Удалить")
        refresh_btn = QPushButton("Обновить")
        
        edit_btn.clicked.connect(self.edit_material)
        delete_btn.clicked.connect(self.delete_material)
        refresh_btn.clicked.connect(self.load_materials)
        
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        
        # Добавляем элементы в основной макет
        layout.addWidget(add_group)
        layout.addWidget(QLabel("Список материалов:"))
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def load_materials(self):
        """
        Загрузка и отображение материалов из базы данных.
        """
        try:
            # Очищаем таблицу
            self.table.setRowCount(0)
            
            # Получаем материалы из базы данных
            materials = self.session.query(Material).all()
            
            for row, mat in enumerate(materials):
                self.table.insertRow(row)
                
                # Заполняем ячейки
                self.table.setItem(row, 0, QTableWidgetItem(str(mat.id)))
                self.table.setItem(row, 1, QTableWidgetItem(mat.name))
                self.table.setItem(row, 2, QTableWidgetItem(mat.unit))
                
                # Форматируем норму расхода с 3 знаками после запятой
                norm_item = QTableWidgetItem(f"{mat.norm:.3f}")
                norm_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row, 3, norm_item)
                
                # Делаем ID не редактируемым
                self.table.item(row, 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке материалов: {str(e)}")
    
    def add_material(self):
        """
        Добавление нового материала в базу данных.
        """
        name = self.name_input.text().strip()
        unit = self.unit_input.text().strip()
        norm = self.norm_input.value()
        
        if not name:
            QMessageBox.warning(self, "Предупреждение", "Введите название материала")
            return
        
        if not unit:
            QMessageBox.warning(self, "Предупреждение", "Введите единицу измерения")
            return
        
        try:
            # Создаем новый материал
            new_material = Material(name=name, unit=unit, norm=norm)
            self.session.add(new_material)
            self.session.commit()
            
            # Очищаем поля ввода
            self.name_input.clear()
            self.unit_input.clear()
            self.norm_input.setValue(1.0)
            
            # Обновляем таблицу
            self.load_materials()
            
            QMessageBox.information(self, "Успех", "Материал успешно добавлен")
        
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении материала: {str(e)}")
    
    def edit_material(self):
        """
        Редактирование выбранного материала.
        """
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите материал для редактирования")
            return
        
        try:
            # Получаем ID выбранного материала
            mat_id = int(self.table.item(current_row, 0).text())
            mat = self.session.query(Material).filter(Material.id == mat_id).first()
            
            if mat:
                # Обновляем данные материала
                mat.name = self.table.item(current_row, 1).text()
                mat.unit = self.table.item(current_row, 2).text()
                
                # Преобразуем норму из строки в число
                try:
                    norm_value = float(self.table.item(current_row, 3).text())
                    mat.norm = norm_value
                except ValueError:
                    QMessageBox.warning(self, "Предупреждение", "Некорректное значение нормы расхода")
                    return
                
                self.session.commit()
                self.load_materials()  # Обновляем таблицу для правильного форматирования
                QMessageBox.information(self, "Успех", "Материал успешно обновлен")
            else:
                QMessageBox.warning(self, "Предупреждение", "Материал не найден")
        
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при редактировании материала: {str(e)}")
    
    def delete_material(self):
        """
        Удаление выбранного материала.
        """
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите материал для удаления")
            return
        
        reply = QMessageBox.question(
            self, "Подтверждение", 
            "Вы уверены, что хотите удалить выбранный материал?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Получаем ID выбранного материала
                mat_id = int(self.table.item(current_row, 0).text())
                mat = self.session.query(Material).filter(Material.id == mat_id).first()
                
                if mat:
                    self.session.delete(mat)
                    self.session.commit()
                    self.load_materials()
                    QMessageBox.information(self, "Успех", "Материал успешно удален")
                else:
                    QMessageBox.warning(self, "Предупреждение", "Материал не найден")
            
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении материала: {str(e)}")
    
    def closeEvent(self, event):
        """
        Обработчик события закрытия окна.
        """
        self.session.close()
        event.accept()