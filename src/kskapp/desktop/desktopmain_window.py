from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QListWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QFormLayout, QMessageBox, QFileDialog,
    QHeaderView, QComboBox, QDateEdit
)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Имитация подключения к базе и моделей
from database.models import Object, Material, Document
from database.init_db import Session
from core.gost_engine import get_material_norm
from core.gpr_integration import get_gpr_data
from core.calc_engine import calculate_materials_for_object
from core.notifications import notify_manager_low_material
from core.contractor_manager import ContractorForm
from core.reports import generate_materials_report
from api.fuel_card_api import get_fuel_balance, get_fuel_transactions
from utils.telegram_bot import send_telegram_message
from utils.logger import app_logger
from utils.updater import update_app
from utils.autostart import add_to_startup, remove_from_startup
from utils.settings_manager import SettingsWidget
from utils.error_reporter import report_error
from core.field_data_form import FieldDataForm
from core.offline_calc import OfflineCalcWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Исполнительная документация")
        self.setGeometry(100, 100, 1400, 900)

        # Основной слой
        main_layout = QHBoxLayout()

        # Навигация
        self.nav_list = QListWidget()
        self.nav_list.addItems([
            "Объекты",
            "Материалы",
            "Документы",
            "ГПР",
            "Субподрядчики",
            "Топливные карты",
            "Калькулятор",
            "Отчёты",
            "Графики",
            "Полевые данные",
            "Автономный калькулятор",
            "Настройки"
        ])
        self.nav_list.setMaximumWidth(150)
        self.nav_list.currentRowChanged.connect(self.switch_page)

        # Центральный виджет
        self.stacked_widget = QStackedWidget()

        # Создание страниц
        self.objects_page = self.create_objects_page()
        self.materials_page = self.create_materials_page()
        self.documents_page = self.create_documents_page()
        self.gpr_page = self.create_gpr_page()
        self.contractors_page = ContractorForm()
        self.fuel_cards_page = self.create_fuel_cards_page()
        self.calculator_page = self.create_calculator_page()
        self.reports_page = self.create_reports_page()
        self.charts_page = self.create_charts_page()
        self.field_data_page = FieldDataForm()
        self.offline_calc_page = OfflineCalcWidget()
        self.settings_page = SettingsWidget()

        # Добавление страниц в стек
        self.stacked_widget.addWidget(self.objects_page)
        self.stacked_widget.addWidget(self.materials_page)
        self.stacked_widget.addWidget(self.documents_page)
        self.stacked_widget.addWidget(self.gpr_page)
        self.stacked_widget.addWidget(self.contractors_page)
        self.stacked_widget.addWidget(self.fuel_cards_page)
        self.stacked_widget.addWidget(self.calculator_page)
        self.stacked_widget.addWidget(self.reports_page)
        self.stacked_widget.addWidget(self.charts_page)
        self.stacked_widget.addWidget(self.field_data_page)
        self.stacked_widget.addWidget(self.offline_calc_page)
        self.stacked_widget.addWidget(self.settings_page)

        # Сборка основного окна
        main_layout.addWidget(self.nav_list)
        main_layout.addWidget(self.stacked_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # ✅ Логирование запуска
        app_logger.info("Приложение запущено")

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)

    # === СТРАНИЦА: Объекты ===
    def create_objects_page(self):
        layout = QVBoxLayout()

        # Фильтр
        filter_layout = QHBoxLayout()
        self.obj_filter_input = QLineEdit()
        self.obj_filter_input.setPlaceholderText("Фильтр по названию...")
        self.obj_filter_input.textChanged.connect(self.filter_objects)
        filter_layout.addWidget(QLabel("Фильтр:"))
        filter_layout.addWidget(self.obj_filter_input)

        layout.addLayout(filter_layout)

        # Таблица
        self.objects_table = QTableWidget(0, 4)
        self.objects_table.setHorizontalHeaderLabels(["ID", "Название", "Местоположение", "Действия"])
        header = self.objects_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.load_objects_to_table()

        layout.addWidget(self.objects_table)

        # ✅ Кнопка "Рассчитать расход материалов"
        btn_calc = QPushButton("Рассчитать расход материалов")
        btn_calc.clicked.connect(self.calculate_materials_for_current_object)
        layout.addWidget(btn_calc)

        btn_add = QPushButton("Добавить объект")
        btn_add.clicked.connect(self.add_object)
        layout.addWidget(btn_add)

        page = QWidget()
        page.setLayout(layout)
        return page

    def load_objects_to_table(self):
        try:
            session = Session()
            objects = session.query(Object).all()
            self.objects_table.setRowCount(len(objects))
            for i, obj in enumerate(objects):
                self.objects_table.setItem(i, 0, QTableWidgetItem(str(obj.id)))
                self.objects_table.setItem(i, 1, QTableWidgetItem(obj.name))
                self.objects_table.setItem(i, 2, QTableWidgetItem(obj.location))

                # Кнопки "Редактировать", "Удалить"
                btn_layout = QHBoxLayout()
                btn_edit = QPushButton("Редактировать")
                btn_edit.clicked.connect(lambda _, id=obj.id: self.edit_object(id))
                btn_delete = QPushButton("Удалить")
                btn_delete.clicked.connect(lambda _, id=obj.id: self.delete_object(id))

                btn_widget = QWidget()
                btn_widget.setLayout(btn_layout)
                btn_layout.addWidget(btn_edit)
                btn_layout.addWidget(btn_delete)
                btn_layout.setContentsMargins(4, 2, 4, 2)
                self.objects_table.setCellWidget(i, 3, btn_widget)

            session.close()
        except Exception as e:
            app_logger.error(f"Ошибка загрузки объектов: {e}")
            report_error(e)

    def filter_objects(self):
        text = self.obj_filter_input.text().lower()
        for row in range(self.objects_table.rowCount()):
            item = self.objects_table.item(row, 1)  # Название
            visible = text in item.text().lower() if item else False
            self.objects_table.setRowHidden(row, not visible)

    def add_object(self):
        try:
            from PyQt5.QtWidgets import QDialog, QDialogButtonBox
            dialog = QDialog(self)
            dialog.setWindowTitle("Добавить объект")
            form = QFormLayout(dialog)

            name_input = QLineEdit()
            location_input = QLineEdit()

            form.addRow("Название:", name_input)
            form.addRow("Местоположение:", location_input)

            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(lambda: self.save_new_object(name_input.text(), location_input.text(), dialog))
            buttons.rejected.connect(dialog.close)
            form.addRow(buttons)

            dialog.exec_()
        except Exception as e:
            app_logger.error(f"Ошибка добавления объекта: {e}")
            report_error(e)

    def save_new_object(self, name, location, dialog):
        if name and location:
            try:
                session = Session()
                new_obj = Object(name=name, location=location)
                session.add(new_obj)
                session.commit()
                session.close()
                self.load_objects_to_table()
                dialog.close()
            except Exception as e:
                app_logger.error(f"Ошибка сохранения объекта: {e}")
                report_error(e)
        else:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")

    def edit_object(self, obj_id):
        try:
            from PyQt5.QtWidgets import QDialog, QDialogButtonBox
            session = Session()
            obj = session.query(Object).get(obj_id)
            if not obj:
                return

            dialog = QDialog(self)
            dialog.setWindowTitle("Редактировать объект")
            form = QFormLayout(dialog)

            name_input = QLineEdit(obj.name)
            location_input = QLineEdit(obj.location)

            form.addRow("Название:", name_input)
            form.addRow("Местоположение:", location_input)

            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(lambda: self.update_object(obj_id, name_input.text(), location_input.text(), dialog))
            buttons.rejected.connect(dialog.close)
            form.addRow(buttons)

            dialog.exec_()
            session.close()
        except Exception as e:
            app_logger.error(f"Ошибка редактирования объекта: {e}")
            report_error(e)

    def update_object(self, obj_id, name, location, dialog):
        try:
            session = Session()
            obj = session.query(Object).get(obj_id)
            if obj:
                obj.name = name
                obj.location = location
                session.commit()
                self.load_objects_to_table()
            session.close()
            dialog.close()
        except Exception as e:
            app_logger.error(f"Ошибка обновления объекта: {e}")
            report_error(e)

    def delete_object(self, obj_id):
        reply = QMessageBox.question(self, "Удалить", "Вы уверены?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                session = Session()
                obj = session.query(Object).get(obj_id)
                if obj:
                    session.delete(obj)
                    session.commit()
                    self.load_objects_to_table()
                session.close()
            except Exception as e:
                app_logger.error(f"Ошибка удаления объекта: {e}")
                report_error(e)

    # ✅ Функция расчёта материалов
    def calculate_materials_for_current_object(self):
        try:
            selected = self.objects_table.currentRow()
            if selected >= 0:
                obj_id = int(self.objects_table.item(selected, 0).text())
                line_data = [
                    {'type_id': 1, 'length': 100.0, 'width': 0.15},
                    {'type_id': 2, 'length': 50.0, 'width': 0.2}
                ]
                total = calculate_materials_for_object(obj_id, line_data)
                QMessageBox.information(self, "Расход", f"Общий расход: {total:.2f} ед.")
        except Exception as e:
            app_logger.error(f"Ошибка расчёта материалов: {e}")
            report_error(e)

    # === СТРАНИЦА: Материалы ===
    def create_materials_page(self):
        layout = QVBoxLayout()

        # Фильтр
        filter_layout = QHBoxLayout()
        self.mat_filter_input = QLineEdit()
        self.mat_filter_input.setPlaceholderText("Фильтр по названию...")
        self.mat_filter_input.textChanged.connect(self.filter_materials)
        filter_layout.addWidget(QLabel("Фильтр:"))
        filter_layout.addWidget(self.mat_filter_input)

        layout.addLayout(filter_layout)

        # Таблица
        self.materials_table = QTableWidget(0, 6)  # +1 столбец "Остаток"
        self.materials_table.setHorizontalHeaderLabels(["ID", "Название", "Ед. изм.", "Норма", "Остаток", "Действия"])
        header = self.materials_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.load_materials_to_table()

        layout.addWidget(self.materials_table)

        # ✅ Кнопка "Отправить уведомление"
        btn_notify = QPushButton("Отправить уведомление")
        btn_notify.clicked.connect(self.send_notification)
        layout.addWidget(btn_notify)

        btn_add = QPushButton("Добавить материал")
        btn_add.clicked.connect(self.add_material)
        layout.addWidget(btn_add)

        page = QWidget()
        page.setLayout(layout)
        return page

    def load_materials_to_table(self):
        try:
            session = Session()
            materials = session.query(Material).all()
            self.materials_table.setRowCount(len(materials))
            for i, mat in enumerate(materials):
                self.materials_table.setItem(i, 0, QTableWidgetItem(str(mat.id)))
                self.materials_table.setItem(i, 1, QTableWidgetItem(mat.name))
                self.materials_table.setItem(i, 2, QTableWidgetItem(mat.unit))
                self.materials_table.setItem(i, 3, QTableWidgetItem(str(mat.norm)))
                self.materials_table.setItem(i, 4, QTableWidgetItem(str(getattr(mat, 'current_stock', 0))))

                # Кнопки "Редактировать", "Удалить"
                btn_layout = QHBoxLayout()
                btn_edit = QPushButton("Редактировать")
                btn_edit.clicked.connect(lambda _, id=mat.id: self.edit_material(id))
                btn_delete = QPushButton("Удалить")
                btn_delete.clicked.connect(lambda _, id=mat.id: self.delete_material(id))

                btn_widget = QWidget()
                btn_widget.setLayout(btn_layout)
                btn_layout.addWidget(btn_edit)
                btn_layout.addWidget(btn_delete)
                btn_layout.setContentsMargins(4, 2, 4, 2)
                self.materials_table.setCellWidget(i, 5, btn_widget)

            session.close()
            self.check_low_materials()
        except Exception as e:
            app_logger.error(f"Ошибка загрузки материалов: {e}")
            report_error(e)

    def filter_materials(self):
        text = self.mat_filter_input.text().lower()
        for row in range(self.materials_table.rowCount()):
            item = self.materials_table.item(row, 1)  # Название
            visible = text in item.text().lower() if item else False
            self.materials_table.setRowHidden(row, not visible)

    def add_material(self):
        try:
            from PyQt5.QtWidgets import QDialog, QDialogButtonBox
            dialog = QDialog(self)
            dialog.setWindowTitle("Добавить материал")
            form = QFormLayout(dialog)

            name_input = QLineEdit()
            unit_input = QLineEdit()
            norm_input = QLineEdit()

            form.addRow("Название:", name_input)
            form.addRow("Ед. изм.:", unit_input)
            form.addRow("Норма (ГОСТ):", norm_input)

            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(lambda: self.save_new_material(
                name_input.text(), unit_input.text(), float(norm_input.text()), dialog))
            buttons.rejected.connect(dialog.close)
            form.addRow(buttons)

            dialog.exec_()
        except Exception as e:
            app_logger.error(f"Ошибка добавления материала: {e}")
            report_error(e)

    def save_new_material(self, name, unit, norm, dialog):
        if name and unit and norm:
            try:
                session = Session()
                new_mat = Material(name=name, unit=unit, norm=norm)
                session.add(new_mat)
                session.commit()
                session.close()
                self.load_materials_to_table()
                dialog.close()
            except Exception as e:
                app_logger.error(f"Ошибка сохранения материала: {e}")
                report_error(e)
        else:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")

    def edit_material(self, mat_id):
        try:
            from PyQt5.QtWidgets import QDialog, QDialogButtonBox
            session = Session()
            mat = session.query(Material).get(mat_id)
            if not mat:
                return

            dialog = QDialog(self)
            dialog.setWindowTitle("Редактировать материал")
            form = QFormLayout(dialog)

            name_input = QLineEdit(mat.name)
            unit_input = QLineEdit(mat.unit)
            norm_input = QLineEdit(str(mat.norm))

            form.addRow("Название:", name_input)
            form.addRow("Ед. изм.:", unit_input)
            form.addRow("Норма (ГОСТ):", norm_input)

            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(lambda: self.update_material(mat_id, name_input.text(), unit_input.text(), float(norm_input.text()), dialog))
            buttons.rejected.connect(dialog.close)
            form.addRow(buttons)

            dialog.exec_()
            session.close()
        except Exception as e:
            app_logger.error(f"Ошибка редактирования материала: {e}")
            report_error(e)

    def update_material(self, mat_id, name, unit, norm, dialog):
        try:
            session = Session()
            mat = session.query(Material).get(mat_id)
            if mat:
                mat.name = name
                mat.unit = unit
                mat.norm = norm
                session.commit()
                self.load_materials_to_table()
            session.close()
            dialog.close()
        except Exception as e:
            app_logger.error(f"Ошибка обновления материала: {e}")
            report_error(e)

    def delete_material(self, mat_id):
        reply = QMessageBox.question(self, "Удалить", "Вы уверены?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                session = Session()
                mat = session.query(Material).get(mat_id)
                if mat:
                    session.delete(mat)
                    session.commit()
                    self.load_materials_to_table()
                session.close()
            except Exception as e:
                app_logger.error(f"Ошибка удаления материала: {e}")
                report_error(e)

    # ✅ Проверка нехватки материалов
    def check_low_materials(self):
        try:
            session = Session()
            materials = session.query(Material).all()
            for mat in materials:
                current_stock = getattr(mat, 'current_stock', 0)
                if current_stock < mat.norm * 0.1:
                    notify_manager_low_material(mat.name, mat.norm - current_stock)
            session.close()
        except Exception as e:
            app_logger.error(f"Ошибка проверки нехватки материалов: {e}")
            report_error(e)

    # ✅ Отправка уведомления
    def send_notification(self):
        try:
            send_telegram_message("Уведомление: проверьте остатки материалов.")
            QMessageBox.information(self, "Уведомление", "Сообщение отправлено в Telegram.")
        except Exception as e:
            app_logger.error(f"Ошибка отправки уведомления: {e}")
            report_error(e)

    # === СТРАНИЦА: Топливные карты ===
    def create_fuel_cards_page(self):
        layout = QVBoxLayout()
        label = QLabel("Топливные карты")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.fuel_card_input = QLineEdit()
        self.fuel_card_input.setPlaceholderText("Введите ID карты...")
        layout.addWidget(self.fuel_card_input)

        btn_load_balance = QPushButton("Загрузить баланс")
        btn_load_balance.clicked.connect(self.load_fuel_balance)
        layout.addWidget(btn_load_balance)

        self.fuel_balance_label = QLabel("Баланс: —")
        layout.addWidget(self.fuel_balance_label)

        btn_load_transactions = QPushButton("Загрузить транзакции")
        btn_load_transactions.clicked.connect(self.load_fuel_transactions)
        layout.addWidget(btn_load_transactions)

        self.fuel_transactions_table = QTableWidget(0, 3)
        self.fuel_transactions_table.setHorizontalHeaderLabels(["Дата", "Сумма", "Место"])
        layout.addWidget(self.fuel_transactions_table)

        page = QWidget()
        page.setLayout(layout)
        return page

    def load_fuel_balance(self):
        try:
            card_id = self.fuel_card_input.text()
            if card_id:
                balance = get_fuel_balance(card_id)
                self.fuel_balance_label.setText(f"Баланс: {balance} руб.")
        except Exception as e:
            app_logger.error(f"Ошибка загрузки баланса: {e}")
            report_error(e)

    def load_fuel_transactions(self):
        try:
            card_id = self.fuel_card_input.text()
            if card_id:
                transactions = get_fuel_transactions(card_id)
                self.fuel_transactions_table.setRowCount(len(transactions))
                for i, t in enumerate(transactions):
                    self.fuel_transactions_table.setItem(i, 0, QTableWidgetItem(t.get('date', '')))
                    self.fuel_transactions_table.setItem(i, 1, QTableWidgetItem(str(t.get('amount', 0))))
                    self.fuel_transactions_table.setItem(i, 2, QTableWidgetItem(t.get('location', '')))
        except Exception as e:
            app_logger.error(f"Ошибка загрузки транзакций: {e}")
            report_error(e)

    # === СТРАНИЦА: Калькулятор ===
    def create_calculator_page(self):
        layout = QVBoxLayout()
        label = QLabel("Калькулятор расхода материалов")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Форма для расчёта
        form = QFormLayout()

        self.calc_material_input = QLineEdit()
        self.calc_length_input = QLineEdit()
        self.calc_width_input = QLineEdit()

        form.addRow("Материал:", self.calc_material_input)
        form.addRow("Длина (м):", self.calc_length_input)
        form.addRow("Ширина (м):", self.calc_width_input)

        layout.addLayout(form)

        btn_calc = QPushButton("Рассчитать")
        btn_calc.clicked.connect(self.calculate_single_material)
        layout.addWidget(btn_calc)

        self.calc_result_label = QLabel("Результат: —")
        layout.addWidget(self.calc_result_label)

        page = QWidget()
        page.setLayout(layout)
        return page

    def calculate_single_material(self):
        try:
            material_name = self.calc_material_input.text()
            try:
                length = float(self.calc_length_input.text())
                width = float(self.calc_width_input.text())
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Введите корректные числовые значения.")
                return

            from core.calc_engine import calculate_materials_with_gost
            result = calculate_materials_with_gost(material_name, length, width)
            self.calc_result_label.setText(f"Результат: {result:.2f} ед.")
        except Exception as e:
            app_logger.error(f"Ошибка расчёта в калькуляторе: {e}")
            report_error(e)

    # === СТРАНИЦА: Отчёты ===
    def create_reports_page(self):
        layout = QVBoxLayout()
        label = QLabel("Отчёты")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        btn_gen_report = QPushButton("Сгенерировать отчёт по материалам (PDF)")
        btn_gen_report.clicked.connect(self.generate_materials_report)
        layout.addWidget(btn_gen_report)

        page = QWidget()
        page.setLayout(layout)
        return page

    def generate_materials_report(self):
        try:
            from PyQt5.QtWidgets import QFileDialog
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить отчёт", "", "PDF Files (*.pdf)")
            if file_path:
                generate_materials_report(file_path)
                QMessageBox.information(self, "Отчёт", f"Отчёт сохранён: {file_path}")
        except Exception as e:
            app_logger.error(f"Ошибка генерации отчёта: {e}")
            report_error(e)

    # === СТРАНИЦА: Документы ===
    def create_documents_page(self):
        layout = QVBoxLayout()

        # Фильтр
        filter_layout = QHBoxLayout()
        self.doc_filter_input = QLineEdit()
        self.doc_filter_input.setPlaceholderText("Фильтр по типу...")
        self.doc_filter_input.textChanged.connect(self.filter_documents)
        filter_layout.addWidget(QLabel("Фильтр:"))
        filter_layout.addWidget(self.doc_filter_input)

        layout.addLayout(filter_layout)

        # Таблица
        self.documents_table = QTableWidget(0, 5)
        self.documents_table.setHorizontalHeaderLabels(["ID", "Объект", "Тип", "Дата", "Действия"])
        header = self.documents_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.load_documents_to_table()

        layout.addWidget(self.documents_table)

        btn_upload = QPushButton("Загрузить документ")
        btn_upload.clicked.connect(self.upload_document)
        layout.addWidget(btn_upload)

        page = QWidget()
        page.setLayout(layout)
        return page

    def load_documents_to_table(self):
        try:
            session = Session()
            documents = session.query(Document).all()
            self.documents_table.setRowCount(len(documents))
            for i, doc in enumerate(documents):
                self.documents_table.setItem(i, 0, QTableWidgetItem(str(doc.id)))
                self.documents_table.setItem(i, 1, QTableWidgetItem(str(doc.object_id)))
                self.documents_table.setItem(i, 2, QTableWidgetItem(doc.type))
                self.documents_table.setItem(i, 3, QTableWidgetItem(str(doc.created_at)))

                # Кнопки "Редактировать", "Удалить"
                btn_layout = QHBoxLayout()
                btn_edit = QPushButton("Редактировать")
                btn_edit.clicked.connect(lambda _, id=doc.id: self.edit_document(id))
                btn_delete = QPushButton("Удалить")
                btn_delete.clicked.connect(lambda _, id=doc.id: self.delete_document(id))

                btn_widget = QWidget()
                btn_widget.setLayout(btn_layout)
                btn_layout.addWidget(btn_edit)
                btn_layout.addWidget(btn_delete)
                btn_layout.setContentsMargins(4, 2, 4, 2)
                self.documents_table.setCellWidget(i, 4, btn_widget)

            session.close()
        except Exception as e:
            app_logger.error(f"Ошибка загрузки документов: {e}")
            report_error(e)

    def filter_documents(self):
        text = self.doc_filter_input.text().lower()
        for row in range(self.documents_table.rowCount()):
            item = self.documents_table.item(row, 2)  # Тип
            visible = text in item.text().lower() if item else False
            self.documents_table.setRowHidden(row, not visible)

    def upload_document(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Выберите документ", "", "PDF Files (*.pdf);;All Files (*)")
            if file_path:
                QMessageBox.information(self, "Успешно", f"Документ {file_path} загружен.")
        except Exception as e:
            app_logger.error(f"Ошибка загрузки документа: {e}")
            report_error(e)

    def edit_document(self, doc_id):
        try:
            QMessageBox.information(self, "Редактирование", f"Редактирование документа ID: {doc_id}")
        except Exception as e:
            app_logger.error(f"Ошибка редактирования документа: {e}")
            report_error(e)

    def delete_document(self, doc_id):
        reply = QMessageBox.question(self, "Удалить", "Вы уверены?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                session = Session()
                doc = session.query(Document).get(doc_id)
                if doc:
                    session.delete(doc)
                    session.commit()
                    self.load_documents_to_table()
                session.close()
            except Exception as e:
                app_logger.error(f"Ошибка удаления документа: {e}")
                report_error(e)

    # === СТРАНИЦА: ГПР ===
    def create_gpr_page(self):
        layout = QVBoxLayout()
        label = QLabel("ГПР — План/факт объёмы")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        btn_load = QPushButton("Загрузить данные из ГПР")
        btn_load.clicked.connect(self.load_gpr_data)
        layout.addWidget(btn_load)

        self.gpr_table = QTableWidget(0, 4)
        self.gpr_table.setHorizontalHeaderLabels(["Объект", "План", "Факт", "% выполнения"])
        layout.addWidget(self.gpr_table)

        page = QWidget()
        page.setLayout(layout)
        return page

    def load_gpr_data(self):
        try:
            data = get_gpr_data()
            self.gpr_table.setRowCount(len(data))
            for i, item in enumerate(data):
                self.gpr_table.setItem(i, 0, QTableWidgetItem(item['object']))
                self.gpr_table.setItem(i, 1, QTableWidgetItem(str(item['plan'])))
                self.gpr_table.setItem(i, 2, QTableWidgetItem(str(item['fact'])))
                completion = round((item['fact'] / item['plan']) * 100, 2) if item['plan'] != 0 else 0
                self.gpr_table.setItem(i, 3, QTableWidgetItem(f"{completion}%"))
        except Exception as e:
            app_logger.error(f"Ошибка загрузки ГПР: {e}")
            report_error(e)

    # === СТРАНИЦА: Графики ===
    def create_charts_page(self):
        layout = QVBoxLayout()
        label = QLabel("Аналитика и графики")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.chart_widget = MatplotlibWidget()
        layout.addWidget(self.chart_widget)

        btn_refresh = QPushButton("Обновить график")
        btn_refresh.clicked.connect(self.update_chart)
        layout.addWidget(btn_refresh)

        page = QWidget()
        page.setLayout(layout)
        return page

    def update_chart(self):
        try:
            self.chart_widget.update_plot()
        except Exception as e:
            app_logger.error(f"Ошибка обновления графика: {e}")
            report_error(e)

    # === СТРАНИЦА: Настройки ===
    def create_settings_page(self):
        layout = QVBoxLayout()
        label = QLabel("Настройки")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Тип БД
        from config.database_config import USE_SQLITE
        if USE_SQLITE:
            db_label = QLabel("Тип БД: SQLite (автономная версия)")
        else:
            db_label = QLabel("Тип БД: MySQL (серверная версия)")
        layout.addWidget(db_label)

        # ✅ Кнопка резервного копирования
        btn_backup = QPushButton("Создать резервную копию БД")
        btn_backup.clicked.connect(self.create_backup)
        layout.addWidget(btn_backup)

        # ✅ Кнопка проверки обновлений
        btn_update = QPushButton("Проверить обновления")
        btn_update.clicked.connect(update_app)
        layout.addWidget(btn_update)

        # ✅ Кнопка автозапуска
        btn_autostart = QPushButton("Добавить в автозапуск")
        btn_autostart.clicked.connect(add_to_startup)
        layout.addWidget(btn_autostart)

        btn_remove_autostart = QPushButton("Убрать из автозапуска")
        btn_remove_autostart.clicked.connect(remove_from_startup)
        layout.addWidget(btn_remove_autostart)

        page = QWidget()
        page.setLayout(layout)
        return page

    def create_backup(self):
        try:
            from PyQt5.QtWidgets import QFileDialog
            from database.backup_manager import backup_database
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Сохранить резервную копию", f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip", "ZIP Files (*.zip)"
            )
            if file_path:
                backup_database(file_path)
        except Exception as e:
            app_logger.error(f"Ошибка резервного копирования: {e}")
            report_error(e)


# === Виджет для matplotlib ===
class MatplotlibWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.update_plot()

    def update_plot(self):
        try:
            ax = self.figure.add_subplot(111)
            ax.clear()
            x = [1, 2, 3, 4, 5]
            y = [10, 15, 13, 17, 20]
            ax.plot(x, y, label="Объёмы")
            ax.set_title("График выполненных работ")
            ax.legend()
            self.canvas.draw()
        except Exception as e:
            app_logger.error(f"Ошибка отрисовки графика: {e}")
            report_error(e)


# === Запуск приложения ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())