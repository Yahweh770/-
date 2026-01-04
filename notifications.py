from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
from PyQt5.QtWidgets import QMessageBox
import smtplib
from email.mime.text import MimeText

def notify_manager_low_material(material_name, required_amount):
    msg = f"Уведомление: Необходимо заказать {material_name}, недостаёт {required_amount} ед."
    print(msg)  # Вместо этого можно отправить email или в телеграм
    QMessageBox.warning(None, "Нехватка материалов", msg)

def send_email_notification(to_email, subject, body):
    # Пример отправки email
    msg = MimeText(body)
    msg['Subject'] = subject
    msg['From'] = 'admin@company.com'
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('your_email@gmail.com', 'password')
            server.send_message(msg)
    except Exception as e:
        print(f"Ошибка отправки email: {e}")