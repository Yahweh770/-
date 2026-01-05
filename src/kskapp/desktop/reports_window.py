"""
Модуль окна формирования отчетов для приложения KSK Shop.

Этот модуль содержит класс окна для формирования отчетов по проектам.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, 
    QLabel, QGroupBox, QFormLayout, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit,
    QComboBox
)
from PyQt5.QtCore import Qt, QDate
from database.init_db import SessionLocal
from models.models import Object, Material, FieldData
from main import engine
from datetime import datetime


class ReportsWindow(QWidget):
    """
    Класс окна формирования отчетов.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Формирование отчетов")
        self.setGeometry(200, 200, 1000, 700)
        
        # Создаем сессию базы данных
        SessionLocal.configure(bind=engine)
        self.session = SessionLocal()
        
        self.init_ui()
    
    def init_ui(self):
        """
        Инициализация пользовательского интерфейса.
        """
        layout = QVBoxLayout()
        
        # Создаем вкладки для разных типов отчетов
        tab_widget = QTabWidget()
        
        # Вкладка "Отчет по объектам"
        objects_report_tab = self.create_objects_report_tab()
        tab_widget.addTab(objects_report_tab, "Отчет по объектам")
        
        # Вкладка "Отчет по материалам"
        materials_report_tab = self.create_materials_report_tab()
        tab_widget.addTab(materials_report_tab, "Отчет по материалам")
        
        # Вкладка "Отчет по полевым данным"
        field_report_tab = self.create_field_report_tab()
        tab_widget.addTab(field_report_tab, "Отчет по полевым данным")
        
        # Вкладка "Сводный отчет"
        summary_report_tab = self.create_summary_report_tab()
        tab_widget.addTab(summary_report_tab, "Сводный отчет")
        
        layout.addWidget(tab_widget)
        
        # Кнопки управления
        btn_layout = QHBoxLayout()
        
        generate_btn = QPushButton("Сформировать отчет")
        export_btn = QPushButton("Экспортировать отчет")
        clear_btn = QPushButton("Очистить")
        
        generate_btn.clicked.connect(self.generate_report)
        export_btn.clicked.connect(self.export_report)
        clear_btn.clicked.connect(self.clear_report)
        
        btn_layout.addWidget(generate_btn)
        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def create_objects_report_tab(self):
        """
        Создание вкладки отчета по объектам.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Фильтры
        filter_group = QGroupBox("Фильтры")
        filter_layout = QFormLayout()
        
        self.objects_combo = QComboBox()
        objects = self.session.query(Object).all()
        self.objects_combo.addItem("Все объекты", None)
        for obj in objects:
            self.objects_combo.addItem(f"{obj.name} - {obj.location}", obj.id)
        
        filter_layout.addRow("Объект:", self.objects_combo)
        
        filter_group.setLayout(filter_layout)
        
        # Таблица результатов
        self.objects_table = QTableWidget()
        self.objects_table.setColumnCount(3)
        self.objects_table.setHorizontalHeaderLabels(["ID", "Название", "Местоположение"])
        
        # Настройка ширины столбцов
        header = self.objects_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        # Текст отчета
        self.objects_report_text = QTextEdit()
        self.objects_report_text.setMaximumHeight(150)
        
        layout.addWidget(filter_group)
        layout.addWidget(QLabel("Список объектов:"))
        layout.addWidget(self.objects_table)
        layout.addWidget(QLabel("Текст отчета:"))
        layout.addWidget(self.objects_report_text)
        
        tab.setLayout(layout)
        return tab
    
    def create_materials_report_tab(self):
        """
        Создание вкладки отчета по материалам.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Фильтры
        filter_group = QGroupBox("Фильтры")
        filter_layout = QFormLayout()
        
        self.materials_combo = QComboBox()
        materials = self.session.query(Material).all()
        self.materials_combo.addItem("Все материалы", None)
        for mat in materials:
            self.materials_combo.addItem(f"{mat.name} ({mat.unit})", mat.id)
        
        filter_layout.addRow("Материал:", self.materials_combo)
        
        filter_group.setLayout(filter_layout)
        
        # Таблица результатов
        self.materials_table = QTableWidget()
        self.materials_table.setColumnCount(4)
        self.materials_table.setHorizontalHeaderLabels(["ID", "Название", "Единица измерения", "Норма расхода"])
        
        # Настройка ширины столбцов
        header = self.materials_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        # Текст отчета
        self.materials_report_text = QTextEdit()
        self.materials_report_text.setMaximumHeight(150)
        
        layout.addWidget(filter_group)
        layout.addWidget(QLabel("Список материалов:"))
        layout.addWidget(self.materials_table)
        layout.addWidget(QLabel("Текст отчета:"))
        layout.addWidget(self.materials_report_text)
        
        tab.setLayout(layout)
        return tab
    
    def create_field_report_tab(self):
        """
        Создание вкладки отчета по полевым данным.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Фильтры
        filter_group = QGroupBox("Фильтры")
        filter_layout = QFormLayout()
        
        self.field_objects_combo = QComboBox()
        objects = self.session.query(Object).all()
        self.field_objects_combo.addItem("Все объекты", None)
        for obj in objects:
            self.field_objects_combo.addItem(f"{obj.name}", obj.id)
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        
        filter_layout.addRow("Объект:", self.field_objects_combo)
        filter_layout.addRow("Дата начала:", self.start_date)
        filter_layout.addRow("Дата окончания:", self.end_date)
        
        filter_group.setLayout(filter_layout)
        
        # Таблица результатов
        self.field_table = QTableWidget()
        self.field_table.setColumnCount(7)
        self.field_table.setHorizontalHeaderLabels([
            "ID", "Объект", "Тип линии", "Длина", "Ширина", 
            "Использовано", "Дата"
        ])
        
        # Настройка ширины столбцов
        header = self.field_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        # Текст отчета
        self.field_report_text = QTextEdit()
        self.field_report_text.setMaximumHeight(150)
        
        layout.addWidget(filter_group)
        layout.addWidget(QLabel("Полевые данные:"))
        layout.addWidget(self.field_table)
        layout.addWidget(QLabel("Текст отчета:"))
        layout.addWidget(self.field_report_text)
        
        tab.setLayout(layout)
        return tab
    
    def create_summary_report_tab(self):
        """
        Создание вкладки сводного отчета.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Фильтры
        filter_group = QGroupBox("Фильтры")
        filter_layout = QFormLayout()
        
        self.summary_objects_combo = QComboBox()
        objects = self.session.query(Object).all()
        self.summary_objects_combo.addItem("Все объекты", None)
        for obj in objects:
            self.summary_objects_combo.addItem(f"{obj.name}", obj.id)
        
        self.summary_start_date = QDateEdit()
        self.summary_start_date.setDate(QDate.currentDate().addMonths(-1))
        self.summary_start_date.setCalendarPopup(True)
        
        self.summary_end_date = QDateEdit()
        self.summary_end_date.setDate(QDate.currentDate())
        self.summary_end_date.setCalendarPopup(True)
        
        filter_layout.addRow("Объект:", self.summary_objects_combo)
        filter_layout.addRow("Дата начала:", self.summary_start_date)
        filter_layout.addRow("Дата окончания:", self.summary_end_date)
        
        filter_group.setLayout(filter_layout)
        
        # Текст сводного отчета
        self.summary_report_text = QTextEdit()
        
        layout.addWidget(filter_group)
        layout.addWidget(QLabel("Сводный отчет:"))
        layout.addWidget(self.summary_report_text)
        
        tab.setLayout(layout)
        return tab
    
    def generate_report(self):
        """
        Генерация отчета на основе выбранной вкладки.
        """
        current_tab_index = self.findChild(QTabWidget).currentIndex()
        
        if current_tab_index == 0:  # Отчет по объектам
            self.generate_objects_report()
        elif current_tab_index == 1:  # Отчет по материалам
            self.generate_materials_report()
        elif current_tab_index == 2:  # Отчет по полевым данным
            self.generate_field_report()
        elif current_tab_index == 3:  # Сводный отчет
            self.generate_summary_report()
    
    def generate_objects_report(self):
        """
        Генерация отчета по объектам.
        """
        try:
            # Очищаем таблицу
            self.objects_table.setRowCount(0)
            
            # Получаем ID выбранного объекта
            selected_obj_id = self.objects_combo.currentData()
            
            # Формируем запрос
            if selected_obj_id is None:
                objects = self.session.query(Object).all()
            else:
                objects = self.session.query(Object).filter(Object.id == selected_obj_id).all()
            
            # Заполняем таблицу
            for row, obj in enumerate(objects):
                self.objects_table.insertRow(row)
                self.objects_table.setItem(row, 0, QTableWidgetItem(str(obj.id)))
                self.objects_table.setItem(row, 1, QTableWidgetItem(obj.name))
                self.objects_table.setItem(row, 2, QTableWidgetItem(obj.location))
                
                # Делаем ID не редактируемым
                self.objects_table.item(row, 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            
            # Формируем текст отчета
            report_text = f"Отчет по объектам: Найдено {len(objects)} объектов\n"
            report_text += "=" * 50 + "\n"
            
            for obj in objects:
                report_text += f"ID: {obj.id}, Название: {obj.name}, Местоположение: {obj.location}\n"
            
            self.objects_report_text.setPlainText(report_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при генерации отчета по объектам: {str(e)}")
    
    def generate_materials_report(self):
        """
        Генерация отчета по материалам.
        """
        try:
            # Очищаем таблицу
            self.materials_table.setRowCount(0)
            
            # Получаем ID выбранного материала
            selected_mat_id = self.materials_combo.currentData()
            
            # Формируем запрос
            if selected_mat_id is None:
                materials = self.session.query(Material).all()
            else:
                materials = self.session.query(Material).filter(Material.id == selected_mat_id).all()
            
            # Заполняем таблицу
            for row, mat in enumerate(materials):
                self.materials_table.insertRow(row)
                self.materials_table.setItem(row, 0, QTableWidgetItem(str(mat.id)))
                self.materials_table.setItem(row, 1, QTableWidgetItem(mat.name))
                self.materials_table.setItem(row, 2, QTableWidgetItem(mat.unit))
                
                # Форматируем норму расхода с 3 знаками после запятой
                norm_item = QTableWidgetItem(f"{mat.norm:.3f}")
                norm_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.materials_table.setItem(row, 3, norm_item)
                
                # Делаем ID не редактируемым
                self.materials_table.item(row, 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            
            # Формируем текст отчета
            report_text = f"Отчет по материалам: Найдено {len(materials)} материалов\n"
            report_text += "=" * 50 + "\n"
            
            for mat in materials:
                report_text += f"ID: {mat.id}, Название: {mat.name}, Ед.изм: {mat.unit}, Норма: {mat.norm:.3f}\n"
            
            self.materials_report_text.setPlainText(report_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при генерации отчета по материалам: {str(e)}")
    
    def generate_field_report(self):
        """
        Генерация отчета по полевым данным.
        """
        try:
            # Очищаем таблицу
            self.field_table.setRowCount(0)
            
            # Получаем параметры фильтрации
            selected_obj_id = self.field_objects_combo.currentData()
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            # Формируем запрос
            query = self.session.query(FieldData).filter(
                FieldData.date >= start_date,
                FieldData.date <= end_date
            )
            
            if selected_obj_id is not None:
                query = query.filter(FieldData.object_id == selected_obj_id)
            
            field_data = query.all()
            
            # Заполняем таблицу
            for row, data in enumerate(field_data):
                self.field_table.insertRow(row)
                
                # Получаем название объекта
                obj = self.session.query(Object).filter(Object.id == data.object_id).first()
                obj_name = obj.name if obj else "Неизвестный объект"
                
                # Получаем тип линии
                # Для упрощения, в реальном приложении нужно получить название типа линии
                line_type_name = f"Тип {data.line_type_id}" if data.line_type_id else "Неизвестный тип"
                
                self.field_table.setItem(row, 0, QTableWidgetItem(str(data.id)))
                self.field_table.setItem(row, 1, QTableWidgetItem(obj_name))
                self.field_table.setItem(row, 2, QTableWidgetItem(line_type_name))
                self.field_table.setItem(row, 3, QTableWidgetItem(f"{data.length:.2f}"))
                self.field_table.setItem(row, 4, QTableWidgetItem(f"{data.width:.2f}"))
                self.field_table.setItem(row, 5, QTableWidgetItem(f"{data.material_used:.2f}"))
                self.field_table.setItem(row, 6, QTableWidgetItem(data.date.strftime("%Y-%m-%d")))
                
                # Делаем ID не редактируемым
                self.field_table.item(row, 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            
            # Формируем текст отчета
            report_text = f"Отчет по полевым данным: Найдено {len(field_data)} записей\n"
            report_text += f"Период: {start_date} - {end_date}\n"
            report_text += "=" * 50 + "\n"
            
            for data in field_data:
                obj = self.session.query(Object).filter(Object.id == data.object_id).first()
                obj_name = obj.name if obj else "Неизвестный объект"
                
                report_text += f"ID: {data.id}, Объект: {obj_name}, Длина: {data.length:.2f}, "
                report_text += f"Ширина: {data.width:.2f}, Использовано: {data.material_used:.2f}, "
                report_text += f"Дата: {data.date.strftime('%Y-%m-%d')}\n"
            
            self.field_report_text.setPlainText(report_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при генерации отчета по полевым данным: {str(e)}")
    
    def generate_summary_report(self):
        """
        Генерация сводного отчета.
        """
        try:
            # Получаем параметры фильтрации
            selected_obj_id = self.summary_objects_combo.currentData()
            start_date = self.summary_start_date.date().toPyDate()
            end_date = self.summary_end_date.date().toPyDate()
            
            # Формируем запросы
            query = self.session.query(FieldData).filter(
                FieldData.date >= start_date,
                FieldData.date <= end_date
            )
            
            if selected_obj_id is not None:
                query = query.filter(FieldData.object_id == selected_obj_id)
            
            field_data = query.all()
            
            # Вычисляем итоговые значения
            total_length = sum(data.length for data in field_data)
            total_material_used = sum(data.material_used for data in field_data)
            total_records = len(field_data)
            
            # Формируем текст отчета
            report_text = "Сводный отчет по проекту\n"
            report_text += "=" * 50 + "\n"
            report_text += f"Период: {start_date} - {end_date}\n"
            report_text += f"Всего записей: {total_records}\n"
            report_text += f"Общая длина: {total_length:.2f} м\n"
            report_text += f"Всего использовано материалов: {total_material_used:.2f} ед\n"
            
            if field_data:
                avg_material_per_record = total_material_used / total_records
                report_text += f"Среднее использование материалов на запись: {avg_material_per_record:.2f} ед\n"
            
            report_text += "\nДетализация:\n"
            report_text += "-" * 30 + "\n"
            
            for data in field_data:
                obj = self.session.query(Object).filter(Object.id == data.object_id).first()
                obj_name = obj.name if obj else "Неизвестный объект"
                
                report_text += f"• {data.date.strftime('%Y-%m-%d')}: {obj_name}, "
                report_text += f"длина {data.length:.2f} м, использовано {data.material_used:.2f} ед\n"
            
            self.summary_report_text.setPlainText(report_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при генерации сводного отчета: {str(e)}")
    
    def export_report(self):
        """
        Экспорт отчета в файл.
        """
        try:
            # Получаем текст отчета с текущей вкладки
            current_tab_index = self.findChild(QTabWidget).currentIndex()
            
            if current_tab_index == 0:
                report_text = self.objects_report_text.toPlainText()
            elif current_tab_index == 1:
                report_text = self.materials_report_text.toPlainText()
            elif current_tab_index == 2:
                report_text = self.field_report_text.toPlainText()
            elif current_tab_index == 3:
                report_text = self.summary_report_text.toPlainText()
            else:
                report_text = ""
            
            if not report_text:
                QMessageBox.warning(self, "Предупреждение", "Нет данных для экспорта")
                return
            
            # Генерируем имя файла
            from datetime import datetime
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            # Сохраняем в файл
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_text)
            
            QMessageBox.information(self, "Успех", f"Отчет экспортирован в файл: {filename}")
        
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте отчета: {str(e)}")
    
    def clear_report(self):
        """
        Очистка текста отчета.
        """
        current_tab_index = self.findChild(QTabWidget).currentIndex()
        
        if current_tab_index == 0:
            self.objects_report_text.clear()
        elif current_tab_index == 1:
            self.materials_report_text.clear()
        elif current_tab_index == 2:
            self.field_report_text.clear()
        elif current_tab_index == 3:
            self.summary_report_text.clear()
    
    def closeEvent(self, event):
        """
        Обработчик события закрытия окна.
        """
        self.session.close()
        event.accept()