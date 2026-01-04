from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)

class OfflineCalcWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        label = QLabel("Автономный калькулятор расхода")
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

        form = QFormLayout()

        self.material_input = QLineEdit()
        self.length_input = QLineEdit()
        self.width_input = QLineEdit()

        form.addRow("Материал (норма):", self.material_input)
        form.addRow("Длина (м):", self.length_input)
        form.addRow("Ширина (м):", self.width_input)

        self.layout.addLayout(form)

        btn_calc = QPushButton("Рассчитать")
        btn_calc.clicked.connect(self.calculate)
        self.layout.addWidget(btn_calc)

        self.result_label = QLabel("Результат: —")
        self.layout.addWidget(self.result_label)

    def calculate(self):
        try:
            material_name = self.material_input.text()
            length = float(self.length_input.text())
            width = float(self.width_input.text())

            # Пример нормы (в автономном режиме можно хранить в словаре)
            norms = {
                "Термопласт": 0.3,
                "Алкидная краска": 0.2
            }
            norm = norms.get(material_name, 0.0)
            result = length * width * norm

            self.result_label.setText(f"Результат: {result:.2f} кг")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректные числовые значения.")