from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QFormLayout, QLineEdit, QDialog, QDialogButtonBox, QMessageBox
)
from strodservice.models.models import Contractor
from strodservice.database.init_db import SessionLocal

class ContractorForm(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        label = QLabel("Субподрядчики")
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "ИНН", "Действия"])
        self.load_contractors()

        self.layout.addWidget(self.table)

        btn_add = QPushButton("Добавить субподрядчика")
        btn_add.clicked.connect(self.add_contractor)
        self.layout.addWidget(btn_add)

    def load_contractors(self):
        session = SessionLocal()
        contractors = session.query(Contractor).all()
        self.table.setRowCount(len(contractors))
        for i, c in enumerate(contractors):
            self.table.setItem(i, 0, QTableWidgetItem(str(c.id)))
            self.table.setItem(i, 1, QTableWidgetItem(c.name))
            self.table.setItem(i, 2, QTableWidgetItem(c.inn))

            btn_layout = QHBoxLayout()
            btn_edit = QPushButton("Редактировать")
            btn_edit.clicked.connect(lambda _, id=c.id: self.edit_contractor(id))
            btn_delete = QPushButton("Удалить")
            btn_delete.clicked.connect(lambda _, id=c.id: self.delete_contractor(id))

            btn_widget = QWidget()
            btn_widget.setLayout(btn_layout)
            btn_layout.addWidget(btn_edit)
            btn_layout.addWidget(btn_delete)
            btn_layout.setContentsMargins(4, 2, 4, 2)
            self.table.setCellWidget(i, 3, btn_widget)

        session.close()

    def add_contractor(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить субподрядчика")
        form = QFormLayout(dialog)

        name_input = QLineEdit()
        inn_input = QLineEdit()

        form.addRow("Название:", name_input)
        form.addRow("ИНН:", inn_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.save_contractor(name_input.text(), inn_input.text(), dialog))
        buttons.rejected.connect(dialog.close)
        form.addRow(buttons)

        dialog.exec_()

    def save_contractor(self, name, inn, dialog):
        if name and inn:
            session = SessionLocal()
            new_contractor = Contractor(name=name, inn=inn)
            session.add(new_contractor)
            session.commit()
            session.close()
            self.load_contractors()
            dialog.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")

    def edit_contractor(self, id):
        session = SessionLocal()
        contractor = session.query(Contractor).get(id)
        if not contractor:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Редактировать субподрядчика")
        form = QFormLayout(dialog)

        name_input = QLineEdit(contractor.name)
        inn_input = QLineEdit(contractor.inn)

        form.addRow("Название:", name_input)
        form.addRow("ИНН:", inn_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.update_contractor(id, name_input.text(), inn_input.text(), dialog))
        buttons.rejected.connect(dialog.close)
        form.addRow(buttons)

        dialog.exec_()
        session.close()

    def update_contractor(self, id, name, inn, dialog):
        session = SessionLocal()
        contractor = session.query(Contractor).get(id)
        if contractor:
            contractor.name = name
            contractor.inn = inn
            session.commit()
            self.load_contractors()
        session.close()
        dialog.close()

    def delete_contractor(self, id):
        reply = QMessageBox.question(self, "Удалить", "Вы уверены?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            session = SessionLocal()
            contractor = session.query(Contractor).get(id)
            if contractor:
                session.delete(contractor)
                session.commit()
                self.load_contractors()
            session.close()