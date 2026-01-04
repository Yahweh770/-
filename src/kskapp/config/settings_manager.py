from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import json
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QCheckBox, QMessageBox, QLabel
)

SETTINGS_FILE = "settings.json"

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        label = QLabel("Настройки приложения")
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

        self.form = QFormLayout()

        # Поля настроек
        self.telegram_token_input = QLineEdit()
        self.telegram_chat_id_input = QLineEdit()
        self.use_sqlite_checkbox = QCheckBox("Использовать SQLite (автономная версия)")
        self.enable_logging_checkbox = QCheckBox("Включить логирование")

        self.form.addRow("Telegram Bot Token:", self.telegram_token_input)
        self.form.addRow("Telegram Chat ID:", self.telegram_chat_id_input)
        self.form.addRow(self.use_sqlite_checkbox)
        self.form.addRow(self.enable_logging_checkbox)

        self.layout.addLayout(self.form)

        btn_save = QPushButton("Сохранить настройки")
        btn_save.clicked.connect(self.save_settings)
        self.layout.addWidget(btn_save)

        btn_load = QPushButton("Загрузить настройки")
        btn_load.clicked.connect(self.load_settings)
        self.layout.addWidget(btn_load)

        self.load_settings()

    def save_settings(self):
        settings = {
            "telegram_token": self.telegram_token_input.text(),
            "telegram_chat_id": self.telegram_chat_id_input.text(),
            "use_sqlite": self.use_sqlite_checkbox.isChecked(),
            "enable_logging": self.enable_logging_checkbox.isChecked(),
        }
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        QMessageBox.information(self, "Сохранено", "Настройки сохранены.")

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)
            self.telegram_token_input.setText(settings.get("telegram_token", ""))
            self.telegram_chat_id_input.setText(settings.get("telegram_chat_id", ""))
            self.use_sqlite_checkbox.setChecked(settings.get("use_sqlite", False))
            self.enable_logging_checkbox.setChecked(settings.get("enable_logging", True))
        else:
            QMessageBox.information(self, "Загрузка", "Файл настроек не найден, будут использованы значения по умолчанию.")