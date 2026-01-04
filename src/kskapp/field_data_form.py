from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QDateEdit, QTextEdit, QFileDialog,
    QMessageBox
)
from datetime import datetime
from utils.offline_storage import save_field_data_offline  # ✅ Новый импорт
from core.excel_exporter import export_field_data_to_excel

class FieldDataForm(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        label = QLabel("Полевые данные (заполняется на объекте)")
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

        form = QFormLayout()

        # Объект (можно ввести вручную или выбрать из списка)
        self.object_input = QLineEdit()
        form.addRow("Объект:", self.object_input)

        # Тип линии
        self.line_type_input = QLineEdit()
        form.addRow("Тип линии:", self.line_type_input)

        # Длина, ширина
        self.length_input = QLineEdit()
        self.width_input = QLineEdit()
        form.addRow("Длина (м):", self.length_input)
        form.addRow("Ширина (м):", self.width_input)

        # Расход материала
        self.material_used_input = QLineEdit()
        form.addRow("Использовано материала (кг):", self.material_used_input)

        # Заметки
        self.notes_input = QTextEdit()
        form.addRow("Заметки:", self.notes_input)

        # Дата
        self.date_input = QDateEdit()
        self.date_input.setDate(datetime.now().date())
        form.addRow("Дата:", self.date_input)

        # Кнопка выбора фото
        btn_photo = QPushButton("Прикрепить фотоотчёт")
        btn_photo.clicked.connect(self.select_photo)
        form.addRow(btn_photo)

        self.photo_path = None

        self.layout.addLayout(form)

        btn_save = QPushButton("Сохранить данные (автономно)")
        btn_save.clicked.connect(self.save_data_offline)
        self.layout.addWidget(btn_save)

	btn_export = QPushButton("Экспорт в Excel")
	btn_export.clicked.connect(self.export_to_excel)
	self.layout.addWidget(btn_export)

    def select_photo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выбрать фото", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.photo_path = path
            QMessageBox.information(self, "Фото", f"Фото выбрано: {path}")

    def save_data_offline(self):
        try:
            obj_name = self.object_input.text()
            line_type = self.line_type_input.text()
            length = float(self.length_input.text())
            width = float(self.width_input.text())
            material_used = float(self.material_used_input.text())
            notes = self.notes_input.toPlainText()
            date = self.date_input.date().toPyDate()

            record = {
                "object": obj_name,
                "line_type": line_type,
                "length": length,
                "width": width,
                "material_used": material_used,
                "photo_path": self.photo_path,
                "date": date.isoformat(),
                "notes": notes
	def export_to_excel(self):
    	from PyQt5.QtWidgets import QFileDialog
    	file_path, _ = QFileDialog.getSaveFileName(self, "Экспортировать в Excel", "", "Excel Files (*.xlsx)")
    	if file_path:
        export_field_data_to_excel(file_path)
            }

            save_field_data_offline(record)
            QMessageBox.information(self, "Сохранено", "Данные успешно сохранены автономно.")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректные числовые значения.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить: {e}")