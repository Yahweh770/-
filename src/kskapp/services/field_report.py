from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
from fpdf import FPDF
from utils.offline_storage import load_field_data_offline

def generate_field_report_pdf(filepath):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Полевой отчёт по разметке", ln=True, align='C')

    data = load_field_data_offline()

    for record in data:
        pdf.cell(200, 10, txt=f"Объект: {record['object']}", ln=True)
        pdf.cell(200, 10, txt=f"Тип линии: {record['line_type']}", ln=True)
        pdf.cell(200, 10, txt=f"Длина: {record['length']} м", ln=True)
        pdf.cell(200, 10, txt=f"Ширина: {record['width']} м", ln=True)
        pdf.cell(200, 10, txt=f"Расход: {record['material_used']} кг", ln=True)
        pdf.cell(200, 10, txt=f"Дата: {record['date']}", ln=True)
        pdf.cell(200, 10, txt=f"Заметки: {record['notes']}", ln=True)
        pdf.ln(5)

    pdf.output(filepath)