from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import traceback
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtWidgets import QMessageBox

def send_error_report(error_message, traceback_str):
    # Пример отправки на email
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"
    recipient_email = "admin@company.com"

    subject = "Отчёт об ошибке в приложении"
    body = f"""
    Ошибка: {error_message}
    Трассировка:
    {traceback_str}
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        QMessageBox.information(None, "Отчёт отправлен", "Отчёт об ошибке отправлен администратору.")
    except Exception as e:
        QMessageBox.critical(None, "Ошибка", f"Не удалось отправить отчёт: {e}")

def report_error(e):
    error_msg = str(e)
    tb_str = traceback.format_exc()
    send_error_report(error_msg, tb_str)