from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
from fpdf import FPDF
from database.models import Material
from database.init_db import Session

def generate_materials_report(filepath):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Отчёт по материалам", ln=True, align='C')

    session = Session()
    materials = session.query(Material).all()
    for mat in materials:
        pdf.cell(200, 10, txt=f"{mat.name} — {mat.current_stock} ед.", ln=True)

    pdf.output(filepath)
    session.close()